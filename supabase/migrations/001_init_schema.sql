-- =============================================================================
-- History App: initial schema
-- =============================================================================
-- Run this in the Supabase SQL editor (Dashboard -> SQL Editor -> New query).
-- Idempotent: safe to re-run.
-- =============================================================================

-- ---------- timelines ---------------------------------------------------------
create table if not exists timelines (
  id            serial primary key,
  name          text   not null unique,
  slug          text   not null unique,
  display_order integer not null default 0,
  is_featured   boolean not null default false,   -- defaults shown on app open
  created_at    timestamptz not null default now()
);

create index if not exists timelines_display_order_idx on timelines (display_order);

-- ---------- events ------------------------------------------------------------
create table if not exists events (
  id              bigint primary key,             -- carried over from spreadsheet column M
  description     text,
  event_short     text,
  person          text,
  display_name    text,
  type            text,
  region          text,
  country_at_time text,
  country_modern  text,

  -- year is BIGINT so we can store -4_500_000_000 (formation of the Earth)
  start_year      bigint,
  start_month     smallint,
  start_day       smallint,
  end_year        bigint,
  end_month       smallint,
  end_day         smallint,

  is_period       boolean not null default false,  -- column Z = 'period'
  display_date    text,
  period_length   integer,

  wikipedia_link  text,
  other_link      text,

  -- DERIVED: name of the timeline where this event has the highest priority.
  -- Maintained by trigger on event_timeline_priorities. Never write directly.
  main_category   text,

  -- Convenience: priority on the main 'all events' view (spreadsheet column AG).
  -- Editable, but defaults to max(priority) on insert via the importer.
  main_priority   real,

  zoom_hints      jsonb,                            -- optional, from columns F/G/H/I/J/L

  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now()
);

create index if not exists events_start_year_idx on events (start_year);
create index if not exists events_end_year_idx   on events (end_year);
create index if not exists events_main_priority_idx on events (main_priority desc);

-- ---------- junction: event x timeline (priority per timeline) ---------------
create table if not exists event_timeline_priorities (
  event_id    bigint  not null references events(id) on delete cascade,
  timeline_id integer not null references timelines(id) on delete cascade,
  priority    real    not null check (priority >= 0 and priority <= 100),
  primary key (event_id, timeline_id)
);

create index if not exists etp_timeline_priority_idx
  on event_timeline_priorities (timeline_id, priority desc);
create index if not exists etp_event_idx
  on event_timeline_priorities (event_id);

-- =============================================================================
-- Trigger: recompute events.main_category whenever priorities change
-- =============================================================================
-- main_category = name of the timeline where this event has the highest
-- priority. Tie-break by timelines.display_order ASC.
-- NULL if the event has no priority row anywhere.
-- =============================================================================

create or replace function recompute_main_category(p_event_id bigint)
returns void
language sql
as $$
  update events e set main_category = (
    select t.name
    from event_timeline_priorities p
    join timelines t on t.id = p.timeline_id
    where p.event_id = p_event_id
      and p.priority > 0
    order by p.priority desc, t.display_order asc
    limit 1
  )
  where e.id = p_event_id;
$$;

create or replace function trg_etp_recompute()
returns trigger
language plpgsql
as $$
begin
  if (tg_op = 'DELETE') then
    perform recompute_main_category(old.event_id);
    return old;
  else
    perform recompute_main_category(new.event_id);
    return new;
  end if;
end;
$$;

drop trigger if exists etp_after_insert  on event_timeline_priorities;
drop trigger if exists etp_after_update  on event_timeline_priorities;
drop trigger if exists etp_after_delete  on event_timeline_priorities;

create trigger etp_after_insert
  after insert on event_timeline_priorities
  for each row execute function trg_etp_recompute();

create trigger etp_after_update
  after update on event_timeline_priorities
  for each row execute function trg_etp_recompute();

create trigger etp_after_delete
  after delete on event_timeline_priorities
  for each row execute function trg_etp_recompute();

-- updated_at maintenance
create or replace function trg_set_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists events_set_updated_at on events;
create trigger events_set_updated_at
  before update on events
  for each row execute function trg_set_updated_at();

-- =============================================================================
-- Row-level security
-- =============================================================================
-- Reads are public (anonymous + authenticated).
-- Writes are restricted to the email allowlist defined below.
--
-- IMPORTANT: After signing up in Supabase Auth, edit the allowlist
-- by updating the editor_emails() function to include your email.
-- =============================================================================

alter table events                    enable row level security;
alter table timelines                 enable row level security;
alter table event_timeline_priorities enable row level security;

create or replace function editor_emails()
returns text[] language sql immutable as $$
  -- TODO: replace with your real email before going live
  select array['p.lilford@gmail.com']::text[];
$$;

create or replace function is_editor()
returns boolean language sql stable as $$
  select coalesce((auth.jwt() ->> 'email')::text = any (editor_emails()), false);
$$;

-- Public read
drop policy if exists "events_public_read" on events;
create policy "events_public_read"   on events
  for select using (true);

drop policy if exists "timelines_public_read" on timelines;
create policy "timelines_public_read" on timelines
  for select using (true);

drop policy if exists "etp_public_read" on event_timeline_priorities;
create policy "etp_public_read"      on event_timeline_priorities
  for select using (true);

-- Editor-only write
drop policy if exists "events_editor_write" on events;
create policy "events_editor_write"  on events
  for all using (is_editor()) with check (is_editor());

drop policy if exists "timelines_editor_write" on timelines;
create policy "timelines_editor_write" on timelines
  for all using (is_editor()) with check (is_editor());

drop policy if exists "etp_editor_write" on event_timeline_priorities;
create policy "etp_editor_write"     on event_timeline_priorities
  for all using (is_editor()) with check (is_editor());
