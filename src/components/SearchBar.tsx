import { useEffect, useMemo, useRef, useState } from "react";
import { supabase } from "../lib/supabase";
import type { HistoryEvent, Timeline } from "../types/database";
import { normalizeOngoing } from "../lib/dateFormat";

// What the dropdown row represents.
//   "year"        — jumps the timeline to a date.
//   "occurrence"  — jumps to an event's key date and (if needed) swaps in the
//                   timeline where that event has the highest priority score.
//   "timeline"    — swaps the rightmost visible column to this timeline.
//   "surprise"    — picks a random occurrence from the top 10% by priority
//                   and treats it as a search-bar selection. Only present
//                   when the input has fewer than SURPRISE_HIDE_AT chars so
//                   it doesn't clutter active queries.
type ResultRow =
  | { kind: "year"; year: number; label: string }
  | { kind: "occurrence"; event: HistoryEvent }
  | { kind: "timeline"; timeline: Timeline }
  | { kind: "surprise" };

const SEARCH_DEBOUNCE_MS = 180;
const MAX_RESULTS = 10;
// "Surprise me!" stays visible through the first two keystrokes (lengths 0,
// 1, 2) and disappears at three or more chars — by then the user is clearly
// searching for something specific and the random shortcut would just take
// a row away from actual results.
const SURPRISE_HIDE_AT = 3;
// Fraction of the entire occurrence corpus we consider for Surprise me!.
// 0.10 = top 10% by main_priority. Larger = more variety, smaller = more
// "famous" picks. With ~5500 entries this is a ~550-entry pool.
const SURPRISE_TOP_FRACTION = 0.10;

// Parse a free-form year/date string. Returns the year as an integer
// (negative for BCE) or null if the input doesn't look like a date.
// Accepted forms:
//   "1066", "-44"            → 1066, -44
//   "44 BC", "44 BCE"         → -44
//   "1066 AD", "1066 CE"      → 1066
//   "1066-10-14", "1066/10/14" → 1066   (we only need year for scale centring)
export function parseYearInput(raw: string): number | null {
  const t = raw.trim();
  if (!t) return null;

  // ISO-ish date "YYYY-MM-DD" or "YYYY/MM/DD" (optionally negative year).
  let m = t.match(/^(-?\d{1,6})[-/]\d{1,2}[-/]\d{1,2}$/);
  if (m) return parseInt(m[1], 10);

  // Plain signed integer.
  if (/^-?\d+$/.test(t)) {
    const n = parseInt(t, 10);
    if (n >= -1_000_000_000 && n <= 100_000) return n;
  }

  // "44 BC" / "44 BCE" / "44 B.C.E."
  m = t.match(/^(\d+)\s*(BCE?|B\.?C\.?E?\.?)$/i);
  if (m) return -parseInt(m[1], 10);

  // "1066 AD" / "1066 CE"
  m = t.match(/^(\d+)\s*(CE|AD|A\.?D\.?|C\.?E\.?)$/i);
  if (m) return parseInt(m[1], 10);

  return null;
}

// PostgREST `or(...)` parses commas/parens as syntax. Strip the chars that
// would break the filter so a stray punctuation mark doesn't 400 the request.
function sanitiseForOr(s: string): string {
  return s.replace(/[%,()*]/g, " ").trim();
}

// Given a full-life person row, find the highest-priority event/art that
// (a) lives inside their lifespan and (b) mentions them by name. Used by the
// search bar when the Lifespans toggle is off so picking a person from the
// dropdown lands on something visible.
async function topEventForPerson(
  person: HistoryEvent,
): Promise<HistoryEvent | null> {
  const start = person.start_year;
  // For still-living people the lifespan upper bound is "now".
  const end =
    person.end_year ??
    (person.is_ongoing ? new Date().getUTCFullYear() : person.start_year);
  if (start == null || end == null) return null;
  const name = person.title ?? "";
  const cleanName = sanitiseForOr(name);
  if (!cleanName) return null;
  const term = `%${cleanName}%`;
  const { data, error } = await supabase
    .from("occurrences")
    .select("*")
    .neq("id", person.id)
    .eq("is_full_life", false)
    .gte("start_year", start)
    .lte("start_year", end)
    .or(`title.ilike.${term},description.ilike.${term}`)
    .order("main_priority", { ascending: false, nullsFirst: false })
    .limit(1);
  if (error) {
    // eslint-disable-next-line no-console
    console.error("topEventForPerson failed", error);
    return null;
  }
  const row = (data ?? [])[0] as HistoryEvent | undefined;
  return row ? normalizeOngoing(row) : null;
}

function displayYear(y: number): string {
  if (y < 0) return `${Math.abs(y)} BCE`;
  return `${y} CE`;
}

export function SearchBar({
  showLifespans,
  onPickYear,
  onPickOccurrence,
  onPickTimeline,
}: {
  /** Mirrors the header toggle. When false, full-life person results are
   *  substituted at fetch time with the highest-priority event mentioning
   *  the person within their lifespan — otherwise the user could pick a
   *  hidden bar and nothing would be visible to jump to. */
  showLifespans: boolean;
  onPickYear: (year: number) => void;
  onPickOccurrence: (event: HistoryEvent) => void;
  /** Called when a user picks a timeline-row from the search dropdown. The
   *  parent decides which column to swap (typically the rightmost visible
   *  one — see App.tsx::handlePickTimelineFromSearch). */
  onPickTimeline: (timeline: Timeline) => void;
}) {
  const [query, setQuery] = useState("");
  const [debounced, setDebounced] = useState("");
  const [occurrences, setOccurrences] = useState<HistoryEvent[]>([]);
  const [allTimelines, setAllTimelines] = useState<Timeline[]>([]);
  const [open, setOpen] = useState(false);
  const [hi, setHi] = useState(0);
  const [loading, setLoading] = useState(false);
  /** Disabled briefly while we fetch+resolve a random surprise pick. */
  const [surprising, setSurprising] = useState(false);

  const inputRef = useRef<HTMLInputElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  /** Cache of "top SURPRISE_TOP_FRACTION% by main_priority" occurrence ids.
   *  Fetched lazily on the first Surprise click and re-used for subsequent
   *  clicks. Stable for a session — the underlying priorities only change
   *  when data is re-imported. */
  const surpriseIdsRef = useRef<number[] | null>(null);

  // ----- Load all timelines once -----------------------------------------
  // The set is small (~20) and stable enough to fetch eagerly so timeline
  // matches can be filtered locally without round-tripping the network on
  // every keystroke.
  useEffect(() => {
    let cancelled = false;
    (async () => {
      const { data, error } = await supabase
        .from("timelines")
        .select("*")
        .order("display_order", { ascending: true })
        .order("name", { ascending: true });
      if (cancelled) return;
      if (error) {
        // eslint-disable-next-line no-console
        console.error("timeline list fetch failed", error);
        return;
      }
      setAllTimelines((data ?? []) as Timeline[]);
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  // Debounce the input → debounced state used to drive queries.
  useEffect(() => {
    const id = window.setTimeout(() => setDebounced(query), SEARCH_DEBOUNCE_MS);
    return () => window.clearTimeout(id);
  }, [query]);

  // Fetch occurrences whose title or description matches the debounced query.
  useEffect(() => {
    const q = sanitiseForOr(debounced);
    if (!q) {
      setOccurrences([]);
      setLoading(false);
      return;
    }
    let cancelled = false;
    setLoading(true);
    (async () => {
      const term = `%${q}%`;
      const { data, error } = await supabase
        .from("occurrences")
        .select("*")
        .or(`title.ilike.${term},description.ilike.${term}`)
        // Sort by main_priority so the most prominent matches surface first.
        .order("main_priority", { ascending: false, nullsFirst: false })
        .limit(MAX_RESULTS);
      if (cancelled) return;
      if (error) {
        // eslint-disable-next-line no-console
        console.error("search query failed", error);
        setOccurrences([]);
        setLoading(false);
        return;
      }
      let rows = ((data ?? []) as HistoryEvent[]).map(normalizeOngoing);
      // Lifespan-toggle substitution: when full-life bars are hidden, picking
      // a person from the dropdown would land on an invisible entry. Replace
      // each full-life person result with the top-priority event mentioning
      // them inside their lifespan. If no such event exists we fall back to
      // returning the original person row (the user can still pick it and
      // toggle Lifespans back on).
      if (!showLifespans && rows.some((r) => r.is_full_life)) {
        const substituted = await Promise.all(
          rows.map(async (r) => {
            if (!r.is_full_life) return r;
            return (await topEventForPerson(r)) ?? r;
          }),
        );
        if (cancelled) return;
        const seen = new Set<number>();
        rows = substituted.filter((r) => {
          if (seen.has(r.id)) return false;
          seen.add(r.id);
          return true;
        });
      }
      setLoading(false);
      setOccurrences(rows);
    })();
    return () => {
      cancelled = true;
    };
  }, [debounced, showLifespans]);

  // Filter timelines locally by case-insensitive substring on name. Cheap
  // enough to recompute on every keystroke given how few timelines there
  // are (~20).
  const matchingTimelines = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return [] as Timeline[];
    return allTimelines
      .filter((t) => t.name.toLowerCase().includes(q))
      .slice(0, 6);  // cap so timelines don't crowd out occurrences
  }, [allTimelines, query]);

  // Combine surprise-row (if eligible) + year-row + timeline rows +
  // occurrence rows. Surprise sits at the top so the user's eye lands on
  // it when they click the empty input. It vanishes once they've typed
  // SURPRISE_HIDE_AT chars so it doesn't displace genuine results.
  const rows: ResultRow[] = useMemo(() => {
    const out: ResultRow[] = [];
    if (query.trim().length < SURPRISE_HIDE_AT) {
      out.push({ kind: "surprise" });
    }
    const year = parseYearInput(query);
    if (year != null) {
      out.push({ kind: "year", year, label: `Go to ${displayYear(year)}` });
    }
    for (const t of matchingTimelines) {
      out.push({ kind: "timeline", timeline: t });
    }
    for (const e of occurrences) {
      out.push({ kind: "occurrence", event: e });
    }
    return out;
  }, [query, occurrences, matchingTimelines]);

  // Keep the highlighted-row index in bounds whenever the result list changes.
  useEffect(() => {
    if (hi >= rows.length) setHi(0);
  }, [rows.length, hi]);

  // Close the dropdown on outside click.
  useEffect(() => {
    if (!open) return;
    const onDocClick = (ev: MouseEvent) => {
      if (!containerRef.current) return;
      if (!containerRef.current.contains(ev.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", onDocClick);
    return () => document.removeEventListener("mousedown", onDocClick);
  }, [open]);

  /** Lazy-load + cache the id pool for Surprise me!. Counts the corpus,
   *  fetches the top SURPRISE_TOP_FRACTION (capped to 2000 ids to keep the
   *  payload small), and remembers the result on the ref. */
  async function loadSurpriseIds(): Promise<number[]> {
    if (surpriseIdsRef.current) return surpriseIdsRef.current;
    // Count first so we know how many to grab. Exclude resources from the
    // pool — randomly landing on a podcast episode is more confusing than
    // helpful when the user clicked "surprise me" expecting a historical
    // event.
    const countRes = await supabase
      .from("occurrences")
      .select("id", { count: "exact", head: true })
      .neq("occurrence_type", "resource");
    const total = countRes.count ?? 0;
    if (total === 0) {
      surpriseIdsRef.current = [];
      return [];
    }
    const limit = Math.min(2000, Math.max(50, Math.floor(total * SURPRISE_TOP_FRACTION)));
    const { data, error } = await supabase
      .from("occurrences")
      .select("id")
      .neq("occurrence_type", "resource")
      .order("main_priority", { ascending: false, nullsFirst: false })
      .limit(limit);
    if (error) {
      // eslint-disable-next-line no-console
      console.error("surprise pool fetch failed", error);
      surpriseIdsRef.current = [];
      return [];
    }
    const ids = (data ?? []).map((r) => (r as { id: number }).id);
    surpriseIdsRef.current = ids;
    return ids;
  }

  async function pickSurprise() {
    if (surprising) return;
    setSurprising(true);
    try {
      const ids = await loadSurpriseIds();
      if (ids.length === 0) return;
      // Pick a random id, then fetch its full row. Substitute via
      // topEventForPerson when lifespans are hidden so the user always lands
      // on something visible.
      const pickId = ids[Math.floor(Math.random() * ids.length)];
      const { data, error } = await supabase
        .from("occurrences")
        .select("*")
        .eq("id", pickId)
        .single();
      if (error || !data) {
        // eslint-disable-next-line no-console
        console.error("surprise pick fetch failed", error);
        return;
      }
      let chosen = normalizeOngoing(data as HistoryEvent);
      if (!showLifespans && chosen.is_full_life) {
        chosen = (await topEventForPerson(chosen)) ?? chosen;
      }
      onPickOccurrence(chosen);
      setOpen(false);
      setQuery("");
      inputRef.current?.blur();
    } finally {
      setSurprising(false);
    }
  }

  function pick(row: ResultRow) {
    if (row.kind === "surprise") {
      void pickSurprise();
      return;
    }
    if (row.kind === "year") onPickYear(row.year);
    else if (row.kind === "occurrence") onPickOccurrence(row.event);
    else if (row.kind === "timeline") onPickTimeline(row.timeline);
    setOpen(false);
    setQuery("");
    inputRef.current?.blur();
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      if (rows.length) {
        setOpen(true);
        setHi((i) => (i + 1) % rows.length);
      }
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      if (rows.length) {
        setOpen(true);
        setHi((i) => (i - 1 + rows.length) % rows.length);
      }
    } else if (e.key === "Enter") {
      e.preventDefault();
      const row = rows[hi];
      if (row) pick(row);
    } else if (e.key === "Escape") {
      setOpen(false);
      inputRef.current?.blur();
    }
  }

  const showDropdown = open && (rows.length > 0 || loading);

  return (
    <div ref={containerRef} className="relative">
      <input
        ref={inputRef}
        type="text"
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          setOpen(true);
          setHi(0);
        }}
        onFocus={() => setOpen(true)}
        onKeyDown={onKeyDown}
        placeholder="Search…"
        // w-full lets the parent (flex-1 min-w-0 wrapper in App.tsx) shrink the
        // input to fit on phones. On desktop the w-72 override restores the
        // fixed 288px width the design assumes.
        className="w-full md:w-72 px-2 py-1 rounded border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 text-xs placeholder-slate-500 focus:outline-none focus:border-slate-400 dark:focus:border-slate-500"
      />
      {showDropdown && (
        <ul
          className="absolute left-0 right-0 mt-1 z-40 max-h-96 overflow-y-auto rounded border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 shadow-lg text-xs"
          role="listbox"
        >
          {loading && rows.length === 0 && (
            <li className="px-2 py-1 text-slate-500 italic">Searching…</li>
          )}
          {rows.map((row, i) => {
            const active = i === hi;
            const cls = `px-2 py-1 cursor-pointer ${
              active
                ? "bg-slate-200 dark:bg-slate-700 text-slate-900 dark:text-slate-100"
                : "text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800"
            }`;
            if (row.kind === "surprise") {
              return (
                <li
                  key="surprise"
                  className={cls}
                  role="option"
                  aria-selected={active}
                  onMouseEnter={() => setHi(i)}
                  onMouseDown={(ev) => {
                    ev.preventDefault();
                    pick(row);
                  }}
                  aria-disabled={surprising}
                >
                  <div className="flex items-baseline gap-2">
                    <span className="truncate flex-1">
                      <span className="mr-1">🎲</span>
                      {surprising ? "Picking…" : "Surprise me!"}
                    </span>
                    <span className="text-[10px] text-slate-500 shrink-0">
                      random top-priority entry
                    </span>
                  </div>
                </li>
              );
            }
            if (row.kind === "year") {
              return (
                <li
                  key={`year-${row.year}`}
                  className={cls}
                  role="option"
                  aria-selected={active}
                  onMouseEnter={() => setHi(i)}
                  onMouseDown={(e) => {
                    e.preventDefault();
                    pick(row);
                  }}
                >
                  <span className="text-amber-300">⌖</span> {row.label}
                </li>
              );
            }
            if (row.kind === "timeline") {
              const t = row.timeline;
              return (
                <li
                  key={`tl-${t.id}`}
                  className={cls}
                  role="option"
                  aria-selected={active}
                  onMouseEnter={() => setHi(i)}
                  onMouseDown={(ev) => {
                    ev.preventDefault();
                    pick(row);
                  }}
                  title={t.slug}
                >
                  <div className="flex items-baseline gap-2">
                    <span className="truncate flex-1">{t.name}</span>
                    <span className="text-[10px] text-slate-500 shrink-0">
                      (timeline)
                    </span>
                  </div>
                </li>
              );
            }
            const e = row.event;
            const title = e.title ?? "(untitled)";
            const sub =
              e.display_date ??
              (e.start_year != null ? displayYear(e.start_year) : "");
            const mainCat = e.main_category ?? "—";
            return (
              <li
                key={`occ-${e.id}`}
                className={cls}
                role="option"
                aria-selected={active}
                onMouseEnter={() => setHi(i)}
                onMouseDown={(ev) => {
                  ev.preventDefault();
                  pick(row);
                }}
              >
                <div className="flex items-baseline gap-2">
                  <span className="truncate flex-1">{title}</span>
                  <span className="text-[10px] text-slate-500 shrink-0">
                    {sub}
                  </span>
                </div>
                <div className="text-[10px] text-slate-500 truncate">
                  {mainCat}
                </div>
              </li>
            );
          })}
          {!loading && rows.length === 0 && (
            <li className="px-2 py-1 text-slate-500 italic">No matches</li>
          )}
        </ul>
      )}
    </div>
  );
}
