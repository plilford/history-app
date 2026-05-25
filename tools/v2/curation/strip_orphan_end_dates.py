"""
Curation pass: strip orphan `end_month` / `end_day` from entries that lack
`end_year`. Without `end_year` these fields are dead weight (and the DB has
no column to record them — the importer would drop them anyway).

Typical cause: author wrote a period's end month/day but forgot end_year,
leaving the entry looking like a point with a strange month-of-end field.

Idempotent.

Usage:
    cd tools
    python -m v2.curation.strip_orphan_end_dates           # dry run
    python -m v2.curation.strip_orphan_end_dates --apply   # write
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MASTER_PY = ROOT / "v2" / "data" / "master.py"
sys.path.insert(0, str(ROOT))

from v2.data.master import OCCURRENCES  # noqa: E402


def victim_ids() -> list[int]:
    out: list[int] = []
    for o in OCCURRENCES:
        if "end_year" in o:
            continue
        if "end_month" in o or "end_day" in o:
            out.append(o["id"])
    return out


ID_LINE_RE = re.compile(r'^\s*\{"id":\s*([0-9_]+)\s*,')
END_MONTH_FRAG = re.compile(r'"end_month":\s*-?\d+\s*,?\s*')
END_DAY_FRAG = re.compile(r'"end_day":\s*-?\d+\s*,?\s*')


def rewrite(victims: set[int]) -> tuple[str, int, int]:
    text = MASTER_PY.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    m_removed = 0
    d_removed = 0

    in_victim = False
    brace_depth = 0
    for line in lines:
        m = ID_LINE_RE.match(line)
        if m:
            try:
                this_id = int(m.group(1).replace("_", ""))
            except ValueError:
                this_id = None
            in_victim = this_id in victims
            brace_depth = 0

        if in_victim:
            new_line, nm = END_MONTH_FRAG.subn("", line)
            new_line, nd = END_DAY_FRAG.subn("", new_line)
            if nm or nd:
                # Tidy up artefacts
                new_line = re.sub(r",\s*,", ",", new_line)
                new_line = re.sub(r"\{\s*,", "{", new_line)
                new_line = re.sub(r",\s*}", "}", new_line)
                new_line = re.sub(r"  +", " ", new_line)
                # Don't collapse newline-only lines
                if new_line.strip() in ("", ","):
                    # Whole line was just the orphan(s); drop the line entirely
                    line = ""
                else:
                    line = new_line
            m_removed += nm
            d_removed += nd

            brace_depth += line.count("{") - line.count("}")
            if brace_depth <= 0:
                in_victim = False

        out.append(line)

    return "".join(out), m_removed, d_removed


def main() -> int:
    apply = "--apply" in sys.argv
    victims = set(victim_ids())
    print(f"Found {len(victims)} entries with orphan end_month/end_day "
          f"(no end_year present).")

    if not victims:
        return 0

    new_text, m_removed, d_removed = rewrite(victims)
    print(f"Removed {m_removed} `end_month` and {d_removed} `end_day` fragments.")

    if apply:
        MASTER_PY.write_text(new_text, encoding="utf-8")
        print(f"Wrote {MASTER_PY}.")
    else:
        print("(dry run — pass --apply to write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
