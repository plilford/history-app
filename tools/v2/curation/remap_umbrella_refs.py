"""
Remap dangling first_zoom_out / second_zoom_out references after Round J
dedupe. Some umbrella entries got renamed/replaced when we picked canonical
survivors — entries that reference them by title now need to be repointed.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MASTER_PY = ROOT / "v2" / "data" / "master.py"

REMAP: dict[str, str] = {
    "Qing dynasty founded": "Qing dynasty",
    "Gupta Empire (Indian Golden Age)": "Gupta Empire",
}


def main() -> int:
    text = MASTER_PY.read_text(encoding="utf-8")
    total = 0
    for old, new in REMAP.items():
        for key in ("first_zoom_out", "second_zoom_out"):
            pat = re.compile(
                rf'("{key}":\s*)[\'"]{re.escape(old)}[\'"]',
            )
            text, n = pat.subn(rf"\1'{new}'", text)
            if n:
                print(f"  {key}: {old!r} -> {new!r}: {n} entries")
                total += n
    MASTER_PY.write_text(text, encoding="utf-8")
    print(f"Total remaps: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
