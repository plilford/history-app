"""
Delete occurrences that exist in hosted Supabase but no longer in master.py.

Run after dedupe_round_j.py + import_v2.py. The importer only upserts and
doesn't prune; this script reconciles the diff.

CASCADE on occurrence_timeline_priorities + user_favourites takes the
referenced rows with the parent.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def main() -> int:
    from v2.data.master import OCCURRENCES

    load_dotenv(ROOT.parent / ".env")
    sb = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"])

    local_ids = {o["id"] for o in OCCURRENCES}
    print(f"Local master.py: {len(local_ids)} occurrences")

    # Compute the round-J victim set from the .before_round_j backup. That
    # snapshot is master.py exactly as it stood before this dedup batch — the
    # diff against the current master.py is precisely round-J's deletions.
    backup = ROOT / "v2" / "data" / "master.py.before_round_j"
    if not backup.exists():
        print(f"ABORT: backup not found at {backup}")
        return 1
    # Parse the backup just enough to get IDs.
    import re
    backup_text = backup.read_text(encoding="utf-8")
    backup_ids = {
        int(m.group(1).replace("_", ""))
        for m in re.finditer(r'\{"id":\s*([\d_]+),', backup_text)
    }
    print(f"Backup master.py.before_round_j: {len(backup_ids)} occurrences")
    round_j_victims = sorted(backup_ids - local_ids)
    print(f"Round-J victims (deleted from master.py): {len(round_j_victims)}")

    remote_ids: set[int] = set()
    offset = 0
    while True:
        resp = sb.table("occurrences").select("id").range(offset, offset + 999).execute()
        page = resp.data or []
        if not page:
            break
        for r in page:
            remote_ids.add(r["id"])
        if len(page) < 1000:
            break
        offset += 1000
    print(f"Hosted Supabase: {len(remote_ids)} occurrences")

    # Only delete remote rows that are BOTH (a) round-J victims AND (b)
    # currently present in Supabase. This avoids deleting historical orphans
    # from earlier cleanup passes.
    orphans = sorted(set(round_j_victims) & remote_ids)
    print(f"Round-J orphans to delete from Supabase: {len(orphans)}")

    if not orphans:
        return 0

    if len(orphans) > 200:
        print("ABORT: more than 200 round-J orphans — sanity-check first.")
        return 1

    # Delete in chunks (PostgREST's `in` clause is fine up to a few hundred IDs).
    BATCH = 50
    for i in range(0, len(orphans), BATCH):
        chunk = orphans[i : i + BATCH]
        resp = sb.table("occurrences").delete().in_("id", chunk).execute()
        print(f"  deleted batch {i}-{i+len(chunk)-1}: {len(resp.data or [])} rows")

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
