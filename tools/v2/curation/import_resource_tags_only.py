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

from v2.import_v2 import (
    collect_all_occurrences,
    chunked,
    _select_top_resources_per_subject,
)


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
    print(f"Parsed {len(pending_tags)} authorial tag pairs across "
          f"{len({rid for rid, _ in pending_tags})} resources")

    # Same top-N-per-family selection logic as the main importer — the
    # popup should never show every resource that mentioned the subject,
    # only the cream.
    unique = _select_top_resources_per_subject(pending_tags, title_to_id, occurrences)
    unresolved = [
        (rid, t) for rid, t in pending_tags
        if title_to_id.get(t.strip().lower()) is None
    ]
    if unresolved:
        print(f"  {len(unresolved)} unresolved tags")

    # Delete tags for EVERY resource with authorial tags (not just the ones
    # that ended up in the new selection) — otherwise a resource that was
    # previously selected but is now demoted leaves its old tag row behind.
    resource_ids_with_tags = sorted({rid for rid, _ in pending_tags})
    print(f"Clearing resource_tags for {len(resource_ids_with_tags)} resources "
          f"with authorial tags, inserting {len(unique)} rows after top-N "
          f"selection ...")
    for batch in chunked(resource_ids_with_tags, 200):
        sb.table("resource_tags").delete().in_("resource_id", batch).execute()
    for batch in chunked(unique, 500):
        sb.table("resource_tags").insert(batch).execute()

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
