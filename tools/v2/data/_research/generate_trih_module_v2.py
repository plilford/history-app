"""
Render trih_curated_draft_v2.json -> tools/v2/data/the_rest_is_history.py.

v2 generator: handles all 672 numbered TRIH episodes. The v2 curator already
applies manual_curations.OVERRIDES and tag-validates against master.py, so
this generator just needs to read the draft and render the module.

ID range: 1_008_000 + index. Reserved for TRIH module.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[2]
sys.path.insert(0, str(TOOLS))

DRAFT = HERE / "trih_curated_draft_v2.json"
OUT_MODULE = HERE.parent / "the_rest_is_history.py"

START_ID = 1_008_000


def repr_value(v):
    if isinstance(v, str):
        return repr(v)
    if isinstance(v, list):
        return "[" + ", ".join(repr_value(x) for x in v) + "]"
    if isinstance(v, dict):
        return "{" + ", ".join(f"{repr_value(k)}: {repr_value(val)}" for k, val in v.items()) + "}"
    return repr(v)


def render_entry(d: dict, eid: int) -> str:
    title = d["resource_title"]
    start_year = d["subject_start"]
    end_year = d["subject_end"]
    desc = d["description"]
    if len(desc) > 500:
        desc = desc[:497].rstrip() + "..."
    ep_payload = d["resource_episodes"]
    is_series = len(ep_payload) > 1

    lines = ["    {"]
    lines.append(f'     "id": {eid:_},')
    lines.append(f'     "type": "resource",')
    lines.append(f'     "subtype": "podcast-episode",')
    lines.append(f'     "title": {repr_value(title)},')
    lines.append(f'     "start_year": {start_year},')
    if end_year is not None:
        lines.append(f'     "end_year": {end_year},')
    if desc:
        lines.append(f'     "description": {repr_value(desc)},')
    lines.append(f'     "resource_link": {repr_value(ep_payload[0]["url"])},')
    if is_series:
        lines.append(f'     "resource_episodes": {repr_value(ep_payload)},')
    lines.append(f'     "priorities": {{"the-rest-is-history-podcast": 900000}},')
    tags = d["candidate_tags"]
    if tags:
        lines.append(f'     "tags": {repr_value(tags)},')
    lines.append("    },")
    return "\n".join(lines)


def main() -> int:
    drafts = json.loads(DRAFT.read_text(encoding="utf-8"))
    print(f"Loaded {len(drafts)} drafts")

    importable = [d for d in drafts if not d.get("_skip") and d.get("subject_start") is not None]
    skipped = [d for d in drafts if d.get("_skip") or d.get("subject_start") is None]
    print(f"Importable: {len(importable)}, skipped: {len(skipped)}")

    importable.sort(key=lambda d: (d["subject_start"], d["ep_nums"][0]))

    header = r'''"""
The Rest Is History podcast — auto-generated resource entries.

Built from a join of the Megaphone RSS feed (episode numbers + air dates) and
the fan-maintained archive at archive.therestishistory.com (per-episode
`historical_events`, `historical_figures`, `books` lists). Multi-part series
are grouped into a single resource entry; tags are resolved against master.py
titles with date-proximity filtering to keep cross-references tight.

Re-generate by running, from `tools/`:

    .venv\\Scripts\\python.exe -m v2.data._research.parse_trih_rss
    .venv\\Scripts\\python.exe -m v2.data._research.fetch_trih_archive
    .venv\\Scripts\\python.exe -m v2.data._research.curate_trih_v2
    .venv\\Scripts\\python.exe -m v2.data._research.generate_trih_module_v2

Then validate + import:

    .venv\\Scripts\\python.exe -m v2.validate
    .venv\\Scripts\\python.exe -m v2.import_v2

Per-item manual overrides (for eps 1-300, hand-curated previously) live in
manual_curations.py. ID range reserved for TRIH: 1_008_000 - 1_008_999.
"""

from __future__ import annotations

OCCURRENCES: list[dict] = [
'''

    blocks = [render_entry(d, START_ID + i) for i, d in enumerate(importable)]
    body = "\n".join(blocks)
    footer = "\n]\n"

    OUT_MODULE.write_text(header + body + footer, encoding="utf-8")
    print(f"\nWrote {OUT_MODULE} with {len(importable)} entries "
          f"(ids {START_ID}..{START_ID + len(importable) - 1})")
    print(f"Skipped {len(skipped)} items (thematic / undatable):")
    for d in skipped[:30]:
        ep_label = d["ep_nums"][0] if d["ep_nums"] else "?"
        print(f"  ep {ep_label:>3}: {d['resource_title']}")
    if len(skipped) > 30:
        print(f"  ... and {len(skipped) - 30} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
