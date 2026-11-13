import re,json
L=open('honeywell_tool.txt').read().split('\n')
num=re.compile(r'-?\d+\.\d')
out={'R448A':{},'R407F':{},'R404A':{},'R507A':{},'R450A':{},'R407C':{},'R422D':{}}
for l in L:
    left=l[:200]; nums=[float(x) for x in num.findall(left)]
    if len(nums)>=18 and l[:30].strip():
        P=nums[0]
        out['R448A'][P]=nums[2:4]; out['R407F'][P]=nums[5:7]; out['R404A'][P]=nums[9:11]; out['R507A'][P]=[nums[11]]*2
        if len(nums)>=23:
            P2=nums[18]; out['R450A'][P2]=nums[20:22]
    right=l[130:]
    rn=[float(x) for x in num.findall(right)]
    if len(rn)>=8 and len(l)>130 and not l[:120].strip() or (len(rn)>=8 and len(nums)<18):
        P=rn[0]; out['R407C'][P]=rn[2:4]; out['R422D'][P]=rn[5:7]
for k,v in out.items(): print(k,len(v),list(v.items())[:2], list(v.items())[-2:])
json.dump({k:{str(p):t for p,t in v.items()} for k,v in out.items()},open('honeywell_tool.json','w'))
