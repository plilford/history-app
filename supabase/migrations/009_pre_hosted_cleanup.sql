-- =============================================================================
-- 009: Pre-hosted-Supabase cleanup
-- =============================================================================
-- Run this once on the local DB before pg_dump / pg_restore to hosted Supabase.
-- Tidies up things that accumulated during v1→v2 development and that we don't
-- want to inherit on the hosted instance.
--
-- Changes (in execution order):
--
--   1.  Drop the legacy v1 dataset entirely (rows + dataset discriminator
--       column).
--   2.  Restore globally-unique (name, slug) on timelines (was per-dataset
--       in 002 to let v1 + v2 coexist).
--   3.  Consolidate event_short / display_name / person → single `title`.
--   4.  Change priority from real → integer.
--   5.  Replace the `end_year = 2026` placeholder with an explicit
--       `is_ongoing` boolean + NULL end_year/month/day.
--   6.  Drop dead columns: zoom_hints, period_length, country_at_time,
--       country_modern, region. (Keep is_period + is_full_life flags.)
--   7.  pg_trgm extension + GIN trigram indexes on title/description for
--       fast ILIKE search on hosted.
--   8.  Add `start_year <= end_year` check constraint.
--   9.  Rename `events` → `occurrences`, `event_timeline_priorities` →
--       `occurrence_timeline_priorities`, `event_id` → `occurrence_id`.
--       Recreate the related functions, triggers, indexes, and RLS policies
--       at the new names.
--  10.  Auto-maintain `main_priority` via the same trigger that maintains
--       `main_category` (was previously a stale denormalisation set only by
--       the importer).
--  11.  Add `first_zoom_out_id` / `second_zoom_out_id` FK columns alongside
--       the existing text. Backfill from title lookups; provide a SQL
--       helper `rebuild_zoom_out_ids()` for the importer to call after bulk
--       upserts; provide a per-row BEFORE INSERT/UPDATE trigger for normal
--       CRUD via the API.
--
-- One transaction so a partial run leaves nothing behind.
-- =============================================================================

begin;

-- ----------------------------------------------------------------------------
-- 1. Drop the v1 dataset rows.
-- ----------------------------------------------------------------------------
delete from event_timeline_priorities
  where event_id in (select id from events where dataset = 'v1');
delete from events    where dataset = 'v1';
delete from timelines where dataset = 'v1';

-- ----------------------------------------------------------------------------
-- 2. Drop the `dataset` column and restore globally-unique name/slug.
-- ----------------------------------------------------------------------------
drop index if exists timelines_dataset_name_idx;
drop index if exists timelines_dataset_slug_idx;
drop index if exists timelines_dataset_idx;
drop index if exists events_dataset_idx;

alter table timelines drop column if exists dataset;
alter table events    drop column if exists dataset;

alter table timelines drop constraint if exists timelines_name_key;
alter table timelines drop constraint if exists timelines_slug_key;
alter table timelines add  constraint timelines_name_key unique (name);
alter table timelines add  constraint timelines_slug_key unique (slug);

-- ----------------------------------------------------------------------------
-- 3. Consolidate event_short + display_name + person → title.
--    event_short was the canonical v2 title; fall back to the other two for
--    any v1 leftovers (should be none after step 1, but defensive).
-- ----------------------------------------------------------------------------
alter table events add column if not exists title text;
update events
   set title = coalesce(event_short, display_name, person)
 where title is null;
alter table events alter column title set not null;

alter table events drop column if exists event_short;
alter table events drop column if exists display_name;
alter table events drop column if exists person;

-- ----------------------------------------------------------------------------
-- 4. priority: real → integer. The v2 importer already writes integer-valued
--    priorities (90_000..100_000), so the cast is lossless.
-- ----------------------------------------------------------------------------
alter table event_timeline_priorities
  alter column priority type integer using priority::integer;

alter table event_timeline_priorities
  drop constraint if exists event_timeline_priorities_priority_check;
alter table event_timeline_priorities
  add  constraint event_timeline_priorities_priority_check
       check (priority >= 0);

-- ----------------------------------------------------------------------------
-- 5. is_ongoing replaces the `end_year = 2026` placeholder. The convention
--    breaks the moment 2027 rolls around, so make it explicit.
-- ----------------------------------------------------------------------------
alter table events
  add column if not exists is_ongoing boolean not null default false;

update events
   set is_ongoing = true,
       end_year   = null,
       end_month  = null,
       end_day    = null
 where end_year = 2026;

-- ----------------------------------------------------------------------------
-- 6. Drop dead columns.
-- ----------------------------------------------------------------------------
alter table events drop column if exists zoom_hints;
alter table events drop column if exists period_length;
alter table events drop column if exists country_at_time;
alter table events drop column if exists country_modern;
alter table events drop column if exists region;

-- ----------------------------------------------------------------------------
-- 7. pg_trgm + GIN trigram indexes. SearchBar uses `ilike '%term%'` which
--    is exactly what trigram indexes accelerate. Indexed columns must exist
--    in their final form, so we create the indexes AFTER the column ops.
-- ----------------------------------------------------------------------------
create extension if not exists pg_trgm;

create index if not exists events_title_trgm_idx
  on events using gin (title gin_trgm_ops);
create index if not exists events_description_trgm_idx
  on events using gin (description gin_trgm_ops);

-- ----------------------------------------------------------------------------
-- 8. start_year <= end_year check.
-- ----------------------------------------------------------------------------
alter table events drop constraint if exists events_start_le_end_chk;
alter table events
  add  constraint events_start_le_end_chk
       check (
         start_year is null
         or end_year is null
         or start_year <= end_year
       );

-- ----------------------------------------------------------------------------
-- 9. Rename events → occurrences and friends. Drop the old trigger functions
--    first (they reference the old column names by string); recreate against
--    the new names afterwards.
-- ----------------------------------------------------------------------------
drop function if exists recompute_main_category(bigint) cascade;
drop function if exists trg_etp_recompute() cascade;

alter table events                    rename to occurrences;
alter table event_timeline_priorities rename to occurrence_timeline_priorities;
alter table occurrence_timeline_priorities rename column event_id to occurrence_id;

-- Rename the indexes that survived the table rename with their old names.
alter index if exists events_start_year_idx        rename to occurrences_start_year_idx;
alter index if exists events_end_year_idx          rename to occurrences_end_year_idx;
alter index if exists events_main_priority_idx     rename to occurrences_main_priority_idx;
alter index if exists events_key_year_idx          rename to occurrences_key_year_idx;
alter index if exists events_first_zoom_out_idx    rename to occurrences_first_zoom_out_idx;
alter index if exists events_second_zoom_out_idx   rename to occurrences_second_zoom_out_idx;
alter index if exists events_is_full_life_idx      rename to occurrences_is_full_life_idx;
alter index if exists events_title_trgm_idx        rename to occurrences_title_trgm_idx;
alter index if exists events_description_trgm_idx  rename to occurrences_description_trgm_idx;
alter index if exists etp_timeline_priority_idx    rename to otp_timeline_priority_idx;
alter index if exists etp_event_idx                rename to otp_occurrence_idx;

-- Rename the updated_at trigger for tidiness (the function it calls is
-- name-stable so doesn't need touching).
drop trigger if exists events_set_updated_at on occurrences;
create trigger occurrences_set_updated_at
  before update on occurrences
  for each row execute function trg_set_updated_at();

-- Rewrite RLS policy names to match the new tables.
drop policy if exists "events_public_read"  on occurrences;
drop policy if exists "events_editor_write" on occurrences;
drop policy if exists "etp_public_read"     on occurrence_timeline_priorities;
drop policy if exists "etp_editor_write"    on occurrence_timeline_priorities;

create policy "occurrences_public_read"  on occurrences
  for select using (true);
create policy "occurrences_editor_write" on occurrences
  for all using (is_editor()) with check (is_editor());
create policy "otp_public_read"  on occurrence_timeline_priorities
  for select using (true);
create policy "otp_editor_write" on occurrence_timeline_priorities
  for all using (is_editor()) with check (is_editor());

-- ----------------------------------------------------------------------------
-- 10. recompute_main_for_occurrence: keeps both `main_category` AND
--     `main_priority` in sync with occurrence_timeline_priorities. Previously
--     only main_category was trigger-maintained; main_priority was an
--     importer-only column that silently went stale on any DB-side edit.
-- ----------------------------------------------------------------------------
create or replace function recompute_main_for_occurrence(p_occurrence_id bigint)
returns void
language sql
as $$
  update occurrences o set
    main_category = (
      select t.name
        from occurrence_timeline_priorities p
        join timelines t on t.id = p.timeline_id
       where p.occurrence_id = p_occurrence_id
         and p.priority > 0
       order by p.priority desc, t.display_order asc
       limit 1
    ),
    main_priority = (
      select max(p.priority)
        from occurrence_timeline_priorities p
       where p.occurrence_id = p_occurrence_id
         and p.priority > 0
    )
  where o.id = p_occurrence_id;
$$;

create or replace function trg_otp_recompute()
returns trigger
language plpgsql
as $$
begin
  if (tg_op = 'DELETE') then
    perform recompute_main_for_occurrence(old.occurrence_id);
    return old;
  else
    perform recompute_main_for_occurrence(new.occurrence_id);
    return new;
  end if;
end;
$$;

drop trigger if exists otp_after_insert on occurrence_timeline_priorities;
drop trigger if exists otp_after_update on occurrence_timeline_priorities;
drop trigger if exists otp_after_delete on occurrence_timeline_priorities;

create trigger otp_after_insert
  after insert on occurrence_timeline_priorities
  for each row execute function trg_otp_recompute();
create trigger otp_after_update
  after update on occurrence_timeline_priorities
  for each row execute function trg_otp_recompute();
create trigger otp_after_delete
  after delete on occurrence_timeline_priorities
  for each row execute function trg_otp_recompute();

-- One-shot recompute so existing rows reflect what the trigger would produce.
do $$
declare
  o_id bigint;
begin
  for o_id in select id from occurrences loop
    perform recompute_main_for_occurrence(o_id);
  end loop;
end
$$;

-- ----------------------------------------------------------------------------
-- 11. FK columns for the umbrella-period rollup hierarchy. The text columns
--     (first_zoom_out, second_zoom_out) remain — they're the authoring
--     interface in the master.py data files — but every row also gets an
--     `id` column referencing the parent occurrence, enforced by FK.
--
--     Bulk fix is `select rebuild_zoom_out_ids()` — the importer calls this
--     once at the end of its run, after all rows have been upserted.
--     Single-row CRUD via the API is covered by the BEFORE INSERT/UPDATE
--     trigger, which does a title lookup whenever the text changes.
-- ----------------------------------------------------------------------------
alter table occurrences
  add column if not exists first_zoom_out_id  bigint references occurrences(id) on delete set null;
alter table occurrences
  add column if not exists second_zoom_out_id bigint references occurrences(id) on delete set null;

create index if not exists occurrences_first_zoom_out_id_idx
  on occurrences (first_zoom_out_id) where first_zoom_out_id is not null;
create index if not exists occurrences_second_zoom_out_id_idx
  on occurrences (second_zoom_out_id) where second_zoom_out_id is not null;

create or replace function rebuild_zoom_out_ids()
returns void
language sql
as $$
  update occurrences o
     set first_zoom_out_id = (
       select u.id from occurrences u
        where lower(trim(u.title)) = lower(trim(o.first_zoom_out))
          and u.id <> o.id
        limit 1
     )
   where o.first_zoom_out is not null;

  update occurrences o
     set second_zoom_out_id = (
       select u.id from occurrences u
        where lower(trim(u.title)) = lower(trim(o.second_zoom_out))
          and u.id <> o.id
        limit 1
     )
   where o.second_zoom_out is not null;
$$;

-- Backfill once now that the columns exist.
select rebuild_zoom_out_ids();

-- Per-row trigger: keeps FK columns in sync with any direct text edit.
create or replace function trg_sync_zoom_out_ids()
returns trigger
language plpgsql
as $$
begin
  if new.first_zoom_out is null then
    new.first_zoom_out_id := null;
  else
    new.first_zoom_out_id := (
      select id from occurrences
       where lower(trim(title)) = lower(trim(new.first_zoom_out))
         and id <> new.id
       limit 1
    );
  end if;

  if new.second_zoom_out is null then
    new.second_zoom_out_id := null;
  else
    new.second_zoom_out_id := (
      select id from occurrences
       where lower(trim(title)) = lower(trim(new.second_zoom_out))
         and id <> new.id
       limit 1
    );
  end if;
  return new;
end;
$$;

drop trigger if exists occurrences_sync_zoom_out_ids on occurrences;
create trigger occurrences_sync_zoom_out_ids
  before insert or update on occurrences
  for each row execute function trg_sync_zoom_out_ids();

commit;
