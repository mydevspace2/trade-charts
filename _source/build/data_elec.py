"""Builds data/electrical.json and data/gas.json from the parsed code documents in ../src.
Sources:
 - NEC (NFPA 70) Chapter 9 Tables 4, 5, 8 (2017 edition text; these tables carry the same values in 2020/2023)
 - NEC Table 310.16 as printed in NFPA 70-2023 TIA 1691 (NFPA document)
 - NEC Table 314.16(A)/(B) as reprinted by Steel City (ABB/T&B) box catalog page
 - IFGC 2021 Tables 402.4(x) (2021 Seattle Fuel Gas Code chapter 4 = IFGC text; 402.4(2) cross-checked with ICC CodeNotes)
"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(HERE, '..', 'src')
t4 = json.load(open(os.path.join(S, 't4_raw.json')))
fix = {  # rows split across lines in the PDF text, read by hand from the same PDF (40%,60%,53%,31%,ID mm,ID in,100%)
 ('LFMC', '3/8'): [0.077, 0.115, 0.102, 0.059, 12.5, 0.494, 0.192],
 ('LFMC', '1/2'): [0.125, 0.188, 0.166, 0.097, 16.1, 0.632, 0.314],
 ('PVC-80', '1/2'): [0.087, 0.130, 0.115, 0.067, 13.4, 0.526, 0.217],
}
order = ['3/8', '1/2', '3/4', '1', '1-1/4', '1-1/2', '2', '2-1/2', '3', '3-1/2', '4', '5', '6']
conduit = {}
for typ in ('EMT', 'FMC', 'IMC', 'LFMC', 'RMC', 'PVC-40', 'PVC-80'):
    rows = dict(t4[typ])
    for (t, s), v in fix.items():
        if t == typ: rows[s] = v
    out = {}
    for s in order:
        v = rows.get(s)
        if not v or len(v) != 7: continue
        out[s] = {'id_in': v[5], 'area': v[6], 'a40': v[0], 'a53': v[2], 'a31': v[3]}
    conduit[typ] = out
# RMC 3 and 3-1/2: 40% values 3.000 / 4.004 in the PDF; total area = 40%/0.4 (7.499 and 10.010 in the table)
import math
for s_, A, a40 in (('3', 7.499, 3.000), ('3-1/2', 10.010, 4.004)):
    conduit['RMC'][s_] = {'id_in': round(math.sqrt(4 * A / math.pi), 3), 'area': A, 'a40': a40, 'a53': round(0.53 * A, 3), 'a31': round(0.31 * A, 3)}
conduit['RMC'] = {s: conduit['RMC'][s] for s in order if s in conduit['RMC']}
t58 = json.load(open(os.path.join(S, 't5t8_raw.json')))
wire_area = {'THHN': t58['thhn'], 'XHHW': t58['xhhw']}
t8 = {k: {'cmil': v['cmil'], 'cu': v['cu_ohm_kft'], 'al': v['al_ohm_kft']} for k, v in t58['t8'].items()}
for k, cm, cu, al in (('250', 250000, 0.0515, 0.0847), ('300', 300000, 0.0429, 0.0707), ('350', 350000, 0.0367, 0.0605),
                      ('400', 400000, 0.0321, 0.0529), ('500', 500000, 0.0258, 0.0424), ('600', 600000, 0.0214, 0.0353),
                      ('700', 700000, 0.0184, 0.0303), ('750', 750000, 0.0171, 0.0282), ('800', 800000, 0.0161, 0.0265),
                      ('900', 900000, 0.0143, 0.0235), ('1000', 1000000, 0.0129, 0.0212)):
    t8[k] = {'cmil': cm, 'cu': cu, 'al': al}
tia = open(os.path.join(S, 'tia.txt')).read()
amp = {}
for size in ['14', '12', '10', '8', '6', '4', '3', '2', '1', '1/0', '2/0', '3/0', '4/0', '250', '300', '350', '400', '500', '600', '700', '750', '800', '900', '1000']:
    m = re.search(r'^\s*' + re.escape(size) + r'\*?\s+(\d+)\s+(\d+)\s+(\d+)(?:\s+(\d+)\s+(\d+)\s+(\d+))?', tia, re.M)
    cu = [int(m.group(i)) for i in (1, 2, 3)]
    al = [int(m.group(i)) for i in (4, 5, 6)] if m.group(4) and size != '14' else None
    amp[size] = {'cu': cu, 'al': al}
boxes = [  # Table 314.16(A) metal boxes: name, cubic inches
 ('4 x 1-1/4 round/octagonal', 12.5), ('4 x 1-1/2 round/octagonal', 15.5), ('4 x 2-1/8 round/octagonal', 21.5),
 ('4 x 1-1/4 square', 18.0), ('4 x 1-1/2 square', 21.0), ('4 x 2-1/8 square', 30.3),
 ('4-11/16 x 1-1/4 square', 25.5), ('4-11/16 x 1-1/2 square', 29.5), ('4-11/16 x 2-1/8 square', 42.0),
 ('3 x 2 x 1-1/2 device', 7.5), ('3 x 2 x 2 device', 10.0), ('3 x 2 x 2-1/4 device', 10.5), ('3 x 2 x 2-1/2 device', 12.5),
 ('3 x 2 x 2-3/4 device', 14.0), ('3 x 2 x 3-1/2 device', 18.0), ('4 x 2-1/8 x 1-1/2 device', 10.3),
 ('4 x 2-1/8 x 1-7/8 device', 13.0), ('4 x 2-1/8 x 2-1/8 device', 14.5), ('3-3/4 x 2 x 2-1/2 masonry box/gang', 14.0),
 ('3-3/4 x 2 x 3-1/2 masonry box/gang', 21.0)]
allow = {'18': 1.5, '16': 1.75, '14': 2.0, '12': 2.25, '10': 2.5, '8': 3.0, '6': 5.0}
json.dump({'conduit': conduit, 'wire_area': wire_area, 't8': t8, 'ampacity': amp, 'boxes': boxes, 'box_allow': allow},
          open(os.path.join(HERE, 'data', 'electrical.json'), 'w'), indent=0)
graw = json.load(open(os.path.join(S, 'gas_raw.json')))
meta = {  # table: (slug, short title)
 2: ('natural-gas-pipe-sizing-chart', 'Natural gas, Schedule 40 black iron, under 2 psi, 0.5 in. w.c. drop'),
 1: ('natural-gas-pipe-sizing-chart-0-3-inch-drop', 'Natural gas, Schedule 40 black iron, under 2 psi, 0.3 in. w.c. drop'),
 5: ('2-psi-natural-gas-pipe-sizing-chart', 'Natural gas, Schedule 40 black iron, 2 psi system, 1 psi drop'),
 15: ('csst-gas-pipe-sizing-chart', 'Natural gas, CSST, under 2 psi, 0.5 in. w.c. drop'),
 18: ('2-psi-csst-gas-pipe-sizing-chart', 'Natural gas, CSST, 2 psi system, 1 psi drop'),
 21: ('polyethylene-gas-pipe-sizing-chart', 'Natural gas, polyethylene (PE) pipe, under 2 psi, 0.5 in. w.c. drop'),
 28: ('propane-gas-pipe-sizing-chart', 'Propane (LP), Schedule 40 black iron, 11 in. w.c., 0.5 in. w.c. drop'),
 27: ('2-psi-propane-pipe-sizing-chart', 'Propane (LP), Schedule 40 black iron, 2 psi, 1 psi drop'),
 32: ('propane-csst-sizing-chart', 'Propane (LP), CSST, 11 in. w.c., 0.5 in. w.c. drop'),
 33: ('2-psi-propane-csst-sizing-chart', 'Propane (LP), CSST, 2 psi, 1 psi drop'),
 35: ('propane-polyethylene-pipe-sizing-chart', 'Propane (LP), polyethylene (PE) pipe, 11 in. w.c., 0.5 in. w.c. drop'),
 36: ('2-psi-propane-polyethylene-pipe-sizing-chart', 'Propane (LP), polyethylene (PE) pipe, 2 psi, 1 psi drop'),
}
tables = []
for n in (2, 1, 5, 15, 18, 21, 28, 27, 32, 33, 35, 36):
    r = graw[str(n)]
    tables.append({'table': n, 'slug': meta[n][0], 'title': meta[n][1], 'material': r['title'], 'gas': r['gas'], 'inlet': r['inlet'],
                   'drop': r['drop'], 'sg': r['sg'], 'sizes': r['sizes'], 'unit': r['unit'], 'rows': r['rows']})
json.dump({'tables': tables}, open(os.path.join(HERE, 'data', 'gas.json'), 'w'))
print('electrical + gas data written', {k: len(v) for k, v in conduit.items()}, len(amp), len(tables))
