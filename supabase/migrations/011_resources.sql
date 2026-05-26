-- =============================================================================
-- 011: Resource-type occurrences + resource_tags junction
-- =============================================================================
-- Adds support for a new kind of occurrence — RESOURCES — covering things
-- like podcast episodes, history books, documentaries, museum artifacts.
-- Resources don't belong to history themselves; they're meta-content ABOUT
-- history. They render in their own dedicated timelines (slugs marked with
-- is_resource_timeline=true) and never appear on regular timelines.
--
-- Each resource can be tagged to one or more SUBJECTS — the regular
-- occurrences it discusses. This is bidirectional: a regular event's popup
-- will offer "resources about this" while a resource entry knows what
-- subjects it covers.
--
-- Changes:
--   1. occurrences:
--        + resource_link text       — primary external URL (replaces
--                                     wikipedia_link semantically for
--                                     resource rows; wikipedia_link stays
--                                     populated when the resource also has
--                                     a wiki page).
--        + resource_episodes jsonb  — for multi-episode podcast series
--                                     bundled into one occurrence:
--                                     [{title, url, date}, ...].
--   2. timelines:
--        + is_resource_timeline bool not null default false  — discriminator
--          for resource timelines (the-rest-is-history-podcast,
--          popular-history-books, and future similar).
--   3. resource_tags(resource_id, subject_id, created_at) — junction table
--      linking a resource to its subjects. CASCADE on either side. Public
--      read, editor-only write.
--   4. trigger on occurrence_timeline_priorities to enforce:
--        - resource-type occurrence rows can ONLY belong to a
--          resource-type timeline (and vice versa).
-- =============================================================================

begin;

-- ----- 1. occurrences columns ------------------------------------------------
alter table occurrences
  add column if not exists resource_link     text,
  add column if not exists resource_episodes jsonb;

-- ----- 2. timelines flag -----------------------------------------------------
alter table timelines
  add column if not exists is_resource_timeline boolean not null default false;

create index if not exists timelines_is_resource_idx
  on timelines (is_resource_timeline) where is_resource_timeline;

-- ----- 3. resource_tags junction ---------------------------------------------
create table if not exists resource_tags (
  resource_id bigint not null references occurrences(id) on delete cascade,
  subject_id  bigint not null references occurrences(id) on delete cascade,
  created_at  timestamptz not null default now(),
  primary key (resource_id, subject_id),
  check (resource_id <> subject_id)
);

create index if not exists resource_tags_subject_idx on resource_tags (subject_id);

alter table resource_tags enable row level security;

drop policy if exists "resource_tags_public_read" on resource_tags;
create policy "resource_tags_public_read" on resource_tags
  for select using (true);

drop policy if exists "resource_tags_editor_write" on resource_tags;
create policy "resource_tags_editor_write" on resource_tags
  for all using (is_editor()) with check (is_editor());

-- ----- 4. Resource/timeline-type invariant -----------------------------------
-- A resource-type occurrence MUST live on a resource-type timeline, and a
-- non-resource occurrence MUST live on a non-resource timeline. This keeps
-- regular timelines from ever picking up resource rows, and prevents
-- accidental cross-pollination from the importer.
create or replace function trg_otp_check_resource()
returns trigger
language plpgsql
as $$
declare
  v_is_resource          boolean;
  v_is_resource_timeline boolean;
  v_occ_type             text;
  v_tl_name              text;
begin
  select occurrence_type = 'resource', occurrence_type
    into v_is_resource, v_occ_type
    from occurrences where id = new.occurrence_id;
  select is_resource_timeline, name
    into v_is_resource_timeline, v_tl_name
    from timelines where id = new.timeline_id;
  if v_is_resource and not v_is_resource_timeline then
    raise exception
      'resource occurrence id=% (type=%) cannot be priority-tagged on non-resource timeline %',
      new.occurrence_id, v_occ_type, v_tl_name;
  end if;
  if not v_is_resource and v_is_resource_timeline then
    raise exception
      'non-resource occurrence id=% (type=%) cannot be priority-tagged on resource timeline %',
      new.occurrence_id, v_occ_type, v_tl_name;
  end if;
  return new;
end;
$$;

drop trigger if exists otp_check_resource on occurrence_timeline_priorities;
create trigger otp_check_resource
  before insert or update on occurrence_timeline_priorities
  for each row execute function trg_otp_check_resource();

commit;
