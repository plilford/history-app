import { useEffect, useState } from "react";
import type { EventWithPriority } from "../types/database";
import {
  fetchWikiSummary,
  wikiTitleFromUrl,
  type WikiSummary,
} from "../lib/wikipedia";

const POPUP_WIDTH = 360;
const POPUP_MAX_HEIGHT = 420;
const MARGIN = 8;

export function EventPopup({
  event,
  anchorRect,
  onMouseEnter,
  onMouseLeave,
}: {
  event: EventWithPriority;
  anchorRect: DOMRect;
  onMouseEnter: () => void;
  onMouseLeave: () => void;
}) {
  const [summary, setSummary] = useState<WikiSummary | null>(null);
  const [loading, setLoading] = useState(false);

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

  const pos = computePosition(anchorRect);

  return (
    <div
      className="fixed z-50 rounded-lg border border-slate-600 bg-slate-800 text-slate-100 shadow-xl overflow-hidden"
      style={{
        left: pos.left,
        top: pos.top,
        width: POPUP_WIDTH,
        maxHeight: POPUP_MAX_HEIGHT,
      }}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
    >
      {summary?.thumbnail && (
        <img
          src={summary.thumbnail.source}
          alt=""
          className="w-full h-36 object-cover bg-slate-900"
          loading="lazy"
        />
      )}
      <div className="p-3 space-y-2">
        <div className="flex items-baseline justify-between gap-2">
          <h3 className="text-sm font-semibold leading-tight">
            {event.title}
          </h3>
          <span
            className="text-[10px] text-slate-400 shrink-0"
            title={event.date_uncertain ? "Date is approximate or disputed" : undefined}
          >
            {(event.display_date ?? event.start_year ?? "") +
              (event.date_uncertain && !String(event.display_date ?? "").endsWith("*") ? "*" : "")}
          </span>
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
          <p className="text-xs text-slate-200 leading-snug max-h-44 overflow-y-auto pr-1">
            {summary.extract}
          </p>
        ) : event.description ? (
          <p className="text-xs text-slate-200 leading-snug max-h-44 overflow-y-auto pr-1">
            {event.description}
          </p>
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
}

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
