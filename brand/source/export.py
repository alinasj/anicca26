"""Export the Anicca 26 logo as standalone files with real hex colors.

Run from anything; paths are relative to this file:
    python3 export.py

Writes SVGs to ../logo and the site's icons to ../../docs/assets/img.
PNGs are rendered afterwards by render_png.sh (headless Chrome).
Needs fontTools and Jost[wght].ttf next to this file (for outlined text).
"""
import math, os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "..", "logo")
SITE_IMG = os.path.join(HERE, "..", "..", "docs", "assets", "img")
os.makedirs(LOGO, exist_ok=True)
os.makedirs(SITE_IMG, exist_ok=True)

# ---- Palette ---------------------------------------------------------------
RACING = "#12492F"
GOLD = "#D4AF37"
WHITE = "#FFFFFF"
INK = "#13261F"
FADE = ["#9FB13A", "#F7A21B", "#E8661F"]            # leaf green, Marigold, Saffron
DOTS = ["#E8661F", "#D2552A", "#B8452A", "#963826"]  # Saffron falling to copper

# ---- oklab mixing (matches CSS color-mix(in oklab, ...)) -------------------
def _lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def _gam(c): return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
def hex2oklab(h):
    r, g, b = (_lin(int(h[i:i + 2], 16) / 255) for i in (1, 3, 5))
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)
def oklab2hex(L, a, b):
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    rgb = (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
           -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
           -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)
    return "#" + "".join(f"{round(max(0, min(1, _gam(max(0, c)))) * 255):02X}" for c in rgb)
def mix(a, b, t):
    A, B = hex2oklab(a), hex2oklab(b)
    return oklab2hex(*(x + (y - x) * t for x, y in zip(A, B)))

# ---- Mark geometry (same as the approved Draft 7) ----------------------------
C, R, A0, SPAN = 50, 34, 150, 250
def ss(x): x = max(0, min(1, x)); return x * x * (3 - 2 * x)
def pt(deg, r=R): a = math.radians(deg); return C + r * math.cos(a), C + r * math.sin(a)

def band(s0, s1, wf, steps):
    out, inn = [], []
    for i in range(steps + 1):
        s = s0 + (s1 - s0) * i / steps; w = wf(s); d = A0 + SPAN * s
        out.append(pt(d, R + w / 2)); inn.append(pt(d, R - w / 2))
    return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in out + inn[::-1]) + "Z"

def color_at(stops, s):
    if s <= stops[0][0]: return stops[0][1]
    for (sa, ca), (sb, cb) in zip(stops, stops[1:]):
        if s <= sb: return mix(ca, cb, (s - sa) / (sb - sa))
    return stops[-1][1]

def mark(line, mx=8.6, dots=True, small=False, fade=None, dot_colors=None):
    """SVG elements for the mark in a 100x100 box. `line` is the starting color."""
    fade = fade or FADE; DOTS_ = dot_colors or DOTS
    wf = lambda s: mx * ss(s / .32)
    stops = [(0.58, line), (0.72, fade[0]), (0.86, fade[1]), (1.0, fade[2])]
    start = stops[0][0]
    parts = [f'<path d="{band(0, start + 0.012, wf, 120)}" fill="{line}"/>']
    n = 60 if small else 110
    step = (1 - start) / n
    for i in range(n):
        s0 = start + i * step; s1 = min(1, s0 + step * 1.6)
        parts.append(f'<path d="{band(s0, s1, wf, 3)}" fill="{color_at(stops, s0 + step / 2)}"/>')
    # Rounded end: a half-disc that only extends past the end of the line (a full
    # circle would sit on top of the still-blending colors and show its outline).
    # It reaches back 0.6 degrees under the last segment so no seam shows.
    te = A0 + SPAN; r = wf(1) / 2; cx, cy = pt(te)
    back = [pt(te - 0.6, R - r), pt(te - 0.6, R + r)]
    half = [(cx + r * math.cos(math.radians(te + k)), cy + r * math.sin(math.radians(te + k))) for k in range(0, 181, 6)]
    cap = back + half
    parts.append('<path d="M' + " L".join(f"{x:.2f} {y:.2f}" for x, y in cap) + f'Z" fill="{fade[2]}"/>')
    if dots:
        end = A0 + SPAN
        if small:   # two bold dots stay visible at 16-32px
            spec = [(24, 5.0, DOTS_[1]), (44, 4.2, DOTS_[3])]
        else:
            spec = [(19.6, 3.6, DOTS_[0]), (37.0, 3.0, DOTS_[1]), (52.4, 2.4, DOTS_[2]), (65.9, 1.9, DOTS_[3])]
        for off, r, c in spec:
            x, y = pt(end + off)
            parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{c}"/>')
    return "".join(parts)

VB = (11, 11, 78, 78)   # tight crop around the circle

def svg(w, h, body, vb=None, title="Anicca 26"):
    vb = vb or f"0 0 {w} {h}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{vb}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n')

def write(path, text):
    with open(path, "w") as f: f.write(text)
    print("wrote", os.path.relpath(path, HERE))

# ---- Text as outlines (Jost Light) -------------------------------------------
font = TTFont(os.path.join(HERE, "Jost[wght].ttf"))
font = instantiateVariableFont(font, {"wght": 300})
glyphs = font.getGlyphSet(); cmap = font.getBestCmap()
UPM = font["head"].unitsPerEm
CAP = font["OS/2"].sCapHeight or 700

def text_path(txt, x, baseline, size, fill):
    """Return (svg <path>, advance width) for txt at the given size."""
    scale = size / UPM; pen = SVGPathPen(glyphs); cx = 0
    for ch in txt:
        g = cmap[ord(ch)]
        tp = TransformPen(pen, (scale, 0, 0, -scale, x + cx, baseline))
        glyphs[g].draw(tp)
        cx += glyphs[g].width * scale
    return f'<path d="{pen.getCommands()}" fill="{fill}"/>', cx

def wordmark(x, center_y, size, name_fill, stamp_fill):
    """"Anicca" + raised ’26, vertically centered on the cap height."""
    base = center_y + CAP / UPM * size / 2
    p1, w1 = text_path("Anicca", x, base, size, name_fill)
    ss_ = size * 0.4
    p2, w2 = text_path("’26", x + w1 + ss_ * 0.1, base - ss_ * 1.3, ss_, stamp_fill)
    return p1 + p2, w1 + ss_ * 0.1 + w2

def placed_mark(x, y, size, line, **kw):  # kw: mx, small, fade, dot_colors
    k = size / VB[2]
    return f'<g transform="translate({x:.2f} {y:.2f}) scale({k:.4f}) translate({-VB[0]} {-VB[1]})">{mark(line, **kw)}</g>'

def main():
    # ---- Exports -------------------------------------------------------------------
    VARIANTS = {
        # name: (line color of the mark, name color, stamp color)
        "on-dark": (WHITE, WHITE, GOLD),      # Racing Green, dark photos, dark mode
        "on-light": (RACING, INK, GOLD),      # white / light backgrounds
    }
    vb = " ".join(map(str, VB))
    for v, (line, name_c, stamp_c) in VARIANTS.items():
        write(os.path.join(LOGO, f"anicca26-mark-{v}.svg"), svg(512, 512, mark(line), vb))
        # horizontal lockup: mark 64, name 52, gap 10 (as on the board)
        mk = placed_mark(0, 0, 64, line)
        wm, ww = wordmark(74, 32, 52, name_c, stamp_c)
        W = math.ceil(74 + ww + 2)
        write(os.path.join(LOGO, f"anicca26-lockup-{v}.svg"), svg(W, 64, mk + wm))
        # stacked lockup: mark 88, gap 6, name 40
        wm_probe, ww2 = wordmark(0, 0, 40, name_c, stamp_c)
        W2 = math.ceil(max(88, ww2) + 8); cx = W2 / 2
        mk2 = placed_mark(cx - 44, 0, 88, line)
        wm2, _ = wordmark(cx - ww2 / 2, 88 + 6 + 20, 40, name_c, stamp_c)
        write(os.path.join(LOGO, f"anicca26-stacked-{v}.svg"), svg(W2, 88 + 6 + 40 + 4, mk2 + wm2))
    # light-background alternative with a deeper gold, for text-contrast purists
    wm, ww = wordmark(74, 32, 52, INK, "#8A6D12")
    write(os.path.join(LOGO, "anicca26-lockup-on-light-deepgold.svg"),
          svg(math.ceil(74 + ww + 2), 64, placed_mark(0, 0, 64, RACING) + wm))

    # App icon: Racing Green square, white mark at 62%
    def app_icon(size, radius=0, small=False):
        m = size * 0.62; o = (size - m) / 2
        bg = f'<rect width="{size}" height="{size}" rx="{radius}" fill="{RACING}"/>'
        return svg(size, size, bg + placed_mark(o, o, m, WHITE, mx=12 if small else 8.6, small=small))
    write(os.path.join(LOGO, "anicca26-app-icon.svg"), app_icon(1024))
    # Small favicon: thicker line, two bold dots
    write(os.path.join(LOGO, "anicca26-favicon.svg"), app_icon(64, radius=14, small=True))
    write(os.path.join(SITE_IMG, "favicon.svg"), app_icon(64, radius=14, small=True))
    for v in VARIANTS:
        for kind in ("mark", "lockup"):
            src = os.path.join(LOGO, f"anicca26-{kind}-{v}.svg")
            write(os.path.join(SITE_IMG, os.path.basename(src)), open(src).read())
    # Inline-ready full-size mark body (white line) for the animated hero
    write(os.path.join(HERE, "hero-mark-body.svgfrag"), mark(WHITE, dots=False))
    write(os.path.join(HERE, "hero-mark-body-light.svgfrag"), mark(RACING, dots=False))


if __name__ == "__main__":
    main()
