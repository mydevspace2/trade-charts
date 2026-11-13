import re,json
L=open('nec9.txt').read().split('\n')
sizes=['18','16','14','12','10','8','6','4','3','2','1','1/0','2/0','3/0','4/0','250','300','350','400','500','600','700','750','800','900','1000']
def t5(start,end,label):
    out={}
    cur=False
    for l in L[start:end]:
        if label in l: cur=True
        elif re.search(r'^\s+[A-Z]{2,}',l) and label not in l and re.search(r'[A-Z]{3,}.*\d',l) and not l.strip()[0].isdigit(): cur=False
        if not cur: continue
        m=re.search(r'\s(\d{1,4}|\d/0)\s+(\d+\.\d+)\s+(0\.\d{4}|1\.\d{4})',l)
        if m and m.group(1) in sizes: out.setdefault(m.group(1),float(m.group(3)))
    return out
thhn=t5(600,760,'THHN, THWN, THWN-2'); xhhw=t5(680,760,'XHHW')
print('THHN',thhn); print('XHHW',xhhw)
t8={}
for l in L[816:915]:
    m=re.match(r'^\s+(\d{1,4}|\d/0)\s+(\d+\.?\d*)\s+(\d+)\s+(\d+)\s+(.*)$',l)
    if not m: continue
    sz,mm2,cm,q,rest=m.groups()
    if sz not in sizes: continue
    nums=re.findall(r'\d+\.\d+|—',rest)
    if int(q)==1 and sz not in ('18','16','14','12','10','8'): pass
    t8.setdefault(sz,[]).append((int(cm),int(q),nums))
res={}
for sz,rows in t8.items():
    st=[r for r in rows if r[1]>1] or rows
    cm,q,n=st[0]
    # n: strand dia mm,in, overall mm,in, area mm2,in2, cu mm/km, cu kft, coated km, kft, al km, kft
    res[sz]={'cmil':cm,'cu_ohm_kft':float(n[7]) if len(n)>7 else None,'al_ohm_kft':float(n[11]) if len(n)>11 else None,'raw':n}
for k,v in res.items(): print(k,v['cmil'],v['cu_ohm_kft'],v['al_ohm_kft'],len(v['raw']))
json.dump({'thhn':thhn,'xhhw':xhhw,'t8':res},open('t5t8_raw.json','w'))
