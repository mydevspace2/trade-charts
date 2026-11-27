"""Post 34 (run 2026-11-27)."""
import json, os
from core import table
from posts5 import L, sources

NEW_POSTS = [
 ('wire-size-for-80-amp-breaker', 'Wire Size for an 80 Amp Breaker: 3 AWG Copper or 1 AWG Aluminum',
  'What wire size does an 80 amp breaker need? 3 AWG copper, 1 AWG aluminum on 60 \u00b0C terminals (2 AWG at 75 \u00b0C), 8 AWG copper ground, plus voltage drop.', '2026-11-27'),
]
_E = json.load(open(os.path.join(os.path.dirname(__file__), 'data', 'electrical.json')))


def _vd(size, met, ft=100, amps=80, volts=240):
    r = _E['t8'][size][met]
    v = 2 * ft * amps * r / 1000
    return f'{v:.2f} V', f'{v / volts * 100:.2f} %'


def bodies():
    rows = []
    for lab, size, met in [('3 AWG copper', '3', 'cu'), ('2 AWG copper', '2', 'cu'), ('1 AWG aluminum', '1', 'al'), ('2 AWG aluminum', '2', 'al')]:
        v, p = _vd(size, met)
        rows.append((lab, v, p))
    amp = table(['Size', '60 \u00b0C column', '75 \u00b0C column'], [
        ('4 AWG copper', '70 A', '85 A'), ('3 AWG copper', '85 A', '100 A'), ('2 AWG copper', '95 A', '115 A'),
        ('3 AWG aluminum', '65 A', '75 A'), ('2 AWG aluminum', '75 A', '90 A'), ('1 AWG aluminum', '85 A', '100 A')])
    pick = table(['Wiring', 'Copper', 'Aluminum'], [
        ('NM cable, or any 60 \u00b0C terminal', '3 AWG', '1 AWG'),
        ('Single conductors, every termination listed for 75 \u00b0C', '4 AWG', '2 AWG'),
        ('Equipment ground (Table 250.122, 80 A breaker)', '8 AWG', '6 AWG')])
    vd = table(['Size (100 ft one way, 80 A, 240 V)', 'Drop', 'Percent'], rows)
    return {'wire-size-for-80-amp-breaker': f'''
<p class="lead">The short answer: an 80 amp breaker takes 3 AWG copper on ordinary 60 \u00b0C terminals, which is rated 85 A. If every termination is listed for 75 \u00b0C, 4 AWG copper (85 A) also works. Aluminum needs 1 AWG at 60 \u00b0C or 2 AWG at 75 \u00b0C.</p>
<h2>Why 4 AWG copper is not enough on 60 \u00b0C terminals</h2>
<p>NEC 110.14(C) limits circuits of 100 A or less to the 60 \u00b0C column unless the equipment is listed for 75 \u00b0C. Table 310.16 around 80 A reads:</p>
{amp}
<p>4 AWG copper carries only 70 A in the 60 \u00b0C column, below the 80 A breaker. 3 AWG copper carries 85 A there, so it is the standard answer. With 75 \u00b0C terminals throughout, 4 AWG copper is rated 85 A, which also clears 80 A.</p>
<h2>Which size for which wiring method</h2>
{pick}
<p>Aluminum steps up one size from copper in each column. 2 AWG aluminum gives 75 A at 60 \u00b0C (too low) but 90 A at 75 \u00b0C. 1 AWG clears 80 A in both columns. The equipment ground comes from NEC Table 250.122; an 80 A breaker falls in the row for devices up to 100 A. Upsizing the circuit wires for distance also upsizes the ground (250.122(B)).</p>
<h2>Voltage drop on an 80 A run</h2>
<p>Using the resistance values behind our {L('/voltage-drop-calculator/', 'voltage drop calculator')}, single phase, 100 ft one way, full 80 A on 240 V:</p>
{vd}
<p>NEC suggests keeping feeder and branch drop under about 3 % each (informational notes, not a hard rule). Longer runs may call for one size up.</p>
<h2>Continuous loads on an 80 A breaker</h2>
<p>A standard breaker should carry a continuous load (3 hours or more) of no more than 80 % of its rating under NEC 210.20(A) and 215.3, which is 64 A on an 80 A breaker. An EV charger sized at 80 % of an 80 A circuit, for example, is a 64 A charger. Check the nameplate for the minimum circuit ampacity and maximum breaker.</p>
<h2>Is an 80 A breaker standard?</h2>
<p>Yes. NEC 240.6(A) lists 80 A among the standard ratings, between 70 and 90 A. It is common for subpanels, large heat pumps, electric furnaces with strip heat, and EV charging circuits.</p>
<h2>Example: 80 A subpanel, 90 ft, THHN in conduit</h2>
<p>With 75 \u00b0C lugs at both ends, 4 AWG copper (85 A at 75 \u00b0C) satisfies the breaker. If the lug rating is unknown or the lug says 60 \u00b0C, go to 3 AWG copper. Add an 8 AWG copper ground and a neutral, check the drop with the calculator, then size the pipe with the {L('/conduit-fill-calculator/', 'conduit fill calculator')}.</p>
<p>See the {L('/wire-ampacity-chart/', 'wire ampacity chart')}, the {L('/2-awg-wire-ampacity/', '2 AWG ampacity page')}, the guides for a {L('/blog/wire-size-for-70-amp-breaker/', '70 amp breaker')} and a {L('/blog/wire-size-for-60-amp-breaker/', '60 amp breaker')}, and the {L('/electrical/', 'electrical hub')}.</p>
<h2>Limits of this guide</h2>
<p>Values assume 30 \u00b0C ambient and no more than three current-carrying conductors. Hot attics or bundled cables need derating under NEC 310.15. This is a reference, not a substitute for the code your inspector enforces.</p>
{sources([('https://wireref.com/ampacity', 'WireRef: NEC Table 310.16 ampacity chart')])}
'''}

FAQS = {
 'wire-size-for-80-amp-breaker': [
  ('What size wire for an 80 amp breaker?', '3 AWG copper on 60 \u00b0C terminals (4 AWG copper if all terminals are rated 75 \u00b0C), or 1 AWG aluminum (2 AWG at 75 \u00b0C).'),
  ('Can I use 4 AWG on an 80 amp breaker?', 'Only with 75 \u00b0C-rated terminals throughout, where 4 AWG copper is rated 85 A. In the 60 \u00b0C column it is 70 A, too low.'),
  ('What size ground wire for an 80 amp breaker?', '8 AWG copper or 6 AWG aluminum from NEC Table 250.122, larger if you upsize the circuit wires.'),
  ('What wire size for an 80 amp subpanel?', '3 AWG copper with an 8 AWG ground is the safe default; 4 AWG works only with 75 \u00b0C terminations.'),
  ('How many amps can I draw continuously on an 80 amp breaker?', 'At most 64 A for loads running 3 hours or more, which is 80 % of the breaker rating.')],
}
RELATED_GUIDES = {
 '/wire-ampacity-chart/': [('wire-size-for-80-amp-breaker', 'Wire size for an 80 amp breaker')],
 '/2-awg-wire-ampacity/': [('wire-size-for-80-amp-breaker', 'Wire size for an 80 amp breaker')],
 '/voltage-drop-calculator/': [('wire-size-for-80-amp-breaker', 'Wire size for an 80 amp breaker')],
}
