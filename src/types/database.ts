// Hand-written types mirroring the Postgres schema.
// (Can be regenerated with `supabase gen types typescript` later.)

export interface Timeline {
  id: number;
  name: string;
  slug: string;
  display_order: number;
  is_featured: boolean;
  /** Marks a timeline as a "resource" timeline (podcasts, books,
   *  documentaries…) — only occurrence rows with occurrence_type='resource'
   *  may carry priorities on these. The frontend filters resources from
   *  every non-resource timeline. */
  is_resource_timeline: boolean;
}

export interface Occurrence {
  id: number;
  /** Single canonical title (was event_short / display_name / person before
   *  migration 009). */
  title: string;
  description: string | null;

  start_year: number | null;
  start_month: number | null;
  start_day: number | null;
  end_year: number | null;
  end_month: number | null;
  end_day: number | null;

  /** Single representative day for this occurrence (e.g. signature year for a
   *  person; midpoint or peak for a period). Used by the UI to position the
   *  occurrence as one box when the whole range is on screen. */
  key_year: number | null;
  key_month: number | null;
  key_day: number | null;

  is_period: boolean;
  /** True when the occurrence is still going (reigns, presidencies, dynasties,
   *  etc.). end_year/end_month/end_day are null when this is set. */
  is_ongoing: boolean;
  display_date: string | null;

  wikipedia_link: string | null;
  other_link: string | null;
  /** Primary external URL for resource-type entries (podcast episode page,
   *  book seller / Wikipedia page, museum page). Null for regular events,
   *  people, and art. The popup uses this in place of wikipedia_link when
   *  occurrence_type='resource'. */
  resource_link: string | null;
  /** For multi-episode resources (e.g. a podcast series of 4 episodes
   *  bundled into one occurrence): list of `{title, url, date?}`.
   *  Null when a single resource_link is enough. */
  resource_episodes: Array<{ title: string; url: string; date?: string }> | null;
  /** Sub-type discriminator for resource-type rows. Convention:
   *  'podcast-episode', 'book-nonfiction', 'book-fiction', 'documentary',
   *  'museum-artifact'. Drives the frontend colour scheme. Null for
   *  non-resource rows (or resources whose subtype is implicit from the
   *  timeline). */
  resource_subtype: string | null;

  /** Computed by DB trigger. Do not write directly. */
  main_category: string | null;
  main_priority: number | null;

  occurrence_type: "event" | "person" | "art" | "resource";
  date_uncertain: boolean;

  /** Per-region weights (1-10), used by the region filter sliders to modulate
   *  ranking on the master and arts-and-thoughts timelines. Default 5. */
  weight_europe: number | null;
  weight_americas: number | null;
  weight_asia: number | null;
  weight_australasia: number | null;
  weight_africa: number | null;

  /** Name of the immediate umbrella period this occurrence belongs to (e.g.
   *  "Edwardian War" for a battle inside it). Null for standalone occurrences.
   *  At level-1 rollup zoom, occurrences with this set collapse into the
   *  entry whose title matches this string. */
  first_zoom_out: string | null;
  /** Name of the broader umbrella period one level above first_zoom_out (e.g.
   *  "Hundred Years' War" for a battle inside the Edwardian War). Null when
   *  the occurrence has only a single rollup level. */
  second_zoom_out: string | null;

  /** FK to occurrences(id) — populated by trigger from first_zoom_out/title
   *  lookup. Use these in joined queries; the text columns are the
   *  authoring interface. */
  first_zoom_out_id: number | null;
  second_zoom_out_id: number | null;

  /** True when this occurrence is a person's full lifespan (birth-death).
   *  Hidden by default via the "Show lifespans" header toggle. Shorter periods
   *  within a person's life (a reign, term in office, etc.) are stored as
   *  type=event and don't carry this flag. */
  is_full_life: boolean;
}

export interface OccurrenceTimelinePriority {
  occurrence_id: number;
  timeline_id: number;
  priority: number;
}

/** What we usually fetch: occurrence joined with its priority for a given
 *  timeline. */
export interface OccurrenceWithPriority extends Occurrence {
  priority: number;
}

/** Minimal projection of an on-screen occurrence sent to the /api/summary
 *  endpoint. Kept tiny so the request body stays a few KB even with a dense
 *  view. */
export interface CompactOccurrence {
  id: number;
  title: string;
  startYear: number | null;
  endYear: number | null;
  type: Occurrence["occurrence_type"];
  priority: number;
}

export interface UserFavourite {
  user_id: string;
  occurrence_id: number;
  created_at: string;
}

/** Junction row linking a resource occurrence to a subject occurrence it
 *  covers. Bidirectional — the relationship can be queried either way. */
export interface ResourceTag {
  resource_id: number;
  subject_id: number;
  created_at: string;
}

// ---------------------------------------------------------------------------
// Legacy aliases. App.tsx and components reference these names throughout;
// keeping them as type aliases avoids a large rename churn while the schema
// migration settles. New code should prefer the canonical Occurrence /
// OccurrenceWithPriority names.
// ---------------------------------------------------------------------------
export type HistoryEvent = Occurrence;
export type EventWithPriority = OccurrenceWithPriority;
