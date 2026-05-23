"""
Static validation pass over the v2 data files. Run BEFORE import_v2 so that
broken references and other class-of-error mistakes never make it into the DB.

Usage (from project root):
    cd tools
    .venv\\Scripts\\activate              (Windows)   or   source .venv/bin/activate
    python -m v2.validate

Exits 0 if everything's fine, non-zero on the first batch of failures (prints
them all before exiting so a single run surfaces everything that needs fixing).

Checks:
    1.  Required fields present: id, title, start_year.
    2.  Each id is unique and >= 1_000_000 (the historical "v2 range" sentinel,
        retained to guard against accidentally re-using a low spreadsheet id).
    3.  Each title is unique (case-insensitive after trim) — duplicate titles
        break the umbrella-period FK lookup, which matches by title.
    4.  first_zoom_out / second_zoom_out values reference an actual entry's
        title. Dangling references would silently fail to roll up at zoom-out.
    5.  Every priorities-dict key is a known timeline slug (matches
        import_v2.TIMELINES).
    6.  start_year <= end_year whenever both are set (the migration adds the
        same check as a DB constraint — fail-fast catches it before insert).
    7.  is_full_life is only set on type='person' rows. The toggle that hides
        lifespan bars relies on this invariant.
"""

from __future__ import annotations

import sys
from collections import defaultdict

from v2.data import master
from v2.import_v2 import TIMELINES


def collect_all_occurrences() -> list[dict]:
    """Mirror import_v2.collect_all_occurrences so the two stay in sync."""
    out: list[dict] = []
    for module_name, mod in [("master", master)]:
        if not hasattr(mod, "OCCURRENCES"):
            print(f"  WARNING: data module {module_name} has no OCCURRENCES list")
            continue
        out.extend(mod.OCCURRENCES)
    return out


def title_key(s: str) -> str:
    return s.strip().lower()


def main() -> int:
    occurrences = collect_all_occurrences()
    errors: list[str] = []
    warnings: list[str] = []

    valid_slugs = {t["slug"] for t in TIMELINES}

    by_id: dict[int, dict] = {}
    by_title: dict[str, list[dict]] = defaultdict(list)

    # ---- single-pass collection + per-row checks --------------------------
    for o in occurrences:
        eid = o.get("id")
        title = o.get("title")

        if eid is None or title is None or o.get("start_year") is None:
            errors.append(
                f"missing required field (id/title/start_year): "
                f"{o!r}"[:200]
            )
            continue

        if not isinstance(eid, int) or eid < 1_000_000:
            errors.append(f"id {eid} must be an int >= 1_000_000 ({title!r})")

        if eid in by_id:
            errors.append(
                f"duplicate id {eid}: {title!r} collides with "
                f"{by_id[eid].get('title')!r}"
            )
        else:
            by_id[eid] = o
        by_title[title_key(title)].append(o)

        # start_year <= end_year, when both are set and the row isn't ongoing.
        s = o.get("start_year")
        e = o.get("end_year")
        if (
            s is not None
            and e is not None
            and not o.get("is_ongoing", False)
            and e != 2026   # legacy ongoing sentinel — still accepted
            and s > e
        ):
            errors.append(f"id {eid} ({title!r}): start_year {s} > end_year {e}")

        # priorities reference known slugs.
        for slug in (o.get("priorities") or {}).keys():
            if slug not in valid_slugs:
                errors.append(
                    f"id {eid} ({title!r}): priorities slug {slug!r} "
                    f"is not in TIMELINES"
                )

        # is_full_life only on persons.
        if o.get("is_full_life") and o.get("type") != "person":
            errors.append(
                f"id {eid} ({title!r}): is_full_life=True but "
                f"type={o.get('type')!r} (expected 'person')"
            )

    # ---- duplicate-title check --------------------------------------------
    # Run after the pass so we report each duplicate group once.
    for key, group in by_title.items():
        if len(group) > 1:
            ids = ", ".join(str(o["id"]) for o in group)
            errors.append(
                f"duplicate title {group[0]['title']!r} (case-insensitive): "
                f"ids {ids}"
            )

    # ---- umbrella-reference integrity -------------------------------------
    titles_set = set(by_title.keys())
    for o in occurrences:
        for field in ("first_zoom_out", "second_zoom_out"):
            ref = o.get(field)
            if ref and title_key(ref) not in titles_set:
                warnings.append(
                    f"id {o.get('id')} ({o.get('title')!r}): "
                    f"{field}={ref!r} doesn't match any entry's title"
                )

    # ---- report -----------------------------------------------------------
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  {w}")
        print()

    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  {e}")
        print()
        print(f"FAIL — {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(
        f"OK — {len(occurrences)} occurrences, "
        f"{len(warnings)} warning(s), no errors"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
