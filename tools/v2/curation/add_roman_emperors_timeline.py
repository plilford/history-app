"""
Set up the new `roman-emperors` timeline by:

  1. Adding Augustus's reign as a new occurrence (currently missing — the
     dataset jumps from the 7 kings of Rome to Tiberius's reign in 14 CE).
  2. Adding a `roman-emperors` priority on every existing "Reign of X" entry
     that names a Roman/Byzantine emperor (i.e. excludes the 7 pre-Republic
     kings of Rome). Priority = existing roman-history priority + 20_000,
     capped at 1_000_000.

Idempotent: re-running re-applies the same priorities (the curation step) and
skips the Augustus add if it's already there.

Run from `tools/`:
    .venv\\Scripts\\python.exe -m v2.curation.add_roman_emperors_timeline
    .venv\\Scripts\\python.exe -m v2.validate
    .venv\\Scripts\\python.exe -m v2.import_v2
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from v2.curation.append_entries import append_entries
from v2.data.master import OCCURRENCES

# New entry id — picks up where the round-K batch left off.
AUGUSTUS_REIGN_ID = 1_007_535

AUGUSTUS_REIGN = {
    "id": AUGUSTUS_REIGN_ID,
    "type": "event",
    "title": "Reign of Augustus",
    "start_year": -27, "start_month": 1, "start_day": 16,
    "end_year": 14, "end_month": 8, "end_day": 19,
    "description": "Octavian, having defeated Mark Antony at Actium, is granted the title Augustus by the Senate on 16 Jan 27 BCE — the conventional start of the Roman Empire. Augustus refounds Rome on autocratic lines while preserving Republican appearances; reigns until his death in 14 CE.",
    "wikipedia": "https://en.wikipedia.org/wiki/Augustus",
    "priorities": {
        "master":          970_000,
        "roman-history": 1_000_000,
        "roman-emperors": 1_000_000,
    },
    "region_weights": {"europe": 9, "americas": 3, "asia": 5, "australasia": 3, "africa": 5},
}


def is_emperor_reign(o: dict) -> bool:
    """Return True for entries that name a Roman/Byzantine emperor's reign.
    Excludes the 7 kings of Rome (pre-Republic, start_year < -509) and
    coincidentally-named medieval reigns like 'Reign of Philip II Augustus
    of France'."""
    if (o.get("title") or "").lower().startswith("reign of ") is False:
        return False
    pris = o.get("priorities") or {}
    if "roman-history" not in pris:
        return False
    s = o.get("start_year")
    if not isinstance(s, int):
        return False
    # Kings of Rome were all pre-509 BCE. Augustus's reign starts at -27.
    if s < -27:
        return False
    return True


def main() -> int:
    # 1. Add Augustus's reign if not present.
    existing_titles = {(o.get("title") or "").strip().lower() for o in OCCURRENCES}
    if AUGUSTUS_REIGN["title"].lower() not in existing_titles:
        n = append_entries([AUGUSTUS_REIGN])
        print(f"Appended {n} entry: 'Reign of Augustus' (id {AUGUSTUS_REIGN_ID})")
    else:
        print("'Reign of Augustus' already in master.py — skipping the add step.")

    # 2. For each emperor reign, ensure roman-emperors priority is set.
    #    We REWRITE master.py in place by patching just the priorities dicts.
    master_path = ROOT / "v2" / "data" / "master.py"
    text = master_path.read_text(encoding="utf-8")
    edits = 0
    skipped = 0
    for o in OCCURRENCES:
        if not is_emperor_reign(o):
            continue
        pris = o.get("priorities") or {}
        rh = int(pris.get("roman-history") or 0)
        if rh == 0:
            continue
        new_pri = min(1_000_000, rh + 20_000)
        if pris.get("roman-emperors") == new_pri:
            skipped += 1
            continue
        # Patch the priorities dict literal for this id.
        text, ok = patch_priorities_for_id(text, o["id"], "roman-emperors", new_pri)
        if ok:
            edits += 1
        else:
            print(f"  WARN: could not patch priorities for id {o['id']} "
                  f"({o.get('title')!r})")

    master_path.write_text(text, encoding="utf-8")
    print(f"Updated {edits} emperor reign(s) with roman-emperors priority "
          f"({skipped} already correct)")
    return 0


# --------------------------------------------------------------------------- #
# In-place patcher
# --------------------------------------------------------------------------- #

import re

ID_LINE_RE = re.compile(r'^(\s+)\{?"id":\s*([\d_]+),', re.MULTILINE)
PRIORITIES_RE = re.compile(r'("priorities":\s*\{[^{}]*?\})')


def patch_priorities_for_id(
    text: str, eid: int, slug: str, value: int,
) -> tuple[str, bool]:
    """Add (or update) a slug→value pair inside the priorities dict for the
    given occurrence id. master.py's entries are multi-line dicts in the
    canonical 5-line format produced by append_entries — the priorities
    dict is on its own line, never nested in anything weird, so a simple
    regex within the entry's slice works fine."""
    # Find the line with this id.
    target = f"{eid:_}"
    pos = 0
    while True:
        m = ID_LINE_RE.search(text, pos)
        if not m:
            return text, False
        if m.group(2) == target:
            break
        pos = m.end()
    # The entry spans from this id line to its closing `},`. We search
    # forwards for the priorities dict — guaranteed to be inside the same
    # entry because of the canonical layout.
    entry_start = m.start()
    pm = PRIORITIES_RE.search(text, entry_start)
    if not pm:
        return text, False
    inner_dict = pm.group(1)
    if f'"{slug}"' in inner_dict:
        # Update existing entry.
        new_inner = re.sub(
            rf'"{re.escape(slug)}":\s*\d[\d_]*',
            f'"{slug}": {value}',
            inner_dict,
            count=1,
        )
    else:
        # Insert as a new key inside the dict — drop in just before the `}`.
        # Preserve the line's existing style.
        new_inner = inner_dict.rstrip("}").rstrip()
        if not new_inner.endswith(","):
            new_inner += ","
        new_inner = f'{new_inner} "{slug}": {value}}}'
    return text[:pm.start()] + new_inner + text[pm.end():], True


if __name__ == "__main__":
    raise SystemExit(main())
