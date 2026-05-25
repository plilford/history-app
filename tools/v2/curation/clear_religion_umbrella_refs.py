"""
Clear first_zoom_out / second_zoom_out references to the four deleted
religion umbrellas (Christianity / Islam / Judaism / Major religions of the
world). Run after dedupe_round_j.py.

Leaves the religious slug TAG intact (christianity, islam, judaism,
major-religions) — only removes the dangling umbrella reference.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MASTER_PY = ROOT / "v2" / "data" / "master.py"

DANGLING_UMBRELLAS = {
    "Christianity",
    "Islam",
    "Judaism",
    "Major religions of the world",
}


def main() -> int:
    text = MASTER_PY.read_text(encoding="utf-8")
    cleared_first = 0
    cleared_second = 0

    for umb in DANGLING_UMBRELLAS:
        # Match lines like:   "first_zoom_out": "Christianity",
        # or                   "first_zoom_out": 'Christianity',
        # Drop the whole line including its trailing newline + indentation.
        pat = re.compile(
            rf'^[ \t]*"first_zoom_out":[ \t]*[\'"]{re.escape(umb)}[\'"][ \t]*,?[ \t]*\n',
            re.MULTILINE,
        )
        text, n = pat.subn("", text)
        cleared_first += n

        pat2 = re.compile(
            rf'^[ \t]*"second_zoom_out":[ \t]*[\'"]{re.escape(umb)}[\'"][ \t]*,?[ \t]*\n',
            re.MULTILINE,
        )
        text, n2 = pat2.subn("", text)
        cleared_second += n2

    MASTER_PY.write_text(text, encoding="utf-8")
    print(f"Cleared first_zoom_out refs: {cleared_first}")
    print(f"Cleared second_zoom_out refs: {cleared_second}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
