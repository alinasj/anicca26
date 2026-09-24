"""Build a comparison page of alternative color fades for the logo line."""
import os
from export import mark, placed_mark, wordmark, VB, RACING, WHITE, INK, GOLD

OPTIONS = [
    # key, title, description, fade, dots, stamp color, wide?
    ("combo1", "Combo 1 · Marigold line, Saffron dots", "The line warms from green into Marigold. The dots pick up in Saffron orange and deepen to copper.",
     ["#3A9A6A", "#B3B33A", "#F7A21B"], ["#F7A21B", "#E8661F", "#C9502A", "#9E3F26"], "#D4AF37", False),
    ("combo2", "Combo 2 · Marigold into Saffron", "The line passes through Marigold and ends in Saffron. The dots carry the orange down into copper.",
     ["#9FB13A", "#F7A21B", "#E8661F"], ["#E8661F", "#D2552A", "#B8452A", "#963826"], "#D4AF37", False),
    ("marigold", "Marigold · #F7A21B", "Orange-yellow, like the flower. Warm and bright.",
     ["#3A9A6A", "#B3B33A", "#F7A21B"], ["#F7A21B", "#E8832A", "#CF6A2A", "#A84B26"], "#D4AF37", False),
    ("saffron", "Saffron · #E8661F", "True orange, like a leaf in late autumn. The boldest.",
     ["#3A9A6A", "#B79A33", "#E8661F"], ["#E8661F", "#D2552A", "#B8452A", "#963826"], "#D4AF37", False),
]

def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Anicca 26 logo">{body}</svg>'

def lockup(line, name_c, fade, dots, stamp=GOLD):
    mk = placed_mark(0, 0, 64, line, fade=fade, dot_colors=dots)
    wm, ww = wordmark(74, 32, 52, name_c, stamp)
    return svg(int(74 + ww + 2), 64, mk + wm)

cards = []
for key, title, desc, fade, dots, stamp, wide in OPTIONS:
    vb = " ".join(map(str, VB))
    big_light = f'<svg viewBox="{vb}" role="img" aria-label="{title} logo on white">{mark(RACING, fade=fade, dot_colors=dots)}</svg>'
    big_dark = f'<svg viewBox="{vb}" role="img" aria-label="{title} logo on green">{mark(WHITE, fade=fade, dot_colors=dots)}</svg>'
    sw = "".join(f'<i style="background:{c}"><span>{c}</span></i>' for c in fade[1:] + dots[1:])
    cards.append(f'''
<article class="opt{' wide' if wide else ''}">
  <div class="stages"><div class="st light">{big_light}</div><div class="st green">{big_dark}</div></div>
  <div class="lk light">{lockup(RACING, INK, fade, dots, stamp)}</div>
  <div class="lk green">{lockup(WHITE, WHITE, fade, dots, stamp)}</div>
  <h3>{title}</h3><p>{desc}</p>
  <div class="bar">{sw}</div>
</article>''')

html = open(os.path.join(os.path.dirname(__file__), "hue_options_template.html")).read().replace("%%CARDS%%", "".join(cards))
out = os.environ.get("OUT", "hue-options.html")
open(out, "w").write(html)
print("wrote", out, len(html))
