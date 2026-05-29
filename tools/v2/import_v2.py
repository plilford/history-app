"""
Import the curated dataset to Supabase. Run after editing tools/v2/data/*.py.

Usage (from project root):
    cd tools
    .venv\\Scripts\\activate              (Windows)   or   source .venv/bin/activate
    pip install -r requirements.txt      (once)
    python -m v2.import_v2

Idempotent: re-running merges any new/changed occurrences and re-inserts
their priority rows.

Schema notes (post-migration 009):
    * Table is `occurrences` (was `events`).
    * Junction table is `occurrence_timeline_priorities` with column
      `occurrence_id` (was `event_id`).
    * Title lives in a single `title` column (was `event_short` /
      `display_name` / `person`).
    * priority is an integer.
    * `is_ongoing=True` replaces the old `end_year = 2026` placeholder for
      things still going on (reigns, presidencies, dynasties, etc.). The
      importer accepts either form for back-compat.
    * `first_zoom_out_id` / `second_zoom_out_id` FK columns are populated by
      a single RPC call to `rebuild_zoom_out_ids()` at the end of the run.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client, Client

from v2.data import master   # add new modules here as we build them
# Resource-type data modules — separate files for cleanliness. Imported
# lazily so a missing module (e.g. early in scaffolding) doesn't crash the
# importer. See `_optional_module` below.
# from v2.data import the_rest_is_history, popular_history_books

# The timelines we maintain. Edit this list to add more.
# (slug is the lookup key used in each occurrence's "priorities" dict;
#  name is the human-readable label shown in the UI.)
#
# `is_resource_timeline=True` flags a timeline as resource-only: only
# occurrence_type='resource' rows may carry priorities on it, and the
# frontend filters out resources from every other timeline. The DB
# enforces this via the otp_check_resource trigger (migration 011).
# `group` drives the dropdown section a timeline lands in (mirrors the
# TimelineGroup union in src/lib/timelineGroups.ts). Set it on every new
# timeline so it's categorised correctly without a frontend code change.
# Valid values: worldwide | europe | americas | asia | africa | australasia
#               | conflicts | religions | major-periods | resources
TIMELINES = [
    {"slug": "master",            "name": "Master",                "display_order": 0,  "is_featured": True,  "is_resource_timeline": False, "group": "worldwide"},
    {"slug": "arts-and-thoughts", "name": "Arts and Thoughts",     "display_order": 1,  "is_featured": True,  "is_resource_timeline": False, "group": "worldwide"},
    {"slug": "england-monarchs",  "name": "England: Monarchs",     "display_order": 2,  "is_featured": True,  "is_resource_timeline": False, "group": "europe"},
    {"slug": "us-presidents",     "name": "USA: Presidents",       "display_order": 3,  "is_featured": False, "is_resource_timeline": False, "group": "americas"},
    {"slug": "china",             "name": "China",                 "display_order": 4,  "is_featured": False, "is_resource_timeline": False, "group": "asia"},
    {"slug": "usa",               "name": "USA",                   "display_order": 5,  "is_featured": False, "is_resource_timeline": False, "group": "americas"},
    {"slug": "france",            "name": "France",                "display_order": 6,  "is_featured": False, "is_resource_timeline": False, "group": "europe"},
    {"slug": "india",             "name": "India",                 "display_order": 7,  "is_featured": False, "is_resource_timeline": False, "group": "asia"},
    {"slug": "people",            "name": "People",                "display_order": 8,  "is_featured": False, "is_resource_timeline": False, "group": "worldwide"},
    {"slug": "ww1",               "name": "World War I",           "display_order": 9,  "is_featured": False, "is_resource_timeline": False, "group": "conflicts"},
    {"slug": "ww2",               "name": "World War II",          "display_order": 10, "is_featured": False, "is_resource_timeline": False, "group": "conflicts"},
    {"slug": "cold-war",          "name": "Cold War",              "display_order": 11, "is_featured": False, "is_resource_timeline": False, "group": "conflicts"},
    {"slug": "napoleonic",        "name": "Napoleonic Wars",       "display_order": 12, "is_featured": False, "is_resource_timeline": False, "group": "conflicts"},
    {"slug": "industrial",        "name": "Industrial Revolution", "display_order": 13, "is_featured": False, "is_resource_timeline": False, "group": "major-periods"},
    {"slug": "renaissance",       "name": "Renaissance",           "display_order": 14, "is_featured": False, "is_resource_timeline": False, "group": "major-periods"},
    {"slug": "england",           "name": "England",               "display_order": 15, "is_featured": False, "is_resource_timeline": False, "group": "europe"},
    {"slug": "wales",             "name": "Wales",                 "display_order": 16, "is_featured": False, "is_resource_timeline": False, "group": "europe"},
    {"slug": "roman-history",     "name": "Roman History",         "display_order": 16, "is_featured": False, "is_resource_timeline": False, "group": "europe"},
    {"slug": "roman-emperors",    "name": "Rome: Emperors",        "display_order": 17, "is_featured": True,  "is_resource_timeline": False, "group": "europe"},
    {"slug": "ancient-greece",    "name": "Ancient Greece",        "display_order": 17, "is_featured": False, "is_resource_timeline": False, "group": "europe"},
    {"slug": "germany",           "name": "Germany",               "display_order": 18, "is_featured": False, "is_resource_timeline": False, "group": "europe"},
    {"slug": "crusades",          "name": "Crusades",              "display_order": 19, "is_featured": False, "is_resource_timeline": False, "group": "conflicts"},
    {"slug": "japan",             "name": "Japan",                 "display_order": 20, "is_featured": False, "is_resource_timeline": False, "group": "asia"},
    {"slug": "pre-columbian-americas", "name": "Pre-Columbian Americas", "display_order": 21, "is_featured": False, "is_resource_timeline": False, "group": "americas"},
    {"slug": "ottoman",           "name": "Ottoman Empire",        "display_order": 22, "is_featured": False, "is_resource_timeline": False, "group": "asia"},
    {"slug": "major-religions",   "name": "Major Religions",       "display_order": 23, "is_featured": False, "is_resource_timeline": False, "group": "religions"},
    {"slug": "christianity",      "name": "Christianity",          "display_order": 24, "is_featured": False, "is_resource_timeline": False, "group": "religions"},
    {"slug": "islam",             "name": "Islam",                 "display_order": 25, "is_featured": False, "is_resource_timeline": False, "group": "religions"},
    {"slug": "judaism",           "name": "Judaism",               "display_order": 26, "is_featured": False, "is_resource_timeline": False, "group": "religions"},
    # ----- Resource timelines (occurrence_type='resource' only) --------------
    # `resources-combined` is the union view — every resource regardless of
    # source carries a priority here so users can see one feed of all
    # podcasts + books interleaved by date. Per-source resource timelines
    # below let users drill into a single source.
    {"slug": "resources-combined",          "name": "Resources: Combined",           "display_order": 99,  "is_featured": True,  "is_resource_timeline": True, "group": "resources"},
    {"slug": "the-rest-is-history-podcast", "name": "The Rest Is History (podcast)", "display_order": 100, "is_featured": False, "is_resource_timeline": True, "group": "resources"},
    {"slug": "popular-history-books",       "name": "Popular history books",         "display_order": 101, "is_featured": False, "is_resource_timeline": True, "group": "resources"},
]


# Module names that contribute extra OCCURRENCES lists (in addition to
# v2.data.master). Imported lazily so missing modules don't break the
# importer during phased rollouts.
_EXTRA_DATA_MODULES = [
    "v2.data.the_rest_is_history",
    "v2.data.popular_history_books",
]


def _optional_module(name: str):
    """Import the named module if it exists; return None on ImportError so
    the importer can keep going during phased rollouts."""
    try:
        import importlib
        return importlib.import_module(name)
    except ImportError:
        return None


# -------------------------- helpers ------------------------------------------
def chunked(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


# Map a resource_subtype to its "family" — the bucket we cap on. Books of
# any flavour share a cap; podcasts share a cap. Documentaries / museum
# artifacts are their own families (currently empty buckets, future-proof).
_SUBTYPE_FAMILY: dict[str | None, str] = {
    "podcast-episode": "podcast",
    "book-nonfiction": "book",
    "book-fiction":    "book",
    "documentary":     "documentary",
    "museum-artifact": "artifact",
}
# Max number of resources to associate with any single subject, per family.
# Two podcasts + two books + one of each rarer flavour is enough to anchor
# the "Resources covering this subject" popup without drowning the user.
_PER_FAMILY_CAP = 2


def _select_top_resources_per_subject(
    pending_tags: list[tuple[int, str]],
    title_to_id: dict[str, int],
    occurrences: list[dict],
) -> list[dict]:
    """Pick the top N resources per (subject, family) bucket, return the
    rows to insert into the `resource_tags` table.

    Inputs:
      pending_tags  — every (resource_id, subject_title) pair declared by
                      the resource modules' authorial `tags` lists.
      title_to_id   — normalised-title → occurrence_id lookup (built in main).
      occurrences   — every occurrence dict (so we can read resource
                      metadata: priorities, subtype, tag count, episode count).
    """
    from collections import defaultdict

    by_id = {o["id"]: o for o in occurrences}

    # Pre-compute "how many tags does each resource carry" — focused
    # resources outrank broad surveys.
    tags_per_resource: dict[int, int] = defaultdict(int)
    for rid, _ in pending_tags:
        tags_per_resource[rid] += 1

    def score(rid: int, subject_title: str) -> int:
        r = by_id.get(rid)
        if r is None:
            return 0
        pris = (r.get("priorities") or {}).values()
        base = max((int(p) for p in pris), default=0)
        # Specificity: -1k per tag the resource carries (so a 2-tag resource
        # scores +6k higher than an 8-tag one).
        spec = -tags_per_resource[rid] * 1_000
        # Episode-count bonus: a 4-episode series outranks a single episode.
        ep_bonus = min((len(r.get("resource_episodes") or []) or 1) * 1_000, 10_000)
        # Title-match: if the subject's title appears in the resource title,
        # this is a "deep-dive" resource for that subject specifically.
        rt = (r.get("title") or "").lower()
        st_norm = subject_title.strip().lower()
        title_match = 5_000 if st_norm and st_norm in rt else 0
        # Subtype bias matches the resources-combined formula.
        subtype_bias = {
            "book-nonfiction":  5_000,
            "book-fiction":    -2_000,
        }.get(r.get("subtype") or "", 0)
        return base + spec + ep_bonus + title_match + subtype_bias

    # subject_id → family → [(resource_id, score)]
    candidates: dict[int, dict[str, list[tuple[int, int]]]] = defaultdict(
        lambda: defaultdict(list),
    )
    for rid, st in pending_tags:
        sid = title_to_id.get(st.strip().lower())
        if sid is None or sid == rid:
            continue
        r = by_id.get(rid)
        if r is None:
            continue
        family = _SUBTYPE_FAMILY.get(r.get("subtype"), "other")
        candidates[sid][family].append((rid, score(rid, st)))

    # Pick top N per family.
    selected_pairs: set[tuple[int, int]] = set()   # (resource_id, subject_id)
    for sid, by_family in candidates.items():
        for family, items in by_family.items():
            items.sort(key=lambda x: -x[1])
            for rid, _ in items[:_PER_FAMILY_CAP]:
                selected_pairs.add((rid, sid))

    return [
        {"resource_id": rid, "subject_id": sid}
        for (rid, sid) in sorted(selected_pairs)
    ]


def year_str(y: int | None) -> str:
    if y is None:
        return ""
    if y < 0:
        return f"{abs(y):,} BCE"
    return f"{y}"


def is_ongoing_for(o: dict) -> bool:
    """Treat both the explicit flag and the legacy end_year=2026 sentinel as
    'still going'. Eventually master.py should be rewritten to use the flag
    directly, but until then this back-compat keeps both forms working."""
    if o.get("is_ongoing"):
        return True
    return o.get("end_year") == 2026


def build_display_date(o: dict) -> str | None:
    if o.get("display_date"):
        return o["display_date"]
    s = o.get("start_year")
    e = o.get("end_year")
    if s is None:
        return None
    star = "*" if o.get("date_uncertain") else ""
    if is_ongoing_for(o):
        return f"{year_str(s)}–present{star}"
    if e is None or e == s:
        return f"{year_str(s)}{star}"
    return f"{year_str(s)}–{year_str(e)}{star}"


# -------------------------- main ---------------------------------------------
def collect_all_occurrences() -> list[dict]:
    """Pull OCCURRENCES from master.py and any resource modules that exist."""
    out: list[dict] = []
    sources: list[tuple[str, object]] = [("master", master)]
    for name in _EXTRA_DATA_MODULES:
        mod = _optional_module(name)
        if mod is not None:
            sources.append((name, mod))
    for module_name, mod in sources:
        if not hasattr(mod, "OCCURRENCES"):
            print(f"  WARNING: data module {module_name} has no OCCURRENCES list")
            continue
        out.extend(mod.OCCURRENCES)
    return out


def main():
    here = Path(__file__).resolve().parent
    load_dotenv(here.parent.parent / ".env")

    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        sys.exit("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env")

    sb: Client = create_client(url, key)

    # 1. Upsert timelines.
    print(f"Upserting {len(TIMELINES)} timelines ...")
    sb.table("timelines").upsert(TIMELINES, on_conflict="name").execute()

    rows = sb.table("timelines").select("id,slug").execute().data
    slug_to_id = {r["slug"]: r["id"] for r in rows}

    # 2. Collect occurrences from all data modules.
    occurrences = collect_all_occurrences()
    print(f"Parsed {len(occurrences)} occurrences")

    # Sanity: IDs unique. The historical convention is IDs >= 1_000_000 (was
    # to keep v2 distinct from v1 spreadsheet IDs); we keep enforcing it as a
    # guard against accidentally re-using a low spreadsheet ID.
    seen_ids: set[int] = set()
    occurrence_payload: list[dict] = []
    priorities_payload: list[dict] = []
    # Pending resource-tag rows. Subjects are referenced by TITLE in the
    # data files (human-readable + stable); we resolve them to IDs against
    # the union of all parsed entries after the first pass.
    pending_tags: list[tuple[int, str]] = []  # (resource_id, subject_title)
    title_to_id: dict[str, int] = {}          # for tag resolution

    for o in occurrences:
        eid = o["id"]
        if eid < 1_000_000:
            sys.exit(f"occurrence ids must be >= 1_000_000 (got {eid} for {o.get('title')})")
        if eid in seen_ids:
            sys.exit(f"duplicate id: {eid}")
        seen_ids.add(eid)

        s_year = o.get("start_year")
        e_year = o.get("end_year")
        ongoing = is_ongoing_for(o)
        if ongoing:
            # Strip the legacy 2026 placeholder; is_ongoing carries the
            # "still going" semantics now.
            e_year = None
        is_period = e_year is not None and e_year != s_year

        # key_date: a single representative day for the UI to position this
        # occurrence as one box. Default = midpoint of (start, end) for
        # periods, start_year for point events. Override per-occurrence in
        # data files (e.g. set key_year=1913 for Tagore to centre on his
        # Nobel year). Ongoing periods centre on their start until something
        # explicit is set.
        k_year = o.get("key_year")
        if k_year is None:
            if is_period and s_year is not None and e_year is not None:
                k_year = (s_year + e_year) // 2
            else:
                k_year = s_year

        # Region weights: 1-10 per major region. Default neutral 5 across the
        # board if the occurrence doesn't specify one. Stored as five columns
        # for cheap filtering and so the existing CHECK constraints can do the
        # validation, instead of a single jsonb blob.
        rw = o.get("region_weights") or {}
        def _w(key: str) -> int:
            v = rw.get(key, 5)
            try:
                v = int(v)
            except Exception:
                v = 5
            return max(1, min(10, v))

        occurrence_payload.append({
            "id":               eid,
            "occurrence_type":  o.get("type", "event"),
            "title":            o["title"],
            "description":      o.get("description"),
            "start_year":       s_year,
            "start_month":      o.get("start_month"),
            "start_day":        o.get("start_day"),
            "end_year":         e_year,
            "end_month":        None if ongoing else o.get("end_month"),
            "end_day":          None if ongoing else o.get("end_day"),
            "key_year":         k_year,
            "key_month":        o.get("key_month"),
            "key_day":          o.get("key_day"),
            "is_period":        is_period,
            "is_ongoing":       ongoing,
            "date_uncertain":   bool(o.get("date_uncertain", False)),
            "display_date":     build_display_date(o),
            "wikipedia_link":   o.get("wikipedia"),
            "other_link":       o.get("other_link"),
            # Primary external URL for resource-type entries. Falls back to
            # `resource_link` field in data files; null otherwise.
            "resource_link":    o.get("resource_link"),
            # List-of-dicts for multi-episode podcast series bundled into one
            # occurrence: [{"title": ..., "url": ..., "date": ...}, ...].
            "resource_episodes": o.get("resource_episodes"),
            # Optional discriminator for resource flavours — drives the
            # frontend colour scheme. Common values:
            #   'podcast-episode', 'book-nonfiction', 'book-fiction',
            #   'documentary', 'museum-artifact'
            "resource_subtype":  o.get("subtype"),
            "weight_europe":      _w("europe"),
            "weight_americas":    _w("americas"),
            "weight_asia":        _w("asia"),
            "weight_australasia": _w("australasia"),
            "weight_africa":      _w("africa"),
            # Umbrella-period name (e.g. "Edwardian War") for sub-events that
            # were split out of a long period entry. The DB-side trigger
            # populates first_zoom_out_id from this title.
            "first_zoom_out":     o.get("first_zoom_out"),
            # Broader umbrella-period name (e.g. "Hundred Years' War") for
            # rolling sub-events up TWO levels at level-2 zoom.
            "second_zoom_out":    o.get("second_zoom_out"),
            # True when this is a person's full lifespan (birth→death). The
            # frontend hides these by default via a header toggle so the
            # timeline isn't crowded with person bars; the user can opt in.
            "is_full_life":       bool(o.get("is_full_life", False)),
        })

        # Title → id mapping for resource_tag resolution below.
        title_to_id[o["title"].strip().lower()] = eid

        # Resource tags: each resource entry can declare a `tags: [title, ...]`
        # list of subject occurrences it covers. Resolved after the loop.
        for subject_title in (o.get("tags") or []):
            pending_tags.append((eid, subject_title))

        for tl_slug, prio in (o.get("priorities") or {}).items():
            tl_id = slug_to_id.get(tl_slug)
            if tl_id is None:
                print(f"  WARNING: id {eid} ({o['title']}) references unknown timeline slug '{tl_slug}'")
                continue
            priorities_payload.append({
                "occurrence_id": eid,
                "timeline_id":   tl_id,
                "priority":      int(prio),
            })

        # Auto-populate `resources-combined` for every resource-type entry.
        # The combined timeline is the union view of every podcast / book /
        # documentary, so each resource needs a priority row regardless of
        # which per-source timeline carries it natively.
        # Priority = max of the source-timeline priorities + a per-subtype
        # bias (non-fiction books get a small boost over podcast eps, fiction
        # gets a small de-boost) to break ties on similar-dated entries:
        #   book-nonfiction: +5000
        #   podcast-episode: 0 (baseline)
        #   book-fiction:    -2000
        #   documentary, museum-artifact, null: 0
        if o.get("type") == "resource":
            combined_id = slug_to_id.get("resources-combined")
            if combined_id is not None:
                source_pris = [int(p) for p in (o.get("priorities") or {}).values()]
                base = max(source_pris) if source_pris else 900_000
                subtype_bias = {
                    "book-nonfiction":  5_000,
                    "book-fiction":    -2_000,
                }.get(o.get("subtype") or "", 0)
                priorities_payload.append({
                    "occurrence_id": eid,
                    "timeline_id":   combined_id,
                    "priority":      max(0, min(1_000_000, base + subtype_bias)),
                })

    # 3. Upsert occurrences. Chunk small enough to survive flaky connections —
    #    the resource_episodes JSONB column inflates per-row size and large
    #    batches occasionally trip the HTTP/2 stream limit.
    print(f"Upserting {len(occurrence_payload)} occurrences ...")
    for batch in chunked(occurrence_payload, 200):
        sb.table("occurrences").upsert(batch, on_conflict="id").execute()

    # 4. Replace occurrence_timeline_priorities. The recompute_main_for_occurrence
    #    trigger keeps main_category + main_priority in sync as rows arrive.
    print("Replacing occurrence_timeline_priorities ...")
    ids = [e["id"] for e in occurrence_payload]
    if ids:
        for batch in chunked(ids, 500):
            sb.table("occurrence_timeline_priorities").delete().in_(
                "occurrence_id", batch
            ).execute()
    for batch in chunked(priorities_payload, 1000):
        sb.table("occurrence_timeline_priorities").insert(batch).execute()

    # 5. Resolve umbrella references (text → FK id). Faster than letting the
    #    per-row BEFORE trigger fire on every upsert above.
    print("Rebuilding zoom_out FK ids ...")
    sb.rpc("rebuild_zoom_out_ids").execute()

    # 6. Resource tags: resolve subject titles → ids, score each candidate
    #    (resource, subject) pair, and KEEP ONLY the top 2 podcasts + top 2
    #    books per subject. Authorial tag lists in the data modules remain
    #    untouched — they're the canonical "this resource covers these
    #    subjects" assertion — but the visible cross-link (the popup's 📚
    #    list and the resource_tags table) only carries the cream so popular
    #    subjects don't drown the user in tangentially-mentioned references.
    #
    # Scoring (higher = more relevant for THIS subject):
    #   base                        = max(resource.priorities.values())
    #   - (num_tags(resource) * 1k) → focused resources beat broad surveys
    #   + (episode_count * 1k)      → multi-part deep-dives outrank singles
    #   + 5k if subject title appears as substring of resource title
    #   + 5k for book-nonfiction, -2k for book-fiction (matches the
    #     resources-combined bias above)
    tag_rows = _select_top_resources_per_subject(
        pending_tags, title_to_id, occurrences,
    )
    unresolved = [
        (rid, t) for rid, t in pending_tags
        if title_to_id.get(t.strip().lower()) is None
    ]

    if unresolved:
        print(f"  {len(unresolved)} unresolved resource tags (subject title not found):")
        for rid, t in unresolved[:20]:
            print(f"    resource {rid} → {t!r}")
        if len(unresolved) > 20:
            print(f"    ...and {len(unresolved) - 20} more")

    if pending_tags:
        # Replace existing tag rows for any resource we just upserted, so
        # removing a tag in the data file actually removes it on hosted.
        resource_ids_with_tags = sorted({rid for rid, _ in pending_tags})
        print(f"Replacing resource_tags for {len(resource_ids_with_tags)} resources "
              f"({len(tag_rows)} tag rows) ...")
        for batch in chunked(resource_ids_with_tags, 200):
            sb.table("resource_tags").delete().in_("resource_id", batch).execute()
        # Dedupe (data files can list the same subject twice by accident).
        seen_pairs: set[tuple[int, int]] = set()
        unique_tag_rows: list[dict] = []
        for r in tag_rows:
            key = (r["resource_id"], r["subject_id"])
            if key in seen_pairs:
                continue
            seen_pairs.add(key)
            unique_tag_rows.append(r)
        for batch in chunked(unique_tag_rows, 500):
            sb.table("resource_tags").insert(batch).execute()

    print(f"Done. {len(occurrence_payload)} occurrences, "
          f"{len(priorities_payload)} priorities, "
          f"{len(tag_rows)} resource tags. "
          f"main_category and main_priority maintained by trigger.")


if __name__ == "__main__":
    main()
