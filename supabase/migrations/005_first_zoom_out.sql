-- =============================================================================
-- first_zoom_out: name of the overall period this occurrence belongs to.
-- =============================================================================
-- Added 2026-05-17 to support a future zoom-out view that swaps a cluster of
-- specific sub-events for the umbrella period they belong to. When a long
-- period (e.g. "Tang dynasty", "Industrial Revolution") was broken into start
-- /end/mid sub-events, each sub-event records the umbrella period name here so
-- the UI can collapse them back together at lower zoom levels.
--
-- Nullable: most occurrences (singular events, persons, art works) have no
-- parent period and leave this null.
-- =============================================================================

alter table events
  add column if not exists first_zoom_out text;

create index if not exists events_first_zoom_out_idx
  on events (first_zoom_out)
  where first_zoom_out is not null;
