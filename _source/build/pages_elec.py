"""Electrical reference pages: conduit fill, ampacity, voltage drop, offsets, box fill."""
import json, os, math
from core import *

E = json.load(open(os.path.join(HERE, 'data', 'electrical.json')))
CT = {'EMT': ('EMT', 'Electrical Metallic Tubing (EMT)', 'emt-conduit-fill-chart', 'NEC Article 358'),
      'PVC-40': ('PVC Schedule 40', 'Rigid PVC Schedule 40 (and HDPE)', 'pvc-conduit-fill-chart', 'NEC Articles 352/353'),
      'PVC-80': ('PVC Schedule 80', 'Rigid PVC Schedule 80', 'pvc-schedule-80-conduit-fill-chart', 'NEC Article 352'),
      'RMC': ('Rigid (RMC)', 'Rigid Metal Conduit (RMC / GRC)', 'rigid-conduit-fill-chart', 'NEC Article 344'),
      'IMC': ('IMC', 'Intermediate Metal Conduit (IMC)', 'imc-conduit-fill-chart', 'NEC Article 342'),
      'FMC': ('Flex (FMC)', 'Flexible Metal Conduit (FMC)', 'flex-conduit-fill-chart', 'NEC Article 348'),
      'LFMC': ('Liquid-tight (LFMC)', 'Liquidtight Flexible Metal Conduit (LFMC)', 'liquid-tight-conduit-fill-chart', 'NEC Article 350')}
SIZES = ['14', '12', '10', '8', '6', '4', '3', '2', '1', '1/0', '2/0', '3/0', '4/0', '250', '300', '350', '400', '500']
SRC9 = 'NEC (NFPA 70) Chapter 9, Table 1 (fill percentages), Table 4 (conduit areas) and Table 5 (conductor areas)'

def awg(s):
    return f'{s} kcmil' if s.isdigit() and int(s) >= 250 else f'{s} AWG'

def maxfill(area, w):
    """max same-size conductors: Chapter 9 Note 7 lets you round up when the decimal is 0.8 or more (applies when all same size)."""
    if w > 0.53 * area:
        return 0
    if w <= 0.31 * area / 2 * 2 and w * 2 <= 0.31 * area:
        pass
    n40 = 0.40 * area / w
    n = math.floor(n40)
    if n40 - n >= 0.8:
        n += 1
    if n >= 3:
        return n
    if 2 * w <= 0.31 * area:
        return 2
    return 1

def fill_table(typ, wt='THHN'):
    c = E['conduit'][typ]
    sizes = list(c.keys())
    rows = []
    for s in SIZES:
        w = E['wire_area'][wt].get(s)
        if not w:
            continue
        rows.append([awg(s)] + [str(maxfill(c[z]['area'], w)) for z in sizes])
    return ['Conductor'] + [f'{z}"' for z in sizes], rows

FILL_TOOL = '''<section class="tool"><h2>Conduit fill calculator</h2>
<div class="calc" data-tool="fill" data-type="{typ}">
<div class="row"><label>Conduit type <select data-ct>{opts}</select></label><label>Trade size <select data-cs></select></label></div>
<div class="wires" data-wires></div>
<button type="button" class="btn ghost" data-add>+ Add conductors</button>
<output class="res" data-out aria-live="polite"></output>
</div></section>'''

def fill_tool(typ='EMT'):
    opts = ''.join(f'<option value="{k}"{" selected" if k == typ else ""}>{v[0]}</option>' for k, v in CT.items())
    return FILL_TOOL.format(typ=typ, opts=opts)

def conduit_type_page(typ):
    short, full, slug, art = CT[typ]
    path = f'/{slug}/'
    h, rows = fill_table(typ)
    hx, rowsx = fill_table(typ, 'XHHW')
    c = E['conduit'][typ]
    arows = [(f'{z}"', f"{v['id_in']:.3f}", f"{v['area']:.3f}", f"{v['a53']:.3f}", f"{v['a31']:.3f}", f"{v['a40']:.3f}") for z, v in c.items()]
    s34 = c.get('3/4')
    ex = ''
    if s34:
        n12 = maxfill(s34['area'], E['wire_area']['THHN']['12'])
        ex = (f'<p><b>Example.</b> How many 12 AWG THHN fit in 3/4" {short}? The 40% fill area of 3/4" {short} is {s34["a40"]:.3f} in\u00b2 and one 12 AWG THHN is '
              f'{E["wire_area"]["THHN"]["12"]} in\u00b2, so {s34["a40"]:.3f} \u00f7 {E["wire_area"]["THHN"]["12"]} = {s34["a40"] / E["wire_area"]["THHN"]["12"]:.2f}. '
              f'Chapter 9 Note 7 allows rounding up only when the decimal is 0.8 or more, so the answer is <b>{n12} conductors</b>.</p>')
    title = f'{short} Conduit Fill Chart: Max THHN & XHHW Wires by Size'
    desc = f'{short} conduit fill chart per NEC Chapter 9: max THHN/THWN-2 and XHHW wires for every trade size, internal areas, plus a mixed-wire fill calculator.'
    if len(desc) > 159: desc = desc[:156].rsplit(' ', 1)[0] + '.'
    faqs = [(f'How many 12 AWG wires fit in 3/4" {short}?', f'{maxfill(s34["area"], E["wire_area"]["THHN"]["12"])} THHN/THWN-2 conductors at 40% fill.' if s34 else 'See the chart above.'),
            ('What is the 40% conduit fill rule?', 'NEC Chapter 9 Table 1 limits fill to 53% for one conductor, 31% for two and 40% for three or more conductors of the cross-sectional area of the raceway.'),
            ('Do ground wires count in conduit fill?', 'Yes. Equipment grounding and bonding conductors, insulated or bare, are included when calculating fill (Chapter 9, Note 3).'),
            ('Does conduit fill account for ampacity derating?', 'No. With more than three current-carrying conductors you must also apply the adjustment factors of NEC 310.15(C)(1), which may require larger wire.')]
    body = f'''<article><h1>{short} Conduit Fill Chart</h1>
<p class="lead">{full}: maximum number of same-size conductors allowed in {short} under NEC Chapter 9 ({art}). Values follow the 40% rule for three or more conductors and the Note 7 round-up rule; use the calculator for mixed sizes.</p>
{fill_tool(typ)}
<h2>{short}: maximum THHN / THWN / THWN-2 conductors</h2>
{table(h, rows, cls="data chart")}
{ex}
<h2>{short}: maximum XHHW / XHHW-2 conductors</h2>
{table(hx, rowsx, cls="data chart")}
<h2>{short} internal dimensions and allowable fill areas</h2>
{table(['Trade size', 'Internal dia. (in)', '100% area (in\u00b2)', '1 wire 53% (in\u00b2)', '2 wires 31% (in\u00b2)', '3+ wires 40% (in\u00b2)'], arows)}
<h2>How conduit fill is calculated</h2>
<p>Add up the cross-sectional area of every conductor from Chapter 9 Table 5 (including the equipment grounding conductor), then compare the total with the allowable area of the raceway from Table 4: 53% of the internal area for a single conductor, 31% for two, 40% for three or more. When every conductor is the same size, divide the 40% area by one conductor\u2019s area; Note 7 lets you round up if the remainder is 0.8 or more. Nipples 24 inches or shorter may be filled to 60% (Note 4).</p>
<p>Other wire types (TW, THW, RHH, bare conductors, cables) have different areas, so use the calculator with the closest type or the actual manufacturer diameter. Fill is only one check: also verify ampacity adjustment for more than three current-carrying conductors and the bending space at pull points.</p>
<h2>Other raceways</h2>
{links([(f'/{v[2]}/', f'{v[0]} fill chart') for k, v in CT.items() if k != typ] + [('/conduit-fill-calculator/', 'Conduit fill calculator'), ('/wire-ampacity-chart/', 'Wire ampacity chart')])}
<h2>Source</h2>
<p>{SRC9}. Areas are the NEC tabulated values (unchanged in the 2017, 2020 and 2023 editions for these raceways). Confirm the edition adopted in your jurisdiction.</p>
{faq_html(faqs)}
</article>'''
    page(path, title, desc, body, crumbs=[('Electrical', '/electrical/'), (f'{short} fill chart', path)], section='/electrical/',
         schema=[app_ld(f'{short} conduit fill calculator', desc, path), article_ld(title, desc, path), faq_ld(faqs)])

def size_page(typ, size):
    short = CT[typ][0]
    c = E['conduit'][typ][size]
    path = f'/{size.replace("/", "-")}-{typ.lower().replace("pvc-40", "pvc")}-conduit-fill/'
    rows = []
    for s in SIZES:
        w = E['wire_area']['THHN'].get(s); wx = E['wire_area']['XHHW'].get(s)
        n = maxfill(c['area'], w); nx = maxfill(c['area'], wx)
        if n == 0 and nx == 0:
            continue
        rows.append((awg(s), str(n), str(nx)))
    n10 = maxfill(c['area'], E['wire_area']['THHN']['10']); n12 = maxfill(c['area'], E['wire_area']['THHN']['12'])
    title = f'{size}" {short} Conduit Fill: How Many Wires Fit? (NEC)'
    desc = f'How many wires in {size} inch {short}? {n12} \u00d7 12 AWG or {n10} \u00d7 10 AWG THHN. Full table for 14 AWG to 500 kcmil, THHN and XHHW, per NEC Chapter 9.'
    if len(desc) > 159: desc = desc[:156].rsplit(' ', 1)[0] + '.'
    mix_w = 3 * E['wire_area']['THHN']['10'] + E['wire_area']['THHN']['12']
    faqs = [(f'How many 12 AWG THHN fit in {size}" {short}?', f'{n12} conductors.'), (f'How many 10 AWG THHN fit in {size}" {short}?', f'{n10} conductors.'),
            (f'What is the 40% fill area of {size}" {short}?', f'{c["a40"]:.3f} square inches (total internal area {c["area"]:.3f} in\u00b2).')]
    body = f'''<article><h1>{size}" {short} Conduit Fill</h1>
<p class="lead">A {size}-inch {short} holds up to <b>{n12} \u00d7 12 AWG</b> or <b>{n10} \u00d7 10 AWG</b> THHN/THWN-2 conductors at the NEC 40% fill limit. Its internal area is {c["area"]:.3f} in\u00b2 (40% = {c["a40"]:.3f} in\u00b2).</p>
{fill_tool(typ)}
<h2>Maximum conductors in {size}" {short}</h2>
{table(['Conductor', 'THHN / THWN-2', 'XHHW / XHHW-2'], rows)}
<h2>Fill percentage by number of conductors</h2>
<p>How full {size}" {short} is with a given number of same-size THHN/THWN-2 conductors (limit 53% for one, 31% for two, 40% for three or more):</p>
{table(['Conductors'] + [awg(x) + ' THHN' for x in ('14', '12', '10', '8', '6')], [[str(k)] + [f"{100 * k * E['wire_area']['THHN'][x] / c['area']:.0f}%" + ('' if k * E['wire_area']['THHN'][x] <= (0.53 if k == 1 else 0.31 if k == 2 else 0.40) * c['area'] else ' \u2716') for x in ('14', '12', '10', '8', '6')] for k in (1, 2, 3, 4, 6, 9)])}
<p>\u2716 = over the NEC limit for that number of conductors.</p>
<h2>Mixed sizes example</h2>
<p>Three 10 AWG THHN plus one 12 AWG THHN ground: 3 \u00d7 {E["wire_area"]["THHN"]["10"]} + {E["wire_area"]["THHN"]["12"]} = {mix_w:.4f} in\u00b2, which is {100 * mix_w / c["area"]:.1f}% of {size}" {short}
({"within" if mix_w <= c["a40"] else "over"} the 40% limit). For mixed sizes always add the areas instead of using the same-size table.</p>
<h2>Notes</h2>
<ul><li>Counts are for conductors only. Grounding conductors count toward fill.</li><li>With more than three current-carrying conductors, apply ampacity adjustment (NEC 310.15(C)(1)).</li>
<li>A nipple of 24 in. or less may be filled to 60%.</li></ul>
{links([(f'/{CT[typ][2]}/', f'All {short} sizes'), ('/conduit-fill-calculator/', 'Conduit fill calculator'), ('/wire-ampacity-chart/', 'Wire ampacity chart')])}
<p class="src">Source: {SRC9}.</p>
{faq_html(faqs)}
</article>'''
    page(path, title, desc, body, crumbs=[('Electrical', '/electrical/'), (f'{short} fill chart', f'/{CT[typ][2]}/'), (f'{size}" {short}', path)], section='/electrical/',
         schema=[article_ld(title, desc, path), faq_ld(faqs)])
    return path, f'{size}" {short} conduit fill'

AMP_SIZES = ['14', '12', '10', '8', '6', '4', '3', '2', '1', '1/0', '2/0', '3/0', '4/0', '250', '300', '350', '400', '500', '600', '700', '750', '800', '900', '1000']
AMP_PAGES = ['14', '12', '10', '8', '6', '4', '2', '1/0', '2/0', '4/0']
OCPD = {'14': 15, '12': 20, '10': 30}

def amp_page_for(size):
    a = E['ampacity'][size]
    path = f'/{size.replace("/", "-")}-awg-wire-ampacity/' if not (size.isdigit() and int(size) >= 250) else f'/{size}-kcmil-wire-ampacity/'
    lab = awg(size)
    cu, al = a['cu'], a['al']
    title = f'{lab} Wire Ampacity: Copper & Aluminum (NEC 310.16)'
    desc = f'{lab} ampacity per NEC Table 310.16: copper {cu[0]}/{cu[1]}/{cu[2]} A at 60/75/90 \u00b0C' + (f', aluminum {al[0]}/{al[1]}/{al[2]} A' if al else '') + '. Terminal and breaker rules explained.'
    if len(desc) > 159: desc = desc[:156].rsplit(' ', 1)[0] + '.'
    oc = OCPD.get(size)
    t8 = E['t8'].get(size)
    vd = ''
    if t8:
        r = t8['cu']
        for L, I in ((50, cu[1] * 0.8), (100, cu[1] * 0.8)):
            pass
        I = round(cu[1] * 0.8)
        vd = (f'<h2>Voltage drop check for {lab} copper</h2><p>Table 8 gives {lab} stranded copper a DC resistance of {r} \u03a9 per 1,000 ft at 75 \u00b0C. At {I} A on a 240 V '
              f'single-phase circuit, a 100 ft one-way run drops about {2 * 100 * r * I / 1000:.1f} V ({100 * 2 * 100 * r * I / 1000 / 240:.1f}%). Check long runs with the '
              f'<a href="{url("/voltage-drop-calculator/")}">voltage drop calculator</a>.</p>')
    faqs = [(f'How many amps can {lab} copper carry?', f'Per NEC Table 310.16: {cu[0]} A (60 \u00b0C), {cu[1]} A (75 \u00b0C), {cu[2]} A (90 \u00b0C), before any correction or adjustment.'
             + (f' Overcurrent protection for {lab} copper is limited to {oc} A by NEC 240.4(D) in most cases.' if oc else '')),
            (f'Which column do I use for {lab}?', 'Use the column matching the lowest temperature rating among the wire, the terminals and the device. Equipment 100 A or less (or 14\u20131 AWG) is generally 60 \u00b0C unless marked 75 \u00b0C (NEC 110.14(C)). The 90 \u00b0C column is a starting point for derating only.')]
    if al:
        faqs.append((f'How many amps can {lab} aluminum carry?', f'{al[0]} A (60 \u00b0C), {al[1]} A (75 \u00b0C), {al[2]} A (90 \u00b0C) per NEC Table 310.16.'))
    rows = [('Copper', f'{cu[0]} A', f'{cu[1]} A', f'{cu[2]} A')] + ([('Aluminum / copper-clad Al', f'{al[0]} A', f'{al[1]} A', f'{al[2]} A')] if al else [])
    idx = AMP_SIZES.index(size)
    nb = [x for x in AMP_PAGES if x != size]
    body = f'''<article><h1>{lab} Wire Ampacity</h1>
<p class="lead">{lab} copper is rated <b>{cu[0]} A at 60 \u00b0C, {cu[1]} A at 75 \u00b0C and {cu[2]} A at 90 \u00b0C</b> in NEC Table 310.16{f"; aluminum is {al[0]}, {al[1]} and {al[2]} A" if al else ""}. These are base values for not more than three current-carrying conductors at 30 \u00b0C (86 \u00b0F) ambient.</p>
<h2>{lab} ampacity (NEC Table 310.16)</h2>
{table(['Conductor', '60 \u00b0C (TW, UF)', '75 \u00b0C (THWN, XHHW, THW)', '90 \u00b0C (THHN, THWN-2, XHHW-2)'], rows)}
{f'<p><b>Small-conductor rule.</b> Unless specifically permitted elsewhere in the Code, the overcurrent device protecting {lab} copper may not exceed <b>{oc} A</b> (NEC 240.4(D)), even though the table shows a higher ampacity.</p>' if oc else ''}
<h2>Picking the right column</h2>
<p>A conductor\u2019s usable ampacity is limited by the lowest-rated part of the circuit. Most breakers, panelboards and device terminals are rated 60 \u00b0C or 75 \u00b0C (NEC 110.14(C)), so a THHN conductor with a 90 \u00b0C insulation rating is usually sized from the 60 \u00b0C or 75 \u00b0C column. The 90 \u00b0C value is still useful: you may apply ambient-temperature correction and bundling adjustment factors to the 90 \u00b0C ampacity, as long as the final result does not exceed the terminal-rated column.</p>
<h2>When the base ampacity changes</h2>
<ul><li><b>Hot locations</b> (attics, rooftops, boiler rooms): apply the ambient correction factors of 310.15(B).</li>
<li><b>More than three current-carrying conductors</b> in a raceway or cable: apply 310.15(C)(1) adjustment (for example 80% for 4\u20136 conductors).</li>
<li><b>Continuous loads</b>: size the conductor and breaker for 125% of the continuous load (210.19, 215.2).</li></ul>
<h2>{lab} copper after bundling adjustment</h2>
<p>NEC 310.15(C)(1) reduces ampacity when a raceway or cable holds more than three current-carrying conductors. Applied to the 90 \u00b0C value of {cu[2]} A (THHN/THWN-2), then limited to the 75 \u00b0C terminal value of {cu[1]} A:</p>
{table(['Current-carrying conductors', 'Factor', '90 \u00b0C \u00d7 factor', 'Usable (\u2264 75 \u00b0C column)'], [(n_, f'{int(f_ * 100)}%', f'{cu[2] * f_:.1f} A', f'{min(cu[2] * f_, cu[1]):.1f} A') for n_, f_ in (('1\u20133', 1.0), ('4\u20136', 0.8), ('7\u20139', 0.7), ('10\u201320', 0.5))])}
<p>Ambient temperature correction (310.15(B)) applies on top of this when the conductors run through spaces hotter than 30 \u00b0C (86 \u00b0F).</p>
{vd}
{links([(f'/{x.replace("/", "-")}-awg-wire-ampacity/' if not (x.isdigit() and int(x) >= 250) else f'/{x}-kcmil-wire-ampacity/', f'{awg(x)} ampacity') for x in nb] + [('/wire-ampacity-chart/', 'Full ampacity chart'), ('/voltage-drop-calculator/', 'Voltage drop calculator'), ('/conduit-fill-calculator/', 'Conduit fill calculator')])}
<p class="src">Source: NEC (NFPA 70) 2023 Table 310.16, as printed in NFPA TIA 1691; 2026 edition values for these sizes are unchanged per NFPA\u2019s published TIA text. Confirm your adopted edition.</p>
{faq_html(faqs)}
</article>'''
    page(path, title, desc, body, crumbs=[('Electrical', '/electrical/'), ('Ampacity chart', '/wire-ampacity-chart/'), (lab, path)], section='/electrical/',
         schema=[article_ld(title, desc, path), faq_ld(faqs)])
    return path, f'{lab} ampacity'

def elec_pages():
    for typ in CT:
        conduit_type_page(typ)
    size_links = []
    for typ, sizes in (('EMT', ['1/2', '3/4', '1', '1-1/4', '1-1/2', '2']), ('PVC-40', ['1/2', '3/4', '1', '1-1/4'])):
        for s in sizes:
            size_links.append(size_page(typ, s))
    amp_links = [amp_page_for(s) for s in AMP_PAGES]
    # conduit fill calculator page
    faqs = [('How do I calculate conduit fill?', 'Add the Table 5 areas of all conductors (including grounds) and compare with 40% of the conduit internal area from Table 4 when there are three or more conductors.'),
            ('Can I mix wire sizes?', 'Yes. Add each conductor\u2019s area; the same-size Annex C style charts only apply when all conductors are identical.'),
            ('What about cables in conduit?', 'A multiconductor cable is treated as a single conductor using its outside diameter (Chapter 9 Note 9); an elliptical cable uses its major diameter.')]
    body = f'''<article><h1>Conduit Fill Calculator</h1>
<p class="lead">Mix any THHN/THWN-2 or XHHW-2 conductor sizes and counts in EMT, PVC Schedule 40/80, rigid, IMC, flex or liquid-tight. The calculator applies the NEC Chapter 9 53% / 31% / 40% limits and shows the smallest conduit that fits.</p>
{fill_tool('EMT')}
<h2>Rules the calculator applies</h2>
<p>Fill limits come from Chapter 9 Table 1: one conductor 53%, two conductors 31%, three or more 40% of the raceway internal area (Table 4). Conductor areas come from Table 5 for THHN/THWN/THWN-2 and XHHW/XHHW-2. Equipment grounding conductors count. The result does not include ampacity adjustment, which you must apply separately for more than three current-carrying conductors.</p>
<h2>Worked examples</h2>
<p><b>Kitchen circuits in EMT.</b> Two 20 A circuits sharing a raceway: four 12 AWG THHN plus one 12 AWG ground = 5 \u00d7 0.0133 = 0.0665 in\u00b2. 1/2" EMT allows 0.122 in\u00b2 at 40%, so 1/2" works (21.9% fill).</p>
<p><b>Subpanel feeder in PVC.</b> Three 2 AWG THHN (0.1158 in\u00b2 each) plus one 8 AWG ground (0.0366) = 0.3840 in\u00b2. 1" PVC Schedule 40 allows 0.333 in\u00b2, too small; 1-1/4" allows 0.581 in\u00b2 and works.</p>
<p><b>Condenser whip.</b> Two 10 AWG THHN plus a 10 AWG ground in 1/2" liquid-tight: 3 \u00d7 0.0211 = 0.0633 in\u00b2, within the 40% limit for 1/2" LFMC (0.125 in\u00b2).</p>
<h2>Same-size fill charts by raceway</h2>
{links([(f'/{v[2]}/', f'{v[0]} fill chart') for v in CT.values()])}
<h2>Popular sizes</h2>
{links(size_links)}
<p class="src">Source: {SRC9}.</p>
{faq_html(faqs)}
</article>'''
    page('/conduit-fill-calculator/', 'Conduit Fill Calculator (NEC Chapter 9) \u2013 Mixed Wire Sizes', 'Free NEC conduit fill calculator: mix THHN and XHHW sizes in EMT, PVC, rigid, IMC, flex or liquid-tight and get fill % and the smallest conduit that fits.',
         body, crumbs=[('Electrical', '/electrical/'), ('Conduit fill calculator', '/conduit-fill-calculator/')], section='/electrical/',
         schema=[app_ld('Conduit fill calculator', 'NEC Chapter 9 conduit fill', '/conduit-fill-calculator/'), faq_ld(faqs)])
    # ampacity chart
    rows = []
    for s in AMP_SIZES:
        a = E['ampacity'][s]
        al = a['al'] or ['\u2014'] * 3
        rows.append((awg(s), a['cu'][0], a['cu'][1], a['cu'][2], al[0], al[1], al[2]))
    faqs = [('What is NEC Table 310.16?', 'The base allowable ampacity table for insulated conductors rated up to 2000 V with not more than three current-carrying conductors in raceway, cable or earth at 30 \u00b0C ambient.'),
            ('Why is 12 AWG on a 20 A breaker if the table says 25 A?', 'NEC 240.4(D) limits overcurrent protection for 14, 12 and 10 AWG copper to 15, 20 and 30 A in most cases.'),
            ('Which temperature column should I use?', 'The lowest rating of conductor insulation, terminals and equipment. Circuits of 100 A or less generally use 60 \u00b0C unless equipment is marked 75 \u00b0C.')]
    body = f'''<article><h1>Wire Ampacity Chart (NEC Table 310.16)</h1>
<p class="lead">Allowable ampacity of copper and aluminum conductors at 60, 75 and 90 \u00b0C insulation ratings, for not more than three current-carrying conductors at 30 \u00b0C (86 \u00b0F) ambient. Look up a size below or open its page for worked examples.</p>
<section class="tool"><h2>Ampacity lookup</h2><div class="calc" data-tool="amp"><div class="row">
<label>Size <select data-s>{''.join(f'<option value="{s}"{" selected" if s == "10" else ""}>{awg(s)}</option>' for s in AMP_SIZES)}</select></label>
<label>Material <select data-m><option value="cu">Copper</option><option value="al">Aluminum</option></select></label>
<label>Column <select data-c><option value="0">60 \u00b0C</option><option value="1" selected>75 \u00b0C</option><option value="2">90 \u00b0C</option></select></label></div>
<output class="res" data-out aria-live="polite"></output></div></section>
<h2>NEC Table 310.16 ampacities</h2>
{table(['Size', 'Cu 60 \u00b0C', 'Cu 75 \u00b0C', 'Cu 90 \u00b0C', 'Al 60 \u00b0C', 'Al 75 \u00b0C', 'Al 90 \u00b0C'], rows, cls='data chart')}
<p>60 \u00b0C: TW, UF. 75 \u00b0C: RHW, THHW, THW, THWN, XHHW, USE, ZW. 90 \u00b0C: THHN, THHW, THW-2, THWN-2, RHH, RHW-2, USE-2, XHH, XHHW, XHHW-2 and others listed in the table heading.</p>
<h2>Common circuit sizes (copper, 60/75 \u00b0C terminations)</h2>
{table(['Breaker', 'Typical copper size', 'Why'], [('15 A', '14 AWG', '240.4(D) limit for 14 AWG'), ('20 A', '12 AWG', '240.4(D) limit for 12 AWG'), ('30 A', '10 AWG', '240.4(D) limit for 10 AWG'), ('40 A', '8 AWG', '40 A at 60 \u00b0C, 50 A at 75 \u00b0C'), ('50 A', '8 AWG (75 \u00b0C) or 6 AWG (60 \u00b0C)', '75 \u00b0C column 50 A'), ('60 A', '6 AWG (75 \u00b0C)', '65 A at 75 \u00b0C'), ('100 A', '3 AWG (75 \u00b0C)', '100 A at 75 \u00b0C')])}
<p>These assume ordinary conditions (\u22643 current-carrying conductors, 30 \u00b0C ambient, non-continuous load) and terminations rated for the column used. Dwelling services and feeders may use NEC 310.12 instead.</p>
<h2>Using the chart correctly</h2>
<p>Start from the column that matches the lowest temperature rating of any termination. Apply ambient correction (310.15(B)) and adjustment for more than three current-carrying conductors (310.15(C)(1)) to the insulation-rated column, then make sure the result is not above the terminal column. Remember 240.4(D) for small conductors and the 125% rule for continuous loads.</p>
<h2>Ampacity by size</h2>
{links(amp_links)}
<p class="src">Source: NEC (NFPA 70) 2023 Table 310.16, as printed in NFPA TIA 1691 (NFPA). Confirm the edition adopted in your jurisdiction.</p>
{faq_html(faqs)}
</article>'''
    page('/wire-ampacity-chart/', 'Wire Ampacity Chart: NEC Table 310.16 Copper & Aluminum', 'NEC Table 310.16 wire ampacity chart for copper and aluminum, 14 AWG to 1000 kcmil at 60/75/90 \u00b0C, with a quick lookup and the rules for picking a column.',
         body, crumbs=[('Electrical', '/electrical/'), ('Ampacity chart', '/wire-ampacity-chart/')], section='/electrical/',
         schema=[app_ld('Wire ampacity lookup', 'NEC 310.16', '/wire-ampacity-chart/'), article_ld('Wire ampacity chart', 'NEC 310.16', '/wire-ampacity-chart/'), faq_ld(faqs)])
    # voltage drop
    r8 = [(awg(s), f"{v['cmil']:,}", v['cu'], v['al'] if v['al'] else '\u2014') for s, v in E['t8'].items() if s not in ('18', '16')]
    faqs = [('What voltage drop is acceptable?', 'NEC informational notes recommend no more than 3% on a branch circuit and 5% total for feeder plus branch circuit. They are recommendations, not requirements, except where another rule (for example fire pumps) applies.'),
            ('Which formula does the calculator use?', 'Single-phase: VD = 2 \u00d7 L \u00d7 R \u00d7 I \u00f7 1000. Three-phase: VD = 1.732 \u00d7 L \u00d7 R \u00d7 I \u00f7 1000, with L the one-way length in feet and R the NEC Chapter 9 Table 8 resistance in ohms per 1,000 ft.'),
            ('Is Table 8 resistance accurate for AC?', 'It is DC resistance at 75 \u00b0C. For small conductors it is very close to AC impedance; for large conductors (1/0 and up) in steel conduit, Table 9 effective Z gives a more accurate AC result.')]
    body = f'''<article><h1>Voltage Drop Calculator</h1>
<p class="lead">Enter wire size and material, one-way length, load current and system voltage. The calculator uses NEC Chapter 9 Table 8 conductor resistance and also suggests the smallest size that keeps drop under 3%.</p>
<section class="tool"><h2>Calculate voltage drop</h2><div class="calc" data-tool="vd"><div class="row">
<label>Material <select data-m><option value="cu">Copper</option><option value="al">Aluminum</option></select></label>
<label>Size <select data-s>{''.join(f'<option value="{s}"{" selected" if s == "10" else ""}>{awg(s)}</option>' for s in E['t8'] if s not in ('18', '16'))}</select></label>
<label>Phase <select data-ph><option value="1">Single-phase / DC</option><option value="3">Three-phase</option></select></label></div><div class="row">
<label>One-way length (ft) <input type="number" inputmode="decimal" data-l value="100"></label>
<label>Current (A) <input type="number" inputmode="decimal" data-i value="24"></label>
<label>Voltage (V) <input type="number" inputmode="decimal" data-v value="240"></label></div>
<output class="res" data-out aria-live="polite"></output></div></section>
<h2>The formula</h2>
<p class="formula">VD = (2 or 1.732) \u00d7 L \u00d7 R \u00d7 I \u00f7 1000</p>
<p>Use 2 for single-phase and DC circuits (current flows out and back) and 1.732 (\u221a3) for balanced three-phase circuits. L is the one-way length in feet, I the load in amperes and R the resistance in ohms per 1,000 ft. Example: 10 AWG copper (1.24 \u03a9/kft), 100 ft, 24 A, 240 V single-phase: 2 \u00d7 100 \u00d7 1.24 \u00d7 24 \u00f7 1000 = 5.95 V, or 2.5%.</p>
<h2>Why voltage drop matters</h2>
<p>Motors and compressors run hotter and draw more current on low voltage, electronic loads can drop out, and lighting dims. Keeping drop near 3% on branch circuits and 5% overall is the NEC recommendation; equipment manufacturers may require tighter limits. Long runs to detached garages, wells, EV chargers, condensers and solar arrays are the usual problem cases.</p>
<h2>Conductor resistance (NEC Chapter 9 Table 8, stranded, 75 \u00b0C)</h2>
{table(['Size', 'Area (cmil)', 'Copper \u03a9/kft', 'Aluminum \u03a9/kft'], r8, cls='data chart')}
{links([('/wire-ampacity-chart/', 'Wire ampacity chart'), ('/conduit-fill-calculator/', 'Conduit fill calculator'), ('/blog/voltage-drop-3-percent-rule/', 'Guide: the 3% voltage drop rule')])}
<p class="src">Source: NEC (NFPA 70) Chapter 9 Table 8 (uncoated stranded copper and aluminum, DC resistance at 75 \u00b0C).</p>
{faq_html(faqs)}
</article>'''
    page('/voltage-drop-calculator/', 'Voltage Drop Calculator (NEC Table 8, Copper & Aluminum)', 'Free voltage drop calculator for single- and three-phase circuits using NEC Chapter 9 Table 8 resistance. Shows % drop and the smallest wire under 3%.',
         body, crumbs=[('Electrical', '/electrical/'), ('Voltage drop calculator', '/voltage-drop-calculator/')], section='/electrical/',
         schema=[app_ld('Voltage drop calculator', 'Voltage drop per NEC Table 8', '/voltage-drop-calculator/'), faq_ld(faqs)])
    # offsets
    angles = [(10, '10'), (15, '15'), (22.5, '22-5'), (30, '30'), (45, '45'), (60, '60')]
    field = {10: '6 (some use 5.75)', 15: '3.9 (some use 3.86)', 22.5: '2.6', 30: '2', 45: '1.4 (some use 1.41)', 60: '1.2 (some use 1.15)'}
    shrink_field = {10: '1/16 in', 15: '1/8 in', 22.5: '3/16 in', 30: '1/4 in', 45: '3/8 in', 60: '1/2 in'}
    orow = []
    for a, s in angles:
        m = 1 / math.sin(math.radians(a)); sh = math.tan(math.radians(a / 2))
        orow.append((f'<a href="{url(f"/{s}-degree-offset-multiplier/")}">{a}\u00b0</a>', f'{m:.3f}', field[a], f'{sh:.3f} in', shrink_field[a]))
    ofaq = [('What is an offset multiplier?', 'The number you multiply the offset depth by to get the distance between the two bends: 1 \u00f7 sin(angle), the cosecant.'),
            ('What is shrink?', 'How much shorter the conduit run gets because of the offset. Exact shrink per inch of offset = tan(angle \u00f7 2); field tables round it to common fractions.'),
            ('Which angle should I use?', 'Shallow angles (10\u00b0\u201322.5\u00b0) pull easier and look cleaner in tight spaces; 30\u00b0 and 45\u00b0 make shorter offsets. Total bends between pull points may not exceed 360\u00b0.')]
    tool = '''<section class="tool"><h2>Offset calculator</h2><div class="calc" data-tool="off"><div class="row">
<label>Angle <select data-a><option>10</option><option>15</option><option selected>22.5</option><option>30</option><option>45</option><option>60</option></select></label>
<label>Offset depth (in) <input type="number" inputmode="decimal" step="any" data-o value="6"></label></div>
<output class="res" data-out aria-live="polite"></output></div></section>'''
    body = f'''<article><h1>Conduit Offset Multiplier Chart</h1>
<p class="lead">Multiply the offset depth by the multiplier to get the distance between bends, and add the shrink for each inch of offset to the run. Exact trigonometric values are shown next to the rounded numbers bending charts usually print.</p>
{tool}
{table(['Bend angle', 'Exact multiplier (1/sin)', 'Field multiplier', 'Exact shrink per inch', 'Field shrink per inch'], orow)}
<h2>How to bend an offset</h2>
<ol><li>Measure the offset depth (how far the conduit must move over).</li><li>Pick the angle; multiply depth \u00d7 multiplier = distance between the two marks.</li>
<li>Shrink = depth \u00d7 shrink per inch. Add it to the measurement to the obstacle so the offset ends where you need it.</li>
<li>Make the first bend, rotate the conduit 180\u00b0, line up the second mark and bend to the same angle.</li></ol>
<p>Example: 6 in offset at 22.5\u00b0: 6 \u00d7 2.613 = 15.7 in between marks (about 15-11/16 in); shrink 6 \u00d7 0.199 = 1.2 in.</p>
<p class="src">Math: multiplier = csc(\u03b8); shrink per inch = csc(\u03b8) \u2212 cot(\u03b8) = tan(\u03b8/2). Field values are the rounded numbers commonly printed on bender charts. Bender take-up/gain still depends on your bender; check its manual.</p>
{faq_html(ofaq)}
</article>'''
    page('/conduit-offset-multiplier-chart/', 'Conduit Offset Multiplier Chart (10\u00b0 to 60\u00b0) + Shrink', 'Offset multiplier and shrink chart for 10, 15, 22.5, 30, 45 and 60 degree conduit offsets, exact and field values, with a quick offset calculator.',
         body, crumbs=[('Electrical', '/electrical/'), ('Offset multipliers', '/conduit-offset-multiplier-chart/')], section='/electrical/',
         schema=[app_ld('Offset calculator', 'Conduit offset multiplier and shrink', '/conduit-offset-multiplier-chart/'), faq_ld(ofaq)])
    for a, s in angles:
        m = 1 / math.sin(math.radians(a)); sh = math.tan(math.radians(a / 2))
        path = f'/{s}-degree-offset-multiplier/'
        rows = [(f'{d} in', f'{d * m:.2f} in', f'{d * sh:.2f} in') for d in (1, 2, 3, 4, 5, 6, 8, 10, 12, 18, 24)]
        faqs = [(f'What is the multiplier for a {a} degree offset?', f'{m:.3f} exact (1 \u00f7 sin {a}\u00b0); bending charts round it to {field[a]}.'),
                (f'What is the shrink for a {a} degree offset?', f'{sh:.3f} in per inch of offset depth (field value {shrink_field[a]} per inch).')]
        body = f'''<article><h1>{a}\u00b0 Offset Multiplier</h1>
<p class="lead">The multiplier for a {a}-degree offset is <b>{m:.3f}</b> (commonly rounded to {field[a]}). Shrink is <b>{sh:.3f} in per inch</b> of offset depth ({shrink_field[a]} on most bender charts).</p>
{tool.replace('<option selected>22.5</option>', '<option>22.5</option>').replace(f'<option>{a}</option>', f'<option selected>{a}</option>') if a != 22.5 else tool}
<h2>{a}\u00b0 offset table</h2>
{table(['Offset depth', 'Distance between bends', 'Shrink'], rows)}
<h2>Using a {a}\u00b0 offset</h2>
<p>Distance between bends = offset depth \u00d7 {m:.3f}. For a 4 in offset that is {4 * m:.2f} in. Add the shrink ({4 * sh:.2f} in for 4 in) to your measurement to the obstruction. {"A 10\u00b0 offset is long and gentle: good for small kicks at boxes but it needs more room." if a == 10 else "A 45\u00b0 offset is compact but harder to pull through; count it as 90\u00b0 of the 360\u00b0 allowed between pull points." if a == 45 else "Remember each offset adds twice its angle to the 360\u00b0 maximum between pull points."}</p>
{links([('/conduit-offset-multiplier-chart/', 'All offset multipliers')] + [(f'/{t}-degree-offset-multiplier/', f'{b}\u00b0 offset') for b, t in angles if b != a])}
{faq_html(faqs)}
</article>'''
        page(path, f'{a} Degree Offset Multiplier: {m:.3f} (and Shrink)', f'{a} degree conduit offset multiplier is {m:.3f}; shrink is {sh:.3f} in per inch. Table of bend spacing and shrink for 1\u201324 in offsets plus a calculator.',
             body, crumbs=[('Electrical', '/electrical/'), ('Offset multipliers', '/conduit-offset-multiplier-chart/'), (f'{a}\u00b0 offset', path)], section='/electrical/',
             schema=[faq_ld(faqs)])
    # box fill
    brows = [(n, f'{v:.1f}') + tuple(str(int(v // E['box_allow'][s])) for s in ('14', '12', '10', '8', '6')) for n, v in E['boxes']]
    faqs = [('How do I calculate box fill?', 'Count conductors, then add allowances: each internal cable clamp set counts 1, each device yoke counts 2, all equipment grounding conductors together count 1 (plus 1/4 for each beyond four), each fixture stud/hickey counts 1, all based on the largest conductor (NEC 314.16(B)).'),
            ('How many cubic inches per 12 AWG wire?', '2.25 in\u00b3 per conductor (Table 314.16(B)). 14 AWG is 2.00 in\u00b3 and 10 AWG is 2.50 in\u00b3.'),
            ('What volume does a plastic box have?', 'Nonmetallic boxes are marked with their volume by the manufacturer; use the marked value.')]
    body = f'''<article><h1>Box Fill Calculator (NEC 314.16)</h1>
<p class="lead">Pick a standard metal box or enter the marked volume, then count conductors, devices, clamps and grounds. The calculator adds the NEC 314.16(B) allowances and tells you whether the box is large enough.</p>
<section class="tool"><h2>Calculate box fill</h2><div class="calc" data-tool="box"><div class="row">
<label>Box <select data-b>{''.join(f'<option value="{v}">{n} ({v} in\u00b3)</option>' for n, v in E['boxes'])}<option value="custom">Marked volume (enter)</option></select></label>
<label>Volume (in\u00b3) <input type="number" inputmode="decimal" step="any" data-v value="21.0"></label></div>
<div class="row"><label>14 AWG <input type="number" min="0" data-w14 value="0"></label><label>12 AWG <input type="number" min="0" data-w12 value="4"></label><label>10 AWG <input type="number" min="0" data-w10 value="0"></label><label>8 AWG <input type="number" min="0" data-w8 value="0"></label><label>6 AWG <input type="number" min="0" data-w6 value="0"></label></div>
<div class="row"><label>Devices (yokes) <input type="number" min="0" data-dev value="1"></label><label>Internal clamps present <select data-cl><option value="0">No</option><option value="1">Yes</option></select></label>
<label>Grounding conductors <input type="number" min="0" data-eg value="2"></label><label>Fixture studs / hickeys <input type="number" min="0" data-st value="0"></label></div>
<output class="res" data-out aria-live="polite"></output></div></section>
<h2>Volume allowance per conductor (Table 314.16(B))</h2>
{table(['Conductor', 'Volume each'], [(f'{s} AWG', f'{v:.2f} in\u00b3') for s, v in E['box_allow'].items()])}
<h2>Standard metal boxes (Table 314.16(A))</h2>
{table(['Box (trade size)', 'Volume in\u00b3', 'Max 14', 'Max 12', 'Max 10', 'Max 8', 'Max 6'], brows, cls='data chart')}
<p>The maximum-conductor columns assume conductors only, with no clamps, devices or grounds. Subtract the allowances for those first.</p>
<h2>Counting rules in plain words</h2>
<ul><li>Each conductor that enters the box and is spliced or terminated counts once; one that passes through unbroken counts once (a loop long enough to cut counts twice).</li>
<li>Pigtails and jumpers that never leave the box do not count.</li><li>Each device (switch, receptacle) on a yoke counts twice, based on the largest conductor connected to it.</li>
<li>Internal cable clamps count once in total; each type of fixture stud or hickey counts once.</li><li>All equipment grounding conductors count once, with 1/4 extra for each one beyond four.</li></ul>
<p class="src">Source: NEC (NFPA 70) 314.16, Table 314.16(A) and 314.16(B), as reprinted in the Steel City (ABB) metallic box catalog.</p>
{faq_html(faqs)}
</article>'''
    page('/box-fill-calculator/', 'Box Fill Calculator & Chart (NEC 314.16)', 'NEC 314.16 box fill calculator with cubic-inch allowances for 14\u20136 AWG, devices, clamps and grounds, plus the Table 314.16(A) metal box volume chart.',
         body, crumbs=[('Electrical', '/electrical/'), ('Box fill calculator', '/box-fill-calculator/')], section='/electrical/',
         schema=[app_ld('Box fill calculator', 'NEC 314.16 box fill', '/box-fill-calculator/'), faq_ld(faqs)])
    # electrical hub
    body = f'''<article><h1>Electrical Charts &amp; Calculators</h1>
<p class="lead">NEC-based charts and calculators for electricians: conduit fill, ampacity, voltage drop, offset bending and box fill. Values come straight from the NEC tables, with the table number on every page.</p>
<h2>Calculators</h2>
{links([('/conduit-fill-calculator/', 'Conduit fill calculator'), ('/voltage-drop-calculator/', 'Voltage drop calculator'), ('/box-fill-calculator/', 'Box fill calculator'), ('/conduit-offset-multiplier-chart/', 'Offset multiplier & shrink')])}
<h2>Conduit fill charts</h2>
{links([(f'/{v[2]}/', f'{v[0]} fill chart') for v in CT.values()] + size_links)}
<h2>Ampacity</h2>
{links([('/wire-ampacity-chart/', 'Wire ampacity chart (310.16)')] + amp_links)}
<h2>Offset bends</h2>
{links([(f'/{s}-degree-offset-multiplier/', f'{a}\u00b0 offset multiplier') for a, s in angles])}
</article>'''
    page('/electrical/', 'Electrical Charts: Conduit Fill, Ampacity, Voltage Drop', 'NEC electrical reference: conduit fill charts for EMT, PVC and rigid, wire ampacity, voltage drop, conduit offset multipliers and box fill calculators.',
         body, crumbs=[('Electrical', '/electrical/')], section='/electrical/')
    json.dump(E, open(os.path.join(OUT, 'assets', 'electrical.json'), 'w'), separators=(',', ':'))
