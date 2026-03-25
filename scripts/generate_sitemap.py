#!/usr/bin/env python3
"""
Generate site/sitemap.xml and site/robots.txt after `zensical build`.
Uses every .../index.html under site/ (excludes standalone 404.html).
"""
from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = os.environ.get("SITE_URL", "https://prashanthr.net").rstrip("/")
SITE = Path(os.environ.get("SITE_DIR", "site"))


def esc_xml(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def main() -> None:
    if not SITE.is_dir():
        print("generate_sitemap.py: site/ not found — run zensical build first", file=sys.stderr)
        sys.exit(1)

    entries: list[tuple[str, str, str, str]] = []
    for html in sorted(SITE.rglob("index.html")):
        rel = html.relative_to(SITE)
        parent = rel.parent
        if parent == Path("."):
            path = "/"
        else:
            path = "/" + parent.as_posix().strip("/") + "/"
        lastmod = datetime.fromtimestamp(
            html.stat().st_mtime, tz=timezone.utc
        ).strftime("%Y-%m-%d")
        if path == "/":
            priority = "1.0"
        elif path.startswith("/blog"):
            priority = "0.85"
        else:
            priority = "0.7"
        entries.append((path, lastmod, "weekly", priority))

    entries.sort(key=lambda x: x[0])

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path, lastmod, changefreq, priority in entries:
        loc = f"{BASE}/" if path == "/" else f"{BASE}{path}"
        lines.append("  <url>")
        lines.append(f"    <loc>{esc_xml(loc)}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>{changefreq}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")

    sitemap_path = SITE / "sitemap.xml"
    sitemap_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    robots = SITE / "robots.txt"
    robots.write_text(
        "# prashanthr.net\n"
        "User-agent: *\nAllow: /\n\n"
        "# AI crawlers welcome\n"
        "User-agent: GPTBot\nAllow: /\n\n"
        "User-agent: ClaudeBot\nAllow: /\n\n"
        "User-agent: PerplexityBot\nAllow: /\n\n"
        f"Sitemap: {BASE}/sitemap.xml\n",
        encoding="utf-8",
    )
    print(f"generate_sitemap.py: {len(entries)} URLs → {sitemap_path.name}, robots.txt")


if __name__ == "__main__":
    main()
