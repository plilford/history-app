"""
Diagnostic: list post-1500 entries that are year-only point events (no
start_month, no start_day) where adding month/day precision would improve
the rendering. Excludes periods (entries with end_year) and ongoing entries.

Output is grouped: easy hits (treaties / battles / specific named acts
where the date is universally known) first, then everything else.

Usage:
    cd tools
    python -m v2.curation.list_precision_candidates [--all]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from v2.data.master import OCCURRENCES  # noqa: E402


# Title patterns that almost always have a known precise date.
EASY_KEYWORDS = [
    r"\bbattle\b", r"\btreaty\b", r"\bact of\b", r"\bact\b",
    r"\bdeclaration\b", r"\bassassinat", r"\bsigned\b", r"\bcoronation\b",
    r"\bbegins\b", r"\bends\b", r"\bproclaims?\b", r"\bopens\b", r"\bcompleted\b",
    r"\bcrowned\b", r"\bexecut", r"\blaunched\b", r"\bnominated\b", r"\binaug",
    r"\baccession\b", r"\b(?:first|maiden) flight\b",
]
easy_re = re.compile("|".join(EASY_KEYWORDS), re.IGNORECASE)


def candidate_filter(o: dict) -> bool:
    if "start_month" in o or "start_day" in o:
        return False
    if o.get("start_year", 0) < 1500:
        return False
    if "end_year" in o:  # periods: less critical
        return False
    if o.get("is_ongoing"):
        return False
    if o.get("date_uncertain"):  # author flagged it
        return False
    return True


def main() -> int:
    show_all = "--all" in sys.argv
    cands = [o for o in OCCURRENCES if candidate_filter(o)]
    print(f"{len(cands)} post-1500 year-only point entries (excluding periods,"
          f" ongoing, date_uncertain)")

    easy = [o for o in cands if easy_re.search(o.get("title", ""))]
    other = [o for o in cands if not easy_re.search(o.get("title", ""))]
    print(f"  Easy hits (title contains battle/treaty/act/...): {len(easy)}")
    print(f"  Other:                                            {len(other)}")
    print()

    def show(group, label, limit):
        print(f"--- {label} ---")
        # Sort by start_year desc to show modern first (likely more knowable)
        for o in sorted(group, key=lambda x: -x["start_year"])[:limit]:
            print(f"  {o['id']}  {o['start_year']:5d}  {o['title']}")
        if len(group) > limit:
            print(f"  ... ({len(group) - limit} more — pass --all to see them all)")
        print()

    if show_all:
        show(easy, "Easy hits (sorted newest first)", len(easy))
        show(other, "Other candidates (sorted newest first)", len(other))
    else:
        show(easy, "Easy hits — first 60 (sorted newest first)", 60)
        show(other, "Other candidates — first 30 (sorted newest first)", 30)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
