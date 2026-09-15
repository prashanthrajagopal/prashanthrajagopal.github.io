#!/usr/bin/env python3
"""
Generate the Road Trips section from roadtrips/*.json.

  roadtrips/<slug>.json  →  docs/roadtrips/<slug>.md  (+ <slug>-route.svg)
                         →  docs/roadtrips/index.md   (card grid)
                         →  nav block in mkdocs.yml between the ROADTRIPS_NAV markers
                         →  homepage strip in docs/index.md between the ROADTRIPS_HOME markers

Run before `zensical build` / `zensical serve`. No dependencies beyond the stdlib.
Files in roadtrips/ starting with "_" are ignored (the _template.json lives there).
"""
from __future__ import annotations

import html
import json
import math
import re
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "roadtrips"
OUT = ROOT / "docs" / "roadtrips"
MKDOCS = ROOT / "mkdocs.yml"
NAV_START, NAV_END = "  # ROADTRIPS_NAV_START", "  # ROADTRIPS_NAV_END"
HOME = ROOT / "docs" / "index.md"
HOME_START, HOME_END = "<!-- ROADTRIPS_HOME_START -->", "<!-- ROADTRIPS_HOME_END -->"
HOME_TRIPS = 3

esc = html.escape

# ---------------------------------------------------------------- photos
def photo_src(p: dict, width: int = 1600) -> str:
    if p.get("commons"):
        name = re.sub(r"^File:", "", p["commons"]).replace(" ", "_")
        return f"https://commons.wikimedia.org/wiki/Special:FilePath/{quote(name)}?width={width}"
    return p["url"]


def photo_link(p: dict) -> str:
    if p.get("commons"):
        name = re.sub(r"^File:", "", p["commons"]).replace(" ", "_")
        return f"https://commons.wikimedia.org/wiki/File:{quote(name)}"
    return p.get("link") or p["url"]


def photo_credit(p: dict) -> str:
    if p.get("credit"):
        return p["credit"]
    return "Wikimedia Commons · free licence, see file page" if p.get("commons") else "Source"


# ---------------------------------------------------------------- route svg
W, PAD = 900, 92
H = 640  # set per trip in route_svg (taller for many waypoints)
BOX = dict(x0=PAD, y0=PAD + 20, x1=W - PAD, y1=H - 178)
LEGEND_X0 = W - 215
MIN_SEP = 118


def set_canvas(n):
    global H, BOX
    H = 640 if n <= 8 else (760 if n <= 11 else 860)
    BOX = dict(x0=PAD, y0=PAD + 20, x1=W - PAD, y1=H - 178)


def fit_to_box(pts):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    min_x, max_x, min_y, max_y = min(xs), max(xs), min(ys), max(ys)
    span_x = (max_x - min_x) or 1; span_y = (max_y - min_y) or 1
    s = min((BOX["x1"] - BOX["x0"]) / span_x, (BOX["y1"] - BOX["y0"]) / span_y)
    ox = BOX["x0"] + ((BOX["x1"] - BOX["x0"]) - span_x * s) / 2
    oy = BOX["y0"] + ((BOX["y1"] - BOX["y0"]) - span_y * s) / 2
    return [[ox + (x - min_x) * s, oy + (y - min_y) * s] for x, y in pts]


def project(wps, legend_bottom):
    """Geographic shape, gently compressed so a far-away start city doesn't
    squash the loop, then nudged apart so labels don't pile up. The nudging is
    damped and springs back toward the true position so big loops keep their shape."""
    n = len(wps)
    mid_lat = sum(w["lat"] for w in wps) / n
    kx = math.cos(math.radians(mid_lat))
    pts = [[w["lng"] * kx, -w["lat"]] for w in wps]
    cx = sum(p[0] for p in pts) / n; cy = sum(p[1] for p in pts) / n
    max_r = max(math.hypot(p[0] - cx, p[1] - cy) for p in pts) or 1
    power = 0.5 if n <= 8 else 0.7          # compress less when there are many stops
    out = []
    for x, y in pts:
        dx, dy = x - cx, y - cy
        r = math.hypot(dx, dy) / max_r
        k = 0 if r == 0 else (r ** power) / r
        out.append([cx + dx * k, cy + dy * k])
    pts = fit_to_box(out)
    orig = [p[:] for p in pts]
    area = (BOX["x1"] - BOX["x0"]) * (BOX["y1"] - BOX["y0"])
    min_sep = min(MIN_SEP, 0.75 * math.sqrt(area / n))
    for _ in range(80):
        for i in range(n):
            for j in range(i + 1, n):
                dx = pts[j][0] - pts[i][0]; dy = pts[j][1] - pts[i][1]
                d = math.hypot(dx, dy) or 0.01
                if d < min_sep:
                    push = (min_sep - d) * 0.25; ux, uy = dx / d, dy / d
                    pts[i][0] -= ux * push; pts[i][1] -= uy * push
                    pts[j][0] += ux * push; pts[j][1] += uy * push
        for p, o in zip(pts, orig):
            p[0] += (o[0] - p[0]) * 0.02; p[1] += (o[1] - p[1]) * 0.02   # spring back
            p[0] = max(BOX["x0"], min(BOX["x1"], p[0]))
            p[1] = max(BOX["y0"], min(BOX["y1"], p[1]))
            if p[0] > LEGEND_X0 - 130 and p[1] < legend_bottom + 30:
                if LEGEND_X0 - 130 - p[0] > legend_bottom + 30 - p[1]:
                    p[1] = legend_bottom + 30
                else:
                    p[0] = LEGEND_X0 - 130
    return pts


def smooth_path(pts, closed):
    p = pts + [pts[0]] if closed else pts
    d = f"M {p[0][0]:.1f} {p[0][1]:.1f}"
    n = len(p)
    for i in range(n - 1):
        p0 = p[i - 1] if i > 0 else (p[n - 2] if closed else p[i])
        p1, p2 = p[i], p[i + 1]
        p3 = p[i + 2] if i + 2 < n else (p[1] if closed else p2)
        t = 0.18
        c1 = (p1[0] + (p2[0] - p0[0]) * t, p1[1] + (p2[1] - p0[1]) * t)
        c2 = (p2[0] - (p3[0] - p1[0]) * t, p2[1] - (p3[1] - p1[1]) * t)
        d += f" C {c1[0]:.1f} {c1[1]:.1f}, {c2[0]:.1f} {c2[1]:.1f}, {p2[0]:.1f} {p2[1]:.1f}"
    return d


def _label_candidates(name, p, cx, cy):
    """Candidate label placements in preference order: away-from-centre side, then above/below, then the other side."""
    dx, dy = p[0] - cx, p[1] - cy
    dl = math.hypot(dx, dy) or 1; dx /= dl; dy /= dl
    w = len(name) * 8.4 + 22
    right = (p[0] + 24, p[1] + dy * 10, "start")
    left = (p[0] - 24, p[1] + dy * 10, "end")
    above = (p[0], p[1] - 30, "middle")
    below = (p[0], p[1] + 32, "middle")
    if abs(dx) < 0.4:
        order = [above, below, right, left] if dy < 0 else [below, above, right, left]
    else:
        order = [right, above, below, left] if dx > 0 else [left, above, below, right]
    out = []
    for tx, ty, anchor in order:
        rx = tx - w / 2 if anchor == "middle" else (tx - 9 if anchor == "start" else tx - w + 9)
        if rx < 12 or rx + w > W - 12 or ty - 13 < 8 or ty + 13 > H - 8:
            continue
        out.append((tx, ty, anchor, rx, w))
    return out or [(p[0], p[1] + 32, "middle", max(12, min(W - 12 - w, p[0] - w / 2)), w)]


def _overlaps(a, b, pad=4):
    return not (a[0] + a[2] + pad < b[0] or b[0] + b[2] + pad < a[0] or a[1] + a[3] + pad < b[1] or b[1] + b[3] + pad < a[1])


def place_labels(wps, pts, cx, cy):
    """Greedy: for each node pick the first candidate that doesn't overlap placed labels, pins, or the legend."""
    placed = []
    obstacles = [(p[0] - 14, p[1] - 14, 28, 28) for p in pts]
    obstacles.append((LEGEND_X0 - 10, 8, W - LEGEND_X0 + 10, len(wps) * 17 + 56))
    for w, p in zip(wps, pts):
        cands = _label_candidates(w["name"], p, cx, cy)
        chosen = None
        for tx, ty, anchor, rx, lw in cands:
            rect = (rx, ty - 13, lw, 26)
            if not any(_overlaps(rect, o) for o in obstacles) and not any(_overlaps(rect, q["rect"]) for q in placed):
                chosen = (tx, ty, anchor, rx, lw); break
        if chosen is None:
            chosen = cands[0]
        tx, ty, anchor, rx, lw = chosen
        placed.append({"tx": tx, "ty": ty, "anchor": anchor, "rx": rx, "w": lw, "rect": (rx, ty - 13, lw, 26)})
    return placed


def seg_label_pos(a, b, cx, cy, force=None):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    nx, ny = -(b[1] - a[1]), b[0] - a[0]
    ln = math.hypot(nx, ny) or 1; nx /= ln; ny /= ln
    if (mx - cx) * nx + (my - cy) * ny < 0:
        nx, ny = -nx, -ny
    off = force or (34 if math.hypot(b[0] - a[0], b[1] - a[1]) < 120 else 24)
    return mx + nx * off, my + ny * off


def route_svg(t: dict) -> str:
    wps = t["waypoints"]
    set_canvas(len(wps))
    legend_h = len(wps) * 17 + 46
    pts = project(wps, 18 + legend_h)
    closed = t.get("type", "loop") == "loop"
    cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
    path = smooth_path(pts, closed)
    uid = re.sub(r"[^a-z0-9]", "", t["slug"].lower())

    labels = place_labels(wps, pts, cx, cy)
    rects = [(l["rx"] + l["w"] / 2, l["ty"], l["w"]) for l in labels]
    rects += [(p[0], p[1], 30) for p in pts]   # pins count as obstacles for km labels too

    segs = []
    for i, s in enumerate(t.get("segments", [])):
        a = pts[i]; b = pts[(i + 1) % len(pts)]
        if not closed and i + 1 >= len(pts):
            break
        lx, ly = seg_label_pos(a, b, cx, cy)
        k = 1
        while k <= 5 and any(abs(rx - lx) < (rw / 2 + 34) and abs(ry - ly) < 26 for rx, ry, rw in rects):
            lx, ly = seg_label_pos(a, b, cx, cy, 24 + k * 16); k += 1
        rects.append((lx, ly, 60))
        segs.append(f'<g class="seg"><rect x="{lx-30:.1f}" y="{ly-11:.1f}" width="60" height="22" rx="11"/>'
                    f'<text x="{lx:.1f}" y="{ly+4:.1f}">~{s["km"]} km</text></g>')

    nodes = []
    for i, (w, p, l) in enumerate(zip(wps, pts, labels)):
        tx, ty, anchor, rx, lw = l["tx"], l["ty"], l["anchor"], l["rx"], l["w"]
        nodes.append(
            f'<g class="node"><rect x="{rx:.1f}" y="{ty-13:.1f}" width="{lw:.1f}" height="26" rx="13" class="lbg"/>'
            f'<text x="{tx:.1f}" y="{ty+5:.1f}" text-anchor="{anchor}" class="lbl">{esc(w["name"])}</text>'
            f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="13" class="pin"/>'
            f'<text x="{p[0]:.1f}" y="{p[1]+4.5:.1f}" text-anchor="middle" class="num">{i+1}</text></g>')

    legend = "".join(
        f'<tspan x="{W-190}" dy="{0 if i == 0 else 17}"><tspan class="lnum">{i+1}</tspan>  {esc(w["name"])}</tspan>'
        for i, w in enumerate(wps))

    stats = [("Total", f'{t["totalKm"]} km'), ("Ride time", t["hours"])]
    if t.get("hairpins"):
        stats.append(("Hairpins", str(t["hairpins"])))
    stats.append(("Difficulty", t["difficulty"]))
    stats_svg = "".join(
        f'<g transform="translate({18 + i*118},{H-78})"><text class="sk" y="0">{esc(k)}</text><text class="sv" y="26">{esc(v)}</text></g>'
        for i, (k, v) in enumerate(stats))

    return f'''<svg class="rt-map" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Schematic route map of {esc(t["title"])}">
<defs>
<linearGradient id="bg-{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16161a"/><stop offset="1" stop-color="#0a0a0b"/></linearGradient>
<filter id="glow-{uid}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="grid-{uid}" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#ffffff" stroke-opacity="0.04"/></pattern>
</defs>
<style>
.rt-map .seg rect{{fill:#111113;stroke:#5b9aff;stroke-opacity:.55}}
.rt-map .seg text{{fill:#cfe0ff;font:500 12px/1 ui-monospace,Menlo,Consolas,monospace;text-anchor:middle}}
.rt-map .lbg{{fill:#111113;fill-opacity:.94;stroke:#ffffff;stroke-opacity:.1}}
.rt-map .lbl{{fill:#f0efe9;font:600 14px/1 system-ui,-apple-system,Segoe UI,sans-serif}}
.rt-map .pin{{fill:#c8ff00;stroke:#0a0a0b;stroke-width:3}}
.rt-map .num{{fill:#0a0a0b;font:800 13px/1 system-ui,-apple-system,Segoe UI,sans-serif}}
.rt-map .lt{{fill:#c8ff00;font:italic 400 19px/1 Georgia,"Times New Roman",serif}}
.rt-map .lg{{fill:#f0efe9;font:500 12.5px/1 system-ui,-apple-system,Segoe UI,sans-serif}}
.rt-map .lnum{{fill:#c8ff00;font-weight:700}}
.rt-map .sk{{fill:rgba(240,239,233,.5);font:500 10.5px/1 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase}}
.rt-map .sv{{fill:#f0efe9;font:700 19px/1 system-ui,-apple-system,Segoe UI,sans-serif}}
.rt-map .panel{{fill:#111113;fill-opacity:.9;stroke:#ffffff;stroke-opacity:.1}}
</style>
<rect width="{W}" height="{H}" rx="16" fill="url(#bg-{uid})"/>
<rect width="{W}" height="{H}" rx="16" fill="url(#grid-{uid})"/>
<path d="{path}" fill="none" stroke="#5b9aff" stroke-width="14" stroke-opacity=".3" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow-{uid})"/>
<path d="{path}" fill="none" stroke="#8ab8ff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
<path d="{path}" fill="none" stroke="#ffffff" stroke-width="1.6" stroke-dasharray="7 9" stroke-linecap="round" stroke-opacity=".8"/>
{"".join(segs)}
{"".join(nodes)}
<g><rect x="{W-205}" y="18" width="190" height="{legend_h}" rx="12" class="panel"/><text x="{W-190}" y="42" class="lt">Road Trip Route</text><text y="66" class="lg">{legend}</text>
<g transform="translate({W-40},44)"><circle r="14" fill="none" stroke="#fff" stroke-opacity=".4"/><path d="M0-10l5 10-5-4-5 4z" fill="#c8ff00"/><text y="-17" text-anchor="middle" fill="#f0efe9" font-size="10" font-weight="700">N</text></g></g>
<rect x="10" y="{H-104}" width="{len(stats)*118+8}" height="66" rx="12" class="panel"/>
{stats_svg}
</svg>'''


# ---------------------------------------------------------------- pages
def one_block(s: str) -> str:
    """Raw HTML in Markdown must not contain blank lines, or the parser re-enters Markdown mode."""
    return "\n".join(line for line in s.splitlines() if line.strip())


def chips(items):
    return "".join(f'<span class="rt-chip">{esc(x)}</span>' for x in items)


def trip_page(t: dict) -> str:
    hero = (t.get("photos") or [None])[0]
    wps = t["waypoints"]
    closed = t.get("type", "loop") == "loop"

    tiles = [("Distance", f'{t["totalKm"]} km'), ("Ride time", t["hours"])]
    if t.get("hairpins"):
        tiles.append(("Hairpins", str(t["hairpins"])))
    tiles += [("Difficulty", t["difficulty"]), ("Best season", t["bestSeason"])]
    if t.get("startsAt"):
        tiles.append(("Start", t["startsAt"]))
    tiles_html = "".join(f'<div class="rt-tile"><span>{esc(k)}</span><b>{esc(v)}</b></div>' for k, v in tiles)

    rows = []
    for i, s in enumerate(t.get("segments", [])):
        if not closed and i + 1 >= len(wps):
            break
        a, b = wps[i], wps[(i + 1) % len(wps)]
        extra = ""
        if s.get("hairpins"):
            extra += f' <span class="rt-chip rt-chip-accent">{s["hairpins"]} hairpins</span>'
        if s.get("surface"):
            extra += f' <span class="rt-chip">{esc(s["surface"])}</span>'
        road = f'<div class="rt-road">{esc(s["road"])}</div>' if s.get("road") else ""
        rows.append(f'<tr><td>{i+1}</td><td><b>{esc(a["name"])} → {esc(b["name"])}</b>{road}</td>'
                    f'<td class="rt-km">{s["km"]} km</td><td>{esc(s.get("note", ""))}{extra}</td></tr>')

    credit = ""
    if t.get("credit"):
        c = t["credit"]
        name = f'<a href="{esc(c["url"])}" rel="noopener">{esc(c["name"])}</a>' if c.get("url") else esc(c["name"])
        note = f' — {esc(c["note"])}' if c.get("note") else ""
        credit = f'<p class="rt-credit">Route idea: {name}{note}</p>'

    def panel(cls, title, items, lead=""):
        if not items:
            return ""
        lis = "".join(f"<li>{esc(x)}</li>" for x in items)
        return f'<div class="rt-panel {cls}"><h3>{title}</h3>{lead}<ul>{lis}</ul></div>'

    offroad = ""
    if t.get("offroad"):
        o = t["offroad"]
        bar = "".join(f'<i class="{"on" if i <= o.get("rating", 0) else ""}"></i>' for i in range(1, 6))
        lead = f'<div class="rt-rating" aria-label="Off-road rating {o.get("rating", 0)} of 5">{bar}</div>'
        if o.get("summary"):
            lead += f'<p class="rt-lead">{esc(o["summary"])}</p>'
        offroad = panel("rt-offroad", "Off-road &amp; motorcycling notes", o.get("notes", []), lead)

    gallery = ""
    if t.get("photos"):
        figs = "".join(
            f'<figure><a href="{esc(photo_link(p))}" rel="noopener"><img loading="lazy" src="{esc(photo_src(p, 900))}" alt="{esc(p.get("caption", ""))}"></a>'
            f'<figcaption>{esc(p.get("caption", ""))}<br><a href="{esc(photo_link(p))}" rel="noopener">{esc(photo_credit(p))}</a></figcaption></figure>'
            for p in t["photos"])
        gallery = f'<div class="rt-gallery">{figs}</div>'

    sources = ""
    if t.get("sources"):
        sources = "<ul class=\"rt-sources\">" + "".join(
            f'<li><a href="{esc(s["url"])}" rel="noopener">{esc(s["title"])}</a></li>' for s in t["sources"]) + "</ul>"

    hero_style = f' style="background-image:url(\'{esc(photo_src(hero, 1600))}\')"' if hero else ""
    header = one_block(f'''
<div class="rt-hero"{hero_style}>
<div class="rt-hero-inner">
<div class="pr-eyebrow">{esc(t["region"])} · {esc(t["country"])} · {esc(t["days"])}</div>
<h1 class="rt-title">{esc(t["title"])}</h1>
<p class="rt-tagline">{esc(t["tagline"])}</p>
<div class="rt-tags">{chips(t.get("tags", []))}</div>
</div>
</div>
<div class="rt-tiles">{tiles_html}</div>
<p class="rt-summary">{esc(t["summary"])}</p>
{credit}
''')

    legs = one_block(f'''
<div class="rt-panel">
<h3>Leg by leg</h3>
<div class="rt-table-wrap"><table class="rt-segs"><thead><tr><th>#</th><th>Leg</th><th>Dist</th><th>Notes</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
</div>
''')

    side = one_block(f'''
<div class="rt-cols">
<div>{panel("", "Highlights", t.get("highlights", []))}{offroad}</div>
<div>{panel("rt-timings", "Timings, permits &amp; fuel", t.get("timings", []))}{panel("rt-caution", "Cautions", t.get("cautions", []))}</div>
</div>
''')

    md = f'''---
title: {json.dumps(t["title"], ensure_ascii=False)}
description: {json.dumps(t["tagline"], ensure_ascii=False)}
hide:
  - toc
---

{header}

## The route

<img class="rt-map" src="{t["slug"]}-route.svg" alt="Schematic route map of {esc(t["title"])}" width="{W}" height="{H}">

<p class="rt-note">Schematic map generated from waypoint coordinates — the shape follows the geography (compressed so long legs don't squash the loop), distances are labelled per leg. Not a navigation map. <a href="{t["slug"]}-route.svg" download>Download the graphic</a>.</p>

{legs}

{side}
'''
    if gallery:
        md += f"\n## Along the way\n\n{gallery}\n"
    if sources:
        md += f"\n## Sources &amp; further reading\n\n{sources}\n"
    md += '\n<p class="rt-back"><a href="../">← All road trips</a></p>\n'
    return md


def card(t: dict) -> str:
    hero = (t.get("photos") or [None])[0]
    style = f' style="background-image:url(\'{esc(photo_src(hero, 900))}\')"' if hero else ""
    kv = [f"<b>{t['totalKm']}</b> km", f"<b>{esc(t['hours'])}</b>"]
    if t.get("hairpins"):
        kv.append(f"<b>{t['hairpins']}</b> hairpins")
    kv += [f"<b>{esc(t['difficulty'])}</b>", esc(t["days"])]
    return (f'<a class="rt-card" href="{t["slug"]}/">'
            f'<div class="rt-card-photo"{style}><span class="rt-badge">{esc(t["region"])}</span></div>'
            f'<div class="rt-card-body"><h3>{esc(t["title"])}</h3><p>{esc(t["tagline"])}</p>'
            f'<div class="rt-kv">{"".join(f"<span>{x}</span>" for x in kv)}</div></div></a>')


def index_page(trips) -> str:
    total_km = sum(t.get("totalKm", 0) for t in trips)
    regions = sorted({t["region"] for t in trips})
    cards = one_block("\n".join(card(t) for t in trips))
    return f'''---
title: Road Trips
description: A growing catalogue of road trips and motorcycle loops — routes, distances, hairpins, forest timings and the photos that made me want to ride them.
hide:
  - toc
---

<div class="rt-head">
<div class="pr-eyebrow">A personal collection</div>
<h1 class="rt-title">Roads worth the detour</h1>
<p class="rt-intro">Road trips and motorcycle loops I've collected from reels, forums and friends, each turned into a proper route sheet: a generated route graphic, leg-by-leg distances, off-road and motorcycling notes, forest check-post timings, and free-licensed photos of the places along the way.</p>
<div class="rt-stats"><div><b>{len(trips)}</b><span>trips</span></div><div><b>{total_km:,}</b><span>km of road</span></div><div><b>{len(regions)}</b><span>{"region" if len(regions) == 1 else "regions"}</span></div></div>
</div>

<div class="rt-grid">
{cards}
</div>

<p class="rt-note">Route graphics are schematic, not to scale — always ride with a live map. Photos are free-licensed (mostly Wikimedia Commons) and link back to their source.</p>
'''


# ---------------------------------------------------------------- nav + main
def validate(t: dict, f: Path):
    for k in ("slug", "title", "region", "country", "tagline", "summary", "days", "totalKm",
              "hours", "difficulty", "bestSeason", "waypoints"):
        if k not in t:
            sys.exit(f"{f.name}: missing '{k}'")
    if len(t["waypoints"]) < 2:
        sys.exit(f"{f.name}: need at least 2 waypoints")
    expect = len(t["waypoints"]) if t.get("type", "loop") == "loop" else len(t["waypoints"]) - 1
    if "segments" in t and len(t["segments"]) != expect:
        print(f"  ! {f.name}: {len(t['segments'])} segments but {expect} expected", file=sys.stderr)


def home_card(t: dict) -> str:
    kv = [f"<b>{t['totalKm']}</b> km", f"<b>{esc(t['hours'])}</b>"]
    if t.get("hairpins"):
        kv.append(f"<b>{t['hairpins']}</b> hairpins")
    kv.append(f"<b>{esc(t['difficulty'])}</b>")
    return (f'        <a class="pr-trip-card" href="roadtrips/{t["slug"]}/">'
            f'<span class="pr-trip-map"><img src="roadtrips/{t["slug"]}-route.svg" alt="Route map of {esc(t["title"])}" '
            f'width="{W}" height="{H}" loading="lazy"><span class="rt-badge">{esc(t["region"])}</span></span>'
            f'<span class="pr-trip-body"><span class="pr-trip-title">{esc(t["title"])}</span>'
            f'<span class="pr-trip-desc">{esc(t["tagline"])}</span>'
            f'<span class="rt-kv">{"".join(f"<span>{x}</span>" for x in kv)}</span></span></a>')


def update_home(trips):
    """Newest trips as a card strip on the homepage, below the blog cards."""
    text = HOME.read_text(encoding="utf-8")
    if HOME_START not in text or HOME_END not in text:
        print("build_roadtrips.py: home markers not found in docs/index.md, skipping homepage strip", file=sys.stderr)
        return
    block = [
        HOME_START,
        '      <div class="pr-recent-head"><h2 class="pr-recent-title">Road trips</h2>'
        '<a class="pr-section-link" href="roadtrips/">All trips <span aria-hidden="true">&rarr;</span></a></div>',
        '      <div class="pr-trips-grid">',
        *[home_card(t) for t in trips[:HOME_TRIPS]],
        "      </div>",
        f"  {HOME_END}",
    ]
    new = re.sub(re.escape(HOME_START) + r".*?" + re.escape(HOME_END), lambda _m: "\n".join(block), text, flags=re.S)
    if new != text:
        HOME.write_text(new, encoding="utf-8")


def update_nav(trips):
    text = MKDOCS.read_text(encoding="utf-8")
    if NAV_START not in text or NAV_END not in text:
        print("build_roadtrips.py: nav markers not found in mkdocs.yml, skipping nav update", file=sys.stderr)
        return
    block = [NAV_START, "  - Road Trips:", "    - roadtrips/index.md"]
    block += [f"    - {json.dumps(t['title'], ensure_ascii=False)}: roadtrips/{t['slug']}.md" for t in trips]
    block.append(NAV_END)
    new = re.sub(re.escape(NAV_START) + r".*?" + re.escape(NAV_END), lambda _m: "\n".join(block), text, flags=re.S)
    if new != text:
        MKDOCS.write_text(new, encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    trips = []
    for f in sorted(DATA.glob("*.json")):
        if f.name.startswith("_"):
            continue
        t = json.loads(f.read_text(encoding="utf-8"))
        validate(t, f)
        trips.append(t)
    trips.sort(key=lambda t: (t.get("added", ""), t["title"]), reverse=True)

    keep = {"index.md"}
    for t in trips:
        (OUT / f"{t['slug']}.md").write_text(trip_page(t), encoding="utf-8")
        (OUT / f"{t['slug']}-route.svg").write_text(route_svg(t), encoding="utf-8")
        keep |= {f"{t['slug']}.md", f"{t['slug']}-route.svg"}
        print(f"  ✓ {t['title']}")
    (OUT / "index.md").write_text(index_page(trips), encoding="utf-8")
    for stale in OUT.iterdir():
        if stale.name not in keep and stale.suffix in (".md", ".svg"):
            stale.unlink()
    update_nav(trips)
    update_home(trips)
    print(f"Road Trips: {len(trips)} trips → docs/roadtrips/")


if __name__ == "__main__":
    main()
