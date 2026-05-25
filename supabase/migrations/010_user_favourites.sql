-- =============================================================================
-- 010: user_favourites table
-- =============================================================================
-- Per-user "favourites" list. Backs the "My Favourites" pseudo-timeline that
-- appears at the top of the timeline picker for any logged-in user, and the
-- heart badge that appears on favourited occurrences in every timeline view.
--
-- RLS: every user can read/insert/delete only their own rows. There's no
-- editor allowlist concept here — anyone with an auth session can manage
-- their own favourites.
-- =============================================================================

begin;

create table if not exists user_favourites (
  user_id       uuid    not null references auth.users(id) on delete cascade,
  occurrence_id bigint  not null references occurrences(id) on delete cascade,
  created_at    timestamptz not null default now(),
  primary key (user_id, occurrence_id)
);

-- Lookup the user's full list quickly (we read this once per session and keep
-- in memory; an index keeps it cheap even when a user has thousands).
create index if not exists user_favourites_user_idx
  on user_favourites (user_id, created_at desc);

-- For the "is anyone favouriting X" reverse lookup (not used yet, but cheap
-- to have).
create index if not exists user_favourites_occurrence_idx
  on user_favourites (occurrence_id);

alter table user_favourites enable row level security;

-- Read your own favourites only. (No public-read — favourites are private.)
drop policy if exists "user_favourites_self_read" on user_favourites;
create policy "user_favourites_self_read" on user_favourites
  for select using (auth.uid() = user_id);

-- Insert your own favourites only.
drop policy if exists "user_favourites_self_insert" on user_favourites;
create policy "user_favourites_self_insert" on user_favourites
  for insert with check (auth.uid() = user_id);

-- Delete your own favourites only.
drop policy if exists "user_favourites_self_delete" on user_favourites;
create policy "user_favourites_self_delete" on user_favourites
  for delete using (auth.uid() = user_id);

commit;
