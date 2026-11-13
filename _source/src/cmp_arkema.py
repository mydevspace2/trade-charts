import re, CoolProp.CoolProp as CP, json
def K(F): return (F-32)*5/9+273.15
def cp_psig(fl,F,q):
    return CP.PropsSI('P','T',K(F),'Q',q,'HEOS::'+fl)/6894.757-14.6959
lines=open('arkema2025.txt').read().split('\n')
data={}
# block 1: 454B L,V 513A L,V
cols1=[('R454B.mix',0),('R454B.mix',1),('R513A.mix',0),('R513A.mix',1)]
cols2=[('R22',0),('R32',0),('R134a',0),('R404A',0),('R407C',0),('R407C',1),('R410A',0),('R427A.mix',0),('R427A.mix',1),('R1233zd(E)',0),('R448A.mix',0),('R448A.mix',1),('R449A.mix',0),('R449A.mix',1),('R452A.mix',0),('R452A.mix',1)]
mode=1
for i,l in enumerate(lines):
    if 'R-22' in l and 'R-32' in l and 'Sat' in l and i>60: mode=2
    m=re.match(r'^\s*(-?\d+)\s+([\d. ]+)',l)
    if not m: continue
    nums=re.findall(r'-?\d+\.\d|-?\d+',l)
    try: F=int(nums[0])
    except: continue
    if mode==1:
        vals=[float(x) for x in nums[1:5]]
        if len(nums)<6: continue
        cols=cols1
    else:
        vals=[float(x) for x in nums[1:17]]
        if len(nums)<18: continue
        cols=cols2
    for (fl,q),v in zip(cols,vals):
        data.setdefault(f"{fl}|{q}",{})[F]=v
res={}
for key,d in data.items():
    fl,q=key.split('|'); q=int(q)
    worst=(0,None)
    n=0
    for F,v in sorted(d.items()):
        try: p=cp_psig(fl,F,q)
        except Exception as e: continue
        if p<0: c=-p*2.03602  # inHg vacuum
        else: c=p
        diff=c-v; n+=1
        tol=max(0.5,0.01*v)
        if abs(diff)>abs(worst[0]): worst=(round(diff,2),F,v,round(c,2))
    res[key]=(n,worst)
    print(key,n,'worst diff',worst)
json.dump({k:{str(a):b for a,b in v.items()} for k,v in data.items()},open('arkema2025.json','w'))
