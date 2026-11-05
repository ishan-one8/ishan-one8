"""Pit-wall terminal card: a Red Bull-livery pixel portrait beside a driver readout.

    python3 scripts/portrait.py path/to/photo.jpg

The photo itself stays out of the repo; only the pixelated result is written,
to assets/portrait.svg.
"""
import sys
from collections import deque

import numpy as np
from PIL import Image

from kit import F1, esc, measure, svg, write

COLS, ROWS, CELL = 64, 80, 4.5
CROP = (150, 110, 1030, 1210)  # head and shoulders, 4:5
# dark -> light: navy and blue for hair and hoodie, red shadows, yellow highlights
RAMP = ["#0D1640", "#16286A", "#1F3B92", "#3671C6", "#B3124A",
        "#DB0A40", "#F25A2A", "#FF9A1A", "#FFCC00", "#FFE47A"]
RIM = "#DB0A40"

W, H = 1200, 460
PX, PY = 44, 78                      # portrait origin
TX = 392                             # readout column

ROWS_TEXT = [
    ("Driver", "Ishan Kumar  ·  #18"),
    ("Role", "Developer · Builder · Product thinker"),
    ("Study", "B.Tech CSE, Newton School of Technology"),
    ("Based", "Bengaluru, India"),
    ("Langs", "Python · TypeScript · JavaScript"),
    ("Stack", "React · Next.js · Node.js · Git"),
    ("Garage", "InterviewOS · Cricket Analysis · Hand Cricket"),
    ("Fuel", "Red Bull, obviously"),
]


def _flood(mask_bg):
    """Background pixels reachable from the border."""
    h, w = mask_bg.shape
    seen = np.zeros_like(mask_bg)
    q = deque()
    for y in range(h):
        for x in (0, w - 1):
            if mask_bg[y, x] and not seen[y, x]:
                seen[y, x] = True
                q.append((y, x))
    for x in range(w):
        for y in (0, h - 1):
            if mask_bg[y, x] and not seen[y, x]:
                seen[y, x] = True
                q.append((y, x))
    while q:
        y, x = q.popleft()
        for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if 0 <= ny < h and 0 <= nx < w and mask_bg[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True
                q.append((ny, nx))
    return seen


def _largest(fg):
    h, w = fg.shape
    lab = np.zeros(fg.shape, int)
    best, n = (0, 0), 0
    for sy in range(h):
        for sx in range(w):
            if fg[sy, sx] and not lab[sy, sx]:
                n += 1
                lab[sy, sx] = n
                q, c = deque([(sy, sx)]), 0
                while q:
                    y, x = q.popleft()
                    c += 1
                    for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                        if 0 <= ny < h and 0 <= nx < w and fg[ny, nx] and not lab[ny, nx]:
                            lab[ny, nx] = n
                            q.append((ny, nx))
                best = max(best, (c, n))
    return lab == best[1]


def pixels(path):
    """Grid of ramp colours (None = background) for the photo at `path`."""
    im = Image.open(path).convert("RGB").crop(CROP)
    a = np.asarray(im.resize((COLS * 4, ROWS * 4), Image.LANCZOS)).astype(float)
    lum = a @ [0.299, 0.587, 0.114]
    bgish = (lum > 150) & ((a.max(2) - a.min(2)) < 70)   # the pale studio backdrop
    fg = _largest(~_flood(bgish))
    mask = np.asarray(Image.fromarray((fg * 255).astype(np.uint8)).resize((COLS, ROWS), Image.BOX)) > 110
    g = np.asarray(im.convert("L").resize((COLS, ROWS), Image.BOX)).astype(float)
    lo, hi = np.percentile(g[mask], 2), np.percentile(g[mask], 99)
    n = np.clip((g - lo) / (hi - lo), 0, 1)
    grid = []
    for y in range(ROWS):
        row = []
        for x in range(COLS):
            if not mask[y, x]:
                row.append(None)
                continue
            edge = any(not (0 <= y + dy < ROWS and 0 <= x + dx < COLS and mask[y + dy, x + dx])
                       for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            row.append(RIM if edge else RAMP[min(int(n[y, x] * len(RAMP)), len(RAMP) - 1)])
        grid.append(row)
    return grid


def portrait_rects(grid):
    out = []
    for y, row in enumerate(grid):
        x = 0
        while x < COLS:
            c = row[x]
            run = 1
            while x + run < COLS and row[x + run] == c:
                run += 1
            if c:
                out.append(f'<rect x="{PX + x * CELL:g}" y="{PY + y * CELL:g}" width="{run * CELL:g}" height="{CELL:g}" fill="{c}"/>')
            x += run
    return "\n    ".join(out)


def card(grid):
    t = F1
    pw, ph = COLS * CELL, ROWS * CELL
    lines = []
    y0, lh = 112, 30.5
    lines.append(
        f'<text class="f-mono" x="{TX}" y="{y0}" font-size="18" xml:space="preserve">'
        f'<tspan fill="{t["red"]}" font-weight="600">ishan</tspan><tspan fill="{t["text3"]}">@</tspan>'
        f'<tspan fill="{t["yellow"]}" font-weight="600">pitwall</tspan><tspan fill="{t["text3"]}">  ~/driver</tspan></text>')
    lines.append(f'<path d="M{TX} {y0 + 15}H{W - 60}" stroke="{t["hair"]}" stroke-opacity=".16" stroke-dasharray="6 5"/>')
    for i, (k, v) in enumerate(ROWS_TEXT):
        y = y0 + lh * (i + 1.4)
        lines.append(
            f'<text class="f-mono" x="{TX}" y="{y:.1f}" font-size="17" xml:space="preserve">'
            f'<tspan fill="{t["yellow"]}" font-weight="600">{esc(k.ljust(8))}</tspan>'
            f'<tspan fill="{t["text"]}">{esc(v)}</tspan></text>')
    ys = y0 + lh * (len(ROWS_TEXT) + 1.4)
    lines.append(
        f'<text class="f-mono" x="{TX}" y="{ys:.1f}" font-size="17" xml:space="preserve">'
        f'<tspan fill="{t["yellow"]}" font-weight="600">{"Status".ljust(8)}</tspan>'
        f'<tspan fill="{t["text"]}">  on track, open to build</tspan></text>')
    lines.append(f'<circle class="live" cx="{TX + measure("Status  ", 17, "mono") + 6:.1f}" cy="{ys - 5.5:.1f}" r="5" fill="{t["green"]}"/>')
    yp = ys + lh * 1.25
    lines.append(
        f'<text class="f-mono" x="{TX}" y="{yp:.1f}" font-size="17" xml:space="preserve">'
        f'<tspan fill="{t["red"]}" font-weight="600">&gt; </tspan><tspan fill="{t["text2"]}">box box, new idea incoming</tspan></text>')
    cur_x = TX + measure("> box box, new idea incoming", 17, "mono") + 6

    dots = "".join(f'<circle cx="{34 + i * 20}" cy="24" r="6" fill="{c}"/>'
                   for i, c in enumerate([t["red"], t["yellow"], t["blue"]]))

    css = """
.cur{animation:blink 1.1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
.scan{animation:sweep 4.2s linear infinite}
@keyframes sweep{from{transform:translateY(-60px)}to{transform:translateY(420px)}}
.crt{animation:flick 5.2s steps(1) infinite}
@keyframes flick{0%{opacity:.95}12%{opacity:1}31%{opacity:.97}47%{opacity:1}63%{opacity:.93}71%{opacity:1}88%{opacity:.98}}
.live{animation:pulse 1.6s ease-in-out infinite}
@keyframes pulse{50%{opacity:.25}}
"""
    defs = f"""
    <linearGradient id="sweepg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFE47A" stop-opacity="0"/><stop offset=".45" stop-color="#FFE47A" stop-opacity=".10"/>
      <stop offset=".5" stop-color="#FFFFFF" stop-opacity=".26"/><stop offset=".55" stop-color="#FFE47A" stop-opacity=".10"/>
      <stop offset="1" stop-color="#FFE47A" stop-opacity="0"/></linearGradient>
    <radialGradient id="halo" cx=".5" cy=".42" r=".55"><stop stop-color="{t['red']}" stop-opacity=".34"/><stop offset="1" stop-color="{t['red']}" stop-opacity="0"/></radialGradient>
    <pattern id="scanl" width="4" height="4.5" patternUnits="userSpaceOnUse"><rect width="4" height="1.6" fill="#000" opacity=".28"/></pattern>
    <pattern id="kerb" width="32" height="8" patternUnits="userSpaceOnUse"><rect width="16" height="8" fill="{t['red']}"/><rect x="16" width="16" height="8" fill="#F4F6FA"/></pattern>
    <pattern id="livery" width="46" height="46" patternUnits="userSpaceOnUse" patternTransform="rotate(-28)">
      <rect width="8" height="46" fill="{t['red']}" opacity=".9"/><rect x="12" width="3" height="46" fill="{t['yellow']}"/></pattern>
    <clipPath id="screen"><rect x="{PX - 14}" y="{PY - 14}" width="{pw + 28}" height="{ph + 22}" rx="14"/></clipPath>
    <clipPath id="cardc"><rect width="{W}" height="{H}" rx="22"/></clipPath>"""

    body = f"""
  <g clip-path="url(#cardc)">
    <rect width="{W}" height="{H}" fill="{t['bg']}"/>
    <rect width="{W}" height="{H}" fill="url(#dots)"/>
    <rect x="{W - 150}" y="-20" width="190" height="{H + 40}" fill="url(#livery)" opacity=".16"/>
    <text class="f-race" x="{W - 54}" y="{H - 30}" text-anchor="end" font-size="190" font-weight="900" font-style="italic" fill="{t['text']}" fill-opacity=".045">18</text>
    <rect width="{W}" height="48" fill="{t['bg2']}"/>
    <path d="M0 48.5H{W}" stroke="{t['hair']}" stroke-opacity=".10"/>
    {dots}
    <text class="f-mono" x="{W / 2}" y="29" text-anchor="middle" font-size="13" letter-spacing="1" fill="{t['text3']}">ishan@pitwall — telemetry</text>
    <circle class="live" cx="{W - 98}" cy="24" r="4.5" fill="{t['red']}"/>
    <text class="f-race" x="{W - 86}" y="29.5" font-size="14" font-weight="700" letter-spacing="2" fill="{t['text2']}">LIVE</text>

    <g clip-path="url(#screen)">
      <rect x="{PX - 14}" y="{PY - 14}" width="{pw + 28}" height="{ph + 22}" fill="{t['surface']}"/>
      <rect x="{PX - 14}" y="{PY - 14}" width="{pw + 28}" height="{ph + 22}" fill="url(#halo)"/>
      <g class="crt">
    {portrait_rects(grid)}
      </g>
      <rect x="{PX - 14}" y="{PY - 14}" width="{pw + 28}" height="{ph + 22}" fill="url(#scanl)"/>
      <rect class="scan" x="{PX - 14}" y="{PY - 14}" width="{pw + 28}" height="60" fill="url(#sweepg)"/>
      <rect x="{PX - 14}" y="{PY + ph}" width="{pw + 28}" height="8" fill="url(#kerb)"/>
    </g>
    <rect x="{PX - 13.5}" y="{PY - 13.5}" width="{pw + 27}" height="{ph + 21}" rx="13.5" stroke="{t['hair']}" stroke-opacity=".14"/>

    {''.join(lines)}
    <rect class="cur" x="{cur_x:.1f}" y="{yp - 14:.1f}" width="9" height="18" rx="1" fill="{t['yellow']}"/>
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="21.5" stroke="{t['hair']}" stroke-opacity=".12"/>"""

    readout = "; ".join(f"{k}: {v}" for k, v in ROWS_TEXT)
    return svg(t, W, H, body, "Pit wall",
               "Terminal card: a pixel-art portrait of Ishan in Red Bull Racing colours, navy, red and yellow, "
               f"beside a driver readout. {readout}; Status: on track, open to build.", css, defs)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(write("portrait.svg", card(pixels(sys.argv[1]))))
