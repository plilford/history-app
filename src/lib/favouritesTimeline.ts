// Sentinel values for the "My Favourites" pseudo-timeline. There is no
// matching row in the `timelines` table — it's a frontend-only construct that
// the TimelinePicker special-cases at the top of the list and that
// TimelineColumn renders by fetching occurrences via user_favourites instead
// of occurrence_timeline_priorities.
//
// We use a slug starting with `__` so it can't collide with a real DB slug
// (which are lowercase-kebab-case).

export const FAVOURITES_TIMELINE_SLUG = "__favourites__";
export const FAVOURITES_TIMELINE_NAME = "My Favourites";
// Negative id, so it can't collide with any real timelines.id (serial >= 1).
export const FAVOURITES_TIMELINE_ID = -1;
