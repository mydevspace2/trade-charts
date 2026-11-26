"""Post 33 (run 2026-11-26)."""
import json, os
from core import table
from posts5 import L, sources

NEW_POSTS = [
 ('wire-size-for-70-amp-breaker', 'Wire Size for a 70 Amp Breaker: 4 AWG Copper or 2 AWG Aluminum',
  'What wire size does a 70 amp breaker need? 4 AWG copper, 2 AWG aluminum on 60 \u00b0C terminals (3 AWG at 75 \u00b0C), 8 AWG copper ground, plus voltage drop.', '2026-11-26'),
]
_E = json.load(open(os.path.join(os.path.dirname(__file__), 'data', 'electrical.json')))


def _vd(size, met, ft=100, amps=70, volts=240):
    r = _E['t8'][size][met]
    v = 2 * ft * amps * r / 1000
    return f'{v:.2f} V', f'{v / volts * 100:.2f} %'


def bodies():
    rows = []
    for lab, size, met in [('4 AWG copper', '4', 'cu'), ('3 AWG copper', '3', 'cu'), ('2 AWG aluminum', '2', 'al'), ('1 AWG aluminum', '1', 'al')]:
        if size not in _E['t8']:
            continue
        v, p = _vd(size, met)
        rows.append((lab, v, p))
    amp = table(['Size', '60 \u00b0C column', '75 \u00b0C column'], [
        ('6 AWG copper', '55 A', '65 A'), ('4 AWG copper', '70 A', '85 A'), ('3 AWG copper', '85 A', '100 A'),
        ('4 AWG aluminum', '55 A', '65 A'), ('3 AWG aluminum', '65 A', '75 A'), ('2 AWG aluminum', '75 A', '90 A')])
    pick = table(['Wiring', 'Copper', 'Aluminum'], [
        ('NM cable, or any 60 \u00b0C terminal', '4 AWG', '2 AWG'),
        ('Single conductors, every termination listed for 75 \u00b0C', '4 AWG', '3 AWG'),
        ('Equipment ground (Table 250.122, 70 A breaker)', '8 AWG', '6 AWG')])
    vd = table(['Size (100 ft one way, 70 A, 240 V)', 'Drop', 'Percent'], rows)
    return {'wire-size-for-70-amp-breaker': f'''
<p class="lead">The short answer: a 70 amp breaker takes 4 AWG copper. It carries 70 A in the 60 \u00b0C column, so no terminal check is needed. Aluminum needs 2 AWG on 60 \u00b0C terminals, or 3 AWG when every termination is rated 75 \u00b0C.</p>
<h2>Why 4 AWG copper fits exactly</h2>
<p>NEC 110.14(C) limits a circuit of 100 A or less to the 60 \u00b0C column unless the equipment is listed for 75 \u00b0C. Table 310.16 around 70 A reads:</p>
{amp}
<p>4 AWG copper is rated 70 A at 60 \u00b0C, exactly the breaker size, and 85 A at 75 \u00b0C. 6 AWG copper tops out at 65 A even on 75 \u00b0C terminals, so it is too small for a 70 A breaker.</p>
<h2>Which size for which wiring method</h2>
{pick}
<p>Aluminum shifts by one size depending on terminals: 3 AWG gives 65 A at 60 \u00b0C (too low) but 75 A at 75 \u00b0C. 2 AWG clears 70 A in both columns. The equipment ground comes from NEC Table 250.122; a 70 A breaker falls in the row for devices up to 100 A. Upsizing the circuit wires for distance also upsizes the ground (250.122(B)).</p>
<h2>Voltage drop on a 70 A run</h2>
<p>Using the resistance values behind our {L('/voltage-drop-calculator/', 'voltage drop calculator')}, single phase, 100 ft one way, full 70 A on 240 V:</p>
{vd}
<p>NEC suggests keeping feeder and branch drop under about 3 % each (informational notes, not a hard rule). Longer runs may call for one size up.</p>
<h2>Is a 70 A breaker standard?</h2>
<p>Yes. Standard sizes in NEC 240.6(A) include 60, 70, 80, 90 and 100 A. Many 70 A circuits feed subpanels, hot tubs, and large heat pumps or electric furnaces; check the nameplate for the minimum circuit ampacity and maximum breaker.</p>
<h2>Example: 70 A subpanel in a detached garage</h2>
<p>You run THHN in conduit, 120 ft, with 75 \u00b0C lugs at both ends. Copper 4 AWG (85 A at 75 \u00b0C) is the answer, and the lug label is irrelevant because 4 AWG already meets 70 A at 60 \u00b0C. Add an 8 AWG copper ground and a neutral. Check the drop with the calculator, then size the pipe with the {L('/conduit-fill-calculator/', 'conduit fill calculator')}.</p>
<p>See the {L('/wire-ampacity-chart/', 'wire ampacity chart')}, the {L('/4-awg-wire-ampacity/', '4 AWG ampacity page')}, the guides for a {L('/blog/wire-size-for-60-amp-breaker/', '60 amp breaker')} and a {L('/blog/wire-size-for-50-amp-breaker/', '50 amp breaker')}, and the {L('/electrical/', 'electrical hub')}.</p>
<h2>Limits of this guide</h2>
<p>Values assume 30 \u00b0C ambient and no more than three current-carrying conductors. Hot attics or bundled cables need derating under NEC 310.15. This is a reference, not a substitute for the code your inspector enforces.</p>
{sources([('https://wireref.com/ampacity', 'WireRef: NEC Table 310.16 ampacity chart')])}
'''}

FAQS = {
 'wire-size-for-70-amp-breaker': [
  ('What size wire for a 70 amp breaker?', '4 AWG copper, or 2 AWG aluminum on 60 \u00b0C terminals (3 AWG aluminum when all terminals are rated 75 \u00b0C).'),
  ('Can I use 6 AWG on a 70 amp breaker?', 'No. 6 AWG copper is rated 65 A at 75 \u00b0C and 55 A at 60 \u00b0C, both under 70 A.'),
  ('What size ground wire for a 70 amp breaker?', '8 AWG copper or 6 AWG aluminum from NEC Table 250.122, larger if you upsize the circuit wires.'),
  ('What wire size for a 70 amp subpanel?', '4 AWG copper with an 8 AWG ground is the standard choice; go up a size on long runs.'),
  ('Can I use 4 AWG aluminum for 70 amps?', 'No. 4 AWG aluminum is rated 55 A at 60 \u00b0C and 65 A at 75 \u00b0C. Use 3 AWG at 75 \u00b0C or 2 AWG.')],
}
RELATED_GUIDES = {
 '/wire-ampacity-chart/': [('wire-size-for-70-amp-breaker', 'Wire size for a 70 amp breaker')],
 '/4-awg-wire-ampacity/': [('wire-size-for-70-amp-breaker', 'Wire size for a 70 amp breaker')],
 '/2-awg-wire-ampacity/': [('wire-size-for-70-amp-breaker', 'Wire size for a 70 amp breaker')],
 '/voltage-drop-calculator/': [('wire-size-for-70-amp-breaker', 'Wire size for a 70 amp breaker')],
}
