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
