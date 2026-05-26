---
name: monthly-update
description: Monthly database refresh for the Ever-When timeline app. Run when the user asks to "update the database", "do the monthly check", "refresh data", or anything similar. Pulls new podcast episodes, surfaces stale ongoing entries (popes/leaders who have died, wars that ended), and walks the user through curation decisions.
user-invocable: true
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash(.venv/Scripts/python.exe *)
  - Bash(./.venv/Scripts/python.exe *)
  - Bash(cd tools && .venv/Scripts/python.exe *)
  - Bash(git *)
  - Bash(npm run *)
  - Grep
  - Glob
---

# /monthly-update — Ever-When monthly database refresh

This skill orchestrates the recurring maintenance pass on the Ever-When
historical-timeline dataset. The user runs it roughly monthly. Your job is
to walk them through the findings, get their decisions on judgement calls,
and apply changes safely.

## Steps in order

### 1. Run the report

From the project root, generate the freshness report:

```
cd tools && .venv/Scripts/python.exe -m v2.curation.monthly_update
```

This:
- Re-pulls RSS feeds for every podcast registered in `EPISODIC_RESOURCES`
  (currently just The Rest Is History) and counts new episodes since the
  last update.
- Lists `is_ongoing=True` entries needing a "still going?" check.
- Lists living persons (`type=person`, `is_full_life=True`, no end_year).
- Flags "suspicious living" entries — people born >110 years ago with no
  death year (almost always missing data, not real centenarians).
- Reports days since the last hosted-Supabase write.

Read the output. Summarise it back to the user as a short list of action
items — don't make them re-read the raw report.

### 2. Handle each finding type

For each section, follow the rules below. Always **confirm with the user**
before writing — never silently add or modify entries.

#### 2a. New podcast episodes

If `monthly_update.py` shows `+N new` for an episodic resource, ask the
user whether to refresh that podcast now. If yes:

```
cd tools
.venv/Scripts/python.exe -m v2.data._research.parse_trih_rss
.venv/Scripts/python.exe -m v2.data._research.fetch_trih_archive
.venv/Scripts/python.exe -m v2.data._research.curate_trih_v2
.venv/Scripts/python.exe -m v2.data._research.generate_trih_module_v2
.venv/Scripts/python.exe -m v2.validate
.venv/Scripts/python.exe -m v2.import_v2
# If import_v2 hits the rebuild_zoom_out_ids timeout (it usually does):
.venv/Scripts/python.exe -m v2.curation.import_resource_tags_only
.venv/Scripts/python.exe -m v2.curation.monthly_update --mark-imported
```

(Substitute the equivalent pipeline steps for other podcasts when they're
added — the registry in `monthly_update.py::EPISODIC_RESOURCES` lists each
resource's full pipeline.)

**CRITICAL — Series bundling**: This is the most common failure mode when
adding new episodes incrementally over time.

A "series" is a set of consecutive episodes the podcast publishes under a
shared theme — typically titled `"X (Part 1)"`, `"X (Part 2)"`, etc. The
existing curator (`curate_trih_v2.py`) groups these automatically by
detecting a `Part N` suffix on consecutive numbered episodes: when it
sees a `Part 1` it starts a fresh group; subsequent parts join until a
new `Part 1` or a non-part standalone episode appears.

This works perfectly for a series imported in one batch — all parts are
already in the RSS feed when we first see them, so they bundle into a
single `resource_episodes: [...]` payload under one occurrence id.

**The pitfall**: a series sometimes lands across two monthly runs.
Episodes 1-3 ship in week 4 of one month, episodes 4-6 in week 1 of the
next. On the first run we bundle 1-3 into a single occurrence with a
multi-episode `resource_episodes` list. On the next run the curator sees
all 6 episodes, regroups, and emits a single 6-episode bundle. Because
the generator assigns ids by `START_ID + index` in chronological order
within the curated draft, the regrouped bundle gets WHATEVER id falls at
that position — which may NOT be the same id the old 3-episode bundle
had. That breaks `resource_tags` rows pointing at the old id, and
duplicates can sneak in.

**Detection**: after re-running the pipeline, before importing, inspect
the diff on the data module:

```
git diff tools/v2/data/the_rest_is_history.py | head -100
```

Look for:
- An old multi-part bundle (e.g. `"Foo: bar (TRIH eps 600-602)"`) being
  REPLACED with an extended bundle (`"Foo: bar (TRIH eps 600-605)"`) — that's
  the GOOD case, do this.
- An old multi-part bundle being SHORTENED (`600-602` → `600-601`) because
  the curator chose differently — investigate before applying.
- DUPLICATE bundles at adjacent ids covering overlapping episode numbers
  — that's the BAD case. Stop, investigate the curator's grouping logic.

If you see the bad case, the fix is usually to add an explicit override in
`tools/v2/data/_research/manual_curations.py` keyed by the first ep_num of
the series — same OVERRIDES dict the curator already consults. Set the
override's `title` field so both runs produce identical resource_titles.

**One-off bonus episodes** (interviews, livestreams, "what-if" specials):
these don't have a `Part N` suffix and become standalone occurrences. That's
correct — they're not really a series.

**When the user adds a NEW podcast** they want monitored, ask them to:
1. Drop a new module under `tools/v2/data/_research/` with a parser +
   fetcher + curator + generator following the TRIH pattern.
2. Add a new entry to `EPISODIC_RESOURCES` in `monthly_update.py`
   pointing at those scripts. Include the id range (reserve a fresh
   1_010_xxx block).
3. Run the monthly script — the new entry will be picked up next time.

#### 2b. `is_ongoing` entries

These are reigns, conflicts, dynasties, or pontificates currently marked
as still active. For each one in the report, ask the user: has X actually
ended?

If YES (e.g. Pope Francis died April 2025):
1. Locate the entry in `master.py`.
2. Set `end_year`, `end_month`, `end_day` to the closure date.
3. Remove `is_ongoing: True` (or set to `False` — either way the importer
   handles it).
4. If the entry corresponds to a person (e.g. a Pope's pontificate is
   represented as an event on the Pope's life), also update the
   corresponding `type=person, is_full_life=True` row with their death date.

Then re-run `v2.validate` and `v2.import_v2` (recovery via
`import_resource_tags_only` if the RPC times out — pre-existing gotcha).

Example fix for a Papal-style entry:

```python
# Before:
{"id": 1006909, "type": "person", "title": "Pope Francis",
 "start_year": 1936, "start_month": 12, "start_day": 17,
 "is_full_life": True, "is_ongoing": True,
 ...},

# After:
{"id": 1006909, "type": "person", "title": "Pope Francis",
 "start_year": 1936, "start_month": 12, "start_day": 17,
 "end_year": 2025, "end_month": 4, "end_day": 21,
 "is_full_life": True,
 ...},
```

#### 2c. Living persons

Each is a `type=person, is_full_life=True` row with no end_year. For each
one ask the user: is X still alive? If they died:
1. Set `end_year`/`end_month`/`end_day`.
2. (No is_ongoing toggle needed — these aren't marked is_ongoing.)

Often you'll know the answer (e.g. someone famous who died recently).
When unsure, hand it back to the user — don't guess.

#### 2d. Suspicious "living" entries

Person rows missing end_year despite being born >110 years ago. Always a
data-quality gap, never genuinely still living. Look up the death year
on Wikipedia and add it. These don't need user judgement — just fix them
and tell the user what you did.

### 3. Editorial additions

The script doesn't auto-detect "new events that have happened" or "old
events that have risen in prominence" — these are editorial calls.

After the mechanical updates above, ask the user:

> Anything from the news this past month that should be added? Major
> deaths, wars starting / ending, elections, treaties, awards (Nobel,
> Booker), notable releases (films, books that became cultural touchstones)?
> Any existing entries you'd like to re-prioritise?

If they have items, batch them into a curation script under
`tools/v2/curation/add_round_<letter>.py` following the round-K pattern.
Always run `v2.validate` + `v2.curation.audit_and_fix_slugs --apply` +
`v2.import_v2` after each batch.

### 4. Update the state file

Once everything has imported successfully:

```
cd tools && .venv/Scripts/python.exe -m v2.curation.monthly_update --mark-imported
```

This bumps the last-seen episode counts so next month's delta is accurate.

### 5. Commit

Bundle the month's changes into ONE commit per logical unit (one for new
podcast episodes, one for editorial additions, one for ongoing-entry
closures). Use the existing commit-message style (sentence headline, then
body explaining what + why; close with the `Co-Authored-By` line).

Push when the user confirms.

---

## State file

Lives at `tools/v2/curation/monthly_update_state.json` and is committed
to git so it tracks across machines. Tiny — just per-resource episode
counts plus the last-checked timestamp.

## Failure modes worth flagging

- **`rebuild_zoom_out_ids` timeout** during `v2.import_v2` is a known gotcha
  (documented in CLAUDE.md). The data upsert succeeds, but the trigger that
  populates `first_zoom_out_id` FKs times out, and the subsequent
  `resource_tags` step is skipped. Always follow up with
  `v2.curation.import_resource_tags_only`.

- **PostgREST schema cache lag**: if the user has just applied a migration,
  PostgREST takes 1-2 minutes to see new columns. If the import errors with
  "column not found", wait + retry.

- **Hosted Supabase being slow**: imports normally take 30-60s; if a step
  hangs >2min, bail and tell the user. The importer is idempotent — safe to
  retry on next run.
