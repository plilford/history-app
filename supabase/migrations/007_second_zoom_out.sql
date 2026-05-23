-- =============================================================================
-- second_zoom_out: name of the broader (level-2) period this occurrence belongs
-- to. Pairs with first_zoom_out to form a two-level rollup hierarchy.
-- =============================================================================
-- Added 2026-05-19 so the UI can collapse a cluster of sub-events through two
-- progressively-wider zoom levels:
--   - leaf zoom:    show individual events (Battle of Crecy)
--   - level-1 roll: collapse to first_zoom_out  (Edwardian War)
--   - level-2 roll: collapse to second_zoom_out (Hundred Years' War)
--
-- Each level's rollup target is a separate occurrence in `events` with the
-- matching title; the umbrella entry holds the full date range, description,
-- wikipedia link, etc. and is only shown by the UI at its rollup zoom level.
-- =============================================================================

alter table events
  add column if not exists second_zoom_out text;

create index if not exists events_second_zoom_out_idx
  on events (second_zoom_out)
  where second_zoom_out is not null;
