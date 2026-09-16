#!/usr/bin/env python3
"""
Generate site/sitemap.xml and site/robots.txt after `zensical build`.
Uses every .../index.html under site/ (excludes standalone 404.html).
"""
from __future__ import annotations

import os
import subprocess
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


ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
_git_cache: dict[Path, str] = {}


def source_for(path: str) -> Path | None:
    """Map a built URL path back to the file that actually authors it."""
    rel = path.strip("/")
    if not rel:
        return DOCS / "index.md"
    parts = rel.split("/")
    if parts[:2] == ["roadtrips"] and len(parts) == 2:
        data = ROOT / "roadtrips" / f"{parts[1]}.json"   # trip pages are generated from JSON
        if data.is_file():
            return data
    for candidate in (DOCS / f"{rel}.md", DOCS / rel / "index.md"):
        if candidate.is_file():
            return candidate
    return None


def last_modified(path: str, fallback: Path) -> str:
    """Last git commit date of the source file; falls back to file mtime."""
    src = source_for(path)
    if src is not None:
        if src not in _git_cache:
            try:
                out = subprocess.run(
                    ["git", "log", "-1", "--format=%cI", "--", str(src.relative_to(ROOT))],
                    cwd=ROOT, capture_output=True, text=True, timeout=20,
                )
                _git_cache[src] = out.stdout.strip()[:10] if out.returncode == 0 else ""
            except Exception:
                _git_cache[src] = ""
        if _git_cache[src]:
            return _git_cache[src]
    return datetime.fromtimestamp(fallback.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%d")


def rank(path: str) -> tuple[str, str]:
    """(changefreq, priority) — newest, most linkable content first."""
    if path == "/":
        return "daily", "1.0"
    if path in ("/blog/", "/roadtrips/", "/astra/"):
        return "weekly", "0.9"
    if path.startswith("/blog/posts/"):
        return "monthly", "0.9"
    if path.startswith("/roadtrips/"):
        return "monthly", "0.8"
    if path.startswith("/blog/"):
        return "weekly", "0.5"          # archive / category pages
    if path.startswith("/wiki/astra/"):
        return "monthly", "0.7"
    return "monthly", "0.6"


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
        lastmod = last_modified(path, html)
        changefreq, priority = rank(path)
        entries.append((path, lastmod, changefreq, priority))

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
        "User-agent: Google-Extended\nAllow: /\n\n"
        "User-agent: CCBot\nAllow: /\n\n"
        f"Sitemap: {BASE}/sitemap.xml\n",
        encoding="utf-8",
    )
    print(f"generate_sitemap.py: {len(entries)} URLs → {sitemap_path.name}, robots.txt")


if __name__ == "__main__":
    main()
