"""Shared design system for the profile's SVGs.

Every SVG is rendered twice (dark + light) from the same tokens, and carries
its own subset of the fonts it uses, so the typography looks identical on
every device without loading anything from the network.
"""
import base64
import io
import os
import re
from functools import lru_cache

from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(ROOT, "assets")
FONTS = {
    "sans": ("inter.woff2", "IK Sans", "normal", "300 800"),
    "serif": ("serif-italic.woff2", "IK Serif", "italic", "400"),
    "mono": ("mono.woff2", "IK Mono", "normal", "400 600"),
}

THEMES = {
    "dark": dict(
        bg="#08080A", bg2="#0F0F14", surface="#101014", surface2="#17171D",
        text="#FAFAFA", text2="#A1A1AA", text3="#71717A",
        hair="#FFFFFF", hair_op=0.08, hi_op=0.16,
        a1="#6366F1", a2="#A855F7", a3="#06B6D4", aur_op=0.42,
        accent="#A5B4FC", good="#34D399", grain=0.07,
        head1="#FFFFFF", head2="#9C9CA6", invert_bg="#FAFAFA", invert_fg="#09090B",
        dot_op=0.10,
    ),
    "light": dict(
        bg="#FFFFFF", bg2="#F5F5F8", surface="#FFFFFF", surface2="#F4F4F6",
        text="#09090B", text2="#52525B", text3="#8E8E98",
        hair="#000000", hair_op=0.09, hi_op=0.0,
        a1="#6366F1", a2="#A855F7", a3="#06B6D4", aur_op=0.20,
        accent="#4F46E5", good="#059669", grain=0.035,
        head1="#09090B", head2="#55555F", invert_bg="#09090B", invert_fg="#FAFAFA",
        dot_op=0.10,
    ),
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


@lru_cache(None)
def _font(key):
    return TTFont(os.path.join(HERE, "fonts", FONTS[key][0]))


def measure(text, size, font="sans", spacing=0.0, weight=400):
    """Width of `text` in px, from the font's own advance widths."""
    f = _font(font)
    cmap, hmtx, upm = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
    units = sum(hmtx[cmap.get(ord(c), cmap[ord("n")])][0] for c in text)
    w = units / upm * size + spacing * max(len(text) - 1, 0)
    if font == "sans" and weight > 400:
        w *= 1 + (weight - 400) / 400 * 0.06  # Inter widens a little as it gets bolder
    return w


def _subset(key, chars):
    font = TTFont(os.path.join(HERE, "fonts", FONTS[key][0]))
    opts = Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt", "ss01", "cv11"]
    opts.notdef_outline = True
    sub = Subsetter(opts)
    sub.populate(unicodes=[ord(c) for c in chars])
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def _font_css(doc):
    body = re.sub(r"<style>.*?</style>|<defs>.*?</defs>|<title.*?</title>|<desc.*?</desc>", "", doc, flags=re.S)
    chars = set("".join(re.findall(r">([^<]+)<", body))) | set(" .")
    chars = {c for c in chars if c not in "\n\r\t"}
    css = []
    for key, (_, family, style, weight) in FONTS.items():
        if f"f-{key}" in doc:
            css.append(
                f"@font-face{{font-family:'{family}';font-style:{style};font-weight:{weight};"
                f"src:url(data:font/woff2;base64,{_subset(key, chars)}) format('woff2');}}")
    return "".join(css)


BASE_CSS = """
.f-sans{font-family:'IK Sans',Inter,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;font-feature-settings:'ss01','cv11';}
.f-serif{font-family:'IK Serif','Instrument Serif',Georgia,serif;font-style:italic;}
.f-mono{font-family:'IK Mono','JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,monospace;}
@media (prefers-reduced-motion: reduce){*{animation:none!important;}}
"""


def common_defs(t, w, h):
    """Gradients and filters most graphics reuse."""
    return f"""
    <linearGradient id="surf" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{t['surface2']}"/><stop offset="1" stop-color="{t['surface']}"/></linearGradient>
    <linearGradient id="hi" x1="0" x2="1"><stop stop-color="#FFFFFF" stop-opacity="0"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity="{t['hi_op']}"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
    <linearGradient id="aur" x1="0" x2="1"><stop stop-color="{t['a1']}"/><stop offset=".5" stop-color="{t['a2']}"/><stop offset="1" stop-color="{t['a3']}"/></linearGradient>
    <linearGradient id="headg" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{t['head1']}"/><stop offset="1" stop-color="{t['head2']}"/></linearGradient>
    <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{t['text']}" fill-opacity="{t['dot_op']}"/></pattern>
    <filter id="blur" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="60"/></filter>
    <filter id="blurS" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="22"/></filter>
    <filter id="grain" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/>
      <feColorMatrix values="0 0 0 0 .5  0 0 0 0 .5  0 0 0 0 .5  0 0 0 {t['grain'] * 2.4:.3f} 0"/>
    </filter>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000" flood-opacity="{0.0 if t is THEMES['dark'] else 0.06}"/></filter>"""


def tile(t, x, y, w, h, r=22, glow=None):
    """A premium card: soft gradient body, hairline border, lit top edge."""
    g = ""
    if glow:
        cx, cy, col = glow
        g = f'<g clip-path="url(#tc{int(x)}_{int(y)})"><circle cx="{cx}" cy="{cy}" r="120" fill="{col}" opacity="{t["aur_op"] * .55:.2f}" filter="url(#blur)"/></g>'
    return f"""
  <clipPath id="tc{int(x)}_{int(y)}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath>
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#surf)"{'' if t is THEMES['dark'] else ' filter="url(#shadow)"'}/>
  {g}
  <rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="{r - .5}" fill="none" stroke="{t['hair']}" stroke-opacity="{t['hair_op']}"/>
  <path d="M{x + r} {y + .6}H{x + w - r}" stroke="url(#hi)"/>"""


def eyebrow(t, x, y, label, anchor="start"):
    return f'<text class="f-mono" x="{x}" y="{y}" font-size="11.5" letter-spacing="2" fill="{t["text3"]}" text-anchor="{anchor}">{esc(label)}</text>'


def svg(t, w, h, body, title, desc, css="", defs=""):
    doc = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d" fill="none">
  <title id="t">{esc(title)}</title>
  <desc id="d">{esc(desc)}</desc>
  <defs>{common_defs(t, w, h)}{defs}
  </defs>
  <style>/*FONTS*/{BASE_CSS}{css}</style>
{body}
</svg>
"""
    return doc.replace("/*FONTS*/", _font_css(doc))


def write(name, doc):
    os.makedirs(ASSETS, exist_ok=True)
    with open(os.path.join(ASSETS, name), "w", encoding="utf-8") as f:
        f.write(doc)
    return name


def both(name, fn):
    """Render `fn(theme)` as name-dark.svg and name-light.svg."""
    return [write(f"{name}-{k}.svg", fn(t)) for k, t in THEMES.items()]
