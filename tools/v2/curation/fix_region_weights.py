"""
Apply proper region_weights bias to occurrences that have a clear regional
slug (england, china, usa, etc.) but currently have either:
  - no region_weights at all, or
  - region_weights with all values equal (typically all-5 — the "neutral
    placeholder" that earlier passes wrote).

Such entries get colour-coded grey ("global") by the frontend's
occurrenceColor.ts even though they're clearly regional. This script picks
the dominant regional slug (by per-slug priority) and writes the
corresponding bias template to region_weights.

Slugs treated as "regional anchor" (template applies):
    england, england-monarchs, france, germany, ancient-greece,
    roman-history, renaissance, napoleonic, crusades, industrial → europe
    usa, us-presidents, pre-columbian-americas                     → americas
    china, japan, india                                            → asia
    ottoman, islam, judaism                                        → asia (Middle East)

Slugs left as global (no template applied):
    master, arts-and-thoughts, people, major-religions, christianity,
    cold-war, ww1, ww2 (these are intentionally cross-regional — the user
    can layer their own region_weights if they care)

Templates match the CLAUDE.md guidance: ~9 for primary, ~3-4 for others.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MASTER_PY = ROOT / "v2" / "data" / "master.py"
sys.path.insert(0, str(ROOT))

# Five-value bias by region.
TEMPLATES: dict[str, dict[str, int]] = {
    "europe":      {"europe": 9, "americas": 4, "asia": 3, "australasia": 3, "africa": 3},
    "americas":    {"europe": 4, "americas": 9, "asia": 3, "australasia": 3, "africa": 3},
    "asia":        {"europe": 3, "americas": 3, "asia": 9, "australasia": 3, "africa": 3},
    "africa":      {"europe": 3, "americas": 3, "asia": 4, "australasia": 2, "africa": 9},
    "australasia": {"europe": 3, "americas": 3, "asia": 4, "australasia": 9, "africa": 2},
}

# Map each "regional anchor" slug to a template key. Slugs not listed below
# don't bias the region (entries will stay global if no other slug matches).
SLUG_TO_REGION: dict[str, str] = {
    # Europe
    "england":            "europe",
    "england-monarchs":   "europe",
    "france":             "europe",
    "germany":            "europe",
    "ancient-greece":     "europe",
    "roman-history":      "europe",
    "renaissance":        "europe",
    "napoleonic":         "europe",
    "crusades":           "europe",
    "industrial":         "europe",
    # Americas
    "usa":                "americas",
    "us-presidents":      "americas",
    "pre-columbian-americas": "americas",
    # Asia
    "china":              "asia",
    "japan":              "asia",
    "india":              "asia",
    "ottoman":            "asia",
    "islam":              "asia",
    "judaism":            "asia",
}


def is_uniform(rw: dict[str, int] | None) -> bool:
    """True when region_weights is missing or all values are equal."""
    if not rw:
        return True
    vals = set(rw.values())
    return len(vals) <= 1


def dominant_regional_slug(prios: dict[str, int]) -> str | None:
    """Pick the regional-anchor slug with the highest priority for this entry.
    Returns None if no regional slug matches the SLUG_TO_REGION list."""
    candidates = [(s, p) for s, p in prios.items() if s in SLUG_TO_REGION]
    if not candidates:
        return None
    candidates.sort(key=lambda sp: (-sp[1], sp[0]))
    return candidates[0][0]


def render_region_weights(template: dict[str, int]) -> str:
    """Format the dict as it appears in master.py — single-line, ordered."""
    keys = ["europe", "americas", "asia", "australasia", "africa"]
    parts = [f'"{k}": {template[k]}' for k in keys]
    return "{" + ", ".join(parts) + "}"


def main() -> int:
    from v2.data.master import OCCURRENCES

    text = MASTER_PY.read_text(encoding="utf-8")
    fixed = 0
    skipped_no_regional_slug = 0
    skipped_already_biased = 0

    for o in OCCURRENCES:
        prios = o.get("priorities") or {}
        rw = o.get("region_weights")

        if not is_uniform(rw):
            skipped_already_biased += 1
            continue

        slug = dominant_regional_slug(prios)
        if slug is None:
            skipped_no_regional_slug += 1
            continue

        region = SLUG_TO_REGION[slug]
        template = TEMPLATES[region]
        new_rw_str = render_region_weights(template)

        eid = o["id"]
        # Rewrite or insert the region_weights line for this entry.
        # The entry block runs from `{"id": <eid>,` to the closing `}}`. We
        # capture the full block INCLUDING both `}` characters (one closes the
        # last inner dict like priorities or region_weights, one closes the
        # entry itself); the trailing `,\n` is matched but not captured.
        entry_pat = re.compile(
            rf'(\{{"id": {eid:_},.*?\}}\}}),\n',
            re.DOTALL,
        )
        m = entry_pat.search(text)
        if not m:
            print(f"  WARN: could not locate entry {eid} in master.py")
            continue
        block = m.group(1)
        if '"region_weights":' in block:
            # Replace the existing region_weights {...} dict literal.
            new_block = re.sub(
                r'("region_weights":\s*)\{[^}]*\}',
                lambda mm: f"{mm.group(1)}{new_rw_str}",
                block,
                count=1,
            )
            if new_block == block:
                print(f"  WARN: region_weights substitution didn't fire for {eid}")
                continue
            block2 = new_block
        else:
            # Append region_weights as the last field before the entry's
            # closing `}`. Block ends with `...}}` — split off the outer `}`,
            # add the new field, re-attach the outer `}`.
            inner, _, _ = block.rpartition("}")
            block2 = inner.rstrip().rstrip(",") + f',\n     "region_weights": {new_rw_str}' + "}"
        text = text[: m.start()] + block2 + ",\n" + text[m.end():]
        fixed += 1

    MASTER_PY.write_text(text, encoding="utf-8")
    print(f"Fixed region_weights on {fixed} entries")
    print(f"Skipped (already biased): {skipped_already_biased}")
    print(f"Skipped (no regional anchor slug): {skipped_no_regional_slug}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
