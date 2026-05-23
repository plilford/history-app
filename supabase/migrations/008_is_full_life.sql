-- Add is_full_life flag for person occurrences whose date range represents
-- the person's full lifespan (birth → death). A header toggle in the UI hides
-- these by default so the timeline isn't crowded with person bars.
--
-- Periods within a person's life (a reign, presidency, term in office, etc.)
-- are stored as type=event and don't carry is_full_life — they continue to
-- show regardless of the toggle.

alter table public.events
  add column if not exists is_full_life boolean not null default false;

create index if not exists events_is_full_life_idx
  on public.events (is_full_life) where is_full_life = true;
