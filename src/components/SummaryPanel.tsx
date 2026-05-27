import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { CompactOccurrence } from "../types/database";
import { fetchWikiSummary, wikiTitleFromUrl } from "../lib/wikipedia";

export interface SummaryWindow {
  startYear: number;
  endYear: number;
}

interface ResourceItem {
  id: number;
  title: string;
  link: string | null;
  subtype: string | null;
}
interface ImageCandidate {
  id: number;
  title: string;
  wikipedia: string;
  year: number | null;
}
interface SummaryMeta {
  resources: ResourceItem[];
  images: ImageCandidate[];
}
interface ResolvedImage {
  title: string;
  src: string;
  page?: string;
}

export interface SummaryPanelProps {
  window: SummaryWindow | null;
  timelines: Array<{ slug: string; name: string }>;
  showing: CompactOccurrence[];
  viewState: { showLifespans: boolean; regionWeighted: boolean };
  accessToken: string | null;
  /** Auto-regenerate as the view settles. */
  autoMode: boolean;
  /** Increments to force a (re)generation for the current view, bypassing cache. */
  generationTrigger: number;
  /** Full-screen overlay (narrow/app) — suppresses images, per spec. */
  isOverlay: boolean;
  onClose: () => void;
  /** Settle debounce for auto mode (ms). */
  settleMs: number;
  /** Per-session call cap for auto mode. */
  sessionCap: number;
}

// Module-level so they survive panel unmount within a session.
const summaryCache = new Map<string, { content: string; meta: SummaryMeta }>();
let autoCallCount = 0;

const SUMMARY_FONT_MIN = 11;
const SUMMARY_FONT_MAX = 22;
const SUMMARY_FONT_DEFAULT = 13;

function relativeWindowKey(w: SummaryWindow): string {
  const span = Math.max(1, Math.abs(w.endYear - w.startYear));
  const bucket = Math.max(1, span * 0.02); // ~2% of span
  const a = Math.round(w.startYear / bucket);
  const b = Math.round(w.endYear / bucket);
  return `${a}:${b}`;
}

function cacheKey(p: SummaryPanelProps): string {
  if (!p.window) return "";
  const slugs = p.timelines.map((t) => t.slug).sort().join(",");
  return [
    relativeWindowKey(p.window),
    slugs,
    p.viewState.showLifespans ? "L1" : "L0",
    p.viewState.regionWeighted ? "R1" : "R0",
  ].join("|");
}

function fmtYear(y: number): string {
  const r = Math.round(y);
  if (r < 0) return `${Math.abs(r).toLocaleString()} BCE`;
  return `${r.toLocaleString()}`;
}

// Markdown styling without the typography plugin: target child elements via
// Tailwind arbitrary variants.
const MD_CLASS =
  "[&_p]:mb-2 [&_p:last-child]:mb-0 [&_strong]:font-semibold " +
  "[&_a]:text-blue-600 dark:[&_a]:text-blue-400 [&_a]:underline " +
  "[&_em]:italic [&_ul]:list-disc [&_ul]:pl-4 [&_ul]:mb-2";

function subtypeLabel(s: string | null): string {
  switch (s) {
    case "podcast-episode": return "Podcast";
    case "book-nonfiction": return "Book";
    case "book-fiction": return "Novel";
    case "documentary": return "Documentary";
    case "museum-artifact": return "Artifact";
    default: return "Resource";
  }
}

export function SummaryPanel(props: SummaryPanelProps) {
  const { window: win, isOverlay, onClose, autoMode, generationTrigger } = props;

  const [content, setContent] = useState("");
  const [meta, setMeta] = useState<SummaryMeta | null>(null);
  const [status, setStatus] = useState<"idle" | "loading" | "streaming" | "done" | "error">("idle");
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [capReached, setCapReached] = useState(false);
  // Cache key the displayed content belongs to (so we can show a "view changed"
  // hint when the live view has drifted away from it).
  const [displayedKey, setDisplayedKey] = useState<string>("");
  const [resolvedImages, setResolvedImages] = useState<ResolvedImage[]>([]);
  // Reader-adjustable narrative font size (persisted).
  const [fontSize, setFontSize] = useState<number>(() => {
    const v = Number(localStorage.getItem("summaryFontSize"));
    return Number.isFinite(v) && v >= SUMMARY_FONT_MIN && v <= SUMMARY_FONT_MAX ? v : SUMMARY_FONT_DEFAULT;
  });
  useEffect(() => {
    try { localStorage.setItem("summaryFontSize", String(fontSize)); } catch { /* ignore */ }
  }, [fontSize]);

  const abortRef = useRef<AbortController | null>(null);
  const lastTriggerRef = useRef<number>(generationTrigger);
  // Keep the freshest props for the async generator without retriggering it.
  const propsRef = useRef(props);
  propsRef.current = props;

  const liveKey = useMemo(() => cacheKey(props), [props]);

  const generate = useCallback(async (force: boolean) => {
    const p = propsRef.current;
    if (!p.window) return;
    const key = cacheKey(p);

    if (!force) {
      const cached = summaryCache.get(key);
      if (cached) {
        setContent(cached.content);
        setMeta(cached.meta);
        setStatus("done");
        setErrorMsg(null);
        setDisplayedKey(key);
        return;
      }
    } else {
      summaryCache.delete(key);
    }

    if (!p.accessToken) {
      setStatus("error");
      setErrorMsg("Not signed in.");
      return;
    }

    // Abort any in-flight generation.
    abortRef.current?.abort();
    const ac = new AbortController();
    abortRef.current = ac;

    setContent("");
    setMeta(null);
    setResolvedImages([]);
    setErrorMsg(null);
    setCapReached(false);
    setStatus("loading");
    setDisplayedKey(key);

    try {
      const res = await fetch("/api/summary", {
        method: "POST",
        signal: ac.signal,
        headers: {
          "content-type": "application/json",
          Authorization: `Bearer ${p.accessToken}`,
        },
        body: JSON.stringify({
          window: { startYear: p.window.startYear, endYear: p.window.endYear },
          timelines: p.timelines,
          viewState: {
            showLifespans: p.viewState.showLifespans,
            regionWeighted: p.viewState.regionWeighted,
          },
          showing: p.showing,
          userApiKey: null,
        }),
      });

      if (!res.ok || !res.body) {
        let detail = `${res.status}`;
        try {
          const j = await res.json();
          if (res.status === 401) detail = "Couldn't verify your session" + (j?.detail ? ` (${j.detail})` : "") + ".";
          else if (res.status === 403) detail = "This account isn't the editor.";
          else detail = j?.detail || j?.error || detail;
        } catch { /* ignore */ }
        setStatus("error");
        setErrorMsg(detail);
        return;
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let acc = "";
      let buf = "";
      let gotMeta: SummaryMeta | null = null;
      setStatus("streaming");

      for (;;) {
        const { value, done } = await reader.read();
        if (done) break;
        buf += decoder.decode(value, { stream: true });
        let sep: number;
        while ((sep = buf.indexOf("\n\n")) !== -1) {
          const line = buf.slice(0, sep);
          buf = buf.slice(sep + 2);
          if (!line.startsWith("data:")) continue;
          const payload = line.slice(5).trim();
          if (!payload) continue;
          let frame: any;
          try { frame = JSON.parse(payload); } catch { continue; }
          if (frame.t === "text") {
            acc += frame.v;
            setContent(acc);
          } else if (frame.t === "meta") {
            gotMeta = { resources: frame.resources ?? [], images: frame.images ?? [] };
            setMeta(gotMeta);
          } else if (frame.t === "error") {
            setStatus("error");
            setErrorMsg(frame.message ?? "Generation failed.");
            return;
          }
          // frame.t === "done" handled by stream end
        }
      }

      setStatus("done");
      summaryCache.set(key, { content: acc, meta: gotMeta ?? { resources: [], images: [] } });
    } catch (e: any) {
      if (e?.name === "AbortError") return; // superseded by a newer request
      setStatus("error");
      setErrorMsg(String(e?.message ?? e));
    }
  }, []);

  // Manual: regenerate whenever the trigger changes (button click), forcing a
  // fresh call for the current view.
  useEffect(() => {
    if (generationTrigger !== lastTriggerRef.current) {
      lastTriggerRef.current = generationTrigger;
      void generate(true);
    }
  }, [generationTrigger, generate]);

  // Generate on first mount. Deferred a tick: opening the panel flips the
  // columns' reportVisible on, but they report their on-screen sets in the
  // effect phase *after* this mount runs, so the visibleUnion (and thus
  // `showing`) isn't populated synchronously. A 0ms timeout lets that state
  // settle so the first request carries the real on-screen list, not an empty
  // one. generate() reads the freshest props via propsRef.
  const mountedRef = useRef(false);
  useEffect(() => {
    if (mountedRef.current) return;
    mountedRef.current = true;
    const t = setTimeout(() => void generate(false), 0);
    return () => clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Auto: regenerate (cache-first) when the view settles on a new key.
  useEffect(() => {
    if (!autoMode) return;
    if (!liveKey) return;
    if (liveKey === displayedKey && status !== "idle") return;
    const handle = setTimeout(() => {
      const cached = summaryCache.get(liveKey);
      if (cached) {
        void generate(false); // loads from cache
        return;
      }
      if (autoCallCount >= props.sessionCap) {
        setCapReached(true);
        return;
      }
      autoCallCount += 1;
      void generate(false);
    }, props.settleMs);
    return () => clearTimeout(handle);
  }, [autoMode, liveKey, displayedKey, status, generate, props.settleMs, props.sessionCap]);

  // Resolve Wikipedia thumbnails for the side-panel image strip.
  useEffect(() => {
    if (isOverlay || !meta || meta.images.length === 0) {
      setResolvedImages([]);
      return;
    }
    let cancelled = false;
    (async () => {
      const out: ResolvedImage[] = [];
      for (const img of meta.images) {
        if (out.length >= 3) break;
        const title = wikiTitleFromUrl(img.wikipedia) ?? img.title;
        const summary = await fetchWikiSummary(title);
        const src = summary?.thumbnail?.source;
        if (src) out.push({ title: img.title, src, page: summary?.content_urls?.desktop?.page });
      }
      if (!cancelled) setResolvedImages(out);
    })();
    return () => { cancelled = true; };
  }, [meta, isOverlay]);

  // Clean up any in-flight request on unmount.
  useEffect(() => () => abortRef.current?.abort(), []);

  const viewDrifted = status === "done" && displayedKey !== "" && liveKey !== displayedKey;

  const windowLabel = win
    ? `${fmtYear(win.startYear)} – ${fmtYear(win.endYear)}`
    : "";

  // Interleave images between paragraphs once streaming is complete (side
  // panel only). During streaming we render the accumulating text plainly.
  const body = (() => {
    if (status === "done" && !isOverlay && resolvedImages.length > 0) {
      const paras = content.split(/\n{2,}/).filter((s) => s.trim().length > 0);
      const blocks: React.ReactNode[] = [];
      let imgIdx = 0;
      paras.forEach((para, i) => {
        blocks.push(
          <ReactMarkdown key={`p${i}`} remarkPlugins={[remarkGfm]}>{para}</ReactMarkdown>,
        );
        // Insert an image after the 1st and 3rd paragraph.
        if ((i === 0 || i === 2) && imgIdx < resolvedImages.length) {
          const img = resolvedImages[imgIdx++];
          blocks.push(
            <figure key={`img${i}`} className="my-3">
              <img
                src={img.src}
                alt={img.title}
                loading="lazy"
                className="w-full rounded border border-slate-200 dark:border-slate-700"
              />
              <figcaption className="mt-1 text-[10px] text-slate-500 dark:text-slate-400">
                {img.title}
              </figcaption>
            </figure>,
          );
        }
      });
      // Any remaining images go at the end.
      while (imgIdx < resolvedImages.length) {
        const img = resolvedImages[imgIdx++];
        blocks.push(
          <figure key={`imgEnd${imgIdx}`} className="my-3">
            <img src={img.src} alt={img.title} loading="lazy"
              className="w-full rounded border border-slate-200 dark:border-slate-700" />
            <figcaption className="mt-1 text-[10px] text-slate-500 dark:text-slate-400">{img.title}</figcaption>
          </figure>,
        );
      }
      return <div className={MD_CLASS}>{blocks}</div>;
    }
    return (
      <div className={MD_CLASS}>
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
      </div>
    );
  })();

  return (
    <div className="flex flex-col h-full bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-200">
      <div className="flex items-center justify-between gap-2 px-3 py-2 border-b border-slate-200 dark:border-slate-700 flex-shrink-0">
        <div className="min-w-0">
          <div className="text-sm font-semibold">Summary</div>
          {windowLabel && (
            <div className="text-[11px] text-slate-500 dark:text-slate-400 truncate">{windowLabel}</div>
          )}
        </div>
        <div className="flex items-center gap-1 flex-shrink-0">
          <div className="flex items-center rounded border border-slate-200 dark:border-slate-700 overflow-hidden">
            <button
              type="button"
              onClick={() => setFontSize((s) => Math.max(SUMMARY_FONT_MIN, s - 1))}
              disabled={fontSize <= SUMMARY_FONT_MIN}
              title="Smaller text"
              className="px-1.5 py-1 text-[11px] hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-40"
            >
              A−
            </button>
            <button
              type="button"
              onClick={() => setFontSize((s) => Math.min(SUMMARY_FONT_MAX, s + 1))}
              disabled={fontSize >= SUMMARY_FONT_MAX}
              title="Larger text"
              className="px-1.5 py-1 text-[13px] border-l border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-40"
            >
              A+
            </button>
          </div>
          <button
            type="button"
            onClick={() => void generate(true)}
            disabled={status === "loading" || status === "streaming"}
            title="Regenerate for the current view"
            className="text-[11px] px-2 py-1 rounded border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-50"
          >
            ↻ Regenerate
          </button>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close summary"
            className="text-lg leading-none px-2 py-0.5 rounded hover:bg-slate-100 dark:hover:bg-slate-800"
          >
            ×
          </button>
        </div>
      </div>

      <div
        className="flex-1 overflow-y-auto px-3 py-3 leading-relaxed"
        style={{ fontSize }}
      >
        {viewDrifted && (
          <button
            type="button"
            onClick={() => void generate(true)}
            className="mb-3 w-full text-[11px] px-2 py-1.5 rounded bg-amber-50 dark:bg-amber-900/30 border border-amber-300 dark:border-amber-700 text-amber-800 dark:text-amber-200 hover:bg-amber-100 dark:hover:bg-amber-900/50"
          >
            View has changed — regenerate for the current period
          </button>
        )}

        {status === "error" && (
          <div className="text-[12px] text-red-600 dark:text-red-400">
            {errorMsg ?? "Something went wrong."}
            <button
              type="button"
              onClick={() => void generate(true)}
              className="ml-2 underline hover:no-underline"
            >
              Retry
            </button>
          </div>
        )}

        {capReached && status !== "streaming" && status !== "loading" && (
          <div className="mb-3 text-[11px] text-slate-500 dark:text-slate-400">
            Auto-summary paused (session limit reached). Use Regenerate to continue.
          </div>
        )}

        {(status === "loading" || (status === "streaming" && content === "")) && (
          <div className="text-[12px] text-slate-500 dark:text-slate-400 animate-pulse">
            Summarising the visible period…
          </div>
        )}

        {content !== "" && body}

        {status === "done" && meta && meta.resources.length > 0 && (
          <div className="mt-4 pt-3 border-t border-slate-200 dark:border-slate-700">
            <div className="text-[11px] font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400 mb-1.5">
              Go deeper
            </div>
            <ul className="space-y-1.5">
              {meta.resources.map((r) => (
                <li key={r.id} className="text-[12px]">
                  {r.link ? (
                    <a href={r.link} target="_blank" rel="noreferrer"
                      className="text-blue-600 dark:text-blue-400 hover:underline">
                      {r.title}
                    </a>
                  ) : (
                    <span>{r.title}</span>
                  )}
                  <span className="ml-1.5 text-[10px] text-slate-400">{subtypeLabel(r.subtype)}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
