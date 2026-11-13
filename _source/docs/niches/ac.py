import sys,json,urllib.request,urllib.parse,concurrent.futures as cf
def q(args):
    s,hl,gl=args
    u="https://suggestqueries.google.com/complete/search?client=firefox&hl=%s&gl=%s&q=%s"%(hl,gl,urllib.parse.quote(s))
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=15).read()
        try: d=json.loads(r.decode('utf-8'))
        except: d=json.loads(r.decode('latin-1'))
        return s,d[1]
    except Exception as e: return s,['ERR '+str(e)]
if __name__=='__main__':
    hl,gl,out=sys.argv[1],sys.argv[2],sys.argv[3]
    seeds=[l.strip() for l in sys.stdin if l.strip()]
    jobs=[]
    for s in seeds:
        if s.endswith('*'):
            b=s[:-1].strip(); jobs.append((b+' ',hl,gl))
            jobs+= [(b+' '+c,hl,gl) for c in 'abcdefghijklmnopqrstuvwxyz']
        else: jobs.append((s,hl,gl))
    res={}
    with cf.ThreadPoolExecutor(16) as ex:
        for s,l in ex.map(q,jobs): res[s]=l
    json.dump(res,open(out,'w'),ensure_ascii=False,indent=1)
    allv=sorted({x for l in res.values() for x in l})
    print(len(allv)); print('\n'.join(allv))
