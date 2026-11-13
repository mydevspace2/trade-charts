"""Home, blog, About/Contact/Privacy/Terms, 404 and search pages."""
from core import *
from pages_hvac import BY, pf, ps, REFS, COMPARISONS, glide, tp
import json, os

POSTS = [
 ('how-to-read-a-pt-chart', 'How to Read a PT Chart (Dew, Bubble and Glide Explained)', 'Step-by-step guide to reading a refrigerant PT chart: gauge vs absolute pressure, dew vs bubble for blends, glide, and worked superheat and subcooling examples.', '2026-11-13'),
 ('superheat-vs-subcooling', 'Superheat vs Subcooling: Which to Charge By and Why', 'Superheat vs subcooling explained for HVAC techs: what each measures, TXV vs fixed orifice charging, target values and the mistakes that cause bad charges.', '2026-11-13'),
 ('conduit-fill-40-percent-rule', 'Conduit Fill Explained: The NEC 40% Rule With Examples', 'How NEC Chapter 9 conduit fill works: the 53/31/40 percent limits, Table 4 and Table 5 areas, the 0.8 round-up rule, grounds, nipples and worked examples.', '2026-11-13'),
 ('voltage-drop-3-percent-rule', 'Voltage Drop and the 3% Rule: When to Upsize Wire', 'What the NEC actually says about 3% and 5% voltage drop, how to calculate it with Table 8 resistance, and when long runs need a bigger conductor.', '2026-11-13'),
 ('gas-pipe-sizing-longest-length-method', 'How to Size Gas Pipe: The Longest Length Method', 'Size natural gas and propane piping with the IFGC tables: add up Btu, convert to CFH, use the longest run row, and size each branch. Worked example included.', '2026-11-13'),
 ('how-to-tell-water-heater-age', 'How to Tell the Age of a Water Heater From the Serial Number', 'Find a water heater\u2019s manufacture date from its serial number: Bradford White letters, Rheem month-year, A.O. Smith year-week, plus where to find the label.', '2026-11-13'),
]

def post_bodies():
    r410, r454 = BY['r410a'], BY['r454b']
    p118 = pf(r410, 40, 0)
    d454, b454 = pf(r454, 40, 1), pf(r454, 40, 0)
    g454, g407 = glide(r454, 40), glide(BY['r407c'], 40)
    t340 = tp(r410, 340, 0)
    b = {}
    b['how-to-read-a-pt-chart'] = f'''
<p class="lead">A PT chart turns a gauge reading into a temperature. That one conversion is behind every superheat, subcooling and coil-temperature check you make, so it is worth getting exactly right.</p>
<h2>1. What the chart tells you</h2>
<p>When liquid and vapor refrigerant are both present (in the evaporator and condenser), the refrigerant is <b>saturated</b>: its pressure and temperature are locked together. The PT chart lists that pair for every temperature. R-410A at 40 \u00b0F, for example, saturates at {ps(p118)} psig. If your suction gauge reads {p118:.0f} psig, the refrigerant boiling in the evaporator is at about 40 \u00b0F.</p>
<p>The chart does <em>not</em> tell you the temperature of vapor that has left the coil or of liquid that has cooled below saturation. That difference is exactly what superheat and subcooling measure.</p>
<h2>2. Gauge pressure, absolute pressure and vacuum</h2>
<p>Field charts, including ours, list <b>psig</b>: pressure above the surrounding atmosphere. Absolute pressure (psia) is psig plus about 14.7 at sea level. Below atmospheric pressure the chart switches to inches of mercury vacuum (inHg). At altitude the atmosphere is lower, so a gauge reads a little higher than a sea-level chart for the same temperature, roughly 0.5 psi per 1,000 ft; for low-pressure refrigerants that matters more than for R-410A.</p>
<h2>3. Single refrigerants vs blends</h2>
<p>Pure refrigerants (R-22, R-32, R-134a) and azeotropes (R-507A, R-513A) have one pressure per temperature. Zeotropic blends (R-454B, R-407C, R-448A and most 400-series blends) boil over a range of temperatures at a given pressure. The chart then shows two columns:</p>
<ul><li><b>Bubble point</b>: the temperature where liquid starts to boil (first bubble).</li><li><b>Dew point</b>: the temperature where the last liquid has evaporated (last drop).</li></ul>
<p>The difference is the <b>glide</b>. R-454B at 40 \u00b0F shows {ps(d454)} psig dew and {ps(b454)} psig bubble, about a {g454:.1f} \u00b0F glide. R-407C has a much larger glide, about {g407:.1f} \u00b0F at the same pressure level.</p>
<h2>4. Which column to use</h2>
<p><b>Superheat uses the dew column.</b> Refrigerant leaving the evaporator has finished boiling at the dew point, so superheat = suction line temperature \u2212 dew temperature. <b>Subcooling uses the bubble column.</b> Refrigerant leaving the condenser is fully liquid below the bubble point, so subcooling = bubble temperature \u2212 liquid line temperature. Mixing them up on a high-glide blend can make a correct charge look several degrees off.</p>
<h2>5. Worked example (R-410A)</h2>
<p>Suction: 118 psig = 40 \u00b0F saturated. Suction line 52 \u00b0F. Superheat = 12 \u00b0F.<br>Liquid: 340 psig \u2248 {t340:.0f} \u00b0F saturated. Liquid line 95 \u00b0F. Subcooling = {t340-95:.0f} \u00b0F.<br>Compare superheat with the target (fixed orifice) and subcooling with the rating plate (TXV/EEV). Our <a href="{url('/superheat-calculator/')}">superheat</a> and <a href="{url('/subcooling-calculator/')}">subcooling</a> calculators do the lookups for 32 refrigerants.</p>
<h2>6. Common mistakes</h2>
<ul><li>Reading the wrong refrigerant scale (check the rating plate, not the sticker on the tank).</li><li>Measuring pressure and temperature at different places.</li><li>Judging charge before the system has run 15 minutes, or with dirty filters and coils.</li><li>Using a standing (off) pressure to judge charge: it only tells you the refrigerant is present and roughly the ambient temperature.</li><li>Ignoring non-condensables: pressure higher than the chart predicts for a system at rest can mean air in the system.</li></ul>
<p>Open any of our <a href="{url('/pt-chart/')}">32 PT charts</a> for the full table, a two-way lookup and a printable version.</p>'''
    b['superheat-vs-subcooling'] = f'''
<p class="lead">Both numbers tell you where the refrigerant is changing state. Superheat looks at the evaporator outlet, subcooling at the condenser outlet. Which one you charge by depends on the metering device.</p>
<h2>Superheat</h2>
<p>Superheat is how far the suction vapor is above its saturated (dew) temperature. Low superheat means liquid may be reaching the compressor (floodback); high superheat means the evaporator is starving, often from low charge, a restriction or low load. On fixed-orifice systems superheat changes with indoor and outdoor conditions, which is why manufacturers give a <b>target superheat</b> table based on indoor wet bulb and outdoor dry bulb. Our <a href="{url('/target-superheat-calculator/')}">target superheat calculator</a> uses the widely published approximation of those tables.</p>
<h2>Subcooling</h2>
<p>Subcooling is how far the liquid is below its saturated (bubble) temperature. It shows how much liquid is stacked in the condenser. A TXV or EEV holds evaporator superheat roughly constant on its own, so on those systems the charge shows up in subcooling instead, and manufacturers print a target subcooling on the rating plate or in the installation instructions.</p>
<h2>Rule of thumb for charging</h2>
{table(['Metering device', 'Charge by', 'Check'], [('Fixed orifice / piston / cap tube', 'Superheat vs target table', 'Subcooling for sanity'), ('TXV', 'Subcooling vs rating plate', 'Superheat 8\u201312 \u00b0F range typical'), ('EEV / inverter systems', 'Manufacturer procedure (often subcooling in a test mode)', 'Follow service manual')])}
<h2>Before you touch the charge</h2>
<ol><li>Confirm airflow: clean filter, correct blower speed, coils clean.</li><li>Run the system at least 15 minutes, ideally in a stable test mode.</li><li>Measure pressure and temperature at the same location, with insulated clamps on clean copper.</li><li>Use the right PT column: dew for superheat, bubble for subcooling on blends.</li><li>Adjust in small steps and let the system settle between changes. On new installs weigh in the charge, including the line-set adjustment.</li></ol>
<h2>What the combinations suggest</h2>
{table(['Superheat', 'Subcooling', 'Common causes to check'], [('High', 'Low', 'Undercharge, leak'), ('Low', 'High', 'Overcharge'), ('High', 'High', 'Restriction (filter drier, TXV), non-condensables possible'), ('Low', 'Low', 'Low indoor airflow or load, TXV overfeeding, compressor issue')])}
<p>These are starting points for diagnosis, not verdicts: confirm with temperature splits, amperage and the manufacturer\u2019s chart. Use our <a href="{url('/superheat-calculator/')}">superheat</a> and <a href="{url('/subcooling-calculator/')}">subcooling</a> calculators in the field.</p>'''
    b['conduit-fill-40-percent-rule'] = f'''
<p class="lead">Conduit fill is a simple area comparison: the conductors\u2019 total cross-sectional area must not exceed a percentage of the raceway\u2019s internal area. The percentages live in NEC Chapter 9, Table 1.</p>
<h2>The three limits</h2>
{table(['Number of conductors', 'Maximum fill'], [('1', '53%'), ('2', '31%'), ('3 or more', '40%')])}
<p>Two conductors get the lowest limit because two round wires side by side can jam in a bend. The internal areas of each raceway type and trade size are in Chapter 9 Table 4; conductor areas (with insulation) are in Table 5.</p>
<h2>Worked example: same size</h2>
<p>3/4 in EMT has an internal area of 0.533 in\u00b2; 40% is 0.213 in\u00b2. One 12 AWG THHN is 0.0133 in\u00b2. 0.213 \u00f7 0.0133 = 16.0, so 16 conductors fit. Chapter 9 Note 7 lets you round up only when the remainder is 0.8 or more, and only when all conductors are the same size.</p>
<h2>Worked example: mixed sizes</h2>
<p>Three 8 AWG THHN (0.0366 in\u00b2 each) plus one 10 AWG THHN ground (0.0211 in\u00b2) = 0.1309 in\u00b2. In 3/4 in EMT that is 24.6% \u2014 fine. In 1/2 in EMT (0.304 in\u00b2, 40% = 0.122 in\u00b2) it is 43% \u2014 too full. Use our <a href="{url('/conduit-fill-calculator/')}">conduit fill calculator</a> to add any mix and see the smallest raceway that works.</p>
<h2>Details that catch people</h2>
<ul><li><b>Grounds count.</b> Equipment grounding conductors, insulated or bare, are included (Note 3).</li><li><b>Nipples.</b> A raceway section 24 in or shorter between enclosures may be filled to 60% (Note 4).</li><li><b>Cables.</b> A multiconductor cable counts as one conductor using its outside diameter (Note 9).</li><li><b>Raceway type matters.</b> 1 in PVC Schedule 80 holds noticeably less than 1 in EMT; check the right chart.</li><li><b>Fill is not ampacity.</b> More than three current-carrying conductors require the 310.15(C)(1) adjustment, which may force larger wire and therefore larger conduit.</li></ul>
<p>See the same-size charts for <a href="{url('/emt-conduit-fill-chart/')}">EMT</a>, <a href="{url('/pvc-conduit-fill-chart/')}">PVC Schedule 40</a>, <a href="{url('/rigid-conduit-fill-chart/')}">rigid</a> and more.</p>'''
    b['voltage-drop-3-percent-rule'] = f'''
<p class="lead">The famous \u201c3% rule\u201d comes from informational notes in the NEC, not from an enforceable requirement. It is still good engineering, and some equipment manuals make it mandatory.</p>
<h2>What the Code says</h2>
<p>Informational notes in Articles 210 (branch circuits) and 215 (feeders) recommend sizing conductors so voltage drop does not exceed <b>3%</b> on a branch circuit or feeder, and <b>5%</b> for feeder plus branch circuit combined. Informational notes explain; they are not requirements unless your jurisdiction adopts them as such. Specific rules (for example fire pump circuits) do set mandatory limits.</p>
<h2>The calculation</h2>
<p class="formula">VD = K \u00d7 L \u00d7 R \u00d7 I \u00f7 1000, K = 2 (single-phase) or 1.732 (three-phase)</p>
<p>R is conductor resistance in ohms per 1,000 ft from NEC Chapter 9 Table 8, L the one-way length in feet and I the current in amps. Example: a 30 A, 240 V condenser circuit 120 ft from the panel on 10 AWG copper (1.24 \u03a9/kft): 2 \u00d7 120 \u00d7 1.24 \u00d7 30 \u00f7 1000 = 8.9 V, or 3.7%. Upsizing to 8 AWG (0.778 \u03a9/kft) gives 5.6 V, 2.3%.</p>
<h2>When to check</h2>
<ul><li>Detached garages, shops and outbuildings</li><li>Well pumps and irrigation</li><li>EV chargers on long runs</li><li>Rooftop units and condensers far from the panel</li><li>Low-voltage DC (solar, RV, battery) where a few volts is a big percentage</li></ul>
<h2>Watch the details</h2>
<ul><li>Use the actual load current for voltage drop, not the breaker size, unless you want a worst case.</li><li>Table 8 is DC resistance; for large AC conductors in steel raceway, Table 9 impedance is more accurate.</li><li>Upsizing ungrounded conductors for voltage drop requires a proportional increase of the equipment grounding conductor (250.122(B)).</li></ul>
<p>Run the numbers with our <a href="{url('/voltage-drop-calculator/')}">voltage drop calculator</a>, which also shows the smallest size under 3%.</p>'''
    b['gas-pipe-sizing-longest-length-method'] = f'''
<p class="lead">The IFGC sizing tables make gas pipe sizing a lookup: total load, longest length, read the row. Here is the method most inspectors expect, with an example.</p>
<h2>Step 1: total the load</h2>
<p>Add the maximum input from each appliance rating plate. Example house: furnace 80,000 Btu/h, water heater 40,000, range 65,000, dryer 22,000 = 207,000 Btu/h.</p>
<h2>Step 2: convert to the table units</h2>
<p>Natural gas tables are in cubic feet per hour (CFH). Divide by the heating value of the gas; 1,000 Btu/ft\u00b3 is a common assumption, but your utility can give the actual value. 207,000 \u00f7 1,000 = 207 CFH. Propane tables in the IFGC are already in thousands of Btu/h (207 MBH).</p>
<h2>Step 3: find the longest length</h2>
<p>Measure from the point of delivery (meter or second-stage regulator) to the most remote appliance. Say that is the dryer at 60 ft. Under the longest length method, the 60 ft row is used for <em>every</em> section of the system.</p>
<h2>Step 4: size each section</h2>
<p>Using IFGC Table 402.4(2) (Schedule 40 iron, under 2 psi, 0.5 in. w.c. drop), 60 ft row: 1/2 in = 65 CFH, 3/4 in = 137, 1 in = 257, 1-1/4 in = 528.</p>
{table(['Section', 'Load (CFH)', 'Size from 60 ft row'], [('Meter to first tee (all appliances)', '207', '1 in (257)'), ('Branch to furnace', '80', '3/4 in (137)'), ('Branch to range', '65', '1/2 in (65)'), ('Branch to dryer', '22', '1/2 in (65)'), ('Branch to water heater', '40', '1/2 in (65)')])}
<p>Sections that carry several appliances are sized for their combined load. If the load falls exactly on a table value, that size is acceptable; if the length falls between rows, use the longer row.</p>
<h2>Things to confirm</h2>
<ul><li>The table must match your gas, inlet pressure and design pressure drop.</li><li>Many fittings add equivalent length (IFGC Appendix A); CSST tables already include four bends and two fittings.</li><li>CSST sizes are by EHD, which varies by manufacturer.</li><li>Plan capacity for future appliances (generator, pool heater, outdoor kitchen).</li></ul>
<p>Use our <a href="{url('/gas-pipe-sizing/')}">gas pipe sizing calculator</a> with 12 IFGC tables for natural gas and propane.</p>'''
    b['how-to-tell-water-heater-age'] = f'''
<p class="lead">Most water heaters do not print a plain manufacture date. It is coded into the serial number, and each manufacturer uses its own code.</p>
<h2>Find the rating plate</h2>
<p>On a tank water heater the rating plate is the sticker on the front of the jacket, usually above the gas valve or the upper element cover. Copy the serial number exactly; do not confuse it with the model number.</p>
<h2>The main formats</h2>
{table(['Brand family', 'Code', 'Example'], [('Bradford White', '1st letter = year (20-year cycle), 2nd = month', 'HK\u2026 = October 2011 (or 1991)'), ('Rheem, Ruud, Richmond', 'MMYY at the start', '1209D\u2026 = December 2009'), ('A.O. Smith, State', 'YYWW at the start (older: month letter + year)', '2037\u2026 = week 37 of 2020'), ('American, Whirlpool', 'YYWW at the start', '1924\u2026 = week 24 of 2019')])}
<p>Each brand page has a decoder: <a href="{url('/bradford-white-water-heater-age/')}">Bradford White</a>, <a href="{url('/rheem-water-heater-age/')}">Rheem</a>, <a href="{url('/ao-smith-water-heater-age/')}">A.O. Smith</a>, <a href="{url('/state-water-heater-age/')}">State</a>, <a href="{url('/american-water-heater-age/')}">American</a> and more.</p>
<h2>Bradford White\u2019s 20-year loop</h2>
<p>Bradford White year letters repeat every 20 years and skip I, O, Q, R, U and V, so \u201cH\u201d can be 1991 or 2011. Use the condition of the heater, the energy label style and the home\u2019s history to pick the decade.</p>
<h2>Why it matters</h2>
<p>The U.S. Department of Energy estimates 10\u201315 years of life for storage water heaters. Knowing the age helps decide whether to repair or replace, check warranty (registered warranties usually run from the installation date), and plan before a leak forces an emergency replacement.</p>
<h2>When decoding fails</h2>
<p>Use the manufacturer\u2019s online warranty lookup with the full serial number, or call their support line. Store brands are made by one of the big manufacturers; the decoder for that maker usually works.</p>'''
    return b

def site_pages():
    bodies = post_bodies()
    for slug, title, desc, d in POSTS:
        path = f'/blog/{slug}/'
        body = f'<article class="post"><h1>{esc(title)}</h1><p class="meta">Guide \u00b7 Updated {UPDATED_H}</p>{bodies[slug]}</article>'
        page(path, title, desc, body, crumbs=[('Guides', '/blog/'), (title.split(':')[0][:50], path)], section='/blog/', og_type='article',
             schema=[article_ld(title, desc, path, d)])
    body = '<article><h1>Guides</h1><p class="lead">Short, practical explanations behind the charts and calculators.</p><ul class="cards">' + ''.join(
        f'<li><a href="{url(f"/blog/{s}/")}"><b>{esc(t)}</b><span>{esc(dd)}</span></a></li>' for s, t, dd, _ in POSTS) + '</ul></article>'
    page('/blog/', 'Field Guides for HVAC, Electrical & Gas Techs', 'Practical guides for trades: reading PT charts, superheat vs subcooling, conduit fill, voltage drop, gas pipe sizing and water heater age.',
         body, crumbs=[('Guides', '/blog/')], section='/blog/')
    # home
    pop = [('/r454b-pt-chart/', 'R-454B PT chart'), ('/r410a-pt-chart/', 'R-410A PT chart'), ('/r32-pt-chart/', 'R-32 PT chart'), ('/r22-pt-chart/', 'R-22 PT chart'),
           ('/r134a-pt-chart/', 'R-134a PT chart'), ('/r404a-pt-chart/', 'R-404A PT chart'), ('/r448a-pt-chart/', 'R-448A PT chart'), ('/r407c-pt-chart/', 'R-407C PT chart')]
    body = f'''<section class="hero"><h1>Trade charts that are fast, accurate and free</h1>
<p class="lead">Refrigerant PT charts, superheat and subcooling, NEC conduit fill, ampacity, voltage drop, gas pipe sizing and age-by-serial decoders. Every number is sourced and checked; every page works on a phone in a crawlspace.</p>
<div class="actions"><a class="btn" href="{url('/pt-chart/')}">PT charts</a> <a class="btn ghost" href="{url('/conduit-fill-calculator/')}">Conduit fill</a> <a class="btn ghost" href="{url('/gas-pipe-sizing/')}">Gas pipe sizing</a></div></section>
<section class="tool"><h2>Quick PT lookup</h2>
<div class="pt" data-tool="pt-any"><div class="row"><label>Refrigerant <select data-ref>{''.join(f'<option value="{r["slug"]}"{" selected" if r["slug"] == "r454b" else ""}>{r["name"]}</option>' for r in sorted(REFS, key=lambda x: x["name"]))}</select></label></div>
<div class="seg" role="group" aria-label="Lookup direction"><button type="button" data-mode="t2p" aria-pressed="true">Temp &rarr; Pressure</button><button type="button" data-mode="p2t" aria-pressed="false">Pressure &rarr; Temp</button></div>
<div class="row"><label>Value <input type="number" inputmode="decimal" step="any" data-in value="40"></label><label class="u-t">Temp unit <select data-tu><option value="F">\u00b0F</option><option value="C">\u00b0C</option></select></label>
<label class="u-p" hidden>Pressure unit <select data-pu><option value="psig">psig</option><option value="kpa">kPa (gauge)</option><option value="bar">bar (gauge)</option></select></label></div>
<output class="res" data-out aria-live="polite"></output></div></section>
<div class="grid3">
<section class="card"><h2><a href="{url('/pt-chart/')}">Refrigerant PT charts</a></h2><p>32 refrigerants with bubble/dew columns, \u00b0F/\u00b0C, psig/kPa, print view and verification against manufacturer data.</p>{links(pop)}</section>
<section class="card"><h2><a href="{url('/hvac-calculators/')}">HVAC calculators</a></h2><p>Superheat, subcooling and target superheat, plus side-by-side refrigerant comparisons.</p>{links([('/superheat-calculator/', 'Superheat'), ('/subcooling-calculator/', 'Subcooling'), ('/target-superheat-calculator/', 'Target superheat'), ('/r454b-vs-r410a/', 'R-454B vs R-410A'), ('/r32-vs-r454b/', 'R-32 vs R-454B')])}</section>
<section class="card"><h2><a href="{url('/electrical/')}">Electrical</a></h2><p>NEC Chapter 9 conduit fill, Table 310.16 ampacity, voltage drop, offsets and box fill.</p>{links([('/conduit-fill-calculator/', 'Conduit fill calculator'), ('/emt-conduit-fill-chart/', 'EMT fill chart'), ('/pvc-conduit-fill-chart/', 'PVC fill chart'), ('/wire-ampacity-chart/', 'Ampacity chart'), ('/voltage-drop-calculator/', 'Voltage drop'), ('/box-fill-calculator/', 'Box fill')])}</section>
<section class="card"><h2><a href="{url('/gas-pipe-sizing/')}">Gas pipe sizing</a></h2><p>IFGC tables for natural gas and propane in black iron, CSST and PE, with a sizing calculator.</p>{links([('/natural-gas-pipe-sizing-chart/', 'Natural gas, black iron'), ('/csst-gas-pipe-sizing-chart/', 'CSST'), ('/propane-gas-pipe-sizing-chart/', 'Propane')])}</section>
<section class="card"><h2><a href="{url('/age-by-serial-number/')}">Age by serial number</a></h2><p>Decode manufacture dates for water heaters and HVAC equipment, with the manufacturer source cited.</p>{links([('/bradford-white-water-heater-age/', 'Bradford White'), ('/rheem-water-heater-age/', 'Rheem'), ('/ao-smith-water-heater-age/', 'A.O. Smith'), ('/carrier-age-by-serial-number/', 'Carrier'), ('/goodman-age-by-serial-number/', 'Goodman')])}</section>
<section class="card"><h2><a href="{url('/welding/')}">Welding</a></h2><p>MIG starting settings calculator and TIG amperage chart from Miller\u2019s published guidance.</p>{links([('/mig-welding-settings-calculator/', 'MIG settings'), ('/tig-welding-amperage-chart/', 'TIG amperage')])}</section>
</div>
<section><h2>Why techs use Trade Charts</h2>
<ul class="ticks"><li><b>Checked data.</b> Each PT chart is compared point by point with manufacturer or NIST data and shows its maximum deviation.</li>
<li><b>Two-way lookups.</b> Temperature to pressure and pressure to temperature, \u00b0F/\u00b0C and psig/kPa/bar.</li>
<li><b>Code references on the page.</b> NEC and IFGC table numbers and sources are printed with the numbers.</li>
<li><b>Fast and private.</b> Static pages, no ads, no trackers, no cookies, no sign-up. Dark mode and print views built in.</li></ul></section>'''
    page('/', 'Trade Charts: PT Charts, Conduit Fill, Gas Pipe Sizing', 'Free field reference for US trades: refrigerant PT charts, superheat/subcooling, NEC conduit fill and ampacity, gas pipe sizing and age-by-serial decoders.',
         body, section=None, schema=[{'@context': 'https://schema.org', '@type': 'WebSite', 'name': SITE_NAME, 'url': abs_url('/'),
                                      'potentialAction': {'@type': 'SearchAction', 'target': abs_url('/search/') + '?q={search_term_string}', 'query-input': 'required name=search_term_string'}},
                                     {'@context': 'https://schema.org', '@type': 'Organization', 'name': SITE_NAME, 'url': abs_url('/'), 'logo': abs_url('/assets/icon-512.png')}])
    about = f'''<article><h1>About Trade Charts</h1>
<p class="lead">Trade Charts is a free reference site for HVAC/R technicians, electricians, plumbers, gas fitters and welders in the United States. It is built to be fast on a phone, readable in sunlight or in the dark, and honest about where every number comes from.</p>
<h2>Data sources</h2>
<ul><li><b>Refrigerant properties:</b> CoolProp 8 (open-source implementation of the reference equations of state used by NIST REFPROP), ASHRAE Standard 34 blend compositions; R-438A from the DuPont/Chemours ISCEON MO99 chart.</li>
<li><b>Verification charts:</b> Arkema Forane PT chart (2025, REFPROP 10), Honeywell Solstice/Genetron PT charts and pressure-based tool, Hudson Technologies PT charts, Chemours, NIST Chemistry WebBook, ASHRAE/UNEP refrigerant factsheet (2025).</li>
<li><b>GWP:</b> IPCC AR4 values as listed by the UNEP Ozone Secretariat; ASHRAE/UNEP factsheet where noted.</li>
<li><b>Electrical:</b> NEC (NFPA 70) Chapter 9 Tables 1, 4, 5 and 8; Table 310.16 (NFPA 70-2023 as printed in NFPA TIA 1691); 314.16 box fill tables.</li>
<li><b>Gas piping:</b> 2021 International Fuel Gas Code Tables 402.4(1)\u2013402.4(36).</li>
<li><b>Serial number formats:</b> manufacturer documents (Bradford White, Rheem, A.O. Smith, Lennox, Trane, Carrier, Goodman) and the InterNACHI water heater dating chart.</li>
<li><b>Welding:</b> Miller Electric published parameter guides.</li></ul>
<h2>How we check</h2>
<p>Every PT chart is generated by a script and compared point by point against at least one published chart before it can go live; the build fails if any point differs by more than 1 \u00b0F. Code tables are parsed from the source documents and the published values are compared again in automated tests. We publish fewer pages rather than guess: refrigerants, brands and machines we cannot verify are left out and named as such.</p>
<h2>What we are not</h2>
<p>We are not affiliated with NFPA, ICC, ASHRAE or any manufacturer, and this site is not a substitute for the code adopted in your jurisdiction, the equipment installation instructions, or a licensed professional.</p>
<p><a href="{url('/contact/')}">Contact us</a> with corrections or requests.</p></article>'''
    page('/about/', 'About Trade Charts: Sources & How We Verify Data', 'Who runs Trade Charts, which manufacturer, NIST, NEC and IFGC sources the data comes from, and how every chart is verified before it is published.',
         about, crumbs=[('About', '/about/')])
    contact = f'''<article><h1>Contact</h1><p class="lead">Spotted a wrong value, a broken page, or want a refrigerant, table or brand added? Email us and include the page address and the source you are comparing against.</p>
<p class="big"><a href="mailto:topelitemindset1@gmail.com?subject=Trade%20Charts">topelitemindset1@gmail.com</a></p>
<p>We read every message. Corrections backed by a manufacturer document or code text are usually fixed within a few days. We do not offer engineering or code-compliance advice for specific jobs.</p></article>'''
    page('/contact/', 'Contact Trade Charts: Corrections & Requests', 'Send corrections, broken-page reports or requests for new refrigerants, code tables and brands to Trade Charts.', contact, crumbs=[('Contact', '/contact/')])
    privacy = f'''<article><h1>Privacy Policy</h1><p class="lead">Short version: we do not collect personal data. No analytics, no advertising, no cookies, no tracking scripts.</p>
<h2>What happens when you visit</h2><p>Pages are static files served by GitHub Pages. Like any web host, GitHub may log technical data such as your IP address for security and operations; see GitHub\u2019s privacy statement. We do not receive or use those logs for tracking.</p>
<h2>Calculators</h2><p>All calculations run in your browser. Values you type are never sent to a server. A small amount of data (for example the unit you last selected) may be stored in your browser\u2019s local storage so the page remembers it; it never leaves your device and you can clear it in your browser settings.</p>
<h2>Email</h2><p>If you email us, we use your address only to reply.</p>
<h2>Changes</h2><p>If this ever changes (for example if we add privacy-friendly analytics), we will update this page first. Last updated {UPDATED_H}.</p></article>'''
    page('/privacy/', 'Privacy Policy | Trade Charts', 'Trade Charts collects no personal data: no analytics, no ads, no cookies or trackers. Calculators run entirely in your browser.', privacy, crumbs=[('Privacy', '/privacy/')])
    terms = f'''<article><h1>Terms of Use</h1>
<p>Trade Charts provides reference information free of charge. By using the site you agree that:</p>
<ul><li>The content is for general reference and training. It is not engineering advice and does not replace the code adopted by your authority having jurisdiction, equipment manufacturer instructions, or the judgement of a licensed professional.</li>
<li>We work to keep the data accurate and verified, but we make no warranty of accuracy, completeness or fitness for a particular purpose, and we are not liable for any loss or damage arising from use of the site.</li>
<li>Refrigerant, electrical and fuel-gas work can cause injury, death, fire and property damage. Perform it only if you are qualified, licensed and certified where required (for example EPA Section 608 for refrigerants).</li>
<li>NEC and NFPA 70 are trademarks of NFPA; IFGC is a publication of the ICC; product and brand names belong to their owners. Their use here is for identification only.</li>
<li>You may link to and print pages for personal or internal training use. Do not republish the site\u2019s compiled tables wholesale.</li></ul>
<p>Last updated {UPDATED_H}.</p></article>'''
    page('/terms/', 'Terms of Use | Trade Charts', 'Terms of use for Trade Charts: free reference information, no warranty, verify with your adopted code and manufacturer instructions.', terms, crumbs=[('Terms', '/terms/')])
    nf = f'''<article><h1>Page not found</h1><p class="lead">That page does not exist (or moved). Try the search box above or one of these:</p>
{links([('/pt-chart/', 'Refrigerant PT charts'), ('/hvac-calculators/', 'HVAC calculators'), ('/electrical/', 'Electrical charts'), ('/gas-pipe-sizing/', 'Gas pipe sizing'), ('/age-by-serial-number/', 'Age by serial number'), ('/', 'Home')])}</article>'''
    page('/404.html', 'Page Not Found | Trade Charts', 'The page you were looking for was not found. Browse refrigerant PT charts, electrical charts, gas pipe sizing and age decoders.', nf, noindex=True)
    sr = f'''<article><h1>Search</h1><div class="searchpage" data-tool="search"><label class="sr" for="q2">Search</label><input id="q2" type="search" placeholder="r454b, 3/4 emt, propane csst\u2026" data-q><ol class="results" data-r></ol></div></article>'''
    page('/search/', 'Search Trade Charts', 'Search all Trade Charts pages: PT charts, conduit fill, ampacity, gas pipe sizing tables and serial-number decoders.', sr, noindex=True)
