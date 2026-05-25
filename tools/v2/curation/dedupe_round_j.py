"""
Round J cleanup, 2026-05-25.

Two operations:

1. **Delete the four religion-umbrella entries.** Peter explicitly doesn't
   want "Christianity" / "Islam" / "Judaism" / "Major religions of the world"
   as occurrences — they exist as TIMELINE slugs and the umbrella row
   doubles up unhelpfully (drawn end-of-period at 2025, dominates the visual).

2. **Auto-detect and purge clear same-event duplicates.**

   Targets only the unambiguous cases:
     - "X" + "X (parenthetical clarifier)" with same start_year/end_year/shape.
     - "X" + "X (YEAR)" year-suffix duplicates.
     - "X founded/established/published/opens/completed/compiled" +
       "X" with same start_year and the second one being either a period
       or the same point-event — these are the "different framing" dupes.
     - Multi-instance clusters from earlier curation passes where the
       parent script ran multiple times.

   Conservatively leaves "X begins" + "X (period)" pairs alone — those are
   intentional separate point markers + umbrella periods.

   Survivor rule per cluster:
     - Prefer the entry with MORE slug priorities (richer tagging).
     - Tie-break: prefer cleaner title (no parenthetical clarifier).
     - Tie-break: prefer entry with longer description.
     - Tie-break: lowest ID (older / more stable).
   Slugs from the deleted entries are merged into the survivor (taking the
   max priority per slug).

Outputs:
    dupe_clusters_round_j.txt    — human-readable report of every cluster
                                   actioned.
    Rewrites master.py in place.

Idempotent re-runs are safe — already-deleted IDs simply aren't found.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MASTER_PY = ROOT / "v2" / "data" / "master.py"
REPORT = Path(__file__).with_name("dupe_clusters_round_j.txt")
sys.path.insert(0, str(ROOT))


# Religion umbrellas explicitly slated for deletion.
RELIGION_UMBRELLAS = [1_006_895, 1_006_896, 1_006_897, 1_006_898]

# Manually-curated extra dupes the auto-detector misses (e.g. when start_years
# differ by more than the 5-year bucket). Format: (id_to_delete, id_to_keep).
MANUAL_DUPES = [
    # One Thousand and One Nights: 1000889 (900-1400) is the canonical entry;
    # 1001365 ("compiled") is the later-added variant with start=800.
    (1_001_365, 1_000_889),
]


def normalize_title(s: str) -> str:
    s = (s or "").lower()
    # Strip parenthesised content (perspectives, year tags, alt names).
    s = re.sub(r"\([^)]*\)", "", s)
    # Strip framing suffixes that indicate "this is the moment X happened".
    # IMPORTANT: NEVER strip 'begins' / 'ends' here. Those are legitimate
    # point-markers that pair with a PERIOD umbrella entry — they roll up to
    # the umbrella via first_zoom_out and absorb at low zoom. Clustering
    # "X begins" with "X" would delete the rollup-child, which is exactly
    # what we don't want. (Same-shape same-year clusters are still caught:
    # if both "X" and "X begins" are points at year N, they cluster only when
    # neither has a period sibling, which means there's no rollup intent and
    # they're functionally the same entry.)
    s = re.sub(
        r"\b(founded|established|compiled|completed|opens|opened|published|launched|"
        r"announced|signed|ratified|assembled|cancelled|abolished|introduced|invented|"
        r"discovered|premieres|first published)\b",
        " ",
        s,
    )
    # Strip non-alphanumerics, collapse spaces.
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    return " ".join(s.split())


def shape(o: dict) -> str:
    """Coarse shape category — both must match to be considered a duplicate."""
    has_end = o.get("end_year") is not None and o.get("end_year") != o.get("start_year")
    return "period" if has_end else "point"


def has_parenthetical(title: str) -> bool:
    return "(" in (title or "")


# Variant suffixes that disqualify a title from being the "canonical" name.
_VARIANT_SUFFIX = re.compile(
    r"\b(begins|ends|founded|established|compiled|completed|launched|"
    r"announced|signed|ratified|opens|opened|premieres|first published)\b",
    re.IGNORECASE,
)


def looks_canonical(title: str) -> bool:
    """Heuristic: a title that's *not* a variant phrasing of a canonical name.

    Canonical: "Battle of Verdun", "Treaty of Versailles", "Reconquista".
    Variant:   "Battle of Verdun begins", "Treaty of Versailles (German perspective)",
               "Reconquista (Spain)".
    """
    if not title:
        return False
    if "(" in title:
        return False
    if _VARIANT_SUFFIX.search(title):
        return False
    return True


def survivor_key(o: dict) -> tuple:
    """Ranking tuple — HIGHER tuple wins (i.e. survives).

    Order of priority (canonical title comes first so we keep "Reconquista"
    over "Reconquista (Spain)" even if the latter has more slugs — we'll
    merge the slugs into the survivor anyway):
      1. canonical-looking title (no parenthetical, no variant suffix)
      2. clean title (no parenthetical)  — secondary
      3. more slug priorities (richer tagging)
      4. longer description
      5. lower id (more stable)
    """
    canonical = looks_canonical(o.get("title") or "")
    clean = not has_parenthetical(o.get("title") or "")
    num_slugs = len(o.get("priorities") or {})
    desc_len = len(o.get("description") or "")
    return (canonical, clean, num_slugs, desc_len, -(o.get("id") or 0))


def find_duplicates(occurrences: list[dict]) -> list[list[dict]]:
    """Return clusters of dupes (each cluster is >= 2 entries)."""
    # Group by (normalized title, shape, start_year_bucket).
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for o in occurrences:
        n = normalize_title(o.get("title"))
        if not n or len(n) < 5:
            continue
        if o.get("id") in RELIGION_UMBRELLAS:
            # These are being deleted separately; don't pull them into clusters.
            continue
        sy = o.get("start_year")
        if sy is None:
            continue
        # 5-year bucket — handles approximate-date variance.
        bucket = round(sy / 5) * 5
        sh = shape(o)
        groups[(n, sh, bucket)].append(o)

    clusters: list[list[dict]] = []
    for key, group in groups.items():
        if len(group) < 2:
            continue
        # For periods, also require that end years are within 10 years to count.
        if key[1] == "period":
            ends = [o.get("end_year") for o in group if o.get("end_year") is not None]
            if ends and (max(ends) - min(ends) > 10):
                # End years too far apart — not a real cluster.
                continue
        clusters.append(group)
    return clusters


def pick_survivor(cluster: list[dict]) -> tuple[dict, list[dict]]:
    ranked = sorted(cluster, key=survivor_key, reverse=True)
    return ranked[0], ranked[1:]


def merge_slug_priorities(survivor: dict, victim: dict) -> dict:
    """Return the survivor's merged priorities dict (max-per-slug). Doesn't
    mutate the survivor; caller decides whether to write it out."""
    out = dict(survivor.get("priorities") or {})
    for slug, pri in (victim.get("priorities") or {}).items():
        cur = out.get(slug, 0)
        out[slug] = max(cur, pri)
    return out


# ----- master.py rewriting --------------------------------------------------
# The file is appended to in well-formatted chunks. We rely on a per-entry
# regex similar to purge_duplicates.py.


def delete_entry_in_file(text: str, entry_id: int) -> tuple[str, bool]:
    pat = re.compile(
        rf'    \{{"id": {entry_id:_},.*?\}}\}},\n',
        re.DOTALL,
    )
    new_text, n = pat.subn("", text, count=1)
    return new_text, n > 0


def replace_priorities(text: str, entry_id: int, new_priorities: dict) -> tuple[str, bool]:
    """Rewrite the `"priorities": {…}` portion of the given entry."""
    pat = re.compile(
        rf'(\{{"id": {entry_id:_},.*?"priorities":\s*)\{{[^}}]*\}}(.*?\}}\}},)',
        re.DOTALL,
    )
    # Emit a stable, compact priorities dict.
    # Order: master first, then alphabetical for the rest.
    keys = sorted(new_priorities.keys(), key=lambda k: (0 if k == "master" else 1, k))
    parts = []
    for k in keys:
        parts.append(f'"{k}": {new_priorities[k]}')
    rendered = "{" + ", ".join(parts) + "}"

    def repl(m: re.Match) -> str:
        return f"{m.group(1)}{rendered}{m.group(2)}"

    new_text, n = pat.subn(repl, text, count=1)
    return new_text, n > 0


def main() -> int:
    # Load via dynamic import so changes here don't need a reload.
    from v2.data.master import OCCURRENCES

    text = MASTER_PY.read_text(encoding="utf-8")

    # ----- 1. Religion umbrellas ---------------------------------------------
    deleted_umbrella = 0
    for uid in RELIGION_UMBRELLAS:
        text, ok = delete_entry_in_file(text, uid)
        if ok:
            deleted_umbrella += 1

    # ----- 1b. Manual dupes ---------------------------------------------------
    by_id = {o["id"]: o for o in OCCURRENCES}
    deleted_manual = 0
    for del_id, keep_id in MANUAL_DUPES:
        if del_id not in by_id or keep_id not in by_id:
            continue
        # Merge slug priorities into the kept entry.
        keeper = by_id[keep_id]
        merged = dict(keeper.get("priorities") or {})
        for slug, pri in (by_id[del_id].get("priorities") or {}).items():
            merged[slug] = max(merged.get(slug, 0), pri)
        if merged != (keeper.get("priorities") or {}):
            text, _ = replace_priorities(text, keep_id, merged)
        text, ok = delete_entry_in_file(text, del_id)
        if ok:
            deleted_manual += 1

    # ----- 2. Duplicates ------------------------------------------------------
    clusters = find_duplicates(OCCURRENCES)
    deleted_dupes = 0
    merged_slugs = 0
    report_lines: list[str] = []
    report_lines.append(f"Round J cleanup — {len(clusters)} duplicate clusters\n")
    report_lines.append("=" * 70 + "\n\n")

    by_id = {o["id"]: o for o in OCCURRENCES}

    for cluster in sorted(clusters, key=lambda c: c[0].get("title") or ""):
        survivor, victims = pick_survivor(cluster)
        # Merge victims' slugs into the survivor.
        merged = dict(survivor.get("priorities") or {})
        for v in victims:
            merged = {
                **merged,
                **{
                    slug: max(merged.get(slug, 0), pri)
                    for slug, pri in (v.get("priorities") or {}).items()
                },
            }
        # Write the survivor's new priorities into master.py (only if changed).
        if merged != (survivor.get("priorities") or {}):
            text, ok = replace_priorities(text, survivor["id"], merged)
            if ok:
                merged_slugs += 1
        # Delete each victim from master.py.
        for v in victims:
            text, ok = delete_entry_in_file(text, v["id"])
            if ok:
                deleted_dupes += 1

        # Build report entry.
        report_lines.append(
            f"--- {survivor['title']!r}  (start={survivor.get('start_year')}, shape={shape(survivor)}) ---\n"
        )
        report_lines.append(f"  KEEP  id={survivor['id']:_}  slugs={list(merged.keys())}\n")
        for v in victims:
            report_lines.append(
                f"  DROP  id={v['id']:_}  {v['title']!r}  slugs={list((v.get('priorities') or {}).keys())}\n"
            )
        report_lines.append("\n")

    MASTER_PY.write_text(text, encoding="utf-8")
    REPORT.write_text("".join(report_lines), encoding="utf-8")

    print(f"Religion umbrellas deleted: {deleted_umbrella} / {len(RELIGION_UMBRELLAS)}")
    print(f"Manual dupes deleted: {deleted_manual} / {len(MANUAL_DUPES)}")
    print(f"Duplicate clusters: {len(clusters)}")
    print(f"  victims deleted: {deleted_dupes}")
    print(f"  survivors with merged priorities: {merged_slugs}")
    print(f"Report: {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
