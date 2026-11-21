"""Posts 28, 29, 30 (run 2026-11-21)."""
from core import table
from posts5 import L, sources

NEW_POSTS = [
 ('mig-settings-without-a-door-chart', 'MIG Settings Without a Door Chart: Amps, Wire Speed and Voltage',
  'No chart inside your MIG welder? Use Miller\u2019s 1 amp per 0.001 in rule, wire size ranges and wire speed multipliers, with worked examples from 22 ga to 1/4 in.', '2026-11-21'),
 ('tig-tungsten-sizes-and-amperage', 'TIG Tungsten Sizes and Amperage: What Fits Which Current',
  'Pick a TIG tungsten diameter by amperage: Miller current ranges for 2% and pure tungsten, a starting-amps rule by steel thickness and worked examples.', '2026-11-21'),
 ('printable-trade-reference-which-charts-to-carry', 'Printable Truck Reference: Which Charts to Carry in Your Truck',
  'A short list of the charts HVAC techs, electricians, plumbers and welders actually look up on the job, and the page on this site that covers each one.', '2026-11-21'),
]
MIGS = [('22 ga (0.030 in)', 30), ('16 ga (0.060 in)', 60), ('1/8 in (0.125 in)', 125), ('3/16 in (0.188 in)', 188), ('1/4 in (0.250 in)', 250)]
MULT = [('.023', 3.5, 30, 130), ('.030', 2.0, 40, 145), ('.035', 1.6, 50, 180), ('.045', 1.0, 75, 250)]


def bodies():
    b = {}
    def best(a):
        for w, m, lo, hi in MULT:
            if lo <= a <= hi:
                return w, m
        return None, None
    rows = []
    for lab, a in MIGS:
        w, m = best(a)
        rows.append((lab, f'{a} A', f'.0{w[2:]} in' if w else '\u2014', f'{a*m:.0f} ipm' if w else '\u2014'))
    b['mig-settings-without-a-door-chart'] = f'''
<p class="lead">Most MIG welders have a chart inside the wire door. Secondhand machines, older units and some shop rigs do not, and then you need a starting point you can trust. Miller Electric publishes a simple three-step method for solid-wire steel. It takes about a minute and gets you close enough to fine-tune on scrap.</p>
<h2>Step 1: amps from material thickness</h2>
<p>Miller\u2019s rule of thumb is that each 0.001 inch of material thickness needs about 1 amp of output. Material 0.125 inch (1/8 in) thick needs about 125 amps; 0.250 inch needs about 250 amps. Convert gauge to inches first: 22 ga steel is about 0.030 in, 16 ga about 0.060 in, 14 ga about 0.075 in and 12 ga about 0.105 in. Our {L('/mig-welding-settings-calculator/', 'MIG settings calculator')} does the conversion for you.</p>
<h2>Step 2: pick the wire size from the amperage</h2>
<p>Miller ties wire diameter to the amperage range it handles well. To avoid constant wire changes, choose the size that suits the thickness you weld most often.</p>
{table(['Wire diameter', 'Suitable amperage'], [('.023 in', '30\u2013130 A'), ('.030 in', '40\u2013145 A'), ('.035 in', '50\u2013180 A'), ('.045 in', '75\u2013250 A')])}
<h2>Step 3: wire feed speed from the multiplier</h2>
<p>Wire feed speed controls amperage on most machines. Without a chart, multiply the amps by a factor for your wire size to get inches per minute (ipm).</p>
{table(['Wire diameter', 'Multiply amps by', 'Example at 125 A'], [('.023 in', '3.5', '437.5 ipm'), ('.030 in', '2', '250 ipm'), ('.035 in', '1.6', '200 ipm'), ('.045 in', '1', '125 ipm')])}
<h2>Worked examples</h2>
{table(['Thickness', 'Amps', 'Wire in its range', 'Wire speed'], rows)}
<p>Where two wire sizes overlap, either works; the table shows the first match, so check the multiplier table if you prefer a different wire. For example, 125 A on 1/8 in plate fits .030 in wire at 250 ipm, .035 in wire at 200 ipm, or .045 in at 125 ipm.</p>
<h2>Step 4: set the voltage by sound and look</h2>
<p>Miller says voltage changes the height and width of the bead. Set the wire speed first, then adjust voltage for a crisp, stable arc. If the arc stubs into the work, raise the voltage. If it is erratic and burns back at the tip, lower it. Too much voltage gives poor arc control, inconsistent penetration and a turbulent puddle. Too little gives poor starts, spatter, a convex bead and poor tie-in at the toes. For a starting voltage by wire size and amperage, see the voltage chart on the {L('/mig-welding-settings-calculator/', 'calculator page')}.</p>
<h2>Read the bead to fine-tune</h2>
<ul>
<li><b>Narrow, convex bead, poor tie-in:</b> amperage too low, or travel too fast.</li>
<li><b>Wide bead, burn-through on thin metal:</b> amperage too high, or travel too slow.</li>
<li><b>Porosity and pinholes:</b> little or no shielding gas.</li>
</ul>
<p>Change one setting at a time and note the values that work. Write them on tape inside the door and you have your own chart.</p>
<h2>Limits of this method</h2>
<p>The rule applies to solid wire on steel. Aluminum, stainless and flux-core need different settings, as do out-of-position welds and very thick joints. Your machine\u2019s manual and chart come first, and any weld that carries load or must meet a code needs a qualified procedure, not a rule of thumb. For TIG, see our {L('/tig-welding-amperage-chart/', 'TIG amperage chart')} and the guide to {L('/blog/tig-tungsten-sizes-and-amperage/', 'tungsten sizes and amperage')}. All welding references are under {L('/welding/', 'Welding charts')}.</p>
{sources([('https://www.millerwelds.com/resources/article-library/mig-welding-setting-the-correct-parameters', 'Miller Electric: MIG Welding: Setting the Correct Parameters')])}
'''
    b['tig-tungsten-sizes-and-amperage'] = f'''
<p class="lead">Choosing a TIG tungsten comes down to one question: how many amps will you run? Too thin an electrode for the current overheats and balls up or melts; too thick makes the arc hard to start and unstable at low amps. This guide gives the current range for each common diameter, a starting amperage by steel thickness and a worked example.</p>
<h2>Current range by tungsten diameter</h2>
<p>The ranges below follow Miller Electric\u2019s published amperage table for tungsten electrodes. The first column covers 2% alloyed tungsten (thoriated, ceriated or lanthanated) on DC electrode negative; the second covers pure tungsten.</p>
{table(['Tungsten diameter', '2% alloyed tungsten', 'Pure tungsten'], [('1/16 in (1.6 mm)', '50\u2013140 A', '60\u201390 A'), ('3/32 in (2.4 mm)', '125\u2013200 A', '125\u2013160 A'), ('1/8 in (3.2 mm)', '150\u2013325 A', '190\u2013240 A'), ('3/16 in (4.8 mm)', '300\u2013340 A', '260\u2013320 A'), ('1/4 in (6.4 mm)', '\u2014', '330\u2013450 A')])}
<p>Ranges overlap because the best choice depends on duty cycle, joint and preference. Many welders pick the smaller electrode near the low end of a range for easier starts, and step up when running near the top.</p>
<h2>Starting amps by thickness</h2>
<p>A common starting point for steel is about 1 amp per 0.001 in of thickness, the same guideline Miller publishes for MIG. With a foot pedal you can then ease up or down.</p>
{table(['Steel thickness', 'Starting amps', 'Tungsten that fits'], [('22 ga (0.030 in)', 'about 30 A', '1/16 in'), ('16 ga (0.060 in)', 'about 60 A', '1/16 in'), ('1/8 in (0.125 in)', 'about 125 A', '3/32 in'), ('3/16 in (0.188 in)', 'about 188 A', '1/8 in'), ('1/4 in (0.250 in)', 'about 250 A', '1/8 in')])}
<h2>Worked example</h2>
<p>You are welding 1/8 in mild steel. The rule gives about 125 A. Both 1/16 in (50\u2013140 A) and 3/32 in (125\u2013200 A) cover that figure, but 125 A sits at the very bottom of the 3/32 in range and near the top of the 1/16 in range. On a long weld that heats the electrode, 3/32 in is the safer choice for the current you expect to ride at. Start at 125 A, then raise it if the puddle is slow to form.</p>
<h2>Newer inverter-era ranges are higher</h2>
<p>Miller\u2019s later owner\u2019s manuals for inverter machines list higher ceilings for 2% ceriated, lanthanated or thoriated tungsten on DC electrode negative: 1/16 in 70\u2013150 A (some manuals 50\u2013160 A), 3/32 in 150\u2013250 A and 1/8 in 250\u2013400 A. The table above is the more conservative older guide, so it is a safe place to start. Check your machine\u2019s manual for the exact range it supports.</p>
<h2>Which tungsten type?</h2>
<p>Miller\u2019s 2026 knowledge-hub article says pure tungsten is no longer the recommended choice for AC TIG on inverter machines, because rare-earth alloys such as ceriated and lanthanated tungsten outperform it. Miller\u2019s manuals also suggest considering ceria, lanthana or yttria instead of thoria, since grinding dust from thoriated electrodes contains low-level radioactive material, so use local exhaust or a respirator when grinding.</p>
<h2>Setup basics</h2>
<ul>
<li>Grind lengthwise to a point for DC so the arc stays stable and focused.</li>
<li>Typical argon flow is about 15\u201325 cfh. More is not better and can pull air into the arc.</li>
<li>Use filler rod no thicker than the base metal on thin sheet.</li>
<li>Stainless usually needs a little less current than carbon steel; aluminum on AC needs more, with balance and frequency set per your machine\u2019s guide.</li>
</ul>
<p>Use the full {L('/tig-welding-amperage-chart/', 'TIG amperage chart')} for more thicknesses. If you are setting up a MIG machine instead, read {L('/blog/mig-settings-without-a-door-chart/', 'MIG settings without a door chart')} and the {L('/mig-welding-settings-calculator/', 'MIG calculator')}.</p>
<h2>Limits</h2>
<p>These figures are starting points from manufacturer guidance, not a welding procedure. Code or structural work needs a qualified procedure and your machine manual applies first.</p>
{sources([('https://www.millerwelds.com/resources/article-library/mig-welding-setting-the-correct-parameters', 'Miller Electric: 1 amp per 0.001 in thickness guideline'), ('https://www.xedf.com/itw/products/basics_hints/basics5.html', 'Miller \u201cHelp Me Choose\u201d: Amperage for TIG Welding table (mirror of Miller guide)'), ('https://www.millerwelds.com/files/owners-manuals/o253086d_mil.pdf', 'Miller owner\u2019s manual: selecting tungsten for DC or AC with inverter machines'), ('https://www.millerwelds.com/en-US/resources/knowledge-hub/tig-welding/filler-metal-equipment-setup/how-to-choose-the-best-tungsten-for-AC-tig-welding', 'Miller: How to choose the best tungsten for AC TIG welding')])}
'''
    b['printable-trade-reference-which-charts-to-carry'] = f'''
<p class="lead">Every trade has a handful of lookups that come up again and again, and the page you need is rarely the one you have open. Here is a short carry list, grouped by trade, with the page on this site for each. Print the pages you use most or save them to your phone\u2019s home screen.</p>
<h2>HVAC and refrigeration</h2>
<ul>
<li>{L('/pt-chart/', 'Pressure-temperature (PT) charts')}: the master list of refrigerants. The big three are {L('/r410a-pt-chart/', 'R-410A')}, {L('/r22-pt-chart/', 'R-22')} and {L('/r134a-pt-chart/', 'R-134A')}, and newer systems use {L('/r454b-pt-chart/', 'R-454B')}.</li>
<li>{L('/target-superheat-calculator/', 'Target superheat calculator')} for fixed-orifice systems.</li>
<li>{L('/hvac-calculators/', 'HVAC calculators')} for the everyday maths.</li>
<li>{L('/hvac-age-by-serial-number/', 'HVAC age by serial number')} when a customer asks how old the unit is.</li>
</ul>
<h2>Electrical</h2>
<ul>
<li>{L('/conduit-fill-calculator/', 'Conduit fill calculator')} for how many conductors fit a raceway.</li>
<li>{L('/box-fill-calculator/', 'Box fill calculator')} for device boxes.</li>
<li>{L('/voltage-drop-calculator/', 'Voltage drop calculator')} for long runs.</li>
<li>{L('/conduit-offset-multiplier-chart/', 'Conduit offset multipliers')} for bending.</li>
<li>The {L('/electrical/', 'electrical hub')} for wire ampacity pages by AWG size.</li>
</ul>
<h2>Plumbing and gas</h2>
<ul>
<li>{L('/gas-pipe-sizing/', 'Gas pipe sizing')} tables from the IFGC, including {L('/propane-gas-pipe-sizing-chart/', 'propane iron pipe')}, {L('/propane-csst-sizing-chart/', 'CSST')} and {L('/propane-polyethylene-pipe-sizing-chart/', 'polyethylene')}.</li>
<li>{L('/water-heater-age/', 'Water heater age by serial number')} for warranty and replacement talks.</li>
</ul>
<h2>Welding</h2>
<ul>
<li>{L('/mig-welding-settings-calculator/', 'MIG settings calculator')} and the guide to {L('/blog/mig-settings-without-a-door-chart/', 'MIG settings without a door chart')}.</li>
<li>{L('/tig-welding-amperage-chart/', 'TIG amperage chart')} and {L('/blog/tig-tungsten-sizes-and-amperage/', 'tungsten sizes and amperage')}.</li>
</ul>
<h2>How to print or save</h2>
<ol>
<li>Open the page and use your browser\u2019s Print command; choose \u201cSave as PDF\u201d to keep a copy on your phone.</li>
<li>On a phone, use Share, then \u201cAdd to Home Screen\u201d for one-tap access.</li>
<li>Keep one laminated page in the truck for the chart you reach for most, and check the source line on the page before relying on a number for a permit job.</li>
</ol>
<h2>A sample truck binder by trade</h2>
<p>If you only want a one-page-per-topic binder, start with these and add as jobs demand. A residential HVAC tech needs the R-410A and R-454B charts plus one for R-22, because older systems are still in service. An electrician doing remodel work lives in conduit fill, box fill and voltage drop. A plumber or gas fitter wants the pipe sizing table that matches the fuel and the pipe material, and the water heater age page for warranty questions. A welder wants the MIG and TIG starting-point pages when the machine chart is missing.</p>
<h2>Check before you rely on a number</h2>
<ul>
<li>Match the refrigerant on the nameplate to the chart; mixing them up is the commonest mistake.</li>
<li>For gas sizing, confirm the pressure, length and pipe type against the table heading.</li>
<li>For conductors, confirm your local code edition and the termination temperature rating.</li>
<li>For welding settings, treat them as starting points and test on scrap.</li>
</ul>
<h2>Why a reference, not a rulebook</h2>
<p>These pages collect published tables from manufacturers, EPA and code documents so you do not have to hunt through PDFs. Your local code, the equipment nameplate and the manufacturer\u2019s instructions always come first, and every page names its source so you can check it.</p>
<h2>Sources</h2>
<p>Each page linked above lists its own published sources at the bottom, such as the International Fuel Gas Code tables, NEC tables, EPA refrigerant data and Miller Electric guidance.</p>
'''
    return b


FAQS = {
 'mig-settings-without-a-door-chart': [
  ('How many amps do I need to MIG weld 1/8 inch steel?', 'About 125 A by Miller\u2019s rule of 1 amp per 0.001 inch of thickness.'),
  ('What wire speed for .030 wire?', 'Multiply the amps by 2 to get inches per minute. At 125 A that is 250 ipm.'),
  ('Which MIG wire size should I use?', 'Miller lists .023 in for 30\u2013130 A, .030 in for 40\u2013145 A, .035 in for 50\u2013180 A and .045 in for 75\u2013250 A.'),
  ('How do I know if my voltage is right?', 'Aim for a crisp, stable arc. If it stubs into the work, raise voltage; if it is erratic and burns at the tip, lower it.'),
  ('Does this work for aluminum or flux-core?', 'No. The rules are for solid wire on steel. Use the machine manual for other wires and metals.')],
 'tig-tungsten-sizes-and-amperage': [
  ('What tungsten size for 125 amps?', 'Per Miller\u2019s table, 3/32 in 2% tungsten covers 125\u2013200 A, and 1/16 in covers up to 140 A.'),
  ('What is the amp range of 1/8 inch tungsten?', 'About 150\u2013325 A for 2% alloyed tungsten and 190\u2013240 A for pure tungsten.'),
  ('How many amps to TIG weld 1/8 inch steel?', 'A common starting point is about 125 A, adjusted with the foot pedal.'),
  ('How do I grind tungsten for DC?', 'Grind lengthwise to a point so the arc stays stable and focused.'),
  ('How much argon flow does TIG need?', 'Typically about 15\u201325 cfh. More can pull air into the arc.')],
 'printable-trade-reference-which-charts-to-carry': [
  ('Can I print these charts?', 'Yes. Use your browser\u2019s Print command and choose Save as PDF to keep a copy.'),
  ('Which HVAC charts matter most?', 'PT charts for R-410A, R-22 and R-134A, plus R-454B for newer systems, and the target superheat calculator.'),
  ('Can I add the site to my phone?', 'Yes. Use Share, then Add to Home Screen.'),
  ('Are these charts official?', 'They collect published tables with sources named on each page. Code and nameplates come first.'),
  ('Is the site free?', 'Yes. There is no sign-up and no charge.')],
}
RELATED_GUIDES = {
 '/mig-welding-settings-calculator/': [('mig-settings-without-a-door-chart', 'MIG settings without a door chart')],
 '/tig-welding-amperage-chart/': [('tig-tungsten-sizes-and-amperage', 'TIG tungsten sizes and amperage'), ('mig-settings-without-a-door-chart', 'MIG settings without a door chart')],
 '/welding/': [('mig-settings-without-a-door-chart', 'MIG settings without a door chart'), ('tig-tungsten-sizes-and-amperage', 'TIG tungsten sizes and amperage')],
 '/pt-chart/': [('printable-trade-reference-which-charts-to-carry', 'Charts to carry in your truck')],
 '/hvac-calculators/': [('printable-trade-reference-which-charts-to-carry', 'Charts to carry in your truck')],
 '/electrical/': [('printable-trade-reference-which-charts-to-carry', 'Charts to carry in your truck')],
}
