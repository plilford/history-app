-- =============================================================================
-- region weights: per-occurrence relevance score for each major world region
-- =============================================================================
-- Adds five smallint weight columns (europe, americas, asia, australasia,
-- africa) to events, each constrained to 1–10. The frontend exposes a slider
-- per region; their combined effect modulates ranking on the master and
-- arts-and-thoughts:main timelines so the user can tilt those views toward
-- regions they care about.
--
-- Defaults to 5 (neutral). The v2 importer fills these from the
-- `region_weights` dict in each occurrence's data file when present, falling
-- back to 5 across the board when not specified.
-- =============================================================================

alter table events
  add column if not exists weight_europe      smallint not null default 5
    check (weight_europe      between 1 and 10);

alter table events
  add column if not exists weight_americas    smallint not null default 5
    check (weight_americas    between 1 and 10);

alter table events
  add column if not exists weight_asia        smallint not null default 5
    check (weight_asia        between 1 and 10);

alter table events
  add column if not exists weight_australasia smallint not null default 5
    check (weight_australasia between 1 and 10);

alter table events
  add column if not exists weight_africa      smallint not null default 5
    check (weight_africa      between 1 and 10);
