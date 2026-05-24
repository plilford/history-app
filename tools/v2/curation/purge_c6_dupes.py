"""
Auto-build a purge plan from validate.py's duplicate-title errors for the C6
batch. For each (old_id, new_id) pair, look up the old entry's master priority
and emit a tuple that the purge_duplicates script can apply.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from v2.data import master as m
from v2.curation.purge_duplicates import PURGE_PLAN as EXISTING_PLAN

OUT = ROOT / "v2" / "curation" / "c6_purge_tuples.txt"


def main() -> int:
    # Run validate, capture stderr (which has the duplicate errors).
    import os
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(
        [sys.executable, "-m", "v2.validate"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(ROOT),
        env=env,
    )
    out = (proc.stdout or "") + (proc.stderr or "")

    pat = re.compile(r"duplicate title .*?: ids (\d+), (\d+)")
    pairs = pat.findall(out)
    by_id = {o["id"]: o for o in m.OCCURRENCES}

    already = set()
    for (del_id, prom_id, _) in EXISTING_PLAN:
        already.add((del_id, prom_id))

    lines = []
    for a, b in pairs:
        a, b = int(a), int(b)
        # Older entry is the smaller ID; promote the newer (higher) entry.
        old_id = min(a, b)
        new_id = max(a, b)
        if (old_id, new_id) in already:
            continue
        if old_id not in by_id or new_id not in by_id:
            continue
        old_pri = by_id[old_id]["priorities"].get("master", 800_000)
        new_pri = by_id[new_id]["priorities"].get("master", 800_000)
        # Bump promoted entry to the max of old/new master priority.
        bumped = max(old_pri, new_pri)
        lines.append(f"    ({old_id:_}, {new_id:_}, {bumped}),")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(lines)} new purge tuples to {OUT}")
    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
