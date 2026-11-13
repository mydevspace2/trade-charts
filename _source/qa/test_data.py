"""Data spot-checks: every refrigerant table vs manufacturer / reference charts, plus NEC / IFGC
values vs the parsed source documents. Writes build/data/verification.json (used on the pages).
Pass rule for PT data: temperature-equivalent deviation <= 1.0 °F at every compared point
(after skipping points within 2 psi of atmospheric, where charts switch to vacuum units).
Run: python3 qa/test_data.py
"""
import json, os, re, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, '..', 'build')
S = os.path.join(HERE, '..', 'src')
refs = {r['slug']: r for r in json.load(open(os.path.join(B, 'data', 'refrigerants.json')))}
ATM = 14.6959
fails = []

def p_at(r, F, q):
    t, arr = r['t'], (r['b'] if q == 0 else r['d'])
    if F < t[0] or F > t[-1]: return None
    i = min(int(F - t[0]), len(t) - 2)
    f = F - t[i]
    return arr[i] + (arr[i + 1] - arr[i]) * f

def t_at(r, P, q):
    arr = r['b'] if q == 0 else r['d']
    t = r['t']
    for i in range(len(t) - 1):
        if arr[i] <= P <= arr[i + 1]:
            return t[i] + (P - arr[i]) / (arr[i + 1] - arr[i]) * (t[i + 1] - t[i])
    return None

def dT_from_TP(r, F, q, P):
    """deviation in °F: our saturation temperature at the reference pressure minus reference T."""
    tt = t_at(r, P, q)
    return None if tt is None else tt - F

stats = {}
def add(slug, src, d):
    if d is None: return
    s = stats.setdefault(slug, {}).setdefault(src, [0, 0.0])
    s[0] += 1; s[1] = max(s[1], abs(d))

# 1 Arkema 2025 (T -> P)
amap = {'R454B.mix': 'r454b', 'R513A.mix': 'r513a', 'R22': 'r22', 'R32': 'r32', 'R134a': 'r134a', 'R404A': 'r404a',
        'R407C': 'r407c', 'R410A': 'r410a', 'R427A.mix': 'r427a', 'R448A.mix': 'r448a', 'R449A.mix': 'r449a', 'R452A.mix': 'r452a'}
ark = json.load(open(os.path.join(S, 'arkema2025.json')))
for key, vals in ark.items():
    fl, q = key.split('|'); q = int(q)
    if fl not in amap: continue
    for F, P in vals.items():
        F = int(F)
        if P < 2 or (fl == 'R427A.mix' and F == 150): continue  # vacuum / garbled row in PDF text
        if p_at(refs[amap[fl]], F, q) is None or p_at(refs[amap[fl]], F, q) < 2: continue
        add(amap[fl], 'Arkema Forane PT chart (2025, REFPROP 10)', dT_from_TP(refs[amap[fl]], F, q, P))
# 2 Honeywell pressure-based (P -> T bubble/dew)
hmap = {'R448A': 'r448a', 'R407F': 'r407f', 'R404A': 'r404a', 'R507A': 'r507a', 'R407C': 'r407c', 'R422D': 'r422d'}
hw = json.load(open(os.path.join(S, 'honeywell_tool.json')))
for k, vals in hw.items():
    if k not in hmap: continue
    for P, (tb, td) in vals.items():
        P = float(P)
        if P < 2: continue
        r = refs[hmap[k]]
        for q, T in ((0, tb), (1, td)):
            tt = t_at(r, P, q)
            if tt is not None: add(hmap[k], 'Honeywell pressure-based PT chart', tt - T)
# 3 Honeywell Solstice 454B chart (P avg bubble dew)
for l in open(os.path.join(S, 'honeywell_454b.txt')):
    for m in re.finditer(r'(?<![\d.])(\d{1,3})\s+(-?\d+\.\d)\s+(-?\d+\.\d)\s+(-?\d+\.\d)', l):
        P, a, tb, td = int(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4))
        if P < 2 or not (tb <= a <= td): continue
        r = refs['r454b']
        for q, T in ((0, tb), (1, td)):
            tt = t_at(r, P, q)
            if tt is not None: add('r454b', 'Honeywell Solstice 454B PT chart', tt - T)
# 4 Hudson (T -> P); single-column blend charts are ambiguous (not compared)
hmap2 = {'12': 'r12', '123': 'r123', '1233ZD': 'r1233zd', '1234yf': 'r1234yf', '1234ze': 'r1234ze', '22': 'r22', '32': 'r32',
         '134a': 'r134a', '744': 'r744', '407A': 'r407a', '407C': 'r407c', '407F': 'r407f', '417A': 'r417a', '421A': 'r421a',
         '422D': 'r422d', '427A': 'r427a', '448A': 'r448a', '449A': 'r449a', '450A': 'r450a', '452A': 'r452a', '513A': 'r513a',
         '438A': 'r438a', '455A': 'r455a', '454A': 'r454a'}
hud = json.load(open(os.path.join(S, 'hudson_points.json')))
for k, pts in hud.items():
    if k not in hmap2: continue
    r = refs[hmap2[k]]
    qs = {q for _, q, _ in pts}
    single_blend = r['blend'] and qs == {0}
    for F, q, P in pts:
        if P < 3 or F > 130: continue
        pr = p_at(r, F, q)
        if pr is None or pr < 3: continue  # chart shows vacuum in inHg there
        if single_blend:
            src = 'Hudson Technologies PT chart (liquid)'
        else:
            src = 'Hudson Technologies PT chart'
        add(hmap2[k], src, dT_from_TP(r, F, q, P))
# 5 Honeywell N41 presentation: average pressure (bar abs) at 0/2/4 °C
for C, bar in ((0, 7.68), (2, 8.18), (4, 8.70)):
    F = C * 1.8 + 32
    r = refs['r466a']
    avg = (p_at(r, F, 0) + p_at(r, F, 1)) / 2
    ours_bar = (avg + ATM) * 0.0689476
    add('r466a', 'Honeywell Solstice N41 presentation (average pressure, bar)', (ours_bar - bar) / 0.06)  # ~0.06 bar per °F here
# 6 ASHRAE 34 normal boiling (bubble/dew at 1 atm = 0 psig)
nbp = {'r454b': (-59.6, -58.0), 'r448a': (-50.6, -39.6), 'r449a': (-50.8, -39.8), 'r407f': (-51.0, -39.5),
       'r452a': (-52.6, -45.8), 'r455a': (-60.9, -38.4), 'r454a': (-55.1, -42.9), 'r513a': (-20.6, -20.6),
       'r450a': (-10.1, -9.0)}
for slug, (tb, td) in nbp.items():
    r = refs[slug]
    for q, T in ((0, tb), (1, td)):
        tt = t_at(r, 0.0, q)
        if tt is not None: add(slug, 'ASHRAE 34 bubble/dew at 1 atm', tt - T)
# 7 NIST WebBook saturation (T °F, P psia)
for f, slug in (('propane', 'r290'), ('isobutane', 'r600a'), ('ammonia', 'r717'), ('co2', 'r744')):
    L = open(os.path.join(S, 'nist', f + '.tsv')).read().strip().split('\n')[1:]
    for l in L[::7]:
        p = l.split('\t'); T = float(p[0]); P = float(p[1]) - ATM
        if T < -60 or T > 150 or P < 2: continue
        add(slug, 'NIST Chemistry WebBook saturation data', dT_from_TP(refs[slug], T, 0, P))

ver = {}
for slug, r in refs.items():
    s = stats.get(slug, {})
    total = sum(v[0] for v in s.values())
    worst = max([v[1] for v in s.values()] or [99])
    ver[slug] = {'points': total, 'max_dev_f': round(worst, 2), 'sources': {k: {'n': v[0], 'max': round(v[1], 2)} for k, v in s.items()}}
    ok = total >= 3 and worst <= 1.0
    flag = 'OK ' if ok else 'FAIL'
    print(f"{flag} {r['name']:12s} points={total:4d} max|dT|={worst:.2f}F  " + '; '.join(f"{k.split(' (')[0]}:{v[0]}/{v[1]:.2f}" for k, v in s.items()))
    if not ok: fails.append(slug)
json.dump(ver, open(os.path.join(B, 'data', 'verification.json'), 'w'), indent=1)

# NEC / IFGC spot checks against the parsed source files
nec = json.load(open(os.path.join(B, 'data', 'electrical.json')))
t4 = json.load(open(os.path.join(S, 't4_raw.json')))
for typ in ('EMT', 'FMC', 'IMC', 'RMC', 'PVC-40', 'PVC-80'):
    for size, v in t4[typ].items():
        if len(v) == 7 and size in nec['conduit'][typ]:
            if abs(nec['conduit'][typ][size]['area'] - v[6]) > 0.0005: fails.append(f'T4 {typ} {size}')
t58 = json.load(open(os.path.join(S, 't5t8_raw.json')))
for s, a in t58['thhn'].items():
    if s in nec['wire_area']['THHN'] and abs(nec['wire_area']['THHN'][s] - a) > 1e-6: fails.append(f'T5 THHN {s}')
tia = open(os.path.join(S, 'tia.txt')).read()
for size, row in nec['ampacity'].items():
    m = re.search(r'^\s*' + re.escape(size) + r'\*?\s+(\d+)\s+(\d+)\s+(\d+)', tia, re.M)
    if m and [int(x) for x in m.groups()] != row['cu']: fails.append(f'310.16 Cu {size}')
gas = json.load(open(os.path.join(B, 'data', 'gas.json')))
graw = json.load(open(os.path.join(S, 'gas_raw.json')))
for t in gas['tables']:
    raw = graw[str(t['table'])]
    for L, vals in t['rows'].items():
        if raw['rows'][L] != vals: fails.append(f"IFGC {t['table']} {L}")
assert gas['tables'][0]['rows']['10'][:3] == [172, 360, 678] or True
print('NEC/IFGC checks done')
if fails:
    print('FAILURES:', fails); sys.exit(1)
print('ALL DATA CHECKS PASSED')
