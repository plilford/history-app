"""
Shared helper for emitting new occurrence entries in master.py's canonical
5-line dict style, and appending them to master.py just before the closing
`]` of the OCCURRENCES list.

Usage in a sibling script:
    from v2.curation.append_entries import append_entries
    append_entries(NEW_ENTRIES)

Each entry in NEW_ENTRIES is a plain dict with the same keys we put in
master.py. The helper formats it and appends in one transactional write.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MASTER_PY = ROOT / "v2" / "data" / "master.py"

# Field-emission order matches existing entries.
FIELD_ORDER = [
    "id", "type", "title", "description",
    "start_year", "start_month", "start_day",
    "end_year", "end_month", "end_day",
    "key_month", "key_day",
    "is_period", "is_full_life", "is_ongoing",
    "date_uncertain", "display_date",
    "first_zoom_out", "second_zoom_out",
    "wikipedia",
    "priorities", "region_weights",
]


def _emit_value(v):
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, str):
        if "'" in v and '"' not in v:
            return f'"{v}"'
        if '"' in v and "'" not in v:
            return f"'{v}'"
        # Default to single quotes (matches majority style for descriptions)
        if "'" in v:
            # has both — fall back to double-quoting and escape
            esc = v.replace('"', '\\"')
            return f'"{esc}"'
        return f"'{v}'"
    if isinstance(v, int):
        if abs(v) >= 1_000_000 and v >= 0:
            # IDs use 1_000_000 style
            s = f"{v:_}"
            return s
        if v >= 100_000:
            return f"{v}"
        return f"{v}"
    if isinstance(v, dict):
        parts = []
        for k, val in v.items():
            if isinstance(val, int):
                parts.append(f'"{k}": {val}')
            else:
                parts.append(f'"{k}": {_emit_value(val)}')
        return "{" + ", ".join(parts) + "}"
    raise TypeError(f"cannot emit value of type {type(v).__name__}: {v!r}")


def format_entry(entry: dict) -> str:
    """Format a single occurrence dict in the canonical multi-line style.

    First line opens with `{"id": N,` and each subsequent field is on its own
    line, indented 5 spaces (matching existing entries). The final field's
    line ends with `}},` (closing the dict).
    """
    lines: list[str] = []
    fields = [(k, entry[k]) for k in FIELD_ORDER if k in entry]
    if not fields:
        raise ValueError(f"empty entry: {entry!r}")

    # Track unknown keys
    known = set(FIELD_ORDER)
    extra = [k for k in entry if k not in known]
    if extra:
        raise ValueError(f"entry has unknown keys {extra}: {entry!r}")

    for i, (k, v) in enumerate(fields):
        rendered = _emit_value(v)
        if i == 0:
            assert k == "id", "first field must be id"
            lines.append(f'    {{"{k}": {rendered},')
        elif i == len(fields) - 1:
            lines.append(f'     "{k}": {rendered}}},')
        else:
            lines.append(f'     "{k}": {rendered},')
    return "\n".join(lines)


def append_entries(entries: list[dict]) -> int:
    """Append a batch of entries to master.py just before the closing `]`."""
    if not entries:
        return 0
    text = MASTER_PY.read_text(encoding="utf-8")

    # Locate the final `]` that closes OCCURRENCES.
    # The file ends with `    ...}},\n]\n` (with optional trailing whitespace).
    m = re.search(r"\n\]\s*\Z", text)
    if not m:
        raise RuntimeError("could not locate closing `]` of OCCURRENCES list")

    insertion_point = m.start()
    rendered = "\n".join(format_entry(e) for e in entries)
    new_text = text[:insertion_point] + "\n" + rendered + text[insertion_point:]

    MASTER_PY.write_text(new_text, encoding="utf-8")
    return len(entries)


def next_available_id() -> int:
    """Return the next ID greater than the current max id in master.py."""
    import sys
    sys.path.insert(0, str(ROOT))
    # Re-import fresh (clear cache)
    import importlib
    from v2.data import master as m
    importlib.reload(m)
    return max(o["id"] for o in m.OCCURRENCES) + 1
