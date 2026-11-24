"""Post 31 (run 2026-11-24)."""
import json, os
from core import table
from posts5 import L, sources

NEW_POSTS = [
 ('wire-size-for-50-amp-breaker', 'Wire Size for a 50 Amp Breaker: 6 AWG or 8 AWG Copper?',
  'What wire size does a 50 amp breaker need? 6 AWG copper in NM cable, 8 AWG only with 75 \u00b0C terminals, 4 or 6 AWG aluminum, plus ground size and voltage drop.', '2026-11-24'),
]
_E = json.load(open(os.path.join(os.path.dirname(__file__), 'data', 'electrical.json')))


def _vd(size, met, ft=100, amps=50, volts=240):
    r = _E['t8'][size][met]
    v = 2 * ft * amps * r / 1000
    return f'{v:.2f} V', f'{v / volts * 100:.2f} %'


def bodies():
    rows = []
    for lab, size, met in [('6 AWG copper', '6', 'cu'), ('8 AWG copper', '8', 'cu'), ('4 AWG aluminum', '4', 'al'), ('6 AWG aluminum', '6', 'al')]:
        v, p = _vd(size, met)
        rows.append((lab, v, p))
    amp = table(['Size', '60 \u00b0C column', '75 \u00b0C column'], [
        ('10 AWG copper', '30 A', '35 A'), ('8 AWG copper', '40 A', '50 A'), ('6 AWG copper', '55 A', '65 A'), ('4 AWG copper', '70 A', '85 A'),
        ('8 AWG aluminum', '35 A', '40 A'), ('6 AWG aluminum', '40 A', '50 A'), ('4 AWG aluminum', '55 A', '65 A')])
    pick = table(['Wiring', 'Copper', 'Aluminum'], [
        ('NM cable, or any 60 \u00b0C terminal', '6 AWG', '4 AWG'),
        ('Single conductors (THHN in conduit), every termination listed for 75 \u00b0C', '8 AWG', '6 AWG'),
        ('Equipment ground (Table 250.122, 50 A breaker)', '10 AWG', '8 AWG')])
    vd = table(['Size (100 ft one way, 50 A, 240 V)', 'Drop', 'Percent'], rows)
    return {'wire-size-for-50-amp-breaker': f'''
<p class="lead">The short answer: a 50 amp breaker takes 6 AWG copper (or 4 AWG aluminum) in almost every home wiring job. 8 AWG copper also works, but only when every termination on the circuit is rated for 75 \u00b0C conductors. Here is why the answer splits, and how to choose.</p>
<h2>Why there are two answers</h2>
<p>The NEC lets you use a conductor only at the temperature column of the lowest-rated part it connects to (NEC 110.14(C)). For circuits of 100 A or less, the starting point is the 60 \u00b0C column, unless the breaker, panel and devices are listed and identified for 75 \u00b0C conductors. Look at the values around 50 A in Table 310.16:</p>
{amp}
<p>8 AWG copper reaches 50 A only in the 75 \u00b0C column. 6 AWG copper clears 50 A in both columns (55 A and 65 A), so it needs no terminal check. That is why electricians default to 6 AWG for 50 A circuits.</p>
<h2>Which size for which wiring method</h2>
{pick}
<p>The ground size comes from NEC Table 250.122, which sizes the equipment grounding conductor from the breaker rating. A 50 A breaker falls in the row for breakers up to 60 A. If you upsize the circuit wires for distance, the ground must grow in proportion (250.122(B)).</p>
<h2>NM cable (Romex) on a 50 A breaker</h2>
<p>NM cable is held to the 60 \u00b0C ampacity by NEC 334.80, even though its conductors may be rated 90 \u00b0C. In the 60 \u00b0C column, 8 AWG copper carries 40 A, so a 50 A breaker needs 6/3 NM cable (55 A) for a range or RV outlet. Single THHN conductors in conduit are the only case where 8 AWG can make sense, and then only after you check the breaker and device labels.</p>
<h2>Can 10 AWG go on a 50 A breaker?</h2>
<p>Not on an ordinary circuit. NEC 240.4(D) limits overcurrent protection for 10 AWG copper to 30 A. Air conditioners and some motor circuits follow Article 440 instead, where the nameplate sets the breaker size, but that is a different rule for different equipment.</p>
<h2>Does distance change the wire size?</h2>
<p>Table 310.16 sizes a circuit for current, not length. On a long run the voltage drop matters. Using this site\u2019s conductor resistance table (NEC Chapter 9 Table 8, uncoated), the drop of a full 50 A load over 100 ft one way on a 240 V circuit works out as:</p>
{vd}
<p>The drop is 2 \u00d7 length \u00d7 current \u00d7 resistance per 1,000 ft, divided by 1,000. Drop falls in proportion to current, so a lighter load drops less. The NEC\u2019s informational notes suggest keeping the drop at the farthest outlet under about 3 %. At 100 ft, 6 AWG copper stays near 2 %, while 8 AWG is just over 3 %. For longer runs, go up a size and check the exact number with the {L('/voltage-drop-calculator/', 'voltage drop calculator')}.</p>
<h2>Worked example: a garage subpanel</h2>
<p>You are feeding a 50 A subpanel 80 ft away with THHN in conduit, and the breaker is marked for 60/75 \u00b0C wire. 8 AWG copper is allowed by the 75 \u00b0C column, but if the subpanel lugs are marked 60 \u00b0C only, you must use 6 AWG copper. Many installers choose 6 AWG anyway for the lower drop and spare capacity. Add a 10 AWG copper ground and a neutral if the subpanel serves 120 V loads. Then check the pipe: use the {L('/conduit-fill-calculator/', 'conduit fill calculator')} for the number of wires.</p>
<h2>Common 50 A uses</h2>
<ul>
<li>Electric range on a 14-50R or hardwired.</li>
<li>RV outlet (14-50R) or a 40 A EV charger, which needs a breaker at 125 % of its output.</li>
<li>Hot tub, welder or a 50 A feeder to a subpanel.</li>
</ul>
<p>Whatever the load, read the equipment nameplate and your local code edition first. See the full {L('/wire-ampacity-chart/', 'wire ampacity chart')}, the page for {L('/6-awg-wire-ampacity/', '6 AWG ampacity')} and {L('/8-awg-wire-ampacity/', '8 AWG ampacity')}, and the {L('/electrical/', 'electrical hub')}.</p>
<h2>Limits of this guide</h2>
<p>Values assume 30 \u00b0C ambient and no more than three current-carrying conductors. Hot attics, bundled cables or more wires in one conduit need derating under NEC 310.15. This is a reference, not a substitute for the code your inspector enforces.</p>
{sources([('https://wiresizes.com/guides/wire-size-for-50-amp', 'WireSizes: wire size for 50 amp breaker (NEC 2023 references)'), ('https://wireref.com/ampacity', 'WireRef: NEC Table 310.16 ampacity chart'), ('https://electricalflux.com/wire-switches/wire-size-50-amp-rv-plug-nema-14-50', 'ElectricalFlux: 50 A RV plug wire size')])}
'''}


FAQS = {
 'wire-size-for-50-amp-breaker': [
  ('What size wire for a 50 amp breaker?', '6 AWG copper or 4 AWG aluminum in NM cable or on 60 \u00b0C terminals. 8 AWG copper or 6 AWG aluminum works only if every termination is rated 75 \u00b0C.'),
  ('Can I use 8 AWG on a 50 amp breaker?', 'Yes, as single conductors such as THHN in conduit when all terminals are listed for 75 \u00b0C. Not in NM cable, which is held to 40 A.'),
  ('What size ground wire for 50 amps?', '10 AWG copper or 8 AWG aluminum from NEC Table 250.122, larger if you upsize the circuit wires.'),
  ('What wire size for a 50 amp RV outlet?', '6 AWG copper for a 14-50R on a 50 A breaker, going up a size on long runs to limit voltage drop.'),
  ('Can 10 AWG go on a 50 amp breaker?', 'Not on ordinary circuits. NEC 240.4(D) limits 10 AWG copper to a 30 A breaker.')],
}
RELATED_GUIDES = {
 '/wire-ampacity-chart/': [('wire-size-for-50-amp-breaker', 'Wire size for a 50 amp breaker')],
 '/6-awg-wire-ampacity/': [('wire-size-for-50-amp-breaker', 'Wire size for a 50 amp breaker')],
 '/8-awg-wire-ampacity/': [('wire-size-for-50-amp-breaker', 'Wire size for a 50 amp breaker')],
 '/voltage-drop-calculator/': [('wire-size-for-50-amp-breaker', 'Wire size for a 50 amp breaker')],
}
