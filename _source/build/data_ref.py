"""Builds refrigerant saturation tables (data/refrigerants.json).

Source of numbers: CoolProp 8 (open-source, NIST REFPROP-equivalent Helmholtz equations of state;
predefined ASHRAE blend compositions) for every refrigerant except R-438A, whose table comes
straight from the DuPont/Chemours ISCEON MO99 pressure-temperature chart (CoolProp cannot model it
reliably: missing binary interaction parameters). Every refrigerant is cross-checked against
manufacturer / reference charts in qa/test_data.py.
Run: python3 data_ref.py
"""
import json, os, re, math
import CoolProp.CoolProp as CP

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'src')
ATM = 14.6959  # psia
PA_PER_PSI = 6894.757

# slug, label, coolprop fluid, kind, safety, gwp, gwp_src, composition, replaces/uses
R = [
 # A/C & heat pump
 ('r454b','R-454B','R454B.mix','HFO/HFC blend (zeotropic)','A2L','465','UNEP','R-32/R-1234yf (68.9/31.1)','New residential and light-commercial A/C and heat pumps replacing R-410A (new equipment only, not a retrofit).','Opteon XL41, Solstice 454B, Forane 454B'),
 ('r32','R-32','R32','HFC (single component)','A2L','675','AR4','R-32 (100)','New ductless and ducted A/C and heat pumps replacing R-410A (new equipment only).','Forane 32'),
 ('r410a','R-410A','R410A','HFC blend (near-azeotropic)','A1','2,088','UNEP','R-32/R-125 (50/50)','Residential and commercial A/C and heat pumps built before the 2025 A2L transition; now a service refrigerant.','Puron, Suva 9100, Forane 410A'),
 ('r22','R-22','R22','HCFC (single component)','A1','1,810','AR4','R-22 (100)','Legacy A/C and refrigeration. US production and import ended 1 Jan 2020; service from reclaimed or stockpiled gas only.','Freon 22, Genetron 22'),
 ('r407c','R-407C','R407C','HFC blend (zeotropic)','A1','1,774','UNEP','R-32/R-125/R-134a (23/25/52)','Retrofit and new-equipment replacement for R-22 in A/C and some refrigeration.','Freon 407C, Forane 407C'),
 ('r466a','R-466A','R466A.mix','HFC/iodine blend (zeotropic)','A1','733','UNEP','R-32/R-125/R-13I1 (49/11.5/39.5)','Non-flammable lower-GWP alternative to R-410A for new A/C equipment.','Solstice N41'),
 ('r422d','R-422D','R422D.mix','HFC/HC blend (zeotropic)','A1','2,729','UNEP','R-125/R-134a/R-600a (65.1/31.5/3.4)','Retrofit for R-22 in A/C and medium/low-temperature refrigeration.','ISCEON MO29, Genetron 422D'),
 ('r438a','R-438A','TABLE','HFC/HC blend (zeotropic)','A1','2,264','UNEP','R-32/R-125/R-134a/R-600/R-601a (8.5/45/44.2/1.7/0.6)','Mineral-oil compatible retrofit for R-22 in A/C and refrigeration.','Freon / ISCEON MO99'),
 ('r421a','R-421A','R421A.mix','HFC blend (zeotropic)','A1','2,631','UNEP','R-125/R-134a (58/42)','Retrofit for R-22 in A/C and medium-temperature refrigeration.','Choice R421A'),
 ('r417a','R-417A','R417A.mix','HFC/HC blend (zeotropic)','A1','2,346','UNEP','R-125/R-134a/R-600 (46.6/50/3.4)','Retrofit for R-22 in A/C and refrigeration.','ISCEON 59, NU-22'),
 ('r427a','R-427A','R427A.mix','HFC blend (zeotropic)','A1','2,138','UNEP','R-32/R-125/R-143a/R-134a (15/25/10/50)','Retrofit for R-22 in A/C, medium- and low-temperature systems.','Forane 427A'),
 # commercial refrigeration
 ('r404a','R-404A','R404A','HFC blend (near-azeotropic)','A1','3,922','UNEP','R-125/R-143a/R-134a (44/52/4)','Medium- and low-temperature commercial refrigeration; being phased down in new equipment.','Forane 404A, Genetron 404A'),
 ('r507a','R-507A','R507A','HFC blend (azeotropic)','A1','3,985','UNEP','R-125/R-143a (50/50)','Low- and medium-temperature commercial refrigeration (similar to R-404A).','AZ-50, Forane 507A'),
 ('r448a','R-448A','R448A.mix','HFO/HFC blend (zeotropic)','A1','1,386','UNEP','R-32/R-125/R-1234yf/R-134a/R-1234ze(E) (26/26/20/21/7)','Lower-GWP replacement for R-404A, R-507A and R-22 in supermarket and commercial refrigeration (new and retrofit).','Solstice N40, Forane 448A'),
 ('r449a','R-449A','R449A.mix','HFO/HFC blend (zeotropic)','A1','1,396','UNEP','R-32/R-125/R-1234yf/R-134a (24.3/24.7/25.3/25.7)','Lower-GWP replacement for R-404A, R-507A and R-22 in commercial refrigeration (new and retrofit).','Opteon XP40, Forane 449A'),
 ('r407a','R-407A','R407A.mix','HFC blend (zeotropic)','A1','2,107','UNEP','R-32/R-125/R-134a (20/40/40)','Replacement for R-22 and R-404A in medium- and low-temperature refrigeration.','Klea 60, Forane 407A'),
 ('r407f','R-407F','R407F.mix','HFC blend (zeotropic)','A1','1,825','UNEP','R-32/R-125/R-134a (30/30/40)','Replacement for R-22 and R-404A in commercial refrigeration.','Genetron Performax LT'),
 ('r452a','R-452A','R452A.mix','HFO/HFC blend (zeotropic)','A1','2,139','UNEP','R-32/R-125/R-1234yf (11/59/30)','Transport refrigeration and retrofit of R-404A/R-507A.','Opteon XP44, Forane 452A'),
 # R-454C dropped: CoolProp deviates >1 °F from the charts checked
 # ('r454c','R-454C','R454C.mix','HFO/HFC blend (zeotropic)','A2L','145','UNEP','R-32/R-1234yf (21.5/78.5)','Low-GWP option for new commercial refrigeration and heat pumps.','Opteon XL20'),
 ('r455a','R-455A','R455A.mix','HFO/HFC/CO2 blend (zeotropic)','A2L','145','UNEP','R-744/R-32/R-1234yf (3/21.5/75.5)','Low-GWP option for new self-contained commercial refrigeration.','Solstice L40X'),
 ('r454a','R-454A','R454A.mix','HFO/HFC blend (zeotropic)','A2L','236','UNEP','R-32/R-1234yf (35/65)','Low-GWP option for new commercial refrigeration.','Opteon XL40'),
 ('r290','R-290','Propane','Hydrocarbon (propane)','A3','very low (single digits)','NAT','R-290 propane (100)','Self-contained commercial refrigeration (reach-ins, ice machines), some heat pumps. Flammable: follow charge limits and A3 service practice.','Propane (refrigerant grade)'),
 ('r600a','R-600a','IsoButane','Hydrocarbon (isobutane)','A3','very low (single digits)','NAT','R-600a isobutane (100)','Household refrigerators and small appliances. Flammable: follow A3 service practice.','Isobutane (refrigerant grade)'),
 ('r744','R-744','CO2','Natural (carbon dioxide)','A1','1 (by definition)','NAT','R-744 carbon dioxide (100)','Transcritical and cascade supermarket systems, heat-pump water heaters. Very high pressures; critical point 87.8 °F.','CO2'),
 ('r717','R-717','Ammonia','Natural (ammonia)','B2L','0','NAT','R-717 ammonia (100)','Industrial refrigeration (cold storage, food processing). Toxic: follow IIAR and site safety rules.','Ammonia (anhydrous)'),
 # medium / low pressure
 ('r134a','R-134a','R134a','HFC (single component)','A1','1,430','AR4','R-134a (100)','Automotive A/C (older vehicles), medium-temperature refrigeration, chillers, appliances.','Freon 134a, Forane 134a'),
 ('r513a','R-513A','R513A.mix','HFO/HFC blend (azeotropic)','A1','629','UNEP','R-1234yf/R-134a (56/44)','Lower-GWP replacement for R-134a in chillers and medium-temperature refrigeration (not automotive).','Opteon XP10, Forane 513A'),
 ('r450a','R-450A','R450A.mix','HFO/HFC blend (near-azeotropic)','A1','601','UNEP','R-134a/R-1234ze(E) (42/58)','Lower-GWP replacement for R-134a in medium-temperature refrigeration.','Solstice N13'),
 ('r1234yf','R-1234yf','R1234yf','HFO (single component)','A2L','very low (single digits)','NAT','R-1234yf (100)','Automotive A/C in most new vehicles (replaced R-134a).','Opteon YF, Solstice yf'),
 ('r1234ze','R-1234ze(E)','R1234ze(E)','HFO (single component)','A2L','<1','ASHRAE','R-1234ze(E) (100)','Chillers, heat pumps and some medium-temperature systems.','Solstice ze'),
 ('r12','R-12','R12','CFC (single component)','A1','10,900','AR4','R-12 (100)','Legacy automotive A/C and refrigeration (pre-1995). Production banned; recovered gas only.','Freon 12'),
 ('r123','R-123','R123','HCFC (single component)','B1','77','AR4','R-123 (100)','Low-pressure centrifugal chillers. Production for new equipment ended in the US in 2020.','Freon 123, Genetron 123'),
 ('r1233zd','R-1233zd(E)','R1233zd(E)','HCFO (single component)','A1','1','ASHRAE','R-1233zd(E) (100)','Low-pressure centrifugal chillers replacing R-123.','Solstice zd, Forane 1233zd'),
]
# which reference charts check each refrigerant (keys used by qa/test_data.py)
CHECK = {
 'r454b':['Arkema Forane PT chart (2025, REFPROP 10)','Honeywell Solstice 454B PT chart','ASHRAE 34 bubble/dew at 1 atm'],
 'r32':['Arkema Forane PT chart (2025, REFPROP 10)','Hudson Technologies PT chart'],
 'r410a':['Arkema Forane PT chart (2025, REFPROP 10)'],
 'r22':['Arkema Forane PT chart (2025, REFPROP 10)','Hudson Technologies PT chart'],
 'r407c':['Arkema Forane PT chart (2025, REFPROP 10)','Honeywell pressure-based PT chart','Hudson Technologies PT chart'],
 'r466a':['Honeywell Solstice N41 presentation (average pressure, bar)','ASHRAE 34 bubble/dew at 1 atm'],
 'r422d':['Honeywell pressure-based PT chart','Hudson Technologies PT chart'],
 'r438a':['DuPont/Chemours ISCEON MO99 PT chart (source table)','Hudson Technologies PT chart'],
 'r421a':['Hudson Technologies PT chart'],
 'r417a':['Hudson Technologies PT chart'],
 'r427a':['Arkema Forane PT chart (2025, REFPROP 10)','Hudson Technologies PT chart'],
 'r404a':['Arkema Forane PT chart (2025, REFPROP 10)','Honeywell pressure-based PT chart'],
 'r507a':['Honeywell pressure-based PT chart'],
 'r448a':['Arkema Forane PT chart (2025, REFPROP 10)','Honeywell pressure-based PT chart','Hudson Technologies PT chart','ASHRAE 34 bubble/dew at 1 atm'],
 'r449a':['Arkema Forane PT chart (2025, REFPROP 10)','Hudson Technologies PT chart','ASHRAE 34 bubble/dew at 1 atm'],
 'r407a':['Hudson Technologies PT chart'],
 'r407f':['Honeywell pressure-based PT chart','Hudson Technologies PT chart','ASHRAE 34 bubble/dew at 1 atm'],
 'r452a':['Arkema Forane PT chart (2025, REFPROP 10)','Hudson Technologies PT chart','ASHRAE 34 bubble/dew at 1 atm'],
 'r454c':['Hudson Technologies PT chart (liquid)','ASHRAE 34 bubble/dew at 1 atm'],
 'r455a':['Hudson Technologies PT chart (liquid)','ASHRAE 34 bubble/dew at 1 atm'],
 'r454a':['Hudson Technologies PT chart (liquid)','ASHRAE 34 bubble/dew at 1 atm'],
 'r290':['NIST Chemistry WebBook saturation data'],
 'r600a':['NIST Chemistry WebBook saturation data'],
 'r744':['NIST Chemistry WebBook saturation data','Hudson Technologies PT chart'],
 'r717':['NIST Chemistry WebBook saturation data'],
 'r134a':['Arkema Forane PT chart (2025, REFPROP 10)','Hudson Technologies PT chart'],
 'r513a':['Arkema Forane PT chart (2025, REFPROP 10)','Hudson Technologies PT chart','ASHRAE 34 bubble/dew at 1 atm'],
 'r450a':['Hudson Technologies PT chart','ASHRAE 34 bubble/dew at 1 atm'],
 'r1234yf':['Hudson Technologies PT chart'],
 'r1234ze':['Hudson Technologies PT chart'],
 'r12':['Hudson Technologies PT chart'],
 'r123':['Hudson Technologies PT chart'],
 'r1233zd':['Hudson Technologies PT chart'],
}

def k_of_f(F): return (F - 32) / 1.8 + 273.15

def coolprop_table(fl, tmin, tmax):
    fl = 'HEOS::' + fl
    try:
        tc = CP.PropsSI('Tcrit', fl)
    except Exception:
        tc = None
    rows = []
    for F in range(tmin, tmax + 1):
        T = k_of_f(F)
        if tc and T > tc - 1.0:
            break
        try:
            b = CP.PropsSI('P', 'T', T, 'Q', 0, fl) / PA_PER_PSI - ATM
            d = CP.PropsSI('P', 'T', T, 'Q', 1, fl) / PA_PER_PSI - ATM
        except Exception:
            break
        if not (math.isfinite(b) and math.isfinite(d)) or b < d - 0.05 or (rows and b < rows[-1][1]):
            break  # stop at numerical trouble (near critical region of blends)
        rows.append((F, round(b, 2), round(d, 2)))
    return rows

def mo99_table():
    """R-438A from the DuPont ISCEON MO99 pressure-based chart: psig -> bubble/dew °F."""
    pts = []
    for l in open(os.path.join(SRC, 'mo99.txt')):
        n = re.findall(r'-?\d+\.?\d*', l)
        if len(n) in (4, 8) and re.match(r'^\s*-?\d', l):
            for g in range(0, len(n), 4):
                P, _, b, d = [float(x) for x in n[g:g + 4]]
                pts.append((P, b, d))
    pts.sort()
    def inv(col, F):  # temperature -> pressure by linear interpolation on the chart
        for (p1, *t1), (p2, *t2) in zip(pts, pts[1:]):
            a, c = t1[col], t2[col]
            if a <= F <= c:
                return p1 + (p2 - p1) * (F - a) / (c - a)
        return None
    rows = []
    for F in range(-60, 161):
        b, d = inv(0, F), inv(1, F)
        if b is None or d is None:
            continue
        # chart's negative "psig" values are vacuum in psi (not inHg) – keep as psig
        rows.append((F, round(b, 2), round(d, 2)))
    return rows, pts

def build():
    out = []
    for slug, label, fl, kind, safety, gwp, gsrc, comp, uses, trade in R:
        tmin = -60
        if slug in ('r123', 'r1233zd'):
            tmin = -20
        tmax = 160
        if slug in ('r123', 'r1233zd'):
            tmax = 200
        if fl == 'TABLE':
            rows, _ = mo99_table()
            src = 'chart'
        else:
            rows = coolprop_table(fl, tmin, tmax)
            src = 'coolprop'
        blend = any(abs(b - d) > 0.05 for _, b, d in rows)
        crit = None
        if fl not in ('TABLE',):
            try:
                crit = round((CP.PropsSI('Tcrit', 'HEOS::' + fl) - 273.15) * 1.8 + 32, 1)
            except Exception:
                crit = None
        out.append(dict(slug=slug, name=label, fluid=fl, kind=kind, safety=safety, gwp=gwp, gwp_src=gsrc,
                        composition=comp, uses=uses, trade=trade, source=src, blend=blend, tcrit_f=crit,
                        checks=CHECK.get(slug, []), t=[r[0] for r in rows], b=[r[1] for r in rows],
                        d=[r[2] for r in rows]))
        print(f'{label:12s} {src:8s} rows={len(rows):3d} range {rows[0][0]}..{rows[-1][0]} F blend={blend}')
    os.makedirs(os.path.join(HERE, 'data'), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, 'data', 'refrigerants.json'), 'w'))

if __name__ == '__main__':
    build()
