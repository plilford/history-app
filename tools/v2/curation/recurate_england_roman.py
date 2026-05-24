"""
Re-curate per-slug priorities for `england` and `roman-history` to use the
full 0-1M range, basing them on the master priority of each entry.

Rule:
    per_slug_pri = master_priority
    + boost if the entry is unmistakably anchored to this slug
    - penalty if the entry is multi-regional (also tagged on france/china/etc.)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MASTER_PY = ROOT / "v2" / "data" / "master.py"
sys.path.insert(0, str(ROOT))

from v2.data import master as m


COMPETING_REGIONAL = {"france", "china", "india", "usa", "us-presidents", "russia", "japan"}

# Strong markers (substring in title, case-insensitive) — entry is firmly
# anchored to that slug. Boosts within-slug priority slightly above master.
ENGLAND_STRONG = [
    "england", "english", "britain", "british", "london", "tudor", "stuart",
    "plantagenet", "norman conquest of england", "magna carta", "hastings",
    "cromwell", "churchill", "thatcher", "blair", "henry viii", "elizabeth i",
    "elizabeth ii", "queen victoria", "henry v", "edward iii", "william the conqueror",
    "anglo-saxon", "anglo-irish", "reform act", "spitfire", "blitz",
    "nhs", "brexit", "wars of the roses", "spanish armada", "anarchy in england",
    "wessex", "mercia", "northumbria", "domesday", "victorian", "georgian",
    "elizabethan", "edwardian", "agincourt", "bosworth", "naseby", "marston moor",
    "edgehill", "trafalgar", "waterloo", "boyne", "act of union",
    "great fire of london", "great plague of london", "gunpowder plot",
    "windrush", "good friday agreement", "falklands", "diana",
    "battle of britain", "dunkirk", "battle of crécy", "battle of poitiers",
    "owain glyn", "boer war", "great exhibition", "crystal palace",
]

ROMAN_STRONG = [
    "rome ", "romans", "roman ", " rome", "rome's", "punic", "carthage",
    "caesar", "augustus", "tiberius", "caligula", "claudius", "nero",
    "vespasian", "titus", "domitian", "nerva", "trajan", "hadrian",
    "antoninus pius", "marcus aurelius", "commodus", "septimius severus",
    "diocletian", "constantine", "julian the apostate", "theodosius",
    "justinian", "heraclius", "basil", "alexios", "constantine xi",
    "byzantine", "byzantium", "constantinople", "hagia sophia",
    "republic", "principate", "tetrarchy", "patrician", "plebeian",
    "consul", "senate", "tribune", "gracch", "sulla", "marius", "pompey",
    "crassus", "spartacus", "cleopatra", "mark antony", "cicero", "virgil",
    "ovid", "scipio", "hannibal", "etruscan", "samnite", "pyrrhic",
    "twelve tables", "lex ", "alaric", "odoacer", "attila", "vandals",
    "visigoth", "ostrogoth", "battle of cannae", "battle of zama",
    "milvian bridge", "pharsalus", "philippi", "actium", "thermopylae",
    "battle of adrianople", "battle of yarmouk", "battle of manzikert",
    "fall of constantinople", "fall of rome", "fall of the western roman",
]


def make_matchers(strong: list[str]):
    pats = [re.compile(rf"\b{re.escape(s)}\b", re.I) if " " not in s and "-" not in s
            else re.compile(re.escape(s), re.I) for s in strong]
    def matches(text: str) -> bool:
        return any(p.search(text) for p in pats)
    return matches


is_strong_england = make_matchers(ENGLAND_STRONG)
is_strong_roman = make_matchers(ROMAN_STRONG)


def new_priority(occ: dict, slug: str) -> int:
    master = occ["priorities"]["master"]
    title = occ["title"]
    slugs = set(occ["priorities"].keys())
    other_regional = COMPETING_REGIONAL & slugs

    base = master
    if slug == "england":
        strong = is_strong_england(title) or "england-monarchs" in slugs
    else:  # roman-history
        strong = is_strong_roman(title)

    if strong:
        base = min(999_000, base + 30_000)
    if other_regional:
        # Multi-regional event — within-slug importance should be lower than
        # global master priority since the entry is shared with another timeline.
        base = max(400_000, base - 90_000)
    if not strong and slug not in {"england-monarchs"} and not other_regional:
        # Entry is tangentially relevant — bring it down a bit.
        base = max(400_000, base - 30_000)
    return base


def main() -> int:
    # Compute new priorities for every entry tagged england or roman-history.
    new_eng: dict[int, int] = {}
    new_rom: dict[int, int] = {}
    for o in m.OCCURRENCES:
        pri = o.get("priorities", {})
        if "england" in pri:
            new_eng[o["id"]] = new_priority(o, "england")
        if "roman-history" in pri:
            new_rom[o["id"]] = new_priority(o, "roman-history")

    text = MASTER_PY.read_text(encoding="utf-8")

    # Find each occurrence block; for each, locate its priorities line and
    # rewrite the england and/or roman-history value.
    id_re = re.compile(r'\{"id": (\d[\d_]*),')
    matches = list(id_re.finditer(text))
    rewrites = 0

    pri_re = re.compile(r'("priorities":\s*\{)([^}]*)(\})')
    val_re = lambda s: re.compile(rf'"{s}":\s*(\d+)')

    new_parts = []
    cursor = 0
    for i, m_ in enumerate(matches):
        bid = int(m_.group(1).replace("_", ""))
        start = m_.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        new_parts.append(text[cursor:start])
        block = text[start:end]

        if bid in new_eng or bid in new_rom:
            def update(pri_match: re.Match) -> str:
                inner = pri_match.group(2)
                if bid in new_eng:
                    inner = val_re("england").sub(f'"england": {new_eng[bid]}', inner)
                if bid in new_rom:
                    inner = val_re("roman-history").sub(f'"roman-history": {new_rom[bid]}', inner)
                return f"{pri_match.group(1)}{inner}{pri_match.group(3)}"
            new_block, n = pri_re.subn(update, block, count=1)
            if n > 0:
                rewrites += 1
            new_parts.append(new_block)
        else:
            new_parts.append(block)
        cursor = end
    new_parts.append(text[cursor:])

    MASTER_PY.write_text("".join(new_parts), encoding="utf-8")
    print(f"Re-curated priorities for {rewrites} entries "
          f"({len(new_eng)} england, {len(new_rom)} roman-history).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
