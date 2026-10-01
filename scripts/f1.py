"""Red Bull Racing edition: hero, section boards, driver card, garage, footer, buttons."""
import math

from car import CAR_CSS, CAR_DEFS, car
from kit import F1 as T, eyebrow, esc, measure, svg, tile

W = 1200
RED, YELLOW, BLUE, NAVY = T["red"], T["yellow"], T["blue"], T["navy"]


def race(x, y, text, size, weight=900, fill="#FFFFFF", anchor="start", skew=True, extra=""):
    """Titillium, leaned forward like the broadcast graphics."""
    t = (f'<text class="f-race" x="0" y="0" font-size="{size}" font-weight="{weight}" fill="{fill}" '
         f'text-anchor="{anchor}" {extra}>{esc(text)}</text>')
    return f'<g transform="translate({x} {y}){" skewX(-10)" if skew else ""}">{t}</g>'


def chevron(x, y, col, s=1.0):
    return f'<path d="M{x} {y - 5 * s}L{x + 5 * s} {y}L{x} {y + 5 * s}" stroke="{col}" stroke-width="{2 * s}" stroke-linecap="round" stroke-linejoin="round"/>'


def logo_at(redbull_logo, rb_w, cx, cy, width):
    return f'<g transform="translate({cx} {cy}) scale({width / rb_w:.4f})">{redbull_logo()}</g>'


STRIPES = f"""
    <pattern id="livery" width="46" height="46" patternUnits="userSpaceOnUse" patternTransform="rotate(-28)">
      <rect width="46" height="46" fill="none"/><rect width="8" height="46" fill="{RED}" opacity=".9"/><rect x="12" width="3" height="46" fill="{YELLOW}"/>
    </pattern>
    <pattern id="kerb" width="48" height="10" patternUnits="userSpaceOnUse">
      <rect width="24" height="10" fill="{RED}"/><rect x="24" width="24" height="10" fill="#F4F6FA"/>
    </pattern>
    <pattern id="cheq" width="16" height="16" patternUnits="userSpaceOnUse">
      <rect width="16" height="16" fill="#FFFFFF"/><rect width="8" height="8" fill="#0A0D16"/><rect x="8" y="8" width="8" height="8" fill="#0A0D16"/>
    </pattern>"""


# ───────────────────────── hero ─────────────────────────
def hero(redbull_logo, rb_w):
    H = 620
    cyc = 7.0
    on = [0.6 + i * 0.6 for i in range(5)]
    off = 3.9
    lights_css = "".join(
        f".l{i}{{animation:l{i} {cyc}s steps(1) infinite;}}"
        f"@keyframes l{i}{{0%{{opacity:0;}}{on[i] / cyc * 100:.1f}%{{opacity:1;}}{off / cyc * 100:.1f}%,100%{{opacity:0;}}}}"
        for i in range(5))
    pods = []
    gx, gy = 832, 44
    for i in range(5):
        px = gx + 26 + i * 62
        pods.append(f"""
    <rect x="{px - 22}" y="{gy + 10}" width="44" height="86" rx="10" fill="#05070F" stroke="#2A3352"/>
    <circle cx="{px}" cy="{gy + 32}" r="14" fill="#1A1F2E"/><circle cx="{px}" cy="{gy + 72}" r="14" fill="#1A1F2E"/>
    <g class="l{i}"><circle cx="{px}" cy="{gy + 32}" r="14" fill="#FF1E2D" filter="url(#glowR)"/><circle cx="{px}" cy="{gy + 72}" r="14" fill="#FF1E2D" filter="url(#glowR)"/></g>""")
    leds = []
    cols = ["#22C55E"] * 5 + ["#FF1E2D"] * 5 + ["#3B82F6"] * 5
    for i, c in enumerate(cols):
        leds.append(f'<rect x="{56 + i * 22}" y="410" width="16" height="10" rx="3" fill="#1A1F2E"/>'
                    f'<rect class="led" style="animation-delay:{i * .1:.1f}s" x="{56 + i * 22}" y="410" width="16" height="10" rx="3" fill="{c}"/>')
    speeds = [312, 327, 338, 346, 342, 335]
    spd = "".join(
        f'<g class="spd{" spd0" if k == 0 else ""}" style="animation-delay:{k * .5:.1f}s">{race(66, 482, str(v), 40, 900, "#FFFFFF", skew=False)}</g>'
        for k, v in enumerate(speeds))
    lines = "".join(
        f'<rect class="sl" style="animation-delay:{-k * .23:.2f}s" x="{420 + (k * 97) % 560}" y="{410 + (k * 37) % 120}" '
        f'width="{60 + (k * 53) % 120}" height="{1 + k % 2}" rx="1" fill="#FFFFFF" opacity=".5"/>'
        for k in range(14))
    defs = f"""{CAR_DEFS}{STRIPES}
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="28"/></clipPath>
    <linearGradient id="hbg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0B1433"/><stop offset=".6" stop-color="#060B1E"/><stop offset="1" stop-color="#03050E"/></linearGradient>
    <linearGradient id="road" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#0E1222"/><stop offset="1" stop-color="#05070F"/></linearGradient>
    <linearGradient id="fade" x1="0" x2="1"><stop stop-color="#fff" stop-opacity="0"/><stop offset=".25" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <mask id="liveryMask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
    <filter id="glowR" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>"""
    css = f"""{CAR_CSS}
    {lights_css}
    .lo{{animation:lo {cyc}s steps(1) infinite;}}
    @keyframes lo{{0%{{opacity:0;}}{off / cyc * 100:.1f}%{{opacity:1;}}95%,100%{{opacity:0;}}}}
    .led{{opacity:0;animation:led 2.6s steps(1) infinite;}}
    @keyframes led{{0%{{opacity:0;}}8%,70%{{opacity:1;}}75%,100%{{opacity:0;}}}}
    .spd{{opacity:0;animation:spd 3s steps(1) infinite;}}
    @keyframes spd{{0%{{opacity:1;}}16.6%,100%{{opacity:0;}}}}
    .sl{{animation:sl .9s linear infinite;}}
    @keyframes sl{{from{{transform:translateX(160px);opacity:0;}}30%{{opacity:.6;}}to{{transform:translateX(-520px);opacity:0;}}}}
    .kerb{{animation:kerb .35s linear infinite;}}
    @keyframes kerb{{to{{transform:translateX(-48px);}}}}
    .dash{{animation:dash .5s linear infinite;}}
    @keyframes dash{{to{{transform:translateX(-120px);}}}}
    .rise{{animation:rise 1s cubic-bezier(.2,.7,.2,1) both;}}
    .r2{{animation-delay:.12s;}} .r3{{animation-delay:.24s;}}
    @keyframes rise{{from{{opacity:0;transform:translateX(-24px);}}to{{opacity:1;transform:none;}}}}
    .ping{{transform-box:fill-box;transform-origin:center;animation:ping 2s cubic-bezier(0,0,.2,1) infinite;}}
    @keyframes ping{{75%,100%{{transform:scale(2.6);opacity:0;}}}}
    @media (prefers-reduced-motion: reduce){{.l0,.l1,.l2,.l3,.l4,.lo,.led{{opacity:0;}} .spd{{opacity:0;}} .spd0{{opacity:1;}}}}"""
    status_w = 30 + measure("ON TRACK  ·  OPEN TO BUILD", 12, "mono") + 16
    body = f"""
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#hbg)"/>
  <circle cx="900" cy="380" r="260" fill="{BLUE}" opacity=".22" filter="url(#blur)"/>
  <circle cx="260" cy="120" r="200" fill="{RED}" opacity=".12" filter="url(#blur)"/>
  <rect width="{W}" height="{H}" fill="url(#dots)"/>
  <g mask="url(#liveryMask)" opacity=".5"><rect x="600" y="-40" width="700" height="460" fill="url(#livery)"/></g>
  <text class="f-race" x="1150" y="400" text-anchor="end" font-size="330" font-weight="900" fill="none" stroke="#FFFFFF" stroke-opacity=".06" stroke-width="2" transform="skewX(-10)">18</text>

  <!-- start lights -->
  <rect x="{gx - 14}" y="{gy}" width="{5 * 62 + 16}" height="106" rx="14" fill="#0A0E1C" stroke="#2A3352"/>
  <rect x="{gx + 140}" y="0" width="22" height="{gy}" fill="#0A0E1C"/>
  {''.join(pods)}
  <g class="lo">{race(gx + 140, gy + 142, "LIGHTS OUT AND AWAY WE GO", 18, 700, YELLOW, "middle")}</g>

  <!-- badge row -->
  <g class="rise">
    {logo_at(redbull_logo, rb_w, 98, 66, 84)}
    {race(152, 72, "RACING EDITION", 17, 700, "#FFFFFF")}
    <path d="M300 54H346L340 80H294Z" fill="{RED}"/>
    {race(320, 73, "#18", 17, 900, "#FFFFFF", "middle")}
  </g>
  <g class="rise r2"><g transform="translate(56 112)">
    <rect width="{status_w:.0f}" height="30" rx="15" fill="#0E1838" stroke="#2A3A6B"/>
    <circle class="ping" cx="16" cy="15" r="4.5" fill="{T['green']}"/><circle cx="16" cy="15" r="4.5" fill="{T['green']}"/>
    <text class="f-mono" x="30" y="19.5" font-size="12" fill="#DDE4F5">ON TRACK  ·  OPEN TO BUILD</text>
  </g></g>

  <!-- name -->
  <g class="rise r2">
    {race(50, 262, "ISHAN", 124, 900, "#FFFFFF")}
    {race(50, 372, "KUMAR", 124, 900, RED)}
    <path d="M64 388H470" stroke="{YELLOW}" stroke-width="4"/>
  </g>

  <!-- telemetry -->
  <g class="rise r3">
    {''.join(leds)}
    <g transform="translate(56 432)">
      <rect width="150" height="66" rx="12" fill="#0B1330" stroke="#2A3A6B"/>
      {eyebrow(T, 12, 20, "SPEED")}
      <text class="f-mono" x="138" y="20" text-anchor="end" font-size="11" fill="{T['text3']}">KM/H</text>
    </g>
    {spd}
    <g transform="translate(216 432)">
      <rect width="86" height="66" rx="12" fill="#0B1330" stroke="#2A3A6B"/>
      {eyebrow(T, 12, 20, "GEAR")}
    </g>
    {race(232, 482, "8", 40, 900, YELLOW, skew=False)}
    <g transform="translate(312 432)">
      <rect width="120" height="66" rx="12" fill="#0B1330" stroke="#2A3A6B"/>
      {eyebrow(T, 12, 20, "DRS")}
    </g>
    {race(326, 482, "OPEN", 30, 900, T['green'], skew=False)}
    <text class="f-mono" x="58" y="528" font-size="12.5" letter-spacing="2" fill="{T['text2']}">DEVELOPER  ·  BUILDER  ·  PRODUCT THINKER</text>
  </g>

  <!-- speed lines + car -->
  {lines}
  {car(540, 392, 0.94, logo_at(redbull_logo, rb_w, 0, 0, 116))}

  <!-- track -->
  <rect y="544" width="{W}" height="{H - 544}" fill="url(#road)"/>
  <g class="kerb"><rect x="0" y="544" width="{W + 96}" height="9" fill="url(#kerb)"/></g>
  <g class="dash" opacity=".35">{''.join(f'<rect x="{k * 120}" y="586" width="60" height="4" rx="2" fill="#FFFFFF"/>' for k in range(12))}</g>
  <text class="f-mono" x="{W - 56}" y="{H - 16}" text-anchor="end" font-size="11" letter-spacing="2" fill="{T['text3']}">@ISHAN-ONE8  ·  SEASON 2026</text>
  <rect width="{W}" height="{H}" filter="url(#grain)" opacity=".8"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="27.5" stroke="#FFFFFF" stroke-opacity=".12"/>
"""
    return svg(T, W, H, body, "Ishan Kumar — Red Bull Racing edition",
               "A Red Bull Racing style F1 car, number 18, races across the banner while five start lights come on "
               "and go out: lights out and away we go. Ishan Kumar — developer, builder, product thinker. "
               "On track and open to build.", css, defs)


# ───────────────────────── section boards ─────────────────────────
SECTIONS = [
    ("about", "01", "THE DRIVER", "SECTOR 1  ·  ABOUT"),
    ("work", "02", "THE GARAGE", "SECTOR 2  ·  PROJECTS"),
    ("stack", "03", "POWER UNIT", "SECTOR 3  ·  TOOLKIT"),
    ("numbers", "04", "TELEMETRY", "LIVE  ·  FROM GITHUB"),
    ("activity", "05", "THE SEASON", "CONTRIBUTIONS  ·  STREAKS"),
]


def section(num, title, sub):
    H = 92
    tw = measure(title, 40, "race", weight=900) * 1.02
    body = f"""
  <defs>{STRIPES}<clipPath id="sc"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  <linearGradient id="sf" x1="0" x2="1"><stop stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>
  <mask id="sm"><rect width="{W}" height="{H}" fill="url(#sf)"/></mask></defs>
  <g clip-path="url(#sc)">
    <rect width="{W}" height="{H}" fill="#0A1230"/>
    <rect width="{W}" height="{H}" fill="url(#dots)"/>
    <g mask="url(#sm)" opacity=".55"><rect x="{W - 260}" width="260" height="{H}" fill="url(#cheq)" opacity=".18"/></g>
    <path d="M0 0H118L96 {H}H0Z" fill="{RED}"/>
    <path d="M118 0H128L106 {H}H96Z" fill="{YELLOW}"/>
    {race(50, 62, num, 44, 900, "#FFFFFF", "middle")}
    {race(150, 60, title, 40, 900, "#FFFFFF")}
    <text class="f-mono" x="{150 + tw + 28:.0f}" y="56" font-size="12" letter-spacing="2" fill="{T['text3']}">{esc(sub)}</text>
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="17.5" stroke="#FFFFFF" stroke-opacity=".1"/>"""
    return svg(T, W, H, body, f"{num} — {title.title()}", f"Section {num}: {title.title()} ({sub.title()})")


# ───────────────────────── driver card ─────────────────────────
def helmet(redbull_logo, rb_w):
    return f"""
  <g>
    <path d="M-120 40C-130 -60 -50 -130 40 -120C120 -112 150 -50 140 20L130 60C60 70 -60 72 -110 64C-120 58 -122 50 -120 40Z" fill="url(#helm)"/>
    <path d="M-118 12C-70 -14 -10 -24 22 -18L18 6C-30 8 -86 22 -120 38Z" fill="{RED}"/>
    <path d="M-116 34C-84 22 -40 12 18 10L16 22C-36 24 -80 34 -114 48Z" fill="{YELLOW}"/>
    <circle cx="-26" cy="-82" r="34" fill="{YELLOW}"/>
    <g transform="translate(-26 -66) scale({92 / rb_w:.4f})">{redbull_logo()}</g>
    <path d="M20 -42C70 -50 122 -38 140 -10L136 20C100 8 52 6 14 10C8 -8 10 -30 20 -42Z" fill="url(#visor)"/>
    <path d="M34 -34C70 -38 104 -30 124 -14" stroke="#FFFFFF" stroke-opacity=".45" stroke-width="3" stroke-linecap="round"/>
    <path d="M-110 64C-40 74 60 72 130 60L126 74C60 84 -40 86 -104 78Z" fill="#0A0D16"/>
    <path d="M-60 -104C-20 -126 40 -126 80 -100" stroke="#FFFFFF" stroke-opacity=".25" stroke-width="4" stroke-linecap="round"/>
    {race(-70, 56, "18", 30, 900, "#FFFFFF", "middle")}
  </g>"""


def driver(redbull_logo, rb_w):
    H = 470
    g = 16
    lw = 400
    rx = lw + g
    rw = W - rx
    rows = [
        ("DRIVER", "Ishan Kumar"),
        ("NUMBER", "18"),
        ("ROLE", "Developer · Builder · Product thinker"),
        ("SPECIALITY", "Python, web products & AI experiments"),
        ("RACE PLAN", "Learn  ›  Build  ›  Ship  ›  Improve"),
    ]
    rws = []
    for i, (k, v) in enumerate(rows):
        y = 102 + i * 50
        rws.append(f"""
  <g class="rise" style="animation-delay:{.1 * i:.1f}s">
    <text class="f-mono" x="{rx + 32}" y="{y}" font-size="11.5" letter-spacing="2" fill="{T['text3']}">{k}</text>
    <text class="f-race" x="{rx + 200}" y="{y + 1}" font-size="21" font-weight="600" fill="#FFFFFF">{esc(v)}</text>
    <path d="M{rx + 32} {y + 18}H{W - 32}" stroke="#FFFFFF" stroke-opacity=".07"/>
  </g>""")
    wave = "".join(
        f'<rect class="vu" style="animation-delay:{-k * .07:.2f}s" x="{rx + 210 + k * 6}" y="{H - 82}" width="3" height="26" rx="1.5" fill="{YELLOW}"/>'
        for k in range(26))
    defs = f"""{STRIPES}
    <linearGradient id="helm" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#2E4796"/><stop offset=".6" stop-color="{NAVY}"/><stop offset="1" stop-color="#101A3E"/></linearGradient>
    <linearGradient id="visor" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#1F2A44"/><stop offset=".5" stop-color="#0A0D16"/><stop offset="1" stop-color="#3B2A6B"/></linearGradient>"""
    css = """
    .rise{animation:rise .8s cubic-bezier(.2,.7,.2,1) both;}
    @keyframes rise{from{opacity:0;transform:translateX(-14px);}to{opacity:1;transform:none;}}
    .float{animation:float 5s ease-in-out infinite;} @keyframes float{50%{transform:translateY(-8px);}}
    .vu{transform-box:fill-box;transform-origin:center;animation:vu .9s ease-in-out infinite alternate;}
    @keyframes vu{from{transform:scaleY(.2);}to{transform:scaleY(1);}}
    .ping{transform-box:fill-box;transform-origin:center;animation:ping 2s cubic-bezier(0,0,.2,1) infinite;}
    @keyframes ping{75%,100%{transform:scale(2.6);opacity:0;}}"""
    body = f"""
  {tile(T, 0, 0, lw, H, glow=(lw / 2, 180, RED))}
  <g clip-path="url(#tc0_0)"><g opacity=".35"><rect x="-80" y="300" width="560" height="220" fill="url(#livery)"/></g></g>
  {eyebrow(T, 28, 44, "DRIVER  ·  #18")}
  <g class="float"><g transform="translate({lw / 2 + 4} 226)">{helmet(redbull_logo, rb_w)}</g></g>
  <ellipse cx="{lw / 2}" cy="350" rx="120" ry="10" fill="#000" opacity=".45" filter="url(#blurS)"/>
  {race(lw / 2, 410, "ISHAN KUMAR", 32, 900, "#FFFFFF", "middle")}
  <text class="f-mono" x="{lw / 2}" y="438" text-anchor="middle" font-size="11.5" letter-spacing="2" fill="{T['text3']}">SEASON 2026  ·  ON TRACK</text>

  {tile(T, rx, 0, rw, H, glow=(W, 0, BLUE))}
  {eyebrow(T, rx + 32, 44, "DRIVER PROFILE")}
  <g transform="translate({W - 32 - 210} 26)">
    <rect width="210" height="30" rx="15" fill="#0E1838" stroke="#2A3A6B"/>
    <circle class="ping" cx="16" cy="15" r="4.5" fill="{T['green']}"/><circle cx="16" cy="15" r="4.5" fill="{T['green']}"/>
    <text class="f-mono" x="30" y="19.5" font-size="11.5" fill="#DDE4F5">ON TRACK · OPEN TO BUILD</text>
  </g>
  {''.join(rws)}
  <g transform="translate({rx + 32} {H - 100})">
    <rect width="{rw - 64}" height="62" rx="14" fill="#0B1330" stroke="#2A3A6B"/>
    <path d="M0 14A14 14 0 0 1 14 0H120L104 62H14A14 14 0 0 1 0 48Z" fill="{RED}"/>
    {race(56, 38, "TEAM RADIO", 16, 900, "#FFFFFF", "middle")}
  </g>
  {wave}
  {race(rx + 380, H - 61, '"Box box, new idea incoming."', 21, 700, "#FFFFFF", extra='font-style="italic"', skew=False)}"""
    return svg(T, W, H, body, "The driver",
               "Driver profile. Driver: Ishan Kumar. Number 18. Role: developer, builder, product thinker. "
               "Speciality: Python, web products and AI experiments. Race plan: learn, build, ship, improve. "
               "Status: on track, open to build. Team radio: box box, new idea incoming.", css, defs)


# ───────────────────────── garage (projects as circuits) ─────────────────────────
def closed_curve(pts, s=1.0, ox=0, oy=0):
    pts = [(ox + x * s, oy + y * s) for x, y in pts]
    n = len(pts)
    d = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d + "Z", pts[0]


CIRCUITS = [
    [(20, 120), (40, 50), (110, 22), (150, 66), (205, 34), (262, 58), (250, 122), (170, 140), (100, 104)],
    [(26, 72), (78, 18), (176, 34), (250, 18), (262, 86), (204, 136), (124, 108), (58, 140)],
    [(18, 44), (140, 16), (262, 40), (236, 96), (154, 84), (124, 136), (36, 128)],
    [(40, 26), (226, 28), (262, 74), (196, 98), (250, 134), (60, 140), (16, 88)],
]

COMPOUND = {"Python": RED, "TypeScript": YELLOW}

PROJECTS = [
    ("interviewos", "P1", "InterviewOS", ["Adaptive AI technical interviews with a", "polished, real-time candidate experience."], ["TypeScript", "AI", "Web"]),
    ("cricket", "P2", "Cricket Score Analysis", ["Exploring cricket scores and match", "patterns through Python data analysis."], ["Python", "Data"]),
    ("hand-cricket", "P3", "Hand Cricket Game", ["The playground classic, rebuilt as an", "interactive terminal game."], ["Python", "CLI", "Game logic"]),
    ("marks", "P4", "Student Marks Analyser", ["Turning raw student marks into clear", "performance insights and grade spreads."], ["Python", "Analytics"]),
]


def project(i, slug, pos, title, desc, tags):
    CW, CH = 590, 350
    VX, VY, VW, VH = 12, 12, CW - 24, 196
    track, start = closed_curve(CIRCUITS[i], 1.12, VX + 28, VY + 18)
    dur = 6 + i
    chips, x = [], 28
    for s in tags:
        w = measure(s, 13.5, "race", weight=600) + 40
        col = COMPOUND.get(s, "#F4F6FA")
        chips.append(f'<rect x="{x:.1f}" y="306" width="{w:.1f}" height="28" rx="14" fill="#0E1838" stroke="#2A3A6B"/>'
                     f'<circle cx="{x + 15:.1f}" cy="320" r="7" fill="#0A0D16" stroke="{col}" stroke-width="2.5"/>'
                     f'<text class="f-race" x="{x + 28:.1f}" y="324.5" font-size="13.5" font-weight="600" fill="#E6EBF7">{esc(s)}</text>')
        x += w + 8
    sectors = "".join(
        f'<rect x="{VX + 360 + k * 62}" y="{VY + 120}" width="56" height="8" rx="4" fill="{c}"/>'
        f'<text class="f-mono" x="{VX + 360 + k * 62}" y="{VY + 146}" font-size="10.5" fill="{T["text3"]}">S{k + 1}</text>'
        for k, c in enumerate([T["purple"], T["green"], YELLOW]))
    defs = f"""<clipPath id="vc"><rect x="{VX}" y="{VY}" width="{VW}" height="{VH}" rx="14"/></clipPath>"""
    css = """
    .ping{transform-box:fill-box;transform-origin:center;animation:ping 2s cubic-bezier(0,0,.2,1) infinite;}
    @keyframes ping{75%,100%{transform:scale(2.6);opacity:0;}}"""
    body = f"""
  {tile(T, 0, 0, CW, CH)}
  <g clip-path="url(#vc)">
    <rect x="{VX}" y="{VY}" width="{VW}" height="{VH}" fill="#070D24"/>
    <rect x="{VX}" y="{VY}" width="{VW}" height="{VH}" fill="url(#dots)"/>
    <circle cx="{VX + 160}" cy="{VY + 100}" r="140" fill="{BLUE}" opacity=".25" filter="url(#blur)"/>
    <path d="{track}" stroke="#000" stroke-opacity=".5" stroke-width="16" stroke-linejoin="round"/>
    <path d="{track}" stroke="#2C3962" stroke-width="12" stroke-linejoin="round"/>
    <path d="{track}" stroke="#E6EBF7" stroke-width="3" stroke-linejoin="round"/>
    <path d="{track}" stroke="{T['purple']}" stroke-width="4" stroke-linecap="round" pathLength="100" stroke-dasharray="16 84">
      <animate attributeName="stroke-dashoffset" from="16" to="-84" dur="{dur}s" repeatCount="indefinite"/>
    </path>
    <rect x="{start[0] - 6:.1f}" y="{start[1] - 8:.1f}" width="12" height="16" fill="url(#cheq)" transform="rotate(-60 {start[0]:.1f} {start[1]:.1f})"/>
    <circle r="7" fill="{RED}" stroke="#FFFFFF" stroke-width="2"><animateMotion dur="{dur}s" repeatCount="indefinite" path="{track}"/></circle>
    {race(VX + 360, VY + 54, f"CIRCUIT {i + 1:02d}", 26, 900, "#FFFFFF")}
    <text class="f-mono" x="{VX + 360}" y="{VY + 80}" font-size="11" letter-spacing="1.8" fill="{T['text3']}">FASTEST LAP  ·  PURPLE</text>
    {sectors}
    <circle class="ping" cx="{VX + 366}" cy="{VY + 172}" r="4" fill="{T['green']}"/><circle cx="{VX + 366}" cy="{VY + 172}" r="4" fill="{T['green']}"/>
    <text class="f-mono" x="{VX + 378}" y="{VY + 176}" font-size="11" letter-spacing="1.8" fill="{T['green']}">GREEN FLAG</text>
  </g>
  <rect x="{VX + .5}" y="{VY + .5}" width="{VW - 1}" height="{VH - 1}" rx="13.5" stroke="#FFFFFF" stroke-opacity=".08"/>
  <path d="M28 226H84L76 256H20Z" fill="{RED}"/>
  {race(51, 250, pos, 22, 900, "#FFFFFF", "middle")}
  {race(98, 251, title, 26, 700, "#FFFFFF", skew=False)}
  <g class="f-race" font-size="16" fill="{T['text2']}"><text x="28" y="280">{esc(desc[0])}</text><text x="28" y="298">{esc(desc[1])}</text></g>
  {''.join(chips)}
  <path d="M{CW - 70} 226H{CW - 24}L{CW - 32} 256H{CW - 78}Z" fill="#0E1838" stroke="#2A3A6B"/>
  {chevron(CW - 54, 241, YELLOW, 1.1)}{chevron(CW - 46, 241, YELLOW, 1.1)}"""
    return svg(T, CW, CH, f"<defs>{STRIPES}</defs>" + body, f"{pos} — {title}",
               f"{pos}: {title}. {' '.join(desc)} Built with {', '.join(tags)}. Drawn as a race circuit with a car lapping it.", css, defs)


# ───────────────────────── footer ─────────────────────────
def footer(redbull_logo, rb_w):
    H = 380
    flag = []
    fx, fy, sq = 120, 92, 18
    for c in range(9):
        cells = "".join(
            f'<rect x="{fx + c * sq}" y="{fy + r * sq}" width="{sq}" height="{sq}" fill="{"#FFFFFF" if (r + c) % 2 else "#0A0D16"}"/>'
            for r in range(7))
        flag.append(f'<g class="wave" style="animation-delay:{-c * .12:.2f}s">{cells}</g>')
    defs = f"""{STRIPES}<clipPath id="frame"><rect width="{W}" height="{H}" rx="28"/></clipPath>"""
    css = """
    .wave{animation:wave 1.4s ease-in-out infinite;} @keyframes wave{50%{transform:translateY(10px);}}
    .flagg{transform-box:fill-box;transform-origin:left center;animation:sway 2.8s ease-in-out infinite;}
    @keyframes sway{50%{transform:rotate(-4deg);}}"""
    body = f"""
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="url(#hbgF)"/>
    <circle cx="{W - 200}" cy="{H}" r="260" fill="{RED}" opacity=".18" filter="url(#blur)"/>
    <circle cx="240" cy="{H}" r="220" fill="{BLUE}" opacity=".22" filter="url(#blur)"/>
    <rect width="{W}" height="{H}" fill="url(#dots)"/>
    <rect x="{fx - 8}" y="{fy - 16}" width="7" height="280" rx="3" fill="#C9D2EA"/>
    <g class="flagg">{''.join(flag)}</g>
    <text class="f-mono" x="460" y="112" font-size="12" letter-spacing="2.4" fill="{YELLOW}">CHEQUERED FLAG  ·  SEE YOU AT THE NEXT RACE</text>
    {race(456, 186, "LET'S BUILD SOMETHING", 54, 900, "#FFFFFF")}
    {race(456, 250, "REMARKABLE.", 64, 900, RED)}
    <text class="f-race" x="460" y="292" font-size="19" fill="{T['text2']}">Have an idea? I'm always up for building something useful.</text>
    {logo_at(redbull_logo, rb_w, W - 116, 76, 104)}
    <rect y="{H - 12}" width="{W}" height="12" fill="url(#kerb)"/>
    <rect width="{W}" height="{H}" filter="url(#grain)" opacity=".8"/>
  </g>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="27.5" stroke="#FFFFFF" stroke-opacity=".12"/>"""
    defs += """<linearGradient id="hbgF" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0B1433"/><stop offset="1" stop-color="#03050E"/></linearGradient>"""
    return svg(T, W, H, body, "Chequered flag",
               "A waving chequered flag. See you at the next race. Let's build something remarkable. "
               "Have an idea? I'm always up for building something useful.", css, defs)


# ───────────────────────── buttons ─────────────────────────
def button(label, primary):
    H = 48
    tw = measure(label, 16, "race", weight=700)
    w = 34 + tw + 18 + 18 + 22
    bg = RED if primary else "#0E1838"
    body = f"""
  <path d="M12 .5H{w - .5:.1f}L{w - 12.5:.1f} {H - .5}H.5Z" fill="{bg}" stroke="{'none' if primary else '#2A3A6B'}"/>
  <path d="M{w - 30:.1f} .5H{w - 22:.1f}L{w - 34:.1f} {H - .5}H{w - 42:.1f}Z" fill="{YELLOW if primary else RED}"/>
  {race(26, 30.5, label, 16, 700, "#FFFFFF", skew=False)}
  {chevron(30 + tw + 8, 25, "#FFFFFF", 1)}"""
    return svg(T, round(w), H, body, label, f"Button: {label}")
