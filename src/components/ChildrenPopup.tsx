import { useEffect, useMemo, useRef, useState } from "react";
import type { Occurrence } from "../types/database";
import { supabase } from "../lib/supabase";
import { normalizeOngoing } from "../lib/dateFormat";

/**
 * Modal showing every child of a given umbrella entry, ordered by global
 * priority (main_priority desc), with priority-bucket colouring:
 *   - top 10  → dark blue  (the marquee items)
 *   - next 10 → light blue
 *   - rest    → dark grey
 *
 * Children = any occurrence whose first_zoom_out_id or second_zoom_out_id
 * matches the umbrella's id. The list also includes the begins/ends point
 * markers if the umbrella has them (those are children too).
 */
export function ChildrenPopup({
  umbrella,
  onClose,
  onPickOccurrence,
}: {
  umbrella: Occurrence;
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
    if (!q) return children;
    return children.filter((c) => (c.title ?? "").toLowerCase().includes(q));
  }, [children, query]);

  // Compute priority-tier index using the ORIGINAL ranked list (children),
  // so the colour stays stable while the user searches. Index 0..9 = top 10,
  // 10..19 = next 10, 20+ = rest.
  const tierByIndex = useMemo(() => {
    const m = new Map<number, "top" | "mid" | "rest">();
    children.forEach((c, i) => {
      m.set(c.id, i < 10 ? "top" : i < 20 ? "mid" : "rest");
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
              return (
                <li
                  key={child.id}
                  className="border-b border-slate-200 dark:border-slate-800 last:border-b-0"
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
                  </button>
                </li>
              );
            })}
        </ul>
      </div>
    </div>
  );
}
