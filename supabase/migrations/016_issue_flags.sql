-- =============================================================================
-- 016: issue_flags
-- =============================================================================
-- User-reported issues / suggestions for individual occurrences. Any signed-in
-- user can file a flag against an occurrence (wrong date, typo, mis-ranked
-- priority, etc.); the editor reviews them via the in-app "Review flagged
-- issues" dashboard.
--
-- RLS:
--   - Any logged-in user — INSERT a flag, but only as themselves
--     (reporter_email must match their JWT email).
--   - Editor (is_editor()) — full read/write (review, resolve, delete).
--   - Anonymous — no access.
-- =============================================================================

begin;

create table if not exists issue_flags (
  id               bigserial   primary key,
  occurrence_id    bigint      not null references occurrences(id) on delete cascade,
  occurrence_title text        not null,            -- snapshot for review display
  reporter_email   text        not null,
  aspect           text        not null,            -- title|description|date|resources|priority|other
  note             text,                            -- optional, required only for "other" (enforced client-side)
  status           text        not null default 'open',  -- open|resolved
  created_at       timestamptz not null default now(),
  resolved_at      timestamptz
);

create index if not exists issue_flags_status_idx
  on issue_flags (status, created_at desc);

alter table issue_flags enable row level security;

-- Logged-in user: file a flag, but only as themselves (case-insensitive email
-- match — emails elsewhere are normalised that way too).
drop policy if exists "issue_flags_self_insert" on issue_flags;
create policy "issue_flags_self_insert" on issue_flags
  for insert with check (
    lower(reporter_email) = lower(coalesce((auth.jwt() ->> 'email')::text, ''))
  );

-- Editor: full read/write (review, resolve, delete).
drop policy if exists "issue_flags_editor_all" on issue_flags;
create policy "issue_flags_editor_all" on issue_flags
  for all using (is_editor()) with check (is_editor());

-- Explicit grants — Supabase is changing the Data API default for the public
-- schema in October 2026 (new tables won't be auto-exposed). Adding grants
-- here future-proofs this table.
grant insert, select, update, delete on issue_flags to authenticated;
grant usage, select on sequence issue_flags_id_seq to authenticated;

commit;
