"""
Add the new round-K subject titles to existing resources' `tags` lists,
based on the suggest_resource_tags output.

A regex/brace-counting parser over the resource module is too fragile
because the entries contain nested dicts (resource_episodes). This script
takes a safer route: import the module, mutate its OCCURRENCES list in
memory, then re-serialise back to disk preserving the entries' original
text layout via a line-level patch — locate each entry's `}` closing line
by counting indentation depth on a per-line basis.

Run from `tools/`:
    .venv\\Scripts\\python.exe -m v2.curation.add_round_k_tags
    .venv\\Scripts\\python.exe -m v2.validate
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRIH_PY = ROOT / "v2" / "data" / "the_rest_is_history.py"
BOOKS_PY = ROOT / "v2" / "data" / "popular_history_books.py"

# (module_path, resource_id, [tags_to_add])
EDITS: list[tuple[Path, int, list[str]]] = [
    # TRIH ----------------------------------------------------------------
    (TRIH_PY, 1008313, ["Richard Nixon"]),                       # Watergate (eps 106-107)
    (TRIH_PY, 1008233, ["Lyndon B. Johnson"]),                   # Oil: Conflict (ep 168)
    (TRIH_PY, 1008173, ["Richard Nixon"]),                       # History's Greatest Dogs (ep 323)
    (TRIH_PY, 1008197, ["Hadrian"]),                             # Hadrian and Antinous (ep 340)
    (TRIH_PY, 1008111, ["Catherine of Aragon", "Jane Seymour",
                        "Catherine Howard", "Catherine Parr",
                        "Mary Boleyn"]),                         # Six Wives of Henry VIII (ep 74)
    (TRIH_PY, 1008168, ["Catherine Howard"]),                    # Historical Love Island: The Sequel (ep 357)
    (TRIH_PY, 1008296, ["Konrad Adenauer"]),                     # Adenauer to Angela (ep 102)
    # Books ---------------------------------------------------------------
    (BOOKS_PY, 1009221, ["John Adams"]),                         # John Adams (McCullough)
    (BOOKS_PY, 1009105, ["Alexander Hamilton"]),                 # Alexander Hamilton (Chernow)
    (BOOKS_PY, 1009286, ["Ulysses S. Grant"]),                   # Memoirs (Grant)
    (BOOKS_PY, 1009501, ["Hadrian"]),                            # Memoirs of Hadrian (Yourcenar)
    (BOOKS_PY, 1009555, ["Mary Boleyn"]),                        # The Other Boleyn Girl (Gregory)
    (BOOKS_PY, 1009290, ["Battle of Mogadishu"]),                # Black Hawk Down (Bowden)
    (BOOKS_PY, 1009678, ["Siege of Sarajevo"]),                  # Sarajevo Marlboro (Jergović)
]

# Each entry in these modules starts with a line containing `"id": N_NNN_NNN,`
# and the dict's closing `},` is indented FOUR spaces (the entry-level indent).
# Nested dicts (e.g. inside resource_episodes lists) close at deeper indents.
ENTRY_ID_LINE_RE = re.compile(r'^\s+\{?"id":\s*([\d_]+),')
ENTRY_CLOSE_RE = re.compile(r'^    \},\s*$')
TAGS_LINE_RE = re.compile(r'^(\s+)"tags":\s*\[(.*)\],?\s*$')


def find_entry_range(lines: list[str], eid: int) -> tuple[int, int] | None:
    """Return (start_line_idx, close_line_idx_inclusive) for the entry whose
    id is `eid`. close_line_idx is the line containing `    },` that ends
    the entry at the 4-space indent level."""
    target = f"{eid:_}"
    start = None
    for i, line in enumerate(lines):
        m = ENTRY_ID_LINE_RE.match(line)
        if m and m.group(1) == target:
            start = i
            break
    if start is None:
        return None
    # Walk forward to find the entry's closing `    },`
    for j in range(start + 1, len(lines)):
        if ENTRY_CLOSE_RE.match(lines[j]):
            return start, j
    return None


def find_tags_line(lines: list[str], start: int, end: int) -> int | None:
    """Find a `"tags": [...]` line at entry-level indent (5 spaces) within
    [start, end]. Skips deeper-indented tags inside nested dicts."""
    for i in range(start, end + 1):
        m = TAGS_LINE_RE.match(lines[i])
        if m and len(m.group(1)) == 5:
            return i
    return None


def parse_existing_tag_list(s: str) -> list[str]:
    out: list[str] = []
    for tok in re.findall(r"'([^']*)'|\"([^\"]*)\"", s):
        out.append(tok[0] or tok[1])
    return out


def patch_books_file(path: Path, edits_for_file: list[tuple[int, list[str]]]) -> int:
    """popular_history_books.py uses a compact format with entries roughly
    one block apiece, terminated by `"tags": [...]},` on a single line.
    Find each entry's tags line by regex and append."""
    text = path.read_text(encoding="utf-8")
    changes = 0
    for eid, new_tags in edits_for_file:
        # Match the entire entry block from its `"id": <eid>,` to the
        # entry-terminating `]},` that ends the tags list.
        entry_re = re.compile(
            rf'(\{{"id":\s*{eid:_},(?:[^\n]|\n     [^\n]*)*?"tags":\s*\[)([^\]]*)(\]\}},)',
            re.DOTALL,
        )
        m = entry_re.search(text)
        if not m:
            print(f"  WARN: id={eid} not found in {path.name}")
            continue
        existing = parse_existing_tag_list(m.group(2))
        existing_norm = {t.strip().lower() for t in existing}
        additions = [t for t in new_tags if t.strip().lower() not in existing_norm]
        if not additions:
            print(f"  id={eid} in {path.name}: all suggested tags already present, skipping")
            continue
        combined = existing + additions
        new_inner = ", ".join(repr(t) for t in combined)
        text = text[:m.start()] + m.group(1) + new_inner + m.group(3) + text[m.end():]
        changes += 1
        print(f"  id={eid} in {path.name}: appended {additions}")
    path.write_text(text, encoding="utf-8")
    return changes


def patch_file(path: Path, edits_for_file: list[tuple[int, list[str]]]) -> int:
    lines = path.read_text(encoding="utf-8").split("\n")
    changes = 0
    # Apply edits from bottom up so insertions don't shift later indices.
    edits_with_ranges: list[tuple[int, list[str], tuple[int, int]]] = []
    for eid, new_tags in edits_for_file:
        rng = find_entry_range(lines, eid)
        if rng is None:
            print(f"  WARN: id={eid} not found in {path.name}")
            continue
        edits_with_ranges.append((eid, new_tags, rng))
    # Sort by entry start descending so bottom-up patches don't invalidate
    # earlier indices.
    edits_with_ranges.sort(key=lambda x: -x[2][0])

    for eid, new_tags, (start, end) in edits_with_ranges:
        tags_line_idx = find_tags_line(lines, start, end)
        if tags_line_idx is not None:
            m = TAGS_LINE_RE.match(lines[tags_line_idx])
            assert m
            existing = parse_existing_tag_list(m.group(2))
            existing_norm = {t.strip().lower() for t in existing}
            additions = [t for t in new_tags if t.strip().lower() not in existing_norm]
            if not additions:
                print(f"  id={eid} in {path.name}: all suggested tags already present, skipping")
                continue
            combined = existing + additions
            new_inner = ", ".join(repr(t) for t in combined)
            trailing_comma = "," if lines[tags_line_idx].rstrip().endswith(",") else ""
            lines[tags_line_idx] = f'     "tags": [{new_inner}]{trailing_comma}'
            print(f"  id={eid} in {path.name}: appended {additions}")
        else:
            # Insert a new tags line just before the entry's closing `    },`.
            # The line preceding `    },` may need its trailing comma added if
            # missing. The generator's emitted format always leaves a trailing
            # comma on the last field, so we just splice in our tags line.
            new_inner = ", ".join(repr(t) for t in new_tags)
            new_line = f'     "tags": [{new_inner}],'
            # Ensure the previous line (last field) ends with a comma.
            prev_line = lines[end - 1]
            if not prev_line.rstrip().endswith(","):
                lines[end - 1] = prev_line.rstrip() + ","
            lines.insert(end, new_line)
            print(f"  id={eid} in {path.name}: inserted new tags line {new_tags}")
        changes += 1

    path.write_text("\n".join(lines), encoding="utf-8")
    return changes


def main() -> int:
    by_file: dict[Path, list[tuple[int, list[str]]]] = {}
    for path, eid, tags in EDITS:
        by_file.setdefault(path, []).append((eid, tags))

    total = 0
    for path, edits in by_file.items():
        print(f"\n{path.name}:")
        if path == BOOKS_PY:
            total += patch_books_file(path, edits)
        else:
            total += patch_file(path, edits)
    print(f"\nTotal entries updated: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
