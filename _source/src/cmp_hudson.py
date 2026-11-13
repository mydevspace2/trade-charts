import re,subprocess,json,glob,os, CoolProp.CoolProp as CP
os.chdir(os.path.dirname(os.path.abspath(__file__))+'/hudson')
cpn={'12':'R12','123':'R123','1233ZD':'R1233zd(E)','1234yf':'R1234yf','1234ze':'R1234ze(E)','507':'R507A','744':'CO2','22':'R22','134a':'R134a','32':'R32','410A':'R410A','404A':'R404A','407C':'R407C'}
def fl(r): return cpn.get(r, f'R{r}.mix')
def TF(f,psig,q): return (CP.PropsSI('T','P',(psig+14.6959)*6894.757,'Q',q,'HEOS::'+f)-273.15)*1.8+32
def PP(f,F,q): return CP.PropsSI('P','T',(F-32)/1.8+273.15,'Q',q,'HEOS::'+f)/6894.757-14.6959
allpts={}
for pdf in sorted(glob.glob('R-*.pdf')):
    r=pdf[2:-4]; txt=subprocess.run(['pdftotext','-layout',pdf,'-'],capture_output=True,text=True).stdout
    two='Liquid' in txt
    pts=[]
    for l in txt.split('\n'):
        n=re.findall(r'-?\d+(?:\.\d+)?',l)
        k=4 if len(n) in (4,8) else 3
        if len(n) in (3,4,6,8) and re.match(r'^\s*-?\d',l):
            for g in range(0,len(n)-k+1,k):
                grp=n[g:g+k]
                try:
                    F=float(grp[0]);C=float(grp[1])
                except: continue
                if abs((F-32)/1.8-C)>0.15: continue
                vals=[float(x) for x in grp[2:]]
                pts.append((F,vals))
    f=fl(r); worst=0; n=0; detail=None
    for F,vals in pts:
        qs=[0,1] if len(vals)==2 else [0]
        for q,v in zip(qs,vals):
            allpts.setdefault(r,[]).append([F,q,v])
            try: p=PP(f,F,q)
            except: continue
            if p<3 or v<3: continue
            try: t=TF(f,v,q)
            except: continue
            d=t-F; n+=1
            if abs(d)>abs(worst): worst=d; detail=(F,q,v,round(p,2))
    print(f"R-{r:7s} {f:12s} two={two} pts={len(pts)} cmp={n} worst dT={worst:+.2f}F at {detail}")
json.dump(allpts,open('../hudson_points.json','w'))
