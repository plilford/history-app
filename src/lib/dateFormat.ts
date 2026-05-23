// =============================================================================
// Adaptive date formatting based on the timescale currently visible on screen.
// =============================================================================
//
// Default ("auto") granularity used inside event boxes depends on how many
// years are visible in the viewport at the current zoom:
//
//   visible < 20 years  →  "day month year"   (e.g. "23 November 1913")
//   visible ≥ 20 years  →  "year"             (e.g. "1913")
//
// The user can override via the date-display setting:
//   "always" → always use day precision
//   "auto"   → default zoom-dependent behaviour above
//   "never"  → always year-only
//
// Ranges use the same granularity for both endpoints, joined with " – ".
//
// Notes:
// - Negative years render with a "BCE" suffix and the magnitude is comma-
//   formatted ("3,200 BCE"). Years ≥ 1 render as-is.
// - The * suffix used for `date_uncertain` is the caller's responsibility; this
//   module exposes addUncertaintyMark() to append it consistently.
// - If a finer-grain field is null at a chosen granularity, we degrade to the
//   next coarser unit silently (no "undefined" in the output).
// =============================================================================

export type Granularity = "year" | "month" | "day";

export type DateDisplayMode = "always" | "auto" | "never";

const MONTH_NAMES = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December",
];

const MONTH_NAMES_SHORT = [
  "Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
];

/**
 * Decide which granularity to use given how many years are visible and the
 * user's date-display preference. Defaults to "auto", which shows day
 * precision when zoomed in within ~20 years and year only otherwise.
 */
export function granularityForSpan(
  yearsVisible: number,
  mode: DateDisplayMode = "auto",
): Granularity {
  if (mode === "always") return "day";
  if (mode === "never") return "year";
  // "auto"
  if (yearsVisible < 20) return "day";
  return "year";
}

/** Format a year, accounting for BCE (negative years). */
export function formatYear(year: number): string {
  if (year < 0) return `${Math.abs(year).toLocaleString("en-GB")} BCE`;
  return String(year);
}

/** Month index → name. Accepts 1-based (1=Jan) for consistency with Postgres. */
export function monthName(month: number, short = false): string {
  const i = month - 1;
  if (i < 0 || i > 11) return "";
  return short ? MONTH_NAMES_SHORT[i] : MONTH_NAMES[i];
}

/**
 * For occurrences flagged as ongoing (still happening — reigns, presidencies,
 * dynasties), substitute end_year = current year when end_year is null. This
 * lets the placement code treat them as ordinary periods that extend to
 * "now"; the display_date string set by the importer already reads
 * "<start>–present" so the UI label is still accurate.
 */
export function normalizeOngoing<
  T extends {
    end_year: number | null;
    is_ongoing: boolean;
    start_year: number | null;
  },
>(o: T): T {
  if (o.is_ongoing && o.end_year == null && o.start_year != null) {
    return { ...o, end_year: new Date().getUTCFullYear() };
  }
  return o;
}

/** Append "*" to indicate uncertain date, without doubling up. */
export function addUncertaintyMark(s: string, uncertain: boolean): string {
  if (!uncertain || !s) return s;
  return s.endsWith("*") ? s : `${s}*`;
}

/**
 * Format a single date at the given granularity. Degrades gracefully when
 * the finer parts are missing (e.g. no month → fall back to year-only).
 *
 * Pre-1 (BCE) years never show month/day even if requested, because the
 * data we have for those is too coarse to be meaningful day-level.
 */
export function formatPartial(
  year: number | null,
  month: number | null,
  day: number | null,
  granularity: Granularity,
): string {
  if (year == null) return "";
  if (year < 1) return formatYear(year);

  if (granularity === "day" && month != null && day != null) {
    return `${day} ${monthName(month)} ${year}`;
  }
  if ((granularity === "day" || granularity === "month") && month != null) {
    return `${monthName(month)} ${year}`;
  }
  return formatYear(year);
}

/**
 * Format a date range. Both endpoints use the same granularity.
 *
 * If end is null, this is a half-open range (e.g. ongoing). We emit
 * "<start> –" with a dash to indicate open-endedness, matching the existing
 * convention from build_display_date in the importer.
 */
export function formatPartialRange(
  startYear: number | null,
  startMonth: number | null,
  startDay: number | null,
  endYear: number | null,
  endMonth: number | null,
  endDay: number | null,
  granularity: Granularity,
): string {
  const left = formatPartial(startYear, startMonth, startDay, granularity);
  if (endYear == null) return left ? `${left} –` : "";
  const right = formatPartial(endYear, endMonth, endDay, granularity);
  if (!left && !right) return "";
  if (!right) return left;
  if (!left) return right;
  return `${left} – ${right}`;
}
