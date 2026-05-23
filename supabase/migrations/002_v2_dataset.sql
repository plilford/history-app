-- =============================================================================
-- v2 dataset: add dataset versioning and richer occurrence metadata.
-- =============================================================================
-- This migration extends the schema so that two independent datasets ('v1' and
-- 'v2') can coexist in the same tables. The frontend filters by dataset to
-- show one at a time. Non-breaking for v1 — existing rows default to v1.
-- =============================================================================

-- ---- events: add dataset, occurrence_type, date_uncertain -------------------
alter table events
  add column if not exists dataset text not null default 'v1';

alter table events
  add column if not exists occurrence_type text not null default 'event'
    check (occurrence_type in ('event', 'person', 'art'));

alter table events
  add column if not exists date_uncertain boolean not null default false;

create index if not exists events_dataset_idx on events (dataset);

-- ---- priorities: relax the 0–100 range check --------------------------------
-- v1 uses 0–100 floats. v2 uses 90_000–100_000. Both are valid; the frontend
-- only uses priority for ordering, never absolute magnitude.
alter table event_timeline_priorities
  drop constraint if exists event_timeline_priorities_priority_check;
alter table event_timeline_priorities
  add  constraint event_timeline_priorities_priority_check
       check (priority >= 0);

-- ---- timelines: add dataset, make uniqueness per-dataset --------------------
alter table timelines
  add column if not exists dataset text not null default 'v1';

-- The old constraints insist 'name' and 'slug' are globally unique. With two
-- datasets, the same name can legitimately appear in both, so the uniqueness
-- becomes per-(dataset, name).
alter table timelines drop constraint if exists timelines_name_key;
alter table timelines drop constraint if exists timelines_slug_key;

create unique index if not exists timelines_dataset_name_idx
  on timelines (dataset, name);
create unique index if not exists timelines_dataset_slug_idx
  on timelines (dataset, slug);
create index if not exists timelines_dataset_idx on timelines (dataset);
