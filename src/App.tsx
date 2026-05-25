import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import { supabase } from "./lib/supabase";
import type { Timeline, EventWithPriority, HistoryEvent } from "./types/database";
import { EventPopup } from "./components/EventPopup";
import { SearchBar } from "./components/SearchBar";
import { TimelinePicker } from "./components/TimelinePicker";
import { AuthModal } from "./components/AuthModal";
import { SuggestionsPopup } from "./components/SuggestionsPopup";
import { AuthProvider, useAuth } from "./lib/auth";
import { FavouritesProvider, useFavourites } from "./lib/favourites";
import { ThemeProvider, useTheme } from "./lib/theme";
import { FAVOURITES_TIMELINE_NAME, FAVOURITES_TIMELINE_SLUG } from "./lib/favouritesTimeline";
import {
  addUncertaintyMark,
  formatPartial,
  formatPartialRange,
  granularityForSpan,
  normalizeOngoing,
  type DateDisplayMode,
  type Granularity,
} from "./lib/dateFormat";
import { colorFor, type OccurrenceColor } from "./lib/occurrenceColor";
import {
  makeYearScale,
  generateLogTicks,
  generateMonthTicks,
  generateDayTicks,
  type YearScale,
} from "./lib/yearScale";

// HOVER_OPEN_DELAY_MS retired — touch needs immediate open or it races with
// pointerleave; mouse hover opens instantly too and feels snappier.
const HOVER_CLOSE_DELAY_MS = 200;
// (search bar: keeps centre-of-viewport scroll, swaps rightmost timeline column)

type HoverHandler = (event: EventWithPriority, rect: DOMRect) => void;

// Names of the three timeline columns shown on initial load. The user can
// swap any of them via the column-header TimelinePicker; the rightmost slot
// is also where SearchBar drops a freshly-picked timeline.
const DEFAULT_TIMELINE_NAMES = [
  "Master",
  "Arts and Thoughts",
  "England: Monarchs",
];

// Fallback range used until the auto-fetched min/max returns from the DB.
const FALLBACK_YEAR_MIN = -10_000;
const FALLBACK_YEAR_MAX = 2025;
const DEFAULT_PIXELS_PER_YEAR = 4;

// Length of the recent-era "linear band" in the log-compressed axis. Years
// within LINEAR_RANGE_YEARS of yearMax render at the linear pixelsPerYear
// rate; older years are progressively compressed. 500 yr keeps the medieval
// period readable at default zoom without exploding the total scroll height
// for billion-year datasets.
const LINEAR_RANGE_YEARS = 500;

const COLUMN_MIN_WIDTH_PX = 140;      // narrowest width that still feels readable
const AXIS_WIDTH_DESKTOP_PX = 72;
const AXIS_WIDTH_MOBILE_PX = 48;      // tighter on phones to give columns more room
const HEADER_HEIGHT_PX = 37;
// Used by the header to decide when to collapse settings into the hamburger
// menu. Independent of the column-count math below — that's now purely a
// function of how many columns fit at MIN width.
const MOBILE_BREAKPOINT_PX = 768;

// Hook: observes the actual width of the scroll-container element (not
// window.innerWidth — that can over-report on Android TWAs with system
// insets and lead to columns overflowing off-screen) and derives:
//   - visibleColumnCount: how many timeline columns to render right now,
//     so they always fit within the container at >= MIN width
//   - columnWidth: exact px width per column, so cols + axis == container
//   - isMobile: viewport hint for non-layout UI decisions (menu, popup)
//
// Phone portrait (~360px): 2 cols at 144px each
// Phone landscape (~800px): 3 cols at 243px each (capped at desktopColumns)
// Desktop (>= 1024px): 3 cols at ~317px+ each (capped at desktopColumns)
function useResponsiveLayout(
  containerRef: React.RefObject<HTMLElement>,
  desktopColumns: number,
) {
  const [containerWidth, setContainerWidth] = useState<number>(() =>
    typeof window === "undefined" ? 1280 : window.innerWidth,
  );
  useLayoutEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    // Seed from the actual element width on mount; subsequent updates come
    // from the ResizeObserver. Catches the case where the initial render
    // used window.innerWidth but the element is slightly narrower.
    setContainerWidth(el.clientWidth);
    if (typeof ResizeObserver === "undefined") {
      const onResize = () => setContainerWidth(el.clientWidth);
      window.addEventListener("resize", onResize);
      return () => window.removeEventListener("resize", onResize);
    }
    const ro = new ResizeObserver((entries) => {
      const w = entries[0]?.contentRect.width;
      if (typeof w === "number" && w > 0) setContainerWidth(Math.floor(w));
    });
    ro.observe(el);
    return () => ro.disconnect();
  }, [containerRef]);

  const isMobile = containerWidth < MOBILE_BREAKPOINT_PX;
  // Narrower year-axis gutter on phones to give the timeline columns more
  // pixels. Year labels stay readable down to ~48px.
  const axisWidth = isMobile ? AXIS_WIDTH_MOBILE_PX : AXIS_WIDTH_DESKTOP_PX;
  const available = Math.max(0, containerWidth - axisWidth);
  // How many cols of MIN width fit? Cap at desktopColumns (user's choice);
  // floor at 1 (always render at least one column even on hilariously narrow
  // viewports — better than blanking the timeline entirely).
  const visibleColumnCount = Math.max(
    1,
    Math.min(desktopColumns, Math.floor(available / COLUMN_MIN_WIDTH_PX)),
  );
  // Divide remaining width evenly so no horizontal overflow is ever possible.
  const columnWidth = Math.floor(available / visibleColumnCount);
  return { isMobile, containerWidth, axisWidth, visibleColumnCount, columnWidth };
}

// EVENT_BOX_HEIGHT_PX is now dynamic — see `boxHeight` derived from
// occurrenceDensity (8-20) and the current viewport height. Older code paths
// that needed a constant default still use this as a fallback for the
// initial render before viewport size has been measured.
const DEFAULT_EVENT_BOX_HEIGHT_PX = 36;

// MIN_PPY / MAX_PPY clamp the linear-band ppy (the `k` factor in the year
// scale). Even with log-compressed deep time, very low k keeps the whole
// timeline approachable; very high k spaces a single day across the viewport.
const MIN_PPY = 0.05;
// 300 000 px/yr ≈ 821 px per day, so a single day fills a typical viewport.
const MAX_PPY = 300_000;

// Occurrence density: how many boxes should comfortably fit in the viewport at
// once. The actual box height is derived from this and the viewport height.
const MIN_DENSITY = 8;
const MAX_DENSITY = 20;
const DEFAULT_DENSITY = 12;

// Regions used for the region-weight controls (see region weight sliders in
// the header). Each occurrence has a 1–10 weight per region; the user-facing
// slider value is a 0–10 multiplier ("how much do I care about this region").
type Region = "europe" | "americas" | "asia" | "australasia" | "africa";
const REGIONS: { key: Region; label: string }[] = [
  { key: "europe",      label: "Europe" },
  { key: "americas",    label: "Americas" },
  { key: "asia",        label: "Asia" },
  { key: "australasia", label: "Australasia" },
  { key: "africa",      label: "Africa" },
];
type RegionWeights = Record<Region, number>;
const DEFAULT_REGION_FILTER: RegionWeights = {
  europe: 5, americas: 5, asia: 5, australasia: 5, africa: 5,
};
// Slugs of timelines whose ranking should be modulated by region weights.
const REGION_WEIGHTED_SLUGS = new Set(["master", "arts-and-thoughts"]);

// ----- Period-line stagger --------------------------------------------------
// Lines for periods are placed in horizontal "tracks" so that visually
// overlapping period ranges don't all stack on the same x. Track 0 is dead
// centre; subsequent tracks fan outwards alternately so the most visually
// dominant line stays in the middle.
const LINE_TRACK_STRIDE_PX = 10;     // px between adjacent tracks
const LINE_THICKNESS_PX = 2;
// Arrowheads at the start/end of each period line. The arrow is a CSS-border
// triangle centred on the line. Width is the full base of the triangle (left
// to right), height is how far it extends past the endpoint.
const LINE_ARROW_HALF_W_PX = 4;
const LINE_ARROW_H_PX = 5;

function lineXForTrack(track: number, columnWidth: number): number {
  const center = columnWidth / 2 - LINE_THICKNESS_PX / 2;
  if (track === 0) return center;
  const magnitude = Math.ceil(track / 2);
  const sign = track % 2 === 1 ? -1 : 1;
  return center + sign * magnitude * LINE_TRACK_STRIDE_PX;
}

// Short axis-tick label. Keeps small years as plain numbers so the typical
// historical view reads naturally ("-2000", "0", "1500"); only condenses
// once the magnitude reaches geological scale.
function compactYearLabel(y: number): string {
  const abs = Math.abs(y);
  if (abs >= 1_000_000_000) return `${(y / 1_000_000_000).toFixed(1).replace(/\.0$/, "")}B`;
  if (abs >= 1_000_000)     return `${(y / 1_000_000).toFixed(1).replace(/\.0$/, "")}M`;
  if (abs >= 100_000)       return `${(y / 1_000).toFixed(0)}k`;
  return String(y);
}

export default function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <FavouritesProvider>
          <AppInner />
        </FavouritesProvider>
      </AuthProvider>
    </ThemeProvider>
  );
}

function AppInner() {
  const { user, signOut } = useAuth();
  const { ids: favouriteIds, isFavourite } = useFavourites();
  const { theme, toggle: toggleTheme } = useTheme();
  const [authModalOpen, setAuthModalOpen] = useState(false);
  /** When set, the SuggestionsPopup is open seeded on this occurrence. */
  const [suggestionSeed, setSuggestionSeed] = useState<EventWithPriority | null>(null);

  const [timelines, setTimelines] = useState<Timeline[]>([]);
  // Names of the columns to render, in display order. Search may replace the
  // rightmost slot so that a found occurrence lands in a visible timeline.
  const [timelineNames, setTimelineNames] = useState<string[]>(
    () => DEFAULT_TIMELINE_NAMES,
  );
  // Forward-declared so useResponsiveLayout can observe its width. The actual
  // ref attachment happens on <main> further down. Refs are stable across
  // renders, so we can pass it into a hook before the element exists; the
  // hook tolerates ref.current being null on the first render.
  const mainRef = useRef<HTMLElement>(null);
  // Responsive layout: on phones we render fewer columns (2 vs 3) and resize
  // each to fit. The clipped timelines stay in state — rotating to landscape
  // brings them back.
  const { isMobile, visibleColumnCount, columnWidth, axisWidth } =
    useResponsiveLayout(mainRef, DEFAULT_TIMELINE_NAMES.length);

  // Mobile-only: hamburger menu is open. On desktop, settings sit inline in
  // the header so this is always false there.
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  // Close the menu on outside tap / Escape.
  const menuRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!mobileMenuOpen) return;
    const onDocClick = (e: MouseEvent | TouchEvent) => {
      const target = e.target as Node | null;
      if (!target) return;
      if (menuRef.current && !menuRef.current.contains(target)) {
        setMobileMenuOpen(false);
      }
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setMobileMenuOpen(false);
    };
    // pointerdown beats click — closes before the underlying tap fires.
    document.addEventListener("pointerdown", onDocClick);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("pointerdown", onDocClick);
      document.removeEventListener("keydown", onKey);
    };
  }, [mobileMenuOpen]);
  // Auto-close the menu if the viewport grows back to desktop width.
  useEffect(() => {
    if (!isMobile && mobileMenuOpen) setMobileMenuOpen(false);
  }, [isMobile, mobileMenuOpen]);
  const [pixelsPerYear, setPixelsPerYear] = useState(DEFAULT_PIXELS_PER_YEAR);
  const [error, setError] = useState<string | null>(null);

  // Occurrence density (8-20). Higher = smaller boxes, more occurrences fit.
  const [occurrenceDensity, setOccurrenceDensity] = useState<number>(() => {
    const stored = Number(localStorage.getItem("occurrenceDensity"));
    if (Number.isFinite(stored) && stored >= MIN_DENSITY && stored <= MAX_DENSITY) {
      return stored;
    }
    return DEFAULT_DENSITY;
  });
  useEffect(() => {
    localStorage.setItem("occurrenceDensity", String(occurrenceDensity));
  }, [occurrenceDensity]);

  // Date display mode: how aggressively to show day/month inside boxes.
  //   "auto"   → adapt to zoom: day precision below 20yr span, year above
  //   "always" → always show day-month-year (degrading silently if missing)
  //   "never"  → always year-only
  const [dateDisplayMode, setDateDisplayMode] = useState<DateDisplayMode>(() => {
    const stored = localStorage.getItem("dateDisplayMode");
    if (stored === "always" || stored === "never" || stored === "auto") {
      return stored;
    }
    return "auto";
  });
  useEffect(() => {
    localStorage.setItem("dateDisplayMode", dateDisplayMode);
  }, [dateDisplayMode]);

  // Region-weight filter sliders. Persisted to localStorage so the user's
  // preferred regional emphasis carries between sessions.
  const [regionFilter, setRegionFilter] = useState<RegionWeights>(() => {
    try {
      const raw = localStorage.getItem("regionFilter");
      if (raw) {
        const parsed = JSON.parse(raw) as Partial<RegionWeights>;
        return { ...DEFAULT_REGION_FILTER, ...parsed };
      }
    } catch { /* fall through to default */ }
    return DEFAULT_REGION_FILTER;
  });
  useEffect(() => {
    localStorage.setItem("regionFilter", JSON.stringify(regionFilter));
  }, [regionFilter]);
  const [showRegionPanel, setShowRegionPanel] = useState(false);

  // Toggle for showing person full-lifespan occurrences (birth → death bars).
  // Default OFF — these bars are dense and the timeline reads better without
  // them, especially at low zoom. Periods within a person's life (presidency,
  // reign, etc.) are stored as type=event and continue to show regardless.
  const [showLifespans, setShowLifespans] = useState<boolean>(() => {
    return localStorage.getItem("showLifespans") === "true";
  });
  useEffect(() => {
    localStorage.setItem("showLifespans", String(showLifespans));
  }, [showLifespans]);

  // Flash-pulse trigger for the box a search just navigated to. `id` selects
  // which occurrence; `stamp` changes on every search so the same id can be
  // flashed again (the stamp restarts the CSS animation).
  const [flash, setFlash] = useState<{ id: number; stamp: number } | null>(null);

  // When the user clicks a column header we pop a TimelinePicker anchored to
  // that header. `columnIndex` is the position within `timelineNames` to swap
  // when the user picks a different timeline.
  const [picker, setPicker] = useState<
    { columnIndex: number; anchorRect: DOMRect; currentName: string } | null
  >(null);

  // After the user swaps the timeline in a column, the column should
  // auto-centre on its nearest occurrence (by year distance) if nothing it
  // contains is currently visible. `stamp` is a fresh value per swap so the
  // column knows when to re-check; `columnIndex` selects which column performs
  // the check.
  const [swapTarget, setSwapTarget] = useState<
    { columnIndex: number; stamp: number } | null
  >(null);

  // mainRef declared at top of component (so useResponsiveLayout can observe it).
  // After a zoom change, restore scroll so that `year` lines up with
  // `anchorPxFromTop` pixels below the viewport top. Centre-anchored zoom uses
  // anchorPxFromTop = clientHeight/2; cursor-anchored zoom (wheel/pinch) uses
  // the cursor's y position relative to the viewport top.
  const pendingAnchorRef = useRef<{ year: number; anchorPxFromTop: number } | null>(null);

  // Track the scroll viewport so children can decide what's visible.
  const [viewport, setViewport] = useState({ scrollTop: 0, clientHeight: 0 });

  useEffect(() => {
    const main = mainRef.current;
    if (!main) return;
    let rafId: number | null = null;
    const update = () => {
      if (rafId !== null) return;
      rafId = requestAnimationFrame(() => {
        setViewport({
          scrollTop: main.scrollTop,
          clientHeight: main.clientHeight,
        });
        rafId = null;
      });
    };
    update();
    main.addEventListener("scroll", update, { passive: true });
    const ro = new ResizeObserver(update);
    ro.observe(main);
    return () => {
      main.removeEventListener("scroll", update);
      ro.disconnect();
      if (rafId !== null) cancelAnimationFrame(rafId);
    };
  }, []);

  // Visible year range is auto-fitted to the full extent of the data
  // (oldest start_year through newest end-or-start year). The axis itself is
  // log-compressed (see `scale` below) so even billion-year ranges remain
  // scrollable.
  const [dataRange, setDataRange] = useState<{ min: number; max: number } | null>(null);
  const yearMin = dataRange?.min ?? FALLBACK_YEAR_MIN;
  const yearMax = dataRange?.max ?? FALLBACK_YEAR_MAX;

  useEffect(() => {
    let cancelled = false;
    (async () => {
      // Two ordered LIMIT 1 queries — cheaper than scanning min/max ourselves
      // and works with the existing Supabase REST API without an RPC.
      const minQ = supabase
        .from("occurrences")
        .select("start_year")
        .not("start_year", "is", null)
        .order("start_year", { ascending: true })
        .limit(1);
      const maxStartQ = supabase
        .from("occurrences")
        .select("start_year")
        .not("start_year", "is", null)
        .order("start_year", { ascending: false })
        .limit(1);
      const maxEndQ = supabase
        .from("occurrences")
        .select("end_year")
        .not("end_year", "is", null)
        .order("end_year", { ascending: false })
        .limit(1);
      const [minR, maxStartR, maxEndR] = await Promise.all([minQ, maxStartQ, maxEndQ]);
      if (cancelled) return;
      const minYear =
        (minR.data?.[0] as any)?.start_year ?? FALLBACK_YEAR_MIN;
      const maxStart = (maxStartR.data?.[0] as any)?.start_year ?? FALLBACK_YEAR_MAX;
      const maxEnd = (maxEndR.data?.[0] as any)?.end_year ?? maxStart;
      const maxYear = Math.max(maxStart, maxEnd, FALLBACK_YEAR_MAX);
      setDataRange({ min: minYear, max: maxYear });
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  // Log-compressed year ↔ pixel scale. Recomputed whenever the range or zoom
  // changes; children read yearToPx / pxToYear / localPpy through it.
  const scale = useMemo(
    () => makeYearScale(yearMin, yearMax, pixelsPerYear, LINEAR_RANGE_YEARS),
    [yearMin, yearMax, pixelsPerYear],
  );


  // Box height derived from desired occurrence density + viewport.
  // Falls back to the fixed default before the viewport has been measured.
  const eventBoxHeightPx = useMemo(() => {
    if (viewport.clientHeight <= 0) return DEFAULT_EVENT_BOX_HEIGHT_PX;
    return Math.round(viewport.clientHeight / occurrenceDensity);
  }, [viewport.clientHeight, occurrenceDensity]);

  // ----- hover popup state -------------------------------------------------
  const [hovered, setHovered] = useState<
    { event: EventWithPriority; rect: DOMRect } | null
  >(null);
  const popupRef = useRef<HTMLDivElement>(null);
  const openTimerRef = useRef<number | null>(null);
  const closeTimerRef = useRef<number | null>(null);
  const clearTimers = () => {
    if (openTimerRef.current)  { window.clearTimeout(openTimerRef.current);  openTimerRef.current = null; }
    if (closeTimerRef.current) { window.clearTimeout(closeTimerRef.current); closeTimerRef.current = null; }
  };
  // handleBoxEnter is called for BOTH mouse pointerenter (with delay, so
  // moving over a stack of boxes doesn't flicker) AND touch pointerdown.
  // For touch we want immediate open; for mouse the delay is fine. The
  // useHoverBinding hook routes them through the same callback, so we open
  // immediately here and let the close-delay handle anti-flicker.
  const handleBoxEnter: HoverHandler = (event, rect) => {
    clearTimers();
    setHovered({ event, rect });
  };
  const handleBoxLeave = () => {
    if (openTimerRef.current) { window.clearTimeout(openTimerRef.current); openTimerRef.current = null; }
    closeTimerRef.current = window.setTimeout(() => {
      setHovered(null);
    }, HOVER_CLOSE_DELAY_MS);
  };
  const handlePopupEnter = () => clearTimers();
  const handlePopupLeave = handleBoxLeave;
  // Outside-tap dismiss for touch users (the × button works too, but tapping
  // anywhere off the popup feels more natural than hunting for the close
  // button on a small screen).
  useEffect(() => {
    if (!hovered) return;
    const onDocPointerDown = (e: PointerEvent) => {
      if (e.pointerType === "mouse") return;     // desktop uses hover-leave
      const target = e.target as Node | null;
      if (!target) return;
      // Tap inside the popup → keep it open.
      if (popupRef.current && popupRef.current.contains(target)) return;
      // Tap on any event box → handleBoxEnter will swap the popup contents;
      // don't pre-emptively clear here, that would cancel the swap.
      const onAnotherBox = (target as Element).closest?.("[data-occurrence-box]");
      if (onAnotherBox) return;
      clearTimers();
      setHovered(null);
    };
    document.addEventListener("pointerdown", onDocPointerDown);
    return () => document.removeEventListener("pointerdown", onDocPointerDown);
  }, [hovered]);

  useEffect(() => {
    setError(null);
    // Skip DB fetch when the only requested name is the favourites sentinel.
    const realNames = timelineNames.filter((n) => n !== FAVOURITES_TIMELINE_NAME);
    if (realNames.length === 0) {
      setTimelines([]);
      return;
    }
    let cancelled = false;
    (async () => {
      const { data, error } = await supabase
        .from("timelines")
        .select("*")
        .in("name", realNames);
      if (cancelled) return;
      if (error) setError(error.message);
      else setTimelines(data ?? []);
    })();
    return () => {
      cancelled = true;
    };
  }, [timelineNames]);

  // Synthetic Timeline row for the favourites pseudo-timeline. Same shape as
  // a real timelines row so TimelineColumn can render it (with a custom
  // fetch path when timeline.slug === FAVOURITES_TIMELINE_SLUG).
  const favouritesTimeline: Timeline = useMemo(
    () => ({
      id: -1,
      name: FAVOURITES_TIMELINE_NAME,
      slug: FAVOURITES_TIMELINE_SLUG,
      display_order: -1,
      is_featured: false,
    }),
    [],
  );

  // Render the columns in the user-controlled order (timelineNames), not by
  // their DB display_order. The .in() query above returns rows in any order.
  // Clipped to visibleColumnCount so mobile shows 2 instead of 3 — the third
  // is still in timelineNames state and reappears at >= MOBILE_BREAKPOINT_PX.
  const orderedTimelines = useMemo(() => {
    const byName = new Map<string, Timeline>(timelines.map((t) => [t.name, t]));
    byName.set(FAVOURITES_TIMELINE_NAME, favouritesTimeline);
    return timelineNames
      .slice(0, visibleColumnCount)
      .map((n) => byName.get(n))
      .filter((t): t is Timeline => t != null);
  }, [timelines, timelineNames, visibleColumnCount, favouritesTimeline]);

  // Cross-timeline dedup: each non-master column reports the IDs it loaded;
  // we compute the union and pass it to any master column so that events
  // already visible in another lens are hidden from "worldwide:main".
  const [columnIds, setColumnIds] = useState<Record<number, number[]>>({});
  const handleColumnEventsLoaded = useCallback(
    (columnIndex: number, ids: number[]) => {
      setColumnIds((prev) => {
        const existing = prev[columnIndex];
        if (existing && existing.length === ids.length &&
            existing.every((v, i) => v === ids[i])) return prev;
        return { ...prev, [columnIndex]: ids };
      });
    },
    [],
  );
  const masterExcludeIds = useMemo(() => {
    const set = new Set<number>();
    orderedTimelines.forEach((t, idx) => {
      if (t.slug === "master") return;
      const ids = columnIds[idx];
      if (ids) for (const id of ids) set.add(id);
    });
    return set;
  }, [orderedTimelines, columnIds]);

  // ---- Programmatic scroll: centre the viewport on a given year -----------
  function scrollToYear(year: number) {
    const main = mainRef.current;
    if (!main) return;
    const centerPx = HEADER_HEIGHT_PX + scale.yearToPx(year);
    main.scrollTo({
      top: centerPx - main.clientHeight / 2,
      behavior: "smooth",
    });
  }

  // ---- Search handlers ----------------------------------------------------
  function handlePickYear(year: number) {
    scrollToYear(year);
  }

  function handlePickOccurrence(ev: HistoryEvent) {
    // Pick the year to centre on: explicit key year > period midpoint > start.
    let target: number | null = ev.key_year ?? null;
    if (target == null && ev.is_period && ev.start_year != null && ev.end_year != null) {
      target = Math.floor((ev.start_year + ev.end_year) / 2);
    }
    if (target == null) target = ev.start_year;

    // Make sure the timeline where this occurrence has the highest priority is
    // visible: if it isn't, swap it in for the rightmost column.
    if (ev.main_category && !timelineNames.includes(ev.main_category)) {
      setTimelineNames((prev) => {
        if (prev.length === 0) return [ev.main_category!];
        const next = prev.slice();
        next[next.length - 1] = ev.main_category!;
        return next;
      });
    }

    // Set zoom so the occurrence renders at its natural rollup level.
    // Without this, an umbrella period like the Hundred Years' War (a single
    // row spanning 1337-1453) is invisible at the user's current zoom: zoom
    // in and the umbrella is suppressed in favour of its leaf events; zoom
    // out and it gets collapsed into a higher-level rollup umbrella or
    // pushed off by higher-priority neighbours. Choose a target *visible*
    // span based on the occurrence's own span (matching the rollup
    // thresholds in TimelineColumn): leaves at <80yr, mid-period umbrellas
    // in the 80-800yr band, era-spanning umbrellas at ≥800yr.
    const main = mainRef.current;
    if (target != null && main) {
      const start = ev.start_year ?? target;
      const end = ev.end_year ?? start;
      const span = Math.max(0, end - start);
      const naturalLevel = span > 800 ? 2 : span > 10 ? 1 : 0;
      const targetVisibleSpan =
        naturalLevel === 2 ? Math.max(800, span * 1.5) :
        naturalLevel === 1 ? Math.max(80, span * 4) :
        40;
      const viewportH = Math.max(1, main.clientHeight - HEADER_HEIGHT_PX);
      // Convert desired local-ppy at the target year back to the linear-band
      // ppy `k` (the value held in pixelsPerYear). See yearScale.ts:
      //   linear band  (t ≤ L):  localPpy = k
      //   log band     (t > L):  localPpy = k * L / t
      const desiredLocalPpy = viewportH / targetVisibleSpan;
      const t = scale.yearMax - target;
      const L = scale.linearRange;
      const newPpy = t <= L ? desiredLocalPpy : (desiredLocalPpy * t) / L;
      const clamped = Math.max(MIN_PPY, Math.min(MAX_PPY, newPpy));

      if (Math.abs(clamped - pixelsPerYear) / Math.max(pixelsPerYear, clamped) > 0.05) {
        // Zoom is changing meaningfully. Pin the target year at viewport
        // centre across the change; the useLayoutEffect on `scale` will
        // adjust scrollTop once the new scale renders. No separate
        // scrollToYear call needed (and adding one races the layout effect).
        pendingAnchorRef.current = {
          year: target,
          anchorPxFromTop: main.clientHeight / 2,
        };
        setPixelsPerYear(clamped);
      } else {
        // Zoom is already in the right ballpark — smooth-scroll only.
        scrollToYear(target);
      }
    } else if (target != null) {
      scrollToYear(target);
    }

    setFlash({ id: ev.id, stamp: Date.now() });
  }

  // ---- Timeline picker handlers ------------------------------------------
  // Search-bar pick → swap the rightmost VISIBLE column. On desktop and
  // phone landscape that's column index 2 (3 cols rendered); on phone
  // portrait it's index 1 (2 cols rendered). Off-screen columns from
  // timelineNames stay parked in state — when the device rotates back, the
  // user gets them back rather than losing their setup.
  function handlePickTimelineFromSearch(timeline: Timeline) {
    const swapIndex = Math.max(0, visibleColumnCount - 1);
    setTimelineNames((prev) => {
      if (prev.length === 0) return [timeline.name];
      const next = prev.slice();
      // Ensure the array is long enough to address swapIndex. (Off-screen
      // slots beyond swapIndex stay where they were — only the visible
      // rightmost slot changes.)
      while (next.length <= swapIndex) next.push(next[next.length - 1] ?? "");
      // If the picked timeline is already in another column, swap them so
      // the user doesn't end up with duplicate columns.
      const existingIdx = next.indexOf(timeline.name);
      if (existingIdx >= 0 && existingIdx !== swapIndex) {
        next[existingIdx] = next[swapIndex];
      }
      next[swapIndex] = timeline.name;
      return next;
    });
    // After the swap, the new column will fetch its own events. Use the
    // existing swap-target mechanism so it auto-centres if nothing in the
    // new lens is currently in view.
    setSwapTarget({ columnIndex: swapIndex, stamp: Date.now() });
  }

  function handleHeaderClick(columnIndex: number, rect: DOMRect) {
    const currentName = timelineNames[columnIndex] ?? "";
    // Toggle off if the user clicks the same column header twice.
    if (picker && picker.columnIndex === columnIndex) {
      setPicker(null);
      return;
    }
    setPicker({ columnIndex, anchorRect: rect, currentName });
  }

  function handlePickTimeline(name: string) {
    if (!picker) return;
    const swappedIndex = picker.columnIndex;
    // Same name in the same slot — just close, don't trigger a recenter.
    if (timelineNames[swappedIndex] === name) {
      setPicker(null);
      return;
    }
    setTimelineNames((prev) => {
      const next = prev.slice();
      const existingIdx = next.indexOf(name);
      // If the chosen timeline is already in another column, swap the two
      // columns rather than ending up with duplicate columns.
      if (existingIdx >= 0) {
        next[existingIdx] = next[swappedIndex];
      }
      next[swappedIndex] = name;
      return next;
    });
    // Mark this column for an auto-centre check once its new events load.
    // The TimelineColumn for `swappedIndex` will look at its events after the
    // next fetch and, if none overlap the current viewport, ask us to scroll
    // to the nearest one.
    setSwapTarget({ columnIndex: swappedIndex, stamp: Date.now() });
    setPicker(null);
  }

  // Smooth-scroll target requested by a freshly-swapped column. We use the
  // same scrollToYear() helper as the search bar, which animates with
  // `behavior: "smooth"`. The column only invokes this when nothing it
  // contains is currently in view.
  function handleAutoCenter(year: number) {
    scrollToYear(year);
  }

  // Auto-clear the flash state after the animation has finished, so we don't
  // hold a stale reference around forever.
  useEffect(() => {
    if (!flash) return;
    const t = window.setTimeout(() => setFlash(null), 2200);
    return () => window.clearTimeout(t);
  }, [flash]);

  // ---- zoom that keeps an anchor year fixed at a given viewport y --------
  // anchorPxFromTop defaults to the viewport centre (used by the +/- buttons).
  // The wheel/pinch handler passes the cursor's y so the year under the cursor
  // stays put while the rest of the timeline expands/contracts around it.
  function setZoom(newPPY: number, anchorPxFromTop?: number) {
    const clamped = Math.max(MIN_PPY, Math.min(MAX_PPY, newPPY));
    const main = mainRef.current;
    if (main) {
      const anchorY = anchorPxFromTop ?? main.clientHeight / 2;
      const anchorScrollPx = main.scrollTop + anchorY;
      // events area starts HEADER_HEIGHT_PX below the scroll origin
      const anchorYear = scale.pxToYear(anchorScrollPx - HEADER_HEIGHT_PX);
      pendingAnchorRef.current = { year: anchorYear, anchorPxFromTop: anchorY };
    }
    setPixelsPerYear(clamped);
  }

  // After the DOM re-renders at the new zoom, restore the anchor year.
  useLayoutEffect(() => {
    const pending = pendingAnchorRef.current;
    if (pending == null) return;
    const main = mainRef.current;
    if (!main) return;
    const newAnchorPx = HEADER_HEIGHT_PX + scale.yearToPx(pending.year);
    main.scrollTop = newAnchorPx - pending.anchorPxFromTop;
    pendingAnchorRef.current = null;
  }, [scale]);

  // Adaptive zoom factor — bigger steps at higher zoom levels so the user can
  // actually reach the day-resolution end of the range without dozens of clicks.
  function zoomFactor(ppy: number): number {
    if (ppy < 100) return 1.5;
    if (ppy < 5_000) return 2;
    return 3;
  }
  const zoomIn = () => setZoom(pixelsPerYear * zoomFactor(pixelsPerYear));
  const zoomOut = () => setZoom(pixelsPerYear / zoomFactor(pixelsPerYear / 1.5));
  const zoomReset = () => setZoom(DEFAULT_PIXELS_PER_YEAR);

  // ---- wheel / trackpad-pinch zoom ----------------------------------------
  // On Mac and Windows, a trackpad pinch gesture is delivered as a wheel event
  // with ctrlKey=true (the browser would otherwise use it to magnify the
  // page). Ctrl+wheel from a real mouse also lands here. In both cases we
  // intercept and zoom the timeline instead, anchored at the cursor. Plain
  // mouse wheel falls through to the browser as a vertical scroll.
  //
  // Latest ppy/scale captured via refs so the listener (attached once) always
  // uses fresh values without re-binding on every render.
  const pixelsPerYearRef = useRef(pixelsPerYear);
  const scaleRef = useRef(scale);
  useEffect(() => { pixelsPerYearRef.current = pixelsPerYear; }, [pixelsPerYear]);
  useEffect(() => { scaleRef.current = scale; }, [scale]);

  useEffect(() => {
    const main = mainRef.current;
    if (!main) return;
    // ----- Pinch / Ctrl+wheel zoom -----------------------------------------
    // Trackpad pinch fires a burst of ctrlKey wheel events; the gesture also
    // emits subtle non-ctrl wheel events that the browser would scroll on.
    // To make the centre year truly stationary across the whole gesture we
    //   1. lock the anchor year ONCE at the start of the gesture and reuse
    //      it for every subsequent wheel in that gesture (no recompute from
    //      a possibly-perturbed scrollTop);
    //   2. listen on the document at *capture* phase so preventDefault runs
    //      before any descendant scroll handler or browser default;
    //   3. preventDefault on non-ctrl wheel events too while a pinch is
    //      active, so finger-drift doesn't scroll the timeline mid-zoom;
    //   4. also handle Safari's gestureXxx events for trackpad pinch on
    //      macOS Safari, which doesn't fire ctrl+wheel.
    const PINCH_TIMEOUT_MS = 250;
    let gestureAnchorYear: number | null = null;
    let gestureAnchorPxFromTop = 0;
    let lastPinchTs = 0;

    const beginGestureIfNeeded = (now: number) => {
      if (gestureAnchorYear != null && now - lastPinchTs < PINCH_TIMEOUT_MS) {
        return;
      }
      // New gesture — capture the year currently at the viewport centre.
      const anchorY = main.clientHeight / 2;
      const liveScale = scaleRef.current;
      gestureAnchorYear = liveScale.pxToYear(
        main.scrollTop + anchorY - HEADER_HEIGHT_PX,
      );
      gestureAnchorPxFromTop = anchorY;
    };

    const applyZoomStep = (factor: number) => {
      if (gestureAnchorYear == null) return;
      const stepClamped = Math.max(0.2, Math.min(5, factor));
      const currentPPY = pixelsPerYearRef.current;
      const newPPY = Math.max(
        MIN_PPY,
        Math.min(MAX_PPY, currentPPY * stepClamped),
      );
      if (newPPY === currentPPY) return;
      // Reuse the locked gesture anchor — DO NOT recompute from scrollTop,
      // which may have drifted mid-gesture.
      pendingAnchorRef.current = {
        year: gestureAnchorYear,
        anchorPxFromTop: gestureAnchorPxFromTop,
      };
      pixelsPerYearRef.current = newPPY;
      setPixelsPerYear(newPPY);
    };

    const onWheelCapture = (ev: WheelEvent) => {
      // Only act when the cursor is over our scroll container; otherwise let
      // the rest of the page behave normally.
      const target = ev.target as Node | null;
      if (!target || !main.contains(target)) return;

      const now = performance.now();
      if (ev.ctrlKey) {
        ev.preventDefault();
        beginGestureIfNeeded(now);
        lastPinchTs = now;
        // deltaY > 0 → zoom out; exp gives smooth feel for trackpad and Ctrl+wheel.
        applyZoomStep(Math.exp(-ev.deltaY * 0.01));
        return;
      }
      // Non-ctrl wheel: if we're mid-pinch, swallow it so finger-drift can't
      // scroll the viewport and shift the anchor.
      if (now - lastPinchTs < PINCH_TIMEOUT_MS) {
        ev.preventDefault();
        return;
      }
      // Otherwise leave it alone — normal vertical scroll.
    };

    // Safari (and any browser exposing the WebKit gesture API) fires these
    // for trackpad pinch instead of (or in addition to) ctrl+wheel.
    let lastGestureScale = 1;
    const onGestureStart = (ev: Event) => {
      const target = ev.target as Node | null;
      if (!target || !main.contains(target)) return;
      ev.preventDefault();
      lastPinchTs = performance.now();
      lastGestureScale = 1;
      beginGestureIfNeeded(lastPinchTs);
    };
    const onGestureChange = (ev: Event & { scale?: number }) => {
      const target = ev.target as Node | null;
      if (!target || !main.contains(target)) return;
      ev.preventDefault();
      const scaleFactor = ev.scale ?? 1;
      if (scaleFactor <= 0) return;
      lastPinchTs = performance.now();
      const delta = scaleFactor / lastGestureScale;
      lastGestureScale = scaleFactor;
      applyZoomStep(delta);
    };
    const onGestureEnd = (_ev: Event) => {
      lastGestureScale = 1;
      // Don't immediately null the gesture anchor — let the PINCH_TIMEOUT_MS
      // window expire so any trailing wheel events from the same gesture
      // still hit the same anchor year.
    };

    // ----- Touch pinch zoom (Android / iOS, two-finger gesture) ------------
    // The Safari `gesture*` events above don't fire on Android Chrome, and
    // there's no ctrl+wheel from touch — only TouchEvents. Mirror the same
    // zoom-anchored-at-a-fixed-year model:
    //   1. On 2-finger touchstart, lock the anchor year at the midpoint of
    //      the two fingers (not viewport centre — that's the standard
    //      Maps/Photos feel).
    //   2. On touchmove, ratio current finger distance to initial distance,
    //      then apply incremental scale deltas via applyZoomStep.
    //   3. Touchend with <2 fingers clears the pinch state; the
    //      PINCH_TIMEOUT_MS window keeps the locked gestureAnchor alive
    //      briefly to absorb trailing wheel events.
    //   4. preventDefault on 2-finger touchmove only — single-finger
    //      scrolling continues to work normally for navigating the timeline.
    let touchInitialDistance = 0;
    let touchLastScale = 1;
    let touchPinchActive = false;

    const distanceBetween = (a: Touch, b: Touch) =>
      Math.hypot(a.clientX - b.clientX, a.clientY - b.clientY);
    const midpointY = (a: Touch, b: Touch) => (a.clientY + b.clientY) / 2;

    const onTouchStart = (ev: TouchEvent) => {
      if (ev.touches.length < 2) return;     // 1-finger: let browser scroll
      const target = ev.target as Node | null;
      if (!target || !main.contains(target)) return;
      // Claim the gesture immediately. Without this, Android may decide the
      // 2-finger touch is a y-pan (per touch-action: pan-y) before our
      // touchmove fires, and never deliver moves to us — which is the
      // "one-handed pinch sometimes doesn't react" symptom.
      ev.preventDefault();
      const t1 = ev.touches[0];
      const t2 = ev.touches[1];
      touchInitialDistance = distanceBetween(t1, t2);
      touchLastScale = 1;
      touchPinchActive = true;
      // Map the midpoint y from window coords to scroll-container coords,
      // then to a year via the live scale. This becomes the zoom anchor.
      const mainRect = main.getBoundingClientRect();
      const anchorPxInViewport = midpointY(t1, t2) - mainRect.top;
      const liveScale = scaleRef.current;
      gestureAnchorYear = liveScale.pxToYear(
        main.scrollTop + anchorPxInViewport - HEADER_HEIGHT_PX,
      );
      gestureAnchorPxFromTop = anchorPxInViewport;
      lastPinchTs = performance.now();
    };

    const onTouchMove = (ev: TouchEvent) => {
      if (!touchPinchActive || ev.touches.length < 2) return;
      if (touchInitialDistance <= 0) return;
      const target = ev.target as Node | null;
      if (!target || !main.contains(target)) return;
      ev.preventDefault();   // suppress browser native pinch-to-zoom-page
      const t1 = ev.touches[0];
      const t2 = ev.touches[1];
      const dist = distanceBetween(t1, t2);
      if (dist <= 0) return;
      const totalScale = dist / touchInitialDistance;
      const delta = totalScale / touchLastScale;
      touchLastScale = totalScale;
      lastPinchTs = performance.now();
      applyZoomStep(delta);
    };

    const endTouchPinch = () => {
      touchPinchActive = false;
      touchInitialDistance = 0;
      touchLastScale = 1;
      // Leave gestureAnchorYear alone — PINCH_TIMEOUT_MS handles it.
    };
    const onTouchEnd = (ev: TouchEvent) => {
      if (ev.touches.length < 2) endTouchPinch();
    };

    document.addEventListener("wheel", onWheelCapture, {
      passive: false,
      capture: true,
    });
    main.addEventListener("gesturestart", onGestureStart as EventListener);
    main.addEventListener("gesturechange", onGestureChange as EventListener);
    main.addEventListener("gestureend", onGestureEnd as EventListener);
    // touchstart MUST be non-passive so preventDefault on 2-finger taps
    // actually works (passive listeners can't cancel events).
    main.addEventListener("touchstart", onTouchStart, { passive: false });
    main.addEventListener("touchmove",  onTouchMove,  { passive: false });
    main.addEventListener("touchend",   onTouchEnd);
    main.addEventListener("touchcancel", onTouchEnd);
    return () => {
      document.removeEventListener("wheel", onWheelCapture, { capture: true });
      main.removeEventListener("gesturestart", onGestureStart as EventListener);
      main.removeEventListener("gesturechange", onGestureChange as EventListener);
      main.removeEventListener("gestureend", onGestureEnd as EventListener);
      main.removeEventListener("touchstart", onTouchStart);
      main.removeEventListener("touchmove",  onTouchMove);
      main.removeEventListener("touchend",   onTouchEnd);
      main.removeEventListener("touchcancel", onTouchEnd);
    };
  }, []);

  // Format the zoom button label to give a useful unit at high zoom levels.
  function zoomLabel(ppy: number): string {
    if (ppy >= 10_000) {
      const pxPerDay = ppy / 365.25;
      return `${pxPerDay.toFixed(0)} px/day`;
    }
    if (ppy >= 100) return `${Math.round(ppy)} px/yr`;
    return `${ppy.toFixed(2)} px/yr`;
  }

  if (error) {
    return (
      <div className="p-6 text-red-300">
        <h1 className="text-xl font-semibold mb-2">Database error</h1>
        <pre className="whitespace-pre-wrap text-sm">{error}</pre>
        <p className="mt-4 text-slate-400 text-sm">
          Check that VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY are set in .env,
          and that the migration has run.
        </p>
      </div>
    );
  }

  // ----- pieces shared between the desktop header and the mobile menu -------
  const densityControl = (
    <label
      className="flex items-center gap-1 text-slate-400"
      title="Occurrences shown per timeline (smaller = more fit)"
    >
      <span>Density</span>
      <input
        type="range"
        min={MIN_DENSITY}
        max={MAX_DENSITY}
        step={1}
        value={occurrenceDensity}
        onChange={(e) => setOccurrenceDensity(Number(e.target.value))}
        className="w-24"
      />
      <span className="tabular-nums w-6 text-slate-800 dark:text-slate-200">{occurrenceDensity}</span>
    </label>
  );

  const dateModeControl = (
    <label
      className="flex items-center gap-1 text-slate-400"
      title="Show day & month inside occurrence boxes"
    >
      <span>Dates</span>
      <select
        value={dateDisplayMode}
        onChange={(e) => setDateDisplayMode(e.target.value as DateDisplayMode)}
        className="bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded px-1 py-0.5 text-slate-800 dark:text-slate-200"
      >
        <option value="auto">Auto</option>
        <option value="always">Always</option>
        <option value="never">Never</option>
      </select>
    </label>
  );

  const lifespansToggle = (
    <button
      onClick={() => setShowLifespans((v) => !v)}
      title="Show or hide person full-lifespan bars (birth → death)"
      className={`px-2 py-1 rounded border border-slate-200 dark:border-slate-700 ${
        showLifespans ? "bg-slate-200 dark:bg-slate-700 text-slate-900 dark:text-slate-100" : "hover:bg-slate-100 dark:hover:bg-slate-800"
      }`}
    >
      Lifespans
    </button>
  );

  const themeToggle = (
    <button
      onClick={toggleTheme}
      title={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
      aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
      className="px-2 py-1 rounded border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 flex items-center gap-1.5"
    >
      <span aria-hidden>{theme === "dark" ? "☀" : "☾"}</span>
      <span>{theme === "dark" ? "Light" : "Dark"}</span>
    </button>
  );

  const regionsToggle = (
    <button
      onClick={() => setShowRegionPanel((v) => !v)}
      title="Adjust regional emphasis for Worldwide & Arts/Thoughts timelines"
      className={`px-2 py-1 rounded border border-slate-200 dark:border-slate-700 ${
        showRegionPanel ? "bg-slate-200 dark:bg-slate-700 text-slate-900 dark:text-slate-100" : "hover:bg-slate-100 dark:hover:bg-slate-800"
      }`}
    >
      Regions
    </button>
  );

  const regionPanel = (
    <div className="flex flex-wrap items-center gap-3 text-xs">
      <span className="text-slate-400 w-full md:w-auto">
        Regional emphasis (Worldwide &amp; Arts/Thoughts only):
      </span>
      {REGIONS.map((r) => (
        <label key={r.key} className="flex items-center gap-1 text-slate-700 dark:text-slate-300">
          <span className="w-20">{r.label}</span>
          <input
            type="range"
            min={0}
            max={10}
            step={1}
            value={regionFilter[r.key]}
            onChange={(e) =>
              setRegionFilter((prev) => ({
                ...prev,
                [r.key]: Number(e.target.value),
              }))
            }
            className="w-24"
          />
          <span className="tabular-nums w-5 text-slate-800 dark:text-slate-200">
            {regionFilter[r.key]}
          </span>
        </label>
      ))}
      <button
        onClick={() => setRegionFilter(DEFAULT_REGION_FILTER)}
        className="px-2 py-0.5 rounded border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-400"
      >
        Reset
      </button>
    </div>
  );

  const zoomButtons = (
    <div className="flex items-center gap-1 text-xs">
      <button
        onClick={zoomOut}
        title="Zoom out"
        className="px-2 py-1 rounded border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800"
      >
        −
      </button>
      {/* Reset/label only fits on desktop — moves into the mobile menu. */}
      <button
        onClick={zoomReset}
        title="Reset zoom"
        className="hidden md:inline-block px-2 py-1 rounded border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 min-w-[90px]"
      >
        {zoomLabel(pixelsPerYear)}
      </button>
      <button
        onClick={zoomIn}
        title="Zoom in"
        className="px-2 py-1 rounded border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800"
      >
        +
      </button>
    </div>
  );

  return (
    <div className="h-full flex flex-col">
      <header className="sticky top-0 z-40 flex-shrink-0 px-3 md:px-4 py-3 border-b border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 flex items-center gap-2 md:gap-3">
        {/* Title is presentational only; hidden on mobile to free horizontal
            space. The launcher icon and PWA name already identify the app. */}
        <h1 className="hidden md:block text-lg font-semibold flex-shrink-0">
          Ever-When
        </h1>

        {/* Search bar takes whatever room is left. */}
        <div className="flex-1 min-w-0">
          <SearchBar
            showLifespans={showLifespans}
            onPickYear={handlePickYear}
            onPickOccurrence={handlePickOccurrence}
            onPickTimeline={handlePickTimelineFromSearch}
          />
        </div>

        {/* Desktop-only inline settings. Hidden via md:flex on phones. */}
        <div className="hidden md:flex items-center gap-3 text-xs">
          {densityControl}
          {dateModeControl}
          {lifespansToggle}
          {regionsToggle}
          {themeToggle}
        </div>

        {/* Account button — sign in / sign out. Shown on desktop alongside
            zoom buttons; on mobile it lives inside the hamburger menu below. */}
        <div className="hidden md:flex">
          {user ? (
            <button
              type="button"
              onClick={() => signOut()}
              title={`Signed in as ${user.email ?? "user"} — click to sign out`}
              className="text-xs px-2 py-1 rounded border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300"
            >
              Sign out
            </button>
          ) : (
            <button
              type="button"
              onClick={() => setAuthModalOpen(true)}
              className="text-xs px-2 py-1 rounded border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300"
            >
              Sign in
            </button>
          )}
        </div>

        {zoomButtons}

        {/* Hamburger menu — phone only. */}
        <button
          type="button"
          onClick={() => setMobileMenuOpen((v) => !v)}
          aria-label={mobileMenuOpen ? "Close menu" : "Open menu"}
          aria-expanded={mobileMenuOpen}
          className={`md:hidden flex items-center justify-center w-9 h-9 rounded border border-slate-200 dark:border-slate-700 ${
            mobileMenuOpen ? "bg-slate-200 dark:bg-slate-700 text-slate-900 dark:text-slate-100" : "hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300"
          }`}
        >
          <span aria-hidden className="text-lg leading-none">
            {mobileMenuOpen ? "×" : "≡"}
          </span>
        </button>
      </header>

      {/* Mobile menu panel — drops below the header when ≡ is tapped. The
          ref + useEffect above close it on outside tap / Escape. */}
      {mobileMenuOpen && (
        <div
          ref={menuRef}
          className="md:hidden sticky top-[61px] z-30 flex-shrink-0 px-3 py-3 border-b border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 shadow-lg"
        >
          <div className="flex flex-col gap-3 text-xs">
            {densityControl}
            {dateModeControl}
            <div className="flex items-center gap-2 flex-wrap">
              {lifespansToggle}
              {regionsToggle}
              {themeToggle}
              <button
                onClick={zoomReset}
                title="Reset zoom"
                className="px-2 py-1 rounded border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 ml-auto"
              >
                Reset {zoomLabel(pixelsPerYear)}
              </button>
            </div>
            {showRegionPanel && (
              <div className="pt-2 border-t border-slate-200 dark:border-slate-800">{regionPanel}</div>
            )}
            <div className="pt-2 border-t border-slate-200 dark:border-slate-800">
              {user ? (
                <div className="flex items-center justify-between gap-2">
                  <span className="text-slate-400 truncate">
                    {user.email ?? "Signed in"}
                  </span>
                  <button
                    type="button"
                    onClick={() => { signOut(); setMobileMenuOpen(false); }}
                    className="shrink-0 px-2 py-1 rounded border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300"
                  >
                    Sign out
                  </button>
                </div>
              ) : (
                <button
                  type="button"
                  onClick={() => { setAuthModalOpen(true); setMobileMenuOpen(false); }}
                  className="w-full px-2 py-1 rounded border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300"
                >
                  Sign in / Sign up
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Desktop: when Regions toggled on, slide out the panel inline below
          the header (the original behaviour). Phones see this inside the
          mobile menu panel instead, so don't double-render here. */}
      {showRegionPanel && !isMobile && (
        <div className="px-4 py-2 border-b border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900">
          {regionPanel}
        </div>
      )}

      <main
        ref={mainRef}
        className="flex-1 overflow-y-auto overflow-x-hidden"
        // touch-action: pan-y allows finger drag to scroll vertically through
        // years; the gesture handlers below intercept 2-finger touches for
        // pinch zoom. overflow-x-hidden enforces the "single page view, no
        // horizontal scroll" mobile constraint — the column-count formula
        // already guarantees no overflow, this just defends against bugs.
        style={{ touchAction: "pan-y" }}
      >
        <div className="flex items-start">
          <YearAxis
            scale={scale}
            viewportScrollTop={viewport.scrollTop}
            viewportClientHeight={viewport.clientHeight}
            width={axisWidth}
          />
          {orderedTimelines.map((t, idx) => (
            <TimelineColumn
              key={t.id}
              timeline={t}
              columnIndex={idx}
              columnWidth={columnWidth}
              scale={scale}
              viewportScrollTop={viewport.scrollTop}
              viewportClientHeight={viewport.clientHeight}
              boxHeightPx={eventBoxHeightPx}
              regionFilter={regionFilter}
              dateDisplayMode={dateDisplayMode}
              showLifespans={showLifespans}
              onBoxEnter={handleBoxEnter}
              onBoxLeave={handleBoxLeave}
              onHeaderClick={handleHeaderClick}
              swapStamp={
                swapTarget && swapTarget.columnIndex === idx
                  ? swapTarget.stamp
                  : null
              }
              onAutoCenter={handleAutoCenter}
              flash={flash}
              onEventsLoaded={handleColumnEventsLoaded}
              excludeIds={t.slug === "master" ? masterExcludeIds : null}
              favouriteIds={favouriteIds}
              isFavourite={isFavourite}
              userId={user?.id ?? null}
            />
          ))}
        </div>
      </main>

      {hovered && (
        <EventPopup
          ref={popupRef}
          event={hovered.event}
          anchorRect={hovered.rect}
          onMouseEnter={handlePopupEnter}
          onMouseLeave={handlePopupLeave}
          onClose={() => { clearTimers(); setHovered(null); }}
          onFavourited={(ev) => {
            // Close the hover popup and open the suggestions modal.
            clearTimers();
            setHovered(null);
            setSuggestionSeed(ev);
          }}
          onSignInRequest={() => {
            clearTimers();
            setHovered(null);
            setAuthModalOpen(true);
          }}
        />
      )}

      {picker && (
        <TimelinePicker
          currentName={picker.currentName}
          anchorRect={picker.anchorRect}
          onPick={handlePickTimeline}
          onClose={() => setPicker(null)}
          showFavourites={user != null}
        />
      )}

      {authModalOpen && (
        <AuthModal onClose={() => setAuthModalOpen(false)} />
      )}

      {suggestionSeed && (
        <SuggestionsPopup
          seed={suggestionSeed}
          onClose={() => setSuggestionSeed(null)}
          onPickOccurrence={(occ) => {
            // Reuse the existing search-pick handler — it navigates the
            // timeline to the occurrence's year and flashes its box.
            handlePickOccurrence(occ as HistoryEvent);
          }}
        />
      )}
    </div>
  );
}

// ----- Year axis (gutter on the left) ---------------------------------------
// Ticks are generated from the log-compressed scale: local pixels-per-year
// determines a local "nice" year-step, so ticks are dense near today and
// sparse in deep-time bands — all without the user having to switch modes.
//
// When the viewport zooms in tight enough to span a single year (or less) the
// ticks switch to months; tighter still and they switch to days. This works
// out of the box with the existing scale because yearToPx accepts fractional
// years (Feb 1950 → 1950 + 1/12).
function YearAxis({
  scale,
  viewportScrollTop,
  viewportClientHeight,
  width,
}: {
  scale: YearScale;
  viewportScrollTop: number;
  viewportClientHeight: number;
  /** Responsive: 72px on desktop, 48px on phones. */
  width: number;
}) {
  // Year-mode ticks across the whole timeline (cheap to recompute, scale-keyed).
  const yearTicks = useMemo(() => generateLogTicks(scale, 80, 500), [scale]);

  // Sub-year ticks only become visible inside a window around the viewport.
  // Compute the visible year-span and switch granularity at < 2 yr (months)
  // and < ~3 months (days).
  const subTicks = useMemo(() => {
    if (viewportClientHeight <= 0) return null;
    const yTop = scale.pxToYear(viewportScrollTop - HEADER_HEIGHT_PX);
    const yBottom = scale.pxToYear(
      viewportScrollTop + viewportClientHeight - HEADER_HEIGHT_PX,
    );
    const span = Math.max(0, yTop - yBottom);
    if (yBottom < 1) return null;            // months/days not used in BCE
    if (span < 0.25) {
      return { kind: "day" as const, ticks: generateDayTicks(scale, yBottom, yTop) };
    }
    if (span < 2) {
      return { kind: "month" as const, ticks: generateMonthTicks(scale, yBottom, yTop) };
    }
    return null;
  }, [scale, viewportScrollTop, viewportClientHeight]);

  return (
    <div
      className="flex-shrink-0 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-700"
      style={{ width }}
    >
      <div
        className="sticky top-0 z-30 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-700 flex items-center px-2"
        style={{ height: HEADER_HEIGHT_PX }}
      >
        <span className="text-[10px] text-slate-500">
          {subTicks?.kind === "day"
            ? "Day"
            : subTicks?.kind === "month"
              ? "Month"
              : "Year"}
        </span>
      </div>
      <div className="relative" style={{ height: scale.totalHeight }}>
        {/* Year ticks always present — gives the gutter structure when
            scrolling above/below the sub-year zoom region. */}
        {yearTicks.map((y) => {
          const top = scale.yearToPx(y);
          return (
            <div
              key={`y-${y}`}
              className="absolute left-0 right-0 flex items-center"
              style={{ top }}
            >
              <span className="text-[10px] text-slate-400 pr-1">
                {compactYearLabel(y)}
              </span>
              <div className="h-px bg-slate-200 dark:bg-slate-700 flex-1" />
            </div>
          );
        })}
        {/* Sub-year ticks overlaid only inside the deep-zoom region. */}
        {subTicks?.ticks.map((t) => {
          const top = scale.yearToPx(t.fracYear);
          return (
            <div
              key={`s-${t.fracYear}`}
              className="absolute left-0 right-0 flex items-center"
              style={{ top }}
            >
              <span
                className={`text-[10px] pr-1 ${t.isMajor ? "text-slate-700 dark:text-slate-300 font-medium" : "text-slate-500"}`}
              >
                {t.label}
              </span>
              <div
                className={`h-px flex-1 ${t.isMajor ? "bg-slate-600" : "bg-slate-50 dark:bg-slate-800"}`}
              />
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ----- Item: every occurrence reduced to anchor + range info ----------------
// A "point" event is just a period whose start == end == key. Unifying them
// simplifies the placement loop.
type Item = {
  event: EventWithPriority;
  startYear: number;
  endYear: number;     // = startYear for points
  /** Fractional year at which the box would ideally anchor. For low-precision
   *  dates (year-only, month-only) this is the centre of the unknown window
   *  (mid-year, mid-month) so it doesn't all stack on 1 Jan. */
  keyYear: number;
  /** Lower bound of the placement window in fractional years — set to keyYear
   *  for fully-precise dates so there's no precision-driven flex. */
  keyMinYear: number;
  /** Upper bound of the placement window in fractional years. */
  keyMaxYear: number;
  isPeriod: boolean;
  priority: number;
};

// Days-in-month with leap-year awareness (matches yearScale's helper).
function _daysInMonth(year: number, month: number): number {
  return new Date(year, month, 0).getDate();
}
function _daysInYear(year: number): number {
  const isLeap = (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0;
  return isLeap ? 366 : 365;
}
/** day-of-year (0-indexed) for the first day of `month` in `year`. */
function _doyOfMonthStart(year: number, month: number): number {
  let d = 0;
  for (let m = 1; m < month; m++) d += _daysInMonth(year, m);
  return d;
}

function expandToItems(events: EventWithPriority[]): Item[] {
  const items: Item[] = [];
  for (const e of events) {
    if (e.start_year == null) continue;
    const isPeriod =
      e.is_period && e.end_year != null && e.end_year !== e.start_year;
    const start = e.start_year;
    const end = isPeriod ? e.end_year! : e.start_year;

    // Decide which fields drive the key date and its precision.
    // - If key_year is set, use the key_* fields' precision.
    // - Otherwise for point events fall back to start_* precision.
    // - For periods with no key, the midpoint is by construction year-only.
    let keyYearInt: number;
    let keyMonth: number | null;
    let keyDay: number | null;
    if (e.key_year != null) {
      keyYearInt = e.key_year;
      keyMonth = e.key_month;
      keyDay = e.key_day;
    } else if (!isPeriod) {
      keyYearInt = start;
      keyMonth = e.start_month;
      keyDay = e.start_day;
    } else {
      keyYearInt = Math.floor((start + end) / 2);
      keyMonth = null;
      keyDay = null;
    }

    // Compute the placement window from precision. Year-only → anywhere in the
    // year; month-only → anywhere in the month; day-precision → no flex from
    // precision (item-2 ±50% box-height nudge still applies in the placement
    // loop). The keyYear sits in the middle of the window so the box doesn't
    // default to 1 Jan / 1st of month.
    let keyYear: number;
    let keyMinYear: number;
    let keyMaxYear: number;
    const dpy = _daysInYear(keyYearInt);
    if (keyMonth == null) {
      // Year-only precision.
      keyMinYear = keyYearInt;
      keyMaxYear = keyYearInt + (dpy - 1) / dpy;       // Dec 31
      keyYear = keyYearInt + ((dpy / 2) | 0) / dpy;    // ~1 Jul
    } else if (keyDay == null) {
      // Month-only precision.
      const dom = _daysInMonth(keyYearInt, keyMonth);
      const doyStart = _doyOfMonthStart(keyYearInt, keyMonth);
      keyMinYear = keyYearInt + doyStart / dpy;
      keyMaxYear = keyYearInt + (doyStart + dom - 1) / dpy;
      keyYear = keyYearInt + (doyStart + ((dom / 2) | 0)) / dpy;
    } else {
      // Day precision — exact fractional year, no flex range.
      const doy = _doyOfMonthStart(keyYearInt, keyMonth) + (keyDay - 1);
      keyYear = keyYearInt + doy / dpy;
      keyMinYear = keyYear;
      keyMaxYear = keyYear;
    }

    // Item 6 — for periods, expand the placement window to the whole period
    // [start_year, end_year]. The key year still acts as the gravity centre
    // of the search (findFreeSlot starts there), but if it collides the box
    // may roam anywhere inside the period to fit higher-priority neighbours.
    if (isPeriod) {
      keyMinYear = Math.min(keyMinYear, start);
      keyMaxYear = Math.max(keyMaxYear, end);
    }

    items.push({
      event: e,
      startYear: start,
      endYear: end,
      keyYear,
      keyMinYear,
      keyMaxYear,
      isPeriod,
      priority: e.priority ?? 0,
    });
  }
  return items;
}

// Anchor a box can land on. "key" is preferred; "start"/"end" are fallbacks
// used when the key date has scrolled out of view but a range endpoint hasn't.
type AnchorKind = "key" | "start" | "end";

// What we actually render after viewport-aware placement + collision filtering.
type Placed = {
  event: EventWithPriority;
  anchorTop: number;       // px y of the box's top edge in events-div coords
  anchorKind: AnchorKind;
  startTop: number;        // px y for the start year (line endpoint, older = larger)
  endTop: number;          // px y for the end year   (line endpoint, newer = smaller)
  isPeriod: boolean;
  lineTrack: number;       // 0 = centre; only meaningful when isPeriod
  /** When true, the period range line is suppressed at render time. Set
   *  during the stagger pass when other occurrence boxes vertically overlap
   *  this period's line — the line would just be visual noise crossing
   *  through unrelated entries. */
  hideLine: boolean;
  color: OccurrenceColor;
};

// ----- Single timeline column ------------------------------------------------
function TimelineColumn({
  timeline, columnIndex, columnWidth, scale,
  viewportScrollTop, viewportClientHeight,
  boxHeightPx, regionFilter,
  dateDisplayMode,
  showLifespans,
  onBoxEnter, onBoxLeave,
  onHeaderClick,
  swapStamp, onAutoCenter,
  flash,
  onEventsLoaded,
  excludeIds,
  favouriteIds,
  isFavourite,
  userId,
}: {
  timeline: Timeline;
  columnIndex: number;
  /** Width of this column in CSS pixels. Responsive: ~288 on desktop, ~144 on
   *  a 360px phone. Affects both the rendered <section> width and where the
   *  multi-track range lines sit horizontally. */
  columnWidth: number;
  scale: YearScale;
  viewportScrollTop: number; viewportClientHeight: number;
  boxHeightPx: number;
  regionFilter: RegionWeights;
  dateDisplayMode: DateDisplayMode;
  showLifespans: boolean;
  onBoxEnter: HoverHandler;
  onBoxLeave: () => void;
  onHeaderClick: (columnIndex: number, rect: DOMRect) => void;
  /** Stamp set by the parent whenever this column was just swapped. When it
   *  changes, we check whether any of the new occurrences overlap the
   *  viewport and, if not, ask the parent to scroll to the nearest one. */
  swapStamp: number | null;
  onAutoCenter: (year: number) => void;
  flash: { id: number; stamp: number } | null;
  /** Called whenever this column finishes loading events, with the loaded
   *  event IDs. Used by the parent to compute cross-column exclusions. */
  onEventsLoaded?: (columnIndex: number, ids: number[]) => void;
  /** Event IDs to suppress from this column. Used for cross-timeline dedup
   *  (the master column hides events already shown in another visible
   *  column). null/undefined = no exclusion. */
  excludeIds?: Set<number> | null;
  /** Current user's favourite occurrence IDs. Triggers a re-fetch on the
   *  favourites pseudo-timeline when the set changes. */
  favouriteIds: Set<number>;
  isFavourite: (id: number) => boolean;
  userId: string | null;
}) {
  const { yearMin, yearMax, totalHeight } = scale;
  const [events, setEvents] = useState<EventWithPriority[]>([]);
  // Hysteresis: remember the fractional year each occurrence was placed at
  // last render so we can prefer the same position on scroll/zoom. Stored as
  // year (not px) so the cache survives zoom changes — pxToYear is reapplied
  // on each render against the current scale.
  const priorAnchorYearsRef = useRef<Map<number, number>>(new Map());

  // Region weighting only modulates the ranking on a subset of timelines (the
  // worldwide and arts-and-thoughts "main" views). For everything else we keep
  // priorities exactly as the DB returns them.
  const regionWeighted = REGION_WEIGHTED_SLUGS.has(timeline.slug);

  const isFavouritesTimeline = timeline.slug === FAVOURITES_TIMELINE_SLUG;
  // Snapshot of favourite IDs we last fetched on — re-run fetch only when the
  // set changes (Set identity changes on every toggle).
  const favIdsKey = useMemo(
    () => (isFavouritesTimeline ? Array.from(favouriteIds).sort((a, b) => a - b).join(",") : ""),
    [favouriteIds, isFavouritesTimeline],
  );

  useEffect(() => {
    (async () => {
      // --- Favourites pseudo-timeline ---------------------------------------
      // Fetch occurrences by ID from the user's favourites Set. Skip when
      // signed out (no favourites possible) or when the set is empty.
      if (isFavouritesTimeline) {
        if (!userId || favouriteIds.size === 0) {
          setEvents([]);
          if (onEventsLoaded) onEventsLoaded(columnIndex, []);
          return;
        }
        const idsArr = Array.from(favouriteIds);
        const { data, error } = await supabase
          .from("occurrences")
          .select("*")
          .in("id", idsArr);
        if (error) { console.error(error); return; }
        // No priority column to sort by — fabricate a constant priority of
        // 100_000 so every favourite shares the same baseline; the placement
        // loop falls back to year/precision for ordering.
        const rows = (data ?? []).map((r: any) => ({
          ...normalizeOngoing(r),
          priority: 100_000,
        })) as EventWithPriority[];
        setEvents(rows);
        if (onEventsLoaded) onEventsLoaded(columnIndex, rows.map((r) => r.id));
        return;
      }

      const { data, error } = await supabase
        .from("occurrence_timeline_priorities")
        .select("priority, occurrences!inner(*)")
        .eq("timeline_id", timeline.id)
        .lte("occurrences.start_year", yearMax)
        .order("priority", { ascending: false })
        .limit(1000);

      if (error) { console.error(error); return; }

      // normalizeOngoing substitutes end_year = current year for occurrences
      // flagged as still going (e.g. Charles III's reign). Doing it once at
      // fetch time means the placement code can treat them as ordinary
      // periods; the display_date label was set to "<start>–present" by the
      // importer so the visible UI stays accurate.
      const rows = (data ?? []).map((r: any) => ({
        ...normalizeOngoing(r.occurrences),
        priority: r.priority,
      })) as EventWithPriority[];
      setEvents(rows);
      if (onEventsLoaded) {
        onEventsLoaded(columnIndex, rows.map((r) => r.id));
      }
    })();
    // onEventsLoaded is intentionally omitted from deps — it's a stable
    // callback from the parent and we only want the fetch to re-run on
    // timeline/year-range changes.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [timeline.id, timeline.slug, yearMin, yearMax, columnIndex, userId, favIdsKey]);

  // ----- Auto-centre on the nearest occurrence after a swap ---------------
  // When the user picks a new timeline for this column, the parent passes us
  // a fresh `swapStamp`. After the new events arrive we check: does anything
  // in this timeline overlap the current viewport? If yes, do nothing. If no,
  // find the occurrence whose anchor year is closest to the viewport's centre
  // year and ask the parent to smooth-scroll to it.
  //
  // We use a ref so we only run once per stamp — viewport scroll changes etc.
  // shouldn't retrigger the check. A swap to a timeline that returns zero
  // rows simply does nothing (we wait for events to arrive, which they never
  // will, but no harm done).
  const handledSwapStampRef = useRef<number | null>(null);
  useEffect(() => {
    if (swapStamp == null) return;
    if (handledSwapStampRef.current === swapStamp) return;
    if (events.length === 0) return;
    if (viewportClientHeight <= 0) return;
    handledSwapStampRef.current = swapStamp;

    // Convert the viewport pixel range to a year range. Newer years sit at
    // smaller y, so the "top" year of the viewport is the *larger* number.
    const yTop = scale.pxToYear(viewportScrollTop - HEADER_HEIGHT_PX);
    const yBottom = scale.pxToYear(
      viewportScrollTop + viewportClientHeight - HEADER_HEIGHT_PX,
    );
    const minYear = Math.min(yTop, yBottom);
    const maxYear = Math.max(yTop, yBottom);
    const centerYear = (minYear + maxYear) / 2;

    // Anything in view already? Periods count as overlapping when their
    // range intersects [minYear, maxYear]; points count when their key/start
    // year falls inside it.
    const anyInView = events.some((e) => {
      if (e.start_year == null) return false;
      const isPeriod =
        e.is_period && e.end_year != null && e.end_year !== e.start_year;
      if (isPeriod) {
        return !(e.end_year! < minYear || e.start_year! > maxYear);
      }
      const k = e.key_year ?? e.start_year;
      return k >= minYear && k <= maxYear;
    });
    if (anyInView) return;

    // Pick the nearest occurrence by year distance. For periods we measure
    // distance to the nearest point in [start, end]; for point occurrences
    // we use key_year (or start_year as fallback).
    let bestYear: number | null = null;
    let bestDist = Infinity;
    for (const e of events) {
      if (e.start_year == null) continue;
      const isPeriod =
        e.is_period && e.end_year != null && e.end_year !== e.start_year;
      let target: number;
      if (isPeriod) {
        target =
          centerYear < e.start_year
            ? e.start_year
            : centerYear > e.end_year!
            ? e.end_year!
            : centerYear;
      } else {
        target = e.key_year ?? e.start_year;
      }
      const d = Math.abs(target - centerYear);
      if (d < bestDist) {
        bestDist = d;
        bestYear = target;
      }
    }
    if (bestYear != null) onAutoCenter(bestYear);
    // We intentionally exclude viewport* and scale from deps: the check
    // should only run when stamp/events change, not on every scroll.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [swapStamp, events]);

  // ----- Viewport-aware single-box placement --------------------------------
  //
  // For each occurrence (processed in priority order, highest first):
  //   1. Try the KEY date. If the key-anchored box would be on-screen, use it.
  //   2. Else if the occurrence is a period and its range overlaps the
  //      viewport, fall back to whichever endpoint is on-screen (start first,
  //      then end).
  //   3. Skip the occurrence if no anchor is on-screen.
  //   4. Reject if the anchor box collides with an already-placed box.
  //
  // The thin range line is drawn separately during render (clipped to viewport
  // edges) for every placed period.
  const visible = useMemo(() => {
    // Region weighting is a MULTIPLIER on the base priority — not a tie-breaker.
    //   regionScore = sum(slider_r * weight_r) / sum(slider_r)        // 0..10
    //   effectivePriority = basePriority * regionScore / 5
    // So the default sliders (all 5) leave priority unchanged; dialing a
    // region to 0 zeros out occurrences anchored exclusively in that region;
    // dialing one region to 10 with others at 0 promotes that region's events
    // up to ~2x their base while heavily demoting everything else. If every
    // slider is 0 nothing renders — strict interpretation of "region 0 means
    // hide that region".
    const filterSum =
      regionFilter.europe +
      regionFilter.americas +
      regionFilter.asia +
      regionFilter.australasia +
      regionFilter.africa;

    function regionScore(e: EventWithPriority): number {
      if (!regionWeighted) return 5;       // non-weighted timeline: neutral
      if (filterSum <= 0) return 0;        // all sliders zeroed: hide all
      return (
        (e.weight_europe      ?? 5) * regionFilter.europe +
        (e.weight_americas    ?? 5) * regionFilter.americas +
        (e.weight_asia        ?? 5) * regionFilter.asia +
        (e.weight_australasia ?? 5) * regionFilter.australasia +
        (e.weight_africa      ?? 5) * regionFilter.africa
      ) / filterSum;
    }

    // Cross-timeline dedup: drop any event whose ID also appears in another
    // visible column. Used today only for the master column so it shows
    // "world events not already covered by your other lenses".
    const eventsAfterDedup = excludeIds && excludeIds.size > 0
      ? events.filter((e) => !excludeIds.has(e.id))
      : events;

    // Lifespan toggle (off by default): suppress every full-life person entry
    // so the timeline isn't crowded with birth → death bars. Periods within
    // a person's life are stored as type=event and aren't affected.
    const eventsAfterExclude = showLifespans
      ? eventsAfterDedup
      : eventsAfterDedup.filter((e) => !e.is_full_life);

    // --- Two-level rollup ----------------------------------------------------
    // Decide rollup level from the currently-visible year span:
    //   span <  80 yr  -> level 0  (leaf events)
    //   80–800 yr      -> level 1  (collapse to first_zoom_out umbrella)
    //   span >= 800 yr -> level 2  (collapse to second_zoom_out, else first)
    //
    // The 10-yr rule does double duty as "umbrella detection": any event with
    // span > 10 yr is treated as a rollup-only umbrella — hidden at leaf zoom,
    // shown when it's the rollup target at level 1/2.
    const yTopForSpan = scale.pxToYear(viewportScrollTop - HEADER_HEIGHT_PX);
    const yBottomForSpan = scale.pxToYear(
      viewportScrollTop + viewportClientHeight - HEADER_HEIGHT_PX,
    );
    const visibleSpanYrs = Math.max(0, yTopForSpan - yBottomForSpan);
    const rollupLevel =
      visibleSpanYrs >= 800 ? 2 :
      visibleSpanYrs >= 80  ? 1 : 0;

    // Index umbrellas by lowercased title for substitution lookups.
    // The occurrence's canonical title (single `title` column post-009).
    const titleKey = (e: EventWithPriority) =>
      (e.title ?? "").trim().toLowerCase();
    const umbrellaByTitle = new Map<string, EventWithPriority>();
    for (const e of eventsAfterExclude) {
      const k = titleKey(e);
      if (k) umbrellaByTitle.set(k, e);
    }
    const spanOf = (e: EventWithPriority) =>
      (e.end_year ?? e.start_year ?? 0) - (e.start_year ?? 0);
    // An entry is only an "umbrella" if some OTHER entry references it via
    // first_zoom_out or second_zoom_out — otherwise it's a top-level period
    // that should render at its own zoom level (e.g. a monarch reign).
    // Without this check, the previous span>10 rule wrongly hid every long
    // monarch reign (Victoria, George V, George VI, …) at leaf zoom.
    const referencedUmbrellaTitles = new Set<string>();
    for (const e of eventsAfterExclude) {
      if (e.first_zoom_out)
        referencedUmbrellaTitles.add(e.first_zoom_out.trim().toLowerCase());
      if (e.second_zoom_out)
        referencedUmbrellaTitles.add(e.second_zoom_out.trim().toLowerCase());
    }
    // Person/art entries with long lifespans aren't umbrellas — only
    // event-type long periods that are actually referenced as a rollup
    // target should be hidden at leaf zoom.
    const isLongUmbrella = (e: EventWithPriority) =>
      e.occurrence_type === "event" &&
      spanOf(e) > 10 &&
      referencedUmbrellaTitles.has(titleKey(e));

    // Substitute each entry with its rollup target if one applies.
    // Exception: the just-flashed entry (typically from a search pick) is
    // exempted from substitution and from the long-umbrella-at-leaf-zoom
    // suppression — when a user searches for an umbrella they want to see
    // THAT entry, not its parent or its leaves.
    const flashedId = flash?.id ?? null;
    const seen = new Set<number>();
    const rolledEvents: EventWithPriority[] = [];
    for (const e of eventsAfterExclude) {
      const isFlashed = e.id === flashedId;
      let target: EventWithPriority = e;
      if (!isFlashed) {
        if (rollupLevel >= 2 && e.second_zoom_out) {
          const u = umbrellaByTitle.get(e.second_zoom_out.trim().toLowerCase());
          if (u) target = u;
          else if (e.first_zoom_out) {
            const u1 = umbrellaByTitle.get(e.first_zoom_out.trim().toLowerCase());
            if (u1) target = u1;
          }
        } else if (rollupLevel >= 1 && e.first_zoom_out) {
          const u = umbrellaByTitle.get(e.first_zoom_out.trim().toLowerCase());
          if (u) target = u;
        }
      }
      // At leaf zoom, hide event-type entries whose span exceeds 10 yr —
      // they're umbrella periods, only meant to render at rollup zoom.
      // (Person/art entries can have long spans and aren't umbrellas.)
      // Flashed entry bypasses this so a searched-for umbrella always shows.
      if (rollupLevel === 0 && isLongUmbrella(target) && !isFlashed) continue;
      if (seen.has(target.id)) continue;
      seen.add(target.id);
      rolledEvents.push(target);
    }

    const itemsRaw = expandToItems(rolledEvents);
    const items = itemsRaw
      .map((it) => ({
        ...it,
        priority: regionWeighted
          ? (it.priority * regionScore(it.event)) / 5
          : it.priority,
      }))
      // Drop occurrences whose region multiplier killed their priority.
      .filter((it) => it.priority > 0)
      // Sort by priority desc, but pin the flashed entry to the front so it
      // always wins its placement slot — even if higher-priority neighbours
      // would normally crowd it out.
      .sort((a, b) => {
        if (flashedId != null) {
          if (a.event.id === flashedId) return -1;
          if (b.event.id === flashedId) return 1;
        }
        return b.priority - a.priority;
      });

    const yearToTop = (y: number) => scale.yearToPx(y);
    const viewTop = viewportScrollTop - HEADER_HEIGHT_PX;
    const viewBottom =
      viewportScrollTop + viewportClientHeight - HEADER_HEIGHT_PX;
    // True if any part of a boxHeightPx-tall box anchored at `top` is on screen.
    const boxInView = (top: number) =>
      top + boxHeightPx > viewTop && top < viewBottom;

    // Placement: walk items in priority order, claim a slot if the box
    // doesn't overlap an already-placed slot. When the ideal anchor position
    // collides, try nudging the box up/down in 10%-of-box-height increments
    // up to ±50% of box height before giving up. The highest-priority entries
    // are placed first and stay exactly where their key/start/end year says,
    // so the nudge only ever shifts lower-priority boxes to fit around them.
    type Slot = { top: number; bottom: number };
    const slots: Slot[] = [];
    const placed: Placed[] = [];

    const collides = (top: number, bottom: number) =>
      slots.some((s) => !(bottom <= s.top || top >= s.bottom));

    // Search for a free slot for the box anywhere in [minTop, maxTop],
    // walking outward from idealTop in `step`-sized increments and choosing
    // the smallest absolute displacement that fits. priorTop (if given) is
    // used as a hysteresis tiebreaker: when the canonical idealTop collides,
    // we try the previous-render position next so periods don't jump around
    // on scroll. Returns null if no collision-free position exists within the
    // allowed range.
    const findFreeSlot = (
      idealTop: number,
      minTop: number,
      maxTop: number,
      priorTop: number | null,
    ): number | null => {
      const tryPlace = (top: number) =>
        top >= minTop - 0.001 &&
        top <= maxTop + 0.001 &&
        boxInView(top) &&
        !collides(top, top + boxHeightPx);
      // 1. Canonical position (gravity centre).
      if (tryPlace(idealTop)) return idealTop;
      // 2. Prior-render position, when available and within the allowed range.
      if (priorTop != null && tryPlace(priorTop)) return priorTop;
      // 3. Search outward from idealTop, alternating up/down.
      const step = Math.max(1, Math.round(boxHeightPx * 0.1));
      const maxUp = idealTop - minTop;
      const maxDown = maxTop - idealTop;
      const limit = Math.max(maxUp, maxDown);
      for (let nudge = step; nudge <= limit + 0.001; nudge += step) {
        if (nudge <= maxUp + 0.001) {
          const up = idealTop - nudge;
          if (tryPlace(up)) return up;
        }
        if (nudge <= maxDown + 0.001) {
          const down = idealTop + nudge;
          if (tryPlace(down)) return down;
        }
      }
      return null;
    };

    const maxNudgePx = boxHeightPx * 0.5;
    const priorMap = priorAnchorYearsRef.current;

    for (const item of items) {
      const startTop = yearToTop(item.startYear);   // older year = larger y (lower)
      const endTop = yearToTop(item.endYear);       // newer year = smaller y (upper)
      const keyTop = yearToTop(item.keyYear);
      // Precision-driven flex from item 3 (year-only → anywhere in year,
      // month-only → anywhere in month). Smaller year = larger px, so the
      // year-range maps to a top-range with min/max swapped.
      const precisionTopMin = yearToTop(item.keyMaxYear);
      const precisionTopMax = yearToTop(item.keyMinYear);

      // Build the list of candidate anchors to try, in preference order.
      // The "key" candidate has gravity at keyTop and may roam within
      // [precisionTopMin, precisionTopMax] (item 3 + item 6) or within
      // ±50% box-height (item 2), whichever is wider.
      // For periods only, "start" and "end" remain as fallback candidates so
      // a period whose key year has gone off-screen can still anchor on the
      // endpoint that's still visible.
      type Candidate = { ideal: number; kind: AnchorKind; minTop: number; maxTop: number };
      const candidates: Candidate[] = [];
      // The keyflex range overlaps the viewport when ANY top in
      // [precisionTopMin, precisionTopMax] has its box on screen.
      const keyRangeOnScreen =
        precisionTopMax + boxHeightPx > viewTop &&
        precisionTopMin < viewBottom;
      // Periods anchor at start_year / end_year only — never at the
      // mid-period key year. For long-period entries (e.g. Cologne Cathedral
      // 1248-1880) the mid-period anchor caused the box to "reappear" three
      // times when scrolling through the period (at start, key, and end),
      // which felt disorienting. The user wants long periods to anchor only
      // at their actual start and end boundaries.
      if (keyRangeOnScreen && !item.isPeriod) {
        const minTop = Math.min(keyTop - maxNudgePx, precisionTopMin);
        const maxTop = Math.max(keyTop + maxNudgePx, precisionTopMax);
        candidates.push({ ideal: keyTop, kind: "key", minTop, maxTop });
      }
      if (item.isPeriod) {
        const rangeOverlaps = endTop < viewBottom && startTop > viewTop;
        if (rangeOverlaps) {
          if (boxInView(startTop)) {
            candidates.push({
              ideal: startTop,
              kind: "start",
              minTop: startTop - maxNudgePx,
              maxTop: startTop + maxNudgePx,
            });
          }
          if (boxInView(endTop)) {
            candidates.push({
              ideal: endTop,
              kind: "end",
              minTop: endTop - maxNudgePx,
              maxTop: endTop + maxNudgePx,
            });
          }
        }
      }
      if (candidates.length === 0) continue;

      // Prior position from last render (in fractional years), mapped through
      // the current scale to today's pixel coordinates.
      const priorYear = priorMap.get(item.event.id);
      const priorTop = priorYear != null ? yearToTop(priorYear) : null;

      let anchorTop: number | null = null;
      let anchorKind: AnchorKind = "key";
      for (const c of candidates) {
        // Only feed priorTop into findFreeSlot when it falls inside this
        // candidate's allowed range — otherwise it'd be silently rejected.
        const usablePrior =
          priorTop != null && priorTop >= c.minTop && priorTop <= c.maxTop
            ? priorTop
            : null;
        const free = findFreeSlot(c.ideal, c.minTop, c.maxTop, usablePrior);
        if (free != null) {
          anchorTop = free;
          anchorKind = c.kind;
          break;
        }
      }
      if (anchorTop == null) continue;

      const bottom = anchorTop + boxHeightPx;
      slots.push({ top: anchorTop, bottom });
      placed.push({
        event: item.event,
        anchorTop,
        anchorKind,
        startTop,
        endTop,
        isPeriod: item.isPeriod,
        lineTrack: 0,  // assigned in the stagger pass below
        hideLine: false,  // resolved in the stagger pass below
        color: colorFor(item.event),
      });
    }

    // ----- Stagger period lines across tracks ---------------------------------
    // Iterate placed periods in priority order (already sorted by the loop
    // above). For each, find the lowest-numbered track whose previously-claimed
    // segments don't vertically overlap with this one. Track 0 is the centre,
    // so the highest-priority period that's currently visible sits in the
    // middle and lower-priority lines fan outward.
    //
    // Also decide whether to render this period's range line AT ALL: if any
    // OTHER occurrence box sits within the line's visible vertical extent,
    // the line would just cross through unrelated entries and add visual
    // noise. Hide it. (Useful on busy timelines like Master; harmless on
    // sequential timelines like England Monarchs where reigns don't overlap
    // each other, so lines stay visible there.)
    type Claim = { track: number; top: number; bottom: number };
    const claims: Claim[] = [];
    for (const p of placed) {
      if (!p.isPeriod) continue;
      // Clip to viewport so two periods only count as overlapping if their
      // visible line segments overlap (a line far above the viewport doesn't
      // need to dodge one inside it).
      const lineTop = Math.max(p.endTop, viewTop);
      const lineBottom = Math.min(p.startTop, viewBottom);
      if (lineBottom - lineTop <= 0) {
        // No visible line for this period in the current viewport — leave at 0.
        continue;
      }

      // Hide the line if any OTHER placed box (i.e. not this period's own
      // anchor box) vertically overlaps the line's visible extent. Exact
      // match on (top, bottom) identifies the period's own box.
      const ownTop = p.anchorTop;
      const ownBottom = p.anchorTop + boxHeightPx;
      const otherOverlap = slots.some((s) => {
        const isOwn = s.top === ownTop && s.bottom === ownBottom;
        if (isOwn) return false;
        return !(s.bottom <= lineTop || s.top >= lineBottom);
      });
      if (otherOverlap) {
        p.hideLine = true;
        continue;  // No track needed; the line won't render.
      }

      let track = 0;
      while (
        claims.some(
          (c) =>
            c.track === track &&
            !(lineBottom <= c.top || lineTop >= c.bottom),
        )
      ) {
        track++;
      }
      p.lineTrack = track;
      claims.push({ track, top: lineTop, bottom: lineBottom });
    }

    // Persist this render's placements as fractional years for the next render
    // to consult (hysteresis — item 6). Stored as year so the cache survives
    // zoom changes.
    const newPriorMap = new Map<number, number>();
    for (const p of placed) {
      newPriorMap.set(p.event.id, scale.pxToYear(p.anchorTop));
    }
    priorAnchorYearsRef.current = newPriorMap;

    return placed;
  }, [
    events,
    scale,
    viewportScrollTop,
    viewportClientHeight,
    boxHeightPx,
    regionFilter,
    regionWeighted,
    excludeIds,
    showLifespans,
  ]);

  // Granularity for date labels inside boxes. Based on the year-span currently
  // visible in the viewport — derived from the scale's inverse so that the
  // log-compressed bands switch granularity appropriately (e.g. yearly labels
  // near today, century labels back in the medieval band, kya labels in
  // prehistory).
  const granularity: Granularity = useMemo(() => {
    if (viewportClientHeight <= 0) return "year";
    const top = scale.pxToYear(viewportScrollTop - HEADER_HEIGHT_PX);
    const bottom = scale.pxToYear(
      viewportScrollTop + viewportClientHeight - HEADER_HEIGHT_PX,
    );
    const span = Math.max(1, top - bottom);
    return granularityForSpan(span, dateDisplayMode);
  }, [scale, viewportScrollTop, viewportClientHeight, dateDisplayMode]);

  const viewTop = viewportScrollTop - HEADER_HEIGHT_PX;
  const viewBottom = viewportScrollTop + viewportClientHeight - HEADER_HEIGHT_PX;

  return (
    <section
      className="relative flex-shrink-0 border-r border-slate-200 dark:border-slate-700"
      style={{ width: columnWidth }}
    >
      <h2
        className="sticky top-0 z-30 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-700 flex items-center"
        style={{ height: HEADER_HEIGHT_PX }}
      >
        <button
          type="button"
          onClick={(e) => {
            const rect = (e.currentTarget as HTMLElement).getBoundingClientRect();
            onHeaderClick(columnIndex, rect);
          }}
          title="Click to swap this column for another timeline"
          className="w-full h-full px-3 text-left text-sm font-semibold text-slate-900 dark:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800 focus:outline-none focus:bg-slate-100 dark:focus:bg-slate-800 flex items-center justify-between gap-2"
        >
          <span className="truncate">{timeline.name}</span>
          <span aria-hidden className="text-[10px] text-slate-500 shrink-0">▾</span>
        </button>
      </h2>
      <div className="relative" style={{ height: totalHeight }}>
        {visible.map((p) => {
          // Range line (periods only). Full extent from end_year (top) to
          // start_year (bottom), clipped to the visible viewport. Coloured to
          // match the occurrence's box outline, positioned at the assigned
          // horizontal track so overlapping lines don't pile up.
          let lineEl: JSX.Element | null = null;
          if (p.isPeriod && !p.hideLine) {
            const renderTop = Math.max(p.endTop, viewTop);
            const renderBottom = Math.min(p.startTop, viewBottom);
            const h = renderBottom - renderTop;
            if (h > 0) {
              const lineX = lineXForTrack(p.lineTrack, columnWidth);
              // Centre the arrow's triangular base on the line, so the line's
              // 2-px stem runs straight into the middle of the arrow.
              const arrowLeft =
                lineX + LINE_THICKNESS_PX / 2 - LINE_ARROW_HALF_W_PX;
              // Only show an arrowhead when the actual endpoint sits inside
              // the viewport — if the line was clipped, the line just trails
              // off the edge without a misleading terminator.
              const showTopArrow =
                p.endTop >= viewTop && p.endTop <= viewBottom;
              const showBottomArrow =
                p.startTop >= viewTop && p.startTop <= viewBottom;
              lineEl = (
                <>
                  <div
                    className="absolute z-0 pointer-events-none"
                    style={{
                      left: lineX,
                      top: renderTop,
                      width: LINE_THICKNESS_PX,
                      height: h,
                      backgroundColor: p.color.line,
                    }}
                  />
                  {showTopArrow && (
                    <div
                      className="absolute z-0 pointer-events-none"
                      style={{
                        left: arrowLeft,
                        top: p.endTop - LINE_ARROW_H_PX,
                        width: 0,
                        height: 0,
                        borderLeft: `${LINE_ARROW_HALF_W_PX}px solid transparent`,
                        borderRight: `${LINE_ARROW_HALF_W_PX}px solid transparent`,
                        borderBottom: `${LINE_ARROW_H_PX}px solid ${p.color.line}`,
                      }}
                    />
                  )}
                  {showBottomArrow && (
                    <div
                      className="absolute z-0 pointer-events-none"
                      style={{
                        left: arrowLeft,
                        top: p.startTop,
                        width: 0,
                        height: 0,
                        borderLeft: `${LINE_ARROW_HALF_W_PX}px solid transparent`,
                        borderRight: `${LINE_ARROW_HALF_W_PX}px solid transparent`,
                        borderTop: `${LINE_ARROW_H_PX}px solid ${p.color.line}`,
                      }}
                    />
                  )}
                </>
              );
            }
          }

          return (
            <div key={`occ-${p.event.id}`}>
              {lineEl}
              <OccurrenceBox
                top={p.anchorTop}
                heightPx={boxHeightPx}
                event={p.event}
                color={p.color}
                granularity={granularity}
                onEnter={onBoxEnter}
                onLeave={onBoxLeave}
                flashStamp={flash && flash.id === p.event.id ? flash.stamp : null}
                isFavourite={isFavourite(p.event.id)}
              />
            </div>
          );
        })}
      </div>
    </section>
  );
}

// ----- Event box ------------------------------------------------------------
// Binding pattern:
//   - Mouse (desktop): pointerenter / pointerleave drive the popup, matching
//     the original hover model. Opens instantly.
//   - Touch / pen (mobile): pointerdown starts a TAP_DELAY_MS timer. If the
//     finger moves more than TAP_MOVE_THRESHOLD_PX (= scroll started), or the
//     touch is cancelled, the timer is killed and the popup never opens.
//     Otherwise the popup opens when the timer fires, and stays open until
//     the × button or an outside tap dismisses it. The delay-then-cancel
//     pattern stops the popup from flashing in during 1-finger scrolls and
//     during pinch zooms.
const TAP_DELAY_MS = 180;
const TAP_MOVE_THRESHOLD_PX = 8;
function useHoverBinding(
  event: EventWithPriority,
  onEnter: HoverHandler,
  onLeave: () => void,
) {
  const ref = useRef<HTMLDivElement>(null);
  const tapTimerRef = useRef<number | null>(null);
  return {
    ref,
    onPointerEnter: (e: React.PointerEvent) => {
      if (e.pointerType !== "mouse") return;
      if (ref.current) onEnter(event, ref.current.getBoundingClientRect());
    },
    onPointerLeave: (e: React.PointerEvent) => {
      if (e.pointerType !== "mouse") return;
      onLeave();
    },
    onPointerDown: (e: React.PointerEvent) => {
      if (e.pointerType === "mouse") return;
      // Reset any pending tap from a previous (cancelled) interaction.
      if (tapTimerRef.current != null) {
        window.clearTimeout(tapTimerRef.current);
        tapTimerRef.current = null;
      }
      const startX = e.clientX;
      const startY = e.clientY;
      // Document-level listeners so we still catch movement after the finger
      // slides off the box (which is what happens during a scroll).
      const onMove = (me: PointerEvent) => {
        const dx = me.clientX - startX;
        const dy = me.clientY - startY;
        if (Math.hypot(dx, dy) > TAP_MOVE_THRESHOLD_PX) cancel();
      };
      const cancel = () => {
        if (tapTimerRef.current != null) {
          window.clearTimeout(tapTimerRef.current);
          tapTimerRef.current = null;
        }
        document.removeEventListener("pointermove", onMove);
        document.removeEventListener("pointercancel", cancel);
      };
      document.addEventListener("pointermove", onMove);
      document.addEventListener("pointercancel", cancel);
      tapTimerRef.current = window.setTimeout(() => {
        tapTimerRef.current = null;
        document.removeEventListener("pointermove", onMove);
        document.removeEventListener("pointercancel", cancel);
        if (ref.current) onEnter(event, ref.current.getBoundingClientRect());
      }, TAP_DELAY_MS);
    },
  };
}

// Build the adaptive in-box date label.
//
// - Points: format a single date at the current granularity.
// - Periods/people: format the full range at the current granularity.
// - Deep time (year < -10_000) or no structured month/day: fall back to the
//   importer-provided display_date string (handles "~13.8 billion years ago",
//   approximate BCE entries, etc.).
function adaptiveDateLabel(
  event: EventWithPriority,
  granularity: Granularity,
): string {
  const isRange =
    event.is_period && event.end_year != null && event.end_year !== event.start_year;

  // Deep-time override: structured day/month are meaningless for billions BCE.
  const deepTime =
    event.start_year != null && event.start_year < -10_000;
  if (deepTime && event.display_date) {
    return addUncertaintyMark(event.display_date, event.date_uncertain);
  }

  const label = isRange
    ? formatPartialRange(
        event.start_year,
        event.start_month,
        event.start_day,
        event.end_year,
        event.end_month,
        event.end_day,
        granularity,
      )
    : formatPartial(
        event.start_year,
        event.start_month,
        event.start_day,
        granularity,
      );

  // If our adaptive formatter produced nothing (shouldn't happen normally),
  // fall back to display_date.
  const final = label || event.display_date || "";
  return addUncertaintyMark(final, event.date_uncertain);
}

function OccurrenceBox({
  top, heightPx, event, color, granularity, onEnter, onLeave, flashStamp,
  isFavourite,
}: {
  top: number;
  heightPx: number;
  event: EventWithPriority;
  color: OccurrenceColor;
  granularity: Granularity;
  onEnter: HoverHandler;
  onLeave: () => void;
  flashStamp: number | null;
  /** When true, renders a small heart badge in the corner of the box. */
  isFavourite: boolean;
}) {
  const bind = useHoverBinding(event, onEnter, onLeave);

  // When flashStamp changes (a new search has targeted this occurrence) we
  // restart the CSS pulse by removing then re-adding the class, forcing a
  // reflow in between so the animation actually replays.
  useEffect(() => {
    if (flashStamp == null) return;
    const el = bind.ref.current;
    if (!el) return;
    el.classList.remove("flash-ring");
    // Force reflow so the animation restarts when we re-add the class.
    void el.offsetWidth;
    el.classList.add("flash-ring");
    const t = window.setTimeout(() => el.classList.remove("flash-ring"), 2000);
    return () => {
      window.clearTimeout(t);
      el.classList.remove("flash-ring");
    };
  }, [flashStamp, bind.ref]);

  // Scale the in-box text with the box height so lower-density (taller-box)
  // settings actually fill the box rather than leaving big empty bands. The
  // 0.20 multiplier ≈ matches the previous 12-px text at the default density
  // of 12 (≈ 67-px box on an 800-px viewport); the clamp keeps very dense
  // settings legible and very sparse ones from looking comically large.
  const titleFontPx = Math.max(11, Math.min(18, Math.round(heightPx * 0.2)));
  const descFontPx = Math.max(9, Math.min(15, titleFontPx - 2));

  // Outline:
  //   - style: solid (event default) | dashed (person) | dotted (art)
  //   - width: border-2 (period) | border (point)
  //   - colour: same hue as the box fill, fully opaque (see color.border)
  const isPeriodEntry =
    event.is_period &&
    event.end_year != null &&
    event.end_year !== event.start_year;
  const outlineStyleClass =
    event.occurrence_type === "person"
      ? "border-dashed"
      : event.occurrence_type === "art"
        ? "border-dotted"
        : "border-solid";
  const outlineWidthClass = isPeriodEntry ? "border-2" : "border";

  return (
    <div
      ref={bind.ref}
      data-occurrence-box
      onPointerEnter={bind.onPointerEnter}
      onPointerLeave={bind.onPointerLeave}
      onPointerDown={bind.onPointerDown}
      className={`absolute z-10 hover:z-20 left-1 right-1 rounded ${outlineWidthClass} ${outlineStyleClass} px-2 py-1 overflow-hidden transition-colors`}
      style={{
        top,
        height: heightPx,
        backgroundColor: color.fill,
        borderColor: color.border,
      }}
    >
      <div
        className="leading-tight text-slate-900 dark:text-slate-100"
        style={{ fontSize: titleFontPx }}
      >
        <span>{adaptiveDateLabel(event, granularity)}</span>
        <span> {event.title}</span>
        {event.description && (
          <span
            className="text-slate-400"
            style={{ fontSize: descFontPx }}
          >
            {" "}
            {event.description}
          </span>
        )}
      </div>
      {isFavourite && (
        <span
          aria-hidden
          title="Favourite"
          className="absolute top-0.5 right-1 text-rose-400 pointer-events-none leading-none"
          style={{ fontSize: Math.max(10, Math.min(14, titleFontPx - 2)) }}
        >
          ♥
        </span>
      )}
    </div>
  );
}
