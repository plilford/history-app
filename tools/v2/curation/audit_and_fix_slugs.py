"""
Audit + fix slug-tagging gaps across the dataset.

Fixes applied automatically (mechanical, high-confidence):
  1. Anything on christianity/islam/judaism but missing major-religions
     → add major-religions
  2. type=person + is_full_life=True missing 'people' slug
     → add people (priority = master + 30k if not already on people)
  3. type=art missing 'arts-and-thoughts' slug
     → add arts-and-thoughts
  4. Title keyword matches for WW1 / WW2 / Cold War missing those slugs
     → add the slug

Other gaps reported but NOT auto-fixed (false-positive risk too high):
  5. Likely Christian/Islamic content missing the slug — needs manual
     curation, listed for review.
  6. Likely US content missing usa slug — same.

Usage:
    python -m v2.curation.audit_and_fix_slugs           # dry run + report
    python -m v2.curation.audit_and_fix_slugs --apply   # apply mechanical fixes
"""
from __future__ import annotations

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


def derive_priority(occ: dict, *, boost: bool = True) -> int:
    master = occ.get("priorities", {}).get("master", 800_000)
    other_regional = COMPETING_REGIONAL & set(occ.get("priorities", {}).keys())
    base = master
    if boost:
        base = min(999_000, base + 30_000)
    if other_regional:
        base = max(400_000, base - 90_000)
    return base


def audit() -> dict[int, dict[str, int]]:
    """Return {entry_id: {slug: priority}} of mechanical adds."""
    adds: dict[int, dict[str, int]] = {}

    for occ in OCCURRENCES:
        pri = occ.get("priorities", {})
        # 1. Missing major-religions
        if ("christianity" in pri or "islam" in pri or "judaism" in pri) and "major-religions" not in pri:
            adds.setdefault(occ["id"], {})["major-religions"] = derive_priority(occ)

        # 2. Person full-life missing people
        if occ.get("type") == "person" and occ.get("is_full_life") and "people" not in pri:
            # People slug uses a slightly different convention — preserve
            # the existing behaviour: typically master + 30k.
            adds.setdefault(occ["id"], {})["people"] = derive_priority(occ)

        # 3. Art missing arts-and-thoughts
        if occ.get("type") == "art" and "arts-and-thoughts" not in pri:
            adds.setdefault(occ["id"], {})["arts-and-thoughts"] = derive_priority(occ)

        # 4. WW1/WW2/Cold War clear-title matches
        title = (occ.get("title") or "")
        ww1_pat = re.compile(r"\b(world war i\b|wwi\b|first world war|great war\b)", re.I)
        ww2_pat = re.compile(r"\b(world war ii\b|wwii\b|second world war|the holocaust\b|stalingrad|d-day|kursk|barbarossa|nazi\b|hitler\b|midway\b|guadalcanal|leningrad|iwo jima|operation overlord)\b", re.I)
        cw_pat = re.compile(r"\b(cold war\b|berlin wall\b|cuban missile|warsaw pact|nato\b|sputnik\b|iron curtain|space race\b)", re.I)

        if "ww1" not in pri and ww1_pat.search(title) and "ww2" not in pri:
            adds.setdefault(occ["id"], {})["ww1"] = derive_priority(occ)
        if "ww2" not in pri and ww2_pat.search(title):
            adds.setdefault(occ["id"], {})["ww2"] = derive_priority(occ)
        if "cold-war" not in pri and cw_pat.search(title):
            adds.setdefault(occ["id"], {})["cold-war"] = derive_priority(occ)

    return adds


# ----- Soft audit (report only) ---------------------------------------------
def soft_audit() -> None:
    """Report potential gaps that need manual curation, not auto-fix."""
    by_id = {o["id"]: o for o in OCCURRENCES}

    # Christian content not on christianity slug
    chr_pat = re.compile(r"\b(christian|catholic|protestant|orthodox|bishop|monastery|abbey|monk|nun|priest|pope\b|pontiff|crusade|reformation|gospel|apostle|saint|jesus|church|cathedral|martyr|pilgrim|inquisition|jesuit|dominican|franciscan)\b", re.I)
    miss_chr = []
    for o in OCCURRENCES:
        if "christianity" in o.get("priorities", {}):
            continue
        text = (o.get("title") or "") + " " + (o.get("description") or "")
        if chr_pat.search(text):
            y = o.get("start_year")
            if y is None or y < 0:
                continue
            miss_chr.append(o)

    isl_pat = re.compile(r"\b(islam|muslim|caliph|sultan|mosque|quran|sufi|fatimid|abbasid|umayyad|seljuk|mamluk|hajj|mecca|medina|sharia)\b", re.I)
    miss_isl = []
    for o in OCCURRENCES:
        if "islam" in o.get("priorities", {}):
            continue
        text = (o.get("title") or "") + " " + (o.get("description") or "")
        y = o.get("start_year")
        if y is None or y < 500:
            continue
        if isl_pat.search(text):
            miss_isl.append(o)

    print(f"\nSOFT AUDIT (review-only — high false-positive risk):")
    print(f"  Christian-keyword entries missing christianity slug: {len(miss_chr)}")
    for o in miss_chr[:5]:
        print(f"     {o['id']} {o['start_year']:>6} {o['title']}")
    print(f"  ...")
    print(f"  Islamic-keyword entries missing islam slug: {len(miss_isl)}")
    for o in miss_isl[:5]:
        print(f"     {o['id']} {o['start_year']:>6} {o['title']}")


def apply_adds(adds: dict[int, dict[str, int]]) -> int:
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
        if bid in adds:
            def add(pm: re.Match, _adds=adds[bid]) -> str:
                opener, inner, closer = pm.group(1), pm.group(2).strip(), pm.group(3)
                parts = [f'"{s}": {p}' for s, p in _adds.items()]
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
    return rewrites


def main() -> int:
    apply = "--apply" in sys.argv
    adds = audit()

    # Summarise
    by_slug: dict[str, int] = {}
    for v in adds.values():
        for slug in v:
            by_slug[slug] = by_slug.get(slug, 0) + 1
    print(f"HARD AUDIT (auto-fix candidates):")
    for slug, n in by_slug.items():
        print(f"  {slug:<20}: +{n}")
    print(f"  total entries touched: {len(adds)}")

    soft_audit()

    if not apply:
        print("\nDry run. Re-run with --apply to apply mechanical fixes.")
        return 0

    n = apply_adds(adds)
    print(f"\nApplied {n} entries with slug additions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
