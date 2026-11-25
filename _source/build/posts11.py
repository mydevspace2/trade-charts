"""Post 32 (run 2026-11-25)."""
import json, os
from core import table
from posts5 import L, sources

NEW_POSTS = [
 ('wire-size-for-60-amp-breaker', 'Wire Size for a 60 Amp Breaker: 4 AWG or 6 AWG Copper?',
  'What wire size does a 60 amp breaker need? 4 AWG copper in NM cable, 6 AWG only with 75 \u00b0C terminals, 3 or 4 AWG aluminum, plus ground size and voltage drop.', '2026-11-25'),
]
_E = json.load(open(os.path.join(os.path.dirname(__file__), 'data', 'electrical.json')))


def _vd(size, met, ft=100, amps=60, volts=240):
    r = _E['t8'][size][met]
    v = 2 * ft * amps * r / 1000
    return f'{v:.2f} V', f'{v / volts * 100:.2f} %'


def bodies():
    rows = []
    for lab, size, met in [('4 AWG copper', '4', 'cu'), ('6 AWG copper', '6', 'cu'), ('3 AWG aluminum', '3', 'al'), ('4 AWG aluminum', '4', 'al')]:
        v, p = _vd(size, met)
        rows.append((lab, v, p))
    amp = table(['Size', '60 \u00b0C column', '75 \u00b0C column'], [
        ('8 AWG copper', '40 A', '50 A'), ('6 AWG copper', '55 A', '65 A'), ('4 AWG copper', '70 A', '85 A'), ('3 AWG copper', '85 A', '100 A'),
        ('6 AWG aluminum', '40 A', '50 A'), ('4 AWG aluminum', '55 A', '65 A'), ('3 AWG aluminum', '65 A', '75 A')])
    pick = table(['Wiring', 'Copper', 'Aluminum'], [
        ('NM cable, or any 60 \u00b0C terminal', '4 AWG', '3 AWG'),
        ('Single conductors (THHN in conduit), every termination listed for 75 \u00b0C', '6 AWG', '4 AWG'),
        ('Equipment ground (Table 250.122, 60 A breaker)', '10 AWG', '8 AWG')])
    vd = table(['Size (100 ft one way, 60 A, 240 V)', 'Drop', 'Percent'], rows)
    return {'wire-size-for-60-amp-breaker': f'''
<p class="lead">The short answer: a 60 amp breaker takes 4 AWG copper (or 3 AWG aluminum) in NM cable or on 60 \u00b0C terminals. 6 AWG copper (4 AWG aluminum) is enough only when every termination is listed for 75 \u00b0C conductors. This guide shows where the split comes from.</p>
<h2>Why a 60 A circuit has two answers</h2>
<p>NEC 110.14(C) says a conductor may be used only at the temperature column of the lowest-rated part it connects to. For circuits of 100 A or less, you start in the 60 \u00b0C column unless the equipment is listed and identified for 75 \u00b0C. Table 310.16 around 60 A reads:</p>
{amp}
<p>6 AWG copper has only 55 A in the 60 \u00b0C column, which is below 60 A, so it works only in the 75 \u00b0C column (65 A). 4 AWG copper clears 60 A in both columns, so it needs no terminal check.</p>
<h2>Which size for which wiring method</h2>
{pick}
<p>The ground comes from NEC Table 250.122, which sizes the equipment grounding conductor from the breaker rating. A 60 A breaker is still in the row for devices up to 60 A. If you upsize the circuit wires for distance, the ground grows in proportion (250.122(B)).</p>
<h2>NM cable (Romex) on a 60 A breaker</h2>
<p>NM cable is held to the 60 \u00b0C column by NEC 334.80, so 6/3 NM (55 A) is too small for a 60 A breaker, and 4/3 NM cable is the fit. Single THHN conductors in conduit are the usual place where 6 AWG copper makes sense, after you read the breaker and lug labels.</p>
<h2>Does a 55 A rating mean I can use a 55 A breaker?</h2>
<p>NEC 240.4(B) allows rounding up to the next standard breaker size when the conductor ampacity does not match a standard rating, under conditions that include loads not over 800 A and no multi-outlet branch circuits. That is why some installers use 6 AWG copper at 60 A in the 60 \u00b0C column. Not every inspector or equipment label accepts it, so confirm locally before relying on it.</p>
<h2>Does distance change the wire size?</h2>
<p>Table 310.16 sizes a circuit for current, not length. On a long run, voltage drop matters. Using this site\u2019s conductor resistance table (NEC Chapter 9 Table 8, uncoated), the drop of a full 60 A load over 100 ft one way on a 240 V circuit is:</p>
{vd}
<p>The drop is 2 \u00d7 length \u00d7 current \u00d7 resistance per 1,000 ft, divided by 1,000. The NEC\u2019s informational notes suggest keeping drop at the farthest outlet under about 3 %. At 100 ft, 4 AWG copper stays near 1.5 %, while 6 AWG is about 2.5 %. For longer runs, go up a size and check the exact number with the {L('/voltage-drop-calculator/', 'voltage drop calculator')}.</p>
<h2>Worked example: a detached shop subpanel</h2>
<p>You are feeding a 60 A subpanel 70 ft away with THHN in conduit. With 75 \u00b0C lugs at both ends, 6 AWG copper (65 A) is allowed; if either lug is marked 60 \u00b0C, use 4 AWG. Many installers choose 4 AWG anyway for the lower drop and spare capacity. Add a 10 AWG copper ground, and a neutral if the shop has 120 V loads. Then size the pipe with the {L('/conduit-fill-calculator/', 'conduit fill calculator')}.</p>
<h2>Common 60 A uses</h2>
<ul>
<li>A 60 A subpanel feeder for a garage or workshop.</li>
<li>Electric furnace or heat strip circuits and larger hot tubs.</li>
<li>EV chargers, where the continuous load is limited to 80 % of the breaker (48 A on a 60 A breaker).</li>
</ul>
<p>Always read the equipment nameplate and your local code edition first. See the full {L('/wire-ampacity-chart/', 'wire ampacity chart')}, the pages for {L('/4-awg-wire-ampacity/', '4 AWG ampacity')} and {L('/6-awg-wire-ampacity/', '6 AWG ampacity')}, the guide to a {L('/blog/wire-size-for-50-amp-breaker/', '50 amp breaker')}, and the {L('/electrical/', 'electrical hub')}.</p>
<h2>Limits of this guide</h2>
<p>Values assume 30 \u00b0C ambient and no more than three current-carrying conductors. Hot attics, bundled cables or more wires in one conduit need derating under NEC 310.15. This is a reference, not a substitute for the code your inspector enforces.</p>
{sources([('https://wiresizes.com/guides/wire-size-for-60-amp', 'WireSizes: wire size for 60 amp breaker'), ('https://wireref.com/ampacity', 'WireRef: NEC Table 310.16 ampacity chart')])}
'''}

FAQS = {
 'wire-size-for-60-amp-breaker': [
  ('What size wire for a 60 amp breaker?', '4 AWG copper or 3 AWG aluminum in NM cable or on 60 \u00b0C terminals; 6 AWG copper or 4 AWG aluminum when every termination is rated 75 \u00b0C.'),
  ('Can I use 6 AWG on a 60 amp breaker?', 'Yes, as single conductors such as THHN in conduit when all terminals are listed for 75 \u00b0C (65 A). Not in NM cable, which is held to 55 A.'),
  ('What size ground wire for 60 amps?', '10 AWG copper or 8 AWG aluminum from NEC Table 250.122, larger if you upsize the circuit wires.'),
  ('What wire size for a 60 amp subpanel?', '4 AWG copper is the safe choice for most subpanels, with a 10 AWG ground, and one size up on long runs.'),
  ('How far can 4 AWG run on 60 amps?', 'About 100 ft one way gives roughly 1.5 % drop at full 60 A on 240 V; use the voltage drop calculator for longer runs.')],
}
RELATED_GUIDES = {
 '/wire-ampacity-chart/': [('wire-size-for-60-amp-breaker', 'Wire size for a 60 amp breaker')],
 '/6-awg-wire-ampacity/': [('wire-size-for-60-amp-breaker', 'Wire size for a 60 amp breaker')],
 '/4-awg-wire-ampacity/': [('wire-size-for-60-amp-breaker', 'Wire size for a 60 amp breaker')],
 '/voltage-drop-calculator/': [('wire-size-for-60-amp-breaker', 'Wire size for a 60 amp breaker')],
}
