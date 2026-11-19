"""Posts 25, 26, 27 (run 2026-11-19)."""
from core import url, table, esc
from posts5 import L, X, sources
from pages_hvac import BY, pf, ps, glide

NEW_POSTS = [
 ('how-old-is-my-ac-unit-serial-number', 'How Old Is My AC Unit? Serial Number Basics for 5 Major Brands',
  'Find the data plate, read the date code and work out your AC or furnace age: Carrier, Goodman, Lennox, Rheem and Trane formats, worked examples and caveats.', '2026-11-19'),
 ('bradford-white-serial-number-year-letter-code', 'Bradford White Serial Number: The 20-Year Letter Code Explained',
  'Read a Bradford White serial number: the year letter (repeats every 20 years), the month letter, worked examples and how to pick the right decade.', '2026-11-19'),
 ('r22-systems-repair-retrofit-or-replace', 'R-22 Systems Today: Repair, Retrofit or Replace?',
  'What EPA says about R-22 air conditioners after the 2020 ban, why there is no drop-in refrigerant, and how R-22 pressures compare with R-410A.', '2026-11-19'),
]

BW_Y = 'A B C D E F G H J K L M N P S T W X Y Z'.split()
MON = 'January February March April May June July August September October November December'.split()
BW_M = 'A B C D E F G H J K L M'.split()


def bodies():
    b = {}

    # ---- Post 25: AC age ----
    b['how-old-is-my-ac-unit-serial-number'] = f'''
<p class="lead">The manufacture date of an air conditioner, heat pump or furnace is printed on the unit, but not as a date. It is hidden inside the serial number. Each brand uses its own layout, so the first job is knowing which characters to read. Here is how to find the data plate, decode five major brands, and what the answer means for repair-or-replace decisions.</p>
<h2>Step 1: find the data plate</h2>
<p>For a central air conditioner or heat pump, the nameplate is usually on the outdoor condenser, on a side or back panel. EPA\u2019s homeowner guidance says the same plate normally lists the refrigerant too. Furnaces and air handlers carry theirs inside the blower door. Copy the <b>serial number</b>, not the model number printed beside it. They look alike and people mix them up all the time.</p>
<h2>Step 2: match the brand to its date code</h2>
{table(['Brand family', 'Where the date sits', 'Example'], [
 ('Carrier, Bryant, Payne', 'First four digits: week, then year (widely used; Carrier does not publish it)', '3112U12345 = week 31 of 2012'),
 ('Goodman, Amana, Daikin', 'First four digits: year, then month', '1306123456 = June 2013'),
 ('Lennox', 'Plant code (2 digits), year (2 digits), month letter (A = January, B = February\u2026)', '5921CO05716 = 2021, March'),
 ('Rheem, Ruud', 'Week then year, four digits after a letter in the middle of the serial', 'M0106\u2026 = week 1 of 2006'),
 ('Trane, American Standard', 'Newer units appear to start with year then week; confirm with Trane', '1623\u2026 = week 23 of 2016'),
])}
<p>The Goodman rule comes from Goodman\u2019s retailer documentation (2110 means October 2021). The Lennox layout, including the 59 21 CO 05716 example, is from Lennox\u2019s model and serial identification guide. Carrier and Bryant\u2019s week-then-year pattern appears in an Energy Trust of Oregon equipment age guide (3298xxxxxx is the 32nd week of 1998). Several brands, including Carrier and Trane, do not publish a residential serial format, which is why this table says so where it applies. For a warranty claim or insurance question, ask the manufacturer with the full serial number.</p>
<p>Our brand pages decode these for you: {L('/carrier-age-by-serial-number/', 'Carrier')}, {L('/goodman-age-by-serial-number/', 'Goodman')}, {L('/lennox-age-by-serial-number/', 'Lennox')}, {L('/trane-age-by-serial-number/', 'Trane')} and {L('/rheem-hvac-age-by-serial-number/', 'Rheem and Ruud')}.</p>
<h2>Worked examples</h2>
<p>Each example is read as of November 2026.</p>
<ul>
<li><b>Carrier 3112U12345:</b> digits 1\u20132 are the week (31), digits 3\u20134 the year (12), so week 31 of 2012, around early August. The unit is about 14 years old.</li>
<li><b>Goodman 1306123456:</b> year 13, month 06, so June 2013, about 13 years old.</li>
<li><b>Lennox 5921CO05716:</b> plant 59 is Marshalltown, Iowa, year 21 is 2021, and month letter C is March. About 5 years old. Note that the first two digits are a plant, not a date.</li>
</ul>
<h2>What the age tells you</h2>
<p><b>Refrigerant.</b> EPA says equipment containing R-22 could not be manufactured in the U.S. after January 1, 2010. A central air conditioner built before 2010 very likely holds R-22; one built from 2010 onward most likely holds R-410A, which EPA calls the most common alternative in new residential systems. New systems from 2025 increasingly use lower-GWP refrigerants such as R-454B. Always confirm on the nameplate. If you find R-22, read our guide to {L('/blog/r22-systems-repair-retrofit-or-replace/', 'repairing, retrofitting or replacing an R-22 system')}, and see the {L('/r22-pt-chart/', 'R-22 PT chart')}, {L('/r410a-pt-chart/', 'R-410A PT chart')} and {L('/r454b-pt-chart/', 'R-454B PT chart')} for the pressures.</p>
<p><b>Lifespan.</b> The U.S. Department of Energy puts a central air conditioner at 15 to 20 years. ENERGY STAR suggests having a contractor evaluate a heat pump or air conditioner once it is more than 10 years old, and a furnace or boiler once it is more than 15. Age is a reason to ask questions, not an automatic verdict: frequent repairs and rising bills matter as much as the calendar.</p>
<p><b>Warranty.</b> Manufacturers generally start the warranty from the installation date when the unit was registered, and from the manufacture date when it was not. A unit can also sit in a warehouse for months, so the stamped date is when it was built, not when it was installed.</p>
<h2>Bonus: read the capacity from the model number</h2>
<p>Energy Trust\u2019s guide gives a rule of thumb for size. Manufacturers usually put the nominal capacity in Btu/h (in thousands) somewhere in the model number as a two-digit number divisible by 6. Divide it by 12 to get tons. For example, Energy Trust\u2019s sample model 56BAB0042000A0 contains 42, which means 42,000 Btu/h, or 3.5 tons. Some brands use other codes, so treat it as a quick estimate. To check whether the ductwork and charge match that size, use the {L('/hvac-calculators/', 'HVAC calculators')}.</p>
<h2>Common mistakes</h2>
<ul>
<li>Reading the model number instead of the serial number.</li>
<li>Applying one brand\u2019s format to another brand\u2019s unit, such as reading a Lennox plant code as a year.</li>
<li>Forgetting the decade. A two-digit year such as 05 can only be 2005 on a modern plate, but older serials from the 1970s and 1980s use letter codes, so a very old unit needs the brand-specific chart.</li>
<li>Treating the manufacture date as the install date.</li>
</ul>
{sources([('https://insider.energytrust.org/wp-content/uploads/CPF_Age_Information.pdf', 'Energy Trust of Oregon: Age information for air conditioners (serial and model number codes)'), ('https://www.hvacbase.org/hvac-serial-number-decoder', 'HVACBase: how to decode your HVAC serial number, by brand (Lennox guide, Rheem CPSC date code, lifespan figures)'), ('https://hvacdirect.com/knowledge-base/how-do-i-find-my-date-of-manufacture-/', 'HVACDirect: Goodman date of manufacture (first four digits)'), ('https://www.epa.gov/ods-phaseout/homeowners-and-consumers-frequently-asked-questions', 'EPA: Homeowners and consumers FAQ on HCFC-22'), ('https://www.epa.gov/ods-phaseout/equipment-manufacturers-importers-and-exporters-frequent-questions', 'EPA: equipment manufacturers FAQ (no R-22 equipment manufactured after January 1, 2010)')])}
'''

    # ---- Post 26: Bradford White ----
    yrows = [(y, f'{2004 + i} or {2024 + i}') for i, y in enumerate(BW_Y)]
    yt = table(['Year letter', 'Year', 'Year letter', 'Year'], [(yrows[i][0], yrows[i][1], yrows[i + 10][0], yrows[i + 10][1]) for i in range(10)])
    mt = table(['Month letter', 'Month', 'Month letter', 'Month'], [(BW_M[i], MON[i], BW_M[i + 6], MON[i + 6]) for i in range(6)])
    b['bradford-white-serial-number-year-letter-code'] = f'''
<p class="lead">Bradford White makes dating a water heater easier than most brands: the first two characters of the serial number are the year and the month, and the manufacturer publishes the chart. The catch is that the year letters repeat every 20 years, so the same letter can mean two different decades. Here is how to read it and how to pick the right one.</p>
<h2>Where to find the serial number</h2>
<p>Look for the rating plate on the front of the water heater, near the controls. It lists the model number and the serial number. Bradford White\u2019s own My Water Heater page shows where each sits. Use the serial number, not the model number.</p>
<h2>The year letter (first character)</h2>
<p>The first character is a letter for the year of manufacture. Bradford White does not use the letters I, O, Q, R, U or V for years, which leaves 20 letters. Each appears twice on the company\u2019s chart, 20 years apart:</p>
{yt}
<h2>The month letter (second character)</h2>
<p>The second character is the month. Bradford White does not use I, or any letter from N to Z, for the month, so only twelve letters appear:</p>
{mt}
<p>Our {L('/bradford-white-water-heater-age/', 'Bradford White age decoder')} does this lookup for you, and the {L('/water-heater-age/', 'water heater age hub')} covers Rheem, A.O. Smith, State, American and more.</p>
<h2>Worked examples</h2>
<p>Ages below are as of November 2026.</p>
<ul>
<li><b>HK16433183.</b> H = 2011 (or 2031, which has not happened yet). K = October. So October 2011, about 15 years old.</li>
<li><b>TD\u2026</b> T = 2019, D = April. April 2019, about 7 and a half years old.</li>
<li><b>XB\u2026</b> X = 2021, B = February. February 2021, nearly 6 years old.</li>
<li><b>CE\u2026</b> C = 2006 or 2026, E = May. This could be May 2006, a 20-year-old heater, or May 2026, a brand-new one. This is the tricky case.</li>
</ul>
<h2>The decade problem: 2006 or 2026?</h2>
<p>Because the letters repeat, a heater with an A, B or C year letter today could have been built in 2004\u20132006 or in 2024\u20132026. Every letter will have this issue as the years pass. Ways to decide:</p>
<ol>
<li><b>Condition.</b> A tank that is 20 years old shows it: rust at the fittings and bottom, sediment noise, scale on the anode port, and a faded label. A 2-year-old tank looks clean.</li>
<li><b>Warranty lookup.</b> Bradford White\u2019s My Water Heater page has a warranty search that takes the serial number. A real new heater returns warranty information.</li>
<li><b>House history.</b> If the home was built in 2015, a 2006 heater would have been moved there, which is unlikely.</li>
<li><b>Paperwork.</b> Permits, receipts and the installer\u2019s sticker usually show the install date.</li>
<li><b>Ask the manufacturer.</b> Give Bradford White the full serial number.</li>
</ol>
<p>Bradford White\u2019s published chart begins at 2004. Older units use the same letter sequence but the company chart does not list them, so for a pre-2004 heater confirm the date with the manufacturer.</p>
<h2>Sanity checks that catch misreads</h2>
<ul>
<li>If the first character is I, O, Q, R, U or V, it is not a Bradford White year letter. You may have read a different line, or the heater is another brand.</li>
<li>If the second character is a letter from N to Z, or the letter I, it is not a valid month. Recheck the characters, since a zero and an O are easy to mix up.</li>
<li>A heater that decodes to a date in the future is a wrong reading or the other decade.</li>
</ul>
<h2>What the age means</h2>
<p>Tank-type water heaters are generally planned around 10 to 15 years of service, the range used on our decoder pages. Water quality and maintenance shift that a lot. If your heater is 15 or more, watch for water at the base, rumbling from sediment and rusty hot water. See {L('/blog/how-to-tell-water-heater-age/', 'how to tell the age of a water heater')} for the other major brands.</p>
{sources([('https://www.bradfordwhite.com/my-water-heater/', 'Bradford White: My Water Heater (determine the age, year and month letters, serial number location)')])}
'''

    # ---- Post 27: R-22 ----
    names = ['r22', 'r410a', 'r407c', 'r422d', 'r438a']
    rows = []
    for n in names:
        r = BY[n]
        g = glide(r, 40)
        rows.append((r['name'], ps(pf(r, 45, 1)), ps(pf(r, 105, 0)), f'{g:.1f} \u00b0F' if g and g > 0.5 else 'under 1 \u00b0F', r['gwp']))
    pt = table(['Refrigerant', 'Suction side: dew psig at 45 \u00b0F', 'Liquid side: bubble psig at 105 \u00b0F', 'Glide at 40 \u00b0F', 'GWP'], rows)
    b['r22-systems-repair-retrofit-or-replace'] = f'''
<p class="lead">R-22 has not been made in the United States since the start of 2020, yet millions of R-22 air conditioners are still running. The rules are less dramatic than the headlines: you may keep using an R-22 system, you may keep servicing it, and there is no drop-in refrigerant if you decide to change. Here is what EPA actually says and how to think about the choice.</p>
<h2>What the rules say</h2>
<ul>
<li>U.S. production and import of R-22 (HCFC-22) ended on January 1, 2020. You may continue to use R-22 in an existing system for as long as necessary.</li>
<li>Servicing continues from recovered and reclaimed R-22 and from stock produced before 2020. EPA expects it to be available well beyond 2020, but notes that price and availability may change.</li>
<li>Equipment holding R-22 could not be manufactured after January 1, 2010. A central air conditioner on the original R-22 charge is therefore at least 16 years old in 2026.</li>
<li>EPA does not require homeowners to replace or convert an R-22 system.</li>
<li>Only Section 608-certified technicians can buy and handle the refrigerant. It is illegal to knowingly vent it.</li>
<li>If an outdoor unit fails, EPA says owners may replace the condensing unit, as long as the R-22 unit meets the regional efficiency standard.</li>
</ul>
<h2>There is no drop-in replacement</h2>
<p>EPA is blunt about this: there are no \u201cdrop-in\u201d replacements for HCFC-22, and alternative refrigerants will not work well without changes to system components. A retrofit is allowed only with a refrigerant EPA has listed as acceptable under the SNAP program for that use. The technician must recover the remaining R-22 first, follow the manufacturer\u2019s guidelines for the new refrigerant, and explain how performance and energy use may change. Most leak repairs end up recharged with R-22, because that avoids the changes a conversion needs.</p>
<p>Never use \u201cR-22a\u201d or similar products sold as a cheap R-22 substitute. EPA says R-22a is a flammable hydrocarbon blend, not an acceptable alternative, and an R-22 system has no safety features for flammability.</p>
<h2>How the pressures compare</h2>
<p>Saturation pressures show why you cannot swap refrigerants casually. These values come from our PT chart data:</p>
{pt}
<p>R-410A runs far higher than R-22: about {ps(pf(BY['r410a'], 45, 1))} psig on the suction side at 45\u00b0F versus {ps(pf(BY['r22'], 45, 1))} psig for R-22, and {ps(pf(BY['r410a'], 105, 0))} versus {ps(pf(BY['r22'], 105, 0))} psig on the liquid side at 105\u00b0F. An R-22 system is not built for those pressures, so R-410A is not a retrofit for an R-22 system; it needs a new outdoor unit and a matched indoor coil, and new R-410A equipment is itself being replaced by lower-GWP refrigerants. Retrofit blends such as R-407C, R-422D and R-438A run at pressures close to R-22, but they have temperature glide, so you must charge by liquid and compare against the dew or bubble column that matches the side you are reading. Read {L('/blog/refrigerant-temperature-glide/', 'temperature glide explained')} and see {L('/r22-vs-r410a/', 'R-22 vs R-410A')} and {L('/r407c-vs-r22/', 'R-407C vs R-22')}.</p>
<h2>Repair, retrofit or replace?</h2>
<p>This is a judgement call, and EPA leaves it to the owner. Questions that settle most cases:</p>
<ol>
<li><b>Where is the leak, and can it be fixed?</b> EPA recommends finding and repairing leaks instead of topping off. If the leak is in the evaporator or condenser coil, the repair may cost more than the equipment is worth.</li>
<li><b>How old is the system?</b> A central system built to run on R-22 was built before 2010, so it is at least 16 years old. The DOE puts central air conditioner life at 15 to 20 years, so it is near the end either way. Check the serial number using {L('/blog/how-old-is-my-ac-unit-serial-number/', 'how old is my AC unit')}.</li>
<li><b>What is a pound of R-22 costing now?</b> Ask for a written price for the charge and for the repair, since the price changes.</li>
<li><b>What would a retrofit change?</b> Ask the contractor which SNAP-listed refrigerant, what component changes, and what happens to capacity and efficiency.</li>
<li><b>What does the replacement cost?</b> A new system matched to a current refrigerant is the long-term fix, and EPA says an ENERGY STAR model can cut annual energy bills by more than $160, depending on where you live.</li>
</ol>
<p>A small leak on a sound system that is otherwise reliable can justify a repair and recharge for a few more years. A coil leak, a compressor failure or repeated top-ups are the situations where owners most often weigh replacement. A retrofit can make sense where replacing everything is costly, as long as the contractor can name the SNAP-listed refrigerant and the component changes.</p>
<h2>If you are the technician</h2>
<p>Recover the existing refrigerant before opening the circuit, record the amount, and use a leak check before recharging. Do not top off an R-22 system with a different refrigerant; mixing contaminates the charge. When retrofitting, label the system with the new refrigerant and use the correct PT column for that blend.</p>
{sources([('https://www.epa.gov/ods-phaseout/homeowners-and-consumers-frequently-asked-questions', 'EPA: Homeowners and consumers FAQ (no drop-in replacements, retrofit rules, condensing unit replacement)'), ('https://www.epa.gov/sites/default/files/2020-03/documents/residential_air_conditioning_and_the_phaseout_of_hcfc-22_what_you_need_to_know_final_508.pdf', 'EPA: Residential Air Conditioning and the Phaseout of HCFC-22 (2020 fact sheet)'), ('https://www.epa.gov/ods-phaseout/equipment-manufacturers-importers-and-exporters-frequent-questions', 'EPA: Equipment manufacturers FAQ (January 1, 2010 manufacturing rule)'), ('https://www.epa.gov/ods-phaseout/technicians-and-contractors-frequent-questions', 'EPA: Technicians and contractors FAQ (servicing and availability)'), ('https://www.hvacbase.org/hvac-serial-number-decoder', 'HVACBase: HVAC system lifespan (DOE 15 to 20 years for a central air conditioner)')])}
'''
    return b


FAQS = {
 'how-old-is-my-ac-unit-serial-number': [
  ('Where is the serial number on an AC unit?', 'On the data plate of the outdoor condenser, usually on a side or back panel. Furnaces and air handlers carry it inside the blower door.'),
  ('How do I read a Goodman serial number?', 'The first four digits are the year then the month. For example 2110 means October 2021.'),
  ('How do I read a Carrier serial number?', 'Carrier and Bryant units commonly start with the week then the year, so 3298 is week 32 of 1998. Carrier does not publish the format, so confirm for warranty claims.'),
  ('How long does a central air conditioner last?', 'The U.S. Department of Energy puts it at 15 to 20 years. ENERGY STAR suggests having a contractor evaluate one past 10 years.'),
  ('Is the manufacture date the install date?', 'No. Units can wait in a warehouse for months. Warranties usually count from the registered install date.')],
 'bradford-white-serial-number-year-letter-code': [
  ('How do I read a Bradford White serial number?', 'The first character is a letter for the year and the second is a letter for the month. H K means October 2011, for example.'),
  ('Why does the same year letter appear twice?', 'Bradford White\u2019s letters repeat every 20 years, so C is 2006 or 2026 on the company chart.'),
  ('Which letters does Bradford White skip?', 'Year letters skip I, O, Q, R, U and V. Month letters skip I and everything from N to Z.'),
  ('How do I tell which decade my heater is from?', 'Use its condition, the warranty lookup on Bradford White\u2019s My Water Heater page, house history and installation paperwork.'),
  ('Where is the serial number on a Bradford White?', 'On the rating plate on the front of the water heater, near the controls, next to the model number.')],
 'r22-systems-repair-retrofit-or-replace': [
  ('Is R-22 illegal to use?', 'No. EPA says you may continue to use R-22 in an existing system for as long as necessary. Only new production and import ended on January 1, 2020.'),
  ('Can I still get R-22 for service?', 'Yes, from recovered, reclaimed and pre-2020 stock, handled by Section 608 certified technicians. EPA notes price and availability may change.'),
  ('Is there a drop-in replacement for R-22?', 'No. EPA says there are no drop-in replacements and that alternatives will not work well without changes to components.'),
  ('Can I put R-410A in an R-22 system?', 'No. R-410A runs at much higher pressure and needs equipment designed for it, so it requires a new outdoor unit and matched coil.'),
  ('What is R-22a and is it safe?', 'R-22a is a flammable hydrocarbon blend marketed as an R-22 substitute. EPA says it is not an acceptable alternative.')],
}

RELATED_GUIDES = {
 '/hvac-age-by-serial-number/': [('how-old-is-my-ac-unit-serial-number', 'How old is my AC unit'), ('r22-systems-repair-retrofit-or-replace', 'R-22 repair, retrofit or replace')],
 '/age-by-serial-number/': [('how-old-is-my-ac-unit-serial-number', 'How old is my AC unit'), ('bradford-white-serial-number-year-letter-code', 'Bradford White letter code explained')],
 '/carrier-age-by-serial-number/': [('how-old-is-my-ac-unit-serial-number', 'How old is my AC unit')],
 '/goodman-age-by-serial-number/': [('how-old-is-my-ac-unit-serial-number', 'How old is my AC unit')],
 '/lennox-age-by-serial-number/': [('how-old-is-my-ac-unit-serial-number', 'How old is my AC unit')],
 '/trane-age-by-serial-number/': [('how-old-is-my-ac-unit-serial-number', 'How old is my AC unit')],
 '/rheem-hvac-age-by-serial-number/': [('how-old-is-my-ac-unit-serial-number', 'How old is my AC unit')],
 '/bradford-white-water-heater-age/': [('bradford-white-serial-number-year-letter-code', 'Bradford White letter code explained')],
 '/water-heater-age/': [('bradford-white-serial-number-year-letter-code', 'Bradford White letter code explained')],
 '/r22-pt-chart/': [('r22-systems-repair-retrofit-or-replace', 'R-22 repair, retrofit or replace')],
 '/r22-vs-r410a/': [('r22-systems-repair-retrofit-or-replace', 'R-22 repair, retrofit or replace')],
 '/r407c-vs-r22/': [('r22-systems-repair-retrofit-or-replace', 'R-22 repair, retrofit or replace')],
 '/r407c-pt-chart/': [('r22-systems-repair-retrofit-or-replace', 'R-22 repair, retrofit or replace')],
 '/r422d-pt-chart/': [('r22-systems-repair-retrofit-or-replace', 'R-22 repair, retrofit or replace')],
 '/r438a-pt-chart/': [('r22-systems-repair-retrofit-or-replace', 'R-22 repair, retrofit or replace')],
}
