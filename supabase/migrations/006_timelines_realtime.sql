-- =============================================================================
-- Enable Supabase Realtime change-streams for the `timelines` table so the
-- frontend timeline picker stays in sync when a new timeline is added/renamed/
-- removed from the database.
-- =============================================================================
-- Postgres ships a publication called `supabase_realtime` that the Realtime
-- service replicates from. Adding `timelines` to it is what makes
-- `supabase.channel(...).on('postgres_changes', ...)` actually fire for
-- changes to this table.
-- =============================================================================

do $$
begin
  if not exists (
    select 1 from pg_publication where pubname = 'supabase_realtime'
  ) then
    create publication supabase_realtime;
  end if;
end
$$;

do $$
begin
  if not exists (
    select 1
      from pg_publication_tables
     where pubname = 'supabase_realtime'
       and schemaname = 'public'
       and tablename = 'timelines'
  ) then
    alter publication supabase_realtime add table public.timelines;
  end if;
end
$$;
