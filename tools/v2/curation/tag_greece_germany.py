"""
Tag existing master.py entries with `ancient-greece` and `germany` slugs.

Per-slug priority for newly tagged entries is derived from the entry's master
priority (no flat 800k floor):
    base = master_priority
    +30k if title contains a strong slug-anchored marker
    -90k if entry is also on another regional slug (france/china/etc.) — it's
        multi-regional, not slug-owned
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


COMPETING_REGIONAL = {"france", "china", "india", "usa", "us-presidents",
                       "russia", "japan", "england", "england-monarchs"}


# --- Greece -----------------------------------------------------------------
# Title-substring patterns (case-insensitive) that mark entries as Greek-anchored.
GREEK_TITLE_MARKERS = [
    r"\b(ancient )?greece\b", r"\bgreek\b", r"\bathens\b", r"\bathenian\b",
    r"\bsparta\b", r"\bspartan\b", r"\bthebe[ds]\b",
    r"\bminoan\b", r"\bmycenae", r"\bmycenaean\b", r"\bcrete\b",
    r"\btroy\b", r"\btrojan\b", r"\bhomer\b", r"\bhesiod\b", r"\bsappho\b",
    r"\bpythagoras\b", r"\bheraclitus\b", r"\bdemocritus\b", r"\bsocrates\b",
    r"\bplato\b", r"\baristotle\b", r"\bepicurus\b", r"\bdiogenes\b",
    r"\bsolon\b", r"\bcleisthenes\b", r"\bpericles\b", r"\bdemosthenes\b",
    r"\balcibiades\b", r"\bthemistocles\b", r"\bleonidas\b",
    r"\bmarathon\b", r"\bthermopylae\b", r"\bsalamis\b", r"\bplataea\b",
    r"\bmycale\b", r"\bartemisium\b", r"\bdelian league\b", r"\bdelian\b",
    r"\bpeloponnesian\b", r"\baigospotam", r"\bsicilian expedition\b",
    r"\bleuctra\b", r"\bmantinea\b", r"\bchaeronea\b",
    r"\bmacedon\b", r"\bphilip ii of macedon\b", r"\balexander the great\b",
    r"\bgranicus\b", r"\bissus\b", r"\bgaugamela\b", r"\bhydaspes\b",
    r"\bdiadoch", r"\bptolemai", r"\bseleucid\b", r"\bantigonid\b",
    r"\bhellenistic\b", r"\bhellenic\b",
    r"\billiad\b", r"\biliad\b", r"\bodyssey\b", r"\baeschylus\b",
    r"\bsophocles\b", r"\beuripides\b", r"\baristophanes\b",
    r"\bthucydides\b", r"\bherodotus\b", r"\bxenophon\b",
    r"\bphidias\b", r"\bparthenon\b", r"\bacropolis\b",
    r"\bolympic games\b", r"\bolympia\b",
    r"\barchimedes\b", r"\beuclid\b", r"\bptolemy (\(astronom|the astronomer)\b",
    r"\bhippocrates\b",
]
GREEK_TITLE_RE = re.compile("|".join(GREEK_TITLE_MARKERS), re.I)

GREEK_EXTRA_HINTS = {  # exact lowercased titles to include even without regex hit
    "trojan war", "rise of the polis",
}

GREEK_EXCLUDES = {  # exact lowercased titles to skip even if regex hits
    "ancient greece",  # in case a meta entry exists
    "greek fire",  # Byzantine weapon, not Ancient Greece
}


# --- Germany ----------------------------------------------------------------
# We use the user's earlier guidance: include the Holy Roman Empire in Germany
# even though it was excluded from roman-history. Frankish kingdom included
# until the Treaty of Verdun (843) onwards (when East Francia becomes Germany).
GERMAN_TITLE_MARKERS = [
    r"\bgerman[ys]?\b", r"\bgermans\b", r"\bgermanic\b",
    r"\bprussia(n)?\b", r"\bbavaria(n)?\b", r"\bsaxon(y|ic)?\b", r"\brhin(e|eland)\b",
    r"\bbrandenburg\b", r"\bhanover\b", r"\bwurttemberg\b",
    r"\bberlin\b", r"\bmunich\b", r"\bhamburg\b", r"\bdresden\b", r"\bcolog?ne\b",
    r"\bweimar\b", r"\bbonn\b", r"\bfrankfurt\b",
    r"\bholy roman\b", r"\bcharlemagne\b", r"\bcarolingian\b",
    r"\bbarbarossa\b", r"\bfrederick (the great|ii|i)\b",
    r"\bhohenstaufen\b", r"\bhohenzollern\b", r"\bhabsburg\b",
    r"\botto (i|the great)\b", r"\botto i\b",
    r"\bteutoburg\b", r"\bteutonic\b",
    r"\bluther\b", r"\bmelanchthon\b", r"\b95 theses\b", r"\bninety-five theses\b",
    r"\bdiet of worms\b", r"\bpeasants' war\b", r"\bschmalkald",
    r"\bthirty years\b", r"\bwestphalia\b", r"\bgustav(us)? adolph\b",
    r"\bwallenstein\b", r"\bdefenestration of prague\b",
    r"\bbismarck\b", r"\bkaiser\b", r"\bwilhelm[i]?\b",
    r"\bnaz[is]\b", r"\bhitler\b", r"\bhindenburg\b", r"\bgoebbels\b",
    r"\bgoering\b", r"\bhimmler\b", r"\beichmann\b",
    r"\bthird reich\b", r"\breich\b",
    r"\bnuremberg\b", r"\bdachau\b", r"\bauschwitz\b",
    r"\bblitzkrieg\b", r"\bwehrmacht\b", r"\bluftwaffe\b",
    r"\boperation barbarossa\b",
    r"\bstalingrad\b",  # German defeat
    r"\bberlin wall\b", r"\bberlin airlift\b",
    r"\beast germany\b", r"\bwest germany\b", r"\bgdr\b", r"\bfrg\b",
    r"\breunification\b", r"\bdeutschland\b",
    r"\badenauer\b", r"\bbrandt\b", r"\bkohl\b", r"\bmerkel\b", r"\bschr",
    r"\branke\b", r"\bgoethe\b", r"\bschiller\b", r"\bbeethoven\b",
    r"\bmozart\b",  # Austrian — only if German-tagged elsewhere; will exclude below
    r"\bbach\b", r"\bbrahms\b", r"\bwagner\b",  # composers
    r"\bkant\b", r"\bnietzsche\b", r"\bheidegger\b", r"\bhusserl\b", r"\bhegel\b",
    r"\bmarx\b", r"\bengels\b",  # philosophers/economists
    r"\beinstein\b", r"\bplanck\b", r"\bheisenberg\b", r"\bbohr\b",
    r"\bzeppelin\b",
]
GERMAN_TITLE_RE = re.compile("|".join(GERMAN_TITLE_MARKERS), re.I)

GERMAN_EXTRA_HINTS = {
    "world war i", "world war ii",
}

# Things that match the regex but aren't really German history.
GERMAN_EXCLUDES = {
    "marx and engels publish the communist manifesto",  # London-based, more about ideology
    "mozart",  # Austrian
    "mozart's requiem",
    "mozart's the magic flute",
    "wolfgang amadeus mozart",
    "operation market garden",  # Allied operation; tag stalingrad-side only
    "stalin",
    "assassination of martin luther king jr.",  # American civil rights, not Luther
    "martin luther king jr.",
    "martin luther king",
    "glass's einstein on the beach",  # American opera about Einstein
    "reich's music for 18 musicians",  # Steve Reich, American composer
    "wagner group mutiny",  # Russian PMC, not German
}


def is_greek(occ: dict) -> bool:
    title = (occ.get("title") or "").strip().lower()
    if title in GREEK_EXCLUDES:
        return False
    if title in GREEK_EXTRA_HINTS:
        return True
    year = occ.get("start_year")
    # Tight bound: pre-Roman Greece is the focus, with slight overlap.
    if year is not None and year > 200:
        return False
    return bool(GREEK_TITLE_RE.search(occ.get("title") or ""))


def is_german(occ: dict) -> bool:
    title_raw = occ.get("title") or ""
    title = title_raw.strip().lower()
    if title in GERMAN_EXCLUDES:
        return False
    # Anglo-Saxon entries are about England, not Germany.
    if "anglo-saxon" in title or "anglo saxon" in title:
        return False
    # Heptarchy is English.
    if "heptarchy" in title:
        return False
    if title in GERMAN_EXTRA_HINTS:
        return True
    if GERMAN_TITLE_RE.search(title_raw):
        return True
    return False


def derive_priority(occ: dict, slug: str, strong: bool) -> int:
    """Derive within-slug priority from master priority + adjustments."""
    master = occ.get("priorities", {}).get("master", 800_000)
    other_regional = COMPETING_REGIONAL & set(occ.get("priorities", {}).keys())
    base = master
    if strong:
        base = min(999_000, base + 30_000)
    if other_regional:
        base = max(400_000, base - 90_000)
    return base


def main() -> int:
    apply_changes = "--apply" in sys.argv

    proposed: dict[int, dict[str, int]] = {}
    for occ in OCCURRENCES:
        adds: dict[str, int] = {}
        if is_greek(occ) and "ancient-greece" not in occ.get("priorities", {}):
            adds["ancient-greece"] = derive_priority(occ, "ancient-greece", True)
        if is_german(occ) and "germany" not in occ.get("priorities", {}):
            adds["germany"] = derive_priority(occ, "germany", True)
        if adds:
            proposed[occ["id"]] = adds

    eng_count = sum(1 for v in proposed.values() if "ancient-greece" in v)
    ger_count = sum(1 for v in proposed.values() if "germany" in v)
    print(f"Proposed: {eng_count} ancient-greece tags, {ger_count} germany tags. "
          f"{len(proposed)} entries touched.")

    # Sample
    by_id = {o["id"]: o for o in OCCURRENCES}
    grk_sample = sorted(
        [(by_id[i]["start_year"], by_id[i]["title"]) for i, v in proposed.items() if "ancient-greece" in v]
    )[:10]
    ger_sample = sorted(
        [(by_id[i]["start_year"], by_id[i]["title"]) for i, v in proposed.items() if "germany" in v]
    )[:10]
    print()
    print("Sample ancient-greece (first 10 by year):")
    for y, t in grk_sample:
        print(f"  {y:>6}  {t}")
    print()
    print("Sample germany (first 10 by year):")
    for y, t in ger_sample:
        print(f"  {y:>6}  {t}")

    # Write proposal JSON for review
    out_path = Path(__file__).parent / "proposed_greek_german_tags.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(
            {str(k): v for k, v in proposed.items()},
            f, indent=2, sort_keys=True,
        )
    print(f"\nWrote {out_path}")

    if not apply_changes:
        print("Dry run. Re-run with --apply to modify master.py.")
        return 0

    # Apply
    text = MASTER_PY.read_text(encoding="utf-8")
    id_re = re.compile(r'\{"id": (\d[\d_]*),')
    matches = list(id_re.finditer(text))
    pri_re = re.compile(r'("priorities":\s*\{)([^}]*)(\})')

    new_parts = []
    cursor = 0
    rewrites = 0
    for i, m_ in enumerate(matches):
        bid = int(m_.group(1).replace("_", ""))
        start = m_.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        new_parts.append(text[cursor:start])
        block = text[start:end]
        if bid in proposed:
            def add(pm: re.Match) -> str:
                opener, inner, closer = pm.group(1), pm.group(2).strip(), pm.group(3)
                parts = [f'"{s}": {p}' for s, p in proposed[bid].items()]
                joined = ", ".join(parts)
                inner = (inner + ", " + joined) if inner else joined
                return f"{opener}{inner}{closer}"
            new_block, n = pri_re.subn(add, block, count=1)
            if n > 0:
                rewrites += 1
                new_parts.append(new_block)
            else:
                new_parts.append(block)
        else:
            new_parts.append(block)
        cursor = end
    new_parts.append(text[cursor:])

    MASTER_PY.write_text("".join(new_parts), encoding="utf-8")
    print(f"Applied {rewrites} rewrites to master.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
