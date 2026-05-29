-- Add a nullable `group` column to timelines so the dropdown's section
-- grouping is data-driven rather than relying solely on a hardcoded
-- slug→group map in the frontend. New timelines set their group here (via
-- the importer's TIMELINES list) and land in the right dropdown section
-- without a frontend code change.
--
-- Values mirror the frontend TimelineGroup union in src/lib/timelineGroups.ts:
--   worldwide | europe | americas | asia | africa | australasia
--   | conflicts | religions | major-periods | resources
-- Nullable: a NULL group falls back to the frontend slug-map / resource-flag
-- / "major-periods" default, so this is backward-compatible.

alter table timelines add column if not exists "group" text;

-- Backfill existing timelines to their dropdown sections.
update timelines set "group" = 'worldwide'     where slug in ('master', 'arts-and-thoughts', 'people');
update timelines set "group" = 'europe'         where slug in ('england', 'england-monarchs', 'wales', 'france', 'germany', 'roman-history', 'roman-emperors', 'ancient-greece');
update timelines set "group" = 'americas'       where slug in ('usa', 'us-presidents', 'pre-columbian-americas');
update timelines set "group" = 'asia'           where slug in ('china', 'india', 'japan', 'ottoman');
update timelines set "group" = 'conflicts'      where slug in ('ww1', 'ww2', 'cold-war', 'napoleonic', 'crusades');
update timelines set "group" = 'religions'      where slug in ('major-religions', 'christianity', 'islam', 'judaism');
update timelines set "group" = 'major-periods'  where slug in ('renaissance', 'industrial');
update timelines set "group" = 'resources'      where slug in ('resources-combined', 'the-rest-is-history-podcast', 'popular-history-books');
