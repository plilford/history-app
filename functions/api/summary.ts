// Cloudflare Pages Function — POST /api/summary
//
// Generates a streamed, Claude-written narrative of the time window the user is
// currently looking at on the Ever-When timeline, plus a curated tail of
// resources and a few Wikipedia image candidates.
//
// Access: editor-only for now. The request must carry the caller's Supabase
// JWT in the Authorization header; we verify it and check the email against the
// editor allowlist before spending anything on the model.
//
// Billing seam (one code path, three modes):
//   (a) owner-funded  — uses env.ANTHROPIC_API_KEY  [shipping now]
//   (b) metered/paid  — see the `// TODO: metering/quota` marker
//   (c) bring-your-own — body.userApiKey, used transiently, never stored
//
// Streaming protocol (newline-delimited SSE, each frame a single JSON line):
//   data: {"t":"text","v":"<markdown chunk>"}
//   data: {"t":"meta","resources":[...],"images":[...]}
//   data: {"t":"error","message":"..."}
//   data: {"t":"done"}

import { createClient, type SupabaseClient } from "@supabase/supabase-js";
import { createRemoteJWKSet, jwtVerify } from "jose";

interface Env {
  ANTHROPIC_API_KEY?: string;
  EDITOR_EMAIL?: string;
  SUPABASE_URL?: string;
  SUPABASE_ANON_KEY?: string;
  VITE_SUPABASE_URL?: string;
  VITE_SUPABASE_ANON_KEY?: string;
}

// Sonnet 4.6. If the API rejects this id, change it here (single source of
// truth) — Anthropic occasionally pins dated suffixes.
const SUMMARY_MODEL = "claude-sonnet-4-6";
const ANTHROPIC_VERSION = "2023-06-01";
const MAX_TOKENS = 1200;
const DEFAULT_EDITOR_EMAIL = "p.lilford@gmail.com";

// Verify the Supabase access token locally against the project's JWKS (the
// project uses ES256 asymmetric signing keys). This avoids GoTrue's /user
// endpoint, which internal-errors on this project, and is faster (JWKS is
// cached after the first fetch). The JWKSet is created lazily and memoised
// across requests per Supabase URL.
let jwksCache: ReturnType<typeof createRemoteJWKSet> | null = null;
let jwksFor = "";
function getJwks(supabaseUrl: string) {
  if (!jwksCache || jwksFor !== supabaseUrl) {
    jwksFor = supabaseUrl;
    jwksCache = createRemoteJWKSet(
      new URL(`${supabaseUrl}/auth/v1/.well-known/jwks.json`),
    );
  }
  return jwksCache;
}

type CompactOccurrence = {
  id: number;
  title: string;
  startYear: number | null;
  endYear: number | null;
  type: "event" | "person" | "art" | "resource";
  priority: number;
};

interface SummaryRequest {
  window: { startYear: number; endYear: number };
  timelines: Array<{ slug: string; name: string }>;
  viewState?: { showLifespans?: boolean; rollupLevel?: number; regionWeighted?: boolean };
  showing: CompactOccurrence[];
  userApiKey?: string | null;
}

type OccRow = {
  id: number;
  title: string;
  start_year: number | null;
  end_year: number | null;
  occurrence_type: string;
  is_period?: boolean;
  main_priority?: number | null;
  wikipedia_link?: string | null;
};

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });
}

function bce(year: number): string {
  return year < 0 ? `${Math.abs(Math.round(year))} BCE` : `${Math.round(year)} CE`;
}

function occLine(o: { title: string; type?: string; start_year: number | null; end_year: number | null }): string {
  const s = o.start_year;
  const e = o.end_year;
  const span =
    s == null ? "" : e != null && e !== s ? ` (${bce(s)}–${bce(e)})` : ` (${bce(s)})`;
  const t = o.type && o.type !== "event" ? `${o.type}, ` : "";
  return `- ${o.title}${span}${t ? ` [${t.trim().replace(/,$/, "")}]` : ""}`;
}

export const onRequestPost = async (context: {
  request: Request;
  env: Env;
}): Promise<Response> => {
  const { request, env } = context;

  let body: SummaryRequest;
  try {
    body = (await request.json()) as SummaryRequest;
  } catch {
    return json({ error: "invalid_json" }, 400);
  }
  if (!body || !body.window || !Array.isArray(body.showing) || !Array.isArray(body.timelines)) {
    return json({ error: "bad_request" }, 400);
  }

  const supabaseUrl = env.SUPABASE_URL ?? env.VITE_SUPABASE_URL;
  const supabaseAnon = env.SUPABASE_ANON_KEY ?? env.VITE_SUPABASE_ANON_KEY;
  if (!supabaseUrl || !supabaseAnon) {
    return json({ error: "server_misconfigured", detail: "supabase env missing" }, 500);
  }

  // ---- Auth: verify JWT + editor allowlist --------------------------------
  const authHeader = request.headers.get("Authorization") ?? "";
  const token = authHeader.startsWith("Bearer ") ? authHeader.slice(7) : "";
  if (!token) return json({ error: "unauthorized" }, 401);

  const sb: SupabaseClient = createClient(supabaseUrl, supabaseAnon, {
    auth: { persistSession: false, autoRefreshToken: false },
  });

  let email = "";
  try {
    const { payload } = await jwtVerify(token, getJwks(supabaseUrl));
    email = String(payload.email ?? "");
  } catch (e) {
    return json({ error: "unauthorized", detail: (e as Error)?.message ?? "jwt verify failed" }, 401);
  }
  const editorEmail = env.EDITOR_EMAIL ?? DEFAULT_EDITOR_EMAIL;
  if (email.toLowerCase() !== editorEmail.toLowerCase()) {
    return json({ error: "forbidden" }, 403);
  }

  // ---- Resolve API key (billing seam) -------------------------------------
  const apiKey = body.userApiKey || env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    return json({ error: "server_misconfigured", detail: "ANTHROPIC_API_KEY missing" }, 500);
  }
  // TODO: metering/quota — for a future paid tier, check this user's usage
  // against a quota here (and write to ai_summary_usage at message_stop).

  const startYear = Math.round(body.window.startYear);
  const endYear = Math.round(body.window.endYear);
  const currentYear = new Date().getUTCFullYear();
  const showing = body.showing.slice(0, 80);
  const showingIds = new Set(showing.map((s) => s.id));

  // ---- Gather context server-side -----------------------------------------
  const context_ = await gatherContext(sb, body.timelines, startYear, endYear, currentYear, showingIds);

  // ---- Build the Claude prompt --------------------------------------------
  const systemText = buildSystemPrompt();
  const userText = buildUserMessage(body, startYear, endYear, context_);

  // ---- Call Anthropic (streaming) and pipe to the client ------------------
  let upstream: Response;
  try {
    upstream = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "x-api-key": apiKey,
        "anthropic-version": ANTHROPIC_VERSION,
        "content-type": "application/json",
      },
      body: JSON.stringify({
        model: SUMMARY_MODEL,
        max_tokens: MAX_TOKENS,
        system: [{ type: "text", text: systemText, cache_control: { type: "ephemeral" } }],
        messages: [{ role: "user", content: userText }],
        stream: true,
      }),
    });
  } catch (e) {
    return json({ error: "upstream_unreachable", detail: String(e) }, 502);
  }

  if (!upstream.ok || !upstream.body) {
    const detail = await upstream.text().catch(() => "");
    return json({ error: "upstream_error", status: upstream.status, detail }, 502);
  }

  const encoder = new TextEncoder();
  const decoder = new TextDecoder();
  const { readable, writable } = new TransformStream();
  const writer = writable.getWriter();

  const sendFrame = (obj: unknown) =>
    writer.write(encoder.encode(`data: ${JSON.stringify(obj)}\n\n`));

  (async () => {
    try {
      const reader = upstream.body!.getReader();
      let buf = "";
      for (;;) {
        const { value, done } = await reader.read();
        if (done) break;
        buf += decoder.decode(value, { stream: true });
        // SSE frames are separated by a blank line.
        let sep: number;
        while ((sep = buf.indexOf("\n\n")) !== -1) {
          const frame = buf.slice(0, sep);
          buf = buf.slice(sep + 2);
          for (const line of frame.split("\n")) {
            if (!line.startsWith("data:")) continue;
            const payload = line.slice(5).trim();
            if (!payload || payload === "[DONE]") continue;
            let evt: any;
            try {
              evt = JSON.parse(payload);
            } catch {
              continue;
            }
            if (evt.type === "content_block_delta" && evt.delta?.type === "text_delta") {
              await sendFrame({ t: "text", v: evt.delta.text });
            }
          }
        }
      }
      // Curated tail.
      await sendFrame({ t: "meta", resources: context_.resources, images: context_.images });
      await sendFrame({ t: "done" });
    } catch (e) {
      try {
        await sendFrame({ t: "error", message: String(e) });
      } catch { /* writer already closed */ }
    } finally {
      try { await writer.close(); } catch { /* already closed */ }
    }
  })();

  return new Response(readable, {
    headers: {
      "content-type": "text/event-stream; charset=utf-8",
      "cache-control": "no-cache, no-transform",
      connection: "keep-alive",
    },
  });
};

// ---------------------------------------------------------------------------

async function gatherContext(
  sb: SupabaseClient,
  timelines: Array<{ slug: string; name: string }>,
  startYear: number,
  endYear: number,
  currentYear: number,
  showingIds: Set<number>,
) {
  const slugs = timelines.map((t) => t.slug);
  const { data: tlRows } = await sb
    .from("timelines")
    .select("id, slug, is_resource_timeline")
    .in("slug", slugs);
  const nonResourceTimelineIds = (tlRows ?? [])
    .filter((t: any) => !t.is_resource_timeline)
    .map((t: any) => t.id as number);

  // (1) High-priority occurrences within the window, on the selected
  //     (non-resource) timelines, that AREN'T already on screen.
  let contextRows: OccRow[] = [];
  if (nonResourceTimelineIds.length > 0) {
    const { data } = await sb
      .from("occurrence_timeline_priorities")
      .select("priority, occurrences!inner(id,title,start_year,end_year,occurrence_type,wikipedia_link)")
      .in("timeline_id", nonResourceTimelineIds)
      .neq("occurrences.occurrence_type", "resource")
      .lte("occurrences.start_year", endYear)
      .order("priority", { ascending: false })
      .limit(120);
    const byId = new Map<number, OccRow & { priority: number }>();
    for (const r of (data ?? []) as any[]) {
      const o = r.occurrences;
      if (!o) continue;
      const ey = o.end_year ?? currentYear;
      if (ey < startYear) continue; // doesn't overlap the window
      if (showingIds.has(o.id)) continue; // already visible
      const prev = byId.get(o.id);
      if (!prev || r.priority > prev.priority) byId.set(o.id, { ...o, priority: r.priority });
    }
    contextRows = [...byId.values()].sort((a: any, b: any) => b.priority - a.priority).slice(0, 15);
  }

  // (2) Umbrella periods that CONTAIN the window — even if not on any selected
  //     timeline (e.g. "you're inside the Hundred Years' War").
  const { data: umbData } = await sb
    .from("occurrences")
    .select("id,title,start_year,end_year,occurrence_type,is_period,main_priority")
    .eq("is_period", true)
    .lte("start_year", startYear)
    .order("main_priority", { ascending: false, nullsFirst: false })
    .limit(40);
  const umbrellas = ((umbData ?? []) as OccRow[])
    .filter((o) => (o.end_year ?? currentYear) >= endYear)
    .filter((o) => !showingIds.has(o.id))
    .slice(0, 8);

  // (3) Before / after anchors — high-notability reference points outside the
  //     window on each side.
  const [{ data: beforeData }, { data: afterData }] = await Promise.all([
    sb.from("occurrences")
      .select("id,title,start_year,end_year,occurrence_type,main_priority")
      .lt("start_year", startYear)
      .order("main_priority", { ascending: false, nullsFirst: false })
      .limit(4),
    sb.from("occurrences")
      .select("id,title,start_year,end_year,occurrence_type,main_priority")
      .gt("start_year", endYear)
      .order("main_priority", { ascending: false, nullsFirst: false })
      .limit(4),
  ]);
  const before = ((beforeData ?? []) as OccRow[]).filter((o) => !showingIds.has(o.id));
  const after = ((afterData ?? []) as OccRow[]).filter((o) => !showingIds.has(o.id));

  // (4) Resources covering the window — tagged to any in-window subject.
  const subjectIds = [
    ...showingIds,
    ...contextRows.map((o) => o.id),
    ...umbrellas.map((o) => o.id),
  ];
  let resources: Array<{ id: number; title: string; link: string | null; subtype: string | null }> = [];
  if (subjectIds.length > 0) {
    const { data: tagRows } = await sb
      .from("resource_tags")
      .select("resource_id")
      .in("subject_id", subjectIds.slice(0, 200));
    const resourceIds = [...new Set((tagRows ?? []).map((r: any) => r.resource_id as number))];
    if (resourceIds.length > 0) {
      const { data: resRows } = await sb
        .from("occurrences")
        .select("id,title,resource_link,resource_subtype,main_priority")
        .in("id", resourceIds.slice(0, 60))
        .eq("occurrence_type", "resource")
        .order("main_priority", { ascending: false, nullsFirst: false })
        .limit(8);
      resources = ((resRows ?? []) as any[]).map((r) => ({
        id: r.id,
        title: r.title,
        link: r.resource_link ?? null,
        subtype: r.resource_subtype ?? null,
      }));
    }
  }

  // (5) Image candidates — Wikipedia-linked occurrences, preferring what's on
  //     screen. The client resolves thumbnails and shows the first few.
  const topShowingIds = [...showingIds].slice(0, 12);
  let showingWiki: OccRow[] = [];
  if (topShowingIds.length > 0) {
    const { data } = await sb
      .from("occurrences")
      .select("id,title,start_year,end_year,occurrence_type,wikipedia_link")
      .in("id", topShowingIds);
    showingWiki = (data ?? []) as OccRow[];
  }
  const imageSeen = new Set<number>();
  const images: Array<{ id: number; title: string; wikipedia: string; year: number | null }> = [];
  for (const o of [...showingWiki, ...contextRows]) {
    if (imageSeen.has(o.id)) continue;
    if (!o.wikipedia_link) continue;
    imageSeen.add(o.id);
    images.push({ id: o.id, title: o.title, wikipedia: o.wikipedia_link, year: o.start_year });
    if (images.length >= 6) break;
  }

  return { contextRows, umbrellas, before, after, resources, images };
}

function buildSystemPrompt(): string {
  return [
    "You are a historian writing a concise narrative for the Ever-When timeline app.",
    "The reader is looking at a specific window of history across one or more themed timelines.",
    "Write 3–5 short paragraphs of flowing prose (NOT bullet lists) that orient them in this period.",
    "Roughly half your narrative should focus on the occurrences currently ON SCREEN; the other half",
    "should weave in essential surrounding context they cannot see — the broader era or umbrella period",
    "that contains this window (always name the overarching era, war, or dynasty even when it is not",
    "itself on screen, e.g. note when these events fall within the Hundred Years' War), high-importance",
    "contemporaneous events, and brief before/after reference points so the window feels situated in time.",
    "Refer to specific people and events by name. Be accurate; do NOT invent facts, dates, or sources.",
    "Do not address the reader as 'you' or describe the app/screen; just tell the history.",
    "Output prose only — no headings, no bullet points, no lists. A curated resource list is handled separately.",
  ].join(" ");
}

function buildUserMessage(
  body: SummaryRequest,
  startYear: number,
  endYear: number,
  ctx: Awaited<ReturnType<typeof gatherContext>>,
): string {
  const lines: string[] = [];
  lines.push(`WINDOW: ${bce(startYear)} – ${bce(endYear)}`);
  lines.push(`TIMELINES SHOWN: ${body.timelines.map((t) => t.name).join(", ") || "(none)"}`);
  lines.push("");
  lines.push("ON SCREEN NOW (base ~half the narrative on a relevant selection of these — don't be exhaustive):");
  const showingSorted = [...body.showing].sort((a, b) => b.priority - a.priority).slice(0, 40);
  if (showingSorted.length === 0) lines.push("- (nothing currently rendered)");
  for (const o of showingSorted) lines.push(occLine({ title: o.title, type: o.type, start_year: o.startYear, end_year: o.endYear }));
  lines.push("");
  lines.push("BROADER CONTEXT (use for the other ~half; NOT on screen):");
  if (ctx.umbrellas.length) {
    lines.push("Umbrella periods containing this window:");
    for (const o of ctx.umbrellas) lines.push(occLine(o));
  }
  if (ctx.contextRows.length) {
    lines.push("High-priority nearby occurrences not shown:");
    for (const o of ctx.contextRows) lines.push(occLine(o));
  }
  if (ctx.before.length) {
    lines.push("Before this window:");
    for (const o of ctx.before) lines.push(occLine(o));
  }
  if (ctx.after.length) {
    lines.push("After this window:");
    for (const o of ctx.after) lines.push(occLine(o));
  }
  return lines.join("\n");
}
