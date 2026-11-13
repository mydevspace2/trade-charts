"""Refrigerant PT chart pages, PT hub, HVAC calculators and refrigerant comparisons."""
import json, os, math
from core import *

D = os.path.join(HERE, 'data')
REFS = json.load(open(os.path.join(D, 'refrigerants.json')))
VER = json.load(open(os.path.join(D, 'verification.json')))
BY = {r['slug']: r for r in REFS}
ATM = 14.6959

def pf(r, F, q):
    t = r['t']
    if F < t[0] or F > t[-1]:
        return None
    i = min(int(math.floor(F - t[0])), len(t) - 2)
    arr = r['b'] if q == 0 else r['d']
    f = F - t[i]
    return arr[i] + (arr[i + 1] - arr[i]) * f

def tp(r, P, q):
    arr = r['b'] if q == 0 else r['d']
    t = r['t']
    for i in range(len(t) - 1):
        if arr[i] <= P <= arr[i + 1]:
            return t[i] + (P - arr[i]) / (arr[i + 1] - arr[i])
    return None

def ps(p):
    """psig with vacuum shown as inHg"""
    if p is None:
        return '\u2014'
    if p < 0:
        return f'{-p * 2.03602:.1f}&nbsp;inHg vac'
    return f'{p:,.1f}'

def c_of(F): return (F - 32) / 1.8
def f_of(C): return C * 1.8 + 32

def pt_slug(r): return f"/{r['slug']}-pt-chart/"

def glide(r, F):
    b, d = pf(r, F, 0), pf(r, F, 1)
    if b is None:
        return None
    tb, td = tp(r, b, 0), tp(r, b, 1)
    return None if (tb is None or td is None) else td - tb

def nbp(r):
    return tp(r, 0.0, 0), tp(r, 0.0, 1)

GROUP = {
 'A/C and heat pump': ['r454b', 'r32', 'r410a', 'r22', 'r407c', 'r466a', 'r422d', 'r438a', 'r421a', 'r417a', 'r427a'],
 'Commercial refrigeration': ['r404a', 'r507a', 'r448a', 'r449a', 'r407a', 'r407f', 'r452a', 'r455a', 'r454a', 'r290', 'r744', 'r717'],
 'Medium-pressure, automotive and appliances': ['r134a', 'r513a', 'r450a', 'r1234yf', 'r1234ze', 'r600a', 'r12'],
 'Low-pressure chillers': ['r123', 'r1233zd'],
}
RELATED = {
 'r454b': ['r410a', 'r32', 'r466a'], 'r32': ['r454b', 'r410a'], 'r410a': ['r454b', 'r32', 'r22'], 'r22': ['r410a', 'r407c', 'r422d', 'r438a', 'r427a'],
 'r407c': ['r22', 'r410a', 'r427a'], 'r466a': ['r410a', 'r454b', 'r32'], 'r422d': ['r22', 'r438a', 'r417a'], 'r438a': ['r22', 'r422d', 'r427a'],
 'r421a': ['r22', 'r422d', 'r417a'], 'r417a': ['r22', 'r422d', 'r438a'], 'r427a': ['r22', 'r407c', 'r438a'], 'r404a': ['r448a', 'r449a', 'r507a', 'r452a'],
 'r507a': ['r404a', 'r448a', 'r449a'], 'r448a': ['r449a', 'r404a', 'r407a'], 'r449a': ['r448a', 'r404a', 'r407f'], 'r407a': ['r404a', 'r448a', 'r407f'],
 'r407f': ['r407a', 'r448a', 'r404a'], 'r452a': ['r404a', 'r448a', 'r449a'], 'r455a': ['r454a', 'r404a', 'r290'], 'r454a': ['r455a', 'r404a', 'r448a'],
 'r290': ['r600a', 'r404a', 'r134a'], 'r744': ['r717', 'r404a', 'r448a'], 'r717': ['r744', 'r507a'], 'r134a': ['r513a', 'r1234yf', 'r450a', 'r12'],
 'r513a': ['r134a', 'r450a', 'r1234yf'], 'r450a': ['r134a', 'r513a'], 'r1234yf': ['r134a', 'r12', 'r1234ze'], 'r1234ze': ['r1234yf', 'r134a', 'r1233zd'],
 'r600a': ['r290', 'r134a'], 'r12': ['r134a', 'r1234yf'], 'r123': ['r1233zd', 'r1234ze'], 'r1233zd': ['r123', 'r1234ze'],
}
SAFETY = {
 'A1': 'ASHRAE safety group <strong>A1</strong>: lower toxicity and no flame propagation in standard tests. It is still an asphyxiant in enclosed spaces and decomposes into toxic products in a flame or on hot surfaces, so ventilate, never braze on a charged system, and wear eye and skin protection.',
 'A2L': 'ASHRAE safety group <strong>A2L</strong>: lower toxicity and <em>mildly</em> flammable (low burning velocity). Use A2L-rated recovery machines and leak detectors, remove ignition sources, ventilate the work area, and follow the equipment manufacturer\u2019s A2L service instructions and UL 60335-2-40 / ASHRAE 15 requirements for the installation.',
 'A3': 'ASHRAE safety group <strong>A3</strong>: lower toxicity and <em>highly</em> flammable. Only technicians trained for hydrocarbon refrigerants should service it, with spark-proof tools, a hydrocarbon-rated leak detector and recovery equipment, and no ignition sources. Never substitute it into equipment not designed for it.',
 'B1': 'ASHRAE safety group <strong>B1</strong>: higher toxicity, no flame propagation. Chiller rooms need refrigerant monitors and ventilation per ASHRAE 15; use the required PPE and follow the chiller manufacturer\u2019s procedures.',
 'B2L': 'ASHRAE safety group <strong>B2L</strong>: higher toxicity and mildly flammable. Ammonia systems are governed by IIAR standards and site process-safety programs; use ammonia-specific PPE and detection and work only under your facility\u2019s procedures.',
}

def chart_rows_f(r, step=5):
    rows = []
    t0 = int(math.ceil(r['t'][0] / step) * step)
    for F in range(t0, r['t'][-1] + 1, step):
        b, d = pf(r, F, 0), pf(r, F, 1)
        if r['blend']:
            rows.append((f'{F}', ps(b), ps(d), f'{c_of(F):.1f}'))
        else:
            rows.append((f'{F}', ps(b), f'{(b + ATM) * 6.894757 - 101.325:,.0f}' if b is not None else '', f'{c_of(F):.1f}'))
    return rows

def chart_rows_c(r, step=2):
    rows = []
    cmin = math.ceil(c_of(r['t'][0]) / step) * step
    cmax = math.floor(c_of(r['t'][-1]))
    C = cmin
    while C <= cmax:
        F = f_of(C)
        b, d = pf(r, F, 0), pf(r, F, 1)
        kb = (b + ATM) * 6.894757 - 101.325 if b is not None else None
        kd = (d + ATM) * 6.894757 - 101.325 if d is not None else None
        if r['blend']:
            rows.append((f'{C}', f'{kb:,.0f}', f'{kd:,.0f}', f'{kb / 100:,.2f}', f'{kd / 100:,.2f}'))
        else:
            rows.append((f'{C}', f'{kb:,.0f}', f'{kb / 100:,.2f}', f'{F:.1f}'))
        C += step
    return rows

def ver_text(r):
    v = VER[r['slug']]
    srcs = '; '.join(f"{k} ({x['n']} points, max {x['max']:.2f} \u00b0F)" for k, x in v['sources'].items())
    return v, srcs

def source_para(r):
    v, srcs = ver_text(r)
    if r['source'] == 'chart':
        how = ('This table is taken directly from the DuPont/Chemours ISCEON\u00ae MO99\u2122 (R-438A) pressure-temperature chart, '
               'which lists bubble and dew temperatures for each gauge pressure. We converted it to a temperature-based layout by '
               'linear interpolation between the published pressure rows (the open CoolProp library cannot model this five-component '
               'blend reliably, so we did not compute it).')
    else:
        how = ('Pressures are computed with <a href="https://coolprop.org" rel="noopener">CoolProp</a> 8, an open-source property library that '
               'implements the same Helmholtz equations of state used by NIST REFPROP, at 1 \u00b0F steps'
               + (' with the ASHRAE Standard 34 blend composition' if r['blend'] else '') + '.')
    return (f'<p>{how} We then checked the result against published charts: {srcs}. Across all {v["points"]} compared points the largest '
            f'difference is <strong>{v["max_dev_f"]:.2f} \u00b0F</strong> in saturation temperature (our pass limit is 1.0 \u00b0F, about the resolution '
            f'of a good digital gauge). Points within 2 psi of atmospheric pressure are not compared because printed charts switch to vacuum units there.</p>')

def gwp_text(r):
    s = {'UNEP': 'IPCC AR4 100-year value as listed by the UNEP Ozone Secretariat',
         'AR4': 'IPCC AR4 100-year value', 'ASHRAE': 'GWP100 from the ASHRAE/UNEP refrigerant factsheet (2025)',
         'NAT': 'natural refrigerant / ultra-low GWP'}[r['gwp_src']]
    return f"{r['gwp']} <small>({s})</small>"

def pt_tool(r, compact=False):
    data = {'n': r['name'], 't0': r['t'][0], 'b': r['b'], 'd': r['d'], 'bl': r['blend']}
    js = json.dumps(data, separators=(',', ':'))
    return f'''<section class="tool" aria-labelledby="tool-h">
<h2 id="tool-h">{esc(r["name"])} pressure-temperature lookup</h2>
<div class="pt" data-tool="pt">
 <div class="seg" role="group" aria-label="Lookup direction"><button type="button" data-mode="t2p" aria-pressed="true">Temp &rarr; Pressure</button><button type="button" data-mode="p2t" aria-pressed="false">Pressure &rarr; Temp</button></div>
 <div class="row">
  <label>Value <input type="number" inputmode="decimal" step="any" data-in value="40"></label>
  <label class="u-t">Temp unit <select data-tu><option value="F">\u00b0F</option><option value="C">\u00b0C</option></select></label>
  <label class="u-p" hidden>Pressure unit <select data-pu><option value="psig">psig</option><option value="kpa">kPa (gauge)</option><option value="bar">bar (gauge)</option></select></label>
 </div>
 <output class="res" data-out aria-live="polite"></output>
 <script type="application/json" class="ptdata">{js}</script>
</div>
<p class="hint">{"For this zeotropic blend use the <b>dew</b> value for superheat (evaporator / suction line) and the <b>bubble</b> value for subcooling (condenser / liquid line)." if r["blend"] else "Single-component refrigerant: one saturation pressure per temperature, used for both superheat and subcooling."} Valid {r["t"][0]} to {r["t"][-1]} \u00b0F.</p>
</section>'''

def pt_page(r):
    s = r['slug']; n = r['name']
    v = VER[s]
    e40d, e40b = pf(r, 40, 1), pf(r, 40, 0)
    c100 = pf(r, 100, 0)
    c110 = pf(r, 110, 0)
    g40 = glide(r, 40)
    nb, nd = nbp(r)
    path = pt_slug(r)
    key = n.replace('-', '').replace('(E)', '').lower()
    title = f'{n} PT Chart: Pressure-Temperature Table (\u00b0F & \u00b0C)'
    if r['blend']:
        desc = f'{n} PT chart with bubble and dew pressures, \u00b0F and \u00b0C, psig and kPa. Interactive lookup both ways, printable table, GWP and safety class.'
    else:
        desc = f'{n} PT chart: saturation pressure for every temperature in \u00b0F and \u00b0C, psig and kPa. Two-way lookup, printable table, safety class and GWP.'
    if len(desc) > 158:
        desc = desc[:157].rsplit(' ', 1)[0] + '.'
    if e40d is not None:
        if r['blend']:
            lead = (f'<p class="lead">At 40 \u00b0F, {n} has a <b>dew pressure of {ps(e40d)} psig</b> and a bubble pressure of {ps(e40b)} psig '
                    f'(temperature glide about {g40:.1f} \u00b0F). At 100 \u00b0F the bubble (liquid) pressure is {ps(c100)} psig. '
                    f'Use the lookup below for any temperature or pressure, or scroll to the full chart in \u00b0F and \u00b0C.</p>')
        else:
            lead = (f'<p class="lead">At 40 \u00b0F, {n} has a <b>saturation pressure of {ps(e40b)} psig</b>; at 100 \u00b0F it is {ps(c100)} psig. '
                    f'Use the lookup below for any temperature or pressure, or scroll to the full chart in \u00b0F and \u00b0C.</p>')
    else:
        lead = f'<p class="lead">Saturation pressures for {n} from {r["t"][0]} to {r["t"][-1]} \u00b0F.</p>'
    facts = [('Refrigerant', n), ('Type', esc(r['kind'])), ('Composition (mass %)', esc(r['composition'])),
             ('ASHRAE safety group', r['safety']), ('Global warming potential', gwp_text(r)),
             ('Common trade names', esc(r['trade'])), ('Typical use', esc(r['uses']))]
    if nb is not None:
        if r['blend']:
            facts.append(('Bubble / dew point at 0 psig (sea level)', f'{nb:.1f} \u00b0F / {nd:.1f} \u00b0F'))
        else:
            facts.append(('Boiling point at 0 psig (sea level)', f'{nb:.1f} \u00b0F ({c_of(nb):.1f} \u00b0C)'))
    if r['tcrit_f']:
        facts.append(('Critical temperature', f"{r['tcrit_f']:.1f} \u00b0F"))
    if g40 is not None and r['blend']:
        facts.append(('Temperature glide at 40 \u00b0F bubble pressure', f'{g40:.1f} \u00b0F'))
    facts.append(('Data source', 'DuPont/Chemours MO99 chart' if r['source'] == 'chart' else 'CoolProp 8 (REFPROP-equivalent EOS), checked against published charts'))
    ftable = '<div class="tblwrap"><table class="facts"><tbody>' + ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a, b in facts) + '</tbody></table></div>'
    # quick-look table
    ql = []
    for F, lab in ((20, 'Low-temp evaporator'), (35, 'Evaporator'), (40, 'Evaporator (A/C design)'), (45, 'Evaporator'), (70, 'Standing / ambient'),
                   (80, 'Standing / ambient'), (90, 'Condenser'), (100, 'Condenser'), (110, 'Condenser'), (120, 'Condenser (hot day)')):
        b, d = pf(r, F, 0), pf(r, F, 1)
        if b is None:
            continue
        ql.append((f'{F} \u00b0F ({c_of(F):.0f} \u00b0C)', lab, ps(b), ps(d)) if r['blend'] else (f'{F} \u00b0F ({c_of(F):.0f} \u00b0C)', lab, ps(b)))
    qh = ['Temperature', 'Where you see it', 'Bubble (liquid) psig', 'Dew (vapor) psig'] if r['blend'] else ['Temperature', 'Where you see it', 'Pressure psig']
    fh = ['\u00b0F', 'Bubble psig (liquid)', 'Dew psig (vapor)', '\u00b0C'] if r['blend'] else ['\u00b0F', 'psig', 'kPa (gauge)', '\u00b0C']
    ch = ['\u00b0C', 'Bubble kPa(g)', 'Dew kPa(g)', 'Bubble bar(g)', 'Dew bar(g)'] if r['blend'] else ['\u00b0C', 'kPa (gauge)', 'bar (gauge)', '\u00b0F']
    # worked example
    ex = ''
    if e40d is not None and c110 is not None:
        sat_s = pf(r, 40, 1)
        sat_l = pf(r, 105, 0)
        ex = (f'<h2>Worked example: superheat and subcooling with {n}</h2>'
              f'<p><b>Superheat.</b> Suction pressure at the service valve reads {sat_s:.0f} psig. On this chart that pressure is a '
              f'{"dew" if r["blend"] else "saturation"} temperature of about 40 \u00b0F. Your clamp thermometer on the suction line near the same point reads 52 \u00b0F, '
              f'so superheat = 52 \u2212 40 = <b>12 \u00b0F</b>. Compare it with the target from the manufacturer\u2019s charging chart or our '
              f'<a href="{url("/target-superheat-calculator/")}">target superheat calculator</a> (fixed orifice systems).</p>'
              f'<p><b>Subcooling.</b> Liquid line pressure reads {sat_l:.0f} psig, which is a {"bubble" if r["blend"] else "saturation"} temperature of about 105 \u00b0F. '
              f'The liquid line measures 95 \u00b0F, so subcooling = 105 \u2212 95 = <b>10 \u00b0F</b>. TXV and EEV systems are normally charged to the subcooling '
              f'printed on the outdoor unit\u2019s rating plate. Do the math automatically with the <a href="{url("/superheat-calculator/")}">superheat</a> and '
              f'<a href="{url("/subcooling-calculator/")}">subcooling</a> calculators.</p>')
    how = (f'<h2>How to read this {n} PT chart</h2>'
           + (f'<p>{n} is a <b>zeotropic blend</b>, so it does not boil at a single temperature for a given pressure. The <b>bubble point</b> is where the liquid starts to boil; '
              f'the <b>dew point</b> is where the last drop of liquid has evaporated. The difference is the temperature glide. Inside the evaporator the refrigerant moves from '
              f'bubble toward dew, so when you calculate <b>superheat use the dew column</b>; in the condenser it moves from dew to bubble, so for <b>subcooling use the bubble column</b>. '
              f'Using the wrong column on a high-glide blend can throw your superheat or subcooling off by several degrees and lead to an over- or under-charge.</p>'
              if r['blend'] else
              f'<p>{n} is a single-component refrigerant, so each temperature has exactly one saturation pressure. Find the measured pressure in the psig column and read the '
              f'saturated temperature beside it (or type it into the lookup above). That saturated temperature is the starting point for both superheat (suction side) and '
              f'subcooling (liquid side).</p>')
           + '<p>All pressures are <b>gauge pressures at sea level</b> (psig = psia \u2212 14.7). At high altitude a gauge zeroed to the local atmosphere reads higher than '
             'the chart for the same temperature (roughly 0.5 psi per 1,000 ft); digital manifolds with an altitude setting correct for this. Values shown in inHg vac are vacuum '
             '(below atmospheric pressure). The chart describes saturated refrigerant only; it does not tell you whether a system is correctly charged by itself.</p>')
    rel = [(pt_slug(BY[x]), f'{BY[x]["name"]} PT chart') for x in RELATED.get(s, []) if x in BY]
    comps = [c for c in COMPARISONS if s in c[:2]]
    rel += [(f'/{a}-vs-{b}/', f'{BY[a]["name"]} vs {BY[b]["name"]}') for a, b, *_ in comps]
    rel += [('/superheat-calculator/', 'Superheat calculator'), ('/subcooling-calculator/', 'Subcooling calculator'), ('/pt-chart/', 'All PT charts')]
    faqs = []
    if e40d is not None:
        faqs.append((f'What is the {n} pressure at 40 \u00b0F?',
                     f'{n} saturates at {ps(e40d)} psig (dew) and {ps(e40b)} psig (bubble) at 40 \u00b0F.' if r['blend'] else f'{n} saturates at {ps(e40b)} psig at 40 \u00b0F.'))
    if c100 is not None:
        faqs.append((f'What is the {n} pressure at 100 \u00b0F?', f'The {"bubble (liquid) " if r["blend"] else ""}saturation pressure of {n} at 100 \u00b0F is {ps(c100)} psig'
                     + (f' and the dew pressure is {ps(pf(r, 100, 1))} psig.' if r['blend'] else '.')))
    if r['blend']:
        faqs.append((f'Should I use bubble or dew for {n}?', 'Use the dew point for superheat (evaporator and suction line) and the bubble point for subcooling (condenser and liquid line). '
                     f'For {n} the glide at 40 \u00b0F is about {g40:.1f} \u00b0F.' if g40 is not None else 'Use dew for superheat and bubble for subcooling.'))
        faqs.append((f'Can I top off a leaking {n} system?', f'{n} is a blend; a vapor leak can shift its composition. Manufacturers recommend charging blends as liquid and, after a large leak, '
                     'recovering and recharging with new refrigerant. Follow the equipment manufacturer\u2019s instructions.'))
    faqs.append((f'Is {n} flammable?', {'A1': f'No. {n} is ASHRAE safety group A1 (no flame propagation). It can still displace oxygen and form toxic products in a flame.',
                 'A2L': f'{n} is ASHRAE group A2L, meaning mildly flammable with a low burning velocity. Use A2L-rated tools and follow the manufacturer\u2019s service procedures.',
                 'A3': f'Yes. {n} is ASHRAE group A3, highly flammable. Only trained technicians should service it with hydrocarbon-rated equipment.',
                 'B1': f'No, but {n} is safety group B1 (higher toxicity). Use refrigerant monitoring and PPE.',
                 'B2L': f'{n} is group B2L: higher toxicity and mildly flammable.'}[r['safety']]))
    faqs.append((f'Where does this {n} chart come from?', f'{"The DuPont/Chemours MO99 chart" if r["source"] == "chart" else "CoolProp 8, an open-source REFPROP-equivalent property library"}, checked against '
                 f'{v["points"]} points from published charts with a maximum difference of {v["max_dev_f"]:.2f} \u00b0F. Sources are listed on the page.'))
    body = f'''<article>
<h1>{esc(n)} PT Chart</h1>
{lead}
{pt_tool(r)}
<div class="actions"><button type="button" class="btn" data-print>Print chart</button> <a class="btn ghost" href="#chart-f">Jump to \u00b0F chart</a> <a class="btn ghost" href="#chart-c">\u00b0C chart</a></div>
<h2>{esc(n)} key facts</h2>
{ftable}
<p class="safety">{SAFETY[r["safety"]]}</p>
<h2>{esc(n)} pressures at common temperatures</h2>
{table(qh, ql)}
{how}
{ex}
<h2 id="chart-f">{esc(n)} pressure-temperature chart (\u00b0F, psig)</h2>
{table(fh, chart_rows_f(r), cls="data chart")}
<h2 id="chart-c">{esc(n)} pressure-temperature chart (\u00b0C, kPa and bar gauge)</h2>
{table(ch, chart_rows_c(r), cls="data chart")}
<h2>How this chart was made and checked</h2>
{source_para(r)}
<h2>Related charts and tools</h2>
{links(rel)}
{faq_html(faqs)}
</article>'''
    page(path, title, desc, body, crumbs=[('PT Charts', '/pt-chart/'), (f'{n} PT chart', path)], section='/pt-chart/',
         schema=[app_ld(f'{n} PT chart and lookup', desc, path), article_ld(title, desc, path), faq_ld(faqs)])

COMPARISONS = [
 ('r454b', 'r410a', 'r454b-vs-r410a'), ('r32', 'r454b', 'r32-vs-r454b'), ('r32', 'r410a', 'r32-vs-r410a'), ('r22', 'r410a', 'r22-vs-r410a'),
 ('r407c', 'r22', 'r407c-vs-r22'), ('r448a', 'r404a', 'r448a-vs-r404a'), ('r449a', 'r448a', 'r449a-vs-r448a'), ('r1234yf', 'r134a', 'r1234yf-vs-r134a'),
 ('r513a', 'r134a', 'r513a-vs-r134a'), ('r290', 'r134a', 'r290-vs-r134a'), ('r466a', 'r454b', 'r466a-vs-r454b'), ('r438a', 'r422d', 'r438a-vs-r422d'),
]

def comp_page(a, b, slug):
    A, Bb = BY[a], BY[b]
    path = f'/{slug}/'
    title = f'{A["name"]} vs {Bb["name"]}: Pressures, GWP & Safety Compared'
    desc = f'{A["name"]} vs {Bb["name"]} side by side: saturation pressures from 0 to 120 \u00b0F, glide, GWP, safety class and what changes when you service them.'
    if len(desc) > 159: desc = desc[:156].rsplit(' ', 1)[0] + '.'
    rows = []
    for F in (0, 20, 35, 40, 45, 70, 90, 100, 105, 110, 115, 120):
        pa = pf(A, F, 1) if A['blend'] else pf(A, F, 0)
        pb = pf(Bb, F, 1) if Bb['blend'] else pf(Bb, F, 0)
        la = pf(A, F, 0); lb = pf(Bb, F, 0)
        if None in (pa, pb, la, lb):
            continue
        rows.append((f'{F} \u00b0F', ps(pa), ps(pb), ps(la), ps(lb), f'{(la - lb):+.1f}'))
    e = lambda r, F, q: pf(r, F, q)
    d40 = (e(A, 40, 1) or 0) - (e(Bb, 40, 1) or 0)
    d100 = (e(A, 100, 0) or 0) - (e(Bb, 100, 0) or 0)
    pct = 100 * d100 / e(Bb, 100, 0)
    ga, gb = glide(A, 40), glide(Bb, 40)
    facts = [('ASHRAE safety group', A['safety'], Bb['safety']), ('GWP', gwp_text(A), gwp_text(Bb)), ('Type', esc(A['kind']), esc(Bb['kind'])),
             ('Composition (mass %)', esc(A['composition']), esc(Bb['composition'])), ('Glide at 40 \u00b0F', f'{ga:.1f} \u00b0F' if ga is not None and A['blend'] else '~0 \u00b0F',
              f'{gb:.1f} \u00b0F' if gb is not None and Bb['blend'] else '~0 \u00b0F'),
             ('Critical temperature', f"{A['tcrit_f']:.0f} \u00b0F" if A['tcrit_f'] else '\u2014', f"{Bb['tcrit_f']:.0f} \u00b0F" if Bb['tcrit_f'] else '\u2014'),
             ('Typical use', esc(A['uses']), esc(Bb['uses']))]
    ft = '<div class="tblwrap"><table class="data"><thead><tr><th scope="col">Property</th><th scope="col">' + A['name'] + '</th><th scope="col">' + Bb['name'] + '</th></tr></thead><tbody>' + ''.join(
        f'<tr><th scope="row">{x}</th><td>{y}</td><td>{z}</td></tr>' for x, y, z in facts) + '</tbody></table></div>'
    higher = 'higher' if d100 > 0 else 'lower'
    swap = ''
    if {a, b} & {'r454b', 'r32', 'r466a'} and {a, b} & {'r410a'}:
        swap = (f'<p><b>Can you put {A["name"]} in an {Bb["name"]} system?</b> No. A2L and other R-410A replacements are approved for <em>new equipment designed for them</em>, '
                'with matching compressors, oils, metering devices, leak-detection and mitigation controls. Never retrofit a system to a different refrigerant unless the equipment '
                'manufacturer specifically allows it.</p>')
    elif {a, b} == {'r22', 'r410a'}:
        swap = ('<p><b>Can R-410A go into an R-22 system?</b> No. R-410A runs at roughly 60% higher pressures and uses POE oil; R-22 equipment is not rated for it. '
                'R-22 systems are serviced with reclaimed R-22 or an approved retrofit blend such as R-407C, R-422D, R-427A or R-438A, following the blend maker\u2019s retrofit guide.</p>')
    else:
        swap = (f'<p><b>Is {A["name"]} a drop-in for {Bb["name"]}?</b> Treat no refrigerant as a pure drop-in. Some blends are approved retrofits, but oil, seals, metering '
                'devices, pressure controls and charge amount may change. Follow the refrigerant producer\u2019s retrofit guidelines and the equipment manufacturer.</p>')
    faqs = [(f'Does {A["name"]} run at higher pressure than {Bb["name"]}?', f'At a 100 \u00b0F condensing temperature {A["name"]} is about {abs(d100):.0f} psi {higher} '
             f'({pct:+.0f}%) than {Bb["name"]}; at a 40 \u00b0F evaporator the dew pressures differ by {d40:+.1f} psi.'),
            (f'Which is safer, {A["name"]} or {Bb["name"]}?', f'{A["name"]} is ASHRAE group {A["safety"]} and {Bb["name"]} is group {Bb["safety"]}. '
             'A1 = no flame propagation, A2L = mildly flammable, A3 = highly flammable, B = higher toxicity.'),
            (f'Can I mix {A["name"]} and {Bb["name"]}?', 'No. Never mix refrigerants. Mixed refrigerant cannot be charged correctly or reclaimed normally and must be recovered as contaminated refrigerant.')]
    body = f'''<article>
<h1>{A["name"]} vs {Bb["name"]}</h1>
<p class="lead">At 100 \u00b0F condensing, {A["name"]} sits at <b>{ps(e(A, 100, 0))} psig</b> versus <b>{ps(e(Bb, 100, 0))} psig</b> for {Bb["name"]} ({pct:+.0f}%). At a 40 \u00b0F evaporator the
{"dew " if A["blend"] or Bb["blend"] else ""}pressures are {ps(e(A, 40, 1))} and {ps(e(Bb, 40, 1))} psig. {A["name"]} is safety group {A["safety"]}, {Bb["name"]} is {Bb["safety"]}.</p>
<h2>Side-by-side pressure table</h2>
<p>Suction-side columns use the dew pressure (what you compare with superheat); liquid-side columns use the bubble pressure (what you compare with subcooling). For single-component refrigerants both are the same.</p>
{table(["Saturation temp", A["name"] + " dew psig", Bb["name"] + " dew psig", A["name"] + " bubble psig", Bb["name"] + " bubble psig", "Bubble difference, psi"], rows)}
<h2>Properties compared</h2>
{ft}
<h2>What changes in the field</h2>
<p><b>Gauges and hoses.</b> {"The pressures are close enough that the same high-pressure gauges and hoses work, but you must switch to the matching PT scale or refrigerant setting on your digital manifold." if abs(pct) < 15 else "The pressure levels are clearly different, so use gauges, hoses and recovery cylinders rated for the higher-pressure refrigerant and select the right refrigerant on your manifold."}</p>
<p><b>Glide.</b> {"Both refrigerants have little or no glide." if not (A["blend"] and (ga or 0) > 1) and not (Bb["blend"] and (gb or 0) > 1) else "At least one of these is a zeotropic blend with measurable glide: read superheat from the dew column and subcooling from the bubble column, and charge blends as liquid."}</p>
<p><b>Flammability.</b> {SAFETY[A["safety"]] if A["safety"] != "A1" else SAFETY[Bb["safety"]] if Bb["safety"] != "A1" else "Both are A1 (no flame propagation), so no flammable-refrigerant procedures are needed, but standard refrigerant safety still applies."}</p>
{swap}
<h2>Service checklist when you work on both</h2>
<ul><li>Confirm the refrigerant on the rating plate before connecting gauges; never rely on cylinder color or memory.</li>
<li>Use separate recovery cylinders for each refrigerant and label them; mixed refrigerant cannot be reclaimed normally.</li>
<li>Check that your recovery machine, vacuum pump and leak detector are rated for {"A2L " if "A2L" in (A["safety"], Bb["safety"]) else ""}{A["name"]} and {Bb["name"]}.</li>
<li>Charge {"blends as liquid and " if A["blend"] or Bb["blend"] else ""}by weight to the nameplate charge, then confirm with superheat or subcooling.</li>
<li>Read pressures against the right PT chart; at 100 \u00b0F condensing the two differ by {abs(d100):.0f} psi.</li></ul>
<h2>Full charts</h2>
{links([(pt_slug(A), A["name"] + " PT chart"), (pt_slug(Bb), Bb["name"] + " PT chart"), ("/superheat-calculator/", "Superheat calculator"), ("/subcooling-calculator/", "Subcooling calculator"), ("/pt-chart/", "All PT charts")])}
<h2>Sources</h2>
<p>Pressures: {A["name"]} and {Bb["name"]} tables on this site (see each chart\u2019s verification section; maximum deviation from published charts {VER[a]["max_dev_f"]:.2f} \u00b0F and {VER[b]["max_dev_f"]:.2f} \u00b0F). GWP values: IPCC AR4 as listed by the UNEP Ozone Secretariat where marked; safety groups: ASHRAE Standard 34.</p>
{faq_html(faqs)}
</article>'''
    page(path, title, desc, body, crumbs=[('PT Charts', '/pt-chart/'), (f'{A["name"]} vs {Bb["name"]}', path)], section='/pt-chart/',
         schema=[article_ld(title, desc, path), faq_ld(faqs)])

def calc_select():
    opts = ''.join(f'<option value="{r["slug"]}"{" selected" if r["slug"] == "r410a" else ""}>{r["name"]}</option>' for r in sorted(REFS, key=lambda x: x['name']))
    return f'<select data-ref>{opts}</select>'

def hvac_pages():
    for r in REFS:
        pt_page(r)
    for a, b, s in COMPARISONS:
        comp_page(a, b, s)
    # all-refrigerant data file for calculators
    allj = {r['slug']: {'n': r['name'], 't0': r['t'][0], 'b': r['b'], 'd': r['d'], 'bl': r['blend']} for r in REFS}
    os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
    json.dump(allj, open(os.path.join(OUT, 'assets', 'pt-all.json'), 'w'), separators=(',', ':'))
    # PT hub
    groups = ''
    for g, sl in GROUP.items():
        rows = []
        for x in sl:
            r = BY[x]
            rows.append((f'<a href="{url(pt_slug(r))}">{r["name"]}</a>', r['safety'], r['gwp'], ps(pf(r, 40, 1)), ps(pf(r, 100, 0)), esc(r['trade'].split(',')[0])))
        groups += f'<h2>{g}</h2>' + table(['Refrigerant', 'Safety', 'GWP', '40 \u00b0F dew psig', '100 \u00b0F bubble psig', 'Trade name'], rows)
    faqs = [('What is a PT chart?', 'A pressure-temperature (PT) chart lists the saturation pressure of a refrigerant at each temperature. Technicians use it to convert gauge pressure into the saturated temperature needed for superheat and subcooling.'),
            ('Why do some charts have two pressure columns?', 'Zeotropic blends such as R-454B, R-407C and R-448A boil over a temperature range (glide). The bubble column is used for subcooling and the dew column for superheat.'),
            ('Are these PT charts accurate?', 'Each chart is computed with a REFPROP-equivalent equation of state (or taken from the manufacturer chart for R-438A) and checked against published manufacturer and NIST data; every chart page shows how many points were compared and the largest difference.'),
            ('Are the pressures gauge or absolute?', 'Gauge pressure at sea level (psig). Vacuum values are shown in inches of mercury.')]
    body = f'''<article><h1>Refrigerant PT Charts</h1>
<p class="lead">Pick a refrigerant for its full pressure-temperature chart in \u00b0F and \u00b0C, bubble and dew columns for blends, and a two-way lookup. Or use the quick lookup here for any of the {len(REFS)} refrigerants.</p>
<section class="tool"><h2>Quick PT lookup (all refrigerants)</h2>
<div class="pt" data-tool="pt-any"><div class="row"><label>Refrigerant {calc_select()}</label></div>
<div class="seg" role="group" aria-label="Lookup direction"><button type="button" data-mode="t2p" aria-pressed="true">Temp &rarr; Pressure</button><button type="button" data-mode="p2t" aria-pressed="false">Pressure &rarr; Temp</button></div>
<div class="row"><label>Value <input type="number" inputmode="decimal" step="any" data-in value="40"></label>
<label class="u-t">Temp unit <select data-tu><option value="F">\u00b0F</option><option value="C">\u00b0C</option></select></label>
<label class="u-p" hidden>Pressure unit <select data-pu><option value="psig">psig</option><option value="kpa">kPa (gauge)</option><option value="bar">bar (gauge)</option></select></label></div>
<output class="res" data-out aria-live="polite"></output></div></section>
{groups}
<h2>How to use a PT chart</h2>
<p>Read the pressure on your gauge, find it on the chart for the refrigerant in the system, and read the saturated temperature. On the suction side subtract that temperature from the measured suction-line temperature to get superheat; on the liquid side subtract the measured liquid-line temperature from the saturated temperature to get subcooling. For zeotropic blends use the dew column for superheat and the bubble column for subcooling. Our <a href="{url('/blog/how-to-read-a-pt-chart/')}">step-by-step guide</a> walks through both with numbers.</p>
<p>All charts on this site share the same layout, units toggle and print style, so a printed set makes a compact truck reference. Pressures are sea-level gauge values.</p>
<h2>Refrigerant comparisons</h2>
{links([(f'/{s}/', f'{BY[a]["name"]} vs {BY[b]["name"]}') for a, b, s in COMPARISONS])}
<h2>Calculators</h2>
{links([('/superheat-calculator/', 'Superheat calculator'), ('/subcooling-calculator/', 'Subcooling calculator'), ('/target-superheat-calculator/', 'Target superheat calculator')])}
<h2>Not listed here</h2>
<p>We publish a chart only after it matches published manufacturer or NIST data within 1 \u00b0F. R-454C, R-452B and R-502 are not listed yet because we could not verify them to that standard; use the manufacturer\u2019s chart for those.</p>
{faq_html(faqs)}
</article>'''
    page('/pt-chart/', 'Refrigerant PT Charts: 32 Pressure-Temperature Tables', 'Free refrigerant PT charts for R-454B, R-32, R-410A, R-22, R-134a, R-404A, R-448A and 25 more. Bubble/dew, \u00b0F/\u00b0C, psig/kPa, printable.',
         body, crumbs=[('PT Charts', '/pt-chart/')], section='/pt-chart/', schema=[app_ld('Refrigerant PT chart lookup', 'Two-way PT lookup for 32 refrigerants', '/pt-chart/'), faq_ld(faqs)])
    calc_pages()

def calc_pages():
    sel = calc_select()
    unit_p = '<select data-pu><option value="psig">psig</option><option value="kpa">kPa (gauge)</option><option value="bar">bar (gauge)</option></select>'
    unit_t = '<select data-tu><option value="F">\u00b0F</option><option value="C">\u00b0C</option></select>'
    # superheat
    sh_rows = []
    for x in ('r410a', 'r454b', 'r32', 'r22', 'r407c', 'r134a', 'r404a', 'r448a'):
        r = BY[x]
        sh_rows.append((r['name'], ps(pf(r, 35, 1)), ps(pf(r, 40, 1)), ps(pf(r, 45, 1))))
    faqs = [('What is superheat?', 'Superheat is how many degrees the suction vapor is above its saturation (boiling) temperature at the measured pressure: line temperature minus saturated (dew) temperature.'),
            ('What is a normal superheat?', 'It depends on the metering device and conditions. TXV systems usually hold roughly 8\u201312 \u00b0F at the evaporator outlet; fixed-orifice systems need a target that changes with indoor wet bulb and outdoor temperature. Always use the manufacturer\u2019s charging chart.'),
            ('Where do I measure superheat?', 'Measure suction pressure and suction-line temperature at the same point, usually near the outdoor unit service valve for total superheat, with the system running at least 15 minutes.'),
            ('Which column do I use for a blend like R-454B?', 'The dew column. Superheat is measured from the dew point.')]
    body = f'''<article><h1>Superheat Calculator</h1>
<p class="lead">Enter the refrigerant, the suction pressure and the suction-line temperature. The calculator converts pressure to the saturated (dew) temperature from our verified PT data and gives superheat instantly, in \u00b0F or \u00b0C.</p>
<section class="tool"><h2>Calculate superheat</h2>
<div class="calc" data-tool="sh"><div class="row"><label>Refrigerant {sel}</label></div>
<div class="row"><label>Suction pressure <input type="number" inputmode="decimal" step="any" data-p value="118"></label><label>Pressure unit {unit_p}</label></div>
<div class="row"><label>Suction line temp <input type="number" inputmode="decimal" step="any" data-t value="52"></label><label>Temp unit {unit_t}</label></div>
<output class="res" data-out aria-live="polite"></output></div></section>
<h2>How superheat is calculated</h2>
<p><b>Superheat = suction line temperature \u2212 saturated suction temperature.</b> The saturated temperature comes from the PT chart at the measured suction pressure. For zeotropic blends (R-454B, R-407C, R-448A, R-449A and others) the calculator uses the <em>dew</em> temperature, because the refrigerant leaving the evaporator has finished boiling at the dew point.</p>
<p>Example with R-410A: suction pressure 118 psig is a 40 \u00b0F saturated temperature. A suction line at 52 \u00b0F gives 52 \u2212 40 = 12 \u00b0F of superheat.</p>
<h2>Good measurement practice</h2>
<ul><li>Let the system run 15 minutes or more with doors closed and filters clean before you judge the charge.</li>
<li>Clamp the thermometer on clean bare copper within a few inches of the pressure port and insulate it from ambient air.</li>
<li>On fixed-orifice (piston) systems compare the result with a target from indoor wet bulb and outdoor dry bulb, such as our <a href="{url('/target-superheat-calculator/')}">target superheat calculator</a> or the manufacturer\u2019s table.</li>
<li>On TXV/EEV systems superheat is controlled by the valve; charge by <a href="{url('/subcooling-calculator/')}">subcooling</a> unless the manufacturer says otherwise.</li>
<li>Low superheat risks liquid floodback to the compressor; high superheat suggests low charge, a restriction or low airflow on the heat-transfer side.</li></ul>
<h2>What high or low superheat usually means</h2>
{table(['Reading', 'Common causes to check first'], [('High superheat', 'Low charge or leak, restricted metering device or filter drier, low indoor load, kinked line'), ('Low superheat', 'Overcharge (fixed orifice), low indoor airflow (dirty filter or coil, slow blower), TXV bulb loose or overfeeding'), ('Superheat swinging', 'TXV hunting, very low load, intermittent restriction or moisture')])}
<h2>Saturated suction pressures (dew) for common refrigerants</h2>
{table(['Refrigerant', '35 \u00b0F', '40 \u00b0F', '45 \u00b0F'], sh_rows)}
<p>Full tables: <a href="{url('/pt-chart/')}">all PT charts</a>.</p>
{faq_html(faqs)}
</article>'''
    page('/superheat-calculator/', 'Superheat Calculator: R-410A, R-454B, R-32, R-22 & More', 'Free superheat calculator for 32 refrigerants. Enter suction pressure and line temperature; uses dew point for blends. \u00b0F/\u00b0C and psig/kPa.',
         body, crumbs=[('HVAC Calcs', '/hvac-calculators/'), ('Superheat calculator', '/superheat-calculator/')], section='/hvac-calculators/',
         schema=[app_ld('Superheat calculator', 'Superheat from suction pressure and line temperature', '/superheat-calculator/'), faq_ld(faqs)])
    # subcooling
    sc_rows = []
    for x in ('r410a', 'r454b', 'r32', 'r22', 'r407c', 'r134a', 'r404a', 'r448a'):
        r = BY[x]
        sc_rows.append((r['name'], ps(pf(r, 95, 0)), ps(pf(r, 105, 0)), ps(pf(r, 115, 0))))
    faqs = [('What is subcooling?', 'Subcooling is how many degrees the liquid refrigerant is below its saturation (bubble) temperature: saturated liquid temperature minus liquid-line temperature.'),
            ('What should subcooling be?', 'Use the target printed on the outdoor unit or in the installation manual. Many residential TXV systems specify roughly 8\u201312 \u00b0F, but the rating plate value rules.'),
            ('Which column do I use for a blend?', 'The bubble column: subcooling is measured from the bubble point, where the refrigerant is fully condensed.'),
            ('Where do I measure subcooling?', 'Take liquid-line pressure and temperature at the same point, usually at the liquid service valve of the outdoor unit.')]
    body = f'''<article><h1>Subcooling Calculator</h1>
<p class="lead">Enter the refrigerant, liquid-line pressure and liquid-line temperature. The calculator finds the saturated (bubble) temperature from verified PT data and returns the subcooling.</p>
<section class="tool"><h2>Calculate subcooling</h2>
<div class="calc" data-tool="sc"><div class="row"><label>Refrigerant {sel}</label></div>
<div class="row"><label>Liquid pressure <input type="number" inputmode="decimal" step="any" data-p value="340"></label><label>Pressure unit {unit_p}</label></div>
<div class="row"><label>Liquid line temp <input type="number" inputmode="decimal" step="any" data-t value="95"></label><label>Temp unit {unit_t}</label></div>
<output class="res" data-out aria-live="polite"></output></div></section>
<h2>How subcooling is calculated</h2>
<p><b>Subcooling = saturated condensing temperature \u2212 liquid line temperature.</b> The saturated condensing temperature is read from the PT chart at the measured liquid pressure. For blends the calculator uses the <em>bubble</em> temperature.</p>
<p>Example with R-410A: liquid pressure 340 psig is about 105 \u00b0F saturated. A liquid line at 95 \u00b0F gives 105 \u2212 95 = 10 \u00b0F of subcooling.</p>
<h2>Reading the result</h2>
<ul><li><b>Below target:</b> often low charge, but also check for a dirty condenser coil, a restriction or a TXV that is overfeeding.</li>
<li><b>Above target:</b> often overcharge, or a restriction upstream of the metering device holding liquid back in the condenser.</li>
<li>Always confirm with superheat and airflow before adding or removing refrigerant, and weigh the charge when the manufacturer gives a line-length adjustment.</li></ul>
<h2>Good measurement practice</h2>
<ul><li>Measure at the liquid service valve with the system stable for at least 15 minutes and the outdoor coil clean.</li><li>Use an insulated pipe clamp on clean copper; a reading taken in direct sun or on a dirty line will be off.</li><li>On heat pumps in heating mode, follow the manufacturer: many specify weighing in the charge rather than charging by subcooling.</li><li>For long line sets, add or remove refrigerant per the installation manual\u2019s per-foot adjustment.</li></ul>
<h2>Saturated liquid pressures (bubble) for common refrigerants</h2>
{table(['Refrigerant', '95 \u00b0F', '105 \u00b0F', '115 \u00b0F'], sc_rows)}
{faq_html(faqs)}
</article>'''
    page('/subcooling-calculator/', 'Subcooling Calculator: Liquid Pressure to Subcool (\u00b0F/\u00b0C)', 'Free subcooling calculator for R-410A, R-454B, R-32, R-22 and 28 more. Uses the bubble point for blends. Enter liquid pressure and line temperature.',
         body, crumbs=[('HVAC Calcs', '/hvac-calculators/'), ('Subcooling calculator', '/subcooling-calculator/')], section='/hvac-calculators/',
         schema=[app_ld('Subcooling calculator', 'Subcooling from liquid pressure and line temperature', '/subcooling-calculator/'), faq_ld(faqs)])
    # target superheat
    trows = []
    for wb in (56, 60, 64, 68, 72):
        cells = [f'{wb} \u00b0F WB']
        for db in (70, 80, 90, 100, 110):
            v = (3 * wb - 80 - db) / 2
            cells.append(f'{v:.0f}' if v >= 5 else 'below 5 \u2014 see notes')
        trows.append(cells)
    faqs = [('What is target superheat?', 'The superheat a fixed-orifice (piston or capillary) system should have at current indoor wet-bulb and outdoor dry-bulb temperatures when correctly charged.'),
            ('What formula does this calculator use?', 'Target superheat \u2248 (3 \u00d7 indoor wet bulb \u2212 80 \u2212 outdoor dry bulb) \u00f7 2, a widely used approximation of manufacturers\u2019 fixed-orifice charging tables. The equipment manufacturer\u2019s chart always takes priority.'),
            ('Does target superheat apply to TXV systems?', 'No. TXV and electronic expansion valve systems are charged by subcooling; the valve controls superheat.'),
            ('Why does the result say below 5 \u00b0F?', 'At hot outdoor and dry indoor conditions the formula gives very low numbers. Many manufacturers say not to charge by superheat there; check airflow and use the manufacturer method.')]
    body = f'''<article><h1>Target Superheat Calculator</h1>
<p class="lead">For fixed-orifice (piston) A/C systems: enter indoor wet bulb at the return and outdoor dry bulb at the condenser inlet to get the approximate target superheat. Then compare with your measured superheat.</p>
<section class="tool"><h2>Calculate target superheat</h2>
<div class="calc" data-tool="tsh"><div class="row"><label>Indoor wet bulb (\u00b0F) <input type="number" inputmode="decimal" step="any" data-wb value="63"></label>
<label>Outdoor dry bulb (\u00b0F) <input type="number" inputmode="decimal" step="any" data-db value="85"></label>
<label>Measured superheat (\u00b0F, optional) <input type="number" inputmode="decimal" step="any" data-sh></label></div>
<output class="res" data-out aria-live="polite"></output></div></section>
<h2>How the target is estimated</h2>
<p>Fixed metering devices cannot adjust to load, so the correct superheat changes with the heat load on the evaporator (indoor wet bulb) and the condensing conditions (outdoor dry bulb). Manufacturers publish a charging table for each unit. A widely used approximation of those tables is:</p>
<p class="formula">Target superheat \u2248 (3 \u00d7 WB<sub>indoor</sub> \u2212 80 \u2212 DB<sub>outdoor</sub>) \u00f7 2</p>
<p>Example: 63 \u00b0F indoor wet bulb and 85 \u00b0F outdoor: (189 \u2212 80 \u2212 85) \u00f7 2 = 12 \u00b0F. If you measure 20 \u00b0F superheat the system is likely undercharged or short on indoor airflow-related load; if you measure 5 \u00b0F it may be overcharged or have low indoor airflow. Correct airflow first (typically about 400 CFM per ton unless the manufacturer specifies otherwise), then adjust charge in small steps and let the system settle.</p>
<h2>Approximate target superheat table (\u00b0F)</h2>
{table(['Indoor WB \\ Outdoor DB', '70 \u00b0F', '80 \u00b0F', '90 \u00b0F', '100 \u00b0F', '110 \u00b0F'], trows)}
<p>Results below about 5 \u00b0F are not shown because charging by superheat at those conditions risks floodback; follow the manufacturer\u2019s procedure.</p>
<p>Measure actual superheat with the <a href="{url('/superheat-calculator/')}">superheat calculator</a>.</p>
{faq_html(faqs)}
</article>'''
    page('/target-superheat-calculator/', 'Target Superheat Calculator for Fixed-Orifice A/C', 'Target superheat from indoor wet bulb and outdoor dry bulb for piston/fixed-orifice systems, with a quick table and a check against your measured superheat.',
         body, crumbs=[('HVAC Calcs', '/hvac-calculators/'), ('Target superheat', '/target-superheat-calculator/')], section='/hvac-calculators/',
         schema=[app_ld('Target superheat calculator', 'Target superheat for fixed orifice systems', '/target-superheat-calculator/'), faq_ld(faqs)])
    # HVAC calcs hub
    body = f'''<article><h1>HVAC Calculators</h1>
<p class="lead">Field calculators that run in your browser, work offline once loaded, and use the same verified refrigerant data as our PT charts.</p>
{links([('/superheat-calculator/', 'Superheat calculator'), ('/subcooling-calculator/', 'Subcooling calculator'), ('/target-superheat-calculator/', 'Target superheat calculator (fixed orifice)'), ('/pt-chart/', 'PT chart lookup (32 refrigerants)')])}
<h2>Which calculator do I need?</h2>
<p><b>TXV or EEV system:</b> charge by subcooling at the value on the rating plate, then confirm superheat is reasonable. <b>Fixed orifice / piston:</b> charge by superheat against a target that depends on indoor wet bulb and outdoor dry bulb. In every case, make sure airflow and coil condition are right before touching the charge, and weigh in the charge when installing.</p>
<h2>Refrigerant comparisons</h2>
{links([(f'/{s}/', f'{BY[a]["name"]} vs {BY[b]["name"]}') for a, b, s in COMPARISONS])}
</article>'''
    page('/hvac-calculators/', 'HVAC Calculators: Superheat, Subcooling, Target SH', 'Free HVAC field calculators: superheat, subcooling and target superheat for 32 refrigerants, plus refrigerant comparisons. Fast, no sign-up.',
         body, crumbs=[('HVAC Calcs', '/hvac-calculators/')], section='/hvac-calculators/')
