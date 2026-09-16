#!/usr/bin/env python3
"""
Generate Open Graph / Twitter preview images (1200x630 PNG) for posts, trips and the site default.

  docs/blog/posts/<slug>.md  ->  docs/assets/og/blog-<slug>.png
  roadtrips/<slug>.json      ->  docs/assets/og/trip-<slug>.png
                             ->  docs/assets/og/default.png

Rendered with headless Chrome, so this runs locally (CI has no Chrome) and the PNGs are
committed. Images are only re-rendered when the source is newer, or with --force.

  python3 scripts/build_og_images.py [--force]

Requires PyYAML and Google Chrome (or set CHROME=/path/to/chrome).
"""
from __future__ import annotations

import html
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("build_og_images.py: install PyYAML: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "docs" / "blog" / "posts"
TRIPS = ROOT / "roadtrips"
OUT = ROOT / "docs" / "assets" / "og"

CHROME_CANDIDATES = [
    os.environ.get("CHROME", ""),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
]

esc = html.escape


def find_chrome() -> str | None:
    for c in CHROME_CANDIDATES:
        if c and Path(c).exists():
            return c
    return None


def title_size(text: str) -> int:
    n = len(text)
    if n <= 34:
        return 82
    if n <= 52:
        return 70
    if n <= 78:
        return 60
    return 52


def card_html(eyebrow: str, title: str, sub: str, stats: list[str]) -> str:
    chips = "".join(f"<span>{esc(s)}</span>" for s in stats)
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400..700&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@500&display=swap">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ width: 1200px; height: 630px; background: #0a0a0b; color: #f0efe9;
         font-family: "DM Sans", -apple-system, sans-serif; overflow: hidden; position: relative; }}
  .glow {{ position: absolute; top: -280px; right: -200px; width: 760px; height: 760px; border-radius: 50%;
           background: radial-gradient(circle, rgba(200,255,0,0.16), rgba(200,255,0,0) 62%); }}
  .grid {{ position: absolute; inset: 0; opacity: 0.35;
           background-image: linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px),
                             linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px);
           background-size: 60px 60px; }}
  .wrap {{ position: relative; height: 100%; padding: 70px 80px 64px; display: flex; flex-direction: column; }}
  .eyebrow {{ font-family: "JetBrains Mono", monospace; font-size: 22px; letter-spacing: 0.16em;
              text-transform: uppercase; color: #c8ff00; display: flex; align-items: center; gap: 18px; }}
  .eyebrow::before {{ content: ""; width: 46px; height: 2px; background: #c8ff00; }}
  h1 {{ font-family: "Instrument Serif", Georgia, serif; font-weight: 400; letter-spacing: -0.02em;
        line-height: 1.06; margin-top: 34px; font-size: {title_size(title)}px;
        display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }}
  p {{ margin-top: 26px; font-size: 27px; line-height: 1.45; color: rgba(240,239,233,0.68); max-width: 950px;
       display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }}
  .stats {{ margin-top: 26px; display: flex; gap: 14px; flex-wrap: wrap; }}
  .stats span {{ font-family: "JetBrains Mono", monospace; font-size: 21px; color: #f0efe9;
                 background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12);
                 border-radius: 8px; padding: 8px 14px; }}
  footer {{ margin-top: auto; display: flex; align-items: center; justify-content: space-between;
            font-family: "JetBrains Mono", monospace; font-size: 23px; color: rgba(240,239,233,0.55);
            border-top: 1px solid rgba(255,255,255,0.1); padding-top: 26px; }}
  footer b {{ color: #f0efe9; font-weight: 500; }}
</style></head><body>
<div class="glow"></div><div class="grid"></div>
<div class="wrap">
  <div class="eyebrow">{esc(eyebrow)}</div>
  <h1>{esc(title)}</h1>
  {f"<p>{esc(sub)}</p>" if sub else ""}
  {f'<div class="stats">{chips}</div>' if stats else ""}
  <footer><b>prashanthr.net</b><span>Prashanth Rajagopal</span></footer>
</div></body></html>"""


def render(chrome: str, html_text: str, out: Path, tmpdir: Path) -> None:
    src = tmpdir / (out.stem + ".html")
    src.write_text(html_text, encoding="utf-8")
    subprocess.run(
        [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
         "--window-size=1200,630", "--virtual-time-budget=6000",
         f"--screenshot={out}", src.as_uri()],
        check=True, capture_output=True,
    )


def front_matter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---\n", 3)
    if end == -1:
        return None
    return yaml.safe_load(text[3:end]) or {}


def jobs() -> list[tuple[Path, Path, str]]:
    """(output png, newest source file, html) triples."""
    out: list[tuple[Path, Path, str]] = []
    for md in sorted(POSTS.glob("*.md")):
        fm = front_matter(md)
        if not fm or fm.get("draft"):
            continue
        cats = fm.get("categories") or []
        category = str(cats[0]) if cats else "Blog"
        out.append((
            OUT / f"blog-{md.stem}.png", md,
            card_html(f"Blog · {category}", str(fm.get("title", md.stem)), str(fm.get("description", "")), []),
        ))
    for data in sorted(TRIPS.glob("[!_]*.json")):
        t = json.loads(data.read_text(encoding="utf-8"))
        stats = [f"{t['totalKm']} km", t["hours"], t["difficulty"]]
        if t.get("hairpins"):
            stats.insert(2, f"{t['hairpins']} hairpins")
        out.append((
            OUT / f"trip-{t['slug']}.png", data,
            card_html(f"Road trip · {t.get('region', '')}", t["title"], t.get("tagline", ""), stats),
        ))
    out.append((
        OUT / "default.png", Path(__file__),
        card_html(
            "prashanthr.net",
            "Systems that survive production",
            "Distributed systems, agent infrastructure and Astra — an operating system for autonomous agents.",
            ["Blog", "Astra wiki", "Road trips"],
        ),
    ))
    return out


def main() -> None:
    force = "--force" in sys.argv
    chrome = find_chrome()
    if not chrome:
        print("build_og_images.py: Chrome not found — skipping (committed PNGs are used as-is)", file=sys.stderr)
        return
    OUT.mkdir(parents=True, exist_ok=True)
    todo = jobs()
    made = 0
    with tempfile.TemporaryDirectory() as tmp:
        for out, source, markup in todo:
            if not force and out.exists() and out.stat().st_mtime >= source.stat().st_mtime:
                continue
            render(chrome, markup, out, Path(tmp))
            made += 1
    stale = {p for p in OUT.glob("*.png")} - {o for o, _, _ in todo}
    for p in stale:
        p.unlink()
        print(f"  removed stale {p.name}")
    print(f"build_og_images.py: {made} image(s) rendered, {len(todo)} total in {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
