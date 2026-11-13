import re,json
L0=open('nec9.txt').read().split('\n')
L=[]
i=0
while i<len(L0):
    l=L0[i]
    if i+1<len(L0) and L0[i+1].strip().startswith('\u2215'):
        l=l+' '+L0[i+1].strip()[1:]; i+=1
    L.append(l); i+=1
arts_lines={}
metric={'12':'3/8','16':'1/2','21':'3/4','27':'1','35':'1-1/4','41':'1-1/2','53':'2','63':'2-1/2','78':'3','91':'3-1/2','103':'4','129':'5','155':'6'}
import sys
idx={n:[j for j,l in enumerate(L) if n in l][0] for n in ['Article 358','Article 362','Article 348','Article 342','(LFNC-A','(LFNC-B','(LFNC-C','Article 350','Article 344','Schedule 80','Schedule 40,','Type A,','Type EB','Table 5 Dimensions']}
arts0=[(91,'EMT'),(111,'ENT'),(134,'FMC'),(156,'IMC'),(197,'LFNC-A'),(216,'LFNC-B'),(249,'LFNC-C'),(278,'LFMC'),(304,'RMC'),(355,'PVC-80'),(392,'PVC-40'),(416,'PVC-A'),(465,'PVC-EB'),(498,'END')]
keys=['Article 358','Article 362','Article 348','Article 342','(LFNC-A','(LFNC-B','(LFNC-C','Article 350','Article 344','Schedule 80','Schedule 40,','Type A,','Type EB','Table 5 Dimensions']
names=['EMT','ENT','FMC','IMC','LFNC-A','LFNC-B','LFNC-C','LFMC','RMC','PVC-80','PVC-40','PVC-A','PVC-EB','END']
arts=[(idx[k],n) for k,n in zip(keys,names)]
t4={}
for (a,name),(b,_) in zip(arts,arts[1:]):
    rows={}
    for l in L[a:b]:
        m=re.match(r'^\s{5,}(\d{2,3})\s+(.*)$',l)
        if not m or m.group(1) not in metric: continue
        nums=re.findall(r'\d+\.\d+|\d+',m.group(2))
        # drop trade-size tokens: take floats with decimal only for in2 columns
        fl=[x for x in re.findall(r'\d+\.\d+',m.group(2))]
        if len(fl)<5: continue
        # floats: 40%in2, 60%in2, 53%in2, 31%in2, IDmm, IDin, [100%in2]
        vals=[float(x) for x in fl]
        rows[metric[m.group(1)]]=vals
    t4[name]=rows
for k,v in t4.items(): print(k,len(v),list(v.items())[:1])
json.dump(t4,open('t4_raw.json','w'))
