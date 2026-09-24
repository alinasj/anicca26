import math, json
C=50; R=34; A0=150; SPAN=250; MX=8.6
def ss(x): x=max(0,min(1,x)); return x*x*(3-2*x)
wf=lambda s: MX*ss(s/.32)          # starts at 0 width: a pointed tip
def pt(deg,r=R): a=math.radians(deg); return (C+r*math.cos(a), C+r*math.sin(a))
def band(s0,s1,steps):
    out=[];inn=[]
    for i in range(steps+1):
        s=s0+(s1-s0)*i/steps; w=wf(s); deg=A0+SPAN*s
        out.append(pt(deg,R+w/2)); inn.append(pt(deg,R-w/2))
    return "M"+" L".join(f"{x:.2f} {y:.2f}" for x,y in out+inn[::-1])+"Z"
M1="var(--m1)"
def mix(a,b,t):
    p=round((1-t)*100,1)
    if p>=100: return a
    if p<=0: return b
    return f"color-mix(in oklab, {a} {p}%, {b})"
def color_at(stops,s):
    if s<=stops[0][0]: return stops[0][1]
    for (sa,ca),(sb,cb) in zip(stops,stops[1:]):
        if s<=sb: return mix(ca,cb,(s-sa)/(sb-sa))
    return stops[-1][1]
def body(stops):
    start=stops[0][0]
    parts=[f'<path d="{band(0,min(1,start+0.012),int(200*start))}" style="fill:{M1}"/>']
    n=110; step=(1-start)/n
    for i in range(n):
        s0=start+i*step; s1=min(1,s0+step*1.6)   # overlap hides seams
        parts.append(f'<path d="{band(s0,s1,3)}" style="fill:{color_at(stops,s0+step/2)}"/>')
    ex,ey=pt(A0+SPAN)
    parts.append(f'<circle cx="{ex:.2f}" cy="{ey:.2f}" r="{MX/2}" style="fill:{color_at(stops,1)}"/>')
    return "".join(parts)
G="#0f6e56"
options={"rg": [(0.58,M1),(0.72,"#8b5cf6"),(0.86,"#118ab2"),(1.0,"#3a9a6a")]}
_old={
 "leaf":    [(0.62,M1),(0.86,G),(1.0,"#1a9b7a")],
 "rainbow": [(0.58,M1),(0.72,"#8b5cf6"),(0.86,"#118ab2"),(1.0,"#1a9b7a")],
 "spectrum":[(0.50,M1),(0.62,"#ef476f"),(0.74,"#8b5cf6"),(0.87,"#118ab2"),(1.0,"#1a9b7a")],
 "woven":   [(0.66,M1),(0.73,"#1a9b7a"),(0.77,"#ffd166"),(0.84,M1),(1.0,M1)],
}
end=A0+SPAN
offs=[19.6,37.0,52.4,65.9]; radii=[3.6,3.0,2.4,1.9]; cols=["#3a9a6a","#7daa55","#afae45","#d4af37"]
dots=[(*pt(end+o),r,c) for o,r,c in zip(offs,radii,cols)]
a=pt(A0); b=pt(end+10)
arc=f"M{a[0]:.2f} {a[1]:.2f} A{R} {R} 0 1 1 {b[0]:.2f} {b[1]:.2f}"
res={"bodies":{k:body(v) for k,v in options.items()},"dots":dots,"arc":arc}
json.dump(res,open("mark7.json","w"))
print({k:len(v) for k,v in res["bodies"].items()})
