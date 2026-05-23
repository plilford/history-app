# History Timelines

Website + Android app for exploring historical timelines side by side. One Postgres database (Supabase), one React/TypeScript frontend that ships as a PWA on web and as a wrapped Android app.

## Status

v0 scaffolding. Database schema, importer, and a minimal "is the data round-tripping" UI. Real zoom, multi-column layout, editing UI, and deep-time view come next.

## What you need installed

- **Docker Desktop** — runs the local Supabase stack. https://www.docker.com/products/docker-desktop/
- **Supabase CLI** — https://supabase.com/docs/guides/cli/getting-started (on Windows, `scoop install supabase` or download from the release page)
- **Node.js 18+** and npm
- **Python 3.10+** (for the spreadsheet importer)

You do **not** need a Supabase cloud account for local development.

## One-time setup (fully local)

### 1. Start the local Supabase stack

From inside `app/`:

```bash
supabase init        # only the first time — creates supabase/config.toml
supabase start       # boots Postgres, auth, API, Studio in Docker
```

When it finishes, it prints something like:

```
API URL:    http://127.0.0.1:54321
Studio URL: http://127.0.0.1:54323
anon key:   eyJhbGciOi...
service_role key: eyJhbGciOi...
```

Keep that terminal output handy — you'll paste those keys in the next step.

The migration in `supabase/migrations/001_init_schema.sql` is auto-applied on `supabase start`. To re-apply after editing it: `supabase db reset`.

### 2. Configure environment

```bash
cd app
cp .env.example .env
# open .env and paste the anon key + service_role key from step 1
```

### 3. Import the spreadsheet

```bash
cd app/tools
python -m venv .venv
source .venv/bin/activate         # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python import_spreadsheet.py "../../timeline database KA.xlsm"
```

This reads the `events and periods` tab, populates the three tables, and lets the database trigger compute `main_category` for every event.

Dry run (parse only, no writes):
```bash
python import_spreadsheet.py "../../timeline database KA.xlsm" --dry-run
```

### 4. Run the frontend

```bash
cd app
npm install
npm run dev
```

Open http://localhost:5173. You should see three columns: **Worldwide: main**, **Arts and thoughts: main**, **UK: main**, each with the top-priority events from 1500-2025.

To browse / edit the data directly: open the local **Supabase Studio** at the Studio URL printed by `supabase start` (usually http://127.0.0.1:54323).

## Going online (later)

When you want to publish:

1. Create a project at https://supabase.com.
2. `supabase link --project-ref <your-project-ref>` then `supabase db push` to apply the same migration to the cloud DB.
3. Re-run the importer with the cloud URL + service key.
4. Swap the four values in `.env` to the cloud URL + cloud keys.
5. `npm run build` and host the `dist/` folder anywhere static (Netlify, Vercel, Cloudflare Pages — all free).

Nothing in the code or schema changes between local and cloud.

## Project layout

```
app/
├── src/                       # React + TS frontend
│   ├── App.tsx                # entry component
│   ├── lib/supabase.ts        # Supabase client
│   └── types/database.ts      # TS types mirroring the schema
├── supabase/migrations/       # SQL migrations
│   └── 001_init_schema.sql    # tables, trigger, RLS
├── tools/
│   ├── import_spreadsheet.py  # one-shot importer
│   └── requirements.txt
├── .env.example
├── package.json
└── README.md (this file)
```

## Schema highlights

- `events.main_category` is **computed** by trigger from `event_timeline_priorities`. Never write to it directly.
- `event_timeline_priorities` is the junction table: one row per (event, timeline) where the priority is > 0.
- Row-level security: anonymous reads allowed, writes restricted to emails in the `editor_emails()` function. Edit that function to add/remove editors.

## Next steps (not done yet)

- Zoom mechanic (priority threshold derived from years-per-pixel)
- Deep-time view (pre-5,000 BCE)
- Edit-event UI behind Supabase auth
- Timeline picker (which subset of the 61 timelines to show)
- Bubblewrap TWA wrapper for Android
