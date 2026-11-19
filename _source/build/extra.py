"""Extra editorial sections injected before the FAQ of selected pages (keeps page modules readable)."""
from core import url

def L(p, t): return f'<a href="{url(p)}">{t}</a>'

EXTRA = {
'/subcooling-calculator/': f'''<h2>Subcooling on TXV vs fixed-orifice systems</h2>
<p>On a TXV or EEV system the valve keeps evaporator superheat in a narrow band, so extra refrigerant has nowhere to go except the condenser, where it backs up as subcooled liquid. That makes subcooling the most sensitive indicator of charge on those systems, and it is why outdoor units list a target subcooling (often with a tolerance such as \u00b13 \u00b0F). On fixed-orifice systems subcooling still tells you about the condenser, but the charge is set by superheat; use the {L('/target-superheat-calculator/', 'target superheat calculator')}.</p>
<h2>Worked example with a blend</h2>
<p>An R-454B system shows 300 psig at the liquid valve. The bubble temperature at 300 psig is about 99 \u00b0F (see the {L('/r454b-pt-chart/', 'R-454B PT chart')}). The liquid line measures 89 \u00b0F, so subcooling is about 10 \u00b0F. Using the dew column by mistake would give a slightly higher saturation temperature and over-state subcooling by the glide, which for some blends is several degrees.</p>''',
'/target-superheat-calculator/': f'''<h2>Measuring the inputs correctly</h2>
<ul><li><b>Indoor wet bulb:</b> measure in the return air close to the air handler with a psychrometer or a digital wet-bulb probe, after the system has run 15 minutes. Wet bulb includes humidity, which is the main load on the evaporator.</li>
<li><b>Outdoor dry bulb:</b> measure the air entering the condenser coil in the shade, not the temperature reported by a weather app.</li>
<li><b>Measured superheat:</b> suction pressure and suction line temperature at the outdoor service valve, converted with the {L('/superheat-calculator/', 'superheat calculator')}.</li></ul>
<h2>Limits of the approximation</h2>
<p>The formula reproduces the general shape of manufacturer charging tables for residential fixed-orifice systems with standard line sets. It does not account for unusual line lengths, airflow problems or units with special metering. When the manufacturer chart is on the unit or in the installation manual, use it; when the formula gives a number below about 5 \u00b0F, many manufacturers say the system should not be charged by superheat at those conditions.</p>''',
'/hvac-calculators/': f'''<h2>Data behind the calculators</h2>
<p>All three calculators read the same saturation tables as our {L('/pt-chart/', 'PT charts')}: 32 refrigerants computed with a REFPROP-equivalent equation of state (or taken from the manufacturer chart) and compared point by point with Arkema, Honeywell, Hudson Technologies and NIST data. For blends, superheat uses the dew point and subcooling uses the bubble point automatically, so you do not have to remember which column applies.</p>
<h2>Typical workflow on a service call</h2>
<ol><li>Confirm the refrigerant and metering device from the rating plate and the indoor coil.</li><li>Check airflow, filters and coils before anything else.</li><li>Run the system 15 minutes; record suction and liquid pressures and line temperatures.</li><li>Calculate superheat and subcooling and compare with the target or rating plate.</li><li>Adjust charge slowly, wait for the system to settle, and re-measure.</li></ol>
<p>Field notes and examples: {L('/blog/superheat-vs-subcooling/', 'superheat vs subcooling')}, {L('/blog/how-to-read-a-pt-chart/', 'how to read a PT chart')}.</p>''',
'/conduit-fill-calculator/': f'''<h2>Choosing a raceway size in practice</h2>
<p>The NEC limit is a maximum, not a target. Many electricians size one trade size larger than the minimum when a run has several bends, is long, or may get extra circuits later; pulling is easier and the cost difference is small for short runs. Remember that more than three current-carrying conductors in one raceway triggers the ampacity adjustment in 310.15(C)(1), which can push you to larger wire anyway.</p>
<p>Related charts: {L('/wire-ampacity-chart/', 'wire ampacity')}, {L('/voltage-drop-calculator/', 'voltage drop')}, {L('/box-fill-calculator/', 'box fill')}.</p>''',
'/voltage-drop-calculator/': f'''<h2>Quick reference: 3% maximum one-way length</h2>
<p>For 240 V single-phase copper at 80% of the 75 \u00b0C rating (a common continuous-load case), using Table 8 resistance: 12 AWG at 16 A reaches 3% at about 114 ft; 10 AWG at 24 A at about 121 ft; 8 AWG at 40 A at about 116 ft; 6 AWG at 52 A at about 140 ft. Longer than that, upsize or accept more drop where the equipment allows it. Check your own numbers above; these are examples, not limits.</p>''',
'/gas-pipe-sizing/': f'''<h2>Choosing the right table</h2>
<p>Pick the table by four things: <b>gas</b> (natural or propane), <b>material</b> (Schedule 40 steel, CSST, polyethylene for underground outdoor use), <b>system pressure</b> (low pressure under 2 psi, or a 2 psi / 5 psi system with a regulator at the appliances) and the <b>design pressure drop</b> you allow from the meter to the farthest appliance. A 0.5 in. w.c. drop is the most common low-pressure choice in residential work; a 0.3 in. drop is more conservative. Using a table with a larger drop than your design allows will undersize the pipe.</p>
<h2>Example</h2>
<p>A furnace (100,000 Btu/h) and water heater (40,000 Btu/h) on natural gas, black iron, low pressure, 0.5 in. w.c. drop, 40 ft to the farthest appliance: 140 CFH total. The 40 ft row of Table 402.4(2) gives 3/4 in = 170 CFH, so the main can be 3/4 in; the furnace branch (100 CFH) also needs 3/4 in and the water heater branch (40 CFH) 1/2 in (81 CFH).</p>''',
'/mig-welding-settings-calculator/': f'''<h2>Fine-tuning on scrap</h2>
<ul><li>Run a bead on the same thickness and joint type. A steady \u201cbacon frying\u201d sound in short-circuit transfer means you are close.</li><li>Too much spatter and a narrow, ropey bead: raise voltage slightly or lower wire speed.</li><li>Wide, flat bead with poor penetration or burn-through: lower voltage or travel faster.</li><li>Change one setting at a time and write down what works; next time start there.</li></ul>
<p>For TIG settings see the {L('/tig-welding-amperage-chart/', 'TIG amperage chart')}.</p>''',
'/tig-welding-amperage-chart/': f'''<h2>Setting up the machine</h2>
<p>Set the maximum amperage on the machine about 10\u201320% above the starting value in the chart and control the actual current with the pedal; this gives room to push through a heat sink without changing settings. For DC steel and stainless, use DCEN (electrode negative). Pick the tungsten diameter whose current range covers the amperage you need, and grind it to a point lengthwise. Keep the cup size and gas flow appropriate to the joint access; a gas lens helps on outside corners and long stick-out.</p>
<p>For MIG settings see the {L('/mig-welding-settings-calculator/', 'MIG settings calculator')}.</p>''',
'/blog/superheat-vs-subcooling/': f'''<h2>Why airflow comes first</h2>
<p>Both readings depend on heat transfer. Low indoor airflow reduces the load on the evaporator, so superheat falls and it can look like an overcharge; a dirty outdoor coil raises head pressure and changes subcooling. Correct airflow (typically about 350\u2013400 CFM per ton unless the manufacturer says otherwise), clean coils and a clean filter before adjusting the charge. Then use the {L('/pt-chart/', 'PT chart')} for the exact refrigerant on the rating plate.</p>
<h2>A note on A2L systems</h2>
<p>R-454B and R-32 systems are charged the same way, but service practices change: A2L-rated recovery and leak-detection equipment, no ignition sources, and the manufacturer\u2019s instructions for refrigerant detection sensors and mitigation controls.</p>''',
'/blog/how-to-read-a-pt-chart/': f'''<h2>Printing a set for the truck</h2>
<p>Every chart on this site has a print button that strips menus and tools and keeps the \u00b0F and \u00b0C tables. Printing the refrigerants you service most (for example R-410A, R-454B, R-32, R-22 and R-404A) gives a compact backup when your digital manifold does not list a refrigerant.</p>''',
'/blog/conduit-fill-40-percent-rule/': f'''<h2>Quick reference</h2>
<p>For a fast answer without arithmetic, open the same-size chart for your raceway, for example the {L('/3-4-emt-conduit-fill/', '3/4 in EMT page')} (16 \u00d7 12 AWG THHN) or the {L('/1-pvc-conduit-fill/', '1 in PVC page')}. For mixed sizes use the {L('/conduit-fill-calculator/', 'calculator')}.</p>''',
'/blog/voltage-drop-3-percent-rule/': f'''<h2>DC and low-voltage circuits</h2>
<p>On 12 V and 24 V DC systems, a few volts of drop is a large percentage, so wire size is often driven by voltage drop rather than ampacity. Use the single-phase/DC setting in the calculator, which uses the round-trip length (2 \u00d7 one-way).</p>''',
'/blog/gas-pipe-sizing-longest-length-method/': f'''<h2>Branch length method</h2>
<p>The IFGC also allows a branch length method (402.4.2), which sizes each section using the length from the point of delivery to the most remote outlet <em>served by that section</em>, and a hybrid pressure method for CSST systems (402.4.3). These can allow smaller pipe on some branches but take more measuring; the longest length method is simpler and always conservative.</p>''',
'/blog/how-to-tell-water-heater-age/': f'''<h2>HVAC equipment too</h2>
<p>Furnaces, air conditioners and heat pumps also hide the date in the serial number, with different formats: {L('/carrier-age-by-serial-number/', 'Carrier')}, {L('/goodman-age-by-serial-number/', 'Goodman')}, {L('/lennox-age-by-serial-number/', 'Lennox')}, {L('/trane-age-by-serial-number/', 'Trane')} and {L('/rheem-hvac-age-by-serial-number/', 'Rheem/Ruud')}.</p>''',
}


# ---- Phase 1 run 2026-11-14: EMT size pages, computed from data/electrical.json (NEC Ch. 9 Tables 4 and 5) ----
def _emt_extra():
    import json, os
    d = json.load(open(os.path.join(os.path.dirname(__file__), 'data', 'electrical.json')))
    wa = d['wire_area']['THHN']
    out = {}
    for slug, size, label in [('1-2-emt-conduit-fill', '1/2', '1/2 inch'), ('3-4-emt-conduit-fill', '3/4', '3/4 inch'),
                              ('1-emt-conduit-fill', '1', '1 inch'), ('1-1-4-emt-conduit-fill', '1-1/4', '1-1/4 inch'),
                              ('1-1-2-emt-conduit-fill', '1-1/2', '1-1/2 inch')]:
        c = d['conduit']['EMT'].get(size)
        if not c:
            continue
        rows = ''.join(f'<tr><td>{g} AWG THHN</td><td>{wa[g]}</td><td>{int(c["a40"] // wa[g])}</td></tr>' for g in ('14', '12', '10', '8', '6', '4'))
        mix = 3 * wa['12'] + wa['12']  # three 12 AWG + one 12 AWG ground (same size)
        n4 = int(c['a40'] // wa['12'])
        out[f'/{slug}/'] = f'''<h2>How many wires fit in {label} EMT?</h2>
<p>NEC Chapter 9, Table 4 gives {label} EMT a total internal area of {c['area']} sq in. For three or more conductors Table 1 allows 40% of that, {c['a40']} sq in. Dividing by the conductor area from Table 5 (THHN/THWN-2) gives the maximum number of identical conductors:</p>
<table><caption>Maximum THHN conductors in {label} EMT at 40% fill</caption><thead><tr><th>Conductor</th><th>Area, sq in</th><th>Max conductors</th></tr></thead><tbody>{rows}</tbody></table>
<h2>Worked example</h2>
<p>A branch circuit needs three 12 AWG THHN conductors plus a 12 AWG equipment grounding conductor, four conductors in all. Total area is 4 \u00d7 {wa['12']} = {mix:.4f} sq in. The 40% allowance of {label} EMT is {c['a40']} sq in, so it {'fits' if mix <= c['a40'] else 'does not fit'} ({mix / c['area'] * 100:.0f}% of the conduit). The table above says up to {n4} 12 AWG conductors fit.</p>
<h2>How to use this page</h2>
<ol><li>List every conductor, including equipment grounds (NEC Chapter 9, Note 3).</li><li>Look up each insulated conductor area in Table 5; bare grounds use Table 8.</li><li>Add the areas and compare the total with the 40% column.</li><li>If it is over, step up one trade size and recheck. Use the {L('/conduit-fill-calculator/', 'conduit fill calculator')} for mixed sizes.</li></ol>
<p>Rules that change the answer: a section of raceway 24 inches or shorter may be filled to 60% (Note 4), and different insulation types have different areas, so XHHW and THHN results differ. Read the {L('/blog/conduit-fill-40-percent-rule/', 'NEC 40% rule explained')} for the notes in full, and always check with your local inspector, because local amendments exist. Conductor derating for more than three current-carrying conductors is a separate check on the {L('/electrical/', 'electrical hub')}.</p>'''
    return out

EXTRA.update(_emt_extra())
EXTRA['/superheat-calculator/'] = EXTRA.get('/superheat-calculator/', '') + f'''<h2>Worked example</h2>
<p>An R-410A system reads 118 psig at the suction service valve. On the {L('/r410a-pt-chart/', 'R-410A PT chart')} that is a saturation temperature of about 40 \u00b0F. The suction line, measured at the same point, is 52 \u00b0F. Superheat is 52 \u2212 40 = 12 \u00b0F. For a blend such as R-407C or R-454B, read the dew column instead of the bubble column.</p>
<h2>What to do with the number</h2>
<ul><li><b>Fixed orifice (piston):</b> compare with the manufacturer\u2019s target superheat for the indoor wet bulb and outdoor dry bulb; use the {L('/target-superheat-calculator/', 'target superheat calculator')}.</li><li><b>TXV:</b> superheat is held by the valve, so charge by subcooling instead. See {L('/blog/fixed-orifice-vs-txv-how-to-tell/', 'how to tell which you have')}.</li><li>Run the system about 15\u201320 minutes first and fix airflow before judging the charge.</li></ul>'''


def _offset_extra():
    import math
    out = {}
    for a, s in ((10, '10'), (15, '15'), (22.5, '22-5'), (30, '30'), (45, '45'), (60, '60')):
        r = math.radians(a)
        m = 1 / math.sin(r)
        sh = math.tan(r / 2)
        n = int(360 // (2 * a))
        lab = f'{a:g}'
        d1, d2 = 4, 7.5
        other = [x for x in ('10', '15', '22-5', '30', '45', '60') if x != s]
        out[f'/{s}-degree-offset-multiplier/'] = f'''<h2>Worked examples for a {lab}\u00b0 offset</h2>
<p><b>Example 1: a {d1} in. offset.</b> Distance between the two bend marks = {d1} \u00d7 {m:.3f} = {d1 * m:.2f} in. The run gets shorter by {d1} \u00d7 {sh:.3f} = {d1 * sh:.2f} in. (exact; bender charts round the per-inch value). If the conduit must end exactly at a box, measure to the box, then add that {d1 * sh:.2f} in. of shrink to the first mark so the offset lands where you want it.</p>
<p><b>Example 2: a {d2} in. offset.</b> Marks are {d2} \u00d7 {m:.3f} = {d2 * m:.2f} in. apart, and shrink is {d2 * sh:.2f} in. Notice that the spacing grows in direct proportion to the depth, so a deeper offset needs a longer clear run between the obstruction and the next fitting.</p>
<h2>How many {lab}\u00b0 offsets fit before the 360\u00b0 limit</h2>
<p>NEC rules for metal and nonmetallic conduit limit the total bends between pull points (conduit bodies, boxes or enclosures) to 360 degrees, including offsets. A standard offset is two bends of {lab}\u00b0, so it uses {2 * a:g}\u00b0 of that allowance. That means {n} {lab}\u00b0 offsets would use {n * 2 * a:g}\u00b0 of the 360\u00b0, and nothing is left for a 90\u00b0 stub-up. Plan the 90\u00b0 bends first, then see how many offsets still fit.</p>
<h2>Marking and bending steps</h2>
<ol>
<li>Measure how far the conduit must move over (the offset depth) and mark the first bend position on the conduit.</li>
<li>Calculate the spacing: depth \u00d7 {m:.3f}. Measure that distance from the first mark and make the second mark.</li>
<li>Bend the first mark to {lab}\u00b0 with the bender\u2019s arrow or {lab}\u00b0 mark aligned to the first bend mark, as your bender shows.</li>
<li>Rotate the conduit 180\u00b0 (flip it so the first bend faces the opposite direction) and keep the bends in the same plane, then bend the second mark to {lab}\u00b0.</li>
<li>Lay the conduit on a flat floor to check that both legs are in one plane and the offset depth matches your measurement.</li>
</ol>
<h2>Choosing between angles</h2>
<p>The multiplier is simply 1 \u00f7 sin({lab}\u00b0). A larger multiplier means the bends are farther apart and the conduit moves over more gradually, which is easier on a long pull; a smaller one gives a short, abrupt offset that fits in tight spots. Compare the {L(f'/{other[0]}-degree-offset-multiplier/', other[0].replace('-', '.') + '\u00b0')}, {L(f'/{other[3]}-degree-offset-multiplier/', other[3].replace('-', '.') + '\u00b0')} and other angles on the {L('/conduit-offset-multiplier-chart/', 'offset multiplier chart')}, and use the {L('/emt-conduit-fill-chart/', 'EMT fill chart')} to confirm the pipe you are bending is sized for the wire.</p>'''
    return out


EXTRA.update(_offset_extra())


# ---- run 2026-11-16 expansions ----
import json as _j, os as _o
_ED = _j.load(open(_o.path.join(_o.path.dirname(__file__), 'data', 'electrical.json')))


def _amp_extra2():
    out = {}
    A = _ED['ampacity']
    for s, v in A.items():
        slug = s.replace('/', '-')
        p = f'/{slug}-awg-wire-ampacity/'
        c = v['cu']
        lab = f'{s} AWG' if '/' not in s else f'{s} AWG'
        out[p] = f'''<h2>Worked example: bundling and terminals for {lab} copper</h2>
<p>{lab} copper THHN starts at {c[2]} A in the 90 \u00b0C column. With six current-carrying conductors in one conduit the 80% factor of Table 310.15(C)(1) gives {c[2]} \u00d7 0.80 = {c[2] * 0.8:.1f} A. With nine conductors (70%) it is {c[2] * 0.7:.1f} A, and with twelve (50%) it is {c[2] * 0.5:.1f} A. The final ampacity can never exceed the termination column, which is {c[1]} A at 75 \u00b0C and {c[0]} A at 60 \u00b0C, so use the lower of the adjusted value and the terminal value. Our {L('/blog/ampacity-derating-bundled-conductors/', 'derating guide')} works through the full method, and the {L('/blog/60c-75c-90c-ampacity-columns-explained/', 'column guide')} explains why the terminals set the limit.</p>
<h2>Checklist before you pick {lab}</h2>
<ol><li>Read the temperature marking on the breaker and the lugs.</li><li>Count current-carrying conductors in the raceway; grounds do not count.</li><li>Apply ambient and bundling adjustments from the 90 \u00b0C value if the insulation allows.</li><li>Check voltage drop with the {L('/voltage-drop-calculator/', 'voltage drop calculator')} on long runs.</li><li>Confirm the conduit size on the {L('/conduit-fill-calculator/', 'conduit fill calculator')}.</li></ol>'''
    return out


EXTRA.update({k: v for k, v in _amp_extra2().items() if k not in EXTRA})


def _pvc_extra2():
    out = {}
    W = _ED['wire_area']['THHN']
    P40, P80, E = _ED['conduit']['PVC-40'], _ED['conduit']['PVC-80'], _ED['conduit']['EMT']
    for sz in ('1/2', '3/4', '1', '1-1/4'):
        slug = sz.replace('/', '-')
        p = f'/{slug}-pvc-conduit-fill/'
        n = lambda a, w: int(a // W[w])
        rows = ''.join(f'<tr><th scope="row">{w} AWG THHN</th><td>{n(P40[sz]["a40"], w)}</td><td>{n(P80[sz]["a40"], w)}</td></tr>' for w in ('14', '12', '10', '8', '6'))
        out[p] = f'''<h2>How many wires fit: Schedule 40 vs Schedule 80</h2>
<p>At the 40% limit, {sz} in. Schedule 40 PVC offers {P40[sz]['a40']:.3f} sq in. of wire space and Schedule 80 offers {P80[sz]['a40']:.3f} sq in., because the thicker wall of Schedule 80 leaves a smaller opening. Dividing by the THHN conductor areas in Chapter 9 Table 5 gives the maximum number of same-size wires:</p>
<div class="tblwrap"><table class="data"><thead><tr><th scope="col">Wire</th><th scope="col">Schedule 40</th><th scope="col">Schedule 80</th></tr></thead><tbody>{rows}</tbody></table></div>
<p>Counts apply to all conductors of the same size and include grounds. For mixed sizes, add the areas and compare with the usable area, or use the {L('/conduit-fill-calculator/', 'conduit fill calculator')}.</p>
<h2>Using PVC in practice</h2>
<p>PVC is not a ground path, so count the equipment grounding conductor in the fill. Schedule 80 is the one to use where the conduit may be damaged, and expansion fittings are needed on long straight runs. The {L('/blog/emt-vs-pvc-vs-rigid-conduit/', 'conduit comparison guide')} covers the rules, and the {L('/blog/conduit-fill-40-percent-rule/', '40% rule guide')} explains the limit itself.</p>'''
    # 2 EMT page
    out['/2-emt-conduit-fill/'] = f'''<h2>How many wires fit in 2 in. EMT</h2>
<p>The usable area at 40% for 2 in. EMT is {E['2']['a40']:.3f} sq in. Same-size THHN counts: ''' + ', '.join(f'{int(E["2"]["a40"] // W[w])} of {w} AWG' for w in ('12', '10', '8', '6', '4', '2')) + f'''. That size is common for feeders and for runs with many circuits. Remember that more than three current-carrying conductors in the raceway requires an ampacity adjustment (see the {L('/blog/ampacity-derating-bundled-conductors/', 'derating guide')}).</p>
<h2>Tips for 2 in. runs</h2>
<ul><li>Use a conduit body or pull box every 360\u00b0 of bends.</li><li>Lubricate for long pulls and pull the heaviest conductors first.</li><li>Check the {L('/blog/emt-vs-pvc-vs-rigid-conduit/', 'EMT vs PVC vs rigid comparison')} if the run goes outdoors or underground.</li></ul>'''
    return out


EXTRA.update({k: v for k, v in _pvc_extra2().items() if k not in EXTRA})


EXTRA['/hvac-calculators/'] = EXTRA.get('/hvac-calculators/', '') + f'''<h2>Which HVAC calculator should you use?</h2>
<p>Superheat and subcooling are the two numbers that tell you whether a system is charged correctly. Which one you check depends on the metering device. On a fixed orifice or piston system, charge by {L('/superheat-calculator/', 'superheat')}. On a TXV or EEV system, charge by {L('/subcooling-calculator/', 'subcooling')}. Both need the refrigerant\u2019s saturation temperature at the measured pressure, which is what the {L('/pt-chart/', 'PT charts')} give you.</p>
<h2>A basic charging workflow</h2>
<ol>
<li>Let the system run 10 to 15 minutes so pressures settle.</li>
<li>Clamp a thermometer on the suction line near the service valve, and another on the liquid line.</li>
<li>Read suction and liquid pressures and look up the saturation temperatures for the refrigerant on the nameplate.</li>
<li>Superheat is suction line temperature minus suction saturation temperature. Subcooling is liquid saturation temperature minus liquid line temperature.</li>
<li>Compare with the manufacturer\u2019s target. Add or recover refrigerant in small steps, waiting for readings to stabilize between each.</li>
</ol>
<h2>Before you blame the charge</h2>
<p>Dirty filters, a dirty evaporator or condenser coil, low airflow and a bad blower capacitor can all mimic charge problems. Fix airflow first, then check the charge. For background, read {L('/blog/superheat-vs-subcooling/', 'superheat vs subcooling')} and {L('/blog/how-to-read-a-pt-chart/', 'how to read a PT chart')}. Always follow the equipment manufacturer\u2019s charging instructions and EPA rules for handling refrigerant.</p>
'''
EXTRA['/electrical/'] = EXTRA.get('/electrical/', '') + f'''<h2>How to use the electrical references together</h2>
<p>A typical branch circuit job touches several tools in order. First pick the conductor from the ampacity tables, then check the conduit with the {L('/conduit-fill-calculator/', 'conduit fill calculator')}, and finally plan the bends with the {L('/conduit-offset-multiplier-chart/', 'offset multiplier chart')}.</p>
<h2>Workflow for a new circuit</h2>
<ol>
<li>Find the load in amps and apply the 125% rule for continuous loads.</li>
<li>Choose a wire size from the ampacity table at the correct temperature column for your terminations.</li>
<li>If more than three current-carrying conductors share a raceway, apply derating. See {L('/blog/ampacity-derating-bundled-conductors/', 'derating bundled conductors')}.</li>
<li>Check voltage drop on long runs, and read the {L('/blog/detached-garage-subpanel-wire-size/', 'detached garage subpanel example')}.</li>
<li>Size the conduit by fill and the box by volume; see {L('/blog/box-fill-calculation-step-by-step/', 'box fill step by step')}.</li>
</ol>
<p>These pages reproduce published NEC table values for reference. Always verify against the edition of the NEC adopted where you work and follow your local inspector.</p>
'''


# ---- Phase 1 run 2026-11-19: expansions computed from site data ----
def _run1119():
    import json, os, math
    from core import table
    d = json.load(open(os.path.join(os.path.dirname(__file__), 'data', 'electrical.json')))
    wa = d['wire_area']['THHN']
    emt = d['conduit']['EMT']
    order = ['1/2', '3/4', '1', '1-1/4', '1-1/2', '2', '2-1/2', '3', '3-1/2', '4']

    def smallest(total):
        for s in order:
            if emt[s]['a40'] >= total:
                return s
        return None
    out = {}
    # conduit fill calculator
    t1 = 6 * wa['12'] + 3 * wa['10']
    s1 = smallest(t1)
    t2 = 3 * wa['1/0'] + wa['6']
    s2 = smallest(t2)
    prev2 = order[order.index(s2) - 1]
    out['/conduit-fill-calculator/'] = f'''<h2>Worked example 1: a mixed branch-circuit run</h2>
<p>A run carries six 12 AWG THHN conductors and three 10 AWG THHN conductors (two circuits plus a heavier load, grounds included). Conductor areas from NEC Chapter 9 Table 5 are {wa['12']} sq in. for 12 AWG and {wa['10']} sq in. for 10 AWG. Total area = 6 \u00d7 {wa['12']} + 3 \u00d7 {wa['10']} = {t1:.4f} sq in. Nine conductors is more than two, so the 40% limit applies. The smallest EMT with a 40% area at or above that is {s1} in. ({emt[s1]['a40']} sq in. allowed, {t1 / emt[s1]['area'] * 100:.0f}% filled).</p>
<h2>Worked example 2: a feeder with a ground</h2>
<p>Three 1/0 AWG THHN conductors and one 6 AWG THHN equipment ground: 3 \u00d7 {wa['1/0']} + {wa['6']} = {t2:.4f} sq in. {prev2} in. EMT allows only {emt[prev2]['a40']} sq in., so it is too small; {s2} in. EMT allows {emt[s2]['a40']} sq in. and passes ({t2 / emt[s2]['area'] * 100:.0f}% of its area).</p>
<h2>Fill limits at a glance</h2>
{table(['Number of conductors', 'Maximum fill (NEC Ch. 9 Table 1)'], [('1', '53%'), ('2', '31%'), ('Over 2', '40%')])}
<p>Nipples of 24 in. or less may be filled to 60% (Chapter 9 Note 4), and conductors of different insulation types need their own Table 5 areas, so do not mix THHN numbers into an XHHW run. For a ready answer for common sizes, open the {L('/1-2-emt-conduit-fill/', '1/2 in.')}, {L('/3-4-emt-conduit-fill/', '3/4 in.')} or {L('/1-emt-conduit-fill/', '1 in.')} EMT pages.</p>'''
    # 2 in EMT
    c = emt['2']
    rows = [(f'{g} AWG THHN', wa[g], int(c['a40'] // wa[g])) for g in ('12', '10', '8', '6', '4', '2', '1/0', '3/0', '250')]
    mixed = 3 * wa['4/0'] + wa['4']
    out['/2-emt-conduit-fill/'] = f'''<h2>How many wires fit in 2 inch EMT?</h2>
<p>NEC Chapter 9 Table 4 gives 2 in. EMT a total internal area of {c['area']} sq in. For three or more conductors the 40% allowance is {c['a40']} sq in. Dividing by the Table 5 area for each THHN/THWN-2 size gives the maximum number of identical conductors:</p>
{table(['Conductor', 'Area, sq in.', 'Max conductors at 40%'], rows)}
<h2>Worked example: a 200 A feeder</h2>
<p>Three 4/0 AWG THHN conductors and a 4 AWG THHN ground are {3 * wa['4/0']:.4f} + {wa['4']} = {mixed:.4f} sq in. That is {mixed / c['area'] * 100:.0f}% of 2 in. EMT, so it passes the 40% limit ({c['a40']} sq in.). Conductor size for the load still comes from the ampacity tables, see the {L('/wire-ampacity-chart/', 'wire ampacity chart')}.</p>
<h2>When to choose 2 in. EMT</h2>
<p>Two inch is a common size for service and feeder runs, and for large parallel sets split across several raceways. Plan for bends: a longer run with several 90\u00b0 bends is much harder to pull than the fill percentage suggests, so go up a trade size if the pull is long. The {L('/conduit-fill-calculator/', 'conduit fill calculator')} handles mixed conductors, and the {L('/blog/conduit-fill-40-percent-rule/', '40% rule guide')} explains the notes in full.</p>'''
    # offset chart
    mult = {a: 1 / math.sin(math.radians(a)) for a in (22.5, 30, 45)}
    rows = [(f'{dd} in.', f'{dd * mult[22.5]:.2f} in.', f'{dd * mult[30]:.2f} in.', f'{dd * mult[45]:.2f} in.') for dd in (2, 3, 4, 6, 8, 10, 12)]
    out['/conduit-offset-multiplier-chart/'] = f'''<h2>Marks for common offset depths</h2>
<p>Distance between the two bend marks equals the offset depth times the multiplier (1 \u00f7 sin of the bend angle). Using the exact multipliers {mult[22.5]:.3f} (22.5\u00b0), {mult[30]:.3f} (30\u00b0) and {mult[45]:.3f} (45\u00b0):</p>
{table(['Offset depth', 'Marks apart at 22.5\u00b0', 'Marks apart at 30\u00b0', 'Marks apart at 45\u00b0'], rows)}
<p>Field benders round these to 2.6, 2 and 1.4, so a deep offset measured with the rounded values comes out slightly different; for a 12 in. offset at 45\u00b0 the exact distance is {12 * mult[45]:.2f} in. and the rounded one is {12 * 1.4:.1f} in.</p>
<h2>How to use the chart</h2>
<ol><li>Measure the depth from the centerline of the conduit to the new centerline.</li><li>Choose the angle: 30\u00b0 is the default, 45\u00b0 for tight spaces, 22.5\u00b0 for long gentle transitions.</li><li>Read the spacing from the table or the angle page, then mark the first bend position and the second mark that distance away.</li><li>Add shrink to the overall length: the conduit is shorter by depth \u00d7 tan(angle \u00f7 2).</li></ol>
<p>Read {L('/blog/conduit-offset-angles-30-45-22-5/', 'offset angles compared')} for worked examples and {L('/blog/conduit-saddles-kicks-basics/', 'saddles and kicks')} for obstructions that need more than a simple offset.</p>'''
    # electrical hub
    out['/electrical/'] = f'''<h2>Which NEC table answers which question</h2>
{table(['Question', 'Where the answer lives', 'Page on this site'], [
 ('How much current can this wire carry?', 'NEC Table 310.16', L('/wire-ampacity-chart/', 'Wire ampacity chart')),
 ('How many wires fit in this conduit?', 'NEC Chapter 9, Tables 1, 4 and 5', L('/conduit-fill-calculator/', 'Conduit fill calculator')),
 ('How much voltage will I lose on a long run?', 'Chapter 9 Table 8 resistance', L('/voltage-drop-calculator/', 'Voltage drop calculator')),
 ('How many wires fit in this box?', 'NEC 314.16', L('/box-fill-calculator/', 'Box fill calculator')),
 ('How do I derate for more than three conductors?', 'NEC 310.15(C)(1)', L('/blog/ampacity-derating-bundled-conductors/', 'Derating guide')),
])}
<h2>Common electrical mistakes these tools prevent</h2>
<ul><li>Using the 90 \u00b0C ampacity column for a circuit whose terminals are rated 60 \u00b0C or 75 \u00b0C; read {L('/blog/60c-75c-90c-ampacity-columns-explained/', 'the temperature columns explained')}.</li>
<li>Forgetting the equipment ground when counting conduit fill.</li>
<li>Ignoring voltage drop on long runs such as {L('/blog/detached-garage-subpanel-wire-size/', 'a detached garage feeder')}.</li>
<li>Choosing a conduit by fill only, without checking {L('/blog/emt-vs-pvc-vs-rigid-conduit/', 'which raceway type suits the install')}.</li></ul>
<p>When you bend the conduit, the {L('/conduit-offset-multiplier-chart/', 'offset multiplier chart')} gives mark spacing and shrink for each angle.</p>'''
    # hvac calculators hub
    r = BY_REF = None
    import pages_hvac as ph
    r410 = ph.BY['r410a']
    Pl = 335.0
    tb = ph.tp(r410, Pl, 0)
    out['/hvac-calculators/'] = f'''<h2>Worked example: reading both numbers on an R-410A system</h2>
<p>Suction pressure 118 psig and suction line temperature 52 \u00b0F: the dew temperature at 118 psig is about 40 \u00b0F, so superheat is about 12 \u00b0F. Liquid pressure {Pl:.0f} psig and liquid line temperature 95 \u00b0F: the bubble temperature at {Pl:.0f} psig is about {tb:.0f} \u00b0F, so subcooling is about {tb - 95:.0f} \u00b0F. Compare both with the manufacturer\u2019s targets before touching the charge.</p>'''
    # target superheat
    ex = []
    for wb, db in ((62, 95), (67, 90), (72, 85)):
        ex.append((f'{wb} \u00b0F', f'{db} \u00b0F', f'{(3 * wb - 80 - db) / 2:.1f} \u00b0F'))
    out['/target-superheat-calculator/'] = f'''<h2>Worked examples from the formula</h2>
<p>Using target superheat \u2248 (3 \u00d7 WB \u2212 80 \u2212 DB) \u00f7 2:</p>
{table(['Indoor wet bulb', 'Outdoor dry bulb', 'Target superheat'], ex)}
<p>A hot, dry day with a low wet bulb gives a small target, and a mild humid day gives a large one. If your measured superheat is far above target, the system may be undercharged or short of airflow; if it is far below, it may be overcharged or have a restriction. Check airflow and coil condition first, then read {L('/blog/fixed-orifice-vs-txv-how-to-tell/', 'how to tell a fixed orifice from a TXV')} before using this page at all.</p>'''
    return out


for _k, _v in _run1119().items():
    EXTRA[_k] = EXTRA.get(_k, '') + _v


def _run1119b():
    import json, os
    from core import table
    d = json.load(open(os.path.join(os.path.dirname(__file__), 'data', 'electrical.json')))
    C = d['conduit']
    wa = d['wire_area']['THHN']
    out = {}
    for slug, size, lab in (('1-2-pvc-conduit-fill', '1/2', '1/2'), ('3-4-pvc-conduit-fill', '3/4', '3/4'), ('1-pvc-conduit-fill', '1', '1'), ('1-1-4-pvc-conduit-fill', '1-1/4', '1-1/4')):
        e, p40, p80 = C['EMT'][size], C['PVC-40'][size], C['PVC-80'][size]
        n = lambda c: int(c['a40'] // wa['12'])
        out[f'/{slug}/'] = f'''<h2>Schedule 40 vs Schedule 80 vs EMT at {lab} in.</h2>
<p>Thicker walls leave less room for wire. At the same trade size, the 40% area is {p40['a40']} sq in. for Schedule 40 PVC, {p80['a40']} sq in. for Schedule 80 PVC and {e['a40']} sq in. for EMT. With 12 AWG THHN ({wa['12']} sq in. each) that is {n(p40)} conductors in Schedule 40, {n(p80)} in Schedule 80 and {n(e)} in EMT. Use the column for the wall thickness actually installed; underground and exposed runs are often Schedule 80, which holds fewer wires.</p>
<p>See the full comparison in {L('/blog/emt-vs-pvc-vs-rigid-conduit/', 'EMT vs PVC vs rigid')}, and remember PVC expands and contracts with temperature, so long outdoor runs need expansion fittings under the NEC.</p>'''
    out['/hvac-calculators/'] = f'''<h2>When the readings disagree</h2>
<p>If superheat and subcooling both look wrong in the same direction, suspect airflow or a dirty coil before the charge. If they point in opposite directions, a restriction or a metering device problem is more likely than a simple low or high charge. Change one thing at a time and recheck after the system settles.</p>'''
    out['/conduit-offset-multiplier-chart/'] = f'''<p>For exact work, check the angle with an angle finder after the first bend; a bender that is a degree or two off changes the spacing noticeably on deep offsets.</p>'''
    out['/electrical/'] = f'''<h2>Where to start</h2>
<p>Most residential jobs begin with the load: add up the amps, choose the wire from the {L('/wire-ampacity-chart/', 'ampacity chart')}, then size the conduit with the {L('/conduit-fill-calculator/', 'fill calculator')}, check the length against the {L('/voltage-drop-calculator/', 'voltage drop calculator')} and pick the box with the {L('/box-fill-calculator/', 'box fill calculator')}. Everything here reproduces published NEC values, so confirm the edition adopted in your area and your inspector\u2019s local amendments before you buy materials.</p>
<p>New to the tables? Start with the {L('/blog/conduit-fill-40-percent-rule/', '40% fill rule')}, {L('/blog/voltage-drop-3-percent-rule/', 'the 3% voltage drop guideline')} and {L('/blog/box-fill-calculation-step-by-step/', 'box fill step by step')}.</p>'''
    return out

for _k, _v in _run1119b().items():
    EXTRA[_k] = EXTRA.get(_k, '') + _v

EXTRA['/blog/conduit-saddles-kicks-basics/'] = EXTRA.get('/blog/conduit-saddles-kicks-basics/', '') + f'''<h2>Related bending references</h2>
<p>Plain offsets use the {L('/conduit-offset-multiplier-chart/', 'offset multiplier chart')}, and the {L('/blog/conduit-offset-angles-30-45-22-5/', 'offset angles guide')} compares 22.5\u00b0, 30\u00b0 and 45\u00b0. Check that the finished conduit still fits the wire using the {L('/conduit-fill-calculator/', 'conduit fill calculator')}.</p>'''
EXTRA['/r513a-vs-r134a/'] = EXTRA.get('/r513a-vs-r134a/', '') + f'''<h2>Where to find the pressures</h2>
<p>Use the {L('/r513a-pt-chart/', 'R-513A PT chart')} and the {L('/r134a-pt-chart/', 'R-134A PT chart')} side by side when you compare readings, and read {L('/blog/refrigerant-temperature-glide/', 'temperature glide explained')} before assuming a near-azeotropic blend behaves exactly like a single refrigerant.</p>'''
