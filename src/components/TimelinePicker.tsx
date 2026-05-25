import { useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import { supabase } from "../lib/supabase";
import type { Timeline } from "../types/database";
import {
  TIMELINE_GROUP_LABELS,
  TIMELINE_GROUP_ORDER,
  groupForSlug,
  type TimelineGroup,
} from "../lib/timelineGroups";
import {
  FAVOURITES_TIMELINE_ID,
  FAVOURITES_TIMELINE_NAME,
  FAVOURITES_TIMELINE_SLUG,
} from "../lib/favouritesTimeline";

/**
 * Popover used to swap the timeline shown in a column. Mounted as a child of
 * the clicked column header (which provides the anchor rect); the popover
 * itself is positioned fixed relative to the viewport.
 *
 * - Fetches every timeline once, and stays in sync thereafter via a Supabase
 *   Realtime subscription on the `timelines` table. Inserts, updates
 *   (rename), and deletes are reflected without a refresh.
 * - The search input filters the list with case-insensitive substring matching
 *   on the timeline name, plus an autofill suggestion that the user can accept
 *   with Tab or →.
 * - Keyboard: ↑/↓ to walk the list, Enter to pick, Esc to close.
 */
export function TimelinePicker({
  currentName,
  anchorRect,
  onPick,
  onClose,
  showFavourites = false,
}: {
  /** Name of the timeline currently shown in the column being edited. */
  currentName: string;
  /** Bounding rect of the column header — picker is positioned beneath it. */
  anchorRect: DOMRect;
  onPick: (name: string) => void;
  onClose: () => void;
  /** When true (= user is signed in), prepend the "My Favourites"
   *  pseudo-timeline at the top of the list. */
  showFavourites?: boolean;
}) {
  const [allTimelines, setAllTimelines] = useState<Timeline[]>([]);
  const [query, setQuery] = useState("");
  const [hi, setHi] = useState(0);
  const [loading, setLoading] = useState(true);

  const inputRef = useRef<HTMLInputElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const listRef = useRef<HTMLUListElement>(null);

  // ----- Fetch + subscribe to Realtime changes ----------------------------
  // Initial fetch loads every timeline; the Realtime subscription then keeps
  // `allTimelines` in sync with inserts/updates/deletes on the `timelines`
  // table. The picker is therefore always current without needing a manual
  // refresh button.
  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    (async () => {
      const { data, error } = await supabase
        .from("timelines")
        .select("*")
        .order("display_order", { ascending: true })
        .order("name", { ascending: true });
      if (cancelled) return;
      setLoading(false);
      if (error) {
        // eslint-disable-next-line no-console
        console.error("timeline list query failed", error);
        return;
      }
      setAllTimelines((data ?? []) as Timeline[]);
    })();

    const channel = supabase
      .channel("timelines-picker")
      .on(
        "postgres_changes",
        { event: "*", schema: "public", table: "timelines" },
        (payload) => {
          setAllTimelines((prev) => {
            const next = prev.slice();
            const row = (payload.new ?? payload.old) as Timeline | undefined;
            if (!row) return prev;

            if (payload.eventType === "INSERT") {
              if (next.some((t) => t.id === row.id)) return prev;
              next.push(payload.new as Timeline);
            } else if (payload.eventType === "UPDATE") {
              const idx = next.findIndex((t) => t.id === row.id);
              if (idx === -1) next.push(payload.new as Timeline);
              else next[idx] = payload.new as Timeline;
            } else if (payload.eventType === "DELETE") {
              const idx = next.findIndex((t) => t.id === row.id);
              if (idx === -1) return prev;
              next.splice(idx, 1);
            }

            // Re-sort to match the initial query order.
            next.sort(
              (a, b) =>
                a.display_order - b.display_order ||
                a.name.localeCompare(b.name),
            );
            return next;
          });
        },
      )
      .subscribe();

    return () => {
      cancelled = true;
      supabase.removeChannel(channel);
    };
  }, []);

  // ----- Filtering + autofill --------------------------------------------
  // `filtered` is sorted into our display groups (Worldwide, Europe, Americas,
  // Asia, Conflicts, Major periods, …) with the special "My Favourites"
  // pseudo-timeline (when the user is signed in) pinned at the very top. The
  // flat `filtered` array preserves the rendering order; `groupBoundaries`
  // records where group headers should be inserted by the render code.
  // Keyboard navigation still walks the flat array — headers are visual-only.
  const favouritesTimeline: Timeline = useMemo(
    () => ({
      id: FAVOURITES_TIMELINE_ID,
      name: FAVOURITES_TIMELINE_NAME,
      slug: FAVOURITES_TIMELINE_SLUG,
      display_order: -1,
      is_featured: false,
    }),
    [],
  );

  const { filtered, groupBoundaries, favouritesHeaderLabel } = useMemo(() => {
    const q = query.trim().toLowerCase();
    const matchesFavourites =
      showFavourites &&
      (q === "" || FAVOURITES_TIMELINE_NAME.toLowerCase().includes(q));
    const matches = q
      ? allTimelines.filter((t) => t.name.toLowerCase().includes(q))
      : allTimelines;
    // Bucket by group, preserving each group's existing display_order.
    const buckets = new Map<TimelineGroup, Timeline[]>();
    for (const t of matches) {
      const g = groupForSlug(t.slug);
      let arr = buckets.get(g);
      if (!arr) { arr = []; buckets.set(g, arr); }
      arr.push(t);
    }
    // Concat: favourites first (if visible), then the canonical group order.
    const flat: Timeline[] = [];
    const boundaries: { index: number; group: TimelineGroup }[] = [];
    let favLabel: string | null = null;
    if (matchesFavourites) {
      favLabel = "Yours";
      flat.push(favouritesTimeline);
    }
    for (const g of TIMELINE_GROUP_ORDER) {
      const arr = buckets.get(g);
      if (!arr || arr.length === 0) continue;
      boundaries.push({ index: flat.length, group: g });
      flat.push(...arr);
    }
    return {
      filtered: flat,
      groupBoundaries: boundaries,
      favouritesHeaderLabel: favLabel,
    };
  }, [allTimelines, query, showFavourites, favouritesTimeline]);

  const autofillSuggestion = useMemo(() => {
    const q = query.trim();
    if (!q) return "";
    const lower = q.toLowerCase();
    if (
      showFavourites &&
      FAVOURITES_TIMELINE_NAME.toLowerCase().startsWith(lower)
    ) {
      return FAVOURITES_TIMELINE_NAME.slice(q.length);
    }
    const hit = allTimelines.find((t) =>
      t.name.toLowerCase().startsWith(lower),
    );
    if (!hit) return "";
    // The grey ghost text is the *remainder* after what the user has typed.
    // We try to preserve the user's casing for the prefix portion.
    return hit.name.slice(q.length);
  }, [allTimelines, query, showFavourites]);

  // Keep highlight in bounds after filtering shrinks the list.
  useEffect(() => {
    if (hi >= filtered.length) setHi(0);
  }, [filtered.length, hi]);

  // ----- Initial focus + auto-scroll to current ---------------------------
  // Focus the input so the user can start typing immediately. Also scroll the
  // current timeline into view so users opening the picker see where they are.
  useLayoutEffect(() => {
    inputRef.current?.focus();
  }, []);

  useEffect(() => {
    if (loading) return;
    const list = listRef.current;
    if (!list) return;
    const idx = filtered.findIndex((t) => t.name === currentName);
    if (idx < 0) return;
    // Use data-item-idx to look up the right <li> — headers are interleaved
    // as <li role="presentation"> elements so children[idx] doesn't line up.
    const child = list.querySelector<HTMLElement>(`[data-item-idx="${idx}"]`);
    child?.scrollIntoView({ block: "nearest" });
    setHi(idx);
    // Run only once after the initial load.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [loading]);

  // Close on outside click / Escape.
  useEffect(() => {
    const onDocClick = (ev: MouseEvent) => {
      if (!containerRef.current) return;
      if (!containerRef.current.contains(ev.target as Node)) onClose();
    };
    const onKey = (ev: KeyboardEvent) => {
      if (ev.key === "Escape") onClose();
    };
    document.addEventListener("mousedown", onDocClick);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", onDocClick);
      document.removeEventListener("keydown", onKey);
    };
  }, [onClose]);

  // Keep highlighted row scrolled into view as the user arrows through.
  useEffect(() => {
    const list = listRef.current;
    if (!list) return;
    const child = list.querySelector<HTMLElement>(`[data-item-idx="${hi}"]`);
    child?.scrollIntoView({ block: "nearest" });
  }, [hi]);

  function pickByIndex(i: number) {
    const t = filtered[i];
    if (!t) return;
    onPick(t.name);
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      if (filtered.length) setHi((i) => (i + 1) % filtered.length);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      if (filtered.length)
        setHi((i) => (i - 1 + filtered.length) % filtered.length);
    } else if (e.key === "Enter") {
      e.preventDefault();
      pickByIndex(hi);
    } else if (
      (e.key === "Tab" || e.key === "ArrowRight") &&
      autofillSuggestion
    ) {
      // Only commit the autofill on Tab/→ when the cursor is at the end of
      // the input — that's the convention that lets users still edit mid-text.
      const input = inputRef.current;
      if (input && input.selectionStart === query.length) {
        e.preventDefault();
        setQuery(query + autofillSuggestion);
      }
    }
  }

  // ----- Positioning ------------------------------------------------------
  // Popover sits below the column header by default, but we flip above it if
  // there isn't enough viewport room — keeps the picker usable when the user
  // clicks a header near the bottom of a short window.
  const POPOVER_WIDTH = 280;
  const POPOVER_HEIGHT = 360;
  const margin = 6;
  let left = anchorRect.left;
  if (left + POPOVER_WIDTH > window.innerWidth - margin) {
    left = Math.max(margin, window.innerWidth - margin - POPOVER_WIDTH);
  }
  const spaceBelow = window.innerHeight - anchorRect.bottom;
  const flipUp = spaceBelow < POPOVER_HEIGHT && anchorRect.top > spaceBelow;
  const top = flipUp
    ? Math.max(margin, anchorRect.top - POPOVER_HEIGHT - margin)
    : anchorRect.bottom + margin;

  return (
    <div
      ref={containerRef}
      className="fixed z-50 rounded border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 shadow-xl flex flex-col"
      style={{ left, top, width: POPOVER_WIDTH, maxHeight: POPOVER_HEIGHT }}
      role="dialog"
      aria-label="Pick a timeline"
    >
      <div className="p-2 border-b border-slate-200 dark:border-slate-700">
        {/* Wrapper holds the real input and a ghost div for the autofill hint */}
        <div className="relative">
          {/* Ghost text rendered behind the input shows the autofill suggestion */}
          <div
            aria-hidden
            className="absolute inset-0 px-2 py-1 text-xs whitespace-pre pointer-events-none select-none flex items-center"
          >
            <span className="invisible">{query}</span>
            <span className="text-slate-500">{autofillSuggestion}</span>
          </div>
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setHi(0);
            }}
            onKeyDown={onKeyDown}
            placeholder="Search timelines…"
            className="relative w-full px-2 py-1 rounded border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 text-xs placeholder-slate-500 focus:outline-none focus:border-slate-400 dark:focus:border-slate-500"
            autoComplete="off"
            spellCheck={false}
          />
        </div>
      </div>

      <ul
        ref={listRef}
        className="flex-1 overflow-y-auto text-xs"
        role="listbox"
      >
        {loading && (
          <li className="px-2 py-2 text-slate-500 italic">Loading…</li>
        )}
        {!loading &&
          filtered.map((t, i) => {
            // If this item starts a new group, emit a non-selectable header
            // row first. Headers use role="presentation" so screen readers
            // skip them; keyboard navigation also skips them because hi
            // walks the flat `filtered` array, which doesn't include headers.
            const boundary = groupBoundaries.find((b) => b.index === i);
            const favHeader =
              i === 0 && favouritesHeaderLabel ? (
                <li
                  key="hdr-favourites"
                  role="presentation"
                  className="px-2 pt-2 pb-0.5 text-[10px] uppercase tracking-wide text-slate-500 select-none"
                >
                  {favouritesHeaderLabel}
                </li>
              ) : null;
            const header = boundary ? (
              <li
                key={`hdr-${boundary.group}`}
                role="presentation"
                className="px-2 pt-2 pb-0.5 text-[10px] uppercase tracking-wide text-slate-500 select-none"
              >
                {TIMELINE_GROUP_LABELS[boundary.group]}
              </li>
            ) : null;

            const active = i === hi;
            const isCurrent = t.name === currentName;
            const isFavRow = t.slug === FAVOURITES_TIMELINE_SLUG;
            return [
              favHeader,
              header,
              <li
                key={t.id}
                data-item-idx={i}
                role="option"
                aria-selected={active}
                onMouseEnter={() => setHi(i)}
                onMouseDown={(e) => {
                  e.preventDefault();
                  pickByIndex(i);
                }}
                className={`px-2 py-1 cursor-pointer flex items-baseline gap-2 ${
                  active
                    ? "bg-slate-200 dark:bg-slate-700 text-slate-900 dark:text-slate-100"
                    : "text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800"
                }`}
                title={t.slug}
              >
                {isFavRow && (
                  <span aria-hidden className="text-rose-400 shrink-0">♥</span>
                )}
                <span className="truncate flex-1">{t.name}</span>
                {isCurrent && (
                  <span className="text-[10px] text-slate-500 shrink-0">
                    current
                  </span>
                )}
              </li>,
            ];
          })}
        {!loading && filtered.length === 0 && (
          <li className="px-2 py-2 text-slate-500 italic">No matches</li>
        )}
      </ul>

      <div className="px-2 py-1 border-t border-slate-200 dark:border-slate-700 text-[10px] text-slate-500 flex items-center justify-between">
        <span>{allTimelines.length} timelines</span>
        <span>↑↓ Enter · Tab autofill · Esc</span>
      </div>
    </div>
  );
}
