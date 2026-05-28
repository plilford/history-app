-- =============================================================================
-- 014: ai_summary_allowlist
-- =============================================================================
-- Per-user access list for the editor-only AI summary feature. Managed by
-- the editor via the in-app "Manage AI access" dashboard.
--
-- RLS:
--   - Editor (is_editor()) — read + write the whole table.
--   - Any other logged-in user — read ONLY their own row, so the frontend can
--     check whether the current user is allowed to summarise without exposing
--     the rest of the list.
--   - Anonymous — no access.
-- =============================================================================

begin;

create table if not exists ai_summary_allowlist (
  email      text         primary key,
  is_active  boolean      not null default true,
  added_at   timestamptz  not null default now(),
  added_by   text,                                 -- editor email that added the entry
  notes      text                                  -- optional free-text (e.g. "friend testing")
);

create index if not exists ai_summary_allowlist_active_idx
  on ai_summary_allowlist (is_active);

alter table ai_summary_allowlist enable row level security;

-- Editor: full read/write.
drop policy if exists "ai_summary_allowlist_editor_all" on ai_summary_allowlist;
create policy "ai_summary_allowlist_editor_all" on ai_summary_allowlist
  for all using (is_editor()) with check (is_editor());

-- Logged-in user: read your own row only (case-insensitive match — emails
-- elsewhere are normalised that way too).
drop policy if exists "ai_summary_allowlist_self_read" on ai_summary_allowlist;
create policy "ai_summary_allowlist_self_read" on ai_summary_allowlist
  for select using (
    lower(email) = lower(coalesce((auth.jwt() ->> 'email')::text, ''))
  );

-- Explicit grants — Supabase is changing the Data API default for the public
-- schema in October 2026 (new tables won't be auto-exposed). Adding grants
-- here future-proofs this table.
grant select on ai_summary_allowlist to anon, authenticated;
grant insert, update, delete on ai_summary_allowlist to authenticated;

commit;
