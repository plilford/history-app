-- =============================================================================
-- 012: Widen the occurrence_type CHECK to include 'resource'
-- =============================================================================
-- Migration 002 added: check (occurrence_type in ('event', 'person', 'art'))
-- That blocked the importer from inserting resource-type rows. Drop and
-- recreate with 'resource' in the allow-list.
-- =============================================================================

begin;

-- Constraint name is "events_occurrence_type_check" (Postgres named it from
-- the old `events` table; the rename in 009 carried the constraint with it
-- under the old name).
alter table occurrences
  drop constraint if exists events_occurrence_type_check;

alter table occurrences
  add constraint occurrences_occurrence_type_check
    check (occurrence_type in ('event', 'person', 'art', 'resource'));

commit;
