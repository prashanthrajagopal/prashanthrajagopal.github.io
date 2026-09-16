#!/usr/bin/env python3
"""
Generate site/feed.xml (RSS 2.0) from docs/blog/posts/*.md after `zensical build`.

Run after the build, before generate_sitemap.py. Requires PyYAML.
"""
from __future__ import annotations

import html
import os
import re
import sys
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("generate_feed.py: install PyYAML: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "docs" / "blog" / "posts"
BASE = os.environ.get("SITE_URL", "https://prashanthr.net").rstrip("/")
SITE = Path(os.environ.get("SITE_DIR", "site"))
MAX_ITEMS = 20

esc = html.escape


def summary(body: str) -> str:
    if "<!-- more -->" in body:
        body = body.split("<!-- more -->", 1)[0]
    text = re.sub(r"^#+\s+.*$", "", body.strip(), flags=re.MULTILINE)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = " ".join(text.split())
    return text[:497] + "…" if len(text) > 500 else text


def pub_date(raw) -> datetime:
    if hasattr(raw, "timetuple"):
        t = raw.timetuple()
        return datetime(t.tm_year, t.tm_mon, t.tm_mday, 9, 0, tzinfo=timezone.utc)
    y, m, d = (int(x) for x in str(raw)[:10].split("-"))
    return datetime(y, m, d, 9, 0, tzinfo=timezone.utc)


def main() -> None:
    if not SITE.is_dir():
        sys.exit("generate_feed.py: site/ not found — run zensical build first")

    items = []
    for path in sorted(POSTS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        end = text.find("\n---\n", 3)
        fm = yaml.safe_load(text[3:end]) or {}
        if fm.get("draft") or not fm.get("date"):
            continue
        url = f"{BASE}/blog/posts/{path.stem}/"
        cats = fm.get("categories") or []
        items.append({
            "title": str(fm.get("title", path.stem)),
            "url": url,
            "date": pub_date(fm["date"]),
            "description": str(fm.get("description") or summary(text[end + 5:])),
            "categories": [str(c) for c in cats] + [str(t) for t in (fm.get("tags") or [])],
            "image": f"{BASE}/assets/og/blog-{path.stem}.png",
        })

    items.sort(key=lambda i: i["date"], reverse=True)
    items = items[:MAX_ITEMS]
    built = format_datetime(items[0]["date"]) if items else format_datetime(datetime.now(timezone.utc))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/">',
        "  <channel>",
        "    <title>Prashanth Rajagopal — prashanthr.net</title>",
        f"    <link>{BASE}/blog/</link>",
        "    <description>Long-form writing on distributed systems, agent infrastructure, Rails, Go, IoT and electronics.</description>",
        "    <language>en</language>",
        f"    <lastBuildDate>{built}</lastBuildDate>",
        f'    <atom:link href="{BASE}/feed.xml" rel="self" type="application/rss+xml"/>',
        "    <managingEditor>noreply@prashanthr.net (Prashanth Rajagopal)</managingEditor>",
    ]
    for it in items:
        lines += [
            "    <item>",
            f"      <title>{esc(it['title'])}</title>",
            f"      <link>{it['url']}</link>",
            f"      <guid isPermaLink=\"true\">{it['url']}</guid>",
            f"      <pubDate>{format_datetime(it['date'])}</pubDate>",
            f"      <description>{esc(it['description'])}</description>",
            *[f"      <category>{esc(c)}</category>" for c in it["categories"]],
            f'      <enclosure url="{it["image"]}" type="image/png" length="0"/>',
            "    </item>",
        ]
    lines += ["  </channel>", "</rss>"]

    (SITE / "feed.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"generate_feed.py: {len(items)} items → feed.xml")


if __name__ == "__main__":
    main()
