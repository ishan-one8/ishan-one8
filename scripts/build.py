"""Builds every static SVG on the profile (dark + light).

    pip install fonttools brotli
    python scripts/build.py

The live numbers card is built separately by scripts/stats.py.
"""
import math

from kit import THEMES, both, eyebrow, esc, measure, svg, tile

W = 1200


# ───────────────────────── hero ─────────────────────────
def hero(t):
    H = 520
    cx, cy = 925, 255
    ring = lambda rx, ry, sweep: f"M{cx - rx} {cy}A{rx} {ry} 0 0 {sweep} {cx + rx} {cy}"
    rings_back = "".join(
        f'<path d="{ring(rx, ry, 1)}" stroke="url(#ringg)" stroke-width="{sw}" stroke-opacity="{op}"/>'
        for rx, ry, sw, op in [(250, 62, 1, .55), (205, 50, 1.2, .8), (300, 74, .8, .35)])
    rings_front = "".join(
        f'<path d="{ring(rx, ry, 0)}" stroke="url(#ringg)" stroke-width="{sw}" stroke-opacity="{op}"/>'
        for rx, ry, sw, op in [(250, 62, 1, .55), (205, 50, 1.2, .8), (300, 74, .8, .35)])
    orbit = f"M{cx - 250} {cy}A250 62 0 1 0 {cx + 250} {cy}A250 62 0 1 0 {cx - 250} {cy}"
    orbit2 = f"M{cx + 205} {cy}A205 50 0 1 0 {cx - 205} {cy}A205 50 0 1 0 {cx + 205} {cy}"
    dark = t["bg"] == "#08080A"

    defs = f"""
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="28"/></clipPath>
    <linearGradient id="bgg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{t['bg']}"/><stop offset="1" stop-color="{t['bg2']}"/></linearGradient>
    <radialGradient id="dotmask" cx=".72" cy=".45" r=".55"><stop stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
    <mask id="dm"><rect width="{W}" height="{H}" fill="url(#dotmask)"/></mask>
    <radialGradient id="sphere" cx=".38" cy=".32" r=".78">
      <stop stop-color="{'#E0E7FF' if dark else '#FFFFFF'}"/>
      <stop offset=".22" stop-color="{'#A5B4FC' if dark else '#C7D2FE'}"/>
      <stop offset=".55" stop-color="{t['a1']}"/>
      <stop offset=".85" stop-color="{'#2E1065' if dark else '#7C3AED'}"/>
      <stop offset="1" stop-color="{'#120A2A' if dark else '#5B21B6'}"/>
    </radialGradient>
    <linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="{t['a3']}" stop-opacity=".9"/><stop offset=".5" stop-color="{t['a3']}" stop-opacity="0"/>
      <stop offset="1" stop-color="#F472B6" stop-opacity=".55"/>
    </linearGradient>
    <linearGradient id="ringg" x1="0" x2="1"><stop stop-color="{t['text']}" stop-opacity="0"/><stop offset=".5" stop-color="{t['text']}"/><stop offset="1" stop-color="{t['text']}" stop-opacity="0"/></linearGradient>
    <linearGradient id="shineU" gradientUnits="userSpaceOnUse" x1="-260" y1="0" x2="-40" y2="0" gradientTransform="skewX(-20)">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset=".5" stop-color="#FFFFFF" stop-opacity="{.7 if dark else .6}"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="0 0;0 0;1000 0" keyTimes="0;.55;1" dur="7s" repeatCount="indefinite" additive="sum"/>
    </linearGradient>"""
    css = f"""
    .drift1{{animation:d1 16s ease-in-out infinite alternate;}}
    .drift2{{animation:d2 19s ease-in-out infinite alternate;}}
    .drift3{{animation:d3 13s ease-in-out infinite alternate;}}
    @keyframes d1{{to{{transform:translate(-70px,40px);}}}}
    @keyframes d2{{to{{transform:translate(60px,-50px);}}}}
    @keyframes d3{{to{{transform:translate(80px,30px);}}}}
    .float{{animation:fl 7s ease-in-out infinite;}}
    @keyframes fl{{50%{{transform:translateY(-10px);}}}}
    .spin{{transform-origin:{cx}px {cy}px;animation:sp 22s linear infinite;}}
    @keyframes sp{{to{{transform:rotate(360deg);}}}}
    .rise{{animation:rise 1.1s cubic-bezier(.2,.7,.2,1) both;}}
    .r2{{animation-delay:.12s;}} .r3{{animation-delay:.24s;}} .r4{{animation-delay:.36s;}} .r5{{animation-delay:.48s;}}
    @keyframes rise{{from{{opacity:0;transform:translateY(14px);}}to{{opacity:1;transform:none;}}}}
    .ping{{transform-box:fill-box;transform-origin:center;animation:ping 2.4s cubic-bezier(0,0,.2,1) infinite;}}
    @keyframes ping{{75%,100%{{transform:scale(2.6);opacity:0;}}}}"""
    pill_w = 22 + 14 + measure("Available to build", 13.5, weight=500) + 18
    body = f"""
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#bgg)"/>
  <g filter="url(#blur)" opacity="{t['aur_op']}">
    <circle class="drift1" cx="860" cy="150" r="190" fill="{t['a1']}"/>
    <circle class="drift2" cx="1060" cy="360" r="170" fill="{t['a2']}"/>
    <circle class="drift3" cx="700" cy="430" r="140" fill="{t['a3']}"/>
  </g>
  <rect width="{W}" height="{H}" fill="url(#dots)" mask="url(#dm)"/>

  <!-- orb -->
  <g class="float">
    <g transform="rotate(-14 {cx} {cy})">{rings_back}</g>
    <circle cx="{cx}" cy="{cy}" r="170" fill="{t['a1']}" opacity="{.35 if dark else .22}" filter="url(#blurS)"/>
    <circle cx="{cx}" cy="{cy}" r="118" fill="url(#sphere)"/>
    <g class="spin" opacity=".55"><circle cx="{cx}" cy="{cy}" r="118" fill="url(#sheen)" style="mix-blend-mode:screen"/></g>
    <ellipse cx="{cx - 38}" cy="{cy - 50}" rx="44" ry="26" fill="#FFFFFF" opacity=".55" filter="url(#blurS)" transform="rotate(-30 {cx - 38} {cy - 50})"/>
    <circle cx="{cx}" cy="{cy}" r="117.5" stroke="#FFFFFF" stroke-opacity=".25"/>
    <g transform="rotate(-14 {cx} {cy})">{rings_front}
      <circle r="4" fill="{t['text']}"><animateMotion dur="9s" repeatCount="indefinite" path="{orbit}"/></circle>
      <circle r="3" fill="{t['accent']}"><animateMotion dur="13s" repeatCount="indefinite" path="{orbit2}"/></circle>
    </g>
  </g>

  <!-- top bar -->
  <rect x="56" y="44" width="44" height="44" rx="13" fill="{t['surface2']}" stroke="{t['hair']}" stroke-opacity="{t['hair_op'] * 1.6:.2f}"/>
  <text class="f-sans" x="78" y="72" text-anchor="middle" font-size="16" font-weight="650" letter-spacing="-.3" fill="{t['text']}">IK</text>
  <text class="f-mono" x="116" y="71" font-size="13" fill="{t['text3']}">ishan-one8</text>
  <g transform="translate({W - 56 - pill_w} 48)">
    <rect width="{pill_w:.0f}" height="36" rx="18" fill="{t['surface2']}" fill-opacity=".8" stroke="{t['hair']}" stroke-opacity="{t['hair_op'] * 1.6:.2f}"/>
    <circle class="ping" cx="22" cy="18" r="4.5" fill="{t['good']}"/>
    <circle cx="22" cy="18" r="4.5" fill="{t['good']}"/>
    <text class="f-sans" x="36" y="22.5" font-size="13.5" font-weight="500" fill="{t['text']}">Available to build</text>
  </g>

  <!-- headline -->
  <g class="rise">{eyebrow(t, 58, 190, "DEVELOPER  ·  BUILDER  ·  PRODUCT THINKER")}</g>
  <g class="rise r2">
    <text class="f-sans" x="52" y="282" font-size="96" font-weight="640" letter-spacing="-4.2" fill="url(#headg)">Ishan Kumar</text>
    <text class="f-sans" x="52" y="282" font-size="96" font-weight="640" letter-spacing="-4.2" fill="url(#shineU)">Ishan Kumar</text>
  </g>
  <text class="f-sans rise r3" x="56" y="346" font-size="44" font-weight="400" letter-spacing="-1.4" fill="{t['text2']}">Building <tspan class="f-serif" font-size="52" letter-spacing="-.5" fill="url(#aur)">what's next.</tspan></text>
  <g class="rise r4 f-sans" font-size="17" fill="{t['text2']}">
    <text x="57" y="398">I turn ideas into software that ships — web products,</text>
    <text x="57" y="423">Python tools and AI experiments, built end to end.</text>
  </g>

  <!-- footer strip -->
  <path d="M56 458H{W - 56}" stroke="{t['hair']}" stroke-opacity="{t['hair_op']}"/>
  <g class="rise r5">
    {eyebrow(t, 56, 489, "PYTHON  ·  TYPESCRIPT  ·  REACT  ·  NEXT.JS  ·  AI")}
    {eyebrow(t, W - 56, 489, "LEARN  ·  BUILD  ·  SHIP  ·  IMPROVE", "end")}
  </g>
  <rect width="{W}" height="{H}" filter="url(#grain)" opacity=".9"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="27.5" stroke="{t['hair']}" stroke-opacity="{t['hair_op'] * 1.3:.2f}"/>
<path d="M60 .6H{W - 60}" stroke="url(#hi)"/>"""
    return svg(t, W, H, body, "Ishan Kumar — building what's next",
               "Developer, builder and product thinker. A glass orb with orbiting rings floats over a soft aurora; "
               "headline: Ishan Kumar, building what's next. Available to build.", css, defs)


# ───────────────────────── section headers ─────────────────────────
SECTIONS = [
    ("about", "01", "ABOUT", "Ideas in, ", "products out."),
    ("work", "02", "SELECTED WORK", "Things I've ", "built."),
    ("stack", "03", "TOOLKIT", "Powered by ", "Python."),
    ("numbers", "04", "BY THE NUMBERS", "Live from ", "GitHub."),
    ("activity", "05", "ACTIVITY", "Always ", "shipping."),
]


def section(num, label, plain, italic):
    def f(t):
        tw = measure(plain, 40, weight=600, spacing=-1.2) + measure(italic, 46, "serif") + 28
        body = f"""
  {eyebrow(t, 2, 26, f"{num}  —  {label}")}
  <text class="f-sans" x="0" y="80" font-size="40" font-weight="600" letter-spacing="-1.2" fill="{t['text']}">{esc(plain)}<tspan class="f-serif" font-size="46" font-weight="400" letter-spacing="0" fill="url(#aur)">{esc(italic)}</tspan></text>
  <path d="M{tw:.0f} 66H{W}" stroke="{t['hair']}" stroke-opacity="{t['hair_op']}"/>
  <circle cx="{W - 4}" cy="66" r="3" fill="{t['text3']}"/>"""
        return svg(t, W, 100, body, f"{num} — {label.title()}", f"Section {num}: {plain}{italic}")
    return f


# ───────────────────────── about bento ─────────────────────────
def bento(t):
    g = 16
    cw = (W - 2 * g) / 3
    x1, x2, x3 = 0, cw + g, 2 * (cw + g)
    r1h, r2h = 250, 290
    y2 = r1h + g
    H = y2 + r2h
    parts = []

    # A — about
    parts.append(tile(t, x1, 0, 2 * cw + g, r1h, glow=(2 * cw, 20, t["a1"])))
    parts.append(eyebrow(t, x1 + 32, 46, "ABOUT"))
    lines = [
        ("I take ideas from the first sketch to a", None),
        ("", "working product"),
        ("web experiences, Python tools, data", None),
        ("and AI experiments.", None),
    ]
    parts.append(f"""
  <g class="f-sans" font-size="29" font-weight="500" letter-spacing="-.8" fill="{t['text']}">
    <text x="{x1 + 32}" y="104">I take ideas from the first sketch to a</text>
    <text x="{x1 + 32}" y="144"><tspan class="f-serif" font-size="34" font-weight="400" letter-spacing="0" fill="url(#aur)">working product</tspan> — web experiences,</text>
    <text x="{x1 + 32}" y="184" fill="{t['text2']}">Python tools, data and AI experiments.</text>
  </g>
  {eyebrow(t, x1 + 32, 222, "LEARNING BY SHIPPING REAL PROJECTS")}""")

    # B — status
    parts.append(tile(t, x3, 0, cw, r1h, glow=(x3 + cw, r1h, t["good"])))
    parts.append(eyebrow(t, x3 + 28, 46, "STATUS"))
    parts.append(f"""
  <circle class="ping" cx="{x3 + 36}" cy="96" r="6" fill="{t['good']}"/>
  <circle cx="{x3 + 36}" cy="96" r="6" fill="{t['good']}"/>
  <text class="f-sans" x="{x3 + 54}" y="105" font-size="26" font-weight="600" letter-spacing="-.7" fill="{t['text']}">Open to build</text>
  <g class="f-sans" font-size="15.5" fill="{t['text2']}">
    <text x="{x3 + 28}" y="148">Currently turning ideas into</text>
    <text x="{x3 + 28}" y="171">useful software.</text>
  </g>
  <rect x="{x3 + 28}" y="198" width="{cw - 56:.0f}" height="1" fill="{t['hair']}" fill-opacity="{t['hair_op']}"/>
  {eyebrow(t, x3 + 28, 226, "COLLABS · HACKATHONS · IDEAS")}""")

    # C — the loop
    parts.append(tile(t, x1, y2, cw, r2h))
    parts.append(eyebrow(t, x1 + 28, y2 + 44, "THE LOOP"))
    lcx, lcy, lr = x1 + cw / 2, y2 + 166, 70
    circ = f"M{lcx} {lcy - lr}A{lr} {lr} 0 1 1 {lcx - .01} {lcy - lr}"
    nodes = [("Learn", 0), ("Build", 90), ("Ship", 180), ("Improve", 270)]
    nd = []
    for i, (name, ang) in enumerate(nodes):
        a = math.radians(ang - 90)
        nx, ny = lcx + lr * math.cos(a), lcy + lr * math.sin(a)
        lx, ly, anc = nx, ny, "middle"
        if ang == 0: ly -= 16
        if ang == 180: ly += 26
        if ang == 90: lx += 16; ly += 5; anc = "start"
        if ang == 270: lx -= 16; ly += 5; anc = "end"
        nd.append(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="5" fill="{t["surface"]}" stroke="{t["text2"]}" stroke-width="1.5"/>'
                  f'<text class="f-sans" x="{lx:.1f}" y="{ly:.1f}" font-size="14.5" font-weight="500" text-anchor="{anc}" fill="{t["text"]}">{name}</text>')
    parts.append(f"""
  <circle cx="{lcx}" cy="{lcy}" r="{lr}" stroke="{t['hair']}" stroke-opacity="{t['hair_op'] * 2:.2f}" stroke-dasharray="2 5"/>
  <path d="{circ}" stroke="url(#aur)" stroke-width="2" stroke-linecap="round" pathLength="100" stroke-dasharray="22 78">
    <animate attributeName="stroke-dashoffset" from="22" to="-78" dur="6s" repeatCount="indefinite"/>
  </path>
  {''.join(nd)}
  <circle r="5" fill="{t['text']}"><animateMotion dur="6s" repeatCount="indefinite" path="{circ}"/></circle>
  <text class="f-mono" x="{lcx}" y="{lcy + 4}" text-anchor="middle" font-size="10.5" letter-spacing="1.5" fill="{t['text3']}">REPEAT</text>""")

    # D — focus
    parts.append(tile(t, x2, y2, cw, r2h))
    parts.append(eyebrow(t, x2 + 28, y2 + 44, "FOCUS"))
    icons = {
        "ai": f'<path d="M0 -8C1 -2 2 -1 8 0C2 1 1 2 0 8C-1 2 -2 1 -8 0C-2 -1 -1 -2 0 -8Z" fill="{t["accent"]}"/>',
        "web": f'<rect x="-8" y="-6.5" width="16" height="13" rx="2.5" stroke="{t["accent"]}" stroke-width="1.6"/><path d="M-8 -2.5H8" stroke="{t["accent"]}" stroke-width="1.6"/>',
        "py": f'<path d="M-6 -4L-1 0L-6 4M1 5H7" stroke="{t["accent"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
    }
    rows = [("ai", "AI experiments", "LLMs · agents"), ("web", "Web products", "React · Next.js"), ("py", "Python projects", "data · tools")]
    for i, (ic, name, tag) in enumerate(rows):
        ry = y2 + 92 + i * 62
        parts.append(f"""
  <g class="rise r{i + 2}">
    <rect x="{x2 + 28}" y="{ry - 18}" width="36" height="36" rx="10" fill="{t['surface2']}" stroke="{t['hair']}" stroke-opacity="{t['hair_op'] * 1.5:.2f}"/>
    <g transform="translate({x2 + 46} {ry})">{icons[ic]}</g>
    <text class="f-sans" x="{x2 + 78}" y="{ry - 1}" font-size="16" font-weight="550" fill="{t['text']}">{name}</text>
    <text class="f-mono" x="{x2 + 78}" y="{ry + 16}" font-size="11.5" fill="{t['text3']}">{tag}</text>
  </g>""")
        if i < 2:
            parts.append(f'<path d="M{x2 + 28} {ry + 31}H{x2 + cw - 28:.0f}" stroke="{t["hair"]}" stroke-opacity="{t["hair_op"]}"/>')

    # E — stack
    parts.append(tile(t, x3, y2, cw, r2h, glow=(x3, y2 + r2h, t["a2"])))
    parts.append(eyebrow(t, x3 + 28, y2 + 44, "DAILY DRIVERS"))
    stack = ["Python", "TypeScript", "JavaScript", "React", "Next.js", "Node.js", "Git", "Actions"]
    px, py = x3 + 28, y2 + 70
    for i, s in enumerate(stack):
        w = measure(s, 13, "mono") + 26
        if px + w > x3 + cw - 24:
            px, py = x3 + 28, py + 44
        parts.append(f"""
  <g class="rise" style="animation-delay:{.08 * i:.2f}s">
    <rect x="{px:.1f}" y="{py}" width="{w:.1f}" height="34" rx="10" fill="{t['surface2']}" stroke="{t['hair']}" stroke-opacity="{t['hair_op'] * 1.5:.2f}"/>
    <text class="f-mono" x="{px + 13:.1f}" y="{py + 21.5}" font-size="13" fill="{t['text']}">{s}</text>
  </g>""")
        px += w + 8

    css = """
    .rise{animation:rise .9s cubic-bezier(.2,.7,.2,1) both;}
    .r2{animation-delay:.1s;} .r3{animation-delay:.2s;} .r4{animation-delay:.3s;}
    @keyframes rise{from{opacity:0;transform:translateY(10px);}to{opacity:1;transform:none;}}
    .ping{transform-box:fill-box;transform-origin:center;animation:ping 2.4s cubic-bezier(0,0,.2,1) infinite;}
    @keyframes ping{75%,100%{transform:scale(2.6);opacity:0;}}"""
    return svg(t, W, H, "".join(parts), "About Ishan",
               "About: I take ideas from the first sketch to a working product — web experiences, Python tools, data and AI experiments. "
               "Status: open to build. The loop: learn, build, ship, improve. Focus: AI experiments, web products, Python projects. "
               "Daily drivers: Python, TypeScript, JavaScript, React, Next.js, Node.js, Git, GitHub Actions.", css)


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
    dark = t is THEMES["dark"]
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


# ───────────────────────── project cards ─────────────────────────
CW, CH = 590, 340
VX, VY, VW, VH = 12, 12, CW - 24, 184


def vis_interview(t):
    bars = []
    for i in range(30):
        h = 10 + 26 * abs(math.sin(i * .7)) + 10 * abs(math.sin(i * 1.9))
        bars.append(f'<rect class="wv" style="animation-delay:{-i * .09:.2f}s" x="{340 + i * 7}" y="{104 - h / 2:.1f}" width="3.5" height="{h:.1f}" rx="1.75" fill="url(#aur)"/>')
    return f"""
  <rect x="36" y="38" width="250" height="44" rx="14" fill="{t['surface']}" stroke="{t['hair']}" stroke-opacity="{t['hair_op'] * 1.5:.2f}"/>
  <text class="f-sans" x="52" y="65" font-size="13.5" fill="{t['text']}">How would you design a rate limiter?</text>
  <rect x="76" y="96" width="232" height="44" rx="14" fill="{t['a1']}" fill-opacity="{.22 if t['bg'] == '#08080A' else .12}" stroke="{t['a1']}" stroke-opacity=".35"/>
  <text class="f-sans" x="92" y="123" font-size="13.5" fill="{t['text']}">Token bucket, per user</text>
  <circle class="ty" cx="264" cy="118" r="2.5" fill="{t['text2']}"/><circle class="ty" style="animation-delay:.2s" cx="273" cy="118" r="2.5" fill="{t['text2']}"/><circle class="ty" style="animation-delay:.4s" cx="282" cy="118" r="2.5" fill="{t['text2']}"/>
  {''.join(bars)}
  <circle class="ping" cx="348" cy="160" r="3.5" fill="#F43F5E"/><circle cx="348" cy="160" r="3.5" fill="#F43F5E"/>
  <text class="f-mono" x="360" y="164" font-size="11" letter-spacing="1.5" fill="{t['text3']}">LIVE · ADAPTIVE</text>"""


def vis_cricket(t):
    vals = [6, 9, 4, 11, 8, 13, 7, 10, 15, 9, 12, 18, 8, 14, 11, 16, 20, 13, 17, 22]
    base, bw, gap, x0 = 160, 18, 7, 44
    out, pts = [], []
    for i, v in enumerate(vals):
        h = v * 5.4
        x = x0 + i * (bw + gap)
        out.append(f'<rect class="grow" style="animation-delay:{i * .04:.2f}s" x="{x}" y="{base - h:.1f}" width="{bw}" height="{h:.1f}" rx="4" fill="{t["text"]}" fill-opacity="{.10 + v / 22 * .22:.2f}"/>')
        rr = sum(vals[:i + 1]) / (i + 1)
        pts.append(f"{x + bw / 2:.1f},{base - rr * 7.2:.1f}")
    return f"""
  <path d="M{x0} {base + .5}H{x0 + 20 * (bw + gap) - gap}" stroke="{t['hair']}" stroke-opacity="{t['hair_op'] * 2:.2f}"/>
  {''.join(out)}
  <polyline class="draw" points="{' '.join(pts)}" stroke="url(#aur)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" pathLength="100"/>
  <text class="f-mono" x="{x0}" y="36" font-size="11" letter-spacing="1.5" fill="{t['text3']}">RUNS PER OVER</text>
  <text class="f-mono" x="{x0 + 20 * (bw + gap) - gap}" y="36" text-anchor="end" font-size="11" letter-spacing="1.5" fill="{t['accent']}">— RUN RATE</text>"""


def vis_hand(t):
    out = []
    for i in range(6):
        x = 50 + i * 82
        out.append(f"""
  <rect x="{x}" y="92" width="66" height="66" rx="16" fill="{t['surface']}" stroke="{t['hair']}" stroke-opacity="{t['hair_op'] * 1.6:.2f}"/>
  <rect class="pick" style="animation-delay:{i * 1:.0f}s" x="{x}" y="92" width="66" height="66" rx="16" fill="url(#aur)"/>
  <text class="f-sans" x="{x + 33}" y="134" text-anchor="middle" font-size="26" font-weight="600" fill="{t['text']}">{i + 1}</text>""")
    return f"""
  <text class="f-mono" x="50" y="44" font-size="13" fill="{t['text3']}">$ python hand_cricket.py</text>
  <text class="f-mono" x="50" y="68" font-size="13" fill="{t['text']}">&gt; your move<tspan fill="{t['text3']}"> · cpu is thinking</tspan></text>
  <rect class="cur" x="{50 + 8 + measure('> your move · cpu is thinking', 13, 'mono'):.0f}" y="57" width="8" height="15" rx="1" fill="{t['accent']}"/>
  {''.join(out)}"""


def vis_marks(t):
    pts = []
    for i in range(0, 101):
        x = 44 + i * 4.9
        y = 160 - 112 * math.exp(-((i - 56) / 17) ** 2)
        pts.append(f"{x:.1f},{y:.1f}")
    area = "M44,160 L" + " L".join(pts) + f" L{44 + 100 * 4.9:.1f},160 Z"
    bands = [("D", 44, 172), ("C", 216, 118), ("B", 334, 118), ("A", 452, 82)]
    out = []
    for g_, x, w in bands:
        out.append(f'<text class="f-mono" x="{x + w / 2:.0f}" y="40" text-anchor="middle" font-size="12" fill="{t["text3"]}">{g_}</text>')
        if x > 44:
            out.append(f'<path d="M{x} 52V160" stroke="{t["hair"]}" stroke-opacity="{t["hair_op"] * 1.6:.2f}" stroke-dasharray="3 4"/>')
    dots = []
    for i in range(26):
        x = 70 + (i * 37) % 460
        y = 150 - 100 * math.exp(-(((x - 44) / 4.9 - 56) / 17) ** 2) * (.25 + (i * 7 % 10) / 14)
        dots.append(f'<circle class="pop" style="animation-delay:{i * .05:.2f}s" cx="{x}" cy="{y:.1f}" r="3" fill="{t["text"]}" fill-opacity=".55"/>')
    mx = 44 + 56 * 4.9
    return f"""
  <linearGradient id="area" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{t['a1']}" stop-opacity=".45"/><stop offset="1" stop-color="{t['a1']}" stop-opacity="0"/></linearGradient>
  {''.join(out)}
  <path d="{area}" fill="url(#area)"/>
  <polyline class="draw" points="{' '.join(pts)}" stroke="url(#aur)" stroke-width="2.5" pathLength="100" stroke-linecap="round"/>
  <path d="M{mx:.1f} 50V160" stroke="{t['text']}" stroke-opacity=".5"/>
  <text class="f-mono" x="{mx + 7:.1f}" y="40" font-size="11" letter-spacing="1.5" fill="{t['text2']}">MEAN</text>
  {''.join(dots)}
  <path d="M44 160.5H534" stroke="{t['hair']}" stroke-opacity="{t['hair_op'] * 2:.2f}"/>"""


PROJECTS = [
    ("interviewos", "01", "InterviewOS", ["Adaptive AI technical interviews with a", "polished, real-time candidate experience."], ["TypeScript", "AI", "Web"], vis_interview),
    ("cricket", "02", "Cricket Score Analysis", ["Exploring cricket scores and match patterns", "through Python data analysis."], ["Python", "Data"], vis_cricket),
    ("hand-cricket", "03", "Hand Cricket Game", ["The playground classic, rebuilt as an", "interactive terminal game."], ["Python", "CLI", "Game logic"], vis_hand),
    ("marks", "04", "Student Marks Analyser", ["Turning raw student marks into clear", "performance insights and grade spreads."], ["Python", "Analytics"], vis_marks),
]


def project(num, title, desc, tags, vis):
    def f(t):
        tags_svg, x = [], 28
        for s in tags:
            w = measure(s, 12, "mono") + 22
            tags_svg.append(f'<rect x="{x:.1f}" y="296" width="{w:.1f}" height="26" rx="8" fill="{t["surface2"]}" stroke="{t["hair"]}" stroke-opacity="{t["hair_op"] * 1.5:.2f}"/>'
                            f'<text class="f-mono" x="{x + 11:.1f}" y="313" font-size="12" fill="{t["text2"]}">{esc(s)}</text>')
            x += w + 8
        defs = f"""
    <clipPath id="vc"><rect x="{VX}" y="{VY}" width="{VW}" height="{VH}" rx="14"/></clipPath>
    <linearGradient id="vbg" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{t['bg2']}"/><stop offset="1" stop-color="{t['bg']}"/></linearGradient>"""
        css = """
    .wv{transform-box:fill-box;transform-origin:center;animation:wv 1.3s ease-in-out infinite alternate;}
    @keyframes wv{from{transform:scaleY(.25);}to{transform:scaleY(1);}}
    .ty{animation:ty 1.2s ease-in-out infinite;} @keyframes ty{50%{opacity:.2;}}
    .grow{transform-box:fill-box;transform-origin:bottom;animation:grow 1s cubic-bezier(.2,.7,.2,1) both;}
    @keyframes grow{from{transform:scaleY(0);}}
    .draw{stroke-dasharray:100;animation:draw 5s ease-in-out infinite;}
    @keyframes draw{0%{stroke-dashoffset:100;}40%,85%{stroke-dashoffset:0;}100%{stroke-dashoffset:-100;}}
    .pick{opacity:0;animation:pick 6s steps(1) infinite;} @keyframes pick{0%{opacity:.85;}16.6%,100%{opacity:0;}}
    .cur{animation:cur 1s steps(1) infinite;} @keyframes cur{50%{opacity:0;}}
    .pop{transform-box:fill-box;transform-origin:center;animation:pop .6s cubic-bezier(.2,.7,.2,1) both;} @keyframes pop{from{transform:scale(0);}}
    .ping{transform-box:fill-box;transform-origin:center;animation:ping 2s cubic-bezier(0,0,.2,1) infinite;} @keyframes ping{75%,100%{transform:scale(2.6);opacity:0;}}
    .arrow{transition:none;}"""
        body = f"""
  {tile(t, 0, 0, CW, CH)}
  <g clip-path="url(#vc)">
    <rect x="{VX}" y="{VY}" width="{VW}" height="{VH}" fill="url(#vbg)"/>
    <rect x="{VX}" y="{VY}" width="{VW}" height="{VH}" fill="url(#dots)"/>
    <circle cx="{VX + VW}" cy="{VY}" r="130" fill="{t['a1']}" opacity="{t['aur_op'] * .5:.2f}" filter="url(#blur)"/>
    <circle cx="{VX}" cy="{VY + VH}" r="110" fill="{t['a3']}" opacity="{t['aur_op'] * .35:.2f}" filter="url(#blur)"/>
    <g transform="translate({VX} {VY})">{vis(t)}</g>
  </g>
  <rect x="{VX + .5}" y="{VY + .5}" width="{VW - 1}" height="{VH - 1}" rx="13.5" stroke="{t['hair']}" stroke-opacity="{t['hair_op']}"/>
  <text class="f-mono" x="28" y="234" font-size="12" letter-spacing="1.5" fill="{t['text3']}">{num}</text>
  <text class="f-sans" x="54" y="235" font-size="22" font-weight="600" letter-spacing="-.6" fill="{t['text']}">{esc(title)}</text>
  <g class="f-sans" font-size="14.5" fill="{t['text2']}">
    <text x="28" y="262">{esc(desc[0])}</text>
    <text x="28" y="282">{esc(desc[1])}</text>
  </g>
  {''.join(tags_svg)}
  <circle cx="{CW - 44}" cy="228" r="17" fill="{t['surface2']}" stroke="{t['hair']}" stroke-opacity="{t['hair_op'] * 1.6:.2f}"/>
  <path d="M{CW - 49} 233L{CW - 39} 223M{CW - 47} 223H{CW - 39}V231" stroke="{t['text']}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>"""
        return svg(t, CW, CH, body, title, f"Project {num}: {title}. {' '.join(desc)} Built with {', '.join(tags)}.", css, defs)
    return f


# ───────────────────────── footer ─────────────────────────
def footer(t):
    H = 340
    defs = f'<clipPath id="frame"><rect width="{W}" height="{H}" rx="28"/></clipPath>'
    css = """
    .breathe{transform-box:fill-box;transform-origin:center;animation:br 8s ease-in-out infinite;}
    @keyframes br{50%{transform:scale(1.15);opacity:.75;}}"""
    body = f"""
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="{t['bg']}"/>
    <rect width="{W}" height="{H}" fill="url(#dots)" opacity=".7"/>
    <g filter="url(#blur)" opacity="{t['aur_op']}">
      <ellipse class="breathe" cx="470" cy="{H + 40}" rx="260" ry="120" fill="{t['a1']}"/>
      <ellipse class="breathe" style="animation-delay:-3s" cx="730" cy="{H + 50}" rx="260" ry="120" fill="{t['a2']}"/>
      <ellipse class="breathe" style="animation-delay:-5s" cx="600" cy="{H + 70}" rx="200" ry="100" fill="{t['a3']}"/>
    </g>
    {eyebrow(t, W / 2, 84, "WHAT'S NEXT", "middle")}
    <text class="f-sans" x="{W / 2}" y="156" text-anchor="middle" font-size="58" font-weight="600" letter-spacing="-2.4" fill="url(#headg)">Let's build something</text>
    <text class="f-serif" x="{W / 2}" y="222" text-anchor="middle" font-size="72" fill="url(#aur)">remarkable.</text>
    <text class="f-sans" x="{W / 2}" y="270" text-anchor="middle" font-size="17" fill="{t['text2']}">Have an idea? I'm always up for building something useful.</text>
    <rect width="{W}" height="{H}" filter="url(#grain)" opacity=".9"/>
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="27.5" stroke="{t['hair']}" stroke-opacity="{t['hair_op'] * 1.3:.2f}"/>
  <path d="M60 .6H{W - 60}" stroke="url(#hi)"/>"""
    return svg(t, W, H, body, "Let's build something remarkable",
               "What's next: let's build something remarkable. Have an idea? I'm always up for building something useful.", css, defs)


# ───────────────────────── buttons ─────────────────────────
def button(label, primary):
    def f(t):
        H = 48
        tw = measure(label, 15, weight=550)
        w = 26 + tw + 12 + 14 + 22
        bg, fg = (t["invert_bg"], t["invert_fg"]) if primary else (t["surface2"], t["text"])
        ax = 26 + tw + 12
        body = f"""
  <rect x=".5" y=".5" width="{w - 1:.1f}" height="{H - 1}" rx="{(H - 1) / 2}" fill="{bg}" stroke="{t['hair']}" stroke-opacity="{0 if primary else t['hair_op'] * 1.8:.2f}"/>
  <path d="M{w * .2:.0f} .6H{w * .8:.0f}" stroke="url(#hi)"/>
  <text class="f-sans" x="26" y="29.5" font-size="15" font-weight="550" letter-spacing="-.2" fill="{fg}">{esc(label)}</text>
  <path d="M{ax:.1f} 29L{ax + 9:.1f} 20M{ax + 2:.1f} 20H{ax + 9:.1f}V27" stroke="{fg}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>"""
        return svg(t, round(w), H, body, label, f"Button: {label}")
    return f


if __name__ == "__main__":
    made = []
    made += both("hero", hero)
    for slug, num, label, plain, italic in SECTIONS:
        made += both(f"section-{slug}", section(num, label, plain, italic))
    made += both("about", bento)
    made += both("python", python_card)
    for slug, num, title, desc, tags, vis in PROJECTS:
        made += both(f"project-{slug}", project(num, title, desc, tags, vis))
    made += both("footer", footer)
    for slug, label, primary in [("work", "View my work", True), ("instagram", "Instagram", False),
                                 ("github", "Follow on GitHub", True), ("repos", "Browse all repositories", False)]:
        made += both(f"btn-{slug}", button(label, primary))
    print(f"built {len(made)} files")
