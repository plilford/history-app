-- =============================================================================
-- 013: resource_subtype column on occurrences
-- =============================================================================
-- Resources come in flavours: podcast episodes, non-fiction books, fiction
-- books, documentaries, museum artifacts, etc. The frontend's colour
-- scheme branches on this (teal for non-fiction, purple for fiction;
-- future subtypes can add more), and future filters / search may want it.
--
-- Free-text column (no CHECK constraint) so new subtypes don't need a
-- migration. Convention: kebab-case strings —
--   'podcast-episode'
--   'book-nonfiction'
--   'book-fiction'
--   'documentary'
--   'museum-artifact'
-- Null is allowed and means "no specific subtype" (legitimate for podcast
-- episodes where the subtype is implicit from the timeline).
-- =============================================================================

begin;

alter table occurrences
  add column if not exists resource_subtype text;

commit;
