import json, CoolProp.CoolProp as CP
d=json.load(open('honeywell_tool.json'))
names={'R448A':'R448A.mix','R407F':'R407F.mix','R404A':'R404A','R507A':'R507A','R407C':'R407C','R422D':'R422D.mix'}
def TF(fl,psig,q):
    T=CP.PropsSI('T','P',(psig+14.6959)*6894.757,'Q',q,'HEOS::'+fl); return (T-273.15)*9/5+32
for k,fl in names.items():
    worst=[0,0]; n=0
    for P,(b,dw) in d[k].items():
        P=float(P)
        try:
            tb=TF(fl,P,0); td=TF(fl,P,1)
        except Exception as e: continue
        n+=1
        for i,(c,v) in enumerate(((tb,b),(td,dw))):
            if abs(c-v)>abs(worst[i]): worst[i]=round(c-v,2)
    print(k,n,'worst dT bubble/dew °F',worst)
