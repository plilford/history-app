# Session handover — paste this into the next conversation

This session (2026-05-26) wrapped major feature work and content build-up on the Ever-When timeline app. The chat got long — starting a fresh one. Below is everything the next session needs.

---

## TL;DR for the next session

The app at https://ever-when.com now has:
- **Auth + favourites + suggestions popup** (Phase 1 of the original brief)
- **Region-based occurrence colours, dark/light mode** (UI batch)
- **Umbrella ⊞ badge + ChildrenPopup**, child ↰ indicator (rollup UX)
- **Resource type system** — podcasts (The Rest Is History: 181 episodes) and books (162 NF + 92 fiction) live in dedicated "resource" timelines. The renderer places resources by the dates of their **tagged subjects** (so a Joan of Arc book shows in the books column at ~1430 when Joan of Arc is in the master viewport, regardless of when the book was published).
- **📚 badge in EventPopup** showing how many resources cover the subject + ResourcesPopup listing them.
- **Tag chips at the bottom of the popup** for resources — click navigates to the tagged subject.

Hosted Supabase state: **4,753 occurrences**, **377 resource_tag rows**, migrations 001-013 applied.

---

## Outstanding work the user asked for, deferred to this new session

### 1. Rest of TRIH episodes (~370 more, episode 301 → 955)

**The archive site at archive.therestishistory.com is JS-rendered but its API IS accessible** (curl works with a normal user-agent). Confirmed working endpoint: `https://archive.therestishistory.com/api/catalog/episode/{archive_id}`

Sample response includes:
```json
{
  "title": "...",
  "date": "2025-04-30",
  "description": "<rich episode summary>",
  "historical_events": ["Death of Empress Teishi (childbirth, c.1000)", ...],
  "historical_figures": ["Murasaki Shikibu", "Fujiwara no Michinaga", ...],
  "books": [{ "author": "Murasaki Shikibu", "title": "The Tale of Genji" }, ...],
  "eras": [{ "id": 3, "name": "Late Antiquity & Early Middle Ages", ... }]
}
```

**`archive_id` is NOT the same as TRIH episode number.** Archive IDs are internal (saw 65-955 range). To map archive_id ↔ TRIH ep_num, either:
- Scrape the timeline page (`https://archive.therestishistory.com/`) for `<a href="/catalog/episode/N">` links plus their surrounding episode titles — the title contains the TRIH ep number ("65. A Very British Scandal" style).
- Or fetch each archive_id in 1..1000 and match the `date` + `description` field against the existing TRIH RSS data already in `tools/v2/data/_research/trih_episodes_raw.json`.

**Workflow plan for the next session:**

```
1. Extend tools/v2/data/_research/parse_trih_rss.py to keep ALL 672 numbered
   episodes (not just the first 300).
2. Write a fetcher that walks all archive episode IDs, joins to the RSS data
   by date or title, and produces an enriched JSON with historical_events,
   historical_figures, books lists per TRIH episode.
3. Rebuild tools/v2/data/the_rest_is_history.py from the merged data.
   The archive's historical_events / historical_figures lists are MUCH better
   than the heuristic regex matching the current curator uses — many of the
   "thematic" episodes I had to skip will now be datable.
4. Validate + import + apply (will likely need the standalone tag-only
   importer if rebuild_zoom_out_ids times out again — see CLAUDE.md
   gotcha note).
```

If archive API rate-limits, throttle to ~1 req/sec. Episodes are stable so a single fetch is enough.

### 2. Improve tagging on the existing 181 TRIH episodes

Same archive API. The new session should retag the first-300 entries using `historical_events` + `historical_figures` from the archive, which are much more accurate than the substring matching I used. Result will be more 📚 badges in the popup and richer cross-references in the resource column.

### 3. Add 50-100 new occurrences to master.py

See **`tools/v2/curation/suggested_new_occurrences.md`** for my draft list, organised by persons / events / works. Many gaps were surfaced by tag-validation failures during the books curation — these are the subjects routinely referenced by popular history books / podcasts that don't yet have a `master.py` entry. After importing them, run `python -m v2.curation.suggest_resource_tags --since <new_id>` to auto-find existing resources that should now tag the new subjects.

### 4. (Optional) Top up books

Phase 3 came in at 162 NF + 92 fiction (target was 200 + 100). The dataset is the most popular / canonical history books — topping up means going further down the popularity ranking. Easy to add: just append entries to `_NONFICTION` or `_FICTION` in `tools/v2/data/popular_history_books.py` and re-import.

---

## Key tools the next session inherits

### Curation scripts (`tools/v2/curation/`)

- **`suggest_resource_tags.py`** — after adding new master.py entries, finds existing resources whose title/description mentions the new subject. Run with `--since <id>`. Conservative word-bounded matching.
- **`import_resource_tags_only.py`** — recovery script when the main importer hits Supabase's 8-second statement timeout on `rebuild_zoom_out_ids()` and never reaches the tag step. Idempotent.
- **`dedupe_round_j.py`** — the comprehensive auto-dedup. Knows not to cluster "X begins" with the "X" period (that's a rollup pattern, not a duplicate).
- **`fix_region_weights.py`** — sets proper regional bias on entries that had been left at all-5 placeholder.
- **`audit_and_fix_slugs.py`** — auto-tags missed major-religions / people / arts-and-thoughts / WW slugs.

### Research scripts (`tools/v2/data/_research/`)

- **`parse_trih_rss.py`** — pulls Megaphone RSS → JSON (first 300 numbered eps currently)
- **`curate_trih.py`** — auto-curator: groups multi-part series, infers dates, suggests tags
- **`manual_curations.py`** — explicit per-item OVERRIDES dict (247 entries)
- **`generate_trih_module.py`** — merges auto + manual → the_rest_is_history.py
- **`fix_books_tags.py`** — one-shot tag-string fixer used during books curation
- *(All of `tools/v2/data/_research/` is gitignored except `.py` files — raw JSON snapshots regenerate from the scripts)*

### Data modules (`tools/v2/data/`)

- `master.py` — 4,318 regular occurrences (events / people / art)
- `the_rest_is_history.py` — 181 podcast resources
- `popular_history_books.py` — 254 book resources

---

## What just shipped (last commits, all on `main`)

- `bfa2c56` — Phase 2: TRIH 1–300 (181 resource entries)
- `e72f2a2` — Phase 4: resource timeline rendering + subject-driven placement + ResourcesPopup
- `5f80b53` — Phase 3: popular history books (254 entries, NF teal / fiction purple)

Plus today's batch (uncommitted on disk at session end — see git status):
- Popup tag chips + resource_link rendering
- Phase 5 authoring helper
- CLAUDE.md updates

---

## Hosted Supabase migrations applied

- 001-009: original schema work
- 010: `user_favourites` (favourites)
- 011: resources scaffolding (`resource_link`, `resource_episodes`, `is_resource_timeline`, `resource_tags` table, type-mixing trigger)
- 012: widened `occurrence_type` CHECK to include `'resource'`
- 013: `resource_subtype` text column

All migrations live in `supabase/migrations/`. The convention is to paste the SQL into the Supabase dashboard's SQL editor.

---

## Known issues / gotchas to remember

- **Hosted Supabase statement timeout (~8s)** can interrupt the importer's `rebuild_zoom_out_ids()` step, causing the subsequent `resource_tags` write to be skipped. Recovery: `python -m v2.curation.import_resource_tags_only`.
- **PostgREST schema cache** can take 1-2 minutes to pick up new columns after a migration — wait and retry.
- **Resource colour palette**: `subtype: "book-fiction"` → purple, anything else → teal. Lives in `src/lib/occurrenceColor.ts`.
- **Skipped TRIH episodes**: 68 of 249 grouped items were too thematic to date (Greatness, Lessons of History, Top Ten lists, etc.). They're listed in `tools/v2/data/_research/generate_trih_module.py` output. These are skipped intentionally; the new session can re-evaluate using archive API data.

---

## How to use this handover

When you start the new session, paste this whole file into the chat as your first message, prefaced with:

> "Continuing the Ever-When project — please read this handover and then start with [your specific request, e.g. 'fetch the remaining TRIH episodes and improve the existing 181 tags']."

The CLAUDE.md in the project root has the canonical instructions; this handover just summarises the in-flight context.
