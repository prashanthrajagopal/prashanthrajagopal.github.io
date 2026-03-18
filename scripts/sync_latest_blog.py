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


def build_card(p: dict) -> str:
    href = html.escape(f"blog/posts/{p['slug']}/", quote=True)
    title_e = html.escape(p["title"])
    excerpt_e = html.escape(p["excerpt"])
    cat_e = html.escape(p["category"])
    tag = _tag_class(p["category"])
    return f"""  {MARK_START}
  <a class="pr-latest-card" href="{href}">
    <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.45rem;">
      <span class="post-date">{html.escape(p["date_display"])}</span>
      <span class="post-tag {tag}">{cat_e}</span>
    </div>
    <h3 class="post-title" style="margin:0 0 0.35rem;font-family:var(--pr-font-display);font-size:1.25rem;font-weight:400;letter-spacing:-0.01em;color:var(--pr-text);">{title_e}</h3>
    <p class="post-excerpt" style="margin:0;font-size:0.92rem;color:var(--pr-text-secondary);line-height:1.65;max-width:640px;">{excerpt_e}</p>
    <span class="post-read-more" style="display:inline-flex;align-items:center;gap:0.35rem;margin-top:0.45rem;font-size:0.82rem;font-weight:600;color:var(--pr-accent);">Read post <span aria-hidden="true">→</span></span>
  </a>
  {MARK_END}"""


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
    latest = posts[0]
    card = build_card(latest)

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
    print(f"sync_latest_blog.py: featured '{latest['title']}' ({latest['date_display']})")


if __name__ == "__main__":
    main()
