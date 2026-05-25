"""
Snapshot the application data from hosted Supabase to a local JSON file.

Usage (from project root):
    cd tools
    .venv\\Scripts\\python -m backup_hosted          (Windows)
    .venv/bin/python -m backup_hosted                (macOS/Linux)

Reads SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY from project-root .env.
Writes backups/hosted_backup_<UTC_ISO>.json next to the project root.

Captures every row of the three application tables:
    timelines
    occurrences
    occurrence_timeline_priorities

This is a DATA-ONLY backup. Schema, RLS policies, triggers, and functions
are NOT included — they live in supabase/migrations/. If you need a true
pg_dump (schema + data), use the Supabase CLI instead:

    supabase link --project-ref <ref>   (one-time; prompts for DB password)
    supabase db dump --linked -f backup.sql

Paginates in 1000-row pages (PostgREST's default cap).
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client, Client

PAGE_SIZE = 1000

# Tables to dump, in dependency order (parents before children) so re-importing
# from this file would not violate FK constraints.
TABLES = ["timelines", "occurrences", "occurrence_timeline_priorities"]


def dump_table(sb: Client, table: str) -> list[dict]:
    rows: list[dict] = []
    offset = 0
    while True:
        # range() is inclusive on both ends; PostgREST caps each page at the
        # server-side max (typically 1000), so request that explicit window.
        resp = (
            sb.table(table)
            .select("*")
            .range(offset, offset + PAGE_SIZE - 1)
            .execute()
        )
        page = resp.data or []
        rows.extend(page)
        if len(page) < PAGE_SIZE:
            break
        offset += PAGE_SIZE
        print(f"  {table}: {len(rows)} rows so far…")
    return rows


def main() -> None:
    here = Path(__file__).resolve().parent
    load_dotenv(here.parent / ".env")
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        sys.exit("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env")

    sb: Client = create_client(url, key)

    snapshot: dict = {
        "metadata": {
            "supabase_url": url,
            "taken_at_utc": datetime.now(timezone.utc).isoformat(),
            "tool": "tools/backup_hosted.py",
            "tables": TABLES,
        },
        "tables": {},
    }

    for table in TABLES:
        print(f"Dumping {table}…")
        rows = dump_table(sb, table)
        snapshot["tables"][table] = rows
        print(f"  {table}: {len(rows)} rows.")

    backups_dir = here.parent / "backups"
    backups_dir.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = backups_dir / f"hosted_backup_{ts}.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)

    total = sum(len(rows) for rows in snapshot["tables"].values())
    size_mb = out.stat().st_size / (1024 * 1024)
    print()
    print(f"Wrote {out}")
    print(f"  {total} rows total, {size_mb:.1f} MB on disk.")


if __name__ == "__main__":
    main()
