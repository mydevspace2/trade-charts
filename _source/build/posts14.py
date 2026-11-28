"""Post 35 (run 2026-11-28)."""
import json, os
from core import table
from posts5 import L, sources

NEW_POSTS = [
 ('wire-size-for-90-amp-breaker', 'Wire Size for a 90 Amp Breaker: 2 AWG Copper or 1/0 AWG Aluminum',
  'What wire size does a 90 amp breaker need? 2 AWG copper, 1/0 AWG aluminum on 60 \u00b0C terminals (3 AWG Cu, 1 AWG Al at 75 \u00b0C), 8 AWG ground, plus voltage drop.', '2026-11-28'),
]
_E = json.load(open(os.path.join(os.path.dirname(__file__), 'data', 'electrical.json')))


def _vd(size, met, ft=100, amps=90, volts=240):
    r = _E['t8'][size][met]
    v = 2 * ft * amps * r / 1000
    return f'{v:.2f} V', f'{v / volts * 100:.2f} %'


def bodies():
    rows = []
    for lab, size, met in [('3 AWG copper', '3', 'cu'), ('2 AWG copper', '2', 'cu'), ('1 AWG aluminum', '1', 'al'), ('1/0 AWG aluminum', '1/0', 'al')]:
        v, p = _vd(size, met)
        rows.append((lab, v, p))
    amp = table(['Size', '60 \u00b0C column', '75 \u00b0C column'], [
        ('3 AWG copper', '85 A', '100 A'), ('2 AWG copper', '95 A', '115 A'), ('1 AWG copper', '110 A', '130 A'),
        ('1 AWG aluminum', '85 A', '100 A'), ('1/0 AWG aluminum', '100 A', '120 A')])
    pick = table(['Wiring', 'Copper', 'Aluminum'], [
        ('NM cable, or any 60 \u00b0C terminal', '2 AWG', '1/0 AWG'),
        ('Single conductors, every termination listed for 75 \u00b0C', '3 AWG', '1 AWG'),
        ('Equipment ground (Table 250.122, 90 A breaker)', '8 AWG', '6 AWG')])
    vd = table(['Size (100 ft one way, 90 A, 240 V)', 'Drop', 'Percent'], rows)
    return {'wire-size-for-90-amp-breaker': f'''
<p class="lead">The short answer: a 90 amp breaker takes 2 AWG copper on ordinary 60 \u00b0C terminals, which is rated 95 A. If every termination is listed for 75 \u00b0C, 3 AWG copper (100 A) also works. For aluminum, use 1/0 AWG at 60 \u00b0C or 1 AWG at 75 \u00b0C.</p>
<h2>Why 3 AWG copper is not enough on 60 \u00b0C terminals</h2>
<p>NEC 110.14(C) limits circuits of 100 A or less to the 60 \u00b0C column unless the equipment is listed for 75 \u00b0C. Table 310.16 around 90 A reads:</p>
{amp}
<p>3 AWG copper carries only 85 A in the 60 \u00b0C column, below the 90 A breaker. 2 AWG copper carries 95 A there, so it is the standard answer. With 75 \u00b0C terminals throughout, 3 AWG copper is rated 100 A and passes. Many modern breakers and lugs are marked 75 \u00b0C, but read the nameplate rather than assuming.</p>
<h2>Which size for which wiring method</h2>
{pick}
<p>Aluminum steps up about one size from copper in each column. 1 AWG aluminum gives 85 A at 60 \u00b0C (too low) but 100 A at 75 \u00b0C, while 1/0 AWG clears 90 A in both columns. The equipment ground comes from NEC Table 250.122; breakers above 60 A and up to 100 A fall in the row that calls for 8 AWG copper or 6 AWG aluminum. If you upsize the circuit wires for voltage drop, the ground must be increased proportionally.</p>
<h2>Voltage drop on a 90 A run</h2>
<p>Using the resistance values behind our {L('/voltage-drop-calculator/', 'voltage drop calculator')}, single phase, 100 ft one way, full 90 A on 240 V:</p>
{vd}
<p>NEC suggests keeping feeder and branch drop under about 3 % each (informational notes, not a hard rule). Longer runs may call for one size up, and a subpanel feeder rarely carries its full breaker rating all day, so the real drop is often smaller.</p>
<h2>Continuous loads on a 90 A breaker</h2>
<p>A standard breaker should carry a continuous load (3 hours or more) of no more than 80 % of its rating under NEC 210.20(A) and 215.3, which is 72 A on a 90 A breaker. Use this number when sizing EV charging, electric heat, or any load that runs for hours. Check the equipment instructions, since manufacturers publish their own minimum circuit sizes.</p>
<h2>Is a 90 A breaker standard?</h2>
<p>Yes. NEC 240.6(A) lists 90 A among the standard ratings, between 80 and 100 A. It is less common than 60 or 100 A, but turns up on subpanels, large heat pumps, and electric furnaces with strip heat. If a 100 A breaker is available and your wire supports it, many installers choose that instead; check that the wire is rated for the larger breaker.</p>
<h2>Example: 90 A subpanel, 120 ft, THHN in conduit</h2>
<p>With 75 \u00b0C lugs at both ends, 3 AWG copper (100 A at 75 \u00b0C) satisfies the breaker. If the lug rating is unknown or says 60 \u00b0C, go to 2 AWG copper. Add an 8 AWG copper ground and a neutral, then check the drop with the calculator: at 120 ft and 90 A, 2 AWG copper drops about {_vd('2','cu',120)[1]} on 240 V. Finally size the conduit with the {L('/conduit-fill-calculator/', 'conduit fill calculator')}.</p>
<p>See the {L('/wire-ampacity-chart/', 'wire ampacity chart')}, the {L('/2-awg-wire-ampacity/', '2 AWG ampacity page')}, and the guides for an {L('/blog/wire-size-for-80-amp-breaker/', '80 amp breaker')} and a {L('/blog/wire-size-for-70-amp-breaker/', '70 amp breaker')}.</p>
<h2>Limits of this guide</h2>
<p>Values assume 30 \u00b0C ambient and no more than three current-carrying conductors. Hot attics or bundled cables need derating under NEC 310.15. Local amendments and your inspector have the final say, so treat this as a reference.</p>
{sources([('https://wireref.com/ampacity', 'WireRef: NEC Table 310.16 ampacity chart')])}
'''}

FAQS = {
 'wire-size-for-90-amp-breaker': [
  ('What size wire for a 90 amp breaker?', '2 AWG copper on 60 \u00b0C terminals (3 AWG copper if all terminals are rated 75 \u00b0C), or 1/0 AWG aluminum (1 AWG at 75 \u00b0C).'),
  ('Can I use 3 AWG on a 90 amp breaker?', 'Only with 75 \u00b0C-rated terminals throughout, where 3 AWG copper is rated 100 A. In the 60 \u00b0C column it is 85 A, too low.'),
  ('What size ground wire for a 90 amp breaker?', '8 AWG copper or 6 AWG aluminum from NEC Table 250.122, larger if you upsize the circuit wires.'),
  ('What wire size for a 90 amp subpanel?', '2 AWG copper with an 8 AWG ground is the safe default; 3 AWG works only with 75 \u00b0C terminations.'),
  ('How many amps can I draw continuously on a 90 amp breaker?', 'At most 72 A for loads running 3 hours or more, which is 80 % of the breaker rating.')],
}
RELATED_GUIDES = {
 '/wire-ampacity-chart/': [('wire-size-for-90-amp-breaker', 'Wire size for a 90 amp breaker')],
 '/2-awg-wire-ampacity/': [('wire-size-for-90-amp-breaker', 'Wire size for a 90 amp breaker')],
 '/voltage-drop-calculator/': [('wire-size-for-90-amp-breaker', 'Wire size for a 90 amp breaker')],
}
