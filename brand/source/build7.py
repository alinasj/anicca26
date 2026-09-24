import json
m=json.load(open("mark7.json"))
syms="".join(f'<symbol id="b-{k}" viewBox="0 0 100 100">{v}</symbol>' for k,v in m["bodies"].items())
dots="".join(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" style="fill:{c}"/>' for x,y,r,c in m["dots"])
syms+=f'<symbol id="dots" viewBox="0 0 100 100">{dots}</symbol>'
adots="".join(f'<circle class="d d{i+1}" cx="{x:.2f}" cy="{y:.2f}" r="{r}" style="fill:{c}"/>' for i,(x,y,r,c) in enumerate(m["dots"]))
anim=f'''<svg class="anim" viewBox="11 11 78 78" role="img" aria-label="Anicca 26 logo: a line grows from a fine point into a circle, fades into color, then lets go into four dots from green to yellow">
<defs><mask id="reveal" maskUnits="userSpaceOnUse" x="0" y="0" width="100" height="100"><path class="draw" d="{m["arc"]}" pathLength="1" style="fill:none;stroke:#fff;stroke-width:16;stroke-linecap:butt"/></mask></defs>
<g mask="url(#reveal)"><use class="swb" href="#b-rg" width="100" height="100"/></g>{adots}</svg>'''
t=open("template7.html").read().replace("%%SYMBOLS%%",syms).replace("%%ANIM%%",anim)
open("anicca26-directions.html","w").write(t); print(len(t))
