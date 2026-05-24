// Frontend-only grouping of timeline slugs. Used by the TimelinePicker
// dropdown (to render section headers) and the main SearchBar (to label
// timeline-row matches).
//
// This is intentionally not in the database — the dataset of timelines is
// small and stable, and the grouping is a UI concern. Adding a new timeline?
// Add its slug to TIMELINE_SLUG_TO_GROUP below. Slugs not listed fall into
// "major-periods" (the default catch-all).

export type TimelineGroup =
  | "worldwide"
  | "europe"
  | "americas"
  | "asia"
  | "africa"
  | "australasia"
  | "conflicts"
  | "major-periods";

// Display order — groups are rendered top-to-bottom in this order. Empty
// groups (no timelines mapped to them) are hidden by the rendering code.
export const TIMELINE_GROUP_ORDER: TimelineGroup[] = [
  "worldwide",
  "europe",
  "americas",
  "asia",
  "africa",
  "australasia",
  "conflicts",
  "major-periods",
];

// Human-readable header shown in the picker / search-bar.
export const TIMELINE_GROUP_LABELS: Record<TimelineGroup, string> = {
  worldwide: "Worldwide",
  europe: "Europe",
  americas: "Americas",
  asia: "Asia",
  africa: "Africa",
  australasia: "Australasia",
  conflicts: "Conflicts",
  "major-periods": "Major periods",
};

// Slug → group. Unknown slugs default to "major-periods".
const TIMELINE_SLUG_TO_GROUP: Record<string, TimelineGroup> = {
  // Worldwide / cross-cutting themes
  master: "worldwide",
  "arts-and-thoughts": "worldwide",
  people: "worldwide",

  // Europe — country lenses and pan-European classical timelines
  england: "europe",
  "england-monarchs": "europe",
  france: "europe",
  germany: "europe",
  "roman-history": "europe",
  "ancient-greece": "europe",

  // Americas
  usa: "americas",
  "us-presidents": "americas",

  // Asia
  china: "asia",
  india: "asia",

  // Conflicts — wars and inter-state confrontations
  ww1: "conflicts",
  ww2: "conflicts",
  "cold-war": "conflicts",
  napoleonic: "conflicts",

  // Major periods — eras, movements
  renaissance: "major-periods",
  industrial: "major-periods",
};

export function groupForSlug(slug: string): TimelineGroup {
  return TIMELINE_SLUG_TO_GROUP[slug] ?? "major-periods";
}
