"""
Monthly database freshness check + update orchestrator for Ever-When.

Run once a month (or whenever) to:

  1. Re-fetch RSS / archive metadata for every "episodic" resource
     (currently just The Rest Is History — adding new podcasts means adding
     a new entry to EPISODIC_RESOURCES below). Report new episode counts
     so you know whether a re-import is worth doing.

  2. Surface `is_ongoing=True` entries (active reigns, ongoing wars, sitting
     popes, etc.) for review — these go stale when reality catches up.
     Each one needs a human check: is X still going? If not, set end_year
     and clear is_ongoing.

  3. Surface still-living persons (type=person, is_full_life, end_year null)
     for the same sanity check.

  4. Compute "data freshness" — how long since the master.py was last
     imported to hosted Supabase.

The script DOES NOT auto-apply changes. It prints a structured report;
Claude (via the monthly-update SKILL) reads the report and walks you
through each curation decision interactively.

Usage from `tools/`:
    .venv\\Scripts\\python.exe -m v2.curation.monthly_update

Optional flags:
    --json          machine-readable JSON output instead of human-readable
    --no-fetch      skip the network round-trips (just use cached data)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

# State file lives next to this script so it's checked into git — that way
# the "last seen episode count" survives across machines.
STATE_PATH = Path(__file__).parent / "monthly_update_state.json"

# --------------------------------------------------------------------------- #
# REGISTRY: episodic resources whose source feeds we should re-fetch.
#
# When you add a NEW episodic resource module to tools/v2/data/, register it
# here so the monthly check covers it. Each entry tells the script which
# fetcher to re-run and how to count episodes in the result.
#
# The pipeline contract is:
#   parser    → reads source feed, emits tools/v2/data/_research/<x>_raw.json
#   fetcher   → fetches per-episode detail JSON (optional but recommended)
#   curator   → builds the curated draft (handles series-bundling — see notes)
#   generator → writes the final data module (the_rest_is_history.py etc.)
# --------------------------------------------------------------------------- #

EPISODIC_RESOURCES: list[dict] = [
    {
        "name": "The Rest Is History",
        "data_module": "v2.data.the_rest_is_history",
        "id_range": (1_008_000, 1_008_999),
        # Pipeline steps to re-run (as Python -m module paths). Order matters.
        "pipeline": [
            "v2.data._research.parse_trih_rss",
            "v2.data._research.fetch_trih_archive",
            "v2.data._research.curate_trih_v2",
            "v2.data._research.generate_trih_module_v2",
        ],
        # Where the parser dumps the raw episode list — we read it after
        # re-running the parser to count episodes for the report.
        "raw_episode_count_path": "tools/v2/data/_research/trih_episodes_raw.json",
    },
    # Add new episodic resources here, e.g.:
    # {
    #     "name": "Empire",
    #     "data_module": "v2.data.empire_podcast",
    #     "id_range": (1_010_000, 1_010_999),
    #     "pipeline": [...],
    #     "raw_episode_count_path": "...",
    # },
]

# Persons born after this year are presumed potentially still alive — older
# ones with no end_year are flagged as data quality issues (probably just
# missing the death year, not "still living").
MAX_PLAUSIBLE_BIRTH_FOR_LIVING = date.today().year - 110


# --------------------------------------------------------------------------- #
# Report data classes
# --------------------------------------------------------------------------- #

@dataclass
class EpisodicResourceReport:
    name: str
    last_seen_episodes: int | None
    current_episodes: int | None
    new_episodes: int | None
    error: str | None = None


@dataclass
class OngoingEntry:
    id: int
    title: str
    type: str
    start_year: int | None
    years_ongoing: int | None
    notes: str = ""


@dataclass
class Report:
    generated_at: str
    days_since_last_update: int | None
    episodic_resources: list[EpisodicResourceReport] = field(default_factory=list)
    ongoing_entries: list[OngoingEntry] = field(default_factory=list)
    living_persons: list[OngoingEntry] = field(default_factory=list)
    # Persons born >110 years ago with no end_year — almost certainly stale
    # (just missing death year, not actually living).
    suspicious_living: list[OngoingEntry] = field(default_factory=list)


# --------------------------------------------------------------------------- #
# State persistence
# --------------------------------------------------------------------------- #

def load_state() -> dict:
    if not STATE_PATH.exists():
        return {}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"WARN: state file {STATE_PATH.name} unreadable ({e}); starting fresh")
        return {}


def save_state(state: dict) -> None:
    STATE_PATH.write_text(
        json.dumps(state, indent=2, sort_keys=True), encoding="utf-8",
    )


# --------------------------------------------------------------------------- #
# Check 1: episodic resources
# --------------------------------------------------------------------------- #

def check_episodic_resources(
    state: dict, do_fetch: bool,
) -> list[EpisodicResourceReport]:
    out: list[EpisodicResourceReport] = []
    last_seen = state.get("episodic_resources", {})
    for resource in EPISODIC_RESOURCES:
        name = resource["name"]
        prev = last_seen.get(name, {}).get("episode_count")
        try:
            if do_fetch:
                # Re-run the PARSER step only — that's the cheap RSS pull.
                # The full fetcher (per-episode detail) runs only when the
                # user confirms via the skill workflow.
                parser_mod = resource["pipeline"][0]
                _run_module(parser_mod)
            count = _count_episodes(resource["raw_episode_count_path"])
            new_count = count - prev if prev is not None else None
            out.append(EpisodicResourceReport(
                name=name,
                last_seen_episodes=prev,
                current_episodes=count,
                new_episodes=new_count,
            ))
        except Exception as e:
            out.append(EpisodicResourceReport(
                name=name,
                last_seen_episodes=prev,
                current_episodes=None,
                new_episodes=None,
                error=str(e),
            ))
    return out


def _count_episodes(rel_path: str) -> int:
    p = ROOT.parent / rel_path
    data = json.loads(p.read_text(encoding="utf-8"))
    return len(data)


def _run_module(mod: str) -> None:
    """Invoke `python -m <mod>` via runpy so we don't shell out."""
    import runpy
    # runpy chokes if argv isn't reset; save and restore.
    saved_argv = sys.argv[:]
    sys.argv = [mod]
    try:
        runpy.run_module(mod, run_name="__main__")
    finally:
        sys.argv = saved_argv


# --------------------------------------------------------------------------- #
# Check 2: ongoing entries
# --------------------------------------------------------------------------- #

def check_ongoing_entries() -> tuple[list[OngoingEntry], list[OngoingEntry], list[OngoingEntry]]:
    """Returns (ongoing, living_persons, suspicious_living)."""
    from v2.data.master import OCCURRENCES
    current_year = date.today().year
    ongoing: list[OngoingEntry] = []
    living: list[OngoingEntry] = []
    suspicious: list[OngoingEntry] = []
    for o in OCCURRENCES:
        start = o.get("start_year")
        years_ongoing = (current_year - start) if isinstance(start, int) else None

        if o.get("is_ongoing"):
            ongoing.append(OngoingEntry(
                id=o["id"],
                title=o.get("title", ""),
                type=o.get("type", ""),
                start_year=start,
                years_ongoing=years_ongoing,
                notes="is_ongoing=True — confirm still active",
            ))

        # Full-life person with no end_year and not explicitly is_ongoing →
        # split into "plausibly living" vs "suspicious / probably stale".
        if (
            o.get("type") == "person"
            and o.get("is_full_life")
            and o.get("end_year") is None
            and not o.get("is_ongoing")
        ):
            entry = OngoingEntry(
                id=o["id"],
                title=o.get("title", ""),
                type="person",
                start_year=start,
                years_ongoing=years_ongoing,
            )
            if isinstance(start, int) and start < MAX_PLAUSIBLE_BIRTH_FOR_LIVING:
                entry.notes = (
                    f"Born {start} → would be {years_ongoing}+ years old. "
                    f"Likely missing death year (data quality)."
                )
                suspicious.append(entry)
            else:
                entry.notes = "Confirm still living"
                living.append(entry)
    return ongoing, living, suspicious


# --------------------------------------------------------------------------- #
# Check 3: data freshness (vs hosted Supabase)
# --------------------------------------------------------------------------- #

def check_data_freshness() -> int | None:
    """Compare the most-recent imported occurrence to today. Returns days
    since the latest occurrence was inserted/updated, or None if the env
    isn't configured to reach Supabase."""
    if not os.environ.get("SUPABASE_URL"):
        # Try loading .env if present.
        try:
            from dotenv import load_dotenv
            load_dotenv(ROOT.parent / ".env")
        except Exception:
            return None
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not (url and key):
        return None
    try:
        from supabase import create_client
        sb = create_client(url, key)
        r = (
            sb.table("occurrences")
            .select("updated_at")
            .order("updated_at", desc=True)
            .limit(1)
            .execute()
        )
        if not r.data:
            return None
        ts = r.data[0].get("updated_at")
        if not ts:
            return None
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - dt).days
    except Exception as e:
        print(f"WARN: freshness check failed: {e}")
        return None


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def build_report(do_fetch: bool) -> Report:
    state = load_state()
    episodic = check_episodic_resources(state, do_fetch=do_fetch)
    ongoing, living, suspicious = check_ongoing_entries()
    freshness = check_data_freshness()
    return Report(
        generated_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        days_since_last_update=freshness,
        episodic_resources=episodic,
        ongoing_entries=ongoing,
        living_persons=living,
        suspicious_living=suspicious,
    )


def update_state_after_import(report: Report) -> None:
    """Call AFTER you've actually re-imported. Bumps the last-seen episode
    count for each episodic resource so the next run's `new_episodes`
    delta is accurate. (Not called automatically by build_report — the
    skill workflow calls it once the import has succeeded.)"""
    state = load_state()
    state.setdefault("episodic_resources", {})
    for r in report.episodic_resources:
        if r.current_episodes is not None:
            state["episodic_resources"][r.name] = {
                "episode_count": r.current_episodes,
                "last_checked": report.generated_at,
            }
    save_state(state)


def print_human(report: Report) -> None:
    print(f"Monthly database freshness check — {report.generated_at}")
    print()

    if report.days_since_last_update is None:
        print("Data freshness: (could not reach hosted Supabase)")
    else:
        print(f"Data freshness: last occurrence write was "
              f"{report.days_since_last_update} day(s) ago")
    print()

    print(f"==== Episodic resources ({len(report.episodic_resources)}) ====")
    for r in report.episodic_resources:
        if r.error:
            print(f"  {r.name}: ERROR — {r.error}")
            continue
        delta = (
            f"+{r.new_episodes} new" if (r.new_episodes and r.new_episodes > 0)
            else "no new episodes" if r.new_episodes == 0
            else "(first run — no baseline)"
        )
        print(f"  {r.name}: now {r.current_episodes} eps "
              f"(was {r.last_seen_episodes}); {delta}")
    print()

    print(f"==== `is_ongoing` entries ({len(report.ongoing_entries)}) ====")
    print("    Review each: has the period actually ended? If so, set end_year")
    print("    and clear is_ongoing.")
    for e in report.ongoing_entries:
        print(f"  id={e.id} {e.title!r} (started {e.start_year}, "
              f"{e.years_ongoing}yr ongoing)")
    print()

    print(f"==== Living persons ({len(report.living_persons)}) — sanity check ====")
    for e in report.living_persons:
        age = e.years_ongoing
        print(f"  id={e.id} {e.title!r} (b. {e.start_year}, ~{age} yo)")
    print()

    if report.suspicious_living:
        print(f"==== Suspicious 'living' entries ({len(report.suspicious_living)}) ====")
        print("    Person rows missing end_year despite being born >110yr ago.")
        print("    Almost certainly a data-quality gap — find the death year.")
        for e in report.suspicious_living:
            print(f"  id={e.id} {e.title!r} (b. {e.start_year})")
        print()


def print_json(report: Report) -> None:
    # Custom JSON encode (dataclasses → dicts).
    def encode(obj):
        if hasattr(obj, "__dataclass_fields__"):
            return asdict(obj)
        return str(obj)
    print(json.dumps(report, default=encode, indent=2, ensure_ascii=False))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true",
                    help="emit machine-readable JSON instead of a human report")
    ap.add_argument("--no-fetch", action="store_true",
                    help="skip the RSS re-pull (use cached data only)")
    ap.add_argument("--mark-imported", action="store_true",
                    help="update state file with the current episode counts "
                         "(call AFTER you've imported the new data)")
    args = ap.parse_args()
    report = build_report(do_fetch=not args.no_fetch)
    if args.mark_imported:
        update_state_after_import(report)
        print(f"State file updated: {STATE_PATH.name}")
        return 0
    if args.json:
        print_json(report)
    else:
        print_human(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
