"""
Fetch every TRIH episode from archive.therestishistory.com and cache to JSON.

The archive's per-episode endpoint returns rich, human-curated metadata that
the Megaphone RSS feed doesn't expose:

    historical_events:   list[str]   e.g. "Battle of the Somme (1916)"
    historical_figures:  list[str]   e.g. "Murasaki Shikibu"
    books:               list[dict]  [{author, title}, ...]
    eras:                list[dict]  [{id, name, description}, ...]
    summary:             str         (longer than RSS description)
    series_name:         str         when episode is part of a multi-parter
    part_number:         str

We use this to (a) backfill the 370+ episodes we never curated and (b) retag
the existing 181 with much better subject matching than the regex heuristics
in `curate_trih.py`.

Usage (from `tools/`):
    .venv\\Scripts\\python.exe -m v2.data._research.fetch_trih_archive

Idempotent — already-cached episodes are skipped unless --refresh is passed.
Throttles to ~5 req/sec to be polite to a small fan-run site.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
LIST_PATH = HERE / "trih_archive_list.json"
DETAIL_DIR = HERE / "trih_archive_detail"
MERGED_PATH = HERE / "trih_archive_raw.json"

BASE = "https://archive.therestishistory.com/api/catalog"
UA = "Mozilla/5.0 (compatible; EverWhenBot/1.0; +https://ever-when.com)"

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": UA, "Accept": "application/json"})


def fetch_list() -> list[dict]:
    """Pull every episode summary in one request (page_size=2000 returns all)."""
    print("Fetching episode list...")
    r = SESSION.get(f"{BASE}/episodes", params={"page_size": 2000}, timeout=30)
    r.raise_for_status()
    data = r.json()
    eps = data["episodes"]
    print(f"  got {len(eps)} episodes (total reported: {data.get('total')})")
    LIST_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  cached -> {LIST_PATH.name}")
    return eps


def fetch_detail(archive_id: int, throttle_s: float = 0.2) -> dict:
    """Fetch one episode's enriched detail and cache it."""
    cache = DETAIL_DIR / f"{archive_id}.json"
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    r = SESSION.get(f"{BASE}/episode/{archive_id}", timeout=30)
    if r.status_code == 404:
        # Some IDs in the gap-numbered range may genuinely not exist.
        # Cache an empty marker so we don't refetch.
        data = {"id": archive_id, "_missing": True}
        cache.write_text(json.dumps(data), encoding="utf-8")
        return data
    r.raise_for_status()
    data = r.json()
    cache.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    time.sleep(throttle_s)
    return data


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true",
                    help="Re-fetch even cached episodes (default: skip cached)")
    ap.add_argument("--throttle", type=float, default=0.2,
                    help="Seconds between requests (default 0.2 = 5 req/sec)")
    args = ap.parse_args()

    DETAIL_DIR.mkdir(exist_ok=True)

    eps = fetch_list()
    ids = sorted({e["id"] for e in eps})
    print(f"Unique archive IDs: {len(ids)} ({min(ids)}..{max(ids)})")

    if args.refresh:
        for cache in DETAIL_DIR.glob("*.json"):
            cache.unlink()
        print("  cleared existing detail cache")

    cached_before = len(list(DETAIL_DIR.glob("*.json")))
    print(f"Cached details before run: {cached_before}")

    detailed: list[dict] = []
    fetched_now = 0
    for i, archive_id in enumerate(ids, 1):
        cache = DETAIL_DIR / f"{archive_id}.json"
        was_cached = cache.exists()
        d = fetch_detail(archive_id, throttle_s=args.throttle)
        if not was_cached:
            fetched_now += 1
        detailed.append(d)
        if i % 50 == 0 or i == len(ids):
            print(f"  [{i}/{len(ids)}] (fetched this run: {fetched_now})")

    # Filter missing-markers out of the merged dump.
    detailed_ok = [d for d in detailed if not d.get("_missing")]
    print(f"Detail fetches: {len(detailed_ok)} ok, {len(detailed) - len(detailed_ok)} missing")

    MERGED_PATH.write_text(
        json.dumps(detailed_ok, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote merged -> {MERGED_PATH.name} ({MERGED_PATH.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
