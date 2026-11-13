import re,json
L=open('ifgc4.txt').read().split('\n')
want=[1,2,5,9,15,18,21,27,28,30,32,33,35,36]
out={}
def nums(s): return [x.replace(',','') for x in re.findall(r'\d[\d,]*(?:\.\d+)?|\d+-\d+/\d+|\d+/\d+|NA',s)]
for n in want:
    st=[i for i,l in enumerate(L) if f'TABLE 402.4({n})' in l][0]
    hdr=[L[st+k].strip() for k in range(1,7)]
    title=hdr[0]; gas=hdr[1].replace('Gas','').strip(); inlet=hdr[2].replace('Inlet Pressure','').strip(); drop=hdr[3].replace('Pressure Drop','').strip(); sg=hdr[4].replace('Specific Gravity','').strip()
    sizes=None; ids=None; rows={}; unit=None
    for l in L[st+6:st+90]:
        s=l.strip()
        if s.startswith('For SI') or s.startswith('Notes') or 'TABLE 402.4(' in s: 
            if rows: break
        if s.startswith('Nominal'):
            sizes=re.findall(r'\d+-\d+/\d+|\d+/\d+|\d+',s.replace('Nominal',''))
            continue
        if s.startswith('Actual ID') or s.startswith('Outside') or s.startswith('Inside') or s.startswith('SDR'):
            if s.startswith('Actual ID'): ids=s; 
            continue
        if 'Capacity in' in s: unit=s.split('Capacity in')[1].strip(); continue
        if sizes is None and re.match(r'^(\d+\s+){5,}\d+$',s):
            sizes=s.split(); continue
        m=re.match(r'^([\d,]+)\s+(.*)$',s)
        if m and sizes and unit:
            vals=[v.replace(',','') for v in re.findall(r'[\d,]+|NA',m.group(2))]
            if len(vals)>=len(sizes)-1:
                rows[int(m.group(1).replace(',',''))]=[None if v=='NA' else int(v) for v in vals[:len(sizes)]]
    out[n]={'title':title,'gas':gas,'inlet':inlet,'drop':drop,'sg':sg,'sizes':sizes,'unit':unit,'rows':rows}
    print(n,title[:30],gas,inlet,drop,'sizes',sizes,'unit',unit,'rows',len(rows), list(rows.items())[:1])
json.dump(out,open('gas_raw.json','w'))
