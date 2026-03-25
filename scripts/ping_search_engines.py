#!/usr/bin/env python3
"""
Ping search engines after deploy:
 1. Google — ping sitemap URL
 2. IndexNow (Bing, Yandex, DuckDuckGo, Naver) — submit URLs from live sitemap

Requires INDEXNOW_KEY env var for IndexNow. Generate any UUID-like string and
store it as a GitHub secret. The CI writes a matching <key>.txt into site/.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET

BASE = os.environ.get("SITE_URL", "https://prashanthr.net").rstrip("/")
INDEXNOW_KEY = os.environ.get("INDEXNOW_KEY", "")


def ping_google() -> None:
    """Ping Google with the sitemap URL."""
    url = f"https://www.google.com/ping?sitemap={BASE}/sitemap.xml"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"  Google ping: {resp.status}")
    except Exception as e:
        print(f"  Google ping failed: {e}", file=sys.stderr)


def fetch_urls_from_sitemap() -> list[str]:
    """Fetch URL list from the live sitemap.xml."""
    sitemap_url = f"{BASE}/sitemap.xml"
    try:
        with urllib.request.urlopen(sitemap_url, timeout=15) as resp:
            tree = ET.parse(resp)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        return [loc.text for loc in tree.findall(".//sm:loc", ns) if loc.text]
    except Exception as e:
        print(f"  Failed to fetch sitemap: {e}", file=sys.stderr)
        return []


def ping_indexnow() -> None:
    """Submit all site URLs via IndexNow API."""
    if not INDEXNOW_KEY:
        print("  IndexNow: skipped (no INDEXNOW_KEY)", file=sys.stderr)
        return

    urls = fetch_urls_from_sitemap()
    if not urls:
        print("  IndexNow: no URLs found", file=sys.stderr)
        return

    payload = {
        "host": BASE.replace("https://", "").replace("http://", ""),
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE}/{INDEXNOW_KEY}.txt",
        "urlList": urls,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"  IndexNow: {resp.status} ({len(urls)} URLs submitted)")
    except Exception as e:
        print(f"  IndexNow failed: {e}", file=sys.stderr)


def main() -> None:
    print("ping_search_engines.py:")
    ping_google()
    ping_indexnow()


if __name__ == "__main__":
    main()
