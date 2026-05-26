import { useEffect, useMemo, useRef, useState } from "react";
import type { Occurrence } from "../types/database";
import { supabase } from "../lib/supabase";
import { normalizeOngoing } from "../lib/dateFormat";

/**
 * Modal showing every child of a given umbrella entry, ordered chronologically
 * (by end_year for periods, then start_year, then title), with a responsive
 * priority-bucket colouring that scales to umbrella size:
 *   - small umbrellas (≤40 children): top quarter → dark blue, next quarter
 *     → light blue (rounded up; e.g. 5 children → 2 dark, 1 light, 2 rest)
 *   - large umbrellas: capped at 10 dark + 10 light (the original scheme)
 *
 * Children = any occurrence whose first_zoom_out_id or second_zoom_out_id
 * matches the umbrella's id. The list also includes the begins/ends point
 * markers if the umbrella has them (those are children too).
 */
export function ChildrenPopup({
  umbrella,
  highlightedChildId,
  onClose,
  onPickOccurrence,
}: {
  umbrella: Occurrence;
  /** Optional: render this child row with a stronger highlight so the user
   *  can spot which sibling they came from. Set when the popup was opened
   *  via the ↰ indicator on a child box. */
  highlightedChildId?: number;
  onClose: () => void;
  /** Clicking a child navigates the timeline to it (same handler the search
   *  bar uses). */
  onPickOccurrence: (occ: Occurrence) => void;
}) {
  const [children, setChildren] = useState<Occurrence[]>([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    (async () => {
      // Two ordered lists: by priority (for tier-bucket colouring) and by
      // chronology (for display order). We fetch once and sort twice in JS
      // to avoid a duplicate round-trip.
      const { data, error } = await supabase
        .from("occurrences")
        .select("*")
        .or(
          `first_zoom_out_id.eq.${umbrella.id},second_zoom_out_id.eq.${umbrella.id}`,
        )
        .order("main_priority", { ascending: false, nullsFirst: false })
        .limit(500);
      if (cancelled) return;
      if (error) {
        console.error("children fetch failed", error);
        setChildren([]);
      } else {
        setChildren(((data ?? []) as Occurrence[]).map(normalizeOngoing));
      }
      setLoading(false);
    })();
    return () => {
      cancelled = true;
    };
  }, [umbrella.id]);

  // Reverse-chronological sort: most recent at the top. Sort key is end_year
  // for period entries (a period ending later appears before one ending
  // earlier), then start_year, then title for stable ordering. Falls back to
  // start_year when end is null (point events).
  const chronological = useMemo(() => {
    return [...children].sort((a, b) => {
      const aEnd = a.end_year ?? a.start_year ?? Number.NEGATIVE_INFINITY;
      const bEnd = b.end_year ?? b.start_year ?? Number.NEGATIVE_INFINITY;
      if (aEnd !== bEnd) return bEnd - aEnd;
      const aStart = a.start_year ?? Number.NEGATIVE_INFINITY;
      const bStart = b.start_year ?? Number.NEGATIVE_INFINITY;
      if (aStart !== bStart) return bStart - aStart;
      return (a.title ?? "").localeCompare(b.title ?? "");
    });
  }, [children]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [onClose]);

  // Focus the search input on open.
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return chronological;
    return chronological.filter((c) => (c.title ?? "").toLowerCase().includes(q));
  }, [chronological, query]);

  // Compute priority-tier index using the priority-ordered list (children),
  // so the colour reflects notability regardless of chronological position.
  // Bucket sizes scale to umbrella size: for small umbrellas the top quarter
  // (rounded up) is dark blue and the next quarter is light blue; for large
  // umbrellas the original 10/10 cap kicks in.
  const tierByIndex = useMemo(() => {
    const n = children.length;
    // Round up so even tiny umbrellas (3-4 entries) get at least one of each.
    const topSize = Math.min(10, Math.max(1, Math.ceil(n / 4)));
    const midSize = Math.min(10, Math.max(1, Math.ceil(n / 4)));
    const m = new Map<number, "top" | "mid" | "rest">();
    children.forEach((c, i) => {
      m.set(c.id, i < topSize ? "top" : i < topSize + midSize ? "mid" : "rest");
    });
    return m;
  }, [children]);

  return (
    <div
      className="fixed inset-0 z-[60] bg-black/50 flex items-center justify-center px-3"
      onMouseDown={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div
        className="w-full max-w-md max-h-[80vh] flex flex-col rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 shadow-2xl"
        role="dialog"
        aria-label={`Children of ${umbrella.title}`}
      >
        <div className="flex items-start justify-between gap-2 px-4 pt-3 pb-2 border-b border-slate-200 dark:border-slate-800">
          <div className="min-w-0">
            <div className="text-[10px] uppercase tracking-wide text-slate-500">
              Umbrella · {children.length} entries
            </div>
            <h2 className="text-sm font-semibold text-slate-900 dark:text-slate-100 truncate">
              {umbrella.title}
            </h2>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close"
            className="shrink-0 w-8 h-8 flex items-center justify-center rounded text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800"
          >
            <span aria-hidden className="text-lg leading-none">×</span>
          </button>
        </div>

        {/* Search — only show when there are enough entries to warrant it */}
        {children.length > 8 && (
          <div className="px-3 py-2 border-b border-slate-200 dark:border-slate-800">
            <input
              ref={inputRef}
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search children…"
              className="w-full px-2 py-1 rounded border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 text-xs focus:outline-none focus:border-slate-400 dark:focus:border-slate-500"
              autoComplete="off"
              spellCheck={false}
            />
          </div>
        )}

        <ul className="flex-1 overflow-y-auto">
          {loading && (
            <li className="px-4 py-3 text-xs text-slate-500 italic">
              Loading children…
            </li>
          )}
          {!loading && children.length === 0 && (
            <li className="px-4 py-3 text-xs text-slate-500 italic">
              No children found.
            </li>
          )}
          {!loading && children.length > 0 && filtered.length === 0 && (
            <li className="px-4 py-3 text-xs text-slate-500 italic">
              No matches.
            </li>
          )}
          {!loading &&
            filtered.map((child) => {
              const tier = tierByIndex.get(child.id) ?? "rest";
              const titleClass =
                tier === "top"
                  ? "text-blue-800 dark:text-blue-300 font-medium"
                  : tier === "mid"
                    ? "text-blue-600 dark:text-blue-400"
                    : "text-slate-600 dark:text-slate-400";
              const highlighted = child.id === highlightedChildId;
              return (
                <li
                  key={child.id}
                  className={`border-b border-slate-200 dark:border-slate-800 last:border-b-0 ${
                    highlighted
                      ? "bg-amber-100 dark:bg-amber-900/40"
                      : ""
                  }`}
                >
                  <button
                    type="button"
                    onClick={() => {
                      onPickOccurrence(child);
                      onClose();
                    }}
                    className="w-full text-left px-3 py-1.5 flex items-baseline gap-2 hover:bg-slate-100 dark:hover:bg-slate-800/60"
                  >
                    <span className="shrink-0 text-[10px] text-slate-500 tabular-nums w-16">
                      {child.display_date ?? child.start_year ?? ""}
                    </span>
                    <span className={`min-w-0 flex-1 text-xs truncate ${titleClass}`}>
                      {child.title}
                    </span>
                    {highlighted && (
                      <span className="shrink-0 text-[10px] text-amber-700 dark:text-amber-300">
                        ← you
                      </span>
                    )}
                  </button>
                </li>
              );
            })}
        </ul>
      </div>
    </div>
  );
}
