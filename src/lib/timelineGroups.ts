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
  | "religions"
  | "major-periods"
  | "resources";

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
  "religions",
  "major-periods",
  "resources",
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
  religions: "Religions",
  "major-periods": "Major periods",
  resources: "Resources",
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
  wales: "europe",
  france: "europe",
  germany: "europe",
  "roman-history": "europe",
  "ancient-greece": "europe",

  // Americas
  usa: "americas",
  "us-presidents": "americas",
  "pre-columbian-americas": "americas",

  // Asia
  china: "asia",
  india: "asia",
  japan: "asia",
  ottoman: "asia",

  // Conflicts — wars and inter-state confrontations
  ww1: "conflicts",
  ww2: "conflicts",
  "cold-war": "conflicts",
  napoleonic: "conflicts",
  crusades: "conflicts",

  // Religions — major religious traditions
  "major-religions": "religions",
  christianity: "religions",
  islam: "religions",
  judaism: "religions",

  // Major periods — eras, movements
  renaissance: "major-periods",
  industrial: "major-periods",

  // Resources — podcasts, books, documentaries (occurrence_type='resource')
  "the-rest-is-history-podcast": "resources",
  "popular-history-books": "resources",
  "resources-combined": "resources",
};

const VALID_GROUPS = new Set<string>(TIMELINE_GROUP_ORDER);

// Resolution order:
//   1. `dbGroup` — the timeline's `group` column (set in import_v2.py). This is
//      the source of truth for new timelines, so they're categorised correctly
//      without touching this file.
//   2. the static slug map below (legacy / belt-and-braces).
//   3. `isResourceTimeline` — any resource-flagged timeline falls into Resources.
//   4. "major-periods" catch-all.
export function groupForSlug(
  slug: string,
  isResourceTimeline?: boolean,
  dbGroup?: string | null,
): TimelineGroup {
  if (dbGroup && VALID_GROUPS.has(dbGroup)) return dbGroup as TimelineGroup;
  const mapped = TIMELINE_SLUG_TO_GROUP[slug];
  if (mapped) return mapped;
  if (isResourceTimeline) return "resources";
  return "major-periods";
}
