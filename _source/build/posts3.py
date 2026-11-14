"""Posts 10-12 (Phase 1, run 2026-11-14). Sources fetched and read before writing."""
from core import url, table, esc
from pages_hvac import BY, pf, tp, ps


def L(p, t):
    return f'<a href="{url(p)}">{t}</a>'


def X(h, t):
    return f'<a href="{h}" rel="noopener">{t}</a>'


def sources(items):
    return '<h2>Sources</h2><ul class="sources">' + ''.join(f'<li>{X(h, esc(t))}</li>' for h, t in items) + '</ul>'


NEW_POSTS = [
 ('charging-a-heat-pump-in-heating-mode', 'Charging a Heat Pump in Heating Mode: Rules of Thumb and Limits',
  'How to check the charge on a heat pump in winter: when to weigh in, heat-mode rules of thumb, R-410A saturation targets and the mistakes to avoid.', '2026-11-14'),
 ('fixed-orifice-vs-txv-how-to-tell', 'Fixed Orifice vs TXV: How to Tell Which You Have',
  'Piston or TXV? How to identify the metering device, why it decides whether you charge by superheat or subcooling, and what each does when charge changes.', '2026-11-14'),
 ('non-condensables-high-standing-pressure', 'Non-Condensables: Reading High Standing Pressure and Head Pressure',
  'How to tell air in a refrigerant system from a dirty coil or overcharge: the standing-pressure test, the saturation check, symptoms and the fix.', '2026-11-14'),
]


def bodies():
    r = BY['r410a']
    b = {}
    # heat pump example numbers from site PT data
    s25, s30 = pf(r, 25, 1), pf(r, 30, 1)
    c100 = pf(r, 100, 1)
    b['charging-a-heat-pump-in-heating-mode'] = f'''
<p class="lead">Checking the charge on a heat pump in winter is where a lot of good techs get stuck. Subcooling and superheat targets are written for cooling mode, the outdoor coil has turned into the evaporator, and many manufacturers say plainly not to charge by gauges at all below a certain outdoor temperature. This guide covers what the manuals say, the field rules of thumb that help you decide whether to dig deeper, and the checks that come before touching the charge.</p>
<h2>Start with the manufacturer</h2>
<p>Every source we read agrees on one thing: follow the installation manual. The details differ by brand and by model, so there is no universal heating-mode charging table.</p>
<ul>
<li><b>Trane</b> installer manuals call subcooling in cooling mode the only recommended method above 55 \u00b0F outdoor temperature. Below 55 \u00b0F the only recommended method is to weigh in the charge in heating mode, and they note it is important to return in spring or summer to charge accurately in cooling mode.</li>
<li><b>Daikin</b> heat pump instructions require the outdoor temperature to be 60 \u00b0F or higher for gauge checks, and state that the proper method of charging in heat mode is by weight with adjustments for line size and length.</li>
<li><b>Lennox</b> uses 60 \u00b0F as the dividing line: above it, adjust the charge in cooling mode; below it, use the heating mode procedure in its charging bulletin.</li>
<li>A <b>17 SEER R-454B heat pump</b> charging label (A7HP14F18P) lists subcooling targets in heating mode below 65 \u00b0F ambient, with 20 minutes of run time and indoor return air in a stated range.</li>
</ul>
<p>The dividing line is anywhere from 55 to 65 \u00b0F depending on the maker. Write down which one your unit uses before you hook up gauges.</p>
<h2>Do the obvious checks first</h2>
<p>Bryan Orr of HVAC School, writing in ACHR News, lists two steps before any measurement: get any frost off the outdoor coil completely, then check the filter, coils and blower wheel. In heating mode the roles swap. The indoor coil is the condenser, so a dirty filter can cause extremely high head pressure, and a dirty outdoor coil can cause low suction pressure. Both symptoms look like charge problems and are not.</p>
<h2>Heat-mode rules of thumb</h2>
<p>These are diagnostic hints from the same article, not charging targets. They apply with a frost-free coil and outdoor temperatures between 15 and 65 \u00b0F.</p>
{table(['Check', 'Expected (rule of thumb)'], [('Discharge line temperature', '100\u2013110 \u00b0F above outdoor temperature'), ('Suction line temperature', '5\u201315 \u00b0F cooler than outdoor temperature'), ('Suction saturation temperature', '20\u201325 \u00b0F below outdoor ambient (R-410A)'), ('Liquid line temperature', '3\u201315 \u00b0F warmer than indoor temperature'), ('Condensing temperature', '30\u201340 \u00b0F above indoor dry bulb'), ('Superheat (system with heat-mode TXV)', 'about 8\u201314 \u00b0F; subcooling often higher than in cooling')])}
<p>Orr stresses that these only tell you whether to connect gauges and look further. If anything looks off, verify with gauges and the manufacturer data.</p>
<h2>Worked example on R-410A</h2>
<p>Say it is 50 \u00b0F outside. The 20\u201325 \u00b0F rule puts suction saturation at 25\u201330 \u00b0F. On the {L('/r410a-pt-chart/', 'R-410A PT chart')} that is about {ps(s25)}\u2013{ps(s30)} psig at the suction port. If your gauge reads far below that with a clean coil and good indoor airflow, the system may be low on charge or have a restriction. If the indoor side is at 70 \u00b0F, the 30\u201340 \u00b0F rule puts condensing at 100\u2013110 \u00b0F, which is about {ps(c100)} psig at 100 \u00b0F and a little higher at 110 \u00b0F. Use the {L('/subcooling-calculator/', 'subcooling calculator')} once you have a liquid pressure and line temperature.</p>
<p>Notice that none of this tells you how many ounces to add. It tells you whether the numbers are plausible. That is the honest limit of heating-mode gauge checks.</p>
<h2>Weighing in</h2>
<p>If you have repaired a leak or replaced a component, recover the charge and weigh in the nameplate amount plus line-set adjustments. Orr points out that weighing out and in is sensible after a circuit repair, but silly when you only need to confirm the system is working. For a simple check, the rules of thumb above plus a return visit in mild or warm weather is more practical.</p>
<h2>Common mistakes</h2>
<ul>
<li>Using cooling-mode subcooling targets in heating mode.</li>
<li>Reading a frosted outdoor coil, which depresses suction pressure.</li>
<li>Reading the wrong refrigerant scale, especially now that R-454B and R-32 systems are arriving; see {L('/blog/r454b-service-basics/', 'R-454B service basics')}.</li>
<li>Adding charge during defrost or right after it. Allow about 15 minutes of normal operation afterwards (Carrier heating check chart).</li>
<li>Ignoring airflow. Fix the filter and blower before touching refrigerant; see {L('/blog/superheat-vs-subcooling/', 'superheat vs subcooling')}.</li>
</ul>
{sources([('https://www.achrnews.com/articles/140125-checking-the-charge-on-a-heat-pump-in-the-winter', 'ACHR News (Bryan Orr): Checking the Charge on a Heat Pump in the Winter'),
 ('https://elibrary.tranetechnologies.com/public/residential-hvac/Literature/Installation%20Operation%20and%20Maintenance/ODR-SVX003D-EN_04172026.pdf', 'Trane: Heat Pumps installation, operation and maintenance (ODR-SVX003D-EN)'),
 ('https://daikincomfort.com/docs/default-source/dz4se/im-iod-4038d.pdf', 'Daikin Comfort: condensing unit heat pump installation instructions (IM-IOD-4038D)'),
 ('https://s7d9.scene7.com/is/content/lennoxinternational/CORP0723L10-03-000', 'Lennox: Charging HFC-410A Heat Pumps in Heating and Cooling Modes (HP-07-4)'),
 ('https://www.aprsupply.com/ASSETS/DOCUMENTS/ITEMS/EN/RESI_HP_A7HP14F18P_CHARGELABELpdf.pdf', 'R-454B heat pump charging procedure label (A7HP14F18P)'),
 ('https://www.shareddocs.com/hvac/docs/1009/Public/0E/38-12XA.pdf', 'Carrier: Heat Pumps Heating Check Charts (38-12XA)')])}'''

    s_bad = 52 - 40
    b['fixed-orifice-vs-txv-how-to-tell'] = f'''
<p class="lead">Before you pick a charging method you need to know what is metering refrigerant into the evaporator. A piston (fixed orifice) and a thermostatic expansion valve (TXV) respond to a change in charge in opposite ways, so charging a TXV system by superheat, or a piston system by subcooling, gives a meaningless reading. Here is how to tell them apart and what to measure on each.</p>
<h2>What each device does</h2>
<p>HVAC School describes the job of any metering device as creating a pressure drop between the liquid line and the evaporator. As the liquid passes through, part of it flashes to vapor and the rest boils in the coil.</p>
<ul>
<li>A <b>piston</b> is a brass body with a fixed bore. The smaller the bore, the less refrigerant passes. Nothing adjusts it, so flow depends on the pressure difference across it. In many heat pumps the piston is a flow-through type that unseats when the reversing valve changes direction, and there is a second metering device for the other mode. Capillary tubes are another fixed-orifice type, more common in refrigeration.</li>
<li>A <b>TXV</b> opens and closes in response to evaporator load. A sensing bulb on the suction line pushes it open as the line warms, while a spring and an external equalizer push it closed. HVAC School calls it a constant-superheat device: it holds a relatively constant superheat at the evaporator outlet.</li>
</ul>
<h2>How to identify which one you have</h2>
<ol>
<li><b>Read the data plate.</b> Many outdoor units list the charging method and target (subcooling or a superheat chart). Check the indoor unit rating plate too.</li>
<li><b>Look at the indoor coil.</b> A TXV has a bulb clamped to the suction line near the coil outlet and often an equalizer line. A piston sits in a fitting at the liquid line connection, usually behind a nut.</li>
<li><b>Look at the installation manual.</b> Carrier manuals state it plainly: for TXV, use the subcooling method; for piston, use the superheat method.</li>
<li><b>Verify, don\u2019t assume.</b> One charging guide advises removing the front cover if the rating plate does not settle it. Replacement coils are sometimes a different type from the original.</li>
</ol>
<h2>Why the method follows the device</h2>
<p>ACHR News explains that a TXV unit is charged to the subcooling leaving the condenser because the superheat is held nearly constant, typically 8\u201312 \u00b0F in residential air conditioning. A piston cannot regulate anything, so adding refrigerant lowers superheat and removing it raises superheat; superheat tracks the charge directly.</p>
{table(['', 'Fixed orifice (piston)', 'TXV'], [('Flow control', 'Fixed bore, no adjustment', 'Modulates to hold superheat'), ('Primary charging method', 'Superheat vs manufacturer chart', 'Subcooling vs data plate target'), ('Superheat as a charge indicator', 'Yes (changes with charge and load)', 'No (valve holds it)'), ('Superheat target depends on', 'Indoor wet bulb and outdoor dry bulb', 'Not used for charge'), ('Typical subcooling target', 'Diagnostic only', 'Per manufacturer, often 6\u201312 \u00b0F'), ('What else to monitor', 'Subcooling, delta T, pressures', 'Superheat, delta T, pressures')])}
<p>Whichever you use, HVAC School reminds you to keep watching suction pressure, head pressure, superheat, subcooling and delta T or another airflow check.</p>
<h2>Worked example (piston)</h2>
<p>Suppose a piston system on R-410A reads 118 psig on the suction port, which is 40 \u00b0F saturation on the {L('/r410a-pt-chart/', 'R-410A PT chart')}, and the suction line temperature at the condenser is 52 \u00b0F. Superheat is {s_bad} \u00b0F. You then compare that with the manufacturer\u2019s chart for the indoor wet bulb and outdoor dry bulb. Do not use one fixed number for every piston system; the target changes with load. The {L('/superheat-calculator/', 'superheat calculator')} does the subtraction for you.</p>
<h2>Worked example (TXV)</h2>
<p>On a TXV system the plate says 10 \u00b0F subcooling. You read liquid pressure, convert to a saturated liquid temperature and subtract the liquid line temperature measured near the service valve. Add refrigerant to raise subcooling; recover to lower it. The {L('/subcooling-calculator/', 'subcooling calculator')} gives the number. Check airflow first; our guide to {L('/blog/superheat-vs-subcooling/', 'superheat vs subcooling')} lists the usual causes of false readings.</p>
<h2>Heat pumps and mixed systems</h2>
<p>Heat pumps can have a piston on one end and a TXV on the other, or a TXV at both ends with check valves. The mode you are in decides which device is metering, so check the manual for the heating-mode method and read {L('/blog/charging-a-heat-pump-in-heating-mode/', 'charging a heat pump in heating mode')} before you charge in winter.</p>
{sources([('http://www.hvacrschool.com/piston-vs-txv', 'HVAC School (Bryan Orr): Piston vs. TXV Metering Devices'),
 ('https://www.achrnews.com/articles/83383-charging-methods-for-metering-devices', 'ACHR News: Charging Methods for Metering Devices'),
 ('https://manuals.plus/carrier/25sca5-single-stage-heat-pumps-manual.pdf', 'Carrier 25SCA5 heat pump manual (check charge: TXV subcooling, piston superheat)'),
 ('https://www.acservicetech.com/post/should-i-check-the-refrigerant-charge-with-superheat-or-subcooling', 'AC Service Tech: Should I check the refrigerant charge with superheat or subcooling?'),
 ('https://buildingscience.com/sites/default/files/migrate/pdf/BSCInfo_608_Refrigerant_Material_rev.pdf', 'Building Science Corporation: Information Sheet 608 (charging, superheat and subcooling)')])}'''

    b['non-condensables-high-standing-pressure'] = f'''
<p class="lead">High head pressure has a long list of causes, and air in the system is near the bottom of it. When the common causes are ruled out, though, non-condensables are the next suspect, and the PT chart gives you a clean way to prove it. This guide explains how air gets in, how it shows up on your gauges, and how to confirm it.</p>
<h2>What non-condensables are and how they get in</h2>
<p>ACHR News describes air as nitrogen, oxygen and moisture, all harmful to a refrigeration system. Air does not condense, so it collects at the top of the condenser and takes up surface the refrigerant needs. It can enter in two ways:</p>
<ul><li><b>Poor service practice:</b> not purging hoses, or not fully evacuating after the system was opened to replace a part or fix a leak.</li>
<li><b>A low-side leak:</b> if enough refrigerant escapes that the low side runs below atmospheric pressure, air is pulled in. Topping off without recovering and evacuating leaves that air trapped.</li></ul>
<p>The oxygen and moisture can react with the oil and, when heated, form acids that attack motor windings and cause corrosion and sludge, so this is more than a performance issue.</p>
<h2>Rule out the common causes first</h2>
<p>Marchese (Heatcraft), writing in ACHR News, says non-condensables are not a very common cause and that techs should first look at dirty coils, insufficient condenser airflow and recirculation of condenser air. Overcharge is the other look-alike. Our guide to {L('/blog/superheat-vs-subcooling/', 'superheat and subcooling')} shows how an overcharge reads, and the {L('/blog/how-to-read-a-pt-chart/', 'PT chart guide')} covers the basics.</p>
<h2>Symptoms</h2>
<p>ACHR News\u2019 Professor lists the symptoms of air in a system as high discharge temperature, high condensing pressure, high condensing subcooling, high condenser split, high compression ratio, normal to slightly high suction pressure, normal superheat and high amp draw. With a TXV, those look very much like an overcharge, so you need the saturation test below to tell them apart.</p>
{table(['Cause', 'Head pressure', 'Subcooling', 'Clue'], [('Dirty coil / low airflow', 'High', 'Often high', 'Big air split, fix by cleaning or fan repair'), ('Overcharge', 'High', 'High', 'Saturation matches the PT chart'), ('Non-condensables', 'High', 'High to normal', 'Saturation temperature higher than refrigerant temperature'), ('Wrong refrigerant scale', 'Reads wrong', 'Reads wrong', 'Set the right refrigerant on the gauge')])}
<h2>The standing-pressure test (system off)</h2>
<ol>
<li>Identify the refrigerant.</li>
<li>Turn the compressor off but keep the condenser fan running, so everything comes to the same temperature.</li>
<li>Put probes on the discharge line, the liquid line and the air entering the condenser.</li>
<li>When all three read the same temperature, record the condenser pressure.</li>
<li>Convert that pressure to a saturation temperature on the PT chart for that refrigerant.</li>
<li>If the converted temperature is higher than the measured temperatures by more than a few degrees, there are non-condensables.</li>
</ol>
<p>That is the procedure from the Marchese article. Parker\u2019s P-T analysis guide explains the physics: the foreign gas adds its own pressure to the refrigerant pressure, so the actual refrigerant temperature in the condenser is lower than the chart suggests for that pressure.</p>
<h2>Worked example on R-410A</h2>
<p>After a long shutdown, all three probes read 80 \u00b0F. On the {L('/r410a-pt-chart/', 'R-410A PT chart')} 80 \u00b0F saturates at about {ps(pf(r, 80, 1))} psig. If your gauge reads {ps(pf(r, 80, 1) + 40)} psig, the pressure corresponds to roughly {tp(r, pf(r, 80, 1) + 40, 0):.0f} \u00b0F, about {tp(r, pf(r, 80, 1) + 40, 0) - 80:.0f} \u00b0F higher than the actual temperature, and air is a strong suspect. A hose that was not purged is a classic reason. One article suggests that a difference of more than 10 psig on an equalized system often indicates air; treat that as a hint, not a rule.</p>
<h2>Fixing it</h2>
<p>For a small system with a recovery machine, recover the refrigerant, replace the filter drier if the system was open, pull a deep vacuum and weigh in the nameplate charge. Venting refrigerant to purge air is not acceptable under EPA rules. Danfoss\u2019 troubleshooting guidance for larger systems describes purging the condenser with a reclaim system, running the system to operating temperature and purging again if necessary. For A2L systems use equipment rated for them; see {L('/blog/a2l-tools-leak-detectors-recovery-machines/', 'A2L tools')}.</p>
<h2>Prevention</h2>
<ul><li>Purge hoses, and evacuate to a deep vacuum with a micron gauge before opening the circuit to refrigerant.</li><li>Fix low-side leaks before topping off.</li><li>Record the standing-pressure reading at commissioning so you have a baseline.</li></ul>
{sources([('https://www.achrnews.com/articles/102428-checking-for-noncondensables', 'ACHR News (Joe Marchese): Checking For Noncondensables'),
 ('https://www.achrnews.com/articles/129746-the-professor-symptoms-of-air-in-a-refrigeration-system', 'ACHR News (The Professor): Symptoms of Air in a Refrigeration System'),
 ('https://www.achrnews.com/articles/145263-properly-interpreting-liquid-subcooling-in-the-condenser', 'ACHR News: Properly Interpreting Liquid Subcooling in the Condenser'),
 ('https://www.parker.com/content/dam/parker/na/united-states/industries/hvacr/pdfs-hvacr2/Using%20P-T%20Analysis%20as%20a%20Service%20Tool.pdf', 'Parker: Using P-T Analysis as a Service Tool'),
 ('https://reftools.danfoss.com/en/tools/cooling/troubleshooter/system-areas/high-pressure/system/condensing-pressure-too-high/air-or-other-non-condensable-gases-in-refrigerant-system/', 'Danfoss Ref Tools: air or other non-condensable gases in refrigerant system'),
 ('https://hvaclaboratory.com/article/diagnosing-high-head-pressure-in-central-ac-systems-what-you-need-to-know', 'HVAC Laboratory: Diagnosing High Head Pressure in Central AC Systems')])}'''
    return b


FAQS = {
 'charging-a-heat-pump-in-heating-mode': [
  ('Can I charge a heat pump in heating mode?', 'Only by following the manufacturer. Trane says to weigh in the charge below 55 \u00b0F outdoor, Daikin says the proper heat-mode method is by weight, and Lennox has a specific heating-mode procedure below 60 \u00b0F.'),
  ('At what outdoor temperature should I switch to cooling mode to charge?', 'It depends on the maker: Trane 55 \u00b0F, Lennox and Daikin 60 \u00b0F, and an R-454B heat pump label 65 \u00b0F. Check the unit\u2019s manual.'),
  ('What discharge line temperature is normal in heating mode?', 'ACHR News gives a rule of thumb of 100\u2013110 \u00b0F above the outdoor temperature, as a diagnostic hint rather than a charging target.'),
  ('Why does a dirty filter cause high head pressure in heating mode?', 'Because the indoor coil is the condenser in heating mode, so low airflow across it raises condensing pressure.'),
  ('Should I weigh in the charge after a repair?', 'Yes. After a refrigerant circuit repair, recovering and weighing in the nameplate charge plus line-set adjustment is the sound approach.')],
 'fixed-orifice-vs-txv-how-to-tell': [
  ('How do I tell if my system has a TXV or a piston?', 'Check the rating plate, look for a sensing bulb on the suction line near the indoor coil (TXV), or a fitting at the coil liquid connection holding a piston, and read the installation manual.'),
  ('Do I charge a TXV by superheat?', 'No. The valve holds superheat nearly constant, so charge is checked by subcooling against the manufacturer target.'),
  ('Do I charge a piston system by subcooling?', 'The primary method is superheat against the manufacturer chart for the indoor wet bulb and outdoor dry bulb. Subcooling is still useful for diagnosis.'),
  ('Can a heat pump have both devices?', 'Yes. Some heat pumps have a piston in the outdoor unit for heating and another device indoors for cooling, so the mode decides which one is metering.'),
  ('Why not use one superheat number for every piston system?', 'Because target superheat changes with indoor wet bulb and outdoor dry bulb, and manufacturers publish different charts.')],
 'non-condensables-high-standing-pressure': [
  ('What are non-condensables?', 'Gases such as air (nitrogen, oxygen and moisture) that do not condense in the refrigerant circuit and collect at the top of the condenser.'),
  ('How do air and non-condensables get into a system?', 'Through poor service practice, such as not purging hoses or not evacuating after opening the system, or through a low-side leak that lets the low side go below atmospheric pressure.'),
  ('How do I test for non-condensables?', 'With the compressor off and the condenser fan running, wait until the discharge line, liquid line and entering air are the same temperature, convert the pressure to saturation temperature, and see whether it is more than a few degrees higher.'),
  ('Is it just an overcharge?', 'With a TXV the symptoms are similar, including high head pressure and high subcooling. The standing-pressure test separates the two.'),
  ('Can I vent the air out?', 'Do not vent refrigerant. Recover it, evacuate and recharge by weight, or use a reclaim-based purge on larger systems.')],
}

RELATED_GUIDES = {
 '/subcooling-calculator/': [('fixed-orifice-vs-txv-how-to-tell', 'Fixed orifice vs TXV: which do you have?')],
 '/superheat-calculator/': [('fixed-orifice-vs-txv-how-to-tell', 'Fixed orifice vs TXV: which do you have?')],
 '/r410a-pt-chart/': [('charging-a-heat-pump-in-heating-mode', 'Charging a heat pump in heating mode'), ('non-condensables-high-standing-pressure', 'Non-condensables and high standing pressure')],
 '/pt-chart/': [('non-condensables-high-standing-pressure', 'Reading high standing pressure')],
 '/r22-pt-chart/': [('non-condensables-high-standing-pressure', 'Non-condensables and high standing pressure')],
}
