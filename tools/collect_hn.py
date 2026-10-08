"""Collect complete public HN comments. Never assigns labels or splits data."""
import csv
import hashlib
import html
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORIES = [41046773, 44163063, 46990729, 38544729, 48153379, 48292224, 48085821, 47340079]


class PlainText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ("p", "br", "pre"):
            self.parts.append("\n\n")

    def handle_endtag(self, tag):
        if tag in ("p", "pre"):
            self.parts.append("\n\n")

    def handle_data(self, data):
        self.parts.append(data)


def plaintext(raw):
    parser = PlainText()
    parser.feed(raw or "")
    return "".join(parser.parts).strip()


def fetch(story):
    request = urllib.request.Request(f"https://hn.algolia.com/api/v1/items/{story}", headers={"User-Agent": "TakeMeter-student-project/1.0"})
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.load(response)


def walk(item):
    for child in item.get("children", []):
        yield child
        yield from walk(child)


def main():
    directory = ROOT / "collection"
    directory.mkdir(exist_ok=True)
    fetched = list(ThreadPoolExecutor(max_workers=4).map(fetch, STORIES))
    pools = []
    seen = set()
    for story in fetched:
        pool = []
        for item in walk(story):
            raw = item.get("text") or ""
            text = plaintext(raw)
            words = len(text.split())
            normalized = re.sub(r"\s+", " ", text).casefold()
            # Select complete short comments; NEVER truncate an included post.
            if not (5 <= words <= 180) or normalized in seen or text in ("[deleted]", "[dead]"):
                continue
            seen.add(normalized)
            pool.append({"id": item["id"], "story_id": story["id"], "story_title": story["title"],
                         "source_url": f"https://news.ycombinator.com/item?id={item['id']}",
                         "created_at": item.get("created_at"), "text": text, "text_html": raw,
                         "sha256": hashlib.sha256(text.encode()).hexdigest()})
        pools.append(pool)
    chosen = []
    for offset in range(100):
        for pool in pools:
            if offset < len(pool):
                chosen.append(pool[offset])
            if len(chosen) == 260:
                break
        if len(chosen) == 260:
            break
    if len(chosen) < 240:
        raise RuntimeError(f"Only {len(chosen)} suitable complete comments")
    manifest = {"collected_at_utc": datetime.now(timezone.utc).isoformat(), "community": "Hacker News",
                "selection": "8 AI discussion threads; round-robin depth-first comments; 5–180 words, whole text; normalized duplicates excluded; no label-based selection",
                "posts": chosen}
    (directory / "sources.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    with (ROOT / "labels.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["text", "label", "note"])
        writer.writeheader()
        for i, post in enumerate(chosen):
            marker = "cold_pending" if i < 20 else "unlabeled"
            writer.writerow({"text": post["text"], "label": "", "note": f"{marker}; hn_id={post['id']}; source={post['source_url']}"})
    print(f"Collected {len(chosen)} whole comments from {len(fetched)} threads; 0 labels assigned.")


if __name__ == "__main__":
    main()
