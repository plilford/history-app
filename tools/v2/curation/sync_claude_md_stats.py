"""
Re-sync the "Current size" line in CLAUDE.md with the actual count + max ID
from master.py.

Why this exists: the Cowork-mode Write/Edit tools silently truncate large
files on FUSE-mounted workspaces (documented gotcha — see session 15 notes),
which made CLAUDE.md hard to update during normal authoring sessions. This
script uses a Python file rewrite (which is unaffected by the truncation
bug) and targets a single specific line. Safe to re-run.

Usage:
    cd tools
    python -m v2.curation.sync_claude_md_stats          # dry run
    python -m v2.curation.sync_claude_md_stats --apply  # write
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from v2.data.master import OCCURRENCES  # noqa: E402

CLAUDE_MD = ROOT.parent / "CLAUDE.md"

LINE_RE = re.compile(
    r"Current size: \*\*~[\d,]+ entries\*\*, max ID around \*\*[0-9_]+\*\*"
)


def main() -> int:
    apply = "--apply" in sys.argv
    count = len(OCCURRENCES)
    max_id = max(o["id"] for o in OCCURRENCES)
    # Format max_id with underscores: 1_007_020
    max_id_under = f"{max_id:_}"

    text = CLAUDE_MD.read_text(encoding="utf-8")
    new_line = (
        f"Current size: **~{count:,} entries**, "
        f"max ID around **{max_id_under}**"
    )
    new_text, n = LINE_RE.subn(new_line, text)
    if n == 0:
        print("ERROR: couldn't find the 'Current size' line in CLAUDE.md.")
        print("       Maybe it's been reworded? Pattern looked for:")
        print(f"       {LINE_RE.pattern}")
        return 1

    if new_text == text:
        print(f"CLAUDE.md already in sync ({count:,} entries, max ID {max_id_under}).")
        return 0

    print(f"Would update CLAUDE.md → {count:,} entries, max ID {max_id_under}.")
    if apply:
        CLAUDE_MD.write_text(new_text, encoding="utf-8")
        print("Wrote CLAUDE.md.")
    else:
        print("(dry run — pass --apply to write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
