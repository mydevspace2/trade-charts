"""Posts 19, 20, 23 (run 2026-11-17)."""
import json, os
from core import url, table, esc
from posts5 import L, X, sources

G = {t['slug']: t for t in json.load(open(os.path.join(os.path.dirname(__file__), 'data', 'gas.json')))['tables']}


def gv(slug, length, size):
    t = G[slug]
    return t['rows'][str(length)][t['sizes'].index(size)]


NEW_POSTS = [
 ('conduit-offset-angles-30-45-22-5', 'Conduit Offset Angles: 30\u00b0 vs 45\u00b0 vs 22.5\u00b0 (Multipliers and Shrink)',
  'Which bend angle to use for a conduit offset: multipliers, shrink per inch, worked 6 in. offset examples and when 10\u00b0, 22.5\u00b0, 30\u00b0 or 45\u00b0 makes sense.', '2026-11-17'),
 ('conduit-saddles-kicks-basics', 'Conduit Saddles and Kicks: 3-Point Saddle Basics and Shrink',
  'How a 3-point saddle (45\u00b0 center, 22.5\u00b0 sides) and a kick differ from an offset, with the 2.5 spacing rule, shrink and a worked 2 in. pipe example.', '2026-11-17'),
 ('propane-vs-natural-gas-pipe-sizing', 'Propane vs Natural Gas Pipe Sizing: Same House, Different Pipe',
  'Why propane pipe is usually smaller than natural gas pipe for the same load. Worked 100,000 Btu/h example from IFGC tables at 30 ft, low pressure and 2 psi.', '2026-11-17'),
]


def bodies():
    b = {}
    b['conduit-offset-angles-30-45-22-5'] = f'''
<p class="lead">An offset moves conduit over an obstruction with two equal bends. The angle you pick changes how far apart the bends sit, how much length the offset eats, and how easy it is to pull wire. Here is how to choose between the common angles.</p>
<h2>The geometry in one line</h2>
<p>An offset is a right triangle. The offset depth is the side opposite the bend angle and the distance between your two marks is the long diagonal. So distance between bends = depth \u00d7 1 \u00f7 sin(angle). That factor is the multiplier. Because sin 30\u00b0 is exactly 0.5, the 30\u00b0 multiplier is exactly 2.</p>
{table(['Angle', 'Exact multiplier', 'Field multiplier', 'Exact shrink per inch', 'Field shrink per inch'], [('10\u00b0', '5.759', '6', '0.087 in.', '1/16 in.'), ('22.5\u00b0', '2.613', '2.6', '0.199 in.', '3/16 in.'), ('30\u00b0', '2.000', '2', '0.268 in.', '1/4 in.'), ('45\u00b0', '1.414', '1.4', '0.414 in.', '3/8 in.'), ('60\u00b0', '1.155', '1.2', '0.577 in.', '1/2 in.')])}
<p>Field multipliers are the rounded numbers printed on benders. They are close enough for small offsets, but the rounding error grows with depth. At 10\u00b0 the field value of 6 is about 4% longer than the exact 5.759, which is nearly an inch on a 12 in. offset.</p>
<h2>Worked example: a 6 in. offset</h2>
{table(['Angle', 'Marks apart', 'Shrink (field)'], [('22.5\u00b0', '6 \u00d7 2.6 = 15.6 in.', '6 \u00d7 3/16 = 1 1/8 in.'), ('30\u00b0', '6 \u00d7 2 = 12 in.', '6 \u00d7 1/4 = 1 1/2 in.'), ('45\u00b0', '6 \u00d7 1.414 = 8 1/2 in.', '6 \u00d7 3/8 = 2 1/4 in.')])}
<p>Shrink is the length the run loses because the conduit takes the diagonal instead of going straight. You add the shrink to your overall measurement so the conduit still reaches the next box.</p>
<h2>Which angle should you choose?</h2>
<ul>
<li><b>30\u00b0:</b> the default. The math is a doubling, shrink is a clean quarter inch per inch, and the offset is gentle enough for wire pulls.</li>
<li><b>45\u00b0:</b> use when space is tight and the marks must be close together. Shrink is larger, and a steeper offset pulls harder, so avoid it on long runs with many conductors.</li>
<li><b>22.5\u00b0:</b> use for shallow, long transitions, and as the side bends of a saddle. It needs the most room between marks.</li>
<li><b>10\u00b0:</b> only for very slight jogs. Small angle errors turn into big position errors, so it is hard to be accurate.</li>
</ul>
<h2>How to bend the offset</h2>
<ol>
<li>Measure the offset depth from the conduit centerline to where it needs to be.</li>
<li>Pick the angle and multiply the depth by its multiplier to get the mark spacing.</li>
<li>Mark the conduit at the first bend position and the second mark the calculated distance away.</li>
<li>Bend the first mark to the chosen angle, then rotate the conduit 180\u00b0 so the bends stay in one plane, and bend the second mark to the same angle.</li>
<li>Lay the conduit on a flat surface to check that the legs are parallel and nothing twisted.</li>
</ol>
<p>Dedicated pages: {L('/30-degree-offset-multiplier/', '30\u00b0')}, {L('/45-degree-offset-multiplier/', '45\u00b0')}, {L('/22-5-degree-offset-multiplier/', '22.5\u00b0')}, or the full {L('/conduit-offset-multiplier-chart/', 'offset multiplier chart')}.</p>
<h2>Bends and code limits</h2>
<p>Whatever angle you use, the NEC limits bends between pull points to 360\u00b0 total for EMT and rigid conduit, and requires bends that do not reduce the conduit\u2019s internal diameter. Each offset uses twice its angle toward the 360\u00b0 total, so a 30\u00b0 offset counts 60\u00b0. Check the adopted code in your jurisdiction, and use the {L('/emt-conduit-fill-chart/', 'EMT fill chart')} to confirm the conduit is sized for the wire.</p>
<h2>Common mistakes</h2>
<ul>
<li>Forgetting shrink and ending up short at the next box.</li>
<li>Letting the conduit roll between bends so the offset twists.</li>
<li>Mixing field and exact multipliers within one run.</li>
<li>Marking to the edge of the obstruction instead of the centerline of the conduit.</li>
</ul>
{sources([('https://ibendpipe.com/conduit-bending-multipliers', 'iBend Pipe: where conduit bending multipliers come from'), ('https://wirefillchart.com/conduit-bend-offset-calculator', 'WireFillChart: conduit bend offset calculator'), ('https://www.electrakit.com/references/conduit-bending-chart/', 'ElectraKit: conduit bending multipliers (Klein field factors)')])}
'''
    b['conduit-saddles-kicks-basics'] = f'''
<p class="lead">When conduit has to cross a pipe or duct, you use a saddle. When it has to turn a small angle at a wall or box, you use a kick. Both reuse the offset multipliers you already know.</p>
<h2>A kick</h2>
<p>A kick is a single bend of a small angle, used to line conduit up with a box knockout or to change direction slightly. Because there is only one bend, there is no pair of marks: you set the distance from the bend to the box and choose the angle. The shrink constants are the same as for an offset, so a kick of height H at 30\u00b0 loses about H \u00d7 1/4 in. of length, and you allow for that on the leg past the kick.</p>
<h2>The 3-point saddle</h2>
<p>A 3-point saddle is two half-offsets back to back. The center bend is 45\u00b0 and the two outer bends are 22.5\u00b0 each, in the opposite direction. Geometrically the outer legs climb at 22.5\u00b0, so the exact spacing from the center mark to each outer mark is the obstruction height \u00d7 2.613. Many field references round this to 2.5, and others to 2.6.</p>
{table(['Item', 'Rule'], [('Center bend', '45\u00b0'), ('Outer bends', '22.5\u00b0 each, opposite direction'), ('Outer marks', '2.5 \u00d7 obstruction height on each side of the center mark'), ('Shrink', '3/16 in. per inch of height'), ('Center mark position', 'Center of obstruction plus the shrink')])}
<h2>Worked example: crossing a 2 in. pipe</h2>
<p>Obstruction height (outside the pipe plus conduit clearance): 2 in.</p>
<ul>
<li>Outer marks: 2.5 \u00d7 2 = 5 in. each side of the center mark, so 10 in. overall.</li>
<li>Shrink: 2 \u00d7 3/16 = 3/8 in. total.</li>
<li>Bend the center mark to 45\u00b0, then the two outer marks to 22.5\u00b0 in the opposite direction, keeping the conduit flat on the floor between bends.</li>
</ul>
<h2>Saddle or offset?</h2>
<p>Use an {L('/blog/conduit-offset-angles-30-45-22-5/', 'offset')} when conduit changes level and stays on the new level, for example entering a box. Use a saddle when it must go over something and come back to the original level. A 4-point saddle works better for large round obstructions, and you can read more bend types on the {L('/conduit-offset-multiplier-chart/', 'offset multiplier chart')}.</p>
<h2>Tips for accurate saddles</h2>
<ol>
<li>Mark the center of the obstruction on the conduit first, then the outer marks.</li>
<li>Line up the center-of-bend notch on the center mark and the arrow on the outer marks, following your bender\u2019s instructions.</li>
<li>Check that the conduit stays in one plane; twisting between bends is the usual cause of a bad saddle.</li>
<li>Test fit with a piece of scrap before bending expensive conduit.</li>
</ol>
<p>Mind the 360\u00b0 limit between pull points. A saddle uses 45\u00b0 + 22.5\u00b0 + 22.5\u00b0 = 90\u00b0 of that allowance. Confirm sizing with the {L('/conduit-fill-calculator/', 'conduit fill calculator')}.</p>
{sources([('https://ibendpipe.com/conduit-bending-multipliers', 'iBend Pipe: multipliers, shrink and 3-point saddles'), ('https://sparkshift.app/calculators/conduit-bending?bend=concentric', 'SparkShift: conduit bending calculator (saddle rule)'), ('https://www.electrakit.com/references/conduit-bending-chart/', 'ElectraKit: conduit bending chart')])}
'''
    n, p = 'natural-gas-pipe-sizing-chart', 'propane-gas-pipe-sizing-chart'
    n2, p2 = '2-psi-natural-gas-pipe-sizing-chart', '2-psi-propane-pipe-sizing-chart'
    b['propane-vs-natural-gas-pipe-sizing'] = f'''
<p class="lead">Propane carries more energy per cubic foot than natural gas, so the same appliance load needs a smaller pipe on propane. The tables are also written in different units, which trips up many people.</p>
<h2>Different units, different gas</h2>
<p>The IFGC natural gas tables list capacity in cubic feet of gas per hour (CFH) at a specific gravity of 0.60. The propane tables list thousands of Btu per hour (MBH) at a specific gravity of 1.50. To size natural gas you convert the appliance input to CFH by dividing by the heating value, commonly assumed to be 1,000 Btu per cubic foot. For propane you can use the appliance input in MBH directly.</p>
<h2>Worked example: 100,000 Btu/h at 30 ft</h2>
<p>Take a 100,000 Btu/h total load, longest run 30 ft, at low pressure with a 0.5 in. w.c. drop.</p>
{table(['Gas', 'Load in table units', 'Pipe', 'Capacity at 30 ft'], [('Natural gas (CFH)', '100,000 \u00f7 1,000 = 100 CFH', '3/4 in.', f"{gv(n, 30, '3/4')} CFH (1/2 in. holds only {gv(n, 30, '1/2')})"), ('Propane (MBH)', '100 MBH', '1/2 in.', f"{gv(p, 30, '1/2')} MBH")])}
<p>The natural gas run needs 3/4 in. black iron because the 1/2 in. pipe carries just {gv(n, 30, '1/2')} CFH at 30 ft. The propane run gets away with 1/2 in. because the same table row allows {gv(p, 30, '1/2')} MBH. Convert the natural gas capacity to Btu at 1,000 per cubic foot and 3/4 in. is {gv(n, 30, '3/4')} MBH, so propane at 11 in. w.c. through 1/2 in. gets nearly the same Btu flow as natural gas through the next size up.</p>
<h2>Pressure matters more</h2>
<p>A 2 psi system with a 1 psi drop carries far more through the same pipe. At 30 ft, 1/2 in. black iron carries {gv(n2, 30, '1/2')} CFH of natural gas at 2 psi, against {gv(n, 30, '1/2')} CFH at low pressure. For propane, 1/2 in. carries {gv(p2, 30, '1/2')} MBH at 2 psi, against {gv(p, 30, '1/2')} MBH at 11 in. w.c. That is why long runs to a detached building or a large load often use 2 psi with a regulator at each appliance.</p>
<h2>Step by step</h2>
<ol>
<li>Add up the Btu/h input of every appliance on the line.</li>
<li>Natural gas: divide by the heating value to get CFH. Propane: keep MBH.</li>
<li>Measure the longest length from the meter or tank regulator to the farthest appliance.</li>
<li>Choose the table row at or just above that length and use it for every section.</li>
<li>Pick the first pipe size whose capacity is at or above the load.</li>
</ol>
<h2>Cautions</h2>
<ul>
<li>Use the table for the right pressure and drop. Low pressure propane is usually 11 in. w.c. at the appliance side.</li>
<li>Fittings add equivalent length; allow for them on long or twisty runs.</li>
<li>Do not use natural gas orifices on propane appliances; appliances must be converted with the manufacturer\u2019s kit.</li>
<li>Local code and the gas supplier have the last word.</li>
</ul>
<p>See the full tables: {L('/natural-gas-pipe-sizing-chart/', 'natural gas chart')}, {L('/propane-gas-pipe-sizing-chart/', 'propane chart')}, {L('/2-psi-natural-gas-pipe-sizing-chart/', '2 psi natural gas')} and {L('/2-psi-propane-pipe-sizing-chart/', '2 psi propane')}, or run your own load through the {L('/gas-pipe-sizing/', 'gas pipe sizing calculator')}. For method, read the {L('/blog/gas-pipe-sizing-longest-length-method/', 'longest length method guide')}.</p>
{sources([('https://up.codes/viewer/washington/ifgc-2021/chapter/4/gas-piping-installations', 'UpCodes: IFGC 2021 Chapter 4, Gas Piping Installations (Section 402 tables)')])}
'''
    return b


FAQS = {
 'conduit-offset-angles-30-45-22-5': [
  ('What is the multiplier for a 30 degree offset?', 'Exactly 2. Multiply the offset depth by 2 to get the distance between the bend marks.'),
  ('What is the shrink for a 45 degree offset?', 'About 3/8 inch per inch of offset depth (exact value 0.414 in.).'),
  ('Which offset angle is easiest to pull wire through?', 'Shallower angles such as 22.5\u00b0 and 30\u00b0 are easier on conductors than 45\u00b0.'),
  ('Why is the 10 degree multiplier 6?', 'The exact value is 5.759; benders print 6 as an easy rounded number, which adds about 4% error.'),
  ('How many degrees does an offset use toward the 360 degree limit?', 'Twice its bend angle, so a 30\u00b0 offset counts 60\u00b0 toward the limit between pull points.')],
 'conduit-saddles-kicks-basics': [
  ('How is a 3-point saddle bent?', 'With a 45\u00b0 center bend and two 22.5\u00b0 outer bends in the opposite direction.'),
  ('How far apart are the saddle marks?', 'The outer marks sit 2.5 times the obstruction height on each side of the center mark (exact 2.613).'),
  ('What is the shrink for a saddle?', 'About 3/16 inch per inch of obstruction height.'),
  ('What is a kick in conduit bending?', 'A single small-angle bend used to line up conduit with a box or change direction slightly.'),
  ('When do I use a saddle instead of an offset?', 'When the conduit must cross an obstruction and return to its original level.')],
 'propane-vs-natural-gas-pipe-sizing': [
  ('Why is propane pipe smaller than natural gas pipe?', 'Propane holds more Btu per cubic foot and is delivered at higher pressure, so the same pipe carries more energy.'),
  ('What units do the propane tables use?', 'Thousands of Btu per hour (MBH), so you use the appliance input directly.'),
  ('How do I convert Btu/h to CFH for natural gas?', 'Divide by the gas heating value, commonly assumed to be 1,000 Btu per cubic foot.'),
  ('Can I use natural gas appliances on propane?', 'Only with a manufacturer conversion kit; orifices and pressure differ.'),
  ('When should I use a 2 psi system?', 'On long runs or large loads where low-pressure pipe would be oversized, with a regulator at each appliance.')],
}

RELATED_GUIDES = {
 '/conduit-offset-multiplier-chart/': [('conduit-offset-angles-30-45-22-5', 'Conduit offset angles compared'), ('conduit-saddles-kicks-basics', 'Saddles and kicks basics')],
 '/30-degree-offset-multiplier/': [('conduit-offset-angles-30-45-22-5', 'Conduit offset angles compared')],
 '/45-degree-offset-multiplier/': [('conduit-offset-angles-30-45-22-5', 'Conduit offset angles compared'), ('conduit-saddles-kicks-basics', 'Saddles and kicks basics')],
 '/22-5-degree-offset-multiplier/': [('conduit-offset-angles-30-45-22-5', 'Conduit offset angles compared'), ('conduit-saddles-kicks-basics', 'Saddles and kicks basics')],
 '/propane-gas-pipe-sizing-chart/': [('propane-vs-natural-gas-pipe-sizing', 'Propane vs natural gas pipe sizing')],
 '/natural-gas-pipe-sizing-chart/': [('propane-vs-natural-gas-pipe-sizing', 'Propane vs natural gas pipe sizing')],
 '/2-psi-propane-pipe-sizing-chart/': [('propane-vs-natural-gas-pipe-sizing', 'Propane vs natural gas pipe sizing')],
}
