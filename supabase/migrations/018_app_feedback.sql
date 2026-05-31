-- =============================================================================
-- 018: app_feedback
-- =============================================================================
-- General app-level feedback from signed-in users — bugs, ideas, copy tweaks,
-- anything not tied to a single occurrence (those go to issue_flags, migration
-- 016). The editor reviews them in the same in-app dashboard as occurrence
-- flags, under an "App feedback" tab.
--
-- RLS (mirrors issue_flags):
--   - Any logged-in user — INSERT feedback, but only as themselves
--     (reporter_email must match their JWT email).
--   - Editor (is_editor()) — full read/write (review, resolve, delete).
--   - Anonymous — no access.
-- =============================================================================

begin;

create table if not exists app_feedback (
  id             bigserial   primary key,
  reporter_email text        not null,
  category       text,                          -- optional: bug|idea|copy|other|null
  message        text        not null,
  status         text        not null default 'open',  -- open|resolved
  user_agent     text,                          -- snapshot of the sender's browser (bug context)
  app_path       text,                          -- url path the sender was on, if captured
  created_at     timestamptz not null default now(),
  resolved_at    timestamptz
);

create index if not exists app_feedback_status_idx
  on app_feedback (status, created_at desc);

alter table app_feedback enable row level security;

-- Logged-in user: file feedback, but only as themselves (case-insensitive email
-- match — emails elsewhere are normalised that way too).
drop policy if exists "app_feedback_self_insert" on app_feedback;
create policy "app_feedback_self_insert" on app_feedback
  for insert with check (
    lower(reporter_email) = lower(coalesce((auth.jwt() ->> 'email')::text, ''))
  );

-- Editor: full read/write (review, resolve, delete).
drop policy if exists "app_feedback_editor_all" on app_feedback;
create policy "app_feedback_editor_all" on app_feedback
  for all using (is_editor()) with check (is_editor());

-- Explicit grants — Supabase is changing the Data API default for the public
-- schema in October 2026 (new tables won't be auto-exposed). Adding grants
-- here future-proofs this table.
grant insert, select, update, delete on app_feedback to authenticated;
grant usage, select on sequence app_feedback_id_seq to authenticated;

commit;
