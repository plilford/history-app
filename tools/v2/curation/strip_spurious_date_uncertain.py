"""
Curation pass: strip `date_uncertain: True` from any entry where
start_year >= 1500 AND start_month AND start_day are present.

Rationale: CLAUDE.md reserves `date_uncertain` for "genuinely fuzzy ancient
dates (circa 3000 BCE)". Several recent batches sprinkled the flag onto
confidently-dated post-1500 events that already have day precision —
making the renderer treat them as uncertain when the data is precise.

Idempotent: re-running after a pass simply finds nothing to strip.

Usage:
    cd tools
    python -m v2.curation.strip_spurious_date_uncertain          # dry run
    python -m v2.curation.strip_spurious_date_uncertain --apply  # write
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
    """Return ids of entries where date_uncertain is spurious."""
    out: list[int] = []
    for o in OCCURRENCES:
        if not o.get("date_uncertain"):
            continue
        if o.get("start_year", 0) < 1500:
            continue
        if "start_month" not in o or "start_day" not in o:
            continue
        out.append(o["id"])
    return out


# Match a single occurrence dict in master.py by id, then locate and remove
# the `"date_uncertain": True,` (or trailing-comma-less variant) inside it.
# The dicts are 5-line compact style, so we scan by id and rewrite line-by-line.
ID_LINE_RE = re.compile(r'^\s*\{"id":\s*([0-9_]+)\s*,')
DATE_UNCERTAIN_FRAG = re.compile(r'"date_uncertain":\s*True\s*,?\s*')


def rewrite(victims: set[int]) -> tuple[str, int]:
    text = MASTER_PY.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    stripped = 0

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
            # remove the fragment "date_uncertain": True (with optional trailing comma + space)
            new_line, n = DATE_UNCERTAIN_FRAG.subn("", line)
            if n:
                # Clean up double spaces or "  ,  " artefacts left behind.
                new_line = re.sub(r",\s*,", ",", new_line)
                new_line = re.sub(r"\{\s*,", "{", new_line)
                new_line = re.sub(r",\s*}", "}", new_line)
                new_line = re.sub(r"\s+\n", "\n", new_line)
                stripped += n
                line = new_line

            brace_depth += line.count("{") - line.count("}")
            if brace_depth <= 0:
                in_victim = False

        out.append(line)

    return "".join(out), stripped


def main() -> int:
    apply = "--apply" in sys.argv
    victims = set(victim_ids())
    print(f"Found {len(victims)} entries with spurious date_uncertain "
          f"(post-1500 with full day precision).")

    if not victims:
        return 0

    new_text, stripped = rewrite(victims)
    print(f"Removed {stripped} `date_uncertain` fragments from master.py.")

    if apply:
        MASTER_PY.write_text(new_text, encoding="utf-8")
        print(f"Wrote {MASTER_PY}.")
    else:
        print("(dry run — pass --apply to write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
