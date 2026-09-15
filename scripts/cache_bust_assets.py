#!/usr/bin/env python3
"""
Append ?v=<content hash> to the site's own stylesheets/ and javascripts/ links in built HTML.
GitHub Pages caches these for hours while HTML updates immediately, so new markup can
otherwise ship with stale CSS. Run after `zensical build` (theme assets under assets/ are
already fingerprinted and left alone).
"""
from __future__ import annotations

import hashlib
import os
import re
import sys
from pathlib import Path

SITE_DIR = Path(os.environ.get("SITE_DIR", "site"))

LINK_RE = re.compile(r'(href|src)="((?:\./|\.\./)*(?:stylesheets|javascripts)/[^"?#]+\.(?:css|js))"')


def main() -> None:
    if not SITE_DIR.is_dir():
        sys.exit(f"cache_bust_assets.py: {SITE_DIR} not found — run the build first")
    hashes: dict[Path, str] = {}
    pages = 0
    for page in SITE_DIR.rglob("*.html"):
        text = page.read_text(encoding="utf-8")

        def stamp(m: re.Match) -> str:
            asset = (page.parent / m.group(2)).resolve()
            if not asset.is_file():
                return m.group(0)
            if asset not in hashes:
                hashes[asset] = hashlib.sha256(asset.read_bytes()).hexdigest()[:10]
            return f'{m.group(1)}="{m.group(2)}?v={hashes[asset]}"'

        new = LINK_RE.sub(stamp, text)
        if new != text:
            page.write_text(new, encoding="utf-8")
            pages += 1
    print(f"cache_bust_assets.py: versioned {len(hashes)} assets across {pages} pages")


if __name__ == "__main__":
    main()
