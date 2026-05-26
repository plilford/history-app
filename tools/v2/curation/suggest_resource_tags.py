"""
Suggest resource_tag candidates for newly-added master.py entries.

Use case: after appending new occurrences to master.py, run this to find
existing resources (podcast episodes, books) whose title/description
mentions the new subject. Those resources should be tagged to the new
subject so the popup's 📚 badge counts them and the resource timelines
render them when the new subject is in view.

Usage:
    cd tools
    python -m v2.curation.suggest_resource_tags             # all new-ish entries
    python -m v2.curation.suggest_resource_tags --since 1_007_000

Output: prints a checklist for each new entry, listing resource titles
whose pool text contains a word-bounded match for the new entry's title.
Manual review needed — substring matches can be false positives (e.g.
"Henry II" matches every Henry book). The author then edits the relevant
resource entries to add the new subject to their `tags` list.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from v2.import_v2 import collect_all_occurrences


def matches_resource(subject_title: str, resource: dict) -> bool:
    """Word-bounded substring match of subject title in resource's title +
    description. Conservative — avoids over-matching common words."""
    if len(subject_title) < 6:
        return False  # too short, would over-match
    pool = " ".join([
        resource.get("title") or "",
        resource.get("description") or "",
    ]).lower()
    pat = re.compile(rf"\b{re.escape(subject_title.lower())}\b")
    return bool(pat.search(pool))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--since",
        type=lambda s: int(s.replace("_", "")),
        default=1_007_000,
        help="Min id of new entries to consider (default 1_007_000)",
    )
    args = p.parse_args()

    occurrences = collect_all_occurrences()
    resources = [o for o in occurrences if o.get("type") == "resource"]
    new_subjects = [
        o for o in occurrences
        if o.get("type") != "resource" and (o.get("id") or 0) >= args.since
    ]
    print(f"Resources scanned: {len(resources)}")
    print(f"New subjects checked (id >= {args.since:_}): {len(new_subjects)}")
    print()

    suggestions: list[tuple[str, list[str]]] = []
    for sub in new_subjects:
        title = sub.get("title") or ""
        matches = [r for r in resources if matches_resource(title, r)]
        # Skip cases where the resource already has this exact tag (in its
        # `tags` list). The data file is the source of truth — if the tag
        # is there, we don't need to suggest it.
        novel = []
        for r in matches:
            tags = [t.strip().lower() for t in (r.get("tags") or [])]
            if title.lower() in tags:
                continue
            novel.append(r["title"])
        if novel:
            suggestions.append((title, novel))

    if not suggestions:
        print("No suggestions — every matching resource already has the tag.")
        return 0

    print(f"Suggestions ({len(suggestions)} subjects):\n")
    for title, resource_titles in suggestions:
        print(f"## {title}")
        for rt in resource_titles[:10]:
            print(f"  - {rt}")
        if len(resource_titles) > 10:
            print(f"  ...and {len(resource_titles) - 10} more")
        print()
    print("Manual step: open each resource's data module, add the subject")
    print("title to its `tags` list, then run validate.py + import_v2.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
