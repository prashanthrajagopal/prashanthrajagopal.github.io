#!/usr/bin/env python3
"""
Notify search engines after deploy:
 - IndexNow (Bing, Yandex, DuckDuckGo, Naver) — submit URLs from live sitemap

Requires INDEXNOW_KEY env var. Generate any UUID-like string and store it as a
GitHub secret. The CI writes a matching <key>.txt into site/.

Note: Google deprecated sitemap pings in June 2023. Google discovers URLs via
Search Console sitemap submission and natural crawling — no ping needed.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET

BASE = os.environ.get("SITE_URL", "https://prashanthr.net").rstrip("/")
INDEXNOW_KEY = os.environ.get("INDEXNOW_KEY", "")
UA = "prashanthr.net-deploy/1.0"


def fetch_urls_from_sitemap() -> list[str]:
    """Fetch URL list from the live sitemap.xml."""
    sitemap_url = f"{BASE}/sitemap.xml"
    try:
        req = urllib.request.Request(sitemap_url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=15) as resp:
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
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": UA,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"  IndexNow: {resp.status} ({len(urls)} URLs submitted)")
    except urllib.error.HTTPError as e:
        # IndexNow returns 200 or 202 on success; some codes are still OK
        if e.code == 202:
            print(f"  IndexNow: 202 Accepted ({len(urls)} URLs submitted)")
        else:
            print(f"  IndexNow failed: {e.code} {e.reason}", file=sys.stderr)
    except Exception as e:
        print(f"  IndexNow failed: {e}", file=sys.stderr)


def main() -> None:
    print("ping_search_engines.py:")
    ping_indexnow()


if __name__ == "__main__":
    main()
