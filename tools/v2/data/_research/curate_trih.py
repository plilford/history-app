"""
Pre-curation pass over the first 300 TRIH episodes.

Output: a draft list of resource "items" — multi-part series collapsed into
a single item, with best-effort historical date + candidate tags drawn from
master.py title matching. Items I can't confidently date get flagged for
review.

This is a HELPER, not the final data module. It produces
trih_curated_draft.json which the user reviews before I emit the canonical
the_rest_is_history.py.

Algorithm:
  1. Read trih_episodes_raw.json (parser output).
  2. Group consecutive episodes whose titles share a common stem + "(Part N)"
     / "Part N" / "part N" / ": Part N" pattern, OR whose stems match the
     SERIES_HINTS list (for inconsistent / non-numbered series).
  3. For each group (or standalone), build an Item:
       - title: stem (no Part suffix) for series; full title for standalone
       - episodes: list of {ep_num, ep_title, pub_date, url}
       - description: longest episode description (richest source)
       - candidate_tags: master.py titles whose normalized form appears
         as a substring of the item title OR description (first ~200 chars)
       - subject_dates: parsed from title/description — regex for "YYYY",
         "BCE", "BC", common era names
       - dateability: high / medium / low / thematic
  4. Emit trih_curated_draft.json sorted by (earliest subject_year, ep_num).
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(TOOLS))
HERE = Path(__file__).resolve().parent
RAW = HERE / "trih_episodes_raw.json"
OUT = HERE / "trih_curated_draft.json"

# Series-name patterns the regex below catches automatically.
SERIES_SUFFIX_RE = re.compile(
    r"\s*[-:–—]?\s*\(?\s*(?:Pt\.?|Part|part|Episode|Ep\.?)\s*\d+\)?\s*$",
    re.IGNORECASE,
)
# Trailing parenthetical (e.g. "(Part 3)").
TRAILING_PAREN_RE = re.compile(r"\s*\([^)]*\)\s*$")


def stem_of(title: str) -> str:
    """Strip the series-part suffix to get the common stem."""
    s = title.strip()
    # Iteratively strip trailing parenthetical + Part N
    for _ in range(3):
        before = s
        s = TRAILING_PAREN_RE.sub("", s)
        s = SERIES_SUFFIX_RE.sub("", s)
        s = re.sub(r"\s*[-:–—]\s*$", "", s)
        if s == before:
            break
    return s.strip()


def looks_series_part(title: str) -> bool:
    return bool(SERIES_SUFFIX_RE.search(title))


# Extract the Part NUMBER from a series-part title. Returns None if there
# isn't a clear Part number — non-series episodes hit this path too.
PART_NUM_RE = re.compile(
    r"(?:Pt\.?|Part|part|Episode|Ep\.?)\s*(\d+)\)?\s*$",
    re.IGNORECASE,
)


def part_number(title: str) -> int | None:
    m = PART_NUM_RE.search(title)
    return int(m.group(1)) if m else None


# Years in titles/descriptions: "1942", "1066", "44 BCE", "200 BC", "AD 79".
# Negative lookbehind on `-` and lookahead on `-Year`/`-year` to avoid matching
# "200" in phrases like "200-Year Rivalry".
YEAR_RE = re.compile(
    r"(?<!-)\b(?:AD\s*)?(\d{3,4})\s*(?:BCE|BC|B\.?C\.?(?!\w))?\b(?!-(?:[Yy]ear|[Mm]ile))|\b(\d{1,4})\s*BCE?\b",
    re.IGNORECASE,
)
ONLY_BCE_RE = re.compile(r"\b(\d{1,4})\s*BCE?\b", re.IGNORECASE)
# Decade like "the 1960s", "1980s"
DECADE_RE = re.compile(r"\b(\d{3,4})0s\b", re.IGNORECASE)


def parse_years(text: str) -> list[int]:
    """Extract candidate years (positive for CE, negative for BCE) from
    free text. Crude: only catches explicit-year mentions."""
    out: list[int] = []
    seen: set[int] = set()
    for m in ONLY_BCE_RE.finditer(text):
        try:
            y = -int(m.group(1))
            if y not in seen:
                out.append(y); seen.add(y)
        except Exception:
            pass
    for m in YEAR_RE.finditer(text):
        try:
            year_str = m.group(1) or m.group(2)
            if not year_str:
                continue
            y = int(year_str)
            if y < 100 or y > 2025:
                continue
            if y in seen:
                continue
            seen.add(y); out.append(y)
        except Exception:
            pass
    return out


def dateability(years: list[int], title: str) -> str:
    if years:
        if len(years) == 1:
            return "high"
        return "medium"
    # Single 4-digit year as the entire title? Hard to miss.
    if re.match(r"^\d{4}$", title.strip()):
        return "high"
    # Otherwise thematic / hard.
    return "thematic"


# ---- master.py title matching ------------------------------------------------
def load_master_titles() -> list[tuple[str, dict]]:
    """Return [(normalized_title, occurrence_dict), ...] for tagging."""
    from v2.data.master import OCCURRENCES
    out = []
    for o in OCCURRENCES:
        t = (o.get("title") or "").strip()
        if t:
            out.append((t.lower(), o))
    return out


def candidate_tags(
    item_title: str,
    pool_text: str,
    master_titles: list[tuple[str, dict]],
    limit: int = 8,
) -> list[tuple[str, dict]]:
    """Find master.py occurrences relevant to this resource.

    Two-pass matching:
      (a) Forward: master_title appears as a substring of the pool text
          (item_title + per-ep titles + description). Strong signal — the
          podcast description literally names the subject.
      (b) Reverse: item_title's significant tokens appear as
          word-bounded substrings of a master_title. Picks up "9/11" →
          "9/11 attacks", "Pompeii" → "Eruption of Vesuvius / Pompeii
          destroyed", "Sparta" → "Spartan constitution" (but NOT
          "Spartacus" — word boundary blocks the prefix match).
    Returns at most `limit` matches, deduped by master_id."""
    pool_norm = pool_text.lower()
    seen: set[int] = set()
    matches: list[tuple[str, dict, int]] = []  # (title, occ, rank)

    # Pass (a): forward. Longer master titles first (more specific).
    for mt, occ in sorted(master_titles, key=lambda x: -len(x[0])):
        if len(mt) < 6:
            continue
        if mt in pool_norm:
            if occ["id"] in seen:
                continue
            seen.add(occ["id"])
            matches.append((occ["title"], occ, 0))   # rank 0 = best

    # Pass (b): reverse. Episode title (or each significant sub-phrase before
    # a colon) appears as a WORD-BOUNDED substring of a master title.
    # Avoids over-matching on single common tokens like "Great", "Last",
    # "Grand" — only fires when the WHOLE distinctive phrase from the
    # episode title shows up.
    stop = {"the", "a", "an", "of", "and", "or", "in", "on", "to", "for", "by",
            "with", "from", "at", "as", "is", "are", "be", "vs", "vs.",
            "trih", "ep", "eps", "part", "pt"}
    # Candidate phrases: full title + each part before/after a colon, dash.
    title_lower = item_title.lower()
    phrases = [title_lower]
    for sep in (":", "—", "–", " - "):
        for chunk in title_lower.split(sep):
            chunk = chunk.strip()
            if chunk and chunk not in phrases:
                phrases.append(chunk)
    # Require phrase to be at least 5 chars and not be a pure stopword.
    for phrase in phrases:
        if len(phrase) < 5:
            continue
        if phrase in stop:
            continue
        # Word-bounded match. Re.escape handles "9/11" etc. correctly.
        phrase_pat = re.compile(rf"\b{re.escape(phrase)}\b")
        for mt, occ in master_titles:
            if occ["id"] in seen:
                continue
            if phrase_pat.search(mt):
                seen.add(occ["id"])
                matches.append((occ["title"], occ, 1))
                if len(matches) >= limit * 3:
                    break

    # Sort: forward matches first, then reverse. Within each rank, prefer
    # entries with a higher main_priority (more globally notable subjects).
    matches.sort(key=lambda m: (m[2], -(m[1].get("main_priority") or 0)))
    return [(t, o) for t, o, _ in matches[:limit]]


def infer_subject_dates_from_tags(
    tags: list[tuple[str, dict]],
) -> tuple[int | None, int | None]:
    """If we have tag matches, derive the resource's subject span:
       - start_year: min of matched occurrences' start_years
       - end_year:   max of matched non-ongoing occurrences' end_years
    Ongoing entries are EXCLUDED from end-year derivation so a tag like
    "Boris Johnson" (is_ongoing=True with end ~ present) doesn't drag the
    inferred end year to today."""
    starts: list[int] = []
    ends: list[int] = []
    for _, occ in tags:
        s = occ.get("start_year")
        if s is None:
            continue
        starts.append(s)
        if occ.get("is_ongoing"):
            continue
        e = occ.get("end_year")
        if e is not None:
            ends.append(e)
    if not starts:
        return None, None
    span_start = min(starts)
    span_end = max(ends) if ends else None
    if span_end is not None and span_end <= span_start:
        span_end = None
    return span_start, span_end


# ---- main --------------------------------------------------------------------
def main() -> int:
    eps = json.load(open(RAW, encoding="utf-8"))
    print(f"Loaded {len(eps)} episodes")
    master_titles = load_master_titles()
    print(f"Loaded {len(master_titles)} master.py titles for matching")

    # Group consecutive episodes that end with a "Part N" / "(Part N)"
    # marker. We don't require the stems to match — TRIH multi-parters often
    # use different subtitles per episode (e.g. "Crucifixion (Part 1)",
    # "The Jews Against Rome (Part 2)", "The Jewish Revolt (Part 3)").
    # Episodes get put into a group while we're inside a Part-suffix run.
    # A standalone (no Part suffix) ends the run.
    items: list[dict] = []
    current_group: list[dict] | None = None

    def flush():
        nonlocal current_group
        if current_group:
            stem = stem_of(current_group[0]["title_clean"])
            items.append({
                "_group_stem": stem,
                "episodes": current_group,
            })
        current_group = None

    for e in eps:
        title = e["title_clean"]
        pn = part_number(title)
        if pn is not None:
            # If this is "Part 1" (or "(Part 1)") it starts a fresh series,
            # even if we're already mid-group from a previous one.
            if pn == 1:
                flush()
                current_group = [e]
            else:
                if current_group is None:
                    current_group = [e]
                else:
                    current_group.append(e)
        else:
            flush()
            items.append({
                "_group_stem": title,
                "episodes": [e],
            })
    flush()

    print(f"Grouped into {len(items)} items")
    print(f"  {sum(1 for it in items if len(it['episodes']) > 1)} multi-part series")
    print(f"  {sum(1 for it in items if len(it['episodes']) == 1)} standalone episodes")

    # Build curated draft.
    drafts = []
    for it in items:
        eps_in = it["episodes"]
        ep_nums = [e["ep_num"] for e in eps_in]
        is_series = len(eps_in) > 1

        item_title_clean = it["_group_stem"]
        # Resource_episodes payload — kept exactly as the data module needs.
        ep_payload = [
            {
                "title": e["title"],
                "url":   e["apple_url"],
                "date":  e["pub_date"],
            }
            for e in eps_in
        ]

        # Pick the longest description for date/tag analysis.
        desc = max((e["description"] for e in eps_in), key=len)
        # Pool of text to mine: title + each ep title + description (capped).
        pool = " ".join([item_title_clean] + [e["title_clean"] for e in eps_in] + [desc[:600]])

        # Date inference precedence (high → low confidence):
        #   1. Year at the START of the item title ("1981", "1922 ...")
        #   2. Year mentioned in the item title itself (e.g. "Sept 11 attacks 2001")
        #   3. Tag-derived dates from master.py matches
        #   4. Year mentioned in description, EARLIEST first, excluding
        #      anything >= 2018 (likely recording-year boilerplate)
        title_years_all = parse_years(item_title_clean)
        description_years_all = [y for y in parse_years(desc) if y < 2018 or y in title_years_all]

        tags = candidate_tags(item_title_clean, pool, master_titles)
        tag_titles = [t for t, _ in tags]

        subject_start: int | None = None
        subject_end: int | None = None
        confidence = "thematic"

        title_year_match = re.match(r"^(\d{4})\b", item_title_clean.strip())
        if title_year_match:
            subject_start = int(title_year_match.group(1))
            confidence = "high"
        elif title_years_all:
            subject_start = title_years_all[0]
            if len(title_years_all) >= 2:
                yrs = sorted(title_years_all[:2])
                if yrs[1] - yrs[0] <= 200:
                    subject_start, subject_end = yrs
            confidence = "high"
        elif tags:
            ts, te = infer_subject_dates_from_tags(tags)
            if ts is not None:
                subject_start, subject_end = ts, te
                confidence = "medium"
        if subject_start is None and description_years_all:
            yrs = sorted(set(description_years_all))
            subject_start = yrs[0]
            if len(yrs) >= 2 and yrs[-1] - yrs[0] <= 500:
                subject_end = yrs[-1]
            confidence = "low"

        # candidate_years for the report — both title + filtered description.
        years = list(dict.fromkeys(title_years_all + description_years_all))

        # Suggested resource entry title.
        if is_series:
            ep_range = f"{ep_nums[0]}-{ep_nums[-1]}"
            resource_title = f"{item_title_clean} (TRIH eps {ep_range})"
        else:
            resource_title = f"{item_title_clean} (TRIH ep {ep_nums[0]})"

        drafts.append({
            "resource_title":   resource_title,
            "ep_nums":          ep_nums,
            "subject_start":    subject_start,
            "subject_end":      subject_end,
            "confidence":       confidence,
            "candidate_years":  years,
            "candidate_tags":   tag_titles,
            "description":      desc,
            "resource_episodes": ep_payload,
        })

    # Sort by (earliest subject year, ep_num) — chronological by SUBJECT, not
    # by air date. Items without a subject year sort to the end.
    drafts.sort(key=lambda d: (d["subject_start"] if d["subject_start"] is not None else 10_000, d["ep_nums"][0]))

    OUT.write_text(json.dumps(drafts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")

    # Stats
    by_conf = defaultdict(int)
    for d in drafts:
        by_conf[d["confidence"]] += 1
    print()
    print("Confidence breakdown:")
    for k in ("high", "medium", "low", "thematic"):
        print(f"  {k:>8}: {by_conf.get(k, 0)}")
    print(f"  total: {len(drafts)}")

    # Show items with NO candidate tags (likely thematic or out-of-scope).
    no_tags = [d for d in drafts if not d["candidate_tags"]]
    print(f"\nItems with NO tag matches in master.py: {len(no_tags)}")
    for d in no_tags[:20]:
        print(f"  eps {d['ep_nums']}: {d['resource_title']}")
    if len(no_tags) > 20:
        print(f"  ...and {len(no_tags) - 20} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
