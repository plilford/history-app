# History timelines app — project notes for Claude

A historical-timeline web app + Android wrapper. Built by Peter (p.lilford@gmail.com).
He's the sole developer + sole editor.

## Stack (locked)

- Frontend: React + TypeScript + Vite, packaged as a PWA.
- Backend: Supabase (Postgres + REST + Auth + Realtime). **Local Supabase via Docker** during development; hosted Supabase is the next step.
- Android: PWA → Trusted Web Activity (TWA) via Bubblewrap.

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

This migration was just written and is the cleanup pass BEFORE moving to hosted. **It has not been applied yet on hosted.** Order matters; the migration runs in a single transaction.

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

- **Priority scale: 0–1,000,000 integers.** 800k is a soft floor; new entries can break it. Each slug is internally ranked 800k–1M; `master` is the global-notability slug.
- **Region weights are multipliers, not tie-breakers.** `effective = base * sum(slider*weight)/sum(slider) / 5`. Applied to `master` and `arts-and-thoughts` only.
- **Default timelines on app load:** Master, Arts and Thoughts, England: Monarchs.
- **Two-level rollup zoom:** <80yr → leaf events; 80–800yr → collapse to `first_zoom_out`; ≥800yr → collapse to `second_zoom_out` (else first). Umbrellas are first-class rows.
- **Date precision:** Year-only / month-only / day precision all supported. Renderer flexes box position within the unknown window so year-only entries don't all stack on 1 Jan.
- **Ongoing periods:** `is_ongoing=true` + null end_year. Frontend's `normalizeOngoing()` substitutes current year at fetch time so placement code can treat them as ordinary periods.
- **IDs ≥ 1_000_000.** v1 spreadsheet IDs were < 1M; this guard is kept even though v1 is dropped.

## Authoring new occurrences

The data lives in `tools/v2/data/master.py` as a single `OCCURRENCES = [...]` list of dicts. `python -m v2.import_v2` reads it, upserts into `occurrences`, and replaces `occurrence_timeline_priorities` for those IDs. Current size: **3,488 entries**, max ID **1_005_560** (the "Napoleonic Wars" umbrella row). New IDs should start at `1_005_561` and be contiguous within a batch.

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

- **Per-slug priority is internally ranked, not absolute.** Each slug occupies the range 800k–1M; ordering within the slug reflects within-slug importance. `master` is the only slug that reflects global notability.
- New entries on `master` default to **900_000**. Bump to 920k–965k for things that obviously dominate their era; 970k+ for the truly universal markers (printing press, French Revolution, WW2, moon landing).
- For other slugs, pick a value that places the entry in roughly the right spot relative to existing entries on that slug. Don't sweat exact rankings — re-curation is easy later.
- 800k is a soft floor; pushing slightly below is fine for less-prominent inclusions.

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

For 50–1000 entries — write a Python script that constructs the dicts (loops, lookup tables, etc.), then either appends to master.py via the existing `serialize(occs)` helper in `outputs/backfill_dates_session1.py`, or prints the dicts to stdout for you to paste in. Doing one big append in a single edit is cleaner than many small ones.

Either way, before importing:

```
cd tools
python -m v2.validate     # exits non-zero on any error; warnings (e.g. dangling umbrella refs) are non-fatal
python -m v2.import_v2    # idempotent; safe to re-run
```

`main_category` and `main_priority` are recomputed by trigger after each priority change, so don't touch those columns directly.

## Deploy punch list

In rough order. Everything builds on what comes before:

1. **Apply migration 009 to hosted Supabase.**
   - Create the hosted project at supabase.com.
   - Paste `supabase/migrations/001…009_pre_hosted_cleanup.sql` into the SQL editor in order — 009 is wrapped in `begin/commit` so it's atomic on its own. Earlier migrations should be applied via `supabase db push` if you wire up the CLI, or pasted one-by-one.
   - Confirm `pg_trgm` extension enabled, RLS policies exist on `occurrences` / `occurrence_timeline_priorities` / `timelines`, and the `rebuild_zoom_out_ids()` function exists.

2. **Update `.env` with hosted credentials.**
   - `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` for the importer (keep these out of git — they should already be in `.gitignore`).
   - `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` for the frontend.
   - Don't commit either.

3. **Run the importer against hosted.**
   - `cd tools && python -m v2.validate` first — exits non-zero on any data error.
   - Then `python -m v2.import_v2`. Idempotent; safe to re-run.
   - Verify in the Supabase dashboard: `select count(*) from occurrences` should be ~3,489.

4. **Confirm the editor allowlist.**
   - `editor_emails()` in 001_init_schema.sql hard-codes `p.lilford@gmail.com`. Sign up via Supabase Auth with that address before testing edits.

5. **Pick a host for the PWA.** Cloudflare Pages, Vercel, or Netlify all work. Add the two `VITE_*` env vars to the host's settings. Point at the repo root, build command `npm run build`, output `dist/`.

6. **Bubblewrap TWA for Android.** Once the PWA is live at a stable URL, `bubblewrap init --manifest=<url>/manifest.webmanifest`, then `bubblewrap build`. Publishing to Play Store needs the Asset Links file on the same domain so Android trusts the TWA.

## Gotchas worth remembering

- **`main_priority` and `main_category` are trigger-maintained.** Writing to them directly is fine in the importer but will get overwritten on the next priority change. The importer does its work via `occurrence_timeline_priorities` and lets the trigger do the rest.
- **Umbrella references (`first_zoom_out` / `second_zoom_out`) are matched by title string** in master.py. `validate.py` flags any reference that doesn't resolve. After bulk upsert, the importer calls `rebuild_zoom_out_ids()` RPC to populate the FK columns.
- **`master.py` still has ~50 entries with `end_year=2026`.** The importer auto-translates these to `is_ongoing=true`. A future cleanup pass can rewrite master.py to use `is_ongoing: True` natively, but it's not blocking.
- **vite-env.d.ts** at `src/vite-env.d.ts` is a single `/// <reference types="vite/client" />` line. Without it, `import.meta.env` doesn't typecheck.

## How to read more

Full session-by-session history (build of v2 dataset, placement algorithm changes, date backfills, the +1000-row data session, schema cleanup) lives in the Cowork memory at the user's local-agent-mode sessions folder. Most of it is data-build chronology that you won't need unless something in `master.py` looks weird.
