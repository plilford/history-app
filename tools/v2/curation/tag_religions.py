"""
Tag existing entries with religion slugs:
  - christianity, islam, judaism (the three Abrahamic)
  - major-religions (the union of the three above PLUS Buddhism, Hinduism,
    Sikhism, Confucianism, Taoism, Shinto, Zoroastrianism)
  - ottoman (Ottoman Empire — separate from religions but tagged similarly)

Anything tagged on christianity/islam/judaism automatically gets
major-religions too.

Per-slug priority derivation follows the convention used by recent
tagging passes:
    base = master_priority
    +30k if entry has a strong slug-anchored marker in its title
    -90k if entry also tagged on another regional slug (multi-regional)
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
                       "russia", "japan", "england", "england-monarchs",
                       "germany", "ottoman"}


# ----- CHRISTIANITY ---------------------------------------------------------
CHRISTIAN_TITLE_MARKERS = [
    r"\bchristian", r"\bchrist\b", r"\bjesus\b", r"\bgospel",
    r"\bpope\b", r"\bpapacy\b", r"\bpapal\b",
    r"\bbishop\b", r"\barchbishop\b", r"\bcardinal\b",
    r"\bcathedral\b", r"\bbasilica\b", r"\bmonast",
    r"\bvatican\b", r"\bsaint\b", r"\bst\.\b",
    r"\bcatholic", r"\bprotestant", r"\borthodox\b",
    r"\bsacrament", r"\bcrucifixion\b", r"\bresurrection\b",
    r"\bsynod\b", r"\bcouncil of nicaea\b", r"\bcouncil of\b",
    r"\binquisition\b", r"\bjesuit", r"\bdominican", r"\bfranciscan",
    r"\breformation\b", r"\bluther\b", r"\bcalvin\b", r"\bcranmer\b",
    r"\bzwingli\b", r"\btyndale\b", r"\bwycliffe\b", r"\bhuss\b",
    r"\baquinas\b", r"\baugustine\b", r"\bbenedict\b",
    r"\bfrancis of assisi\b", r"\bfrancis xavier\b",
    r"\bedict of milan\b", r"\bedict of nantes\b", r"\bnicene\b",
    r"\bcrusade\b", r"\btemplar", r"\bhospitaller",
    r"\b95 theses\b", r"\bbible\b", r"\bgenesis\b", r"\bgenesis chapter\b",
    r"\bking james (bible|version)\b", r"\bvulgate\b",
    r"\bcouncil of trent\b", r"\binvestiture\b",
    r"\bwhitby\b", r"\bcanterbury\b",  # ecclesiastical centres
    r"\bgreat schism\b", r"\b(east|west)[-–]?west schism\b",
    r"\bavignon papac\b", r"\bvatican (i|ii)\b",
    r"\bbecket\b", r"\bevangel",
]
CHRISTIAN_TITLE_RE = re.compile("|".join(CHRISTIAN_TITLE_MARKERS), re.I)

# Strict title-only set of high-priority Christian heads/figures the regex misses
CHRISTIAN_EXTRA_HINTS = {
    "saint paul", "paul the apostle", "muhammad",  # included muhammad accidentally? no.
    "thomas more", "thomas cranmer", "francis xavier",
    "ignatius of loyola", "teresa of ávila", "teresa of avila",
}

# Hard excludes for Christian — entries that match keywords but aren't really Christian-anchored
CHRISTIAN_EXCLUDES = {
    "muhammad",
    "christianisation of kievan rus'",  # this IS christianity but already tagged
}


# ----- ISLAM ----------------------------------------------------------------
ISLAMIC_TITLE_MARKERS = [
    r"\bislam", r"\bmuslim", r"\bquran\b", r"\bkoran\b",
    r"\bmuhammad\b", r"\bproph(et|et's)\b",
    r"\bcaliph", r"\bsultan", r"\bemir\b",
    r"\bumayyad", r"\babbasid", r"\bfatimid", r"\bayyubid", r"\bmamluk",
    r"\bottoman\b", r"\bseljuk\b", r"\btanzimat\b",
    r"\bhijra\b", r"\bhajj\b", r"\bmecca\b", r"\bmedina\b",
    r"\bsunni\b", r"\bshia\b", r"\bshi'?a\b", r"\bsufi\b", r"\bdervish\b",
    r"\bal-andalus\b", r"\bandalusi", r"\bmoorish\b",
    r"\bsaladin\b", r"\bbaibars\b", r"\bsuleiman\b", r"\bmehmed\b",
    r"\bibn ", r"\bal-",  # ibn / al- prefixes for Islamic figures
    r"\baverroes\b", r"\bavicenna\b", r"\bal-khwarizmi\b", r"\bibn battuta\b",
    r"\bibn khaldun\b", r"\bal-ghazali\b",
    r"\bgranada\b", r"\bcórdoba\b", r"\bcordoba\b",
    r"\bbaghdad\b", r"\bdamascus\b", r"\bistanbul\b", r"\bconstantinople\b",
    r"\bislamic golden age\b", r"\bhouse of wisdom\b",
    r"\breconquista\b", r"\bumayyad", r"\bmosque\b",
]
ISLAMIC_TITLE_RE = re.compile("|".join(ISLAMIC_TITLE_MARKERS), re.I)

ISLAMIC_EXTRA_HINTS = {
    "muhammad",
}

ISLAMIC_EXCLUDES = {
    # The "Constantinople" entries are mostly Christian/Byzantine — only the
    # 1453 fall and post is Islamic. Filter by year.
    "siege of constantinople (674-678)",
    "siege of constantinople (717-718)",
    "founding of constantinople",
    "sack of constantinople by fourth crusade",
    "byzantine recovery of constantinople",
    "great schism",
    "fourth crusade sacks constantinople",
}


# ----- JUDAISM --------------------------------------------------------------
JEWISH_TITLE_MARKERS = [
    r"\bjewish\b", r"\bjewry\b", r"\bjews?\b", r"\bjudaism\b",
    r"\bhebrew", r"\bisrael\b", r"\bisraeli", r"\bjerusalem\b",
    r"\bzion", r"\bzionis",
    r"\btorah\b", r"\btalmud\b", r"\bmishnah\b",
    r"\brabb[iy]\b", r"\bsynagogue\b",
    r"\bpassover\b", r"\bhanukkah\b", r"\bpurim\b",
    r"\bsecond temple\b", r"\bfirst temple\b",
    r"\btemple of solomon\b", r"\bdestruction of the .*temple\b",
    r"\babraham\b", r"\bmoses\b", r"\bdavid\b", r"\bsolomon\b",
    r"\bmaccabe", r"\bsamaritan\b", r"\bpharisee\b",
    r"\bbabylonian captivity\b", r"\bexodus\b",
    r"\bdiaspora\b", r"\bsephard", r"\bashkenaz", r"\byiddish\b",
    r"\bholocaust\b", r"\bshoah\b", r"\bauschwitz\b", r"\btreblinka\b",
    r"\bsobib\b", r"\bdachau\b", r"\bbabi yar\b",
    r"\bkristallnacht\b", r"\bnuremberg race laws\b",
    r"\bwannsee\b", r"\banne frank\b",
    r"\bbalfour declaration\b", r"\bspanish expulsion\b",
    r"\balhambra decree\b",
    r"\bsix-day war\b", r"\byom kippur war\b",
    r"\bcamp david\b", r"\bintifada\b", r"\bgaza\b",
    r"\bzionist congress\b", r"\bdreyfus\b",
]
JEWISH_TITLE_RE = re.compile("|".join(JEWISH_TITLE_MARKERS), re.I)

JEWISH_EXTRA_HINTS = {
    "founding of israel",
}

JEWISH_EXCLUDES = set()


# ----- OTHER MAJOR RELIGIONS (Buddhism/Hinduism/Sikhism/etc.) ---------------
# Anything matching these also gets tagged major-religions (but not the three Abrahamic slugs).
OTHER_RELIGION_MARKERS = [
    r"\bbuddh", r"\bzen\b", r"\bnirvana\b", r"\bdharma\b",
    r"\bsiddhartha\b", r"\bdalai lama\b", r"\bvajrayana\b",
    r"\bhindu", r"\bsanskrit\b", r"\bveda\b", r"\bvedic\b",
    r"\bupanishad", r"\bbhagavad gita\b", r"\bmahabharata\b", r"\bramayana\b",
    r"\bsikh", r"\bguru nanak\b",
    r"\bconfuci", r"\bmencius\b", r"\banalects\b",
    r"\btao\b", r"\btaoism\b", r"\bdaois", r"\blaozi\b", r"\blao tzu\b",
    r"\bshinto\b", r"\bzoroastr", r"\bahura mazda\b",
    r"\bjain", r"\bmaha?vira\b",
    r"\bbaha'i\b", r"\bbahai\b",
]
OTHER_RELIGION_RE = re.compile("|".join(OTHER_RELIGION_MARKERS), re.I)


# ----- OTTOMAN --------------------------------------------------------------
OTTOMAN_TITLE_MARKERS = [
    r"\bottoman\b", r"\bsublime porte\b",
    r"\bjanissar", r"\btopkapi\b",
    r"\bmehmed (ii|iii|iv|v|the conqueror)\b", r"\bbayezid\b",
    r"\bselim\b", r"\bsuleiman\b", r"\bsuleyman\b",
    r"\babdul[- ]?hamid\b", r"\babdulhamid\b",
    r"\btanzimat\b", r"\byoung turks?\b",
    r"\bgallipoli\b", r"\barmenian genocide\b",
    r"\batat[uü]rk\b", r"\btreaty of sèvres\b",
    r"\bblue mosque\b", r"\bbattle of mohács\b",
]
OTTOMAN_TITLE_RE = re.compile("|".join(OTTOMAN_TITLE_MARKERS), re.I)


def _is_ottoman_era(occ: dict) -> bool:
    """Ottoman empire ran 1299-1922. Anything outside that window matched on
    weak keywords is almost certainly a false positive."""
    y = occ.get("start_year")
    if y is None: return True
    return 1200 <= y <= 1950


OTTOMAN_EXCLUDES = {
    "fall of constantinople",  # already Roman-history primary
    "francis of assisi meets sultan al-kamil",
}


# ----- Classification helpers -----------------------------------------------
def matches(occ: dict, regex: re.Pattern, hints: set[str], excludes: set[str]) -> bool:
    title_raw = occ.get("title") or ""
    title = title_raw.strip().lower()
    if title in excludes:
        return False
    if title in hints:
        return True
    return bool(regex.search(title_raw))


def derive_priority(occ: dict, strong: bool) -> int:
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
        slugs = set(occ.get("priorities", {}).keys())
        adds: dict[str, int] = {}

        is_christian = matches(occ, CHRISTIAN_TITLE_RE, CHRISTIAN_EXTRA_HINTS, CHRISTIAN_EXCLUDES)
        is_islamic = matches(occ, ISLAMIC_TITLE_RE, ISLAMIC_EXTRA_HINTS, ISLAMIC_EXCLUDES)
        is_jewish = matches(occ, JEWISH_TITLE_RE, JEWISH_EXTRA_HINTS, JEWISH_EXCLUDES)
        is_other_religion = bool(OTHER_RELIGION_RE.search(occ.get("title") or ""))
        is_ottoman = matches(occ, OTTOMAN_TITLE_RE, set(), OTTOMAN_EXCLUDES) and _is_ottoman_era(occ)

        if is_christian and "christianity" not in slugs:
            adds["christianity"] = derive_priority(occ, True)
        if is_islamic and "islam" not in slugs:
            adds["islam"] = derive_priority(occ, True)
        if is_jewish and "judaism" not in slugs:
            adds["judaism"] = derive_priority(occ, True)
        if is_ottoman and "ottoman" not in slugs:
            adds["ottoman"] = derive_priority(occ, True)

        # Anything in any religion (Abrahamic or other) → major-religions too
        if (is_christian or is_islamic or is_jewish or is_other_religion) and "major-religions" not in slugs:
            adds["major-religions"] = derive_priority(occ, True)

        if adds:
            proposed[occ["id"]] = adds

    # Summarise
    counts = {"christianity": 0, "islam": 0, "judaism": 0, "major-religions": 0, "ottoman": 0}
    for v in proposed.values():
        for slug in v:
            counts[slug] = counts.get(slug, 0) + 1
    print(f"Proposed tags:")
    for slug, n in counts.items():
        print(f"  {slug:<20}: {n}")
    print(f"  entries touched   : {len(proposed)}")

    # Spot-check by sampling earliest entries per slug
    by_id = {o["id"]: o for o in OCCURRENCES}
    for slug in ("christianity", "islam", "judaism", "ottoman"):
        sample = sorted(
            [(by_id[i]["start_year"], by_id[i]["title"]) for i, v in proposed.items() if slug in v]
        )[:8]
        print(f"\n  Sample {slug} (first 8 by year):")
        for y, t in sample:
            print(f"    {y:>6}  {t}")

    out_path = Path(__file__).parent / "proposed_religion_tags.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in proposed.items()}, f, indent=2, sort_keys=True)
    print(f"\nWrote {out_path}")

    if not apply_changes:
        print("Dry run. Re-run with --apply to modify master.py.")
        return 0

    # Apply
    text = MASTER_PY.read_text(encoding="utf-8")
    id_re = re.compile(r'\{"id": (\d[\d_]*),')
    matches_iter = list(id_re.finditer(text))
    pri_re = re.compile(r'("priorities":\s*\{)([^}]*)(\})')

    new_parts: list[str] = []
    cursor = 0
    rewrites = 0
    for i, m_ in enumerate(matches_iter):
        bid = int(m_.group(1).replace("_", ""))
        start = m_.start()
        end = matches_iter[i + 1].start() if i + 1 < len(matches_iter) else len(text)
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
