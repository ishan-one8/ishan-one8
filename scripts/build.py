"""Builds every static SVG on the profile: the Red Bull Racing edition.

    pip install fonttools brotli
    python scripts/build.py

The live telemetry and season cards are built by scripts/stats.py.
"""
import json
import math
import os

from kit import F1, THEMES, eyebrow, esc, measure, svg, tile, write

W = 1200


# ───────────────────────── toolkit orbit + fuel ─────────────────────────
ICONS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons.json")))
INNER = ["typescript", "javascript", "react", "nextdotjs"]
OUTER = ["html5", "css", "nodedotjs", "git", "github", "githubactions"]
TOOLS = ["python"] + INNER + OUTER


def icon_color(t, slug):
    hexc = "#" + ICONS[slug]["hex"]
    return t["text"] if hexc in ("#000000", "#181717") else hexc


RB_OVERLAP = 3.5
RB_W = 2 * ICONS["redbull_bull"]["w"] - RB_OVERLAP


def redbull_logo():
    """The full Red Bull mark: two bulls charging at each other over a golden sun.

    Centred on (0, 0) in bull units; the sun sits behind the clash point."""
    bull, w, h = ICONS["redbull_bull"]["d"], ICONS["redbull_bull"]["w"], ICONS["redbull_bull"]["h"]
    return (f'<g transform="translate({-RB_W / 2:.3f} {-h / 2:.3f})">'
            f'<circle cx="{RB_W / 2:.3f}" cy="3" r="5" fill="#FFCC00"/>'
            f'<path d="{bull}" fill="#DB0A40"/>'
            f'<g transform="translate({RB_W:.3f} 0) scale(-1 1)"><path d="{bull}" fill="#DB0A40"/></g></g>')


def toolkit(t):
    H = 440
    g = 16
    aw = 790
    bx, bw = aw + g, W - aw - g
    cx, cy = 245, 220
    step = 0.8
    cycle = step * len(TOOLS)
    parts = [tile(t, 0, 0, aw, H, glow=(cx, cy, "#3776AB"))]

    # orbit rings
    for r in (108, 178):
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{t["hair"]}" stroke-opacity="{t["hair_op"] * 1.8:.2f}" stroke-dasharray="2 6"/>')

    def badge(slug, x, y, i):
        col = icon_color(t, slug)
        return (f'<g class="upright">'
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="24" fill="{t["surface2"]}" stroke="{t["hair"]}" stroke-opacity="{t["hair_op"] * 1.8:.2f}"/>'
                f'<circle class="spot" style="animation-delay:{i * step:.1f}s" cx="{x:.1f}" cy="{y:.1f}" r="27" stroke="{t["accent"]}" stroke-width="1.5"/>'
                f'<path transform="translate({x - 11:.1f} {y - 11:.1f}) scale(.9167)" d="{ICONS[slug]["d"]}" fill="{col}"/></g>')

    for ring, r, cls in ((INNER, 108, "spinA"), (OUTER, 178, "spinB")):
        items = []
        for k, slug in enumerate(ring):
            a = math.radians(-90 + 360 * k / len(ring) + (0 if cls == "spinA" else 30))
            items.append(badge(slug, cx + r * math.cos(a), cy + r * math.sin(a), TOOLS.index(slug)))
        parts.append(f'<g class="{cls}">{"".join(items)}</g>')

    # python core
    parts.append(f"""
  <circle cx="{cx}" cy="{cy}" r="70" fill="#3776AB" opacity="{t['aur_op'] * .8:.2f}" filter="url(#blurS)"/>
  <circle class="wave" cx="{cx}" cy="{cy}" r="46" stroke="#3776AB" stroke-width="1.5"/>
  <circle class="wave" style="animation-delay:-1.5s" cx="{cx}" cy="{cy}" r="46" stroke="#FFD43B" stroke-width="1.5"/>
  <circle cx="{cx}" cy="{cy}" r="46" fill="{t['surface2']}" stroke="{t['hair']}" stroke-opacity="{t['hair_op'] * 2:.2f}"/>
  <circle class="spot" cx="{cx}" cy="{cy}" r="50" stroke="{t['accent']}" stroke-width="1.5"/>
  <g transform="translate({cx - 30} {cy - 30}) scale(.6)">
    <path d="{PY_LOGO}" fill="url(#pyb)"/><circle cx="39" cy="14.5" r="3.6" fill="#FFFFFF"/>
    <g transform="rotate(180 50 50)"><path d="{PY_LOGO}" fill="url(#pyy)"/><circle cx="39" cy="14.5" r="3.6" fill="#FFFFFF"/></g>
  </g>""")

    # copy + tool list
    tx = 470
    parts.append(eyebrow(t, tx, 56, f"TOOLKIT  ·  {len(TOOLS)} TOOLS"))
    parts.append(f'<text class="f-sans" x="{tx - 2}" y="104" font-size="34" font-weight="600" letter-spacing="-1.2" fill="{t["text"]}">Python at the <tspan class="f-serif" font-size="40" font-weight="400" letter-spacing="0" fill="url(#aur)">core.</tspan></text>')
    parts.append(f'<g class="f-sans" font-size="14.5" fill="{t["text2"]}"><text x="{tx}" y="134">Everything else orbits around it, from</text><text x="{tx}" y="155">the web stack to shipping with Git.</text></g>')
    cw_, ch_ = 141, 32
    for i, slug in enumerate(TOOLS):
        x = tx + (i % 2) * (cw_ + 8)
        y = 180 + (i // 2) * (ch_ + 8)
        name = ICONS[slug]["title"].replace("HTML5", "HTML")
        parts.append(f"""
  <rect x="{x}" y="{y}" width="{cw_}" height="{ch_}" rx="10" fill="{t['surface2']}" stroke="{t['hair']}" stroke-opacity="{t['hair_op'] * 1.5:.2f}"/>
  <rect class="spot" style="animation-delay:{i * step:.1f}s" x="{x}" y="{y}" width="{cw_}" height="{ch_}" rx="10" fill="{t['accent']}" fill-opacity=".08" stroke="{t['accent']}" stroke-width="1.2"/>
  <path transform="translate({x + 11} {y + 9}) scale(.5833)" d="{ICONS[slug]['d']}" fill="{icon_color(t, slug)}"/>
  <text class="f-sans" x="{x + 32}" y="{y + 20.5}" font-size="13" font-weight="500" fill="{t['text']}">{esc(name)}</text>""")

    # fuel: the can
    ccx, top, cw2, chh = bx + bw / 2, 74, 112, 246
    lscale = (cw2 - 16) / RB_W
    l, r_ = ccx - cw2 / 2, ccx + cw2 / 2
    bubbles = "".join(
        f'<circle class="bub" style="animation-delay:{-k * .7:.1f}s;animation-duration:{4 + (k % 3)}s" cx="{ccx + dx}" cy="{top + chh + 10}" r="{rr}" '
        f'stroke="{t["text"]}" stroke-opacity=".35" fill="{t["text"]}" fill-opacity=".06"/>'
        for k, (dx, rr) in enumerate([(-86, 4), (-70, 2.5), (-92, 6), (74, 3), (90, 5), (66, 2), (-60, 3.5), (84, 2.5)]))
    parts.append(tile(t, bx, 0, bw, H, glow=(ccx, top + 120, "#DB0A40")))
    parts.append(f"""
  <g clip-path="url(#tc{int(bx)}_0)">
    <circle cx="{ccx - 40}" cy="{top + 150}" r="90" fill="#1E3A8A" opacity="{t['aur_op'] * .7:.2f}" filter="url(#blur)"/>
    {bubbles}
  </g>
  {eyebrow(t, bx + 26, 56, "FUEL")}
  <ellipse cx="{ccx}" cy="{top + chh + 18}" rx="64" ry="9" fill="#000" opacity="{.5 if t.get('dark') else .14}" filter="url(#blurS)"/>
  <g class="can">
    <g clip-path="url(#canc)">
      <rect x="{l}" y="{top}" width="{cw2}" height="{chh}" fill="url(#canBlue)"/>
      <path d="M{l} {top}H{r_}L{l} {top + chh * .78}Z" fill="url(#checker)"/>
      <rect x="{l}" y="{top + 74}" width="{cw2}" height="104" fill="url(#label)"/>
      <path d="M{l} {top + 74.5}H{r_}M{l} {top + 177.5}H{r_}" stroke="#1D3E96" stroke-opacity=".5"/>
      <g transform="translate({ccx} {top + 112}) scale({lscale:.3f})">{redbull_logo()}</g>
      <text class="f-sans" x="{ccx}" y="{top + 156}" text-anchor="middle" font-size="17" font-weight="800" letter-spacing="-.4" fill="#DB0A40">Red Bull</text>
      <text class="f-sans" x="{ccx}" y="{top + 170}" text-anchor="middle" font-size="6.5" font-weight="700" letter-spacing="1.6" fill="#1D3E96">ENERGY DRINK</text>
      <rect x="{l}" y="{top}" width="{cw2}" height="{chh}" fill="url(#canShade)"/>
      <g fill="#FFFFFF" opacity=".55">
        <ellipse cx="{l + 20}" cy="{top + 60}" rx="1.6" ry="2.4"/><ellipse cx="{l + 76}" cy="{top + 170}" rx="1.3" ry="2"/>
        <ellipse cx="{l + 30}" cy="{top + 190}" rx="1.8" ry="2.8"/><ellipse cx="{l + 84}" cy="{top + 46}" rx="1.2" ry="1.9"/>
        <ellipse cx="{l + 58}" cy="{top + 205}" rx="1.4" ry="2.2"/>
      </g>
    </g>
    <ellipse cx="{ccx}" cy="{top + 2}" rx="{cw2 / 2 - 2}" ry="9" fill="url(#lid)" stroke="#9AA3B2" stroke-width="1"/>
    <ellipse cx="{ccx}" cy="{top + 2}" rx="{cw2 / 2 - 12}" ry="5.5" fill="none" stroke="#8B93A1" stroke-opacity=".8"/>
    <rect x="{ccx - 13}" y="{top - 3}" width="26" height="8" rx="4" fill="#C9CFD8" stroke="#8B93A1" stroke-width=".8"/>
  </g>
  <text class="f-sans" x="{ccx}" y="{H - 52}" text-anchor="middle" font-size="25" font-weight="600" letter-spacing="-.8" fill="{t['text']}">Fueled by <tspan class="f-serif" font-size="30" font-weight="400" letter-spacing="0" fill="#DB0A40">Red Bull.</tspan></text>
  {eyebrow(t, ccx, H - 26, "LATE NIGHTS  ·  BIG IDEAS", "middle")}""")

    defs = f"""
    <linearGradient id="pyb" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#5A9FD4"/><stop offset="1" stop-color="#306998"/></linearGradient>
    <linearGradient id="pyy" x1="1" y1="1" x2="0" y2="0"><stop stop-color="#FFE873"/><stop offset="1" stop-color="#FFD43B"/></linearGradient>
    <clipPath id="canc"><path d="M{l + 6} {top}H{r_ - 6}Q{r_} {top} {r_} {top + 14}V{top + chh - 12}Q{r_} {top + chh} {r_ - 8} {top + chh + 2}Q{ccx} {top + chh + 9} {l + 8} {top + chh + 2}Q{l} {top + chh} {l} {top + chh - 12}V{top + 14}Q{l} {top} {l + 6} {top}Z"/></clipPath>
    <linearGradient id="canBlue" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#1D3E96"/><stop offset="1" stop-color="#0B1E5B"/></linearGradient>
    <pattern id="checker" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(45 {ccx} {top})">
      <rect width="16" height="16" fill="#D7DCE5"/><rect width="8" height="8" fill="#1D3E96"/><rect x="8" y="8" width="8" height="8" fill="#1D3E96"/>
    </pattern>
    <linearGradient id="canShade" x1="0" x2="1">
      <stop stop-color="#000" stop-opacity=".35"/><stop offset=".18" stop-color="#FFF" stop-opacity=".45"/>
      <stop offset=".32" stop-color="#FFF" stop-opacity="0"/><stop offset=".75" stop-color="#000" stop-opacity=".05"/>
      <stop offset="1" stop-color="#000" stop-opacity=".45"/>
    </linearGradient>
    <linearGradient id="label" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#F1F3F7"/><stop offset="1" stop-color="#D5DAE3"/></linearGradient>
    <linearGradient id="lid" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#EEF1F5"/><stop offset="1" stop-color="#A9B1BE"/></linearGradient>"""
    css = f"""
    .spinA{{transform-origin:{cx}px {cy}px;animation:spin 40s linear infinite;}}
    .spinB{{transform-origin:{cx}px {cy}px;animation:spin 64s linear infinite reverse;}}
    .spinA .upright{{transform-box:fill-box;transform-origin:center;animation:spin 40s linear infinite reverse;}}
    .spinB .upright{{transform-box:fill-box;transform-origin:center;animation:spin 64s linear infinite;}}
    @keyframes spin{{to{{transform:rotate(360deg);}}}}
    .spot{{opacity:0;animation:spot {cycle:.1f}s ease-in-out infinite;}}
    @keyframes spot{{0%{{opacity:0;}}2%,{100 / len(TOOLS) - 1:.1f}%{{opacity:1;}}{100 / len(TOOLS) + 2:.1f}%,100%{{opacity:0;}}}}
    .wave{{transform-box:fill-box;transform-origin:center;animation:wave 3s ease-out infinite;}}
    @keyframes wave{{from{{transform:scale(1);opacity:.7;}}to{{transform:scale(1.9);opacity:0;}}}}
    .can{{transform-box:fill-box;transform-origin:center;animation:can 6s ease-in-out infinite;}}
    @keyframes can{{0%,100%{{transform:translateY(0) rotate(-3deg);}}50%{{transform:translateY(-10px) rotate(3deg);}}}}
    .bub{{animation:bub 4s ease-in infinite;}}
    @keyframes bub{{0%{{transform:translateY(0);opacity:0;}}15%{{opacity:1;}}100%{{transform:translateY(-250px);opacity:0;}}}}
    @media (prefers-reduced-motion: reduce){{.spot,.bub{{opacity:0;}}}}"""
    names = ", ".join(ICONS[s_]["title"] for s_ in TOOLS)
    return svg(t, W, H, "".join(parts), "Toolkit",
               f"Toolkit of {len(TOOLS)} tools with Python at the core and the rest orbiting around it: {names}. "
               "Beside it, a floating Red Bull can: fueled by Red Bull — late nights, big ideas.", css, defs)


# ───────────────────────── python showcase ─────────────────────────
PY_LOGO = "M49 6C30 6 31 14 31 14V24H50V27H23C23 27 10 26 10 45C10 64 21 63 21 63H28V54C28 54 27 43 39 43H58C58 43 69 43 69 32V15C69 15 71 6 49 6Z"

CODE = [
    [("# ishan.py", "com")],
    [("class ", "kw"), ("Ishan", "fn"), (":", "")],
    [("    craft = [", ""), ('"web products"', "str"), (", ", ""), ('"python tools"', "str"), (", ", ""), ('"ai experiments"', "str"), ("]", "")],
    [("    loop  = [", ""), ('"learn"', "str"), (", ", ""), ('"build"', "str"), (", ", ""), ('"ship"', "str"), (", ", ""), ('"improve"', "str"), ("]", "")],
    [],
    [("    def ", "kw"), ("build", "fn"), ("(self, idea):", "")],
    [("        while ", "kw"), ("True", "kw"), (":", "")],
    [("            idea = ", ""), ("improve", "fn"), ("(idea)", "")],
    [("            yield ", "kw"), ("ship", "fn"), ("(idea)", "")],
    [],
    [("Ishan", "fn"), ("().", ""), ("build", "fn"), ("(", ""), ('"what\'s next"', "str"), (")", "")],
]


def python_card(t):
    H = 340
    dark = t.get("dark")
    syn = dict(kw="#C4B5FD" if dark else "#7C3AED", fn="#93C5FD" if dark else "#2563EB",
               str="#86EFAC" if dark else "#059669", com=t["text3"])
    syn[""] = t["text"]
    ex, ey, ew, eh = 456, 20, W - 476, H - 40
    lines = []
    for i, segs in enumerate(CODE):
        y = ey + 72 + i * 21
        spans = "".join(f'<tspan fill="{syn[k]}">{esc(txt)}</tspan>' for txt, k in segs)
        lines.append(f'<g class="type" style="animation-delay:{.25 + i * .14:.2f}s">'
                     f'<text class="f-mono" x="{ex + 40}" y="{y}" text-anchor="end" font-size="12" fill="{t["text3"]}" fill-opacity=".7">{i + 1}</text>'
                     f'<text class="f-mono" x="{ex + 60}" y="{y}" font-size="14" xml:space="preserve">{spans}</text></g>')
    last = "".join(txt for txt, _ in CODE[-1])
    cur_x = ex + 60 + measure(last, 14, "mono") + 3
    cur_y = ey + 72 + (len(CODE) - 1) * 21
    defs = f"""
    <linearGradient id="pyb" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#5A9FD4"/><stop offset="1" stop-color="#306998"/></linearGradient>
    <linearGradient id="pyy" x1="1" y1="1" x2="0" y2="0"><stop stop-color="#FFE873"/><stop offset="1" stop-color="#FFD43B"/></linearGradient>
    <clipPath id="ed"><rect x="{ex}" y="{ey}" width="{ew}" height="{eh}" rx="16"/></clipPath>"""
    css = """
    .type{animation:type .5s cubic-bezier(.2,.7,.2,1) both;}
    @keyframes type{from{opacity:0;transform:translateX(-8px);}to{opacity:1;transform:none;}}
    .cur{animation:cur 1.1s steps(1) infinite;} @keyframes cur{50%{opacity:0;}}
    .bob{animation:bob 6s ease-in-out infinite;} @keyframes bob{50%{transform:translateY(-6px);}}"""
    body = f"""
  {tile(t, 0, 0, W, H, glow=(220, 60, "#3776AB"))}
  <g clip-path="url(#tc0_0)"><circle cx="300" cy="{H}" r="120" fill="#FFD43B" opacity="{t['aur_op'] * .35:.2f}" filter="url(#blur)"/></g>
  {eyebrow(t, 32, 48, "PRIMARY LANGUAGE")}
  <g class="bob">
    <circle cx="74" cy="114" r="46" fill="{t['surface2']}" stroke="{t['hair']}" stroke-opacity="{t['hair_op'] * 1.6:.2f}"/>
    <g transform="translate(46 86) scale(.56)">
      <path d="{PY_LOGO}" fill="url(#pyb)"/><circle cx="39" cy="14.5" r="3.6" fill="#FFFFFF"/>
      <g transform="rotate(180 50 50)"><path d="{PY_LOGO}" fill="url(#pyy)"/><circle cx="39" cy="14.5" r="3.6" fill="#FFFFFF"/></g>
    </g>
  </g>
  <text class="f-sans" x="30" y="222" font-size="50" font-weight="600" letter-spacing="-2" fill="url(#headg)">Python <tspan class="f-serif" font-size="56" font-weight="400" letter-spacing="-.5" fill="url(#aur)">is home.</tspan></text>
  <g class="f-sans" font-size="15.5" fill="{t['text2']}">
    <text x="32" y="260">Where most of my ideas start: scripts,</text>
    <text x="32" y="283">data analysis, games and AI experiments.</text>
  </g>
  {eyebrow(t, 32, 314, "SCRIPTS  ·  DATA  ·  GAMES  ·  AI")}

  <g clip-path="url(#ed)">
    <rect x="{ex}" y="{ey}" width="{ew}" height="{eh}" fill="{t['bg']}"/>
    <rect x="{ex}" y="{ey}" width="{ew}" height="40" fill="{t['surface2']}"/>
    <path d="M{ex} {ey + 40.5}H{ex + ew}" stroke="{t['hair']}" stroke-opacity="{t['hair_op']}"/>
    <circle cx="{ex + 22}" cy="{ey + 20}" r="5.5" fill="#FF5F57"/><circle cx="{ex + 40}" cy="{ey + 20}" r="5.5" fill="#FEBC2E"/><circle cx="{ex + 58}" cy="{ey + 20}" r="5.5" fill="#28C840"/>
    <text class="f-mono" x="{ex + ew / 2}" y="{ey + 24.5}" text-anchor="middle" font-size="12" fill="{t['text3']}">ishan.py</text>
    <text class="f-mono" x="{ex + ew - 20}" y="{ey + 24.5}" text-anchor="end" font-size="11" letter-spacing="1" fill="{t['text3']}">PYTHON 3</text>
    {''.join(lines)}
    <rect class="cur" x="{cur_x:.1f}" y="{cur_y - 13}" width="8" height="17" rx="1" fill="{t['accent']}"/>
  </g>
  <rect x="{ex + .5}" y="{ey + .5}" width="{ew - 1}" height="{eh - 1}" rx="15.5" stroke="{t['hair']}" stroke-opacity="{t['hair_op'] * 1.4:.2f}"/>"""
    code_text = " / ".join("".join(x for x, _ in l) for l in CODE if l)
    return svg(t, W, H, body, "Python is home",
               "Primary language: Python, where most of my ideas start: scripts, data analysis, games and AI experiments. "
               f"An editor shows ishan.py: {code_text}", css, defs)



if __name__ == "__main__":
    import f1

    made = [
        write("hero.svg", f1.hero(redbull_logo, RB_W)),
        write("about.svg", f1.driver(redbull_logo, RB_W)),
        write("toolkit.svg", toolkit(F1)),
        write("python.svg", python_card(F1)),
        write("footer.svg", f1.footer(redbull_logo, RB_W)),
    ]
    for slug, num, title, sub in f1.SECTIONS:
        made.append(write(f"section-{slug}.svg", f1.section(num, title, sub)))
    for i, p in enumerate(f1.PROJECTS):
        made.append(write(f"project-{p[0]}.svg", f1.project(i, *p)))
    for slug, label, primary in [("work", "VIEW MY WORK", True), ("instagram", "INSTAGRAM", False),
                                 ("github", "FOLLOW ON GITHUB", True), ("repos", "ALL REPOSITORIES", False)]:
        made.append(write(f"btn-{slug}.svg", f1.button(label, primary)))
    print(f"built {len(made)} files")
