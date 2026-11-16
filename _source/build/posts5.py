"""Posts 16-18 (Phase 1, run 2026-11-16). Sources fetched/searched before writing."""
import json, os
from core import url, table, esc

D = json.load(open(os.path.join(os.path.dirname(__file__), 'data', 'electrical.json')))


def L(p, t):
    return f'<a href="{url(p)}">{t}</a>'


def X(h, t):
    return f'<a href="{h}" rel="noopener">{t}</a>'


def sources(items):
    return '<h2>Sources</h2><ul class="sources">' + ''.join(f'<li>{X(h, esc(t))}</li>' for h, t in items) + '</ul>'


NEW_POSTS = [
 ('ampacity-derating-bundled-conductors', 'Ampacity Derating for Bundled Conductors: NEC 310.15(C)(1) Explained',
  'How to derate wire when more than three current-carrying conductors share a raceway: the 80/70/50% factors, what counts, worked 12, 10 and 3 AWG examples.', '2026-11-16'),
 ('detached-garage-subpanel-wire-size', 'Sizing Wire for a Detached Garage Subpanel (60 A at 100 ft Example)',
  'How to size a 4-wire feeder to a detached garage subpanel: ampacity, voltage drop at 100 ft, ground rods, neutral isolation, with a worked 60 A example.', '2026-11-16'),
 ('box-fill-calculation-step-by-step', 'Box Fill Calculation Step by Step (NEC 314.16 with Real Boxes)',
  'Count conductors, clamps, devices and grounds under NEC 314.16, then compare with real box volumes. Worked examples for a receptacle and two-switch box.', '2026-11-16'),
]


def bodies():
    b = {}
    A = D['ampacity']
    c = lambda s, i: A[s]['cu'][i]
    b['ampacity-derating-bundled-conductors'] = f'''
<p class="lead">The ampacities in NEC Table 310.16 assume no more than three current-carrying conductors in a raceway or cable. Add more and they heat each other, so the code makes you reduce each conductor\u2019s ampacity. That reduction is called derating (the code calls it an adjustment factor), and it is the step most often forgotten when a conduit is crowded with extra circuits. This guide shows the factors, what counts toward the total, and three worked examples using our table values.</p>
<h2>The adjustment factors</h2>
<p>Table 310.15(C)(1) gives the percentage of the Table 310.16 value you may use, based on the number of current-carrying conductors:</p>
{table(['Current-carrying conductors', 'Percent of table ampacity', 'Multiplier'], [('1\u20133', '100%', '1.00'), ('4\u20136', '80%', '0.80'), ('7\u20139', '70%', '0.70'), ('10\u201320', '50%', '0.50'), ('21\u201330', '45%', '0.45'), ('31\u201340', '40%', '0.40'), ('41 and above', '35%', '0.35')])}
<p>The factors apply to the Table 310.16 value \u201cas adjusted for ambient temperature if necessary.\u201d When both apply you multiply the table ampacity by the temperature correction and by the bundling factor. The number is counted across the whole raceway or cable, including spare conductors.</p>
<h2>What counts as a current-carrying conductor</h2>
<ul>
<li><b>Hot conductors:</b> always count.</li>
<li><b>Equipment grounding conductors:</b> never count, because they carry current only during a fault.</li>
<li><b>Neutrals:</b> the neutral of a single-phase 3-wire circuit carries only the unbalance and does not count; the neutral of a 4-wire wye circuit feeding nonlinear loads (computers, LED drivers) does count.</li>
<li><b>Conductors that cannot be energized together:</b> for example, the two sets of conductors of a heating and cooling changeover, are not counted.</li>
<li><b>Paralleled sets:</b> each conductor of a paralleled set counts.</li>
</ul>
<h2>When you do not have to derate</h2>
<p>The derating rule has exceptions. It does not apply to conductors in a raceway no longer than 24 in. (a nipple), and it does not apply to underground conductors entering or leaving an outdoor trench if they are protected by RMC, IMC or rigid nonmetallic conduit up to 10 ft long and there are no more than four conductors. The 24-inch nipple is also the reason the code lets you fill short nipples beyond the 40% limit, which our {L('/blog/conduit-fill-40-percent-rule/', 'conduit fill guide')} covers.</p>
<h2>Example 1: 12 AWG THHN, eight conductors</h2>
<p>You pull four 2-wire 12 AWG circuits (eight current-carrying conductors) through one conduit. THHN is rated 90 \u00b0C, so you may start from the 90 \u00b0C column: 12 AWG copper reads {c('12', 2)} A. Eight conductors fall in the 7\u20139 row, so the factor is 70%: {c('12', 2)} \u00d7 0.70 = {c('12', 2) * 0.70:.0f} A. The 75 \u00b0C column gives {c('12', 1)} A at the terminals, which is higher, so the adjusted {c('12', 2) * 0.70:.0f} A governs. A 20 A breaker is allowed, because 12 AWG is limited to 20 A by 240.4(D) and the adjusted ampacity of {c('12', 2) * 0.70:.0f} A matches it.</p>
<h2>Example 2: 10 AWG THHN, six conductors</h2>
<p>Three 2-wire circuits in one conduit is six current-carrying conductors, an 80% factor. 10 AWG copper at 90 \u00b0C is {c('10', 2)} A, so the adjusted ampacity is {c('10', 2)} \u00d7 0.80 = {c('10', 2) * 0.8:.0f} A. At the terminals the 75 \u00b0C value is {c('10', 1)} A, which is not exceeded, so {c('10', 2) * 0.8:.0f} A is the answer. That is enough for a 30 A circuit. Had you used the 60 \u00b0C column from the start ({c('10', 0)} A), the 80% factor would have given {c('10', 0) * 0.8:.0f} A, which would have forced a bigger wire for no reason. This is why the {L('/blog/60c-75c-90c-ampacity-columns-explained/', '90 \u00b0C starting point')} matters.</p>
<h2>Example 3: 3 AWG feeder, six conductors, 100 A load</h2>
<p>Two sets of three conductors share a conduit. 3 AWG copper at 90 \u00b0C reads {c('3', 2)} A, so adjusted: {c('3', 2)} \u00d7 0.80 = {c('3', 2) * 0.8:.0f} A, and the 75 \u00b0C terminal value is {c('3', 1)} A. The lower number wins: {c('3', 2) * 0.8:.0f} A. If the load is 100 A, 3 AWG fails, and you go up one size to 2 AWG: {c('2', 2)} \u00d7 0.80 = {c('2', 2) * 0.8:.0f} A, which covers 100 A (the 75 \u00b0C terminal value of {c('2', 1)} A is also above 100 A). Without the bundling, the 75 \u00b0C column alone would have allowed 3 AWG. The lesson: bundling can cost you one or two wire sizes.</p>
<h2>Practical ways to avoid derating</h2>
<ol>
<li>Split circuits across two raceways so each has three or fewer current-carrying conductors.</li>
<li>Use a larger conduit and a larger wire only where needed; derating hits every conductor in the raceway equally.</li>
<li>Remember that spare conductors count toward the total.</li>
<li>Use the {L('/wire-ampacity-chart/', 'wire ampacity chart')} to read the base values quickly, and check fill with the {L('/conduit-fill-calculator/', 'conduit fill calculator')}.</li>
</ol>
<p>This guide summarizes the code for learning. Your adopted NEC edition and local amendments decide what is allowed on a real job.</p>
{sources([('https://www.nfpa.org/-/media/project/storefront/catalog/files/code-or-topic-fact-sheets/NECAmpacityWorkflow.pdf', 'NFPA: Using the NEC Ampacity Charts workflow (Table 310.15(C)(1))'), ('https://up.codes/s/adjustment-factor-for-conductor-proximity', 'UpCodes: Adjustment factor for conductor proximity (310.15(C)(1) exceptions)'), ('https://www.ecmag.com/magazine/articles/article-detail/codes-standards-what-constitutes-condition-use-considerations-and-calculations-conductors', 'Electrical Contractor: What Constitutes Condition of Use'), ('https://s3.amazonaws.com/mdpelectrical.com/tables/table310-15C1.html', 'Table 310.15(C)(1) text reproduction (mdpelectrical.com)')])}
'''
    t8 = D['t8']
    def vd(s, amps, ft, v=240):
        r = t8[s]['cu'] / 1000.0
        d = 2 * r * ft * amps
        return d, d / v * 100
    d6, p6 = vd('6', 60, 100)
    d4, p4 = vd('4', 60, 100)
    d8, p8 = vd('8', 60, 100)
    d3, p3 = vd('3', 60, 100)
    b['detached-garage-subpanel-wire-size'] = f'''
<p class="lead">Running power to a detached garage or workshop is one of the most common residential projects, and the wire size is rarely just about ampacity. Over 100 feet, voltage drop often decides the size, and the code adds requirements for a separate grounding electrode and an isolated neutral at the garage. This guide walks through a 60 A, 240 V feeder over 100 ft with copper conductors, using our table data.</p>
<h2>Step 1: Decide the feeder rating</h2>
<p>Add up the garage loads (lights, receptacles, a compressor, a welder, an EV charger) using a load calculation and pick a feeder breaker size. We use 60 A for the example. The feeder is a 2-pole breaker in the house panel that feeds a subpanel in the garage with its own main or disconnect. A disconnecting means is required at or in the separate building.</p>
<h2>Step 2: Check ampacity first</h2>
<p>For a 60 A breaker that has no marked terminal rating, 110.14(C) limits you to the 60 \u00b0C column for circuits of 100 A or less unless the equipment is marked for 75 \u00b0C. Most breakers and lugs today are marked 60/75 \u00b0C, so the 75 \u00b0C column usually applies. From our {L('/wire-ampacity-chart/', 'ampacity chart')}, copper at 75 \u00b0C: 8 AWG = {D['ampacity']['8']['cu'][1]} A, 6 AWG = {D['ampacity']['6']['cu'][1]} A, 4 AWG = {D['ampacity']['4']['cu'][1]} A. For a 60 A load, 6 AWG copper (65 A) is the minimum, assuming no derating for bundling or temperature, which you check with the {L('/blog/ampacity-derating-bundled-conductors/', 'derating guide')}.</p>
<h2>Step 3: Check voltage drop over 100 ft</h2>
<p>The NEC recommends in informational notes that feeder and branch-circuit voltage drop each stay within 3%, and no more than 5% total (our {L('/blog/voltage-drop-3-percent-rule/', '3% rule guide')} covers this). For a single-phase 2-wire feeder the drop is 2 \u00d7 resistance per foot \u00d7 length \u00d7 current, using Chapter 9 Table 8 resistances (uncoated copper). At 60 A and 100 ft one way on 240 V:</p>
{table(['Copper size', 'Resistance (ohm/1000 ft)', 'Drop (volts)', 'Drop (% of 240 V)'], [('8 AWG', f"{t8['8']['cu']}", f'{d8:.1f}', f'{p8:.1f}%'), ('6 AWG', f"{t8['6']['cu']}", f'{d6:.1f}', f'{p6:.1f}%'), ('4 AWG', f"{t8['4']['cu']}", f'{d4:.1f}', f'{p4:.1f}%'), ('3 AWG', f"{t8['3']['cu']}", f'{d3:.1f}', f'{p3:.1f}%')])}
<p>With 6 AWG the drop is about {p6:.1f}%, under the 3% guideline, so it works for a full 60 A load. If the garage is 200 ft away the drop doubles to about {2*p6:.1f}% and you would step up to 4 AWG. Check your own length with the {L('/voltage-drop-calculator/', 'voltage drop calculator')}. Real loads are rarely a continuous 60 A, so these are worst-case figures.</p>
<h2>Step 4: Four wires, isolated neutral</h2>
<p>For new work, the feeder to a detached garage has four conductors: two ungrounded (hots), a grounded neutral and a separate equipment grounding conductor [250.32(B)(1)]. At the garage panel, the neutral bar stays isolated from the enclosure and the ground bar; the neutral-to-ground bond exists only at the service in the main building. The older 3-wire feeder with a bonded neutral at the outbuilding was removed from the code for new installations in 2008. If you bonded the neutral at the garage, neutral current would flow on the ground wire and any metal conduit or piping between the buildings.</p>
<p>The equipment grounding conductor is sized from Table 250.122 based on the feeder breaker. For a 60 A breaker that is 10 AWG copper.</p>
<h2>Step 5: Ground rods at the garage</h2>
<p>250.32(A) requires a grounding electrode system at a separate building supplied by a feeder or by more than one branch circuit. A concrete-encased electrode, if present, counts; otherwise two ground rods are the common solution, and the grounding electrode conductor lands on the ground bar. The only exception is a building served by a single branch circuit that includes an equipment grounding conductor.</p>
<h2>Step 6: Wiring method, burial and GFCI</h2>
<p>Conductors can run in PVC conduit underground or in a cable listed for direct burial; see Table 300.5 for burial depth, which depends on the wiring method and whether the run is under a driveway. THWN-2 in PVC is the usual choice, and our {L('/blog/emt-vs-pvc-vs-rigid-conduit/', 'conduit comparison')} covers the pros and cons. Receptacles in a garage need GFCI protection under 210.8, and the garage needs at least one 20 A circuit for receptacles [210.11(C)(4)].</p>
<h2>Quick checklist</h2>
<ol>
<li>Pick the feeder size from a load calculation.</li>
<li>Choose wire by ampacity (75 \u00b0C column), then by voltage drop at your length.</li>
<li>Four conductors: two hots, neutral, EGC from Table 250.122.</li>
<li>Isolate neutral and ground at the garage panel; add a disconnect.</li>
<li>Install ground rods or a concrete-encased electrode.</li>
<li>Get a permit and inspection; local rules and the adopted NEC edition decide.</li>
</ol>
{sources([('https://electricaltoolbox.com/separate-structure-grounding-calculator', 'ElectricalToolbox: Separate structure grounding (NEC 250.32)'), ('https://www.ecmag.com/magazine/articles/article-detail/codes-standards-equipment-and-structure-grounding-and-bonding-separate-buildings-or', 'Electrical Contractor: Grounding and Bonding at Separate Buildings or Structures'), ('https://www.stpaul.gov/sites/default/files/2023-06/DSI.Bldg_Electrical_Checklist%20Garage.pdf', 'City of St. Paul: Residential Checklist 2023 NEC (Garage)'), ('https://solardesignlab.com/subpanel-neutral-ground-separation', 'Solar Design Lab: Why subpanels separate neutral and ground')])}
'''
    bx = {n: v for n, v in D['boxes']}
    b['box-fill-calculation-step-by-step'] = f'''
<p class="lead">A box that is too full means crowded wires, damaged insulation and a failed inspection. NEC 314.16 sets the rule: add up the volume allowance for every conductor, clamp, device and ground, and compare it with the box\u2019s marked volume in cubic inches. This guide shows the counting rules, then works two real examples against box volumes from Table 314.16(A).</p>
<h2>Step 1: Know the volume per conductor</h2>
<p>Table 314.16(B) gives each conductor size a volume allowance:</p>
{table(['Wire size', 'Allowance (cu in.)'], [(f'{k} AWG', f'{v:.2f}') for k, v in D['box_allow'].items()])}
<h2>Step 2: Count what is in the box</h2>
{table(['Item in the box', 'Allowances', 'Sized by'], [('Each conductor that enters and is spliced or terminated', '1 each', 'Its own size'), ('Conductor that passes through unbroken', '1', 'Its own size'), ('Loop of unbroken conductor 12 in. or longer', '2', 'Its own size'), ('Pigtail that never leaves the box', '0', 'n/a'), ('Internal cable clamps (one or many)', '1 total', 'Largest conductor in the box'), ('Luminaire stud or hickey', '1 per type', 'Largest conductor'), ('Each device yoke (switch, receptacle)', '2 per yoke', 'Largest conductor connected to it'), ('Equipment grounding conductors', '1 for up to 4', 'Largest ground')])}
<p>Clamps that sit outside the box and plastic-box clamps already included in the marked volume add nothing. Small fittings such as locknuts and bushings need no allowance.</p>
<h2>Example 1: A receptacle fed through</h2>
<p>A single-gang box holds one duplex receptacle and two 12/2 NM cables with ground, with internal clamps.</p>
{table(['Item', 'Count', 'Volume'], [('12 AWG conductors (2 hots + 2 neutrals)', '4 \u00d7 2.25', '9.00'), ('Internal clamps', '1 \u00d7 2.25', '2.25'), ('Receptacle yoke', '2 \u00d7 2.25', '4.50'), ('Grounds (2 count as one)', '1 \u00d7 2.25', '2.25'), ('Total', '8 allowances', '18.00 cu in.')])}
<p>Our box table lists a 3 \u00d7 2 \u00d7 3-1/2 device box at {bx['3 x 2 x 3-1/2 device']:.1f} cu in., which fits exactly, and a 4 \u00d7 1-1/2 square box at {bx['4 x 1-1/2 square']:.1f} cu in., which fits with room to spare. A shallow 3 \u00d7 2 \u00d7 2-1/2 box ({bx['3 x 2 x 2-1/2 device']:.1f} cu in.) does not.</p>
<h2>Example 2: Two switches on three 14/2 cables</h2>
<p>A two-gang opening holds two switches with three 14/2 cables with ground.</p>
{table(['Item', 'Count', 'Volume'], [('14 AWG conductors', '6 \u00d7 2.00', '12.00'), ('Internal clamps', '1 \u00d7 2.00', '2.00'), ('Two switch yokes', '2 \u00d7 2 \u00d7 2.00', '8.00'), ('Grounds (3 count as one)', '1 \u00d7 2.00', '2.00'), ('Total', '12 allowances', '24.00 cu in.')])}
<p>A 4-11/16 \u00d7 1-1/4 square box holds {bx['4-11/16 x 1-1/4 square']:.1f} cu in. and passes; a 4 \u00d7 1-1/2 square ({bx['4 x 1-1/2 square']:.1f}) does not. A 4 \u00d7 2-1/8 square at {bx['4 x 2-1/8 square']:.1f} cu in. also passes with room for a plaster ring extension.</p>
<h2>Mixed wire sizes</h2>
<p>When 12 AWG and 14 AWG share a box, count each conductor at its own size; clamps and grounds use the largest conductor in the box, and each device yoke uses the largest conductor connected to that device. A switch on a 14 AWG circuit counts at 2.00 even if a 12 AWG circuit is elsewhere in the box.</p>
<h2>Common mistakes</h2>
<ul>
<li>Counting every ground separately; up to four count as one, and in recent editions each extra adds a quarter allowance.</li>
<li>Counting the device as one instead of two allowances.</li>
<li>Counting pigtails that start and end inside the box.</li>
<li>Forgetting the volume marked on the box already includes extensions you did not install.</li>
<li>Using a box with a barrier without calculating each space separately.</li>
</ul>
<h2>Use the tools</h2>
<p>Run your own numbers with the {L('/box-fill-calculator/', 'box fill calculator')}. If conductors go on to conduit, check wire counts with the {L('/blog/how-many-wires-in-3-4-emt/', 'EMT wire count guide')}. Always confirm with the adopted NEC edition and the inspector.</p>
{sources([('https://up.codes/s/box-fill-calculations', 'UpCodes: Box fill calculations (314.16(B))'), ('https://codes.iccsafe.org/s/ISEP2021P1/national-electrical-code-nec-solar-provisions/ISEP2021P1-NEC-Sec314.16', 'ICC: NEC Section 314.16 text'), ('https://www.field-pm.com/charts/nec-box-fill-rules', 'Field PM: How to calculate box fill with NEC 314.16'), ('https://necwire.com/box-fill-calculator', 'NECwire: Box fill calculator worked examples')])}
'''
    return b


FAQS = {
 'ampacity-derating-bundled-conductors': [
  ('When do I have to derate conductors in conduit?', 'When more than three current-carrying conductors share a raceway or cable longer than 24 inches, per Table 310.15(C)(1).'),
  ('Do ground wires count toward derating?', 'No. Equipment grounding conductors do not count as current-carrying conductors.'),
  ('Does the neutral count?', 'Usually not on a single-phase 3-wire circuit, but yes on a 4-wire wye circuit that feeds nonlinear loads.'),
  ('What is the factor for 7 to 9 conductors?', '70% of the Table 310.16 ampacity.'),
  ('Is derating applied to the 60\u00b0C or 90\u00b0C column?', 'Start from the insulation rating (90\u00b0C for THHN), apply the factors, and make sure the result does not exceed the termination temperature column.')],
 'detached-garage-subpanel-wire-size': [
  ('What size wire for a 60 amp subpanel?', 'By ampacity, 6 AWG copper (65 A at 75\u00b0C). Check voltage drop for long runs; at 100 ft and 60 A, 6 AWG gives about 2.5% drop.'),
  ('Does a detached garage need a ground rod?', 'Generally yes: a feeder or more than one branch circuit requires a grounding electrode at the building under 250.32(A).'),
  ('Should the neutral and ground be bonded in a garage subpanel?', 'No. With a 4-wire feeder, the neutral bar is isolated and bonding happens only at the main service.'),
  ('Can I run a 3-wire feeder to a garage?', 'Not for new work. The allowance was removed in the 2008 NEC; use two hots, a neutral and a ground.'),
  ('Is a disconnect required at the garage?', 'Yes, a disconnecting means is required at or in the separate building.')],
 'box-fill-calculation-step-by-step': [
  ('How many cubic inches per 12 AWG wire?', '2.25 cubic inches per conductor, from Table 314.16(B).'),
  ('How does a device count in box fill?', 'Each yoke counts as two conductor allowances, sized by the largest conductor connected to it.'),
  ('Do ground wires count in box fill?', 'All equipment grounding conductors together count as one allowance of the largest ground, with extra allowance when more than four enter.'),
  ('Do wire nuts or pigtails count?', 'Wire connectors need no allowance and pigtails that stay inside the box count zero.'),
  ('Do cable clamps count?', 'Internal clamps count once total at the largest conductor; external clamps count nothing.')],
}

RELATED_GUIDES = {
 '/wire-ampacity-chart/': [('ampacity-derating-bundled-conductors', 'Ampacity derating for bundled conductors'), ('detached-garage-subpanel-wire-size', 'Sizing wire for a detached garage subpanel')],
 '/12-awg-wire-ampacity/': [('ampacity-derating-bundled-conductors', 'Ampacity derating for bundled conductors')],
 '/10-awg-wire-ampacity/': [('ampacity-derating-bundled-conductors', 'Ampacity derating for bundled conductors')],
 '/3-awg-wire-ampacity/': [('ampacity-derating-bundled-conductors', 'Ampacity derating for bundled conductors')],
 '/conduit-fill-calculator/': [('ampacity-derating-bundled-conductors', 'Ampacity derating for bundled conductors')],
 '/voltage-drop-calculator/': [('detached-garage-subpanel-wire-size', 'Sizing wire for a detached garage subpanel')],
 '/6-awg-wire-ampacity/': [('detached-garage-subpanel-wire-size', 'Sizing wire for a detached garage subpanel')],
 '/box-fill-calculator/': [('box-fill-calculation-step-by-step', 'Box fill calculation step by step')],
}
