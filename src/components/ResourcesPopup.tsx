import { useEffect, useMemo, useState } from "react";
import type { Occurrence } from "../types/database";
import { supabase } from "../lib/supabase";

/**
 * Modal listing the resources (podcast episodes, books, …) tagged to a
 * given subject occurrence. Each row shows the resource's title, date,
 * and a link to its external page (resource_link).
 */
export function ResourcesPopup({
  subject,
  resourceIds,
  onClose,
  onPickOccurrence,
}: {
  subject: Occurrence;
  /** IDs of resources tagged to this subject (from resourcesBySubject). */
  resourceIds: number[];
  onClose: () => void;
  /** Optional: clicking a resource's title navigates the timeline to it
   *  (re-uses the search-pick handler so it auto-zooms + flashes). */
  onPickOccurrence?: (occ: Occurrence) => void;
}) {
  const [resources, setResources] = useState<Occurrence[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    if (resourceIds.length === 0) {
      setResources([]);
      setLoading(false);
      return;
    }
    setLoading(true);
    (async () => {
      const { data, error } = await supabase
        .from("occurrences")
        .select("*")
        .in("id", resourceIds);
      if (cancelled) return;
      if (error) {
        console.error("resources fetch failed", error);
        setResources([]);
      } else {
        setResources((data ?? []) as Occurrence[]);
      }
      setLoading(false);
    })();
    return () => {
      cancelled = true;
    };
  }, [resourceIds]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [onClose]);

  // Group resources by occurrence_type → resource — but in practice all
  // entries here are type=resource. We just sort them by start_year then
  // title for stable display.
  const sorted = useMemo(() => {
    return [...resources].sort((a, b) => {
      const sa = a.start_year ?? 0;
      const sb = b.start_year ?? 0;
      if (sa !== sb) return sa - sb;
      return (a.title ?? "").localeCompare(b.title ?? "");
    });
  }, [resources]);

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
        aria-label={`Resources about ${subject.title}`}
      >
        <div className="flex items-start justify-between gap-2 px-4 pt-3 pb-2 border-b border-slate-200 dark:border-slate-800">
          <div className="min-w-0">
            <div className="text-[10px] uppercase tracking-wide text-slate-500">
              Resources · {resourceIds.length}
            </div>
            <h2 className="text-sm font-semibold text-slate-900 dark:text-slate-100 truncate">
              {subject.title}
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

        <ul className="flex-1 overflow-y-auto">
          {loading && (
            <li className="px-4 py-3 text-xs text-slate-500 italic">
              Loading…
            </li>
          )}
          {!loading && sorted.length === 0 && (
            <li className="px-4 py-3 text-xs text-slate-500 italic">
              No resources tagged to this subject.
            </li>
          )}
          {!loading &&
            sorted.map((r) => (
              <li
                key={r.id}
                className="border-b border-slate-200 dark:border-slate-800 last:border-b-0 px-3 py-2 flex flex-col gap-0.5"
              >
                <div className="flex items-baseline justify-between gap-2">
                  <button
                    type="button"
                    onClick={() => {
                      if (onPickOccurrence) {
                        onPickOccurrence(r);
                        onClose();
                      }
                    }}
                    className="min-w-0 flex-1 text-left text-xs font-medium text-slate-900 dark:text-slate-100 hover:text-blue-700 dark:hover:text-blue-300 truncate"
                  >
                    {r.title}
                  </button>
                  <span className="shrink-0 text-[10px] text-slate-500 tabular-nums">
                    {r.display_date ?? r.start_year ?? ""}
                  </span>
                </div>
                {r.resource_link && (
                  <a
                    href={r.resource_link}
                    target="_blank"
                    rel="noreferrer"
                    className="text-[10px] text-blue-600 dark:text-blue-400 hover:underline truncate"
                  >
                    {r.resource_link.replace(/^https?:\/\//, "").slice(0, 80)}
                  </a>
                )}
                {r.resource_episodes &&
                  Array.isArray(r.resource_episodes) &&
                  r.resource_episodes.length > 1 && (
                    <div className="text-[10px] text-slate-500">
                      {r.resource_episodes.length} episodes
                    </div>
                  )}
              </li>
            ))}
        </ul>

        <div className="px-3 py-2 border-t border-slate-200 dark:border-slate-800 flex items-center justify-end">
          <button
            type="button"
            onClick={onClose}
            className="px-3 py-1.5 rounded text-xs text-slate-800 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
}
