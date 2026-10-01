"""The F1 car: a side-on Red Bull Racing-style car, drawn facing right.

`car(ox, oy, s)` returns SVG for the car with its rear-wheel ground contact
near (ox + 100*s, oy + 151*s). Wheels spin; the body sits on a light
suspension wobble so it reads as moving at speed.
"""

NAVY = "#1B2A5C"
NAVY_DK = "#121D42"
NAVY_LT = "#24387A"
CARBON = "#0A0D16"
RED = "#DB0A40"
YELLOW = "#FFCC00"

BODY = ("M58 96L64 72C140 58 220 40 286 30L300 28C312 28 318 34 320 44L326 60L392 64"
        "C450 70 540 92 604 108C613 111 613 117 602 118L420 118C400 122 380 128 360 130"
        "L120 130C90 128 70 118 58 96Z")
SIDEPOD = "M206 86C262 76 340 74 394 82L398 110C340 122 262 126 204 122C198 110 198 96 206 86Z"
ENGINE_SPINE = "M70 74C150 60 230 44 300 30L304 40C236 54 160 70 76 90Z"
NOSE_TIP = "M560 99C580 104 596 107 604 108C613 111 613 117 602 118L560 118Z"


def wheel(cx, cy, r, compound, spin_cls):
    spokes = "".join(
        f'<path d="M{cx} {cy}L{cx + (r * .62) * __import__("math").cos(a * 0.5236):.2f} '
        f'{cy + (r * .62) * __import__("math").sin(a * 0.5236):.2f}" stroke="#3A4256" stroke-width="2.4"/>'
        for a in range(0, 12, 2))
    return f"""
  <g>
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="#0B0B0F"/>
    <circle cx="{cx}" cy="{cy}" r="{r - 1.5}" stroke="#1C1E26" stroke-width="3"/>
    <circle cx="{cx}" cy="{cy}" r="{r * .80:.1f}" stroke="{compound}" stroke-width="2.6"/>
    <g class="{spin_cls}">
      <circle cx="{cx}" cy="{cy}" r="{r * .80:.1f}" stroke="#FFFFFF" stroke-opacity=".55" stroke-width="2.6" stroke-dasharray="6 40"/>
      <circle cx="{cx}" cy="{cy}" r="{r * .66:.1f}" fill="#16181F"/>
      {spokes}
      <circle cx="{cx}" cy="{cy}" r="{r * .66:.1f}" stroke="#545C72" stroke-width="1.2" stroke-dasharray="3 7"/>
    </g>
    <circle cx="{cx}" cy="{cy}" r="{r * .2:.1f}" fill="{YELLOW}"/>
    <circle cx="{cx}" cy="{cy}" r="{r * .08:.1f}" fill="#0B0B0F"/>
  </g>"""


def car(ox, oy, s=1.0, logo=""):
    """Car group. `logo` is SVG for the sidepod mark, drawn centred on (0, 0) and ~110px wide."""
    return f"""
<g transform="translate({ox} {oy}) scale({s})">
  <ellipse cx="320" cy="152" rx="320" ry="10" fill="#000" opacity=".55" filter="url(#carShadow)"/>
  <g class="chassis">
    <!-- rear wing -->
    <path d="M30 86L48 86L56 128L36 128Z" fill="{CARBON}"/>
    <path d="M6 16H64L68 30L64 94L40 100L12 94Z" fill="{NAVY_DK}"/>
    <path d="M6 16H64L66 23H8Z" fill="{RED}"/>
    <path d="M10 34H64M12 44H63" stroke="{NAVY_LT}" stroke-width="2"/>
    <text class="f-race" x="35" y="74" text-anchor="middle" font-size="12" font-weight="900" fill="#FFFFFF" font-style="italic">IK</text>
    <!-- floor & diffuser -->
    <path d="M44 130L584 130L600 140L40 142Z" fill="{CARBON}"/>
    <path d="M44 130H584" stroke="{YELLOW}" stroke-opacity=".7" stroke-width="1.2"/>
    <!-- body -->
    <path d="{BODY}" fill="url(#bodyG)"/>
    <path d="{ENGINE_SPINE}" fill="{NAVY_DK}" opacity=".7"/>
    <path d="{SIDEPOD}" fill="url(#podG)"/>
    <path d="M394 82L406 84L408 108L398 110Z" fill="{CARBON}"/>
    <path d="M204 122C262 126 340 122 398 110" stroke="{RED}" stroke-width="5"/>
    <path d="M410 104C470 106 530 110 600 116" stroke="{RED}" stroke-width="4"/>
    <path d="{NOSE_TIP}" fill="{YELLOW}"/>
    <path d="M300 28C312 28 318 34 320 44L310 46C306 38 302 34 296 32Z" fill="{CARBON}"/>
    <!-- livery -->
    <g transform="translate(300 100)">{logo}</g>
    <text class="f-race" x="446" y="98" text-anchor="middle" font-size="22" font-weight="900" fill="#FFFFFF" font-style="italic" transform="rotate(7 446 98)">18</text>
    <text class="f-race" x="190" y="66" font-size="11" font-weight="700" letter-spacing="1.5" fill="{YELLOW}" transform="rotate(-9 190 66)">ISHAN</text>
    <!-- cockpit, driver, halo -->
    <path d="M326 60L392 64L388 70L330 68Z" fill="{CARBON}"/>
    <g transform="translate(352 56)">
      <path d="M-14 6C-15 -6 -6 -14 4 -13C13 -12 17 -5 16 4L12 9H-12Z" fill="{NAVY}"/>
      <path d="M-14 1C-12 -8 -4 -12 4 -12C10 -11 14 -8 15 -3Z" fill="{RED}"/>
      <path d="M2 -6H15L16 2H4Z" fill="#0A0D16"/>
      <circle cx="-4" cy="-9" r="3" fill="{YELLOW}"/>
    </g>
    <path d="M330 48C346 36 374 40 398 64" stroke="#2A2F3D" stroke-width="5" stroke-linecap="round"/>
    <path d="M404 62L408 52H420" stroke="#2A2F3D" stroke-width="2.4"/>
    <!-- front wing -->
    <path d="M540 126L632 122L640 138L548 142Z" fill="{CARBON}"/>
    <path d="M552 129L630 126M556 135L634 132" stroke="{RED}" stroke-width="1.6"/>
    <path d="M612 102H638V142H616Z" fill="{NAVY_DK}"/>
    <path d="M612 102H638V108H613Z" fill="{RED}"/>
  </g>
  {wheel(100, 110, 41, RED, "spin")}
  {wheel(512, 110, 41, RED, "spin")}
</g>"""


CAR_DEFS = f"""
    <linearGradient id="bodyG" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{NAVY_LT}"/><stop offset=".55" stop-color="{NAVY}"/><stop offset="1" stop-color="{NAVY_DK}"/></linearGradient>
    <linearGradient id="podG" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#2A4290"/><stop offset="1" stop-color="{NAVY}"/></linearGradient>
    <filter id="carShadow" x="-10%" y="-200%" width="120%" height="500%"><feGaussianBlur stdDeviation="6"/></filter>"""

CAR_CSS = """
    .spin{transform-box:fill-box;transform-origin:center;animation:wspin .35s linear infinite;}
    @keyframes wspin{to{transform:rotate(360deg);}}
    .chassis{animation:rumble .18s steps(2) infinite;}
    @keyframes rumble{50%{transform:translateY(.8px);}}"""
