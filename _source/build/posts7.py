"""Posts 21, 22, 24 (run 2026-11-18)."""
import json, os
from core import url, table, esc
from posts5 import L, X, sources
from posts6 import gv

NEW_POSTS = [
 ('2-psi-gas-systems-explained', '2 PSI Gas Systems Explained: When and How to Size One',
  'What a 2 psi gas piping system is, why it allows much smaller pipe than low pressure, the regulator rules, and a worked IFGC example at 30 ft.', '2026-11-18'),
 ('csst-sizing-ehd-numbers-explained', 'CSST Sizing and EHD Numbers Explained (With a Worked Example)',
  'What the EHD number on CSST gas tubing means, why it is not a pipe size, how to pick EHD from IFGC tables by CFH and length, with a worked example.', '2026-11-18'),
 ('btu-to-cfh-gas-conversion', 'Converting Btu/h to CFH for Gas Pipe Sizing (Step by Step)',
  'How to turn appliance Btu/h input into cubic feet per hour for natural gas pipe sizing, total a multi-appliance load, and avoid the common unit mistakes.', '2026-11-18'),
]


def bodies():
    b = {}
    n12, n34, n1 = (gv('natural-gas-pipe-sizing-chart', 30, z) for z in ('1/2', '3/4', '1'))
    p12, p34, p1 = (gv('2-psi-natural-gas-pipe-sizing-chart', 30, z) for z in ('1/2', '3/4', '1'))
    b['2-psi-gas-systems-explained'] = f'''
<p class="lead">Most houses run gas at low pressure, about half a pound or less, which is roughly 7 in. of water column at the appliance. A 2 psi system raises the pressure in the piping and puts a regulator at each appliance, so a much smaller pipe can carry the same load. It is common for long runs, big loads and homes using CSST.</p>
<h2>Low pressure vs 2 psi</h2>
<p>Gas moves because pressure falls along the pipe. The IFGC tables size pipe so the pressure drop stays within an allowed amount. A low pressure system can only spare a fraction of an inch of water column, so the pipe must be large. A 2 psi system can spare a full 1 psi, which is about 28 in. w.c., so the same job fits in far smaller pipe.</p>
{table(['Schedule 40 pipe at 30 ft', 'Low pressure (0.5 in. w.c. drop)', '2 psi system (1 psi drop)'], [('1/2 in.', f'{n12} CFH', f'{p12} CFH'), ('3/4 in.', f'{n34} CFH', f'{p34} CFH'), ('1 in.', f'{n1} CFH', f'{p1} CFH')])}
<p>Those numbers come from our {L('/natural-gas-pipe-sizing-chart/', 'natural gas chart')} and {L('/2-psi-natural-gas-pipe-sizing-chart/', '2 psi chart')}, which copy IFGC Tables 402.4(2) and 402.4(5). At 30 ft, half-inch pipe carries {p12} CFH on a 2 psi system but only {n12} CFH at low pressure.</p>
<h2>The catch: regulators</h2>
<p>Appliances are built for low pressure. Each one needs a line regulator that steps the 2 psi down to the appliance pressure, normally 7 in. w.c. for natural gas. The code requires the regulator to be listed for the job, sized for the load, and installed where it can be reached and vented as the manufacturer instructs. Check the adopted code in your area for exact placement and vent rules. Many jurisdictions also want a pressure test at a higher pressure than a low pressure system.</p>
<h2>Where 2 psi makes sense</h2>
<ul>
<li>Long runs from the meter to a detached building or far corner of a large house.</li>
<li>High total loads such as a multi-appliance home with a pool heater or generator.</li>
<li>Systems using CSST, where manufacturers publish 2 psi tables.</li>
<li>Retrofits where pulling larger low pressure pipe would be costly.</li>
</ul>
<p>For a small house with short runs, low pressure pipe is usually simpler and cheaper because it needs no extra regulators.</p>
<h2>Worked example</h2>
<p>A furnace and water heater total 100,000 Btu/h. For natural gas that is 100 CFH. The longest run is 30 ft.</p>
<ol>
<li>Low pressure: the first pipe at or above 100 CFH in the 30 ft row is 3/4 in. ({n34} CFH), since 1/2 in. only gives {n12} CFH.</li>
<li>2 psi: 1/2 in. already carries {p12} CFH, far above 100 CFH, so half-inch pipe is enough.</li>
</ol>
<p>Run your own numbers with the {L('/gas-pipe-sizing/', 'gas pipe sizing calculator')}. The same logic applies to propane: compare the {L('/2-psi-propane-pipe-sizing-chart/', '2 psi propane chart')}, and see {L('/blog/propane-vs-natural-gas-pipe-sizing/', 'propane vs natural gas sizing')}.</p>
<h2>Mistakes to avoid</h2>
<ul>
<li>Using a 2 psi table on a system with no regulator at the appliance.</li>
<li>Mixing tables: each pressure and drop has its own table.</li>
<li>Forgetting that 2 psi tables use a 1 psi drop, not 0.5 in. w.c.</li>
<li>Skipping the manufacturer instructions for CSST at elevated pressure.</li>
</ul>
{sources([('https://up.codes/viewer/washington/ifgc-2021/chapter/4/gas-piping-installations', 'UpCodes: IFGC 2021 Chapter 4, Gas Piping Installations'), ('https://www.iccsafe.org/building-safety-journal/bsj-dives/codenotes-fuel-gas-pipe-sizing', 'ICC CodeNotes: Fuel Gas Pipe Sizing')])}
'''
    b['csst-sizing-ehd-numbers-explained'] = f'''
<p class="lead">CSST, corrugated stainless steel tubing, is not sized by inches. It is sized by an EHD number such as 13, 18 or 25. A bigger EHD means more capacity. Here is what that number means and how to use it with the code tables.</p>
<h2>What EHD means</h2>
<p>The IFGC defines EHD as Equivalent Hydraulic Diameter, a measure of the relative hydraulic efficiency between different tubing sizes. The greater the EHD, the greater the gas capacity. Because corrugated tubing flows differently from smooth steel pipe, the EHD gives it a rating you can compare across manufacturers. It is not a physical diameter, so do not read it like a nominal pipe size.</p>
<h2>Capacity by EHD at low pressure</h2>
{table(['Length', 'EHD 13', 'EHD 15', 'EHD 18', 'EHD 19', 'EHD 23', 'EHD 25'], [(f'{l} ft',) + tuple(f"{gv('csst-gas-pipe-sizing-chart', l, z)} CFH" for z in ('13', '15', '18', '19', '23', '25')) for l in (10, 30, 50)])}
<p>These are IFGC Table 402.4(15) values for natural gas under 2 psi with a 0.5 in. w.c. drop; the full table is on our {L('/csst-gas-pipe-sizing-chart/', 'CSST sizing chart')}. Notice the drop with length: EHD 18 carries 82 CFH at 10 ft but only 47 CFH at 30 ft.</p>
<h2>How to size CSST step by step</h2>
<ol>
<li>Add up the CFH of every appliance on the run. For natural gas, divide each Btu/h by 1,000 (see our {L('/blog/btu-to-cfh-gas-conversion/', 'Btu to CFH guide')}).</li>
<li>Measure the length from the meter or regulator to the farthest outlet.</li>
<li>Find that length, or the next longer row, in the table.</li>
<li>Move across the row to the first EHD with capacity at or above the load.</li>
</ol>
<h2>Worked example</h2>
<p>A furnace and water heater total 60 CFH at 30 ft. The 30 ft row gives EHD 13 = {gv('csst-gas-pipe-sizing-chart', 30, '13')}, EHD 15 = {gv('csst-gas-pipe-sizing-chart', 30, '15')}, EHD 18 = {gv('csst-gas-pipe-sizing-chart', 30, '18')} and EHD 19 = {gv('csst-gas-pipe-sizing-chart', 30, '19')}. The first that covers 60 CFH is EHD 19 ({gv('csst-gas-pipe-sizing-chart', 30, '19')} CFH).</p>
<h2>Fittings and bends</h2>
<p>The table already includes losses for four 90-degree bends and two end fittings. For each extra bend or fitting, add 1.3 ft of tubing length to your measurement (L = 1.3n) and re-read the table at the longer length.</p>
<h2>Manufacturer rules still apply</h2>
<p>Code tables give a general sizing basis, but each CSST brand is listed with its own installation instructions covering bonding, strike protection, support and fittings. Follow the manufacturer manual and local code, and use a certified installer. For higher pressure see the {L('/2-psi-csst-gas-pipe-sizing-chart/', '2 psi CSST chart')} and {L('/blog/2-psi-gas-systems-explained/', '2 psi systems explained')}; for propane use the {L('/propane-csst-sizing-chart/', 'propane CSST chart')}.</p>
<h2>Why capacity drops so quickly with length</h2>
<p>Gas flowing through a long run loses pressure to friction. Because the table holds the pressure drop fixed at 0.5 in. w.c., every extra foot reduces how much gas the tubing can pass. Doubling the run does not halve the capacity exactly, but the table shows the trend: EHD 18 carries 82 CFH at 10 ft, 47 CFH at 30 ft and 37 CFH at 50 ft. Keep trunk lines short and use home-run or branch layouts when you can.</p>
<h2>Comparing CSST to black iron</h2>
<p>A rough comparison helps when planning a retrofit. At 30 ft, 1/2 in. Schedule 40 pipe carries 95 CFH at low pressure, while EHD 18 CSST carries 47 CFH and EHD 25 carries 112 CFH. Manufacturers map their nominal sizes to EHD differently, so always check the brand\u2019s own chart. You can compare pipe tables on the {L('/gas-pipe-sizing/', 'gas pipe sizing page')}.</p>
{sources([('https://www.seattle.gov/documents/Departments/SDCI/Codes/FuelGasCode/2021SFGCChapter4.pdf', 'Seattle 2021 Fuel Gas Code, Chapter 4 (Table 402.4(15) notes and EHD definition)'), ('https://www.iccsafe.org/building-safety-journal/bsj-dives/codenotes-fuel-gas-pipe-sizing', 'ICC CodeNotes: Fuel Gas Pipe Sizing')])}
'''
    b['btu-to-cfh-gas-conversion'] = f'''
<p class="lead">Appliance labels list gas input in Btu per hour, but natural gas pipe sizing tables are in cubic feet per hour (CFH). One simple division connects them. Getting this step wrong is the most common reason a gas line ends up the wrong size.</p>
<h2>The formula</h2>
<p>CFH = appliance input in Btu/h \u00f7 heating value of the gas in Btu per cubic foot. The IFGC sizing procedure uses a typical natural gas heating value of 1,000 Btu per cubic foot unless the gas supplier gives a different number. So a 40,000 Btu/h water heater needs 40 CFH.</p>
<h2>Totaling several appliances</h2>
{table(['Appliance', 'Input (Btu/h)', 'CFH'], [('Furnace', '80,000', '80'), ('Water heater', '40,000', '40'), ('Range', '65,000', '65'), ('Dryer', '22,000', '22'), ('Total', '207,000', '207')])}
<p>Add the Btu/h first, then divide once. With a longest run of 40 ft, the Schedule 40 low pressure table needs a pipe carrying at least 207 CFH in the 40 ft row; check it on the {L('/natural-gas-pipe-sizing-chart/', 'natural gas chart')} or enter the load in the {L('/gas-pipe-sizing/', 'calculator')}.</p>
<h2>Propane is different</h2>
<p>The IFGC propane tables are written in thousands of Btu per hour (MBH). You use the Btu/h input directly, so no heating-value division is needed: 207,000 Btu/h is 207 MBH. Do not feed a propane load into a natural gas table in CFH. See {L('/blog/propane-vs-natural-gas-pipe-sizing/', 'propane vs natural gas sizing')}.</p>
<h2>Step by step</h2>
<ol>
<li>Read the input rating (not output or efficiency) from each appliance nameplate.</li>
<li>Add the Btu/h of all appliances on that pipe section.</li>
<li>Divide by 1,000 for natural gas (or by the supplier\u2019s heating value).</li>
<li>Look up the longest length and choose a pipe that carries at least that many CFH.</li>
</ol>
<h2>Common mistakes</h2>
<ul>
<li>Using output Btu/h instead of input.</li>
<li>Dividing each appliance and rounding down before adding.</li>
<li>Reading MBH tables as CFH.</li>
<li>Forgetting future appliances; a little oversizing is cheaper than redoing the line.</li>
</ul>
<p>For CSST the same CFH number goes into the {L('/blog/csst-sizing-ehd-numbers-explained/', 'EHD table')}.</p>
<h2>Quick reference examples</h2>
<ul>
<li>30,000 Btu/h gas fireplace: 30 CFH.</li>
<li>50,000 Btu/h tank water heater: 50 CFH.</li>
<li>150,000 Btu/h tankless water heater: 150 CFH, often the biggest load in a house, so size for it first.</li>
<li>35,000 Btu/h outdoor grill: 35 CFH.</li>
</ul>
<h2>Why total load matters</h2>
<p>The IFGC longest length method sizes every section for the load it carries, using the longest run from the meter. A trunk line feeding all appliances carries the total, while a branch to one dryer carries only the dryer. Convert each appliance first, then add them section by section. A common shortcut is to add every appliance, find the longest length, and size the whole system from one row. That is conservative and often fine for houses, but it can oversize branches.</p>
<h2>A note on units</h2>
<p>You may see MBH on labels, meaning thousands of Btu per hour, so 80 MBH equals 80,000 Btu/h and 80 CFH of natural gas. Others write kBtu/h. Never confuse MBH with MMBtu, which is a million Btu.</p>
{sources([('https://up.codes/viewer/washington/ifgc-2021/chapter/4/gas-piping-installations', 'UpCodes: IFGC 2021 Chapter 4, Gas Piping Installations'), ('https://www.iccsafe.org/building-safety-journal/bsj-dives/codenotes-fuel-gas-pipe-sizing', 'ICC CodeNotes: Fuel Gas Pipe Sizing')])}
'''
    return b


FAQS = {
 '2-psi-gas-systems-explained': [
  ('What is a 2 psi gas system?', 'A piping system operated at about 2 psi with a regulator at each appliance, allowing smaller pipe than low pressure.'),
  ('Do I need a regulator on a 2 psi system?', 'Yes. Appliances need a regulator that steps pressure down, normally to 7 in. w.c. for natural gas.'),
  ('What pressure drop do 2 psi tables use?', '1 psi, versus 0.5 in. w.c. in the common low pressure table.'),
  ('Is 2 psi cheaper to install?', 'Pipe is smaller, but regulators add cost, so it pays off mainly on long runs and large loads.'),
  ('Can I convert an existing system to 2 psi?', 'Only with the right regulators, a code-compliant pressure test and approval from your inspector and gas supplier.')],
 'csst-sizing-ehd-numbers-explained': [
  ('What does EHD mean in CSST?', 'Equivalent Hydraulic Diameter, a relative measure of the tubing\u2019s hydraulic efficiency. Higher EHD means more capacity.'),
  ('Is EHD the same as pipe diameter?', 'No. It is a flow rating, not a physical size.'),
  ('How many feet do extra fittings add?', 'The IFGC note adds 1.3 ft of tubing length per additional bend or fitting beyond those built into the table.'),
  ('Which table do I use for CSST?', 'IFGC Tables 402.4(15) to 402.4(17), depending on pressure and drop.'),
  ('Can I use code tables instead of the manufacturer manual?', 'Follow the manufacturer\u2019s listed instructions and local code; the tables are a sizing basis only.')],
 'btu-to-cfh-gas-conversion': [
  ('How do I convert Btu/h to CFH?', 'Divide by the gas heating value. For natural gas the IFGC procedure assumes 1,000 Btu per cubic foot.'),
  ('How many CFH is a 100,000 Btu/h furnace?', 'About 100 CFH on natural gas at 1,000 Btu per cubic foot.'),
  ('Do propane tables use CFH?', 'The IFGC propane tables use thousands of Btu per hour (MBH).'),
  ('Should I use input or output Btu?', 'Use input rating from the nameplate.'),
  ('What if my gas has a different heating value?', 'Use the value from your gas supplier in the same division.')],
}

RELATED_GUIDES = {
 '/2-psi-natural-gas-pipe-sizing-chart/': [('2-psi-gas-systems-explained', '2 psi gas systems explained')],
 '/2-psi-propane-pipe-sizing-chart/': [('2-psi-gas-systems-explained', '2 psi gas systems explained')],
 '/2-psi-csst-gas-pipe-sizing-chart/': [('2-psi-gas-systems-explained', '2 psi gas systems explained'), ('csst-sizing-ehd-numbers-explained', 'CSST and EHD numbers')],
 '/csst-gas-pipe-sizing-chart/': [('csst-sizing-ehd-numbers-explained', 'CSST and EHD numbers')],
 '/propane-csst-sizing-chart/': [('csst-sizing-ehd-numbers-explained', 'CSST and EHD numbers')],
 '/gas-pipe-sizing/': [('btu-to-cfh-gas-conversion', 'Btu/h to CFH conversion'), ('2-psi-gas-systems-explained', '2 psi gas systems explained')],
 '/natural-gas-pipe-sizing-chart/': [('btu-to-cfh-gas-conversion', 'Btu/h to CFH conversion')],
}
