"""
TRIH curator v2 — uses the archive.therestishistory.com per-episode metadata
(`historical_events`, `historical_figures`, `books`, `summary`) to produce a
much higher-quality draft than the v1 regex-against-master.py heuristic.

Inputs:
  trih_episodes_raw.json  (RSS — all 672 numbered eps with ep_num, pub_date, ...)
  trih_archive_raw.json   (archive — ~696 detailed eps with historical_events, ...)

Algorithm:
  1. Join each RSS episode to its archive twin by date (±1 day fuzzy),
     disambiguating same-date collisions by fuzzy title match.
  2. Group RSS eps into multi-part series (same logic as v1).
  3. For each item, collect ALL archive historical_events + historical_figures
     across its episodes. Parse years from event strings.
  4. Resolve those strings into master.py occurrence titles via a normalized
     title set + per-figure lifespan lookup. Drops unresolved strings.
  5. Date inference precedence (high → low confidence):
       title_year > manual_overrides > tag-derived (from resolved master entries)
         > earliest historical_event year.

Output: trih_curated_draft_v2.json, ready for generate_trih_module_v2.py.
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict, Counter
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[2]
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(HERE))   # so `manual_curations` is importable

RSS_PATH = HERE / "trih_episodes_raw.json"
ARC_PATH = HERE / "trih_archive_raw.json"
OUT = HERE / "trih_curated_draft_v2.json"

# Same series-grouping regexes as v1.
SERIES_SUFFIX_RE = re.compile(
    r"\s*[-:–—]?\s*\(?\s*(?:Pt\.?|Part|part|Episode|Ep\.?)\s*\d+\)?\s*$",
    re.IGNORECASE,
)
PART_NUM_RE = re.compile(
    r"(?:Pt\.?|Part|part|Episode|Ep\.?)\s*(\d+)\)?\s*$",
    re.IGNORECASE,
)
TRAILING_PAREN_RE = re.compile(r"\s*\([^)]*\)\s*$")


def stem_of(title: str) -> str:
    s = title.strip()
    for _ in range(3):
        before = s
        s = TRAILING_PAREN_RE.sub("", s)
        s = SERIES_SUFFIX_RE.sub("", s)
        s = re.sub(r"\s*[-:–—]\s*$", "", s)
        if s == before:
            break
    return s.strip()


def part_number(title: str) -> int | None:
    m = PART_NUM_RE.search(title)
    return int(m.group(1)) if m else None


# ---- Date parsing from historical_events strings ------------------------------
# Matches a trailing year or year-range in parens at the end of the string.
# Handles: "(1986)", "(1653–1658)", "(c. 1900)", "(~5000 BC)", "(490 BC)",
# "(AD 79)", "(11 September 2001)", "(1918–1923)"
TRAIL_PAREN_RE = re.compile(r"\(([^)]+)\)\s*$")
YEAR_NUM_RE = re.compile(r"\b(\d{1,4})\b")
BCE_HINT_RE = re.compile(r"\b(BCE?|B\.?C\.?)\b", re.IGNORECASE)


def parse_event_year(s: str) -> tuple[int | None, int | None]:
    """Extract (start, end) years from a historical_events string. Returns
    (None, None) if no parseable year. Ranges return (start, end); single
    year returns (year, None). BCE produces negative ints."""
    m = TRAIL_PAREN_RE.search(s)
    if not m:
        return None, None
    inner = m.group(1)
    is_bce = bool(BCE_HINT_RE.search(inner))
    nums = [int(n) for n in YEAR_NUM_RE.findall(inner) if 1 <= int(n) <= 4000]
    if not nums:
        return None, None
    # Filter to plausible year values (avoid days/months in "11 September 2001")
    # — month names + day numbers would be < 32 / < 13, so prefer 3+digit nums
    # where present.
    big = [n for n in nums if n >= 100]
    if big:
        nums = big
    if is_bce:
        nums = [-n for n in nums]
    if len(nums) == 1:
        return nums[0], None
    start, end = min(nums), max(nums)
    if end == start:
        return start, None
    if abs(end - start) > 500:
        # Probably day + year in same parens. Take the bigger number alone.
        return end, None
    return start, end


def strip_paren_suffix(s: str) -> str:
    """Drop a single trailing parenthetical for tag normalization.
    'Battle of Marathon (490 BC)' -> 'Battle of Marathon'."""
    return TRAIL_PAREN_RE.sub("", s).strip()


def normalize_title(s: str) -> str:
    """Aggressive normalization for fuzzy master.py title matching."""
    s = s.lower().strip()
    # Collapse whitespace, drop punctuation noise.
    s = re.sub(r"[‐-―]", "-", s)  # unicode dashes -> ascii
    s = re.sub(r"['‘’“”]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s


def normalize_person(s: str) -> str:
    """Person-name normalization: strip parenthetical aliases.
    'Mark Twain (Samuel Langhorne Clemens)' -> 'mark twain'.
    'Harold Godwinson (Harold II of England)' -> 'harold godwinson'."""
    s = strip_paren_suffix(s)
    return normalize_title(s)


# ---- Master.py title index ---------------------------------------------------
def build_master_index() -> tuple[dict[str, dict], dict[str, list[dict]]]:
    """Returns:
      title_idx: normalized_title -> occurrence dict (exact match)
      keyword_idx: significant_word -> list of occurrences with that word in title
    """
    from v2.data.master import OCCURRENCES
    title_idx: dict[str, dict] = {}
    keyword_idx: dict[str, list[dict]] = defaultdict(list)
    stop = {"the", "a", "an", "of", "and", "or", "in", "on", "to", "for", "by",
            "with", "from", "at", "as", "is", "are", "be", "vs", "vs.", "de", "la",
            "el", "le", "von", "van"}
    for o in OCCURRENCES:
        title = (o.get("title") or "").strip()
        if not title:
            continue
        n = normalize_title(title)
        title_idx[n] = o
        # Add to keyword index — pick distinctive words (len>=4, not stopwords).
        for word in re.findall(r"[a-z0-9]+", n):
            if len(word) < 4 or word in stop:
                continue
            keyword_idx[word].append(o)
    return title_idx, keyword_idx


def resolve_event(s: str, title_idx: dict[str, dict]) -> dict | None:
    """Match a historical_events string to a master.py occurrence.
    Tries: full normalized string, stripped of trailing paren."""
    candidates = []
    n_full = normalize_title(s)
    candidates.append(n_full)
    n_stripped = normalize_title(strip_paren_suffix(s))
    if n_stripped != n_full:
        candidates.append(n_stripped)
    for n in candidates:
        if n in title_idx:
            return title_idx[n]
    return None


def resolve_figure(s: str, title_idx: dict[str, dict]) -> dict | None:
    """Match a historical_figures string to a master.py person/event title."""
    candidates = [normalize_person(s), normalize_title(s)]
    # Also try stripping titles/honorifics.
    name = strip_paren_suffix(s)
    for prefix_re in [
        r"^(?:King|Queen|Emperor|Empress|Pope|Lord|Sir|Saint|St\.?|"
        r"Captain|Capt\.?|General|Gen\.?|Admiral|Adm\.?|"
        r"Rear Admiral|Vice Admiral|Marshal|Field Marshal|"
        r"President|Prime Minister|PM|Chancellor|Tsar|Czar|"
        r"Dr\.?|Mr\.?|Mrs\.?|Ms\.?|Father|Rev\.?|Cardinal|Archbishop|"
        r"Bishop|Brother|Sister|Mother)\s+",
    ]:
        new = re.sub(prefix_re, "", name, flags=re.IGNORECASE)
        if new != name:
            candidates.append(normalize_title(new))
    for n in candidates:
        if n in title_idx:
            return title_idx[n]
    return None


def collect_tags(eps_in_group: list[dict], title_idx: dict[str, dict]) -> list[tuple[str, dict, str, int]]:
    """For all archive episodes in this group, resolve historical_events +
    historical_figures into master.py occurrences. Returns
    [(master_title, occurrence_dict, source, ep_count), ...] deduped by
    master_id. `ep_count` is the number of episodes in the group that
    reference this subject — used as the primary signal for picking the
    central subject vs tangential asides."""
    seen: dict[int, list] = {}   # master_id -> [title, occ, source, count, ep_indices_set]
    for idx, ep in enumerate(eps_in_group):
        a = ep.get("_archive") or {}
        for s in (a.get("historical_events") or []):
            occ = resolve_event(s, title_idx)
            if not occ:
                continue
            entry = seen.setdefault(occ["id"], [occ["title"], occ, "event", 0, set()])
            entry[4].add(idx)
        for s in (a.get("historical_figures") or []):
            occ = resolve_figure(s, title_idx)
            if not occ:
                continue
            entry = seen.setdefault(occ["id"], [occ["title"], occ, "figure", 0, set()])
            entry[4].add(idx)
    out: list[tuple[str, dict, str, int]] = []
    for title, occ, src, _, ep_idxs in seen.values():
        out.append((title, occ, src, len(ep_idxs)))
    return out


def filter_tags_by_proximity(
    tags: list[tuple[str, dict, str, int]],
    subject_start: int | None,
    subject_end: int | None,
) -> list[tuple[str, dict, str, int]]:
    """Drop tags whose date window doesn't overlap the subject's expanded
    window. This is the main quality filter — without it the archive's
    `historical_figures` list pulls in famous historians / passing references
    that aren't really what the episode is about (e.g. Carnegie on a
    'Dinosaurs' ep, Churchill on a '1066' ep)."""
    if subject_start is None:
        return tags
    end_eff = subject_end if subject_end is not None else subject_start
    span = max(abs(end_eff - subject_start), 1)
    # Min 50 years (so a point event still tolerates a tag dated within ±50);
    # max 500 years (so a deep-time subject like 'Dinosaurs' or 'Neanderthals'
    # doesn't end up admitting modern figures who happen to have studied it).
    padding = min(500, max(50, int(span * 0.25)))
    lo = subject_start - padding
    hi = end_eff + padding
    out: list[tuple[str, dict, str, int]] = []
    for t, occ, src, count in tags:
        ts = occ.get("start_year")
        if ts is None:
            out.append((t, occ, src, count))   # uncertain — don't filter
            continue
        te = occ.get("end_year") or ts
        if occ.get("is_ongoing"):
            te = max(te or ts, 2026)   # ongoing extends to now
        # Keep if the tag's date range OVERLAPS the padded subject window.
        if te < lo or ts > hi:
            continue
        out.append((t, occ, src, count))
    return out


# ---- Date inference from archive events --------------------------------------
def collect_event_years(eps_in_group: list[dict]) -> list[int]:
    """Pull all parseable years from archive historical_events strings across
    the group. Returns a flat sorted list (may include duplicates for stats)."""
    years: list[int] = []
    for ep in eps_in_group:
        a = ep.get("_archive") or {}
        for s in (a.get("historical_events") or []):
            start, end = parse_event_year(s)
            if start is not None:
                years.append(start)
            if end is not None:
                years.append(end)
    return sorted(years)


def infer_dates(eps_in_group: list[dict], tags: list[tuple[str, dict, str, int]],
                title_year: int | None = None) -> tuple[int | None, int | None, str]:
    """Returns (start, end, confidence_label).

    Tag preference order (highest first):
      a. ep_count (tag mentioned in most episodes of the group = central subject)
      b. main_priority (notability — breaks ties for single-ep items)
      c. proximity to median historical_event year (final tiebreaker)
    """
    # 1. Year baked into the item title — highest confidence.
    if title_year is not None:
        return title_year, None, "high"

    if tags:
        dated = [t for t in tags if t[1].get("start_year") is not None]
        if dated:
            ev_years = collect_event_years(eps_in_group)
            mid = ev_years[len(ev_years) // 2] if ev_years else 0
            # Composite score: (count desc, event>figure tiebreak, priority
            # desc, dist to mid asc). Events tend to BE the episode's topic;
            # figures are usually characters mentioned within the topic. So
            # when count is tied, prefer the event interpretation — fixes the
            # Helen of Troy case where Trojan War (event) and Socrates (figure)
            # both have count=2 but the show is clearly about Troy.
            # main_priority is DB-trigger-maintained — in master.py source it's
            # always None, so we read priorities["master"] directly.
            def score(t):
                title, occ, src, count = t
                pri = (occ.get("priorities") or {}).get("master") or 0
                src_rank = 0 if src == "event" else 1   # lower is better
                dist = abs((occ.get("start_year") or 0) - mid)
                return (-count, src_rank, -pri, dist)
            dated.sort(key=score)
            best = dated[0]
            occ = best[1]
            s = occ.get("start_year")
            e = None if occ.get("is_ongoing") else occ.get("end_year")
            if s is not None and e is not None and e <= s:
                e = None
            return s, e, "medium"

    # 3. Earliest event year from the archive's own list.
    ev_years = collect_event_years(eps_in_group)
    if ev_years:
        # Cluster: if all within 100 years, take min+max as period; else
        # take the median.
        unique = sorted(set(ev_years))
        if unique[-1] - unique[0] <= 100:
            return unique[0], (unique[-1] if unique[-1] != unique[0] else None), "low"
        return unique[len(unique) // 2], None, "low"

    return None, None, "thematic"


# ---- RSS <-> archive join -----------------------------------------------------
def join_rss_archive(rss: list[dict], arc: list[dict]) -> list[dict]:
    """Attach matching archive item to each RSS ep under '_archive'.
    Strategy: same-date exact -> single archive; collision -> title fuzzy
    -> fall back to ±1 day. Logs unmatched."""
    arc_by_date: dict[str, list[dict]] = defaultdict(list)
    for a in arc:
        if a.get("date"):
            arc_by_date[a["date"]].append(a)

    def fuzzy_title_match(rss_title: str, candidates: list[dict]) -> dict:
        rt = normalize_title(stem_of(rss_title))
        best = None
        best_score = 0
        for a in candidates:
            at = normalize_title(stem_of(a.get("title") or ""))
            # Token overlap
            rt_toks = set(re.findall(r"[a-z0-9]+", rt))
            at_toks = set(re.findall(r"[a-z0-9]+", at))
            if not rt_toks:
                continue
            score = len(rt_toks & at_toks) / max(len(rt_toks), 1)
            if score > best_score:
                best, best_score = a, score
        return best if best_score >= 0.3 else candidates[0]

    matched = 0
    for ep in rss:
        d = ep.get("pub_date")
        if not d:
            ep["_archive"] = None
            continue
        # Exact date
        cands = arc_by_date.get(d) or []
        # ±1 day fallback
        if not cands:
            try:
                base = date.fromisoformat(d)
                for delta in (-1, 1):
                    alt = (base + timedelta(days=delta)).isoformat()
                    cands = arc_by_date.get(alt) or []
                    if cands:
                        break
            except Exception:
                pass
        if not cands:
            ep["_archive"] = None
            continue
        ep["_archive"] = cands[0] if len(cands) == 1 else fuzzy_title_match(ep["title_clean"], cands)
        matched += 1
    print(f"  RSS→archive join: {matched}/{len(rss)} matched")
    return rss


# ---- Main --------------------------------------------------------------------
def main() -> int:
    rss = json.load(open(RSS_PATH, encoding="utf-8"))
    arc = json.load(open(ARC_PATH, encoding="utf-8"))
    print(f"Loaded {len(rss)} RSS episodes, {len(arc)} archive episodes")

    rss = join_rss_archive(rss, arc)

    title_idx, keyword_idx = build_master_index()
    print(f"Loaded master.py title index ({len(title_idx)} unique titles)")

    # Manual overrides (eps 1-300 hand-curated previously).
    try:
        from manual_curations import OVERRIDES  # type: ignore
    except Exception:
        OVERRIDES = {}
    print(f"Loaded {len(OVERRIDES)} manual overrides")

    # Group RSS eps into items (multi-part series detection).
    items: list[dict] = []
    current_group: list[dict] | None = None

    def flush():
        nonlocal current_group
        if current_group:
            stem = stem_of(current_group[0]["title_clean"])
            items.append({"_stem": stem, "episodes": current_group})
        current_group = None

    for e in rss:
        title = e["title_clean"]
        pn = part_number(title)
        if pn is not None:
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
            items.append({"_stem": title, "episodes": [e]})
    flush()

    print(f"Grouped into {len(items)} items "
          f"({sum(1 for it in items if len(it['episodes']) > 1)} multi-part, "
          f"{sum(1 for it in items if len(it['episodes']) == 1)} standalone)")

    # Build drafts.
    drafts: list[dict] = []
    for it in items:
        eps_in = it["episodes"]
        ep_nums = [e["ep_num"] for e in eps_in]
        first_ep = ep_nums[0]
        is_series = len(eps_in) > 1
        stem = it["_stem"]

        ep_payload = [
            {
                "title": e["title"],
                "url":   e["apple_url"],
                "date":  e["pub_date"],
            }
            for e in eps_in
        ]

        # Resource title.
        if is_series:
            resource_title = f"{stem} (TRIH eps {ep_nums[0]}-{ep_nums[-1]})"
        else:
            resource_title = f"{stem} (TRIH ep {first_ep})"

        # Description: prefer archive summary > archive description > longest RSS desc.
        desc = ""
        for ep in eps_in:
            a = ep.get("_archive") or {}
            for key in ("summary", "description"):
                cand = a.get(key) or ""
                if len(cand) > len(desc):
                    desc = cand
        if not desc:
            desc = max((e["description"] for e in eps_in), key=len, default="")

        # Tags from archive enrichment (UNFILTERED — date proximity filtered later).
        tag_tuples_all = collect_tags(eps_in, title_idx)

        # Title-year override.
        title_year_match = re.match(r"^(\d{4})\b", stem.strip())
        title_year = int(title_year_match.group(1)) if title_year_match else None

        # First-pass date inference (may be overridden below).
        subject_start, subject_end, confidence = infer_dates(
            eps_in, tag_tuples_all, title_year=title_year
        )

        # Apply manual override — wins on dates BEFORE we filter tags so the
        # proximity filter uses the right window (e.g. the Dinosaurs ep's
        # override pushes the window back to the Mesozoic, dropping Carnegie).
        override = OVERRIDES.get(first_ep, "_USE_AUTO")
        if override is None:
            # Skip: thematic / undatable per manual decision.
            drafts.append({
                "resource_title": resource_title, "ep_nums": ep_nums,
                "subject_start": None, "subject_end": None,
                "confidence": "skipped", "candidate_tags": [],
                "resource_episodes": ep_payload,
                "description": desc[:600], "_skip": True,
            })
            continue
        override_tags: list[str] | None = None
        if isinstance(override, dict):
            # If override sets "start", treat dates atomically — subject_end
            # comes from override["end"] (or None if not specified). Avoids
            # the case where infer_dates set an end from unrelated archive
            # events that doesn't apply once the start is overridden.
            if "start" in override:
                subject_start = override["start"]
                subject_end = override.get("end")
                confidence = "override"
            elif "end" in override:
                subject_end = override["end"]
            if "title" in override:
                resource_title = override["title"]
            if "tags" in override:
                override_tags = [t for t in override["tags"] if normalize_title(t) in title_idx]

        # Filter archive tags by date proximity to FINAL subject window.
        tag_tuples = filter_tags_by_proximity(tag_tuples_all, subject_start, subject_end)
        # Sort by (count desc, priority desc) — central subjects to the front.
        tag_tuples.sort(key=lambda t: (
            -t[3],
            -((t[1].get("priorities") or {}).get("master") or 0),
        ))
        candidate_tags = [t for t, _, _, _ in tag_tuples]

        # Merge with manual override tags if present (override tags first,
        # archive tags appended where not duplicated).
        if override_tags is not None:
            seen = {normalize_title(t) for t in override_tags}
            merged = list(override_tags)
            for t in candidate_tags:
                if normalize_title(t) not in seen:
                    seen.add(normalize_title(t))
                    merged.append(t)
            candidate_tags = merged

        candidate_tags = candidate_tags[:12]

        drafts.append({
            "resource_title":   resource_title,
            "ep_nums":          ep_nums,
            "subject_start":    subject_start,
            "subject_end":      subject_end,
            "confidence":       confidence,
            "candidate_tags":   candidate_tags,
            "description":      desc[:600],
            "resource_episodes": ep_payload,
        })

    # Sort chronologically by subject_start, ep_num.
    drafts.sort(key=lambda d: (
        d["subject_start"] if d["subject_start"] is not None else 10_000,
        d["ep_nums"][0],
    ))

    OUT.write_text(json.dumps(drafts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT.name}")

    by_conf = Counter(d["confidence"] for d in drafts)
    print()
    print("Confidence breakdown:")
    for k in ("override", "high", "medium", "low", "thematic", "skipped"):
        print(f"  {k:>9}: {by_conf.get(k, 0)}")
    print(f"  total: {len(drafts)}")

    no_tags = [d for d in drafts if not d["candidate_tags"] and not d.get("_skip")]
    print(f"\nNon-skipped items with NO tag matches: {len(no_tags)}")
    for d in no_tags[:15]:
        print(f"  eps {d['ep_nums']}: {d['resource_title']}")
    if len(no_tags) > 15:
        print(f"  ... and {len(no_tags) - 15} more")

    no_date = [d for d in drafts if d["subject_start"] is None and not d.get("_skip")]
    print(f"\nNon-skipped items with NO inferred date: {len(no_date)}")
    for d in no_date[:15]:
        print(f"  eps {d['ep_nums']}: {d['resource_title']}")
    if len(no_date) > 15:
        print(f"  ... and {len(no_date) - 15} more")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
