import json, CoolProp.CoolProp as CP
def K(F): return (F-32)*5/9+273.15
def cp(fl,F,q): return CP.PropsSI('P','T',K(F),'Q',q,'HEOS::'+fl)/6894.757-14.6959
d=json.load(open('arkema2025.json'))
for key,vals in d.items():
    fl,q=key.split('|');q=int(q)
    rows=[]
    for F,v in vals.items():
        F=int(F)
        try:p=cp(fl,F,q)
        except: continue
        if p<2: continue
        rows.append((F,v,round(p,2),round(p-v,2),round(100*(p-v)/v,2)))
    w=max(rows,key=lambda r:abs(r[4]))
    wa=max(rows,key=lambda r:abs(r[3]))
    print(f"{key:16s} n={len(rows)} worst% {w}  worstabs {wa}")
