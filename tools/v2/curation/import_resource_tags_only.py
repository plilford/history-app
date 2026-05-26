"""
Re-import resource_tags only (skip occurrence + priority upserts + zoom-out
rebuild). Useful when a previous import hit a statement-timeout on
rebuild_zoom_out_ids() and never reached the tags step.

Reads `tags: [title, ...]` from every entry in master + the resource data
modules, resolves titles → ids, replaces rows in resource_tags. Idempotent.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client, Client

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from v2.import_v2 import collect_all_occurrences, chunked


def main() -> int:
    load_dotenv(ROOT.parent / ".env")
    sb: Client = create_client(
        os.environ["SUPABASE_URL"],
        os.environ["SUPABASE_SERVICE_ROLE_KEY"],
    )

    occurrences = collect_all_occurrences()
    title_to_id = {(o["title"]).strip().lower(): o["id"] for o in occurrences if "title" in o}
    pending_tags: list[tuple[int, str]] = []
    for o in occurrences:
        for subject_title in (o.get("tags") or []):
            pending_tags.append((o["id"], subject_title))
    print(f"Parsed {len(pending_tags)} tag rows across {len({rid for rid, _ in pending_tags})} resources")

    tag_rows: list[dict] = []
    unresolved: list[tuple[int, str]] = []
    for resource_id, subject_title in pending_tags:
        sid = title_to_id.get(subject_title.strip().lower())
        if sid is None:
            unresolved.append((resource_id, subject_title))
            continue
        if sid == resource_id:
            continue
        tag_rows.append({"resource_id": resource_id, "subject_id": sid})

    if unresolved:
        print(f"  {len(unresolved)} unresolved tags")

    # Dedupe.
    seen: set[tuple[int, int]] = set()
    unique: list[dict] = []
    for r in tag_rows:
        k = (r["resource_id"], r["subject_id"])
        if k in seen:
            continue
        seen.add(k)
        unique.append(r)

    resource_ids = sorted({r["resource_id"] for r in unique})
    print(f"Replacing resource_tags for {len(resource_ids)} resources ({len(unique)} tag rows) ...")
    for batch in chunked(resource_ids, 200):
        sb.table("resource_tags").delete().in_("resource_id", batch).execute()
    for batch in chunked(unique, 500):
        sb.table("resource_tags").insert(batch).execute()

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
