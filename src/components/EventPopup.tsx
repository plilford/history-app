import { forwardRef, useEffect, useState } from "react";
import type { EventWithPriority } from "../types/database";
import {
  fetchWikiSummary,
  wikiTitleFromUrl,
  type WikiSummary,
} from "../lib/wikipedia";
import { useAuth } from "../lib/auth";
import { useFavourites } from "../lib/favourites";

const POPUP_WIDTH = 360;
const POPUP_MAX_HEIGHT = 420;
const MARGIN = 8;
// Below this viewport width we drop the desktop "anchored to the event"
// behaviour and pin the popup to the bottom of the screen across full width.
// Matches the column-count breakpoint in App.tsx.
const POPUP_MOBILE_BREAKPOINT_PX = 768;

export const EventPopup = forwardRef<HTMLDivElement, {
  event: EventWithPriority;
  anchorRect: DOMRect;
  onMouseEnter: () => void;
  onMouseLeave: () => void;
  /** Tap close (×) and tap-outside dismiss. Required for touch devices where
   *  mouseleave never fires. */
  onClose: () => void;
  /** When the user adds this occurrence to favourites, the parent shows the
   *  SuggestionsPopup. Not called on un-favourite. */
  onFavourited?: (event: EventWithPriority) => void;
  /** When set, the heart button is disabled and clicking it opens the auth
   *  modal instead — supplied by the parent. */
  onSignInRequest?: () => void;
}>(function EventPopup({
  event,
  anchorRect,
  onMouseEnter,
  onMouseLeave,
  onClose,
  onFavourited,
  onSignInRequest,
}, ref) {
  const [summary, setSummary] = useState<WikiSummary | null>(null);
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();
  const { isFavourite, toggle } = useFavourites();
  const fav = isFavourite(event.id);

  async function handleFavouriteClick() {
    if (!user) {
      onSignInRequest?.();
      return;
    }
    const wasFav = fav;
    const isNowFav = await toggle(event.id);
    // Only trigger suggestions on add, not remove.
    if (!wasFav && isNowFav) onFavourited?.(event);
  }

  useEffect(() => {
    const title = wikiTitleFromUrl(event.wikipedia_link);
    if (!title) {
      setSummary(null);
      return;
    }
    setLoading(true);
    setSummary(null);
    let cancelled = false;
    fetchWikiSummary(title).then((s) => {
      if (cancelled) return;
      setSummary(s);
      setLoading(false);
    });
    return () => {
      cancelled = true;
    };
  }, [event.id, event.wikipedia_link]);

  // On mobile, render as a bottom sheet spanning the full width (so it covers
  // both visible timeline columns). On desktop, position next to the event.
  const isMobile =
    typeof window !== "undefined" &&
    window.innerWidth < POPUP_MOBILE_BREAKPOINT_PX;

  const containerStyle: React.CSSProperties = isMobile
    ? {
        left: 0,
        right: 0,
        bottom: 0,
        // Allow up to 70vh on mobile so longer Wikipedia summaries don't get
        // cut off above the weblink. The container itself scrolls vertically.
        maxHeight: "70vh",
        borderRadius: "12px 12px 0 0",
      }
    : (() => {
        const pos = computePosition(anchorRect);
        return {
          left: pos.left,
          top: pos.top,
          width: POPUP_WIDTH,
          maxHeight: POPUP_MAX_HEIGHT,
        };
      })();

  return (
    <div
      ref={ref}
      // overflow-y-auto on the outer container lets the user scroll within the
      // popup to reach the weblink/links at the bottom — the previous
      // overflow-hidden was clipping content past the maxHeight.
      className="fixed z-50 border border-slate-300 dark:border-slate-600 bg-slate-50 dark:bg-slate-800 text-slate-900 dark:text-slate-100 shadow-xl overflow-y-auto overflow-x-hidden overscroll-contain"
      style={{
        ...containerStyle,
        ...(isMobile ? {} : { borderRadius: 8 }),
      }}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
    >
      {summary?.thumbnail && (
        <img
          src={summary.thumbnail.source}
          alt=""
          className="w-full h-36 object-cover bg-white dark:bg-slate-900"
          loading="lazy"
        />
      )}
      <div className="p-3 space-y-2">
        <div className="flex items-baseline justify-between gap-2">
          <h3 className="text-sm font-semibold leading-tight flex-1">
            {event.title}
          </h3>
          <span
            className="text-[10px] text-slate-400 shrink-0"
            title={event.date_uncertain ? "Date is approximate or disputed" : undefined}
          >
            {(event.display_date ?? event.start_year ?? "") +
              (event.date_uncertain && !String(event.display_date ?? "").endsWith("*") ? "*" : "")}
          </span>
          <button
            type="button"
            onClick={handleFavouriteClick}
            aria-label={
              !user
                ? "Sign in to favourite"
                : fav
                  ? "Remove from favourites"
                  : "Add to favourites"
            }
            title={
              !user
                ? "Sign in to favourite"
                : fav
                  ? "Remove from favourites"
                  : "Add to favourites"
            }
            className={`shrink-0 -mt-1 w-7 h-7 flex items-center justify-center rounded hover:bg-slate-200 dark:hover:bg-slate-700 focus:outline-none focus:bg-slate-200 dark:focus:bg-slate-700 ${
              fav
                ? "text-rose-400 hover:text-rose-300"
                : "text-slate-400 hover:text-slate-900 dark:hover:text-slate-100"
            }`}
          >
            <span aria-hidden className="text-sm leading-none">
              {fav ? "♥" : "♡"}
            </span>
          </button>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close"
            className="shrink-0 -mt-1 -mr-1 w-7 h-7 flex items-center justify-center rounded text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-200 dark:hover:bg-slate-700 focus:outline-none focus:bg-slate-200 dark:focus:bg-slate-700"
          >
            <span aria-hidden className="text-base leading-none">×</span>
          </button>
        </div>

        {summary?.description && (
          <div className="text-[11px] text-slate-400 italic">
            {summary.description}
          </div>
        )}

        {event.main_category && (
          <div className="text-[10px] text-slate-500">
            main: {event.main_category}
          </div>
        )}

        {summary?.extract ? (
          <p className="text-xs text-slate-800 dark:text-slate-200 leading-snug">{summary.extract}</p>
        ) : event.description ? (
          <p className="text-xs text-slate-800 dark:text-slate-200 leading-snug">{event.description}</p>
        ) : loading ? (
          <p className="text-xs text-slate-500 italic">Loading…</p>
        ) : null}

        {event.wikipedia_link && (
          <a
            href={event.wikipedia_link}
            target="_blank"
            rel="noreferrer"
            className="block text-[10px] text-blue-400 hover:text-blue-300 underline truncate"
          >
            {event.wikipedia_link.replace(/^https?:\/\//, "")}
          </a>
        )}

        {event.other_link && (
          <a
            href={event.other_link}
            target="_blank"
            rel="noreferrer"
            className="block text-[10px] text-blue-400 hover:text-blue-300 underline truncate"
          >
            {event.other_link.replace(/^https?:\/\//, "")}
          </a>
        )}
      </div>
    </div>
  );
});

function computePosition(rect: DOMRect): { left: number; top: number } {
  const winW = window.innerWidth;
  const winH = window.innerHeight;
  // Prefer the right side of the anchor; flip left if it won't fit.
  let left = rect.right + MARGIN;
  if (left + POPUP_WIDTH > winW) {
    left = rect.left - POPUP_WIDTH - MARGIN;
  }
  if (left < MARGIN) left = MARGIN;
  // Align with anchor top; nudge up if it would clip off the bottom.
  let top = rect.top;
  if (top + POPUP_MAX_HEIGHT > winH) {
    top = Math.max(MARGIN, winH - POPUP_MAX_HEIGHT - MARGIN);
  }
  if (top < MARGIN) top = MARGIN;
  return { left, top };
}
