# History timelines app — project notes for Claude

A historical-timeline web app + Android wrapper. Built by Peter (p.lilford@gmail.com).
He's the sole developer + sole editor.

## Stack (locked)

- Frontend: React + TypeScript + Vite, packaged as a PWA. **Deployed at https://ever-when.com via Cloudflare Pages** (auto-deploys from GitHub `main`).
- Backend: Supabase Postgres + REST + Auth + Realtime. **Production runs on hosted Supabase**; a local Supabase via Docker may still exist as a dev sandbox but the live app and the data importer talk to hosted.
- Android: PWA → Trusted Web Activity (TWA) via Bubblewrap, packaged as `com.everwhen.app`. Asset-links file is served from the same domain so Android trusts the TWA.

## Where things are

- `src/` — React app. Entry is `src/App.tsx` (~1900 lines, single-file by design).
- `src/types/database.ts` — canonical Postgres row types. **`Occurrence` / `OccurrenceWithPriority`** are the new names; `HistoryEvent` / `EventWithPriority` are kept as type aliases so the rest of the code didn't need a sweeping rename.
- `src/lib/yearScale.ts` — log-compressed year ↔ pixel mapping. Handles billion-year ranges.
- `src/lib/dateFormat.ts` — adaptive date formatting + `normalizeOngoing<T>()` helper.
- `src/components/{EventPopup,SearchBar,TimelinePicker}.tsx`.
- `supabase/migrations/` — numbered SQL files, run in order via `supabase db reset` or pasted into the SQL editor.
- `tools/v2/import_v2.py` — bulk data importer; reads `tools/v2/data/master.py`.
- `tools/v2/validate.py` — static validation pass over `master.py`. Run before each import: `python -m v2.validate`.

## Schema as of migration 009 (`009_pre_hosted_cleanup.sql`)

This is the cleanup pass that landed alongside the move to hosted Supabase. **Applied in production.** Order matters; the migration runs in a single transaction.

Tables:

- `occurrences` (renamed from `events`) — every row is one historical occurrence: an event, a person's lifespan, or a work of art.
  - `title text not null` — single canonical title (replaced `event_short` / `display_name` / `person`).
  - `occurrence_type` is `{event, person, art}`. Period vs point is a flag (`is_period`), not a type. Person-lifespan vs person-event is the `is_full_life` flag.
  - `is_ongoing boolean` — replaces the legacy `end_year = 2026` placeholder.
  - `first_zoom_out` / `second_zoom_out` text + `first_zoom_out_id` / `second_zoom_out_id` FK columns. The text is the authoring interface in `master.py`; the FK is populated by a DB trigger + `rebuild_zoom_out_ids()` RPC.
  - `main_category` + `main_priority` are auto-maintained by trigger from `occurrence_timeline_priorities`. Never write directly.
- `occurrence_timeline_priorities` (renamed from `event_timeline_priorities`).
  - `occurrence_id` (renamed from `event_id`), `timeline_id`, `priority integer >= 0`.
- `timelines` — global unique (name, slug). No `dataset` column anymore (v1 dropped).

RLS:

- Reads are public.
- Writes require `auth.jwt() -> 'email'` to be in `editor_emails()`. Currently just `p.lilford@gmail.com`.

## Locked conventions

- **Priority scale: 0–1,000,000 integers.** No floor — calibrate new entries against existing entries on the same slug. `master` is the global-notability slug; other slugs are internally ranked by within-slug importance, which is *not* the same as global importance (e.g. Magna Carta is huge on `england` but Hamilton's tariff is high on `usa` despite being globally minor). Re-curation is easy and expected.
- **Region weights are multipliers, not tie-breakers.** `effective = base * sum(slider*weight)/sum(slider) / 5`. Applied to `master` and `arts-and-thoughts` only.
- **Default timelines on app load:** Master, Arts and Thoughts, England: Monarchs.
- **Two-level rollup zoom:** <80yr → leaf events; 80–800yr → collapse to `first_zoom_out`; ≥800yr → collapse to `second_zoom_out` (else first). Umbrellas are first-class rows. Search-pick auto-zooms to the entry's natural rollup level and exempts the flashed entry from substitution/hiding (see `handlePickOccurrence` in App.tsx).
- **Date precision:** Year-only / month-only / day precision all supported. Renderer flexes box position within the unknown window so year-only entries don't all stack on 1 Jan.
- **Ongoing periods:** `is_ongoing=true` + null end_year. Frontend's `normalizeOngoing()` substitutes current year at fetch time so placement code can treat them as ordinary periods.
- **IDs ≥ 1_000_000.** v1 spreadsheet IDs were < 1M; this guard is kept even though v1 is dropped.

## Authoring new occurrences

The data lives in `tools/v2/data/master.py` as a single `OCCURRENCES = [...]` list of dicts. `python -m v2.import_v2` reads it, upserts into `occurrences`, and replaces `occurrence_timeline_priorities` for those IDs. Current size: **~3,902 entries**, max ID around **1_006_119**. New IDs should continue from there, contiguous within a batch. (Run `python -c "from v2.data.master import OCCURRENCES; print(max(o['id'] for o in OCCURRENCES))"` to get the precise current max.)

### Entry shape

Compact 5-line dict format — match the existing style; don't reformat the file:

```python
{"id": 1_005_560, "type": "event", "title": "Berlin Wall falls",
 "start_year": 1989, "start_month": 11, "start_day": 9,
 "description": "East Germany opens border crossings; symbolic end of the Iron Curtain.",
 "wikipedia": "https://en.wikipedia.org/wiki/Fall_of_the_Berlin_Wall",
 "priorities": {"master": 970_000, "cold-war": 990_000}},
```

Keys are double-quoted; values use whatever quoting reads naturally. IDs use underscore separators (`1_005_560`); years, months, days, priorities are bare ints (`1989`, `970_000`).

### ID conventions

- Sequential, contiguous within a batch. Don't leave gaps inside a session unless deliberately reserving for related entries.
- Always `>= 1_000_000`. `validate.py` enforces this.
- Author IDs by hand; the importer uses `on_conflict="id"`, so re-running with the same ID updates the row.

### Title conventions

- Globally unique, case-insensitive after trim. `validate.py` flags duplicates.
- For point-events that are really moments inside a longer period, prefer the framing "**\<Person\> begins/launches/opens \<Thing\>**" and keep the entry as a point (start_year only). E.g. "Gandhi begins the Salt March" on 12 Mar 1930, NOT a period.
- For real periods (wars, reigns, dynasties), use a noun-phrase title and supply both start and end dates. E.g. "World War II", 1 Sep 1939 → 2 Sep 1945.
- Don't reformat existing titles unless asked. Existing entries' framing is intentional.

### Priority conventions

- **Per-slug priority is internally ranked, not absolute.** Use the full 0–1,000,000 range. `master` reflects global notability; other slugs reflect within-slug importance ("how essential is this to telling THIS timeline's story?").
- **Calibrate against existing entries on the same slug.** Before picking a number, scan a few neighbour entries in master.py (or query Supabase). Match the granularity you see there.
- Rough master-slug calibration (existing distribution: min ~600k, median ~900k, max 1M):
  - **990k+**: civilizational hinges (Big Bang, French Revolution, fall of Constantinople, Luther's 95 Theses).
  - **950–989k**: major events most educated people know (Battle of Hastings, Treaty of Versailles, moon landing).
  - **900–949k**: significant turning points (Battle of Marathon, dissolution of monasteries, Battle of Sedan).
  - **800–899k**: important but not universally known (Solon's reforms, Bismarck's social insurance, Peasants' Revolt).
  - **700–799k**: notable specific events (individual battles, treaties, local reforms).
  - **600–699k**: regional/niche importance only.
  - **<600k**: minor curiosities.
- Per-slug priority is typically `master + 30k` for entries firmly anchored to that slug (`Magna Carta` on `england`, `Hagia Sophia` on `roman-history`) and `master - 90k` when the entry is multi-regional and the slug isn't the primary lens (`D-Day` on `england`, `Hannibal's Hydaspes` on `ancient-greece`). See `tools/v2/curation/recurate_england_roman.py` for the rule applied at scale.
- Don't sweat exact rankings — re-curation is easy and there are scripts in `tools/v2/curation/` that redistribute priorities automatically.

### Region weights (1–10, default 5)

Five columns: `europe`, `americas`, `asia`, `australasia`, `africa`. They modulate ranking on `master` and `arts-and-thoughts` views; everywhere else they're ignored.

- Truly global events: leave all at 5 (omit `region_weights` entirely).
- Region-anchored events: bias toward the relevant region(s). E.g. a US presidency might be `{"americas": 9, "europe": 4}`; a French Revolution detail entry `{"europe": 9, "americas": 4}`; a Chinese dynasty `{"asia": 9, "europe": 4}`.
- Treat the values as "how much would someone in that region care about this", not "where it happened" — events with global influence get high marks across multiple regions.

### Type / lifespan conventions

- `type: "event"` (default) — events, periods, wars, dynasties, treaties.
- `type: "person"` — a person's full lifespan only. Birth-year → death-year. **Always pair with `is_full_life: True`.**
- `type: "art"` — discrete works (paintings, films, novels, symphonies). Point events; use the year of completion/publication.
- Person-events (publications, accessions, decisions made by a person) are `type: "event"`, NOT `type: "person"`.
- Bands and ensembles (The Beatles, Rolling Stones) are modelled as `type: "person"` WITHOUT `is_full_life=True` — they should keep rendering when the Lifespans toggle is off.
- **Invariant:** every `is_full_life=True` person needs at least one related `type: "event"` or `type: "art"` entry inside their lifespan, name-matching their title or description. The search bar's lifespan fallback relies on this.

### Date precision

- Pre-1500 entries: year-only is fine, that's all we usually have. Set `date_uncertain: True` for genuinely fuzzy ancient dates ("circa 3000 BCE").
- Post-1500: aim for month/day precision wherever it's reliably known. Renderer adapts at zoom; the precision-driven flex stops year-only entries from stacking on 1 Jan.
- Ongoing periods (reigns, presidencies, dynasties currently active): set `is_ongoing: True` and omit end_year. The importer also accepts the legacy `end_year: 2026` form and translates it.
- Use `display_date` to override the auto-generated label only when the auto version is misleading (BCE "circa" dates, deep-time geological events, etc.).

### Slug conventions

- Every entry should include `master` in its `priorities` dict.
- Add additional slugs based on the entry's actual relevance. Don't pile entries onto a slug just because they're loosely related.
- New slug needed? Add it to `TIMELINES` in `tools/v2/import_v2.py` BEFORE referencing it in master.py, otherwise the importer prints a warning and skips the priority row. `validate.py` flags unknown slugs.

### Umbrella references (rollup zoom)

If a new entry belongs to a broader period that exists as its own row, point to that row's title:

```python
"first_zoom_out": "World War II",
"second_zoom_out": "Twentieth century wars",   # optional
```

Match the umbrella's title exactly (case-insensitive trim). `validate.py` flags any reference that doesn't resolve. The importer calls `rebuild_zoom_out_ids()` after upsert to populate the FK columns.

### Authoring workflow

For 1–30 entries — edit `master.py` directly, append to the end of `OCCURRENCES`. Read the last ~30 entries first to anchor on the recent style and pick the next free ID.

For 50–1000 entries — write a Python script that constructs the dicts (loops, lookup tables, etc.) and appends to master.py. Use `tools/v2/curation/append_entries.py` — it has a `format_entry()` + `append_entries(entries)` helper that emits the canonical 5-line dict style and appends just before the closing `]` of the OCCURRENCES list. The recent `phase_d_*.py` and `phase_c*.py` scripts in `tools/v2/curation/` are working examples. Doing one big append in a single script run is cleaner than many small ones, and the importer's `on_conflict="id"` makes re-runs safe.

For de-duplication: `validate.py` flags case-insensitive title collisions. When a new batch collides with an existing entry, decide which to keep (mine is usually richer; old is usually the master-priority baseline). `tools/v2/curation/purge_duplicates.py` is the pattern: delete one ID, bump the other's master priority to preserve historical ranking. `tools/v2/curation/purge_c6_dupes.py` auto-generates the (delete_id, keep_id, new_master_pri) tuples from validate's error output, which is far faster than transcribing them by hand.

Either way, before importing:

```
cd tools
python -m v2.validate     # exits non-zero on any error; warnings (e.g. dangling umbrella refs) are non-fatal
python -m v2.import_v2    # idempotent; safe to re-run
```

`main_category` and `main_priority` are recomputed by trigger after each priority change, so don't touch those columns directly.

## Production setup

What's actually wired up:

- **Hosted Supabase project.** Migrations 001–009 applied. `pg_trgm` extension, RLS policies on `occurrences` / `occurrence_timeline_priorities` / `timelines`, and the `rebuild_zoom_out_ids()` RPC are all in place.
- **`.env` files** (gitignored) hold hosted credentials:
  - `tools/.env` — `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` for the importer.
  - Project root `.env` — `VITE_SUPABASE_URL` + `VITE_SUPABASE_ANON_KEY` for the frontend dev build. Cloudflare Pages has the same two vars set in its build settings.
- **Editor allowlist** at `editor_emails()` in `001_init_schema.sql` permits only `p.lilford@gmail.com` to write. Production Supabase Auth is wired to this email.
- **Cloudflare Pages** serves https://ever-when.com from the `main` branch. Build command `npm run build`, output `dist/`. Auto-deploys on push.
- **Bubblewrap TWA** packages the PWA as `com.everwhen.app` for Android. Asset-links file is at `/.well-known/assetlinks.json` (served via `public/_redirects` because dotfiles don't ship in `dist/` by default).

### Deploying changes

**Code changes (frontend):**
1. Edit `src/*` — the change does NOT reach ever-when.com or the Android app until it's committed and pushed.
2. `git add` → `git commit` → `git push origin main`.
3. Cloudflare Pages builds and deploys in ~1–2 minutes. The PWA service worker has `autoUpdate` + `clientsClaim` + `skipWaiting`, so installed PWA / TWA users pick up the new bundle on next launch.

**Data changes (occurrences, priorities, timelines):**
1. Edit `tools/v2/data/master.py` (directly or via a script in `tools/v2/curation/`).
2. `cd tools && python -m v2.validate` — fail-fast check; exits non-zero on any error.
3. `python -m v2.import_v2` — upserts to hosted Supabase. Idempotent. The hosted DB picks up changes immediately; the frontend reads on each load.

**Schema migrations:**
1. Add a new `supabase/migrations/NNN_*.sql` file.
2. Apply via the Supabase SQL editor (paste contents) or `supabase db push` if you've wired up the CLI.
3. master.py + import_v2.py may need follow-up edits if the migration changes table shape.

## Gotchas worth remembering

- **`main_priority` and `main_category` are trigger-maintained.** Writing to them directly is fine in the importer but will get overwritten on the next priority change. The importer does its work via `occurrence_timeline_priorities` and lets the trigger do the rest.
- **Umbrella references (`first_zoom_out` / `second_zoom_out`) are matched by title string** in master.py. `validate.py` flags any reference that doesn't resolve. After bulk upsert, the importer calls `rebuild_zoom_out_ids()` RPC to populate the FK columns.
- **`master.py` still has ~50 entries with `end_year=2026`.** The importer auto-translates these to `is_ongoing=true`. A future cleanup pass can rewrite master.py to use `is_ongoing: True` natively, but it's not blocking.
- **vite-env.d.ts** at `src/vite-env.d.ts` is a single `/// <reference types="vite/client" />` line. Without it, `import.meta.env` doesn't typecheck.
- **Frontend changes don't reach ever-when.com until pushed.** Editing `src/*` only updates local dev (`npm run dev`). The live site is whatever last built from `main` on Cloudflare Pages. If a fix "isn't working", check `git status` first.
- **Search-pick zoom behaviour** (in `handlePickOccurrence`): clicking a search result auto-zooms to the entry's natural rollup level and force-shows it (exempts from rollup substitution + pins to front of placement queue). This is the only place where the renderer treats one entry preferentially; the override is scoped to the 2.2s flash window.

## How to read more

Full session-by-session history (build of v2 dataset, placement algorithm changes, date backfills, the +1000-row data session, schema cleanup) lives in the Cowork memory at the user's local-agent-mode sessions folder. Most of it is data-build chronology that you won't need unless something in `master.py` looks weird.
