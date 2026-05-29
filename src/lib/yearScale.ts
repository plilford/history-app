// Year ↔ pixel mapping for the timeline.
//
// The mapping is linear within a "recent" band (the last LINEAR_RANGE_YEARS
// years before yearMax) and log-compressed for everything older. This lets a
// single scrollable timeline span the full data range — which can extend to
// billions of years for geological occurrences — while still leaving
// human-history detail readable at the recent end.
//
// The older band uses a DOUBLE-log compression (a log of the log) so that deep
// antiquity is squeezed much harder than a plain log would, without making the
// recent/early-modern transition feel abrupt. DEEP_COMPRESSION (D) tunes the
// strength: D → 0 recovers the plain natural-log curve; larger D compresses
// older history more. The derivative is still continuous at the linear/log seam
// so the visual scale transitions smoothly when scrolling between eras, and the
// compression ramps in gradually (early-modern centuries are barely affected;
// the squeeze accrues in ancient and deep-time bands).
//
//   t = yearMax - year   (years before yearMax)
//   u = ln(t / L)
//   t ≤ L : px(t) = k * t                                  (linear, k px/yr)
//   t > L : px(t) = k * L * (1 + (1/D) * ln(1 + D * u))     (double-log)
//
// Derivative (local pixels-per-year):
//   t ≤ L : dpx/dt = k
//   t > L : dpx/dt = k * L / (t * (1 + D * u))
// Both branches give k at t = L (u = 0), so the seam is smooth.

// Strength of the deep-time squeeze in the log band. Higher = more compressed.
// 0.5 keeps the last few centuries near-linear while shrinking BCE / deep-time
// bands substantially. Lower it toward 0 to approach a plain log curve.
const DEEP_COMPRESSION = 0.5;

export type YearScale = {
  yearMin: number;
  yearMax: number;
  k: number;            // linear ppy in the recent band
  linearRange: number;  // length of the linear band in years
  totalHeight: number;
  /** Pixel y-coordinate. yearMax → 0, older years → larger px. */
  yearToPx(year: number): number;
  /** Inverse of yearToPx. */
  pxToYear(px: number): number;
  /** Local pixels-per-year at the given year — derivative of yearToPx. */
  localPpy(year: number): number;
};

export function makeYearScale(
  yearMin: number,
  yearMax: number,
  k: number,
  linearRange: number,
): YearScale {
  const L = Math.max(1, linearRange);
  const D = DEEP_COMPRESSION;

  function yearToPx(year: number): number {
    const t = yearMax - year;
    if (t <= 0) return 0;
    if (t <= L) return k * t;
    const u = Math.log(t / L);
    return k * L * (1 + (1 / D) * Math.log(1 + D * u));
  }

  function pxToYear(px: number): number {
    if (px <= 0) return yearMax;
    if (px <= k * L) return yearMax - px / k;
    const P = px / (k * L);
    // Invert px = k*L*(1 + (1/D)*ln(1 + D*u)) for u = ln(t/L):
    const u = (Math.exp((P - 1) * D) - 1) / D;
    const t = L * Math.exp(u);
    return yearMax - t;
  }

  function localPpy(year: number): number {
    const t = yearMax - year;
    if (t <= L) return k;
    const u = Math.log(t / L);
    return (k * L) / (t * (1 + D * u));
  }

  const totalHeight = yearToPx(yearMin);
  return {
    yearMin,
    yearMax,
    k,
    linearRange: L,
    totalHeight,
    yearToPx,
    pxToYear,
    localPpy,
  };
}

// "Nice" year steps used for tick placement, spanning yearly through 1-billion-
// year intervals so deep-time bands get sensibly-rounded labels too.
const NICE_TICK_STEPS = [
  1, 2, 5, 10, 20, 25, 50,
  100, 200, 250, 500,
  1_000, 2_000, 5_000,
  10_000, 20_000, 50_000,
  100_000, 200_000, 500_000,
  1_000_000, 2_000_000, 5_000_000,
  10_000_000, 20_000_000, 50_000_000,
  100_000_000, 200_000_000, 500_000_000,
  1_000_000_000,
];

/** Smallest "nice" step that is ≥ targetYearGap. */
export function pickNiceStep(targetYearGap: number): number {
  for (const s of NICE_TICK_STEPS) {
    if (s >= targetYearGap) return s;
  }
  return NICE_TICK_STEPS[NICE_TICK_STEPS.length - 1];
}

/**
 * Generate axis ticks for a log-compressed timeline. Density varies with
 * position: near yearMax the ticks fall on small (yearly, decadal) values; in
 * deep-time bands they fall on million- or billion-year values.
 *
 * Algorithm: walk year-space from yearMax going older. At each step look up
 * local ppy, pick the smallest "nice" year-step that produces ≥ targetPixelGap
 * pixels of separation, snap to a multiple of that step, and repeat. Because
 * local ppy is monotonically non-increasing as we go older, the chosen step
 * is monotonically non-decreasing — no backtracking.
 */
export function generateLogTicks(
  scale: YearScale,
  targetPixelGap: number = 80,
  maxTicks: number = 500,
): number[] {
  const { yearMin, yearMax } = scale;
  const ticks: number[] = [];

  let y = yearMax;
  for (let iter = 0; iter < maxTicks; iter++) {
    const ppy = scale.localPpy(y);
    if (!Number.isFinite(ppy) || ppy <= 0) break;
    const targetYearGap = targetPixelGap / ppy;
    const step = pickNiceStep(targetYearGap);
    // Largest multiple of step strictly less than y. Subtract 1 so a y that's
    // already a multiple of step still advances by one full step.
    const aligned = Math.floor((y - 1) / step) * step;
    if (aligned <= yearMin) break;
    if (ticks.length > 0 && ticks[ticks.length - 1] === aligned) break;
    ticks.push(aligned);
    y = aligned;
  }
  return ticks;
}

// -----------------------------------------------------------------------------
// Sub-year axis ticks — used when the viewport spans a single year (months)
// or a single month (days). Years are expressed as fractional values so the
// log-scaled yearToPx works unchanged: e.g. March 1950 = 1950 + 2/12.
// -----------------------------------------------------------------------------

export type SubYearTick = {
  /** Fractional year — feed into scale.yearToPx for the pixel position. */
  fracYear: number;
  /** Label to render. Major ticks get year/month context; minor are short. */
  label: string;
  /** Major ticks (1 Jan / 1st of month) get stronger styling. */
  isMajor: boolean;
};

const MONTH_SHORT = [
  "Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
];

/** Days in `month` (1-based) of `year`. */
function daysInMonth(year: number, month: number): number {
  // Date(year, month, 0) gives the last day of month (1-based here).
  return new Date(year, month, 0).getDate();
}

/** Convert (year, month, day) to a fractional year using actual month lengths. */
export function fractionalYear(year: number, month: number, day: number): number {
  const isLeap = (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0;
  const daysInYear = isLeap ? 366 : 365;
  let doy = 0;
  for (let m = 1; m < month; m++) doy += daysInMonth(year, m);
  doy += day - 1;
  return year + doy / daysInYear;
}

/** Month ticks visible in [yBottom, yTop] (yBottom older, yTop newer). */
export function generateMonthTicks(
  _scale: YearScale,
  yBottom: number,
  yTop: number,
): SubYearTick[] {
  const ticks: SubYearTick[] = [];
  const startYear = Math.floor(yBottom);
  const endYear = Math.ceil(yTop);
  for (let y = startYear; y <= endYear; y++) {
    if (y < 1) continue;       // months meaningless in this dataset pre-1 CE
    for (let m = 1; m <= 12; m++) {
      const fy = fractionalYear(y, m, 1);
      if (fy < yBottom - 0.01 || fy > yTop + 0.01) continue;
      ticks.push({
        fracYear: fy,
        label: m === 1 ? `${MONTH_SHORT[0]} ${y}` : MONTH_SHORT[m - 1],
        isMajor: m === 1,
      });
    }
  }
  return ticks;
}

/** Day ticks visible in [yBottom, yTop]. Thins out at wider spans. */
export function generateDayTicks(
  _scale: YearScale,
  yBottom: number,
  yTop: number,
): SubYearTick[] {
  const ticks: SubYearTick[] = [];
  const startYear = Math.floor(yBottom);
  const endYear = Math.ceil(yTop);
  // Pick a stride so we get a manageable number of ticks even if the user
  // zooms out a little before the year-tick mode kicks back in.
  const span = Math.max(yTop - yBottom, 0.0001);
  // Rough day count visible in the viewport.
  const dayCount = span * 365;
  // Aim for ~30 ticks max at any zoom; otherwise use 1-day stride.
  const stride =
    dayCount > 120 ? 7
    : dayCount > 60 ? 3
    : 1;
  for (let y = startYear; y <= endYear; y++) {
    if (y < 1) continue;
    for (let m = 1; m <= 12; m++) {
      const dim = daysInMonth(y, m);
      for (let d = 1; d <= dim; d += stride) {
        const fy = fractionalYear(y, m, d);
        if (fy < yBottom - 0.001 || fy > yTop + 0.001) continue;
        ticks.push({
          fracYear: fy,
          label: d === 1 ? `${MONTH_SHORT[m - 1]} ${y}` : String(d),
          isMajor: d === 1,
        });
      }
    }
  }
  return ticks;
}
