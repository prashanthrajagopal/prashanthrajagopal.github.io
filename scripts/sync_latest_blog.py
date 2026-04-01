#!/usr/bin/env python3
"""
Update docs/index.md "Latest from the blog" from the post with the newest `date:` in frontmatter.
Run before `zensical build` / `zensical serve` (requires PyYAML: pip install pyyaml).
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("sync_latest_blog.py: install PyYAML: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "docs" / "blog" / "posts"
INDEX = ROOT / "docs" / "index.md"

MARK_START = "<!-- LATEST_BLOG_AUTOGEN_START -->"
MARK_END = "<!-- LATEST_BLOG_AUTOGEN_END -->"

MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def _parse_date(raw) -> tuple:
    """Return (year, month, day) for sorting."""
    if hasattr(raw, "timetuple"):
        t = raw.timetuple()
        return (t.tm_year, t.tm_mon, t.tm_mday)
    s = str(raw)[:10]
    y, m, d = (int(x) for x in s.split("-"))
    return (y, m, d)


def _format_date(raw) -> str:
    y, m, d = _parse_date(raw)
    return f"{d} {MONTHS[m - 1]} {y}"


def _excerpt(body: str) -> str:
    if "<!-- more -->" in body:
        body = body.split("<!-- more -->", 1)[0]
    para = body.strip().split("\n\n")[0]
    para = re.sub(r"^#+\s+.*$", "", para, flags=re.MULTILINE)
    para = re.sub(r"\*\*([^*]+)\*\*", r"\1", para)
    para = re.sub(r"\*([^*]+)\*", r"\1", para)
    para = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", para)
    para = " ".join(para.split())
    if len(para) > 260:
        para = para[:257].rsplit(" ", 1)[0] + "…"
    return para


def _tag_class(category: str) -> str:
    c = (category or "").lower()
    if "astra" in c:
        return "tag-astra"
    return "tag-architecture"


def load_post(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---\n", 3)
    if end == -1:
        return None
    fm = yaml.safe_load(text[3:end]) or {}
    if fm.get("draft"):
        return None
    raw_date = fm.get("date")
    if not raw_date:
        return None
    title = fm.get("title") or path.stem.replace("-", " ").title()
    cats = fm.get("categories") or []
    category = cats[0] if isinstance(cats, list) and cats else "Blog"
    body = text[end + 5 :]
    return {
        "sort_key": _parse_date(raw_date),
        "date_display": _format_date(raw_date),
        "title": title,
        "category": str(category),
        "slug": path.stem,
        "excerpt": _excerpt(body),
    }


NUM_RECENT = 5


def build_card(posts: list[dict]) -> str:
    lines = [f"  {MARK_START}"]
    for p in posts[:NUM_RECENT]:
        href = html.escape(f"blog/posts/{p['slug']}/", quote=True)
        title_e = html.escape(p["title"])
        cat_e = html.escape(p["category"])
        tag = _tag_class(p["category"])
        lines.append(
            f'      <a class="pr-recent-row" href="{href}">'
            f'<span class="post-date">{html.escape(p["date_display"])}</span>'
            f'<span class="pr-recent-title-text">{title_e}</span>'
            f'<span class="post-tag {tag}">{cat_e}</span>'
            f"</a>"
        )
    lines.append(f"  {MARK_END}")
    return "\n".join(lines)


def main() -> None:
    posts = []
    for path in sorted(POSTS_DIR.glob("*.md")):
        meta = load_post(path)
        if meta:
            posts.append(meta)
    if not posts:
        print("sync_latest_blog.py: no posts in", POSTS_DIR, file=sys.stderr)
        sys.exit(1)
    posts.sort(key=lambda x: x["sort_key"], reverse=True)
    card = build_card(posts)

    index = INDEX.read_text(encoding="utf-8")
    if MARK_START in index and MARK_END in index:
        pattern = re.compile(
            re.escape(MARK_START) + r"[\s\S]*?" + re.escape(MARK_END),
            re.MULTILINE,
        )
        new_index, n = pattern.subn(card.strip(), index, count=1)
        if n != 1:
            sys.exit("sync_latest_blog.py: marker replace failed")
    else:
        print("sync_latest_blog.py: markers missing in index.md", file=sys.stderr)
        sys.exit(1)

    INDEX.write_text(new_index, encoding="utf-8")
    titles = [p["title"] for p in posts[:NUM_RECENT]]
    print(f"sync_latest_blog.py: {NUM_RECENT} recent posts → index.md ({titles[0]}, ...)")


if __name__ == "__main__":
    main()
