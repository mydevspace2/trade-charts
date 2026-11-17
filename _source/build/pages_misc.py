"""Gas pipe sizing, age-by-serial decoders, welding."""
import json, os
from core import *

G = json.load(open(os.path.join(HERE, 'data', 'gas.json')))

def sz(s, csst):
    return f'EHD {s}' if csst else f'{s}"'

GT = {2: 'Natural Gas Pipe Sizing Chart: Black Iron, 0.5 in. w.c. Drop', 1: 'Natural Gas Pipe Sizing Chart: Black Iron, 0.3 in. w.c. Drop',
      5: '2 PSI Natural Gas Pipe Sizing Chart: Black Iron', 15: 'CSST Gas Pipe Sizing Chart: Natural Gas, Low Pressure',
      18: '2 PSI CSST Gas Pipe Sizing Chart: Natural Gas', 21: 'Polyethylene Gas Pipe Sizing Chart: Natural Gas',
      28: 'Propane Gas Pipe Sizing Chart: Black Iron, 11 in. w.c.', 27: '2 PSI Propane Pipe Sizing Chart: Black Iron',
      32: 'Propane CSST Sizing Chart: 11 in. w.c. Low Pressure', 33: '2 PSI Propane CSST Sizing Chart',
      35: 'Propane Polyethylene Pipe Sizing Chart: 11 in. w.c.', 36: '2 PSI Propane Polyethylene Pipe Sizing Chart'}

def gas_pages():
    os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
    json.dump(G, open(os.path.join(OUT, 'assets', 'gas.json'), 'w'), separators=(',', ':'))
    opts = ''.join(f'<option value="{t["table"]}">{esc(t["title"])}</option>' for t in G['tables'])
    tool = lambda sel: f'''<section class="tool"><h2>Gas pipe sizing calculator</h2><div class="calc" data-tool="gas" data-table="{sel}"><div class="row">
<label>System / table <select data-tb>{opts.replace(f'value="{sel}"', f'value="{sel}" selected')}</select></label></div><div class="row">
<label>Total connected load (Btu/h) <input type="number" inputmode="numeric" data-btu value="120000"></label>
<label>Longest run, meter to farthest appliance (ft) <input type="number" inputmode="numeric" data-len value="50"></label>
<label class="hv">Gas heating value (Btu/ft\u00b3) <input type="number" inputmode="numeric" data-hv value="1000"></label></div>
<output class="res" data-out aria-live="polite"></output></div></section>'''
    for t in G['tables']:
        path = f'/{t["slug"]}/'
        csst = 'CSST' in t['material']
        lp = 'Propane' in t['gas']
        unit = 'thousand Btu/h (MBH)' if lp else 'cubic feet per hour (CFH)'
        rows = []
        for L, vals in t['rows'].items():
            rows.append([f'{int(L):,} ft'] + [f'{v:,}' if v is not None else 'NA' for v in vals])
        heads = ['Length'] + [sz(s, csst) for s in t['sizes']]
        r10 = t['rows'].get('10') or t['rows'].get(next(iter(t['rows'])))
        L50 = t['rows'].get('50')
        h1 = GT[t['table']]
        title = h1 + ' (IFGC)'
        desc = f"IFGC Table 402.4({t['table']}) gas pipe sizing chart: {t['title']}. Capacity in {unit} for every length, plus a sizing calculator."
        if len(desc) > 159: desc = desc[:156].rsplit(' ', 1)[0] + '.'
        ex = ''
        if L50 and not lp:
            need = 120  # CFH for 120,000 Btu/h at 1000 Btu/ft3
            pick = next((sz(s, csst) for s, v in zip(t['sizes'], L50) if v and v >= need), None)
            ex = (f'<p><b>Example.</b> A 120,000 Btu/h total load is 120 CFH at 1,000 Btu/ft\u00b3. With a 50 ft longest run, read the 50 ft row and pick the first size '
                  f'with at least 120 CFH: <b>{pick}</b>. Branches are sized the same way using the same 50 ft row and only the load each branch carries.</p>') if pick else ''
        elif L50 and lp:
            pick = next((sz(s, csst) for s, v in zip(t['sizes'], L50) if v and v >= 120), None)
            ex = (f'<p><b>Example.</b> A 120,000 Btu/h propane load is 120 MBH. With a 50 ft longest run, the first size in the 50 ft row with at least 120 is <b>{pick}</b>.</p>') if pick else ''
        faqs = [('What is the longest length method?', 'IFGC 402.4.1: find the length from the point of delivery to the most remote outlet and use that single length row of the table to size every section of the system, each for the load it carries.'),
                ('How do I convert Btu/h to CFH?', 'Divide the appliance input by the gas heating value. Natural gas is often about 1,000 Btu per cubic foot (check with your utility); 120,000 Btu/h \u00f7 1,000 = 120 CFH.' if not lp else 'Propane tables in the IFGC are already in thousands of Btu per hour, so a 120,000 Btu/h load is 120 in the table.'),
                ('Do fittings count?', 'The IFGC tables are based on straight pipe; Appendix A suggests adding equivalent length for runs with four or more fittings. CSST tables already include four 90\u00b0 bends and two end fittings; add 1.3 ft for each extra bend or fitting.' if csst else 'The tables assume a normal number of fittings. IFGC Appendix A suggests adding equivalent length when a run has four or more fittings.')]
        notes = ('<p>CSST sizes are given as EHD (equivalent hydraulic diameter) flow designations; check the manufacturer\u2019s EHD for its tube sizes, because the same nominal size can differ between brands. '
                 'The table includes losses for four 90-degree bends and two end fittings.</p>') if csst else ''
        body = f'''<article><h1>{esc(h1)}</h1>
<p class="lead">IFGC Table 402.4({t["table"]}): {esc(t["material"].lower())}, {esc(t["gas"].lower())} gas, inlet pressure {esc(t["inlet"])}, pressure drop {esc(t["drop"])}, specific gravity {esc(t["sg"])}. Capacities are in <b>{unit}</b>.</p>
{tool(t["table"])}
<h2>Capacity table ({unit})</h2>
{table(heads, rows, cls="data chart")}
{ex}
{notes}
<h2>How to size gas pipe with this table</h2>
<ol><li>Add up the maximum input (nameplate Btu/h) of every appliance the section serves.</li>
<li>{"Convert to CFH by dividing by the heating value of your gas." if not lp else "Propane tables are in thousands of Btu/h; use the load directly."}</li>
<li>Measure the length from the meter or regulator outlet to the farthest appliance; use the next longer row if your length falls between rows.</li>
<li>In that row, choose the first pipe size whose capacity equals or exceeds the load. Repeat for each branch with its own load, using the same row.</li></ol>
<p>Use this table only for the exact gas, pressure and pressure drop in its heading; a different design pressure drop needs a different table. Low-pressure (under 2 psi) systems usually serve appliances at about 7 in. w.c. natural gas or 11 in. w.c. propane; 2 psi and 5 psi systems need a line regulator ahead of the appliances.</p>
<h2>Other gas sizing tables</h2>
{links([(f'/{x["slug"]}/', x["title"]) for x in G["tables"] if x["table"] != t["table"]])}
<p class="src">Source: 2021 International Fuel Gas Code (IFGC) Table 402.4({t["table"]}) (text as adopted in the 2021 Seattle Fuel Gas Code chapter 4; Table 402.4(2) cross-checked with ICC CodeNotes). Many jurisdictions use the IRC (Table G2413.4) or NFPA 54 with the same values; confirm your adopted code. Values reproduced as published.</p>
{faq_html(faqs)}
</article>'''
        page(path, title, desc, body, crumbs=[('Gas Pipe', '/gas-pipe-sizing/'), (f'Table 402.4({t["table"]})', path)], section='/gas-pipe-sizing/',
             schema=[app_ld('Gas pipe sizing calculator', desc, path), article_ld(title, desc, path), faq_ld(faqs)])
    faqs = [('How do you size natural gas pipe?', 'Total the Btu/h load, convert to CFH, find the longest run, and pick the size from the matching IFGC table row with enough capacity. Repeat for each branch.'),
            ('What size gas line for 100,000 Btu?', 'It depends on length and material. In Schedule 40 iron at under 2 psi with 0.5 in. w.c. drop, 100 CFH needs 1/2" up to about 20 ft and 3/4" up to about 70 ft (Table 402.4(2)). Use the calculator for your run.'),
            ('Is propane sized differently?', 'Yes. Propane has higher energy per cubic foot, so IFGC propane tables are in thousands of Btu/h and allow smaller pipe for the same load.')]
    body = f'''<article><h1>Gas Pipe Sizing Charts &amp; Calculator</h1>
<p class="lead">Size natural gas and propane piping in black iron, CSST and polyethylene with the IFGC capacity tables. Enter the load and the longest run; the calculator picks the smallest size that works.</p>
{tool(2)}
<h2>Natural gas tables</h2>
{links([(f'/{x["slug"]}/', x["title"]) for x in G["tables"] if 'Natural' in x['gas']])}
<h2>Propane (LP) tables</h2>
{links([(f'/{x["slug"]}/', x["title"]) for x in G["tables"] if 'Propane' in x['gas']])}
<h2>Before you size</h2>
<p>Confirm the delivery pressure with the utility or propane supplier, the allowable pressure drop your design uses, and every appliance input on its rating plate. Plan for future appliances such as a generator, pool heater or range. The tables are the code\u2019s capacities; the installation still needs permits, pressure testing and inspection per your local code.</p>
<p>Read our guide: <a href="{url('/blog/gas-pipe-sizing-longest-length-method/')}">how to size gas pipe with the longest length method</a>.</p>
{faq_html(faqs)}
</article>'''
    page('/gas-pipe-sizing/', 'Gas Pipe Sizing Chart & Calculator (Natural Gas & Propane)', 'Gas pipe sizing calculator and IFGC charts for natural gas and propane: black iron, CSST and PE at low pressure and 2 psi. Pick size from Btu and length.',
         body, crumbs=[('Gas Pipe', '/gas-pipe-sizing/')], section='/gas-pipe-sizing/',
         schema=[app_ld('Gas pipe sizing calculator', 'IFGC gas pipe sizing', '/gas-pipe-sizing/'), faq_ld(faqs)])

# ---------- age by serial ----------
BW_Y = 'A B C D E F G H J K L M N P S T W X Y Z'.split()
MON = 'January February March April May June July August September October November December'.split()
WH = [
 ('bradford-white', 'Bradford White', 'bw', 'Water heater', 'The first two letters of the serial number: first letter = year, second letter = month. The year letters repeat every 20 years (A = 2004 or 2024), skipping I, O, Q, R, U and V; month letters run A (January) to M (December), skipping I.',
  'Example: <b>HK</b>16433183 = H (2011) + K (October) = October 2011.', 'Bradford White official \u201cDetermine the age of my water heater\u201d chart (bradfordwhite.com/my-water-heater) and service manuals', 'https://www.bradfordwhite.com/my-water-heater/', 'BH6511396'),
 ('rheem', 'Rheem', 'mmyy', 'Water heater', 'Rheem water heater serials are 10 characters: the first two digits are the month and the next two the year of manufacture, followed by a plant line code letter and a sequence number.',
  'Example: <b>1209</b>D01234 = December 2009.', 'Rheem \u201cHow to locate and read your Rheem water heating serial numbers\u201d', 'https://www.rheem.com/how-to-locate-and-read-your-rheem-water-heating-serial-numbers', '1209D01234'),
 ('ruud', 'Ruud', 'mmyy', 'Water heater', 'Ruud is a Rheem Manufacturing brand and uses the same serial layout: first two digits = month, next two = year.',
  'Example: <b>0514</b>A12345 = May 2014.', 'Rheem serial number guide; InterNACHI water heater dating chart (Ruud: 1st and 2nd digit = month, 3rd and 4th = year)', 'https://www.nachi.org/water-heater-dating-chart.htm', '0514A12345'),
 ('richmond', 'Richmond', 'mmyy', 'Water heater', 'Richmond water heaters are built by Rheem: first two digits = month, next two = year.',
  'Example: <b>0818</b>M12345 = August 2018.', 'InterNACHI water heater dating chart (Richmond)', 'https://www.nachi.org/water-heater-dating-chart.htm', '0818M12345'),
 ('ge', 'GE (Rheem-built)', 'mmyy', 'Water heater', 'InterNACHI lists General Electric and Hotpoint among the Rheem trade names: on Rheem-built GE units the first two digits are the month and the next two the year. GE water heaters made by other manufacturers may use a different format; if the decoded date looks wrong, check the label or call GE.',
  'Example: <b>0307</b>X12345 = March 2007.', 'InterNACHI water heater dating chart (Rheem trade names include General Electric, Hotpoint)', 'https://www.nachi.org/water-heater-dating-chart.htm', '0307X12345'),
 ('ao-smith', 'A.O. Smith', 'yyww', 'Water heater', 'Current A.O. Smith serials begin with the year (two digits) and the week (two digits). Older units (before about 2008) used a letter for the month in the second position followed by a two-digit year.',
  'Example: <b>2037</b>07002601001 = week 37 of 2020 (early September). Older: 2<b>C06</b>2938405 = March 2006.', 'A.O. Smith \u201cProduction date of my device\u201d; City of Palo Alto water heater age guide', 'https://aosmithinternational.com/manufacturing-date-device/', '2037070026'),
 ('state', 'State', 'yyww', 'Water heater', 'State is an A.O. Smith brand. Current serials start with year + week like A.O. Smith; older State units used a month letter (A = January \u2026 M = December) followed by a two-digit year in the first three characters.',
  'Example: <b>1715</b>A012345 = week 15 of 2017. Older: <b>J89</b>xxx = October 1989.', 'A.O. Smith production-date guide; InterNACHI water heater dating chart (State Industries)', 'https://www.nachi.org/water-heater-dating-chart.htm', '1715A01234'),
 ('american', 'American Water Heater', 'yyww', 'Water heater', 'American Water Heater (also many store brands) uses the first four digits: two-digit year then two-digit week.',
  'Example: <b>1924</b>115263020 = week 24 of 2019. InterNACHI example: 8906xxx = 6th week of 1989.', 'InterNACHI water heater dating chart (American: 1st 2 digits = year, 2nd 2 digits = week)', 'https://www.nachi.org/water-heater-dating-chart.htm', '1924115263'),
 ('whirlpool', 'Whirlpool', 'yyww', 'Water heater', 'Whirlpool-branded water heaters are built by American Water Heater, which InterNACHI lists with Whirlpool among its trade names: first two digits = year, next two = week.',
  'Example: <b>1103</b>A12345 = week 3 of 2011.', 'InterNACHI water heater dating chart (American / U.S. Craftmaster trade names include Whirlpool)', 'https://www.nachi.org/water-heater-dating-chart.htm', '1103A12345'),
]
HV = [
 ('carrier', 'Carrier, Bryant & Payne', 'wwyy', 'HVAC unit', 'Since the 1980s Carrier-family serials (Carrier, Bryant, Payne, Day & Night) start with four digits: week of manufacture (01\u201353) then two-digit year, followed by a plant letter and a sequence number.',
  'Example: <b>3112</b>U12345 = week 31 of 2012. <b>0106</b>E00001 = week 1 of 2006 (plant E).', 'Carrier service literature (48TC series, serial number nomenclature); Energy Trust of Oregon equipment age guide', 'https://insider.energytrust.org/wp-content/uploads/CPF_Age_Information.pdf', '3112U12345'),
 ('goodman', 'Goodman, Amana & Daikin', 'yymm', 'HVAC unit', 'Goodman, Amana and Daikin residential units use a 10-digit serial whose first four digits are the year (two digits) and the month (two digits).',
  'Example: <b>1306</b>123456 = June 2013. <b>2110</b>xxxxxx = October 2021.', 'Goodman warranty documentation (\u201cthe first four digits\u2026 year and month\u201d); HVACDirect manufacturer FAQ', 'https://hvacdirect.com/knowledge-base/how-do-i-find-my-date-of-manufacture-/', '1306123456'),
 ('lennox', 'Lennox', 'lennox', 'HVAC unit', 'Lennox serials begin with a two-digit plant code, then a two-digit year, then a month letter (A = January, B = February\u2026), then a sequence number.',
  'Example: 59<b>21C</b>O05716 = plant 59 (Marshalltown, IA), 2021, March.', 'Lennox model and serial number identification guide (Form 210965, 2025)', 'https://www.hvacbase.org/hvac-serial-number-decoder', '5921C05716'),
 ('trane', 'Trane & American Standard', 'trane', 'HVAC unit', 'Residential Trane and American Standard units made from 2010 have a 10-character serial starting with year (two digits) and week (two digits). 2002\u20132009 units have a 9-character serial starting with a one-digit year and two-digit week. Older units use a letter code for the year.',
  'Example: <b>1623</b>xxxxxx = week 23 of 2016. <b>752</b>xxxxxx (9 characters) = week 52 of 2007.', 'Trane Commercial Help Center (serial date codes); inspector references', 'https://support.trane.com/hc/en-us/articles/44514808922893-How-to-read-a-Light-Commercial-Unit-Serial-Number-Date-Code', '1623A1234X'),
 ('rheem-hvac', 'Rheem & Ruud HVAC', 'rheemhvac', 'HVAC unit', 'Rheem and Ruud air conditioners, heat pumps and furnaces built since November 2013 use a serial with a plant letter, a two-digit week, a two-digit year and a production number. Older serials are longer but contain the same week + year after a letter.',
  'Example: F <b>0813</b> 9999 = plant F (Fort Smith, AR), week 8 of 2013.', 'Rheem serial number nomenclature (as published in Rheem literature)', 'https://www.rheem.com/rheem_model_serial_numbers/', 'F08139999'),
]

def age_examples(kind, n):
    rows = []
    for y in (2006, 2009, 2012, 2015, 2018, 2020, 2022, 2024, 2025):
        mo, wkn = 3 + (y % 9), 10 + (y % 40)
        yy = f'{y % 100:02d}'
        ex = {'bw': (BW_Y[(y - 2004) % 20] + 'ABCDEFGHJKLM'[mo - 1] + '\u2026', f'{MON[mo - 1]} {y} (or {y - 20})'),
              'mmyy': (f'{mo:02d}{yy}\u2026', f'{MON[mo - 1]} {y}'), 'yyww': (f'{yy}{wkn:02d}\u2026', f'week {wkn} of {y}'),
              'wwyy': (f'{wkn:02d}{yy}\u2026', f'week {wkn} of {y}'), 'yymm': (f'{yy}{mo:02d}\u2026', f'{MON[mo - 1]} {y}'),
              'lennox': (f'59{yy}{"ABCDEFGHJKLM"[mo - 1]}\u2026', f'{MON[mo - 1]} {y}'), 'trane': (f'{yy}{wkn:02d}\u2026 (10 characters)' if y >= 2010 else f'{y % 10}{wkn:02d}\u2026 (9 characters)', f'week {wkn} of {y}'),
              'rheemhvac': (f'F{wkn:02d}{yy}\u2026', f'week {wkn} of {y}' if y >= 2013 else 'older format')}[kind]
        rows.append(ex)
    return (f'<h2>{esc(n)} serial number date examples</h2><p>How the start of the serial reads for units built in different years (the rest of the serial is a production number and does not affect the date):</p>'
            + table(['Serial begins with', 'Manufactured'], rows)
            + '<p>Digits that do not fit the pattern (for example a \u201cmonth\u201d of 14 or a week of 60) mean the serial uses a different or older format; check for a printed date on the label or ask the manufacturer.</p>')

def age_pages():
    def decoder(kind, example):
        return f'''<section class="tool"><h2>Decode a serial number</h2><div class="calc" data-tool="age" data-kind="{kind}"><div class="row">
<label>Serial number <input type="text" data-sn value="{example}" autocapitalize="characters" spellcheck="false"></label></div>
<output class="res" data-out aria-live="polite"></output></div></section>'''
    allb = [(f'/{s}-water-heater-age/', f'{n} water heater age') for s, n, *_ in WH] + [(f'/{s}-age-by-serial-number/', f'{n} age by serial') for s, n, *_ in HV]
    for group, items, suffix, hub in ((WH, WH, 'water-heater-age', '/water-heater-age/'), (HV, HV, 'age-by-serial-number', '/hvac-age-by-serial-number/')):
        for s, n, kind, typ, rule, ex, src, srcurl, example in items:
            path = f'/{s}-{suffix}/'
            wh = typ == 'Water heater'
            title = f'{n} {"Water Heater Age" if wh and not n.endswith("Water Heater") else "Age"} by Serial Number (Decoder)'
            desc = f'Find the age of a {n} {"water heater" if wh else "AC, heat pump or furnace"} from its serial number. Free decoder, format examples and the manufacturer source.'
            if len(desc) > 159: desc = desc[:156].rsplit(' ', 1)[0] + '.'
            bwt = age_examples(kind, n)
            if kind == 'bw':
                bwt = '<h2>Bradford White year and month letters</h2>' + table(['Letter', 'Year', 'Month letter', 'Month'],
                      [(y, f'{1984 + i} or {2004 + i}', 'ABCDEFGHJKLM'[i] if i < 12 else '', MON[i] if i < 12 else '') for i, y in enumerate(BW_Y)])
            life = ('<p><b>How long do water heaters last?</b> The U.S. Department of Energy puts the life of a storage (tank) water heater at roughly 10\u201315 years and tankless units at 20 years or more; water quality, maintenance and installation shift that a lot. '
                    'Age alone does not mean a heater must be replaced, but an older tank with rust at the fittings, rumbling or water on the floor should be evaluated.</p>') if wh else (
                    '<p><b>Why the age matters.</b> Age helps decide repair versus replace, estimate remaining warranty (most manufacturer warranties run from installation date with registration, or from manufacture date if not registered), and tells you which refrigerant the unit likely uses: most residential A/C built before 2010 used R-22, units from 2010 to 2024 mostly R-410A, and new systems from 2025 increasingly use A2L refrigerants such as R-454B or R-32. Check the rating plate for the actual refrigerant.</p>')
            faqs = [(f'How do I tell the age of a {n} {"water heater" if wh else "unit"}?', re.sub('<[^>]+>', '', rule)),
                    ('Where is the serial number?', 'On the rating plate: for tank water heaters it is the label on the front of the jacket near the controls; for outdoor units it is on the data plate on the side or back panel; furnaces have it inside the blower door.' ),
                    ('Is the manufacture date the install date?', 'No. Units can sit in a warehouse for months. For warranty, manufacturers use the installation date if the product was registered, so keep your invoice.')]
            body = f'''<article><h1>{esc(n)} {"Water Heater Age" if wh else "Age"} by Serial Number</h1>
<p class="lead">{rule}</p>
{decoder(kind, example)}
<p>{ex}</p>
{bwt}
<h2>How to read it step by step</h2>
<ol><li>Find the rating plate and copy the serial number exactly (not the model number).</li><li>Type it in the decoder above or read the characters described on this page.</li>
<li>Sanity-check the result: the unit cannot be newer than the house addition it serves or older than the refrigerant/standards printed on the plate.</li>
<li>If the plate shows a printed manufacture date, that date overrides any decoding.</li></ol>
{life}
<h2>Where to find the {"rating plate" if wh else "data plate"}</h2>
<p>{"On tank water heaters the rating plate is the large label on the front of the jacket, normally above the gas control or the upper heating element cover. On tankless units it is on the side or inside the front cover. The plate lists the model number, serial number, capacity, input rating and the fuel or voltage; the serial number is usually printed with a barcode." if wh else "On outdoor condensers and heat pumps the data plate is on a side or rear panel, often near the service valves or the electrical access panel. On furnaces and air handlers it is inside the blower or burner compartment door. Write down the model number too: it tells you capacity (tons or Btu/h), efficiency series and the refrigerant."}</p>
<h2>What to do with the age</h2>
<ul><li>Check warranty: register new equipment, and keep the installation invoice; many warranties are longer when registered.</li><li>Plan replacement before failure on older equipment, especially before summer or winter peak season.</li><li>Look up the right parts and service literature for that production period.</li><li>For home inspections, report the decoded date and the method used, and note any uncertainty about the decade.</li></ul>
<h2>Source</h2>
<p>{esc(src)}: <a href="{srcurl}" rel="noopener">{esc(srcurl.split("/")[2])}</a>. Formats change over time; when in doubt, the manufacturer\u2019s warranty lookup with the full serial number gives the authoritative date.</p>
<h2>Other brands</h2>
{links([x for x in allb if x[0] != path][:12])}
{faq_html(faqs)}
</article>'''
            page(path, title, desc, body, crumbs=[('Age by Serial', '/age-by-serial-number/'), (('Water heaters' if wh else 'HVAC'), hub), (n, path)],
                 section='/age-by-serial-number/', schema=[app_ld(f'{n} serial number age decoder', desc, path), faq_ld(faqs)])
    for hub, items, h1, kind, d in (('/water-heater-age/', WH, 'Water Heater Age by Serial Number', 'water heater', 'Find any water heater\u2019s age from its serial number: Bradford White, Rheem, Ruud, A.O. Smith, State, American, Whirlpool, Richmond and GE.'),
                                     ('/hvac-age-by-serial-number/', HV, 'HVAC Age by Serial Number', 'AC, heat pump or furnace', 'Find the age of an AC, heat pump or furnace from the serial number: Carrier, Bryant, Payne, Goodman, Amana, Lennox, Trane, American Standard, Rheem, Ruud.')):
        suffix = 'water-heater-age' if items is WH else 'age-by-serial-number'
        rows = [(f'<a href="{url(f"/{s}-{suffix}/")}">{esc(n)}</a>', esc(re.sub('<[^>]+>', '', ex))) for s, n, kind_, typ, rule, ex, *_ in items]
        body = f'''<article><h1>{h1}</h1><p class="lead">Pick the brand on the rating plate. Each page explains where the date hides in that maker\u2019s serial number, gives a decoder and links the manufacturer source.</p>
{table(['Brand', 'How the date is coded (example)'], rows)}
<h2>Brands not listed</h2><p>We only publish decoders for formats documented by the manufacturer or a recognised inspector association. For other brands (for example Rinnai, Navien or York) use the manufacturer\u2019s warranty lookup with the full serial number, or call their support line.</p>
{links([('/age-by-serial-number/', 'All age-by-serial decoders')])}</article>'''
        page(hub, f'{h1} (All Brands Decoder)', d[:159], body, crumbs=[('Age by Serial', '/age-by-serial-number/'), (h1.split(' by')[0], hub)], section='/age-by-serial-number/')
    body = f'''<article><h1>Age by Serial Number</h1><p class="lead">Decode the manufacture date hidden in water heater and HVAC serial numbers. Every decoder cites the manufacturer or inspector-association source it follows.</p>
<h2>Water heaters</h2>{links([(f'/{s}-water-heater-age/', n) for s, n, *_ in WH])}
<h2>Air conditioners, heat pumps and furnaces</h2>{links([(f'/{s}-age-by-serial-number/', n) for s, n, *_ in HV])}
<h2>Tips</h2><ul><li>Use the serial number, not the model number.</li><li>A printed date on the label beats any decoding.</li><li>Letter-coded years can repeat (Bradford White every 20 years): use the unit\u2019s condition and the house history to pick the right decade.</li></ul>
<p>Guide: <a href="{url('/blog/how-to-tell-water-heater-age/')}">how to tell the age of a water heater</a>.</p></article>'''
    page('/age-by-serial-number/', 'Age by Serial Number: Water Heater & HVAC Decoders', 'Free age-by-serial-number decoders for water heaters (Bradford White, Rheem, A.O. Smith\u2026) and HVAC units (Carrier, Goodman, Lennox, Trane, Rheem).',
         body, crumbs=[('Age by Serial', '/age-by-serial-number/')], section='/age-by-serial-number/')

import re

def welding_pages():
    mig = [('24 ga (0.024 in)', 24), ('22 ga (0.030 in)', 30), ('18 ga (0.048 in)', 48), ('16 ga (0.060 in)', 60), ('14 ga (0.075 in)', 75), ('12 ga (0.105 in)', 105),
           ('1/8 in (0.125 in)', 125), ('3/16 in (0.188 in)', 188), ('1/4 in (0.250 in)', 250)]
    WIRE = [('.023', 3.5, 30, 130), ('.030', 2.0, 40, 145), ('.035', 1.6, 50, 180), ('.045', 1.0, 75, 250)]
    rows = []
    for lab, a in mig:
        cells = [lab, f'{a} A']
        for w, m, lo, hi in WIRE:
            cells.append(f'{a * m:.0f} ipm' if lo <= a <= hi else '\u2014')
        rows.append(cells)
    volt = [('0.023 in', '20.0/480', '18.3/350', '18.0/240', '17.0/190', '15.8/125'), ('0.030 in', '19.0/290', '18.0/250', '17.3/200', '16.3/115', '15.9/95'),
            ('0.035 in', '18.4/265', '17.4/230', '16.5/190', '15.8/120', '15.0/88'), ('0.045 in', '17.5/195', '17.2/190', '16.5/165', '15.5/95', '\u2014')]
    faqs = [('How many amps for 1/8 inch steel MIG?', 'About 125 A by Miller\u2019s rule of 1 amp per 0.001 in of thickness. With .030 wire that is about 250 ipm wire speed, with .035 about 200 ipm.'),
            ('What wire size should I use?', 'Miller recommends .023 in for 30\u2013130 A, .030 in for 40\u2013145 A, .035 in for 50\u2013180 A and .045 in for 75\u2013250 A. Choose the wire that covers your most common thickness.'),
            ('Is this better than my door chart?', 'No. The chart inside your welder\u2019s door is written for that machine and should be your first reference. Use these rules when you have no chart, then fine-tune on scrap.')]
    body = f'''<article><h1>MIG Welder Settings Calculator</h1>
<p class="lead">Enter material thickness and wire diameter for a starting amperage and wire feed speed on mild steel, using Miller Electric\u2019s published rules of thumb. Then fine-tune voltage on scrap with your machine\u2019s door chart.</p>
<section class="tool"><h2>Starting settings</h2><div class="calc" data-tool="mig"><div class="row">
<label>Thickness (in) <input type="number" inputmode="decimal" step="any" data-th value="0.125"></label>
<label>Wire <select data-w><option value=".023">.023 in</option><option value=".030">.030 in</option><option value=".035" selected>.035 in</option><option value=".045">.045 in</option></select></label></div>
<output class="res" data-out aria-live="polite"></output></div></section>
<h2>The three rules</h2>
<ol><li><b>Amperage from thickness:</b> about 1 amp for every 0.001 in of material (1/8 in = 125 A).</li>
<li><b>Wire size from amperage:</b> .023 in 30\u2013130 A; .030 in 40\u2013145 A; .035 in 50\u2013180 A; .045 in 75\u2013250 A.</li>
<li><b>Wire feed speed from amperage:</b> multiply amps by 3.5 (.023), 2 (.030), 1.6 (.035) or 1 (.045) inches per minute per amp.</li></ol>
<h2>Starting wire speed by thickness (mild steel, solid wire)</h2>
{table(['Thickness', 'Amps', '.023 wire', '.030 wire', '.035 wire', '.045 wire'], rows)}
<h2>Miller starting voltage / wire speed (steel, ER70S-6, 75% Ar / 25% CO2)</h2>
{table(['Wire', '3/16 in V/ipm', '1/8 in V/ipm', '14 ga V/ipm', '18 ga V/ipm', '22 ga V/ipm'], volt)}
<p>Wire stick-out about 3/8 in for short-circuit transfer. Flux-cored wire, stainless and aluminum need different settings; follow the wire maker\u2019s data.</p>
<p class="src">Sources: Miller Electric, \u201cMIG Welding: Setting the Correct Parameters\u201d (millerwelds.com) and Miller Canada \u201cMIG welding parameter choices\u201d table (millerwelds.ca). Starting points only; test on scrap.</p>
{faq_html(faqs)}
</article>'''
    page('/mig-welding-settings-calculator/', 'MIG Welder Settings Calculator: Amps & Wire Speed by Thickness', 'MIG welding settings calculator for mild steel: amperage, wire size and wire feed speed by thickness using Miller rules, plus a voltage starting chart.',
         body, crumbs=[('Welding', '/welding/'), ('MIG settings calculator', '/mig-welding-settings-calculator/')], section='/welding/',
         schema=[app_ld('MIG settings calculator', 'MIG starting settings', '/mig-welding-settings-calculator/'), faq_ld(faqs)])
    tung = [('1/16 in (1.6 mm)', '50\u2013140 A', '60\u201390 A'), ('3/32 in (2.4 mm)', '125\u2013200 A', '125\u2013160 A'), ('1/8 in (3.2 mm)', '150\u2013325 A', '190\u2013240 A'),
            ('3/16 in (4.8 mm)', '300\u2013340 A', '260\u2013320 A'), ('1/4 in (6.4 mm)', '\u2014', '330\u2013450 A')]
    th = [('22 ga (0.030 in)', 30), ('18 ga (0.048 in)', 48), ('16 ga (0.060 in)', 60), ('14 ga (0.075 in)', 75), ('1/8 in (0.125 in)', 125), ('3/16 in (0.188 in)', 188), ('1/4 in (0.250 in)', 250)]
    def tg(a):
        return '1/16 in' if a <= 90 else '3/32 in' if a <= 160 else '1/8 in'
    trows = [(lab, f'about {a} A', tg(a)) for lab, a in th]
    faqs = [('How many amps to TIG weld 1/8 inch steel?', 'A common starting point is about 1 amp per 0.001 in of thickness, so roughly 125 A for 1/8 in mild steel, adjusted with the foot pedal.'),
            ('Which tungsten size for 150 amps?', 'Per Miller\u2019s table, 3/32 in 2% tungsten covers about 125\u2013200 A; 1/8 in covers about 150\u2013325 A.')]
    body = f'''<article><h1>TIG Welding Amperage Chart</h1>
<p class="lead">Starting TIG amperage by steel thickness and the current range of each tungsten diameter. Use a foot pedal or remote to fine-tune from these numbers.</p>
<h2>Starting amperage by thickness (mild steel, DCEN)</h2>
{table(['Thickness', 'Starting amperage', 'Suggested tungsten'], trows)}
<p>The thickness rule here is the same 1 amp per 0.001 in guideline Miller publishes for MIG, widely used as a TIG starting point on steel. Stainless usually needs a little less current; aluminum (AC) needs more and depends heavily on balance and frequency settings, so follow your machine\u2019s guide.</p>
<h2>Tungsten current ranges (Miller)</h2>
{table(['Tungsten diameter', '2% (thoriated/ceriated/lanthanated)', 'Pure tungsten'], tung)}
<h2>Tips</h2><ul><li>Grind the tungsten lengthwise to a point for DC; the included angle changes the arc shape.</li><li>Typical argon flow is 15\u201325 cfh; more is not better and can pull in air.</li><li>Use filler rod no thicker than the base metal for thin sheet.</li></ul>
{links([('/mig-welding-settings-calculator/', 'MIG settings calculator'), ('/welding/', 'All welding references')])}
<p class="src">Source: Miller Electric amperage tables for tungsten electrodes (\u201cAmperage for TIG welding\u201d), Miller MIG parameter guide for the thickness rule.</p>
{faq_html(faqs)}
</article>'''
    page('/tig-welding-amperage-chart/', 'TIG Welding Amperage Chart: Amps by Thickness & Tungsten', 'TIG welding amperage chart: starting amps for steel from 22 ga to 1/4 in, suggested tungsten size and Miller tungsten current ranges.',
         body, crumbs=[('Welding', '/welding/'), ('TIG amperage chart', '/tig-welding-amperage-chart/')], section='/welding/', schema=[article_ld('TIG welding amperage chart', 'TIG amps', '/tig-welding-amperage-chart/'), faq_ld(faqs)])
    body = f'''<article><h1>Welding Settings Charts</h1><p class="lead">Starting settings for MIG and TIG from manufacturer guidance. Your machine\u2019s door chart comes first; these help when it is missing or does not cover your thickness.</p>
{links([('/mig-welding-settings-calculator/', 'MIG settings calculator (amps, wire speed, voltage)'), ('/tig-welding-amperage-chart/', 'TIG amperage chart')])}
<h2>Machine-specific charts</h2><p>We will add machine door charts only where the manufacturer publishes the chart in a public manual, with the manual cited on the page.</p></article>'''
    page('/welding/', 'Welding Settings Charts: MIG & TIG Starting Points', 'MIG and TIG welding reference: starting amps, wire feed speed, voltage and tungsten size from Miller\u2019s published guidance.',
         body, crumbs=[('Welding', '/welding/')], section='/welding/')
