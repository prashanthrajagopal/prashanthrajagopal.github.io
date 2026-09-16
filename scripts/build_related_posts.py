#!/usr/bin/env python3
"""
Append a "Related reading" block to each blog post, between markers, based on shared
tags and category. Internal links help readers and give crawlers a denser link graph.

  python3 scripts/build_related_posts.py

Idempotent: the block is regenerated in place each run. Requires PyYAML.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("build_related_posts.py: install PyYAML: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "docs" / "blog" / "posts"
START, END = "<!-- RELATED_START -->", "<!-- RELATED_END -->"
HOW_MANY = 3


def load(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---\n", 3)
    if end == -1:
        return None
    fm = yaml.safe_load(text[3:end]) or {}
    if fm.get("draft"):
        return None
    cats = fm.get("categories") or []
    return {
        "path": path,
        "slug": path.stem,
        "title": str(fm.get("title", path.stem)),
        "description": str(fm.get("description", "")),
        "tags": {str(t).lower() for t in (fm.get("tags") or [])},
        "category": str(cats[0]) if cats else "",
        "date": str(fm.get("date", "")),
        "text": text,
        "body_end": end + 5,
    }


def score(a: dict, b: dict) -> tuple[int, int, str]:
    shared = len(a["tags"] & b["tags"])
    same_cat = 1 if a["category"] and a["category"] == b["category"] else 0
    return (shared * 2 + same_cat, shared, b["date"])


def block_for(post: dict, others: list[dict]) -> str:
    ranked = sorted(others, key=lambda o: score(post, o), reverse=True)
    picks = [o for o in ranked if score(post, o)[0] > 0][:HOW_MANY]
    if len(picks) < HOW_MANY:                       # top up with the newest posts
        for o in sorted(others, key=lambda o: o["date"], reverse=True):
            if o not in picks:
                picks.append(o)
            if len(picks) == HOW_MANY:
                break
    items = "\n".join(
        f'  <a class="pr-related-item" href="{p["slug"]}.md">'
        f'<span class="pr-related-title">{p["title"]}</span>'
        f'<span class="pr-related-desc">{p["description"]}</span></a>'
        for p in picks
    )
    return f'''{START}
<aside class="pr-related" markdown="0">
  <h2 class="pr-related-head">Related reading</h2>
{items}
</aside>
{END}'''


def main() -> None:
    posts = [p for p in (load(f) for f in sorted(POSTS.glob("*.md"))) if p]
    changed = 0
    for post in posts:
        others = [o for o in posts if o["slug"] != post["slug"]]
        block = block_for(post, others)
        text = post["text"]
        if START in text and END in text:
            new = re.sub(re.escape(START) + r"[\s\S]*?" + re.escape(END), lambda _m: block, text, count=1)
        else:
            new = text.rstrip() + "\n\n" + block + "\n"
        if new != text:
            post["path"].write_text(new, encoding="utf-8")
            changed += 1
    print(f"build_related_posts.py: {changed} post(s) updated, {len(posts)} total")


if __name__ == "__main__":
    main()
