# Demand-first niche hunt (research date 13 Nov 2026)

Method: start from what people ask for (Reddit/forums, Google autocomplete, 2026–27 rules, data stuck in PDFs, non-English markets). Then check whether a good free answer already exists. Niches scored in plan.md, premium-niches.md, micro-gaps.md and niche-pipeline.md were skipped.
Nothing was built, bought or posted.

**Data caveats**
- Volumes are Ahrefs free Keyword Generator buckets (<100, >100, >1K). They are estimates, not exact numbers.
- SERP checks used web_search with a country filter, which only approximates Google pages 1–2.
- Build days and scores are my judgement.
- Raw files:
  - `work/niches/raw/demand/` holds us_ac1.json/.txt (US autocomplete) and serp-notes.md (every SERP seen).
  - Ahrefs notes are in `/workspace/web/notes/4d33c9a5-39ad-43fa-885b-d72bfcc6b372/`: `ahrefs-kw-demand-a-*/ahrefs-keyword-results.md`, `ahrefs-kw-demand-b-*/ahrefs-keyword-results.md` and `ahrefs-tc-demand-*/ahrefs-traffic.md`.

## Headline finding
Demand-first does not get around the AI tool swarm. I assessed 34 new candidates and **28 failed the crowding rule**. The swarm now reaches:
- equipment fault codes (fajnepodnosniki.pl lists 8,310 JLG/Genie codes and gets 0 visits/mo)
- Dutch and Swedish boiler and heat-pump codes (instalpunt 806 codes, paraatservice 4,800, husradarn 741)
- car-seat expiry, tire DOT plant codes, transponder chips, sewing bobbins and DMC↔Anchor floss
- 2026 rules: Section 232 HTS, EUDR Annex I (amended Sep 2026), CBAM defaults, the new 1099-R boxes 7a–7d

The swarm sites are young and nearly all get 0–100 visits/mo. Examples: anzscofinder 0, howoldismyunit 0, dtlgc 0, helovesmath 32 (falling), matchthatpaint 72. Being crowded does not mean anyone is winning, but it does mean being first is no longer possible.

Real gaps only remain where the data is a **trade catalogue that nobody has transcribed**. Key blank cross-references are the clearest case. A few others are borderline, where the only competitors are vendor PDFs, retailers or 2–3 programmatic sites.

**No candidate beats the 7/10 trades-hub benchmark.** The best is about 5.5.

## Top 15 (compact)
| # | Niche (market) | Demand evidence | Ahrefs (est.) | SERP p1–2 / crowding | Best competitor traffic (Ahrefs free) | Long-tail pages from public data | Static JS / build days | Free .com (RDAP 404) | Score |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Key blank cross-reference + locksmith reference hub** (US): blank ↔ Ilco/JMA/Silca/Curtis/Axxess equivalents, keyway by lock brand, pinning charts | r/Locksmith "Key blank guide?" (answer: "the Ilco key blank directory… is available online", i.e. a PDF); r/lockpicking "Ilco has free PDFs"; r/Locksmith "can't find them anywhere"; paid software exists (Blackhawk KBX 85,000 blanks, InstaCode, Framon) | "kw1 key blank" >100 Easy (9 kw); "key blank cross reference" <100 Easy, **68 phrase variants** (ch751, hl1, abus, sargent, axxess…) | Ilco directory PDFs, retailers (easykeys per-blank pages, lockpicks.com, CLK), carkeysource guide, thmkey printable PDFs, dtlgc.com legacy search. **0–1 free tool: GAP** | easykeys.com 10.4K/mo, but mostly brand terms + "key replacement" (it is a retailer); dtlgc.com 0 | ~800–1,500 (popular blanks × makers' numbers, plus lock-brand and keyway pages; Ilco Section 10 cross-ref + retailer xrefs are facts) | Yes, JSON search. 12–18 days (data transcription is the work) | keyblankfinder.com, keyblankcross.com, keyblanklookup.com, whatkeyblank.com, keyblankchart.com | **5.5** |
| 2 | **TPMS relearn procedure by make/model/year** (US) | BITOG "Compilation of TPMS relearning by manufacturer" thread (users swap Dill lookup + Halderman PDFs); r/chevycolorado "TPMS reset without tools"; GM/Ram forums | "tpms relearn procedure" <100 Easy, **96 phrase variants** (per vehicle) | Vendor PDFs (Dill, Halderman, Würth; TIA chart is paid), ATEQ per-model articles, el50448 & Autel vendor lookups, tpmsdirect, mytpms.com.au; programmatic entrants ownerspecs.com and scantoolmatch.com. **Borderline** (2–3 tools) | tpmsdirect.com 672/mo (falling) | ~1,500–3,000 (make × model × year range; procedures are short factual steps, must be reworded) | Yes. 10–14 days | tpmsrelearns.com, relearntpms.com, tpmsrelearnguide.com | **4.5** |
| 3 | Circuit-breaker interchangeability (UL classified CL/CHQ/QD ↔ HOM/QO/QP/THQL) (US) | DIY StackExchange "Is this Eaton breaker compatible with my Siemens panel?"; Mike Holt and InterNACHI threads | "circuit breaker compatibility chart" <100 Easy (15 variants by brand) | Eaton/Siemens PDFs + turn2engineering chart + allbreakersales searchable chart + 6–8 contractor articles. Content-crowded, 2 tools | turn2engineering.com 12.2K/mo (whole engineering site, not this page) | ~150–300 (breaker catalog no. → classified equivalent; panel family pages) | Yes. 5–7 days | breakerinterchange.com, breakerfits.com, breakercrossref.com | **4** standalone; **add to US trades hub** |
| 4 | State test raw→scale conversion hub (STAAR + NY Regents, later other states) (US) | Teachers/parents search per admin; TEA and NYSED only publish per-test PDFs | STAAR table <100 (9 variants by year); Algebra 1 Regents chart <100 (20 variants) | STAAR: TEA PDFs on p1, 4–5 tools deeper (helovesmath, imasterly, statetestscores…). Regents: nysedregents PDFs + geniusprep, num8ers, revisiontown | geniusprep.com 466/mo (rising); helovesmath.com 32/mo | ~300–600 (subject × grade × admin, each year) | Yes. 6–8 days, plus re-transcription every June/Jan | staarconversion.com, staarrawscore.com, regentscurve.com, regentsconversion.com | **4** (seasonal) |
| 5 | Small-engine age/spec by serial (Kohler, Briggs, Tecumseh, Kawasaki) (US) | Mower-repair forums; Briggs publishes only a FAQ rule + antique PDF | "kohler engine serial number lookup" <100 Easy (3 kw) | Official Briggs FAQ, manuals.plus, howoldismyunit, homeproductsupport. 2–3 tools, thin | howoldismyunit.com 0 | ~100–200 | Yes. 4–6 days | engineagebyserial.com, smallenginedate.com | **3.5**; add to trades hub (next to water-heater age) |
| 6 | Car-seat expiration by model (US) | Parents; manuals bury the "useful life" line | "car seat expiration" **>1K Easy, 787 variants**; "graco car seat expiration" >1K | 8+ tools/catalogues: carseatfacts, leoella, cribworthy, carseatcheck, nrtechstudio, carseathaven, babycarseat.info, themomsite. **FAIL** | not checked | ~400 (model pages) | Yes. 6 days | carseatexpires.com, carseatexpiry.com | 3.5 (best demand, fails crowding) |
| 7 | ANZSCO → OSCA mapping (AU) | Visa applicants; Home Affairs had not adopted OSCA (anzscofinder, Jun 2026) | <100 (2 kw) | ABS official + anzscofinder, visaplan, immiiq | anzscofinder.com 0 | ~1,000 occupations | Yes. 5 days | anzscotoosca.com, oscacode.com | 3 (**watch**: spikes when Home Affairs switches) |
| 8 | Outboard year by serial (Mercury/Yamaha) (US) | Boat forums | "2 stroke mercury outboard serial number year chart" >100 Easy; head <100 | obparts, boatlaunchmap, maxrules, boatserialnumber + decoders. FAIL | not checked | ~200 | Yes. 4 days | — | 3 |
| 9 | Garage-door learn-button → compatible remote (US) | Homeowners | not checked | Chamberlain official tool + openermatch, garageopenermatch, garagedoorzone. FAIL-ish | not checked | ~300 | Yes | — | 3 |
| 10 | Section 232 derivative HTS lookup (US) | Importers; frequent Federal Register inclusions | not checked | dutytrade, tariffsentinel, htshero, htslookup, tariffsapi, costvanta. FAIL | not checked | ~900 codes | Yes | — | 3 |
| 11 | Tire DOT plant code lookup (US) | Consumers checking tire origin | "tire dot code lookup" >100 Medium (12 kw) | treadsley, treadgrade, tireage, vehdb, whoactuallymakes, flatfixvault, wfirm. FAIL | not checked | ~1,250 plants | Yes | dotplantcode.com | 2.5 |
| 12 | BM ↔ SW paint equivalents (US) | Reddit r/paint asks | "sherwin williams equivalent to benjamin moore" <100 Easy (11 kw, per colour) | matchthatpaint, paintcolorhq, palettes.page, hueandkit + 4. FAIL | matchthatpaint.com 72/mo (rising) | ~3,000 colours | Yes | paintmatchup.com | 2.5 |
| 13 | Lift/forklift/compact-equipment fault codes (US) | US autocomplete 10/10 for JLG, Genie, Skyjack, Crown, Hyster, Bobcat | "jlg fault codes" <100 (9 kw); "genie scissor lift fault codes" <100 (1 kw) | fajnepodnosniki (8,310 codes), carcodefinder, codeready, partao, flatearthequipment + 5. FAIL | fajnepodnosniki.pl 0 | ~10,000 codes | Yes | liftfaultcodes.com | 2.5 |
| 14 | Industrial lubricant equivalents (US) | Maintenance techs | "mobil dte 25 equivalent" <100 (2 kw) | materialref.com programmatic + aoilw + vendor charts. FAIL | not checked | ~2,000 products | Yes | lubecrossref.com, oilequivalent.com | 2.5 |
| 15 | E-bike/scooter error codes (Bafang, Segway, Xiaomi) (US) | Autocomplete 10/10 | "bafang error code" <100 (28 kw) | swarm (5+ tools). FAIL | not checked | ~500 | Yes | — | 2.5 |

Also assessed and failed (score 2–2.5):
- reading-level converter, M365 SKU lookup, CBAM default values (DE <100, 10 kw), UK SOC going rate (GB <100, 2 kw)
- Japanese water-heater error codes, Dutch storingscodes, Swedish heat-pump alarm codes
- faucet cartridge cross-reference (Ahrefs: no keyword ideas), DMC↔Anchor (<100, 7 kw), sewing bobbin by model
- 1099-R codes, T4A boxes, UK term dates, TEKS, transponder chips, EUDR HS scope, Kwikset/Schlage pinning (fold into #1)

## Top 5: why, and the domain
1. **Key blank cross-reference hub** (keyblankfinder.com or whatkeyblank.com). This is the only clear gap.
   - Page 1 is the Ilco PDF directory, retailers and paid desktop software. The one free search (dtlgc) gets 0 visits.
   - Locksmiths and DIYers ask on Reddit and get pointed to PDFs.
   - There are 68 phrase variants with a clean "<blank> key blank cross reference" pattern, and "kw1 key blank" is >100.
   - Weaknesses: low volumes, low-value audience (blanks cost $1), and retailers like easykeys already rank per-blank pages that list cross-refs.
   - Monetise with key machines, Lishi tools and Amazon blank kits.
   - Moat: transcription effort (thousands of rows) that the swarm skips.
2. **TPMS relearn by vehicle** (tpmsrelearns.com).
   - Big long tail (96 per-vehicle variants) and a classic "data trapped in vendor PDFs" pattern.
   - Already being entered by ownerspecs and scantoolmatch, so speed matters.
   - Good fit for automotive tool affiliates (TPMS tools $20–$500).
3. **Breaker interchangeability** (breakerinterchange.com).
   - Small, but the same audience as the planned US trades hub (electricians and homeowners).
   - Best as a hub section rather than its own domain.
4. **STAAR + Regents conversion hub** (staarconversion.com / regentscurve.com).
   - Official answers are PDFs per test.
   - Seasonal spikes around score release.
   - Needs re-transcription each administration. A thin tool layer exists but has almost no traffic (helovesmath 32/mo).
5. **Small-engine age by serial** (engineagebyserial.com). Thin SERP and a natural add-on to the hub's water-heater-age section.

**Beats 7/10? No.** The best is 5.5, against the trades-hub benchmark of ~7.

## Recommendation (judgement)
- Keep the **US trades field-reference hub** as the main build. Add breaker interchangeability (#3) and small-engine age (#5) as sections. They share its audience and reuse the same lookup template.
- If a second domain is wanted, the only candidate worth it is the **key blank / locksmith reference hub** (#1), probably joined later by TPMS relearn (#2) as an automotive section ("keys and tire service").
- Put ANZSCO→OSCA on a watch list and re-check when Home Affairs adopts OSCA.

## Rules added from this hunt
- Autocomplete depth (10/10 suggestions) does not mean a gap any more. Every 10/10 fault-code seed in the US batch was already swarmed.
- The surviving gap signal is a page 1 of **catalogue PDFs + retailers + paid desktop software**, with no free web lookup that gets traffic.
- Non-English code lookups (NL, SE, JP) are swarmed too. Being non-English is no longer a moat on its own.
