"""
One-off curation script: tag existing master.py entries with 'england' and/or
'roman-history' priority slugs.

Strategy: rule-based curation with explicit allow lists. Two passes are made:

Pass 1 (auto-include from strong signals):
  - any entry already on `england-monarchs` -> england
  - any entry whose first/second zoom-out points to a clear British umbrella -> england
  - any entry whose title contains an unambiguous British marker -> england
  - any entry whose title or description contains an unambiguous Roman marker -> roman-history

Pass 2 (curated overrides): explicit ID list to add or exclude.

Writes the proposed (id -> [slugs to add]) mapping to a JSON file for review,
then (if --apply) does an in-place text rewrite of master.py's priorities lines.

Usage:
    python -m v2.curation.tag_england_roman           # dry run, writes proposed_tags.json
    python -m v2.curation.tag_england_roman --apply   # actually edit master.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MASTER_PY = ROOT / "v2" / "data" / "master.py"

sys.path.insert(0, str(ROOT))
from v2.data.master import OCCURRENCES  # noqa: E402


# --- Default priorities for newly tagged entries --------------------------
# Within-slug ranking: 800k floor, 1M ceiling. We map per-tier priorities so
# the new slug timelines have a sensible default ordering. The user can re-
# curate later.
DEFAULT_ENGLAND_PRIORITY = 880_000
DEFAULT_ROMAN_PRIORITY = 880_000

# --- Strong-signal rules --------------------------------------------------
BRITISH_UMBRELLAS = {
    "anarchy in england",
    "anglo-saxon settlement of britain",
    "english reformation",
    "victorian era",
    "wars of the roses",
    "english civil war",
}

# Unambiguous British markers — substrings (case-insensitive) in TITLE only.
# Keep these tight to avoid over-tagging US entries that mention 'British'.
BRITISH_TITLE_MARKERS = [
    r"\bengland\b", r"\benglish\b", r"\bbritain\b", r"\bbritish\b",
    r"\bUK\b", r"\bUnited Kingdom\b",
    r"\banglo[- ]saxon\b", r"\banglo[- ]norman\b",
    r"\btudor\b", r"\bstuart\b", r"\bplantagenet\b", r"\bhanoverian\b",
    r"\bnorman conquest\b", r"\bmagna carta\b", r"\bdomesday\b",
    r"\bwessex\b", r"\bmercia\b", r"\bnorthumbria\b",
    r"\blondon\b", r"\bedinburgh\b", r"\bdublin\b",
    r"\bscotland\b", r"\bscottish\b", r"\bwales\b", r"\bwelsh\b",
    r"\birish\b", r"\bireland\b", r"\bulster\b",
    r"\bvictorian\b", r"\bgeorgian\b", r"\belizabethan\b", r"\bedwardian\b",
    r"\bhastings\b", r"\bagincourt\b", r"\bbosworth\b", r"\bwaterloo\b",
    r"\bcromwell\b", r"\bchurchill\b", r"\bthatcher\b", r"\bgladstone\b",
    r"\bdisraeli\b", r"\bbrunel\b", r"\bnewton\b", r"\bdarwin\b",
    r"\bshakespeare\b", r"\bdickens\b", r"\baustin\b", r"\bbronte\b",
    r"\bspitfire\b", r"\bblitz\b", r"\bdunkirk\b",
    r"\bbritish empire\b", r"\bbritish commonwealth\b",
    r"\bbrexit\b", r"\bsuez\b",
    r"\battlee\b", r"\bblair\b", r"\bmajor\b", r"\bcameron\b",
    r"\bmonarchy\b",
]
BRITISH_TITLE_RE = re.compile("|".join(BRITISH_TITLE_MARKERS), re.I)

# Whitelist additions where the strong-signal regex misses something.
# (Plain English titles for famous British people/events/works that lack a
# British keyword in the title.)
ENGLAND_EXTRA_TITLE_HINTS = {
    # monarchs / dynasties (titles often just say 'Henry V', 'Mary I', etc.)
    "alfred the great", "athelstan", "edmund i", "eadred", "edgar the peaceful",
    "edward the confessor", "harold godwinson",
    "william the conqueror", "william ii", "henry i", "stephen of england",
    "henry ii of england", "richard i", "king john", "henry iii of england",
    "edward i", "edward ii", "edward iii", "richard ii of england",
    "henry iv of england", "henry v", "henry vi", "edward iv", "edward v",
    "richard iii", "henry vii", "henry viii", "edward vi",
    "mary i", "elizabeth i", "james i of england",
    "charles i of england", "charles ii of england",
    "william iii", "mary ii", "queen anne",
    "george i", "george ii", "george iii", "george iv",
    "william iv", "queen victoria", "edward vii", "george v",
    "edward viii", "george vi", "elizabeth ii", "king charles iii",
    "magna carta", "bayeux tapestry", "battle of hastings",
    "domesday book", "hundred years' war", "wars of the roses",
    "battle of agincourt", "battle of bosworth field", "battle of waterloo",
    "great fire of london", "great plague of london", "gunpowder plot",
    "act of union", "boer war", "battle of trafalgar",
    "industrial revolution", "stephenson's rocket",
    "isaac newton", "william shakespeare", "charles dickens",
    "geoffrey chaucer", "jane austen", "the bronte sisters",
    "charles darwin", "michael faraday", "alan turing",
    "winston churchill", "margaret thatcher", "tony blair",
    "diana, princess of wales", "the beatles", "rolling stones",
    "battle of britain", "blitz",
    "good friday agreement", "falklands war",
}

# --- Roman markers --------------------------------------------------------
ROMAN_TITLE_MARKERS = [
    r"\bromans?\b", r"\brome\b", r"\bbyzant", r"\bconstantinople\b",
    r"\bcaesar\b", r"\baugust(us|an)\b", r"\bcaligula\b", r"\bclaudius\b",
    r"\bnero\b", r"\bvespasian\b", r"\btitus\b", r"\bdomitian\b",
    r"\bnerva\b", r"\btrajan\b", r"\bhadrian\b", r"\bantonin",
    r"\bmarcus aurelius\b", r"\bcommodus\b",
    r"\bdiocletian\b", r"\bconstantine\b", r"\btheodosius\b",
    r"\bjulian\b", r"\bvalentinian\b", r"\bhonorius\b",
    r"\bjustinian\b", r"\bheraclius\b", r"\bbasil\b", r"\balexius\b",
    r"\bpunic\b", r"\bcarthag", r"\bhannibal\b", r"\bscipio\b",
    r"\bgallic wars?\b", r"\bgaul\b",
    r"\bcicero\b", r"\bvirgil\b", r"\bovid\b", r"\bseneca\b", r"\btacitus\b",
    r"\blivy\b", r"\bcato\b", r"\bsulla\b", r"\bpompey\b", r"\bcrassus\b",
    r"\bmark antony\b", r"\bcleopatra\b", r"\bspartacus\b", r"\bgladiator\b",
    r"\bcolosseum\b", r"\bpompeii\b", r"\bvesuvius\b", r"\bpantheon\b",
    r"\baeneid\b", r"\bgallic\b",
    r"\bconsul\b", r"\bsenate\b", r"\btribune\b", r"\bdictator\b",
    r"\betruscan\b", r"\bremus\b", r"\bromulus\b",
    r"\bostrogoth", r"\bvisigoth", r"\balaric\b", r"\bodoacer\b",
    r"\battila\b", r"\bvandals\b",
]
ROMAN_TITLE_RE = re.compile("|".join(ROMAN_TITLE_MARKERS), re.I)

# Hard excludes — entries that match the regex but are NOT really England/Roman.
# Add by exact title (case-insensitive). Stays small; mostly addresses obvious
# false positives from the broad regex (e.g. 'British Mandate of Palestine'
# is more Israel/Palestine history than English history).
EXCLUDE_FROM_ENGLAND = {
    "american declaration of independence",
    "boston tea party",
    "us declaration of independence",
}
EXCLUDE_FROM_ROMAN = {
    "alexander the great",  # pre-Roman; in scope for separate Greek timeline
    "cyrus the great",
    "mao zedong",
    "genghis khan",
    "world war i",
    "world war ii",
    "ww1",
    "ww2",
    "berlin wall falls",
    "reign of philip ii augustus of france",
    "philip ii augustus of france",
    "philip ii augustus",
    "charlemagne crowned holy roman emperor",
    "coronation of charlemagne",
    "investiture controversy",  # HRE vs Papacy
    "norman conquest of sicily",  # in scope for Norman/England arguably, not Roman
    "synod of whitby",  # Anglo-Saxon Christianity — England-only
    "parthian empire",
    "christianisation of kievan rus'",
    "kievan rus'",
    "reign of charlemagne",
    "reign of æthelwulf",
    "avignon papacy begins",
    "avignon papacy ends",
    "battle of bouvines",
    "first crusade",
    "second crusade",
    "third crusade",
    "fifth crusade",
    "sixth crusade",
    "seventh crusade",
    "muslim conquest of egypt",  # arguable but skip to keep tight
    "muslim conquest of syria",
    "edward the confessor",  # already england-tagged; not core Roman
}

# Roman titles that don't trip the regex but DO belong.
ROMAN_EXTRA_TITLE_HINTS = {
    "founding of rome", "founding of rome (traditional)",
    "fall of the western roman empire", "fall of constantinople",
    "first triumvirate", "second triumvirate",
    "battle of cannae", "battle of zama", "battle of pharsalus",
    "battle of philippi", "battle of actium", "battle of teutoburg forest",
    "battle of milvian bridge", "battle of adrianople", "battle of yarmouk",
    "battle of manzikert", "sack of rome by visigoths",
    "edict of milan", "edict of caracalla", "conversion of constantine",
    "founding of constantinople", "fourth crusade", "sack of constantinople by fourth crusade",
    "east–west schism", "great schism",
    "first council of nicaea", "council of chalcedon",
    "twelve tables", "law of the twelve tables",
    "year of the four emperors", "crisis of the third century",
    "diocletianic persecution", "tetrarchy",
    "battle of the milvian bridge",
}


def classify(occ: dict) -> tuple[bool, bool]:
    """Return (tag_england, tag_roman) for a single occurrence."""
    title = (occ.get("title") or "").strip().lower()
    desc = (occ.get("description") or "").strip().lower()
    slugs = set(occ.get("priorities", {}).keys())
    fzo = (occ.get("first_zoom_out") or "").strip().lower()
    szo = (occ.get("second_zoom_out") or "").strip().lower()
    year = occ.get("start_year")

    # --- England ---
    eng = False
    if title in EXCLUDE_FROM_ENGLAND:
        eng = False
    elif "england-monarchs" in slugs:
        eng = True
    elif fzo in BRITISH_UMBRELLAS or szo in BRITISH_UMBRELLAS:
        eng = True
    elif BRITISH_TITLE_RE.search(occ.get("title") or ""):
        # Filter out a couple of common false positives in the broad regex:
        bad = False
        if title.startswith("american "):
            bad = True
        if "british mandate" in title:
            bad = True
        if "british raj" in title:  # better suited to India timeline; still arguably English
            bad = False
        if not bad:
            eng = True
    elif title in ENGLAND_EXTRA_TITLE_HINTS:
        eng = True

    # --- Roman ---
    rom = False
    if title in EXCLUDE_FROM_ROMAN:
        rom = False
    elif title in ROMAN_EXTRA_TITLE_HINTS:
        rom = True
    elif ROMAN_TITLE_RE.search(occ.get("title") or ""):
        # Need to avoid stuff like 'Holy Roman Empire' (per user decision: exclude HRE)
        # unless it's the founding moment of HRE under Charlemagne (skip — out of scope).
        if "holy roman empire" in title:
            rom = False
        elif year is not None and (year < -800 or year > 1500):
            # Tight bound: Roman/Byzantine span. Allow some pre/post context.
            rom = False
        else:
            rom = True
    else:
        # Description-only check: only fire if year falls in the core Roman span
        # AND description mentions a strong Roman marker. Otherwise too noisy.
        if year is not None and -800 <= year <= 1453:
            if ROMAN_TITLE_RE.search(occ.get("description") or ""):
                # Description-only matches are weaker — only count if at least
                # one Roman marker is a "core" one (Rome/Roman/Byzantine/etc).
                if re.search(r"\b(rome|roman|romans|byzantine|byzantium|caesar)\b",
                             occ.get("description") or "", re.I):
                    rom = True

    return eng, rom


def main() -> int:
    apply_changes = "--apply" in sys.argv

    proposed: dict[int, list[str]] = {}
    eng_count = rom_count = both_count = 0

    for occ in OCCURRENCES:
        eng, rom = classify(occ)
        if not (eng or rom):
            continue
        slugs = []
        if eng and "england" not in occ.get("priorities", {}):
            slugs.append("england")
        if rom and "roman-history" not in occ.get("priorities", {}):
            slugs.append("roman-history")
        if slugs:
            proposed[occ["id"]] = slugs
            if "england" in slugs:
                eng_count += 1
            if "roman-history" in slugs:
                rom_count += 1
            if len(slugs) == 2:
                both_count += 1

    # Write proposal JSON for review
    out_path = Path(__file__).parent / "proposed_tags.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "summary": {
                    "england_total": eng_count,
                    "roman_history_total": rom_count,
                    "both": both_count,
                    "entries_touched": len(proposed),
                },
                "tags": {str(k): v for k, v in proposed.items()},
            },
            f,
            indent=2,
            sort_keys=True,
        )
    print(f"Proposed: {eng_count} england tags, {rom_count} roman-history tags, "
          f"{both_count} both-tagged. {len(proposed)} entries touched.")
    print(f"Wrote {out_path}")

    if not apply_changes:
        print("\nDry run. Re-run with --apply to modify master.py.")
        return 0

    # --- Apply by line-level rewrite of the priorities line for each id ----
    text = MASTER_PY.read_text(encoding="utf-8")

    # Each occurrence dict has an "id": N line and a "priorities": {...} line.
    # We split the file into per-occurrence blocks using {"id": ...} as the
    # boundary, then rewrite each block whose id is in our proposed set.
    id_re = re.compile(r'\{"id": (\d[\d_]*),')

    # Build an index of (id, start_pos_of_id_line) for every occurrence.
    matches = list(id_re.finditer(text))
    spans: list[tuple[int, int, int]] = []  # (id_int, block_start, block_end)
    for i, m in enumerate(matches):
        bid = int(m.group(1).replace("_", ""))
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        spans.append((bid, start, end))

    # For each block we need to update, locate its `"priorities": {...}` line
    # and inject our new slug(s). The dict is on a single line in master.py.
    new_chunks: list[str] = []
    cursor = 0
    rewrites = 0

    pri_re = re.compile(r'("priorities":\s*\{)([^}]*)(\})')

    for bid, start, end in spans:
        new_chunks.append(text[cursor:start])
        block = text[start:end]
        if bid in proposed:
            new_slugs = proposed[bid]
            def add_slugs(match: re.Match) -> str:
                opener, inner, closer = match.group(1), match.group(2).strip(), match.group(3)
                additions = []
                for s in new_slugs:
                    priority = DEFAULT_ENGLAND_PRIORITY if s == "england" else DEFAULT_ROMAN_PRIORITY
                    additions.append(f'"{s}": {priority}')
                if inner.endswith(","):
                    new_inner = inner + " " + ", ".join(additions)
                else:
                    new_inner = inner + ", " + ", ".join(additions)
                return f"{opener}{new_inner}{closer}"

            new_block, n = pri_re.subn(add_slugs, block, count=1)
            if n == 0:
                print(f"  WARN: id {bid}: no priorities dict found, skipped")
                new_chunks.append(block)
            else:
                new_chunks.append(new_block)
                rewrites += 1
        else:
            new_chunks.append(block)
        cursor = end
    new_chunks.append(text[cursor:])
    new_text = "".join(new_chunks)

    MASTER_PY.write_text(new_text, encoding="utf-8")
    print(f"Applied {rewrites} rewrites to master.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
