-- =============================================================================
-- 015: ai_summary_allowlist caps + ai_summary_usage table
-- =============================================================================
-- Adds per-user daily / monthly call caps to the allowlist, and a log table
-- recording one row per /api/summary call.
--
-- Caps:
--   daily_cap, monthly_cap on ai_summary_allowlist. NULL = unlimited.
--   Defaults 20 / 200 for new entries — protective but easy to lift in the
--   admin dashboard.
--
-- Usage log:
--   ai_summary_usage(id, user_email, created_at). Worker inserts one row per
--   call (whether Anthropic succeeds or not — the request still counts toward
--   the cap because partial generations still spend tokens).
--
-- RLS on ai_summary_usage:
--   - Editor (is_editor()) — full read/write.
--   - Logged-in user — SELECT and INSERT only rows whose user_email matches
--     their JWT email. (Self-insert is safe: the only thing a user could do
--     by spamming inserts is exhaust their own quota faster — self-harm only.)
--   - Anonymous — no access.
-- =============================================================================

begin;

-- ---- allowlist caps -------------------------------------------------------
alter table ai_summary_allowlist
  add column if not exists daily_cap   int default 20,
  add column if not exists monthly_cap int default 200;

-- ---- usage log -----------------------------------------------------------
create table if not exists ai_summary_usage (
  id          bigserial   primary key,
  user_email  text        not null,
  created_at  timestamptz not null default now()
);

-- Fast lookup of "how many calls for this user since X" — the Worker queries
-- this on every request (day count + month count).
create index if not exists ai_summary_usage_email_time_idx
  on ai_summary_usage (user_email, created_at desc);

alter table ai_summary_usage enable row level security;

-- Editor: full read/write.
drop policy if exists "ai_summary_usage_editor_all" on ai_summary_usage;
create policy "ai_summary_usage_editor_all" on ai_summary_usage
  for all using (is_editor()) with check (is_editor());

-- Logged-in user: read your own usage.
drop policy if exists "ai_summary_usage_self_read" on ai_summary_usage;
create policy "ai_summary_usage_self_read" on ai_summary_usage
  for select using (
    lower(user_email) = lower(coalesce((auth.jwt() ->> 'email')::text, ''))
  );

-- Logged-in user: insert your own usage row.
drop policy if exists "ai_summary_usage_self_insert" on ai_summary_usage;
create policy "ai_summary_usage_self_insert" on ai_summary_usage
  for insert with check (
    lower(user_email) = lower(coalesce((auth.jwt() ->> 'email')::text, ''))
  );

grant select on ai_summary_usage to anon, authenticated;
grant insert on ai_summary_usage to authenticated;

commit;
