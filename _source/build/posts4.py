"""Posts 13-15 (Phase 1, run 2026-11-15). Sources fetched and read before writing."""
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
 ('emt-vs-pvc-vs-rigid-conduit', 'EMT vs PVC vs Rigid Conduit: Which Raceway to Choose',
  'EMT, PVC and rigid (RMC) compared by NEC article: where each is allowed, what each cannot do, support, expansion, grounding and the fill area you get.', '2026-11-15'),
 ('how-many-wires-in-3-4-emt', 'How Many Wires Fit in 3/4 EMT? Worked Examples by Wire Size',
  'How many THHN wires fit in 3/4 inch EMT: 14, 12, 10, 8 and 6 AWG counts at the 40% limit, the math behind them, mixed-size example and derating.', '2026-11-15'),
 ('60c-75c-90c-ampacity-columns-explained', '60\u00b0C vs 75\u00b0C vs 90\u00b0C Ampacity Columns Explained (NEC 110.14(C))',
  'Which column of NEC Table 310.16 to use: why THHN wire is 90\u00b0C but you size to 60\u00b0C or 75\u00b0C, with 10, 6 and 3 AWG examples and the termination rule.', '2026-11-15'),
]


def bodies():
    b = {}
    E, P, R = D['conduit']['EMT'], D['conduit']['PVC-40'], D['conduit']['RMC']
    P80 = D['conduit']['PVC-80']
    rows = [(s, f"{E[s]['id_in']:.3f}", f"{P[s]['id_in']:.3f}", f"{P80[s]['id_in']:.3f}", f"{R[s]['id_in']:.3f}", f"{E[s]['a40']:.3f}", f"{P[s]['a40']:.3f}", f"{P80[s]['a40']:.3f}", f"{R[s]['a40']:.3f}") for s in ('1/2', '3/4', '1', '1-1/4', '2')]
    b['emt-vs-pvc-vs-rigid-conduit'] = f'''
<p class="lead">Choosing between EMT, PVC and rigid metal conduit (RMC) is mostly a question of where the pipe will live. Indoors and protected, EMT is the cheap, fast answer. Underground or in a wet, corrosive spot, PVC is the usual pick. Where the raceway can be hit by a forklift or must carry a hazardous-location rating, you move to rigid. This guide lines the three up by NEC article so you can decide with the code in your hand, and shows how much wire space each gives you.</p>
<h2>The three at a glance</h2>
{table(['', 'EMT', 'PVC (Sch 40/80)', 'Rigid metal (RMC)'], [('NEC article', '358', '352', '344'), ('Material', 'Thin-wall steel or aluminum tubing', 'Rigid plastic', 'Thick-wall threaded steel'), ('Joining', 'Set-screw or compression fittings, no threads', 'Solvent-weld', 'Threaded couplings or threadless fittings'), ('Doubles as ground path?', 'Yes, with listed fittings', 'No, run a separate grounding conductor', 'Yes'), ('Severe physical damage', 'Not permitted [358.12]', 'Schedule 80 only [352.10(F)]', 'Permitted [344.10(A)]'), ('Trade size range', '1/2 to 6', '1/2 to 6 [352.20]', '1/2 to 6')])}
<h2>EMT: the indoor workhorse</h2>
<p>Electrical metallic tubing is light, easy to cut and bends with a hand bender, which is why it dominates commercial branch-circuit work. Section 358.10 permits it exposed and concealed, in dry, damp or wet locations, and in concrete in direct contact with the earth when it is protected by approved corrosion protection. In wet locations the fittings must be listed for wet locations, and the support screws and straps must be corrosion resistant.</p>
<p>What EMT cannot do: it is not permitted where subject to severe physical damage, and it cannot support luminaires or other equipment (a conduit body no larger than the tubing is the exception) [358.12]. Because the tube is thin, a flattened or dented section is easy to create; the {L('/conduit-offset-multiplier-chart/', 'offset multiplier chart')} helps you bend neatly and avoid kinks.</p>
<h2>PVC: underground, wet and corrosive</h2>
<p>PVC does not rust, so it is the common choice for burial and for wet or corrosive spots. The trade-offs are written into Article 352:</p>
<ul>
<li><b>Physical damage:</b> PVC is not permitted where subject to physical damage unless identified for the application. Schedule 40 is not identified for that use; Schedule 80 is.</li>
<li><b>Temperature:</b> not permitted where the ambient temperature exceeds 50 \u00b0C (122 \u00b0F) [352.12(D)], and not in plenums.</li>
<li><b>Support:</b> secure within 3 ft of every box, cabinet or termination fitting, then at the intervals in Table 352.30.</li>
<li><b>Expansion:</b> install expansion fittings in straight runs between fixed points where the expected length change is 1/4 in. or more [352.44]. With sun exposure, installers add 30 \u00b0F to the high ambient temperature when sizing for expansion, per the fitting maker.</li>
<li><b>Grounding:</b> plastic is not a ground path, so a separate equipment grounding conductor goes in the pipe.</li>
</ul>
<h2>Rigid metal conduit: maximum protection</h2>
<p>EC&amp;M\u2019s code summary notes that RMC and IMC can be used in all atmospheric conditions and occupancies, can be used where subject to physical damage (no other metal raceway can), and can go in concrete or direct burial with approved corrosion protection. They are also usable in hazardous locations, while EMT cannot. RMC can be threaded; if it is, a bushing must protect the conductors where they exit. The price is weight, labor and cost: a threaded run takes much longer to install than the same size of EMT.</p>
<h2>How much wire space you get</h2>
<p>At the same trade size the inside diameters are different, so the 40% fill area differs. Using the areas on our fill charts (NEC Chapter 9 Table 4), here is the usable area for more than two wires:</p>
{table(['Trade size', 'EMT ID (in)', 'PVC 40 ID', 'PVC 80 ID', 'RMC ID', 'EMT 40% (sq in)', 'PVC 40 40%', 'PVC 80 40%', 'RMC 40%'], rows)}
<p>The pattern: PVC Schedule 80 has the thickest wall, so it holds the least; EMT and rigid are close, with EMT slightly smaller at 3/4 in. than rigid. Check an exact size on the {L('/emt-conduit-fill-chart/', 'EMT')}, {L('/pvc-conduit-fill-chart/', 'PVC')} and {L('/rigid-conduit-fill-chart/', 'rigid')} fill charts, or run the {L('/conduit-fill-calculator/', 'conduit fill calculator')}. Our {L('/blog/conduit-fill-40-percent-rule/', '40% rule guide')} explains how the limit is applied.</p>
<h2>A quick decision guide</h2>
<ol>
<li><b>Exposed to vehicles or impact?</b> Use RMC or IMC (or PVC Schedule 80 where allowed).</li>
<li><b>Buried or in a corrosive, wet spot?</b> PVC is the usual first choice; RMC with corrosion protection also works.</li>
<li><b>Hazardous (classified) location?</b> Rigid or IMC, following the hazardous-location articles; not EMT, and not PVC except where specifically permitted.</li>
<li><b>Indoor, dry, protected run?</b> EMT is the standard.</li>
<li><b>Short connection to vibrating equipment?</b> Add a flexible whip for the last few feet, with a wire-type grounding conductor or a length within the 250.118 limits.</li>
</ol>
<p>Always confirm with your local inspector: jurisdictions adopt different NEC editions and add amendments, and the permitted-use sections above are summaries, not a substitute for the code text.</p>
{sources([('https://www.mikeholt.com/newsletters.php?action=display&letterID=2720', 'Mike Holt, EC&M: NEC Questions and Answers based on the 2020 NEC (PVC Art. 352, EMT Art. 358)'), ('https://www.ecmweb.com/national-electrical-code/code-basics/article/55371892/nec-requirements-for-metal-raceways', 'EC&M: NEC Requirements for Metal Raceways'), ('https://www.ecmag.com/magazine/articles/article-detail/codes-standards-general-installation-requirements-part-viii', 'Electrical Contractor: General Installation Requirements, Part VIII')])}
'''
    # ---- 3/4 EMT
    a = E['3/4']['a40']
    A = D['wire_area']['THHN']
    cnt = lambda w, area=a: int(area / A[w] + 1e-9)
    wr = [(w + ' AWG', f'{A[w]:.4f}', cnt(w), f'{cnt(w) * A[w]:.3f}') for w in ('14', '12', '10', '8', '6')]
    mix = 4 * A['12'] + 3 * A['10']
    b['how-many-wires-in-3-4-emt'] = f'''
<p class="lead">The quick answer for ordinary THHN wire in 3/4 inch EMT: 21 conductors of 14 AWG, 16 of 12 AWG, 10 of 10 AWG, 5 of 8 AWG or 4 of 6 AWG, all at the NEC 40% fill limit. Those numbers come straight from the Chapter 9 tables, but the real answer on a job also depends on what else is in the pipe, how many wires are carrying current and how the ampacity is derated. This page shows the math and works three examples.</p>
<h2>The inputs</h2>
<p>NEC Chapter 9 Table 4 gives 3/4 trade size EMT an internal area of {E['3/4']['area']} sq in. (inside diameter {E['3/4']['id_in']} in.). For more than two conductors the maximum fill is 40% of that area, which is {a} sq in. Table 5 gives the area of each conductor; for THHN the values are in the table below. The count is the usable area divided by the wire area, always rounded <i>down</i>, because you cannot install a fraction of a wire.</p>
{table(['THHN size', 'Area each (sq in)', 'Max wires at 40%', 'Area used (sq in)'], wr)}
<p>Use the {L('/3-4-emt-conduit-fill/', '3/4 EMT fill page')} for the full list including XHHW, or the {L('/conduit-fill-calculator/', 'conduit fill calculator')} for your own mix.</p>
<h2>Example 1: a home-run of 12 AWG circuits</h2>
<p>Suppose you want to pull several 20-amp, 120-volt circuits in one pipe. Each circuit needs a hot, a neutral and (usually) a ground, and all three count toward fill. Eight conductors of 12 AWG take {8 * A['12']:.3f} sq in., well inside the {a} limit. Even 16 conductors of 12 AWG ({16 * A['12']:.3f} sq in.) fit. So fill is not the constraint here; ampacity derating is, as explained below.</p>
<h2>Example 2: mixed 12 and 10 AWG</h2>
<p>You need four 12 AWG and three 10 AWG THHN conductors. Add the areas: 4 \u00d7 {A['12']} + 3 \u00d7 {A['10']} = {mix:.4f} sq in. Compare it with {a}: {'it fits' if mix <= a else 'it does not fit'}, with {a - mix:.3f} sq in. to spare. For a mix you always add areas rather than counting wires.</p>
<h2>Example 3: how many 6 AWG feeders?</h2>
<p>Four 6 AWG THHN conductors use {4 * A['6']:.4f} sq in. A fifth would be {5 * A['6']:.4f} sq in., over the {a} limit. If those four are the neutral plus three hots of a subpanel feeder, the ground goes in too, and Table 5 area must include it; a smaller bare or insulated ground adds to the total, so check it with the calculator before you buy the wire.</p>
<h2>Grounding conductors and nipples</h2>
<p>Equipment grounding conductors count in the fill calculation when they are installed in the raceway. NEC Chapter 9 Table 1 Note 4 also allows 60% fill for a raceway section 24 inches or shorter (a nipple), and our {L('/blog/conduit-fill-40-percent-rule/', '40% rule guide')} covers that note and the rounding rule in detail.</p>
<h2>Fill is not the same as ampacity</h2>
<p>Electrical Contractor magazine points out that the ampacity values in Table 310.15(B)(16) (now 310.16) assume no more than three current-carrying conductors in the raceway and a 30 \u00b0C (86 \u00b0F) ambient. Put 16 current-carrying wires in a 3/4 pipe and the code requires you to adjust the ampacity down, often by half or more. In practice that means that you may physically fit 16 wires but need a larger wire size, or two pipes, to carry the load. Our {L('/wire-ampacity-chart/', 'wire ampacity chart')} gives base values, and the {L('/voltage-drop-calculator/', 'voltage drop calculator')} checks long runs.</p>
<h2>Pulling tips for a full 3/4 pipe</h2>
<ul>
<li>Pull all conductors together rather than adding wires later; a second pull drags on the first set.</li>
<li>Keep bends under the NEC limit of 360 degrees total between pull points, offsets included.</li>
<li>Use listed wire-pulling lubricant for the heavier counts and larger sizes.</li>
<li>If the count is close to the limit, step up to 1 inch EMT. It holds roughly 62% more wire area than 3/4 inch ({E['1']['a40']} vs {a} sq in.).</li>
</ul>
<p>Rules and tables vary slightly by code edition and by local amendment, so confirm with your inspector before ordering material.</p>
{sources([('https://www.ecmag.com/magazine/articles/article-detail/codes-standards-sizing-conductors', 'Electrical Contractor: Sizing Conductors (ampacity table assumptions)'), ('https://ecmag.com/section/codes-standards/sizing-conductors', 'Electrical Contractor: Sizing Conductors, Code in Focus (Table 310.15(B)(16))'), ('https://www.ecmweb.com/national-electrical-code/code-basics/article/55371892/nec-requirements-for-metal-raceways', 'EC&M: NEC Requirements for Metal Raceways (360-degree bend limit)')])}
'''
    b['60c-75c-90c-ampacity-columns-explained'] = f'''
<p class="lead">NEC Table 310.16 gives three ampacities for each wire size: one under 60 \u00b0C, one under 75 \u00b0C and one under 90 \u00b0C. THHN wire is marked 90 \u00b0C, so it seems natural to read the 90 \u00b0C column. Usually you cannot. Section 110.14(C) ties the ampacity you may use to the temperature rating of the terminals at the ends of the circuit, and those are mostly rated 60 \u00b0C or 75 \u00b0C. This guide explains the rule and works three examples with our table values.</p>
<h2>The rule in one sentence</h2>
<p>NEC 110.14(C) says the temperature rating associated with a conductor\u2019s ampacity must be selected and coordinated so as not to exceed the lowest temperature rating of any connected termination, conductor or device. Charles Miller, writing in Electrical Contractor, compares it to a chain: it is only as strong as the weakest link. If a 90 \u00b0C conductor has a 60 \u00b0C terminal on one end and a 75 \u00b0C terminal on the other, the 60 \u00b0C terminal governs.</p>
<h2>Which column when you do not know the terminals</h2>
<p>The code supplies defaults, based on the circuit rating or the conductor sizes the equipment is marked for:</p>
{table(['Equipment', 'Default column', 'Code reference'], [('Circuits rated 100 A or less, or terminals marked for 14 AWG through 1 AWG', '60 \u00b0C', '110.14(C)(1)(a)'), ('Circuits rated over 100 A, or terminals marked for conductors larger than 1 AWG', '75 \u00b0C', '110.14(C)(1)(b)')])}
<p>A higher column is allowed only when the equipment is listed and identified for it. A common example: the terminals are marked 60/75 \u00b0C, meaning listed for both 60 \u00b0C and 75 \u00b0C conductors, so a THHN conductor may be sized from the 75 \u00b0C column. Miller also warns that very little equipment is listed and identified for use with 90 \u00b0C conductors at their 90 \u00b0C ampacity: only individual lugs, terminal bars and equipment for circuits over 600 volts. The conductor\u2019s ampacity must also never exceed the lowest-rated termination.</p>
<h2>So why buy 90 \u00b0C wire?</h2>
<p>Because the 90 \u00b0C column is still useful for adjustment and correction. The code lets you start from the 90 \u00b0C ampacity when you apply ambient-temperature correction or conductor-bundling adjustment, as long as the final result does not exceed the termination column. For a hot attic, a bundle of many wires or a long conduit run in the sun, that extra starting number can save a wire size.</p>
<h2>Worked values from the table</h2>
{table(['Copper size', '60 \u00b0C', '75 \u00b0C', '90 \u00b0C'], [(w + ' AWG', *D['ampacity'][w]['cu']) for w in ('10', '8', '6', '4', '3', '1', '1/0')])}
<p>Look at the full table on our {L('/wire-ampacity-chart/', 'wire ampacity chart')}, or pick a single size such as {L('/10-awg-wire-ampacity/', '10 AWG')} or {L('/6-awg-wire-ampacity/', '6 AWG')}.</p>
<h3>Example 1: 10 AWG THHN to a 30 A breaker</h3>
<p>Typical 30 A residential circuit, equipment marked for 14\u20131 AWG, no other information. The default is the 60 \u00b0C column: 10 AWG copper is rated {D['ampacity']['10']['cu'][0]} A, enough for a 30 A load. Had the equipment been listed and marked for 75 \u00b0C, the value would be {D['ampacity']['10']['cu'][1]} A, but the common 30 A overcurrent limit for 10 AWG copper still applies [240.4(D)], which is a separate rule from this table.</p>
<h3>Example 2: 6 AWG THHN feeding a 60 A subpanel breaker</h3>
<p>At 60 A the default is again 60 \u00b0C, so 6 AWG copper counts as {D['ampacity']['6']['cu'][0]} A. That is too small for a 60 A breaker. With 75 \u00b0C terminals (very common on modern breakers and lugs) it counts as {D['ampacity']['6']['cu'][1]} A, which works. This is why the label on the equipment matters.</p>
<h3>Example 3: 3 AWG to a 100 A feeder</h3>
<p>3 AWG copper reads {D['ampacity']['3']['cu'][0]} A at 60 \u00b0C, {D['ampacity']['3']['cu'][1]} A at 75 \u00b0C and {D['ampacity']['3']['cu'][2]} A at 90 \u00b0C. With 75 \u00b0C terminals the conductor carries {D['ampacity']['3']['cu'][1]} A, matching a 100 A device. The 90 \u00b0C value of {D['ampacity']['3']['cu'][2]} A could only be used as the starting point for derating, never as the final rating at the lugs.</p>
<h2>Checklist before you size a conductor</h2>
<ol>
<li>Read the marked temperature rating on every breaker, lug and device on the circuit; the lowest one rules.</li>
<li>If a rating is unknown, use the 60 \u00b0C column (100 A or less) or the 75 \u00b0C column (over 100 A).</li>
<li>Apply ambient-temperature and bundling adjustments from the insulation\u2019s own column, then confirm the result does not exceed the termination column.</li>
<li>Check voltage drop on long runs with the {L('/voltage-drop-calculator/', 'voltage drop calculator')} and fill with the {L('/conduit-fill-calculator/', 'conduit fill calculator')}.</li>
</ol>
<p>This guide summarizes the code for learning; your adopted NEC edition and local amendments decide what is allowed on a real job.</p>
{sources([('https://ecmag.com/section/codes-standards/sizing-conductors', 'Electrical Contractor (Charles R. Miller): Sizing Conductors, NEC Table 310.15(B)(16) and Termination Temps'), ('https://www.ecmag.com/magazine/articles/article-detail/codes-standards-general-installation-requirements-part-viii', 'Electrical Contractor: General Installation Requirements, Part VIII (110.14(C))'), ('https://www.nfpa.org/-/media/project/storefront/catalog/files/code-or-topic-fact-sheets/NECAmpacityWorkflow.pdf', 'NFPA: Using the NEC Ampacity Charts workflow')])}
'''
    return b


FAQS = {
 'emt-vs-pvc-vs-rigid-conduit': [
  ('Can I use EMT underground?', 'EMT may be installed in concrete in direct contact with the earth when approved corrosion protection is provided [358.10(B)], but PVC is the more common choice for burial.'),
  ('Does PVC conduit need a ground wire?', 'Yes. PVC is nonmetallic, so it cannot serve as the equipment grounding path and a separate grounding conductor is installed in the pipe.'),
  ('When is Schedule 80 PVC required?', 'When the conduit is subject to physical damage: Schedule 40 is not identified for that use, Schedule 80 is [352.10(F)].'),
  ('Can EMT be used outdoors?', 'Yes, in wet locations when the fittings are listed for wet locations and the support hardware is corrosion resistant [358.10, 358.42].'),
  ('Which conduit holds the most wire at 3/4 trade size?', 'Rigid has the largest 40% area on our charts (0.220 sq in.), followed by EMT (0.213), PVC 40 (0.203) and PVC 80.')],
 'how-many-wires-in-3-4-emt': [
  ('How many 12 AWG THHN wires fit in 3/4 EMT?', '16, based on 0.213 sq in. of usable area (40% of 0.533) divided by 0.0133 sq in. per wire.'),
  ('How many 10 AWG wires fit in 3/4 EMT?', '10 conductors of THHN fit at the 40% limit.'),
  ('Do ground wires count toward conduit fill?', 'Yes. Equipment grounding conductors installed in the raceway are included in the fill calculation.'),
  ('Is the number of wires limited by ampacity too?', 'Yes. Table ampacities assume no more than three current-carrying conductors; more than that requires an ampacity adjustment.'),
  ('Can I fill a short nipple to 60%?', 'Yes. A raceway section 24 inches or shorter may be filled to 60% under Chapter 9 Table 1 Note 4.')],
 '60c-75c-90c-ampacity-columns-explained': [
  ('Why can\u2019t I use the 90\u00b0C column for THHN?', 'Because 110.14(C) limits ampacity to the lowest temperature rating of any termination, and most terminals are rated 60\u00b0C or 75\u00b0C.'),
  ('Which column do I use for a 30 amp circuit?', 'With no other marking, the 60\u00b0C column, because the circuit is rated 100 A or less. Terminals listed and marked for 75\u00b0C allow the 75\u00b0C column.'),
  ('When is the 75\u00b0C column the default?', 'For circuits over 100 A or terminals marked for conductors larger than 1 AWG [110.14(C)(1)(b)].'),
  ('What is the benefit of 90\u00b0C rated wire?', 'You can start ambient-temperature correction and bundling adjustment from the 90\u00b0C value, provided the final ampacity does not exceed the termination column.'),
  ('What does a 60/75\u00b0C terminal marking mean?', 'The equipment is listed for both 60\u00b0C and 75\u00b0C conductors, so 75\u00b0C-rated wire may be sized from the 75\u00b0C column.')],
}

RELATED_GUIDES = {
 '/emt-conduit-fill-chart/': [('emt-vs-pvc-vs-rigid-conduit', 'EMT vs PVC vs rigid conduit'), ('how-many-wires-in-3-4-emt', 'How many wires fit in 3/4 EMT')],
 '/3-4-emt-conduit-fill/': [('how-many-wires-in-3-4-emt', 'How many wires fit in 3/4 EMT')],
 '/pvc-conduit-fill-chart/': [('emt-vs-pvc-vs-rigid-conduit', 'EMT vs PVC vs rigid conduit')],
 '/rigid-conduit-fill-chart/': [('emt-vs-pvc-vs-rigid-conduit', 'EMT vs PVC vs rigid conduit')],
 '/conduit-fill-calculator/': [('how-many-wires-in-3-4-emt', 'How many wires fit in 3/4 EMT')],
 '/wire-ampacity-chart/': [('60c-75c-90c-ampacity-columns-explained', '60\u00b0C vs 75\u00b0C vs 90\u00b0C columns explained')],
 '/10-awg-wire-ampacity/': [('60c-75c-90c-ampacity-columns-explained', '60\u00b0C vs 75\u00b0C vs 90\u00b0C columns explained')],
 '/6-awg-wire-ampacity/': [('60c-75c-90c-ampacity-columns-explained', '60\u00b0C vs 75\u00b0C vs 90\u00b0C columns explained')],
 '/12-awg-wire-ampacity/': [('60c-75c-90c-ampacity-columns-explained', '60\u00b0C vs 75\u00b0C vs 90\u00b0C columns explained')],
}
