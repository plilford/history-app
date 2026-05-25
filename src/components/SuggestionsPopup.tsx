import { useEffect, useState } from "react";
import type { Occurrence } from "../types/database";
import { fetchSuggestions, type Suggestion } from "../lib/suggestions";
import { useAuth } from "../lib/auth";
import { useFavourites } from "../lib/favourites";

/**
 * Modal shown immediately after the user favourites an occurrence. Suggests
 * ~10 related occurrences (same umbrella / top of the seed's primary slug)
 * with a heart toggle on each so the user can quickly favourite several.
 */
export function SuggestionsPopup({
  seed,
  onClose,
  onPickOccurrence,
}: {
  seed: Occurrence;
  onClose: () => void;
  /** Optional: clicking a suggestion's title navigates the timeline to it. */
  onPickOccurrence?: (occ: Occurrence) => void;
}) {
  const { user } = useAuth();
  const { isFavourite, toggle } = useFavourites();
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fetchSuggestions(seed.id, user?.id ?? null, 10).then((s) => {
      if (cancelled) return;
      setSuggestions(s);
      setLoading(false);
    });
    return () => {
      cancelled = true;
    };
  }, [seed.id, user?.id]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [onClose]);

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
        aria-label="You may also like"
      >
        <div className="flex items-start justify-between gap-2 px-4 pt-3 pb-2 border-b border-slate-200 dark:border-slate-800">
          <div className="min-w-0">
            <div className="text-[10px] uppercase tracking-wide text-slate-500">
              Favourited
            </div>
            <h2 className="text-sm font-semibold text-slate-900 dark:text-slate-100 truncate">
              {seed.title}
            </h2>
            <div className="text-xs text-slate-400 mt-0.5">
              You may also like…
            </div>
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
              Loading suggestions…
            </li>
          )}
          {!loading && suggestions.length === 0 && (
            <li className="px-4 py-3 text-xs text-slate-500 italic">
              No related occurrences found.
            </li>
          )}
          {!loading &&
            suggestions.map(({ occurrence, reason }) => {
              const fav = isFavourite(occurrence.id);
              return (
                <li
                  key={occurrence.id}
                  className="border-b border-slate-200 dark:border-slate-800 last:border-b-0 px-3 py-2 flex items-start gap-2 hover:bg-slate-100 dark:hover:bg-slate-800/50"
                >
                  <button
                    type="button"
                    onClick={() => toggle(occurrence.id)}
                    aria-label={fav ? "Remove favourite" : "Add favourite"}
                    title={fav ? "Remove favourite" : "Add favourite"}
                    className={`shrink-0 w-7 h-7 flex items-center justify-center rounded text-base ${
                      fav
                        ? "text-rose-400 hover:text-rose-300"
                        : "text-slate-500 hover:text-slate-800 dark:hover:text-slate-200"
                    }`}
                  >
                    <span aria-hidden>{fav ? "♥" : "♡"}</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      if (onPickOccurrence) {
                        onPickOccurrence(occurrence);
                        onClose();
                      }
                    }}
                    className="min-w-0 flex-1 text-left"
                  >
                    <div className="text-sm font-medium text-slate-900 dark:text-slate-100 truncate">
                      {occurrence.title}
                    </div>
                    <div className="text-[10px] text-slate-500 flex items-center gap-1.5">
                      <span>{occurrence.display_date ?? occurrence.start_year ?? ""}</span>
                      <span aria-hidden>·</span>
                      <span className="truncate">{reason}</span>
                    </div>
                  </button>
                </li>
              );
            })}
        </ul>

        <div className="border-t border-slate-200 dark:border-slate-800 px-3 py-2 flex items-center justify-end">
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
