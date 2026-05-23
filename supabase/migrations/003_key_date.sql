-- =============================================================================
-- key_date: a single representative day for each occurrence
-- =============================================================================
-- Adds key_year/key_month/key_day to events. Used by the UI to position a
-- period/person as a single box (instead of two boxes for start+end) when the
-- whole range is on screen. Falls back to start/end when key_date is offscreen.
--
-- All three columns are nullable. The v2 importer fills key_year with the
-- midpoint of (start_year, end_year) when not specified, or start_year for
-- point events. key_month / key_day stay null unless explicitly set in data.
-- =============================================================================

alter table events
  add column if not exists key_year  bigint;

alter table events
  add column if not exists key_month smallint;

alter table events
  add column if not exists key_day   smallint;

create index if not exists events_key_year_idx on events (key_year);
