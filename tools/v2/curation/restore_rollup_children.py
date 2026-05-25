"""
Restore "X begins" / "X ends" entries that round-J dedupe deleted, in the
cases where there's a parallel PERIOD umbrella entry — making this a
legitimate rollup pattern (umbrella visible at low zoom, child point visible
at high zoom).

Source: backups/hosted_backup_20260525T151351Z.json (the pre-dedupe snapshot).

Updates each restored entry's first_zoom_out to point at the surviving
umbrella's title — that's what makes the rollup work in the renderer.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MASTER_PY = ROOT / "v2" / "data" / "master.py"
BACKUP = ROOT.parent / "backups" / "hosted_backup_20260525T151351Z.json"
sys.path.insert(0, str(ROOT))

# (deleted_id, umbrella_title_in_current_data)
# The umbrella must be a PERIOD entry — point-vs-point restoration would just
# recreate the visual duplicate.
#
# Skipped:
#   - Arab Spring begins (1_001_402): id 1_006_646 with the same title already
#     exists and already plays the rollup-child role; restoring 1_001_402
#     would create a real duplicate.
#   - Battle of Verdun begins, Battle of Tannenberg ends: their surviving
#     umbrella entries are POINTS (not periods), so restoring would recreate
#     the same-shape visual duplicate the original dedupe was meant to remove.
#     Convert the surviving entries to periods if you want the rollup back.
RESTORE_PLAN = [
    (1_000_617, "Haitian Revolution"),
    (1_001_079, "Spanish flu pandemic"),
    (1_003_008, "Tang dynasty"),
    (1_003_134, "Gupta Empire"),         # title in backup: "Gupta Empire (Indian Golden Age) begins"
    (1_003_140, "Delhi Sultanate"),
    (1_003_143, "Vijayanagara Empire"),
]


def format_entry(o: dict) -> str:
    """Render an occurrence dict to the canonical 5-line master.py format."""
    # Reconstruct the field order used in master.py. Required first, then
    # optional in their conventional positions.
    lines = ["    {"]

    def kv(key, val, last=False):
        if isinstance(val, str):
            rendered = repr(val)
        else:
            rendered = repr(val)
        sep = "" if last else ","
        return f'     "{key}": {rendered}{sep}'

    # Recreate the dict; the importer is tolerant of key order.
    # Use a simple multi-line dict with explicit field order matching master.py
    # convention.
    fields = []
    for k in (
        "id", "type", "title", "description",
        "start_year", "start_month", "start_day",
        "end_year", "end_month", "end_day",
        "key_year", "key_month", "key_day",
        "is_period", "is_ongoing", "display_date", "date_uncertain",
        "wikipedia_link", "other_link", "occurrence_type",
        "is_full_life",
        "first_zoom_out", "second_zoom_out",
        "main_category", "main_priority",
        "weight_europe", "weight_americas", "weight_asia", "weight_australasia", "weight_africa",
    ):
        if k not in o:
            continue
        v = o[k]
        if v is None:
            continue
        # Skip importer-managed / DB-computed columns.
        if k in {"main_category", "main_priority", "is_period", "first_zoom_out_id", "second_zoom_out_id"}:
            continue
        # Translate DB column names to master.py field names where they differ.
        master_key = k
        if k == "wikipedia_link":
            master_key = "wikipedia"
        if k == "other_link":
            master_key = "other_link"
        if k == "occurrence_type":
            master_key = "type"
        fields.append((master_key, v))
    # priorities + region_weights aren't in the DB row JSON — they're recoverable
    # from occurrence_timeline_priorities and weight_* columns. The backup has
    # weight_* fields; we already captured them above. Priorities are looked up
    # separately below.
    return fields


def main() -> int:
    from v2.data.master import OCCURRENCES

    backup = json.loads(BACKUP.read_text(encoding="utf-8"))
    occs = backup["tables"]["occurrences"]
    prios = backup["tables"]["occurrence_timeline_priorities"]
    timelines = backup["tables"]["timelines"]
    timeline_slug_by_id = {t["id"]: t["slug"] for t in timelines}

    backup_by_id: dict[int, dict] = {o["id"]: o for o in occs}
    # Build priorities lookup: occurrence_id -> {slug: priority}
    prios_by_occ: dict[int, dict[str, int]] = {}
    for p in prios:
        prios_by_occ.setdefault(p["occurrence_id"], {})[timeline_slug_by_id[p["timeline_id"]]] = p["priority"]

    current_ids = {o["id"] for o in OCCURRENCES}

    text = MASTER_PY.read_text(encoding="utf-8")
    restored = 0
    new_entries_to_append: list[str] = []

    for restore_id, umbrella_title in RESTORE_PLAN:
        if restore_id in current_ids:
            print(f"  SKIP: id {restore_id} already in master.py")
            continue
        row = backup_by_id.get(restore_id)
        if not row:
            print(f"  WARN: id {restore_id} not in backup; cannot restore")
            continue

        # Build the master.py dict from the DB row.
        d: dict = {
            "id": row["id"],
            "type": row.get("occurrence_type", "event"),
            "title": row["title"],
        }
        if row.get("description"):
            d["description"] = row["description"]
        d["start_year"] = row["start_year"]
        for k in ("start_month", "start_day", "end_year", "end_month", "end_day",
                  "key_year", "key_month", "key_day"):
            if row.get(k) is not None:
                d[k] = row[k]
        if row.get("is_ongoing"):
            d["is_ongoing"] = True
        if row.get("display_date"):
            d["display_date"] = row["display_date"]
        if row.get("date_uncertain"):
            d["date_uncertain"] = True
        if row.get("wikipedia_link"):
            d["wikipedia"] = row["wikipedia_link"]
        if row.get("other_link"):
            d["other_link"] = row["other_link"]
        if row.get("is_full_life"):
            d["is_full_life"] = True
        # **Force** first_zoom_out to the surviving umbrella's title — even if
        # the backup row's first_zoom_out was different. That's the whole
        # point of restoring this entry: to make it a rollup child.
        d["first_zoom_out"] = umbrella_title
        if row.get("second_zoom_out"):
            d["second_zoom_out"] = row["second_zoom_out"]

        # Priorities (recovered from junction table snapshot).
        d["priorities"] = prios_by_occ.get(restore_id, {})
        if not d["priorities"]:
            print(f"  WARN: no priorities in backup for id {restore_id}; skipping")
            continue

        # Region weights
        rw: dict[str, int] = {}
        for region in ("europe", "americas", "asia", "australasia", "africa"):
            v = row.get(f"weight_{region}")
            if v is not None:
                rw[region] = v
        if rw and any(v != 5 for v in rw.values()):
            d["region_weights"] = rw

        # Render to master.py-style entry.
        # Use the canonical compact 5-line format the existing entries use.
        new_entries_to_append.append(render_entry(d))
        restored += 1

    if not new_entries_to_append:
        print("Nothing to restore.")
        return 0

    # Append before the closing bracket of OCCURRENCES.
    # Find the last `]` that closes OCCURRENCES.
    pat = re.compile(r"^\]\s*$", re.MULTILINE)
    matches = list(pat.finditer(text))
    if not matches:
        print("ABORT: couldn't find closing `]` of OCCURRENCES in master.py")
        return 1
    last = matches[-1]
    block = "".join(new_entries_to_append)
    text = text[: last.start()] + block + text[last.start() :]
    MASTER_PY.write_text(text, encoding="utf-8")

    print(f"Restored {restored} entries to master.py")
    return 0


def render_entry(d: dict) -> str:
    """Render the dict as a Python literal master.py can import. Doesn't try
    to match the exact 5-line compact format used elsewhere — just emits a
    clean readable block with the conventional key order."""
    lines = ["    {"]
    key_order = [
        "id", "type", "title",
        "start_year", "start_month", "start_day",
        "end_year", "end_month", "end_day",
        "key_year", "key_month", "key_day",
        "is_ongoing", "is_full_life", "date_uncertain",
        "display_date",
        "description", "wikipedia", "other_link",
        "first_zoom_out", "second_zoom_out",
        "priorities", "region_weights",
    ]
    seen = set()
    for k in key_order:
        if k not in d:
            continue
        seen.add(k)
        lines.append(f'     "{k}": {d[k]!r},')
    # Catch any keys we didn't anticipate.
    for k, v in d.items():
        if k in seen:
            continue
        lines.append(f'     "{k}": {v!r},')
    lines.append("    },\n")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
