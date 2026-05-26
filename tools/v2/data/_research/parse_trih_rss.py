"""
Parse The Rest Is History RSS feed (Megaphone) into a JSON list of the
first 300 numbered episodes in chronological order. Output is written to
`trih_episodes_raw.json` for the curation script to consume.

For each episode we capture:
    title, episode_number, pub_date, description (raw HTML stripped to text),
    apple_url, megaphone_guid, duration_sec

We DON'T try to determine the historical subject date here — that's done in
the curation script, which adds tags + dates against master.py.
"""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path

HERE = Path(__file__).resolve().parent
RSS_PATH = HERE / "trih_rss.xml"
OUT_PATH = HERE / "trih_episodes_raw.json"

NS = {
    "itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
    "content": "http://purl.org/rss/1.0/modules/content/",
}

# Match a title's leading episode number: "1. Foo", "100. Foo", "282: Foo",
# "100. Decolonising Africa". Captures the numeric prefix.
EP_NUM_RE = re.compile(r"^(\d{1,4})\s*[:.]\s+")


def strip_html(s: str) -> str:
    """Brutal but adequate: drop tags, decode entities, collapse whitespace.
    We only need this for a clean one-line description — the original HTML
    is preserved in resource_episodes if the user wants it later."""
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def parse_duration(s: str | None) -> int | None:
    """itunes:duration is either seconds (string int) or HH:MM:SS / MM:SS."""
    if not s:
        return None
    s = s.strip()
    if s.isdigit():
        return int(s)
    parts = [int(p) for p in s.split(":") if p.strip().isdigit()]
    if len(parts) == 3:
        h, m, sec = parts
        return h * 3600 + m * 60 + sec
    if len(parts) == 2:
        m, sec = parts
        return m * 60 + sec
    return None


def main() -> int:
    tree = ET.parse(RSS_PATH)
    root = tree.getroot()
    items = root.findall("./channel/item")
    items_chrono = list(reversed(items))  # oldest first
    print(f"Feed items (total): {len(items_chrono)}")

    out: list[dict] = []
    for it in items_chrono:
        title = (it.findtext("title") or "").strip()
        m = EP_NUM_RE.match(title)
        if not m:
            # Trailers, bonus episodes, ads — skip for the first-300 scope.
            continue
        ep_num = int(m.group(1))
        pub_raw = it.findtext("pubDate") or ""
        pub_iso = None
        if pub_raw:
            try:
                pub_iso = parsedate_to_datetime(pub_raw).date().isoformat()
            except Exception:
                pub_iso = None
        link = it.findtext("link") or ""
        guid = it.findtext("guid") or ""
        duration = parse_duration(it.findtext("itunes:duration", namespaces=NS))
        # RSS <link> is empty for TRIH. Use the audio enclosure URL — it's
        # the most stable direct-to-episode link the feed exposes.
        enclosure = it.find("enclosure")
        audio_url = enclosure.get("url") if enclosure is not None else None
        if not link and audio_url:
            link = audio_url
        description_html = it.findtext("description") or ""
        description = strip_html(description_html)
        # Crop the "Learn more about your ad choices" boilerplate that Megaphone
        # appends to every description.
        for boiler in [
            "Learn more about your ad choices.",
            "Visit podcastchoices.com",
            "Visit megaphone.fm/adchoices",
        ]:
            idx = description.find(boiler)
            if idx > 0:
                description = description[:idx].strip()

        out.append({
            "ep_num":       ep_num,
            "title":        title,
            "title_clean":  title[m.end():],  # title with episode-number prefix stripped
            "pub_date":     pub_iso,
            "apple_url":    link,
            "megaphone_guid": guid,
            "duration_sec": duration,
            "description":  description[:600],   # cap to a reasonable size
        })

    # Keep only the first 300 numbered episodes in chronological order.
    out_300 = out[:300]
    print(f"Numbered episodes parsed: {len(out)}")
    print(f"Returning first 300 in chronological order")
    print(f"  oldest: ep {out_300[0]['ep_num']} ({out_300[0]['pub_date']}) {out_300[0]['title_clean']!r}")
    print(f"  newest: ep {out_300[-1]['ep_num']} ({out_300[-1]['pub_date']}) {out_300[-1]['title_clean']!r}")

    OUT_PATH.write_text(json.dumps(out_300, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
