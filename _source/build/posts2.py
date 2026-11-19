"""Blog posts added after launch (Phase 1 build-out), FAQs for every post, and expansions of the launch posts.
Every factual claim is tied to a cited source (listed in each post's Sources section) or computed from this site's verified PT data."""
from core import url, table, esc
from pages_hvac import BY, REFS, pf, tp, ps, glide


def L(p, t):
    return f'<a href="{url(p)}">{t}</a>'


def X(href, t):
    return f'<a href="{href}" rel="noopener">{t}</a>'


def sources(items):
    return '<h2>Sources</h2><ul class="sources">' + ''.join(f'<li>{X(h, esc(t))}</li>' for h, t in items) + '</ul>'


# slug, title, description, date published
NEW_POSTS = [
 ('r454b-service-basics', 'R-454B Service Basics for R-410A Techs: Pressures, Tools, Charging',
  'What changes when an R-410A tech services R-454B: lower pressures for the same coil temperature, glide, A2L tools, red-band cylinders and charging steps.', '2026-11-13'),
 ('a2l-tools-leak-detectors-recovery-machines', 'A2L Tools: Leak Detectors, Recovery Machines and What Changes',
  'Which tools must change for A2L refrigerants like R-454B and R-32: non-sparking recovery machines and vacuum pumps, sealed leak detectors, red-band cylinders.', '2026-11-13'),
 ('refrigerant-temperature-glide', 'Refrigerant Temperature Glide: Why Blends Have Two Pressures',
  'Temperature glide explained: why zeotropic blends show bubble and dew columns, glide values for 20 blends from our charts, and how glide changes charging.', '2026-11-13'),
]


def new_bodies():
    r410, r454, r32 = BY['r410a'], BY['r454b'], BY['r32']
    b = {}
    # ---------------- R-454B service basics ----------------
    rows = []
    for F in (20, 40, 45, 100, 110, 120):
        rows.append((f'{F} \u00b0F', ps(pf(r410, F, 1)), ps(pf(r454, F, 1)), ps(pf(r454, F, 0))))
    t118d = tp(r454, 118.0, 1)
    d40, b40 = pf(r454, 40, 1), pf(r454, 40, 0)
    p410_40 = pf(r410, 40, 1)
    b100, p410_100 = pf(r454, 100, 0), pf(r410, 100, 0)
    t300b = tp(r454, 300.0, 0)
    t300_410 = tp(r410, 300.0, 0)
    g454 = glide(r454, 40)
    b['r454b-service-basics'] = f'''
<p class="lead">R-454B is the refrigerant most US residential split-system manufacturers moved to when new equipment had to drop below 700 GWP. For a tech who knows R-410A the good news is that it runs at similar pressures with the same POE oil. The differences are small but they matter: slightly lower pressures for the same coil temperature, a little glide, and the A2L (mildly flammable) safety rules.</p>
<h2>Why R-454B is showing up on your calls</h2>
<p>Under the EPA Technology Transitions rule, new residential and light commercial air conditioners and heat pumps manufactured or imported from January 1, 2025 must use a refrigerant with a GWP below 700. R-410A (GWP 2,088) does not qualify; R-454B does. In May 2026 EPA finalized a revision that removed the January 1, 2026 installation deadline for R-410A systems built or imported before 2025, so you will keep seeing both refrigerants side by side for years: new R-454B installs, existing R-410A systems, and leftover R-410A inventory still being installed. Repairs of existing R-410A systems are not restricted by these rules.</p>
<h2>What R-454B is</h2>
{table(['Property', 'R-454B', 'R-410A'], [('Composition (weight %)', 'R-32 / R-1234yf 68.9 / 31.1', 'R-32 / R-125 50 / 50'), ('ASHRAE safety class', 'A2L (lower toxicity, mildly flammable)', 'A1 (no flame propagation)'), ('GWP (AR4)', '466', '2,088'), ('Oil', 'POE', 'POE'), ('Glide', '~1.1 K (~2 \u00b0F) at atmospheric pressure per Chemours; about 2.7 \u00b0F at a 40 \u00b0F evaporator on our chart', 'about 0.2 \u00b0F')])}
<p>Composition, GWP and glide are from the Chemours Opteon XL41 product information sheet; R-410A GWP is the IPCC AR4 value listed by the UNEP Ozone Secretariat.</p>
<h2>Pressures: close to R-410A, but not the same</h2>
<p>This is the part that trips people up. At the same saturation temperature R-454B runs a few psi <em>lower</em> than R-410A. At a 40 \u00b0F evaporator R-410A sits at about {ps(p410_40)} psig, while R-454B shows {ps(d40)} psig at the dew point. At a 100 \u00b0F condensing temperature R-410A is about {ps(p410_100)} psig and R-454B about {ps(b100)} psig at the bubble point.</p>
{table(['Saturation temp', 'R-410A (psig)', 'R-454B dew (psig)', 'R-454B bubble (psig)'], rows, caption='Values from the verified PT data on this site')}
<p>Turn it around and the risk is clear. If an R-454B system shows 118 psig on the suction and you read it on an R-410A scale, you will call it 40 \u00b0F. On the R-454B dew column 118 psig is about {t118d:.0f} \u00b0F, so the superheat you calculate is several degrees too high and you may add refrigerant to a system that does not need it. On the high side, 300 psig is about {t300b:.0f} \u00b0F bubble for R-454B versus {t300_410:.0f} \u00b0F for R-410A, which shifts subcooling by roughly the same amount. Always set the digital manifold to R-454B or use the {L('/r454b-pt-chart/', 'R-454B PT chart')}.</p>
<h2>Glide: small, but use the right column</h2>
<p>R-454B is a zeotropic blend. At a 40 \u00b0F evaporator the dew and bubble pressures differ by about {abs(d40 - b40):.1f} psi, a glide of roughly {g454:.1f} \u00b0F on our chart data. That is small compared with R-407C, but large enough that you should use the dew column for superheat and the bubble column for subcooling. Our {L('/superheat-calculator/', 'superheat')} and {L('/subcooling-calculator/', 'subcooling')} calculators pick the right column automatically. For background see {L('/blog/refrigerant-temperature-glide/', 'temperature glide explained')}.</p>
<h2>Tools: the core four</h2>
<p>JB Industries and Carrier\u2019s A2L tools catalog both list the same four tools that touch the refrigerant circuit and must be A2L-compatible: <b>manifolds and gauges</b> (with R-454B scales or updated refrigerant tables), <b>vacuum pumps</b> (non-sparking), <b>recovery machines</b> (non-sparking) and <b>electronic leak detectors</b> (sealed so they cannot spark). Tools that never touch the refrigerant usually carry over. Details are in our guide to {L('/blog/a2l-tools-leak-detectors-recovery-machines/', 'A2L tools')}.</p>
<h2>Cylinders and hoses</h2>
<ul><li>A2L recovery and refrigerant cylinders have a <b>red band</b> or red top, a <b>pressure relief valve</b> instead of a rupture disc, and <b>left-hand (reverse) threads</b>.</li>
<li>You need a reverse-thread adapter to connect standard hoses to them.</li>
<li>Recover R-454B only into a cylinder marked for it; never mix it with R-410A, even though the pressures look similar.</li>
<li>Separate hoses (or careful purging) avoid cross-contamination between R-410A and R-454B systems.</li></ul>
<h2>Charging an R-454B system step by step</h2>
<ol><li>Read the outdoor unit rating plate and installation manual. They give the factory charge, the line-set adjustment and the target subcooling.</li>
<li>Remove ignition sources from the work area and ventilate it.</li>
<li>Evacuate with an A2L-rated pump and confirm the vacuum with a micron gauge.</li>
<li>Weigh in the charge as a liquid (it is a blend, so liquid charging keeps the composition right).</li>
<li>Run the system at least 15 minutes, then check subcooling against the rating plate (most R-454B splits use a TXV or EEV) and confirm superheat is reasonable.</li>
<li>Adjust in small amounts, letting the system settle between changes.</li></ol>
<h2>Refrigerant detection systems</h2>
<p>Many R-454B indoor units include a refrigerant detection system (RDS): a sensor that, above a set concentration, turns on the indoor blower to dilute a leak and locks out the compressor or heat. UL 60335-2-40 requires these on systems whose charge exceeds a limit tied to the refrigerant\u2019s flammability. Wire and test the sensor exactly as the installation instructions say; a disconnected sensor can leave the system in a lockout or without its leak protection.</p>
<h2>What does not change</h2>
<p>Airflow first, clean coils, correct line-set sizing, nitrogen while brazing on an open and recovered system, triple-checking the rating plate: good R-410A habits carry straight over. Compare the two refrigerants side by side on our {L('/r454b-vs-r410a/', 'R-454B vs R-410A')} page.</p>
{sources([('https://www.epa.gov/climate-hfcs-reduction/technology-transitions-hfc-restrictions-sector', 'US EPA: Technology Transitions HFC restrictions by sector'),
          ('https://www.epa.gov/system/files/documents/2026-05/fact-sheet-san-12166-technology-transitions-frm.pdf', 'US EPA fact sheet: Technology Transitions final rule, May 2026'),
          ('https://www.chemours.com/en/-/media/files/opteon/opteon-xl41-product-information.pdf', 'Chemours: Opteon XL41 (R-454B) product information'),
          ('https://www.jbind.com/a2l-ready-tools/', 'JB Industries: A2L ready tools'),
          ('https://www.shareddocs.com/hvac/docs/1006/Public/06/570-178.pdf', 'Carrier Replacement Components: 2025 A2L (R-454B & R-32) compatible tools')])}'''

    # ---------------- A2L tools ----------------
    b['a2l-tools-leak-detectors-recovery-machines'] = f'''
<p class="lead">A2L refrigerants such as R-454B and R-32 are classed as mildly flammable. They need a strong ignition source and a high concentration to burn, but that is enough to change which tools you can put on the system. The good news: you do not need a whole new truck. Only the tools that touch the refrigerant circuit, or that could be an ignition source in a leak, need attention.</p>
<h2>What \u201cmildly flammable\u201d means for your tools</h2>
<p>ASHRAE Standard 34 puts refrigerants with low flammability and a low burning velocity in class 2L. Carrier\u2019s A2L tools guide sums up the practical side: a direct flame and a high refrigerant concentration are needed to ignite it, a flame is unlikely to sustain itself, and its spread rate is slower than walking speed. The risk comes from tools with brushes, relays and switches that can spark inside a cloud of leaked refrigerant. That is why the rule of thumb from distributors and tool makers is: tools that touch the refrigerant circuit must be non-sparking and rated or listed for A2L use.</p>
<h2>The four tools that change</h2>
{table(['Tool', 'What changes for A2L', 'Can it still be used on R-410A?'], [
 ('Recovery machine', 'Non-sparking (brushless) motor and switches; listed for A2L. UL 1963 covers flammable-refrigerant recovery equipment in its Supplement SB.', 'Yes, if it is listed for both; purge between refrigerants.'),
 ('Vacuum pump', 'Non-sparking motor (typically brushless DC).', 'Yes.'),
 ('Electronic leak detector', 'Sealed so the sensor and electronics cannot ignite a leak; must detect HFO/A2L blends.', 'Yes, most A2L detectors also sense HFCs.'),
 ('Manifold and gauges', 'Saturation scales for R-454B and R-32 (analog) or updated refrigerant tables (digital).', 'Yes; separate hoses are recommended to avoid cross-contamination.')])}
<h2>Recovery machines</h2>
<p>A standard recovery machine with a brushed motor or an open pressure switch can spark. A2L-rated machines use brushless motors and sealed electrical components. Look for a listing that names A2L or flammable refrigerants; UL 1963, the safety standard for recovery and recycling equipment, covers equipment for flammable refrigerants when it is investigated to its Supplement SB. EPA also requires recovery equipment used on stationary systems to be certified (normally to AHRI 740). Many current machines handle both A1 and A2L refrigerants and have a purge or self-clear mode so you do not carry R-410A into an R-454B system or the other way round.</p>
<h2>Leak detectors</h2>
<p>Use the electronic detector to find the area of the leak, then confirm the exact spot with bubble solution, which has no spark risk at all. Electronic \u201csniffers\u201d for A2L work should be fully sealed. Check that the detector is specified for HFO blends; some older heated-diode sensors were designed around HFCs and may read R-454B or R-32 poorly. Several manufacturers list compliance with EN 14624 or SAE J2791/J2913 sensitivity tests on A2L-capable models.</p>
<h2>Vacuum pumps and micron gauges</h2>
<p>Evacuation itself does not change: pull the system down and prove it with a micron gauge, because a compound gauge cannot read at micron levels. The pump must be non-sparking, since at the start of evacuation it may move residual refrigerant through its motor area. JB Industries recommends a triple evacuation on A2L systems.</p>
<h2>Cylinders, adapters and hoses</h2>
<ul><li><b>Red band:</b> A2L refrigerant and recovery cylinders carry a red band or red top and warning labels.</li>
<li><b>Relief valve:</b> they use a pressure relief valve instead of a rupture disc.</li>
<li><b>Left-hand threads:</b> the valve outlet is reverse-threaded, so you need a reverse-thread adapter for your hoses.</li>
<li><b>One refrigerant per cylinder:</b> an R-454B or R-32 recovery cylinder is for that refrigerant only; R-410A still needs its own.</li></ul>
<h2>Tools that usually do not change</h2>
<p>Scales, temperature clamps, psychrometers, wireless probes that never contact refrigerant, tubing cutters, flaring and swaging tools all carry over. Carrier\u2019s list adds one item many techs had not carried before: a multipurpose fire extinguisher on the truck. Press-fit and mechanical fittings are an option where brazing is impractical, but brazing on an evacuated, recovered system purged with nitrogen is still normal practice.</p>
<h2>A checklist before your first A2L call</h2>
<ol><li>Recovery machine listed for A2L, and a red-band recovery cylinder for each A2L refrigerant you service.</li>
<li>Reverse-thread adapters for cylinders.</li>
<li>Sealed, A2L-capable electronic leak detector plus bubble solution.</li>
<li>Non-sparking vacuum pump and a micron gauge.</li>
<li>Digital manifold updated with R-454B and R-32, or analog gauges with those scales.</li>
<li>A fire extinguisher, ventilation plan and the manufacturer\u2019s A2L installation and service instructions.</li></ol>
<p>Pressures and saturation temperatures are in our {L('/r454b-pt-chart/', 'R-454B')} and {L('/r32-pt-chart/', 'R-32')} PT charts; charging steps are in {L('/blog/r454b-service-basics/', 'R-454B service basics')}.</p>
{sources([('https://www.shareddocs.com/hvac/docs/1006/Public/06/570-178.pdf', 'Carrier Replacement Components: 2025 A2L (R-454B & R-32) compatible tools'),
          ('https://www.jbind.com/a2l-ready-tools/', 'JB Industries: A2L ready tools'),
          ('https://law.resource.org/pub/us/cfr/ibr/inc/ul/ul.s1963.4.2025.pdf', 'UL 1963, Refrigerant Recovery/Recycling Equipment (scope, Supplement SB)'),
          ('https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-82/subpart-F/section-82.158', '40 CFR 82.158: standards for recovery and recycling equipment'),
          ('https://www.hilmor.com/hilmor-a2l-tools', 'hilmor: A2L tools (leak detector certifications)'),
          ('https://www.chadwellsupply.com/resources/product-knowledge/pk-a2l/a2l-refrigerant-tools-and-storage', 'Chadwell Supply: A2L refrigerant tools and storage'),
          ('https://www.chemours.com/en/-/media/files/opteon/opteon-xl41-product-information.pdf', 'Chemours: Opteon XL41 product information')])}'''

    # ---------------- Glide ----------------
    blends = [r for r in REFS if r['blend']]
    grows = []
    for r in sorted(blends, key=lambda r: -(glide(r, 40) or 0)):
        g = glide(r, 40)
        if g is None:
            continue
        cls = 'High' if g >= 5 else ('Low' if g >= 1 else 'Near zero')
        grows.append((L(f"/{r['slug']}-pt-chart/", r['name']), r['safety'], f'{g:.1f}', cls))
    r407c = BY['r407c']
    p40d = pf(r407c, 40, 1)
    tb_at = tp(r407c, p40d, 0)
    s_dew = 52 - 40
    s_bub = 52 - tb_at
    p_liq = pf(r407c, 110, 0)
    td_liq = tp(r407c, p_liq, 1)
    b['refrigerant-temperature-glide'] = f'''
<p class="lead">Open a PT chart for R-407C or R-448A and you will see two pressure columns for every temperature. That is temperature glide: a blend does not boil at one temperature. Understanding it is the difference between a correct charge and one that is several degrees off.</p>
<h2>What glide is</h2>
<p>A pure refrigerant such as R-32 or R-134a boils and condenses at a single temperature for a given pressure. A <b>zeotropic blend</b> (the 400-series refrigerants) is a mix of refrigerants with different boiling points. At constant pressure the more volatile component boils off first, the remaining liquid gets richer in the less volatile one, and its boiling temperature rises. The blend starts to boil at the <b>bubble point</b> and finishes at the <b>dew point</b>. The difference between them is the <b>temperature glide</b>. Azeotropic blends (500-series, such as R-507A and R-513A) behave like a single refrigerant and have essentially no glide.</p>
<h2>Glide of common blends</h2>
<p>We computed the glide at a 40 \u00b0F bubble temperature from the PT data on this site (each chart is verified against published manufacturer or NIST data). National Refrigerants describes blends with a glide under about 5 \u00b0F as near-azeotropes, where glide and fractionation have little effect in practice.</p>
{table(['Blend', 'Safety class', 'Glide at 40 \u00b0F (\u00b0F)', 'Glide'], grows, caption='Computed from this site\u2019s verified PT data')}
<p>Notice the split: R-410A, R-404A, R-507A and R-513A act like single refrigerants, while most R-22 and R-404A replacements (R-407C, R-427A, R-438A, R-448A, R-449A, R-407A/F) glide 7\u201311 \u00b0F, and the low-GWP refrigeration blends R-454A and R-455A glide even more.</p>
<h2>Which column to use</h2>
<ul><li><b>Superheat</b> starts where the last liquid boils off, so use the <b>dew</b> temperature at suction pressure.</li>
<li><b>Subcooling</b> starts where the vapor has fully condensed, so use the <b>bubble</b> temperature at liquid pressure.</li></ul>
<p>If you use a digital manifold, check that it is set to the exact blend on the rating plate. R-407A, R-407C and R-407F share the same three components in different proportions, and their charts show different pressures at the same temperature, so a near miss on the refrigerant setting gives the wrong saturation temperatures.</p>
<p>Sporlan, Chemours and National Refrigerants all give the same rule. Our {L('/superheat-calculator/', 'superheat')} and {L('/subcooling-calculator/', 'subcooling')} calculators apply it automatically.</p>
<h2>Worked example: R-407C</h2>
<p>Suction pressure {ps(p40d)} psig. On the {L('/r407c-pt-chart/', 'R-407C PT chart')} that is 40 \u00b0F dew, but only about {tb_at:.0f} \u00b0F bubble. With a 52 \u00b0F suction line, superheat is <b>{s_dew:.0f} \u00b0F</b> using the dew column. Using the bubble column by mistake gives {s_bub:.0f} \u00b0F, which looks like a starving evaporator and could lead you to overcharge.</p>
<p>On the liquid side at {ps(p_liq)} psig, the bubble temperature is 110 \u00b0F and the dew temperature about {td_liq:.0f} \u00b0F. With a 100 \u00b0F liquid line, subcooling is 10 \u00b0F on the bubble column; the dew column would claim about {td_liq - 100:.0f} \u00b0F.</p>
<h2>Glide in the coil</h2>
<p>In a real evaporator the refrigerant enters as a mix of liquid and vapor, so the coil inlet is already part way along the glide; the coil temperature rises from inlet to outlet even with no pressure drop. Some compressor makers rate blends at a <b>mid-point</b> (average) temperature rather than the dew point, which is why catalog evaporating temperatures for high-glide blends can look a few degrees different from your gauge. For field charging, stick to dew for superheat and bubble for subcooling.</p>
<h2>Fractionation and charging</h2>
<p>Because the vapor and liquid of a zeotropic blend have different compositions, taking vapor out of a cylinder changes what is left in it. Charge blends as <b>liquid</b> from the cylinder (meter it into the suction side slowly so it flashes before the compressor).</p>
<h2>Retrofits</h2>
<p>When an R-22 system is retrofitted to a high-glide blend such as R-407C or R-438A, the TXV may need adjustment, and the pressures you are used to no longer mean the same thing. Compare the two directly on {L('/r407c-vs-r22/', 'R-407C vs R-22')} and {L('/r438a-vs-r422d/', 'R-438A vs R-422D')}. For the basics of reading two columns, see {L('/blog/how-to-read-a-pt-chart/', 'how to read a PT chart')}.</p>
{sources([('https://www.parker.com/content/dam/Parker-com/Literature/Sporlan/Sporlan-pdf-files/Sporlan-pdf-Educational/Form-5-492-Refrig-Blends.pdf', 'Sporlan (Parker) Form 5-492: System considerations for refrigerant blends'),
          ('https://refrigerants.com/resources/terminology', 'National Refrigerants: terminology (near azeotrope, temperature glide)'),
          ('https://refrigerants.com/resources/faqs/', 'National Refrigerants: FAQs (bubble/dew point, fractionation)'),
          ('https://www.freon.com/en/-/media/files/freon/freon-mo99-faq.pdf', 'Chemours: Freon MO99 FAQ (glide, liquid charging, dew/bubble)'),
          ('https://www.bitzer.de/shared_media/html/a-500-501/en-GB/681376523.html', 'Bitzer: general characteristics of zeotropic blends (mean temperatures)'),
          ('https://assets.danfoss.com/documents/59790/AP136386417202en-000201.pdf', 'Danfoss: refrigerants application guide (mid-point vs dew point)')])}'''
    return b


# FAQs for every post (launch posts included). Answers restate the cited content of the post.
FAQS = {
 'how-to-read-a-pt-chart': [
  ('Is a PT chart in psig or psia?', 'Field PT charts, including ours, are in psig (gauge pressure). Absolute pressure is psig plus about 14.7 psi at sea level. Below 0 psig the chart shows inches of mercury vacuum.'),
  ('Which column do I use for superheat on a blend?', 'The dew column. Superheat is measured from the point where the last liquid has boiled off, which is the dew point.'),
  ('Which column do I use for subcooling on a blend?', 'The bubble column. Subcooling is measured from the point where the vapor has fully condensed, which is the bubble point.'),
  ('Can I judge the charge from standing pressure?', 'No. With the system off, pressure only tells you refrigerant is present and roughly the ambient temperature. Judge charge with the system running, using superheat or subcooling.'),
  ('Why does my gauge read higher than the chart for a system at rest?', 'If the system has equalized at a known ambient temperature and the pressure is clearly above the chart value, non-condensables such as air, or the wrong refrigerant, are possible causes.')],
 'superheat-vs-subcooling': [
  ('Do I charge a TXV system by superheat or subcooling?', 'By subcooling. The TXV holds superheat roughly constant, so extra refrigerant shows up as subcooling. Use the target on the rating plate or in the installation manual.'),
  ('Do I charge a piston (fixed orifice) system by superheat or subcooling?', 'By superheat, compared with the manufacturer\u2019s target superheat table based on indoor wet bulb and outdoor dry bulb.'),
  ('What does high superheat and low subcooling usually mean?', 'Most often an undercharge or a leak. Confirm with airflow checks and the manufacturer\u2019s chart before adding refrigerant.'),
  ('How long should the system run before I take readings?', 'At least 15 minutes, ideally in a stable test mode, so pressures and temperatures settle.'),
  ('Does airflow affect superheat?', 'Yes. Low indoor airflow lowers the load on the evaporator and lowers superheat, which can look like an overcharge. Fix airflow before touching the charge.')],
 'conduit-fill-40-percent-rule': [
  ('What is the maximum conduit fill for three or more wires?', '40% of the raceway\u2019s internal area, from NEC Chapter 9 Table 1. One conductor may use 53% and two conductors 31%.'),
  ('Do ground wires count in conduit fill?', 'Yes. Equipment grounding and bonding conductors, insulated or bare, are counted (Chapter 9, Note 3).'),
  ('Can I round up when the calculation gives a fraction?', 'Only when all conductors are the same size and the decimal is 0.8 or more (Chapter 9, Note 7).'),
  ('What fill is allowed in a short nipple?', 'A raceway section 24 inches or shorter between enclosures may be filled to 60% (Chapter 9, Note 4).'),
  ('Is conduit fill the same for EMT and PVC?', 'No. The percentage is the same, but internal areas differ by raceway type in Chapter 9 Table 4, so the same trade size holds a different number of wires.')],
 'voltage-drop-3-percent-rule': [
  ('Is the 3% voltage drop rule required by the NEC?', 'For general branch circuits and feeders it is an informational note, a recommendation rather than a requirement, unless your jurisdiction makes it mandatory. Some specific articles, such as fire pumps, set enforceable limits.'),
  ('What is the combined voltage drop recommendation?', 'The informational notes recommend no more than 3% on a branch circuit or feeder and no more than 5% for the feeder and branch circuit together.'),
  ('Do I use the breaker size or the load current?', 'Use the actual load current for a realistic answer. Using the breaker rating gives a conservative worst case.'),
  ('If I upsize the wire for voltage drop, do I upsize the ground too?', 'Yes. NEC 250.122(B) requires the equipment grounding conductor to be increased in proportion to the increase in the ungrounded conductors.'),
  ('What resistance values should I use?', 'NEC Chapter 9 Table 8 gives DC resistance per 1,000 ft. For large AC conductors in steel raceway, Table 9 impedance values are more accurate.')],
 'gas-pipe-sizing-longest-length-method': [
  ('What is the longest length method?', 'You measure from the point of delivery to the most remote appliance and use that one length row of the IFGC table for every section of the system, each sized for the load it carries.'),
  ('How do I convert Btu/h to CFH for natural gas?', 'Divide the Btu/h load by the heating value of the gas. 1,000 Btu per cubic foot is a common assumption; your utility can give the actual value.'),
  ('What if my length falls between two table rows?', 'Use the next longer row. If the load falls exactly on a table value, that pipe size is acceptable.'),
  ('Are propane tables in CFH?', 'No. The IFGC propane tables list capacity in thousands of Btu per hour (MBH), so you can use the appliance input directly.'),
  ('Do fittings add length?', 'Yes, fittings add equivalent length (IFGC Appendix A). CSST manufacturer tables typically already include an allowance for bends and fittings.')],
 'how-to-tell-water-heater-age': [
  ('Where is the serial number on a water heater?', 'On the rating plate sticker on the front of the tank jacket, usually above the gas valve or the upper element cover. Do not confuse it with the model number.'),
  ('How do I read a Rheem water heater serial number?', 'Rheem, Ruud and Richmond serials start with the month and year of manufacture: 1209 means December 2009.'),
  ('How do I read a Bradford White serial number?', 'The first letter is the year on a 20-year cycle and the second letter is the month. Because the letters repeat, H can mean 1991 or 2011.'),
  ('How long does a tank water heater last?', 'The US Department of Energy estimates 10 to 15 years for storage water heaters.'),
  ('What if the serial number does not decode?', 'Use the manufacturer\u2019s warranty lookup with the full serial number or call their support line. Store brands are built by major manufacturers and usually follow that maker\u2019s format.')],
 'r454b-service-basics': [
  ('Can I use my R-410A gauges on R-454B?', 'The pressures are in the same range, but the saturation scales differ. Use a digital manifold set to R-454B or analog gauges with an R-454B scale, and keep separate hoses or purge them to avoid cross-contamination.'),
  ('Is R-454B a drop-in for R-410A?', 'No. R-454B is used in equipment designed and listed for it as an A2L refrigerant. Do not add it to an R-410A system or mix the two.'),
  ('Does R-454B use the same oil as R-410A?', 'Yes, both use POE oil.'),
  ('Is R-454B charged as a liquid?', 'Yes. It is a zeotropic blend, so it is charged as liquid from the cylinder to keep its composition correct.'),
  ('Can R-410A systems still be installed?', 'EPA\u2019s May 2026 final rule removed the January 1, 2026 installation deadline for residential and light commercial systems built or imported before January 1, 2025, so that inventory can be installed until it runs out. New equipment manufactured from 2025 must be below 700 GWP.')],
 'a2l-tools-leak-detectors-recovery-machines': [
  ('Do I need a new recovery machine for R-454B and R-32?', 'You need one that is non-sparking and listed for A2L refrigerants. Many current machines handle both A1 and A2L refrigerants with a purge mode between them.'),
  ('Can I use my old leak detector on A2L refrigerants?', 'Only if it is sealed against sparking and rated to detect HFO and A2L blends. Bubble solution is always safe for pinpointing a leak.'),
  ('Why do A2L cylinders have left-hand threads?', 'The reverse threads, red band and relief valve make A2L cylinders hard to confuse with A1 refrigerant cylinders. A reverse-thread adapter connects your hoses.'),
  ('Do I need a new vacuum pump?', 'You need a non-sparking pump, typically with a brushless DC motor. Many newer pumps already qualify; check the manufacturer\u2019s A2L listing.'),
  ('Which tools do not need to change?', 'Tools that never touch the refrigerant or create sparks, such as scales, clamps, psychrometers, cutters and flaring tools, usually carry over.')],
 'refrigerant-temperature-glide': [
  ('What is temperature glide?', 'The difference between the bubble point and the dew point of a zeotropic blend at the same pressure. It happens because the blend\u2019s components boil at different temperatures.'),
  ('Which refrigerants have glide?', 'Zeotropic 400-series blends. R-407C, R-448A, R-449A and R-427A glide around 10 \u00b0F; R-410A and R-404A glide less than 1 \u00b0F. Pure refrigerants and 500-series azeotropes have essentially none.'),
  ('Do I use dew or bubble for superheat?', 'Dew for superheat, bubble for subcooling.'),
  ('Why must blends be charged as liquid?', 'The vapor in the cylinder has a different composition from the liquid. Charging vapor changes the composition in the system and in the cylinder; this is called fractionation.'),
  ('What is a near-azeotrope?', 'A blend with a small glide, under about 5 \u00b0F, where glide and fractionation have little practical effect, such as R-410A and R-404A.')],
}


# Extra sections for the launch posts (to bring them to 600+ useful words).
EXPAND = {
 'superheat-vs-subcooling': f'''<h2>Worked example: piston system</h2>
<p>An R-410A split with a fixed orifice. Indoor return wet bulb 63 \u00b0F, outdoor air entering the condenser 85 \u00b0F. The {L('/target-superheat-calculator/', 'target superheat calculator')} gives (3 \u00d7 63 \u2212 80 \u2212 85) \u00f7 2 = 12 \u00b0F. Suction pressure converts to 40 \u00b0F saturated, and the suction line at the outdoor unit reads 58 \u00b0F: 18 \u00b0F superheat, 6 \u00b0F above target. With airflow and coils confirmed, that points to a low charge; add refrigerant slowly and recheck after the system settles.</p>''',
 'conduit-fill-40-percent-rule': f'''<h2>Step by step for any job</h2>
<ol><li>List every conductor in the raceway, including grounds, with its size and insulation type.</li>
<li>Look up each conductor\u2019s area in Chapter 9 Table 5 (THHN/THWN-2, XHHW and so on all differ).</li>
<li>Add the areas.</li>
<li>Pick the raceway type and look up the 40% column of Table 4 for each trade size.</li>
<li>Choose the smallest size whose 40% area is larger than your total, then consider one size up for long or bendy pulls.</li></ol>
<h2>Example with XHHW</h2>
<p>Insulation type changes the answer. XHHW has a thinner jacket than THW, so the same copper takes less room. Always use the Table 5 row for the insulation actually on the reel, not the one you assume.</p>''',
 'voltage-drop-3-percent-rule': f'''<h2>Worked example: three-phase</h2>
<p>A 208 V three-phase rooftop unit drawing 40 A, 150 ft from the panel, on 8 AWG copper (0.778 \u03a9/kft from Table 8): 1.732 \u00d7 150 \u00d7 0.778 \u00d7 40 \u00f7 1000 = 8.1 V, or 3.9% of 208 V. On 6 AWG (0.491 \u03a9/kft) it is 5.1 V, 2.5%. At 208 V a few volts matter more than at 480 V, so lower-voltage systems are where voltage drop most often drives the wire size.</p>
<h2>Why it matters for equipment</h2>
<p>Motors and compressors draw more current when the voltage at their terminals is low, which raises their temperature and shortens their life, and electronic controls may drop out. Many equipment installation manuals give an allowed voltage range at the unit; check it on long runs.</p>''',
 'gas-pipe-sizing-longest-length-method': f'''<h2>Propane version of the same house</h2>
<p>For propane on the IFGC tables you do not convert to CFH: the tables are in thousands of Btu/h. The same 207,000 Btu/h house is 207 MBH. Use the propane table that matches your system (for example the 11 in. w.c. low-pressure table downstream of the second-stage regulator) and the same longest-length row. Our {L('/propane-gas-pipe-sizing-chart/', 'propane pipe sizing chart')} has those tables.</p>
<h2>Common mistakes</h2>
<ul><li>Measuring only to the nearest appliance instead of the most remote one.</li><li>Using a table for a different gas, pressure or pressure drop.</li><li>Forgetting future appliances such as a generator or pool heater.</li></ul>''',
 'how-to-tell-water-heater-age': f'''<h2>Worked examples</h2>
{table(['Serial starts with', 'Brand', 'Decodes to'], [('HK', 'Bradford White', 'October 2011 (or 1991)'), ('1209', 'Rheem / Ruud', 'December 2009'), ('2037', 'A.O. Smith / State', 'Week 37 of 2020'), ('1924', 'American', 'Week 24 of 2019')])}
<p>Type the serial into the decoder for that brand to check the full format and any exceptions; see all brands on the {L('/water-heater-age/', 'water heater age')} page.</p>
<h2>Signs it may be near the end</h2>
<ul><li>Rust-colored hot water or rust at the base of the tank.</li><li>Moisture or drips around the tank.</li><li>Rumbling or popping from sediment build-up.</li><li>An age at or beyond the 10\u201315 year range DOE gives.</li></ul>
<p>Once you know the date, write it on the jacket with a marker so the next person does not have to decode the serial again.</p>''',
}

# Related-guide links injected on tool pages (internal linking, SEO).
RELATED_GUIDES = {
 '/r454b-pt-chart/': [('r454b-service-basics', 'R-454B service basics for R-410A techs'), ('refrigerant-temperature-glide', 'Temperature glide explained')],
 '/r454b-vs-r410a/': [('r454b-service-basics', 'R-454B service basics for R-410A techs'), ('a2l-tools-leak-detectors-recovery-machines', 'A2L tools: what changes')],
 '/r32-pt-chart/': [('a2l-tools-leak-detectors-recovery-machines', 'A2L tools: leak detectors and recovery machines')],
 '/r32-vs-r454b/': [('a2l-tools-leak-detectors-recovery-machines', 'A2L tools: what changes'), ('r454b-service-basics', 'R-454B service basics')],
 '/r410a-pt-chart/': [('r454b-service-basics', 'Moving from R-410A to R-454B'), ('how-to-read-a-pt-chart', 'How to read a PT chart')],
 '/r407c-pt-chart/': [('refrigerant-temperature-glide', 'Temperature glide: why R-407C has two columns')],
 '/r448a-pt-chart/': [('refrigerant-temperature-glide', 'Temperature glide: why R-448A has two columns')],
 '/r449a-pt-chart/': [('refrigerant-temperature-glide', 'Temperature glide explained')],
 '/pt-chart/': [('how-to-read-a-pt-chart', 'How to read a PT chart'), ('refrigerant-temperature-glide', 'Temperature glide explained')],
 '/superheat-calculator/': [('superheat-vs-subcooling', 'Superheat vs subcooling'), ('refrigerant-temperature-glide', 'Why blends use the dew column')],
 '/subcooling-calculator/': [('superheat-vs-subcooling', 'Superheat vs subcooling'), ('refrigerant-temperature-glide', 'Why blends use the bubble column')],
 '/conduit-fill-calculator/': [('conduit-fill-40-percent-rule', 'The NEC 40% rule explained')],
 '/emt-conduit-fill-chart/': [('conduit-fill-40-percent-rule', 'The NEC 40% rule explained')],
 '/voltage-drop-calculator/': [('voltage-drop-3-percent-rule', 'Voltage drop and the 3% rule')],
 '/gas-pipe-sizing/': [('gas-pipe-sizing-longest-length-method', 'The longest length method, step by step')],
 '/natural-gas-pipe-sizing-chart/': [('gas-pipe-sizing-longest-length-method', 'How to size gas pipe')],
 '/water-heater-age/': [('how-to-tell-water-heater-age', 'How to tell the age of a water heater')],
 '/bradford-white-water-heater-age/': [('how-to-tell-water-heater-age', 'How to tell the age of a water heater')],
}


def related_html(path):
    items = RELATED_GUIDES.get(path)
    if not items:
        return ''
    return '<h2>Related guides</h2><ul>' + ''.join(f'<li>{L(f"/blog/{s}/", t)}</li>' for s, t in items) + '</ul>'


# ---- posts 10-12 (posts3.py) ----
import posts3 as _p3
NEW_POSTS.extend(_p3.NEW_POSTS)
FAQS.update(_p3.FAQS)
for _k, _v in _p3.RELATED_GUIDES.items():
    RELATED_GUIDES.setdefault(_k, []).extend(_v)
_orig_nb = new_bodies


def new_bodies():
    d = _orig_nb()
    d.update(_p3.bodies())
    return d

import posts4 as _p4
NEW_POSTS.extend(_p4.NEW_POSTS)
FAQS.update(_p4.FAQS)
for _k, _v in _p4.RELATED_GUIDES.items():
    RELATED_GUIDES.setdefault(_k, []).extend(_v)
_orig_nb2 = new_bodies


def new_bodies():
    d = _orig_nb2()
    d.update(_p4.bodies())
    return d


import posts5 as _p5
NEW_POSTS.extend(_p5.NEW_POSTS)
FAQS.update(_p5.FAQS)
for _k, _v in _p5.RELATED_GUIDES.items():
    RELATED_GUIDES.setdefault(_k, []).extend(_v)
_orig_nb3 = new_bodies


def new_bodies():
    d = _orig_nb3()
    d.update(_p5.bodies())
    return d

import posts6 as _p6
NEW_POSTS.extend(_p6.NEW_POSTS)
FAQS.update(_p6.FAQS)
for _k, _v in _p6.RELATED_GUIDES.items():
    RELATED_GUIDES.setdefault(_k, []).extend(_v)
_orig_nb4 = new_bodies


def new_bodies():
    d = _orig_nb4()
    d.update(_p6.bodies())
    return d

import posts7 as _p7
NEW_POSTS.extend(_p7.NEW_POSTS)
FAQS.update(_p7.FAQS)
for _k, _v in _p7.RELATED_GUIDES.items():
    RELATED_GUIDES.setdefault(_k, []).extend(_v)
_orig_nb5 = new_bodies


def new_bodies():
    d = _orig_nb5()
    d.update(_p7.bodies())
    return d

import posts8 as _p8
NEW_POSTS.extend(_p8.NEW_POSTS)
FAQS.update(_p8.FAQS)
for _k, _v in _p8.RELATED_GUIDES.items():
    RELATED_GUIDES.setdefault(_k, []).extend(_v)
_orig_nb6 = new_bodies


def new_bodies():
    d = _orig_nb6()
    d.update(_p8.bodies())
    return d
