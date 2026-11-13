# Micro-niche gaps for zero-budget static tool sites (US/UK/CA/AU), all verticals

Owner: Yasir. Research date: **13 Nov 2026**. Status: **research only. Nothing was bought, built or posted.**
Follows `micro-tool-website-playbook`, the crowding rule and the premium-country hub rule in `work/knowledge-base/niche-pipeline.md`. Skipped on purpose (already covered): HVAC, insurance/CRE worksheets, 401(k), Form 2210, farm calibration, and all EU/compliance/tax ideas in `plan.md` and `premium-niches.md`.

## How the numbers were gathered (read first)
- **Problem evidence:** Google autocomplete (US, `work/niches/ac.py`) → raw in `work/niches/raw/micro/us_ac.json` / `.txt`, plus forum threads seen in the SERPs (Weld Talk, WeldingWeb, Reddit, Langmuir forum).
- **Volumes:** Ahrefs **free** Keyword Generator, Google, Phrase match, US (UK for grade boundaries), 13 Nov 2026. Buckets only (`<100`, `>100`, `>1K`). **Every volume is an estimate.** Notes: `/workspace/web/notes/4d33c9a5-39ad-43fa-885b-d72bfcc6b372/ahrefs-micro-a-*`, `-b-*`, `-c-*`, `-d-*`.
- **Competitor traffic:** Ahrefs free Traffic Checker (domain incl. subdomains), 13 Nov 2026. Notes: `ahrefs-micro-tc1-*`, `ahrefs-micro-tc2-*`.
- **SERPs:** `web_search` with country=US (GB for exams). An approximation of Google, not a VPN view. Tool counts are dedicated tool/chart pages seen on the first ~20 results. No competitor tool was tested by hand.
- **CPC tier:** **estimate only**, judged from the niche (no free CPC data).
- **Domains:** `curl https://rdap.verisign.com/com/v1/domain/NAME` on 13 Nov 2026 (404 = unregistered then). Can change any time.
- **Not Ahrefs-checked:** quilt backing, aquarium stocking, EV charge time per model (SERP only). Not checked at all: knitting yarn calculators, candle/epoxy resin, climbing grades, concrete/roofing/flooring/paint, Part 107 drones, NCLEX dosage beyond drip rate. Marked as such below.

---

## 0. Headline finding: the AI swarm has reached every hobby and trade vertical too

The EU/compliance "swarm" finding holds across **all** verticals scanned. By Nov 2026 almost every calculator, chart and file-viewer query has **8–17 dedicated, client-side, often programmatic tool sites** on page 1, most launched in 2026 and sitting at **0 organic traffic**:

| Checked in Ahrefs Traffic Checker (13 Nov 2026) | Niche | Organic/mo |
|---|---|---|
| ratedarc.com | MIG settings (the only tool site in the welding SERP) | 0 |
| timbermath.com | wood movement, 59 per-species pages | 0 |
| chainsawchainsize.com | per-saw chain pages | 0 |
| agebyserialnumber.com | water-heater serial decoder | 0 |
| layercaliber.com | per-printer resin settings | 0 |
| getchipload.com | per-bit CNC feeds (185 settings, 73 bits) | 9 ($6) |
| gradeboundaries.uk | per-subject exam boundaries | 0 |
| plumbmath.com | gas pipe sizing | 0 |
| statfile.tools | SPSS .sav viewer | 0 |
| cutchart.com | per-machine laser settings | 0 |

Important nuance: these sites are **young** (most 2026). Zero traffic proves the niche is crowded and that "be first with a tool" no longer works; it does **not** prove nobody will win later. The only thing still scarce is **hand-extracted data that is locked in PDFs, door stickers and manuals**, where the swarm has not bothered to transcribe it yet.

---

## 1. Candidates (26), grouped by vertical

Score (1–10) = demand + SERP weakness + static-JS feasibility + programmatic depth + premium CPC, with a heavy crowding penalty. HVAC hub benchmark = **6.5**.

### Trades (welding, machining, woodworking, plumbing)

#### M1. Welding & cutting machine settings hub (per-machine MIG door charts, TIG, plasma cut charts), US — **Score 6**
- **Problem evidence:** autocomplete "hobart 140 settings chart", "hobart handler 140 settings chart", "mig welder settings chart [metric/pdf/uk/for beginners/for steel]"; Weld Talk threads back to 2006 asking for settings for gauges not on the door chart (e.g. "no settings on the chart for 14ga and 12ga"); Harbor Freight Titanium Easy-Flux 125 users say its door chart "runs hot" (fypower.org, WeldingWeb thread converting A–J to volts).
- **Volume (Ahrefs US):** "mig welder settings chart" **>100 Easy**, 25 phrase variants ("miller mig welder settings chart" **>100**; lincoln 140 / 180 / 180c, esab, hobart, yeswelder 135, everlast, millermatic 252, cig, clarke `<100`); "aluminum tig welding settings chart" **>100 Easy** (13 TIG variants); "titanium easy flux 125 settings chart" `<100` (3 variants); "hypertherm 45xp cut chart", "millermatic 211 settings chart", "plasma cutter cut chart" `<100`; "hobart 140 settings chart" and "lincoln 140 settings chart" → **no data** (tiny, though autocomplete shows them).
- **SERP top 5 ("hobart handler 140 settings chart", US):** 1 ratedarc.com (one page comparing 6 machines' door charts; **0 traffic**); 2 makers.dozuki.com guide; 3 Northern Tool PDF manual; 4 Tractor Supply PDF manual; 5 Weld Talk forum. Also ManualsLib, more PDFs, WeldingWeb. Titanium Easy-Flux 125: reviews + HF PDF manual + ManualsLib + forum, **no tool**. Hypertherm 45XP cut chart: **all PDFs** (Hypertherm manuals, dealer CSVs). PrimeWeld TIG225X: Weldmonger blog + PDF manual. → **Passes the crowding rule** (1 tool site, the rest PDFs/forums).
- **Competitor traffic:** ratedarc.com 0.
- **CPC (estimate):** Medium (welding supply, wire, helmets, machines; Amazon affiliate fit).
- **Programmatic pages:** ~60–150: one page per machine (Hobart Handler 100/140/190/210 MVP, Lincoln 140/180/210 MP, Millermatic 141/142/211/212/255, Eastwood, YesWelder, Titanium 125/140/170, Vulcan, Forney, Everlast, PrimeWeld), each with its door chart as an HTML table + a gauge→setting lookup that interpolates missing gauges; plus plasma cut-chart pages per machine × material (Hypertherm 30/45/65/85, Lincoln, Miller, Everlast); plus TIG settings per machine × metal.
- **Static JS:** yes (JSON tables → HTML pages; one interpolation script).
- **Build:** 14–20 days (most of it is transcribing door charts from public manuals/PDFs and checking them; cite the manual per page).
- **Risks:** low per-page volume (many machine pages will be `<100` or unmeasured); data accuracy (publish "maker's starting point" + source link); ratedarc could expand.
- **Domain (.com free 13 Nov):** `weldsettingschart.com`, `welderchart.com`, `weldcharts.com`, `welderdoorchart.com` (taken: migsettings.com, tigsettings.com).
- **vs HVAC 6.5:** same pattern (trades field reference, US 99%) and a cleaner SERP, but smaller per-page demand and heavier data entry. Slightly below.

#### M2. Gas pipe sizing chart / calculator, US — **Score 4 as a new domain; strong add-on to the HVAC hub**
- **Volume:** "gas pipe sizing chart" **>1K Easy**, **169 phrase variants** (natural gas, BTU, 2 psi, LP/propane, CSST, copper, pdf several at `>100`).
- **SERP (US):** turn2engineering (chart + calculator), engtank, PDF charts, ezvirtualtools, plumbcalc.pro, Trane help page, fireplace store chart, plumbmath (**0 traffic**), preppool, fielddojo, edu.kg site, mepcalcs, toolgrit, comfort-calc, closecrew, Play Store app → **12+ tools: fails the crowding rule** as a standalone.
- **CPC:** Medium-High (plumbing/HVAC contractors). **Programmatic:** ~40–80 (gas × material × pressure × length tables). **Static JS:** yes. **Build:** 4–6 days as a section.
- **Domain:** `gaspipechart.com`, `gaspipesizingchart.com` free (gaspipesizing.com taken).
- **Verdict:** don't start a domain; add as pages on the HVAC/trades hub (same techs, same intrysys-style per-variant model).

#### M3. Water heater age by serial number (per brand), US — **Score 4 standalone; add-on to the HVAC hub**
- **Volume:** "water heater age by serial number" **>100 Medium**, **50 variants**; AO Smith / Bradford White / Whirlpool / American **>100 Easy** each; Rheem, State, Reliance, GE, Rinnai, Navien, Lochinvar, Ruud, Kenmore `<100`.
- **SERP:** brand pages (Bradford White), abgre, InterNACHI chart, Palo Alto city page, agebyserialnumber (**0**), **intrysys.com** (already ranks, it is the HVAC benchmark site), repairmeyourself, waterheaterhub, specmyhouse, ownerspec, building-center, agefromserial → **crowded**.
- **CPC:** Medium-High (water-heater replacement leads). **Programmatic:** ~20–30 brand pages. **Build:** 3–4 days. **Domain:** `heaterage.com` free.
- **Verdict:** only as part of a trades hub.

#### M4. Wood movement calculator (per species), US — **Score 2.5**
- **Volume:** **>100 Easy**, 3 variants only. **SERP:** timbermath (59 per-species pages, 0 traffic), builderology, cutmath, doneinbrowser, KM Tools, getkerfcalc, sundryard, sagulator, artysan, thewoodworkingbench (per-species), kerfworks, kerfmath, ecowoods, superglobalcalculator, woodmove.vercel, woodtoolchest → **15+, fails**. CPC Low-Med. Domain `woodmovementcalc.com` free.

#### M5. Deck/floor joist span pages (2x8 joist span etc.), US — **Score 3**
- **Volume:** "2x8 joist span" **>100 Easy**, 16 variants. **SERP:** permitdeck, turn2engineering, UpCodes, reuven.tools, deckmath, deckjoistspan.com (exact-match per size), framingplan, joistspan.com (per species), deckpro.studio, uzi-tools, thebackyardstandard, webstructural → **12+, fails**. CPC Medium (decking). Domain `joistspans.com` free.

### Automotive

#### M6. Regear / gear ratio for tire size, US — **Score 2.5**
- **Volume:** "gear ratio for 35 inch tires" `<100` Easy, 20 vehicle variants (Jeep JK/JL, Silverado, F150). **SERP:** jscalc-blog, gear-ratio-calculator.com (per-tire pages), overlanding.tools, tirereference, everycalculators, carmath, truckingcalc (per-size pages), tiresize.app, 4x4playground, mycarcalc, thewrenchbros, ajdesigner, tiresizehq, jeep blogs → **12+, fails**. Domain `regearcalc.com` free.

#### M7. EV charging time per model, US — **Score 2.5** (SERP only, not Ahrefs-checked)
- **SERP ("how long to charge kia ev9 level 2"):** wattprice (per-model pages), thechargeport, evseekers, motivegrid (per-model), censusev, Zapmap, dealer pages, evchargetimecalculator (per-model), wattsimple (per-model) → **5+ programmatic per-model sites, fails**. Domain `evchargetimes.com` free.

*(VIN/paint-code lookups and tyre-size calculators were not run: big incumbents like paintref, wheel-size and NHTSA are known to own them.)*

### Marine, aviation, radio

#### M8. Boat prop slip calculator (+ per-outboard prop pages), US — **Score 2.5**
- **Volume:** "prop slip calculator" **>100 Easy**, "mercury prop slip calculator" **>100**, 15 variants. **SERP:** calcspec, Mercury Racing (official), Laukkanen, boaterinput, calculatorshelf, bblades, calculatorlib, midwestboatandprops, boatcalculators.com.au, calculator.academy, buckshotracing, ezvirtualtools, nizpromarine, superglobalcalculator, propslip.com.au → **15+, fails**. Per-outboard prop charts are owned by Yamaha's own prop selector + performance bulletins. Domain `propslipcalc.com` free.

#### M9. Crosswind component calculator (per airport), US — **Score 3**
- **Volume:** "crosswind calculator" **>1K Easy**, 24 variants (gusts, e6b, runway). **SERP:** flightstratix (airport mode), flightkit, pilotised, Pilot Institute, aerowindy, moneydeck, occ.hk (5,691 airports), planefit, aerotoolbox, skyduty, clearmetar, aerocompanion, goaround, aviametrix, aviateai, tanod.dev → **15+ incl. per-airport live METAR tools, fails**. Domain `crosswindcalc.com` free.

#### M10. Ham radio dipole length per band, US — **Score 2**
- **Volume:** "dipole length calculator" `<100` Easy, 7 variants. **SERP:** calccorp, superglobalcalculator, 3roam (per-band), calculatorlib, radioranked, hamdeck, k5hh, radioing, joteo, bencritt, MDARC, 73qrz, practicalantennas → **12+, fails**. Domain `dipolecalc.com` free.

*(Part 107 drone not checked: the space is FAA/B4UFLY apps + training schools, not tool-shaped.)*

### Crafts

#### M11. Soap: lye calculator + SAP value per oil, US — **Score 2.5**
- **Volume:** "lye calculator" **>100 Hard**, 115 variants ("brambleberry lye calculator" >100). **SERP (per-oil "sap value of shea butter"):** soapcalc.app (per-oil pages), sjsoap, formulary, soapmakingtoolbox, formulanorth, Soaper's Choice, soapformulator (per-oil), soapledger (131 oils), fromnaturewithlove, artizsoap, pandataps, savon-calcul (per-oil), sekiyasourcing, soaply, emiagro → **15+, KD Hard, fails**. lyecalc.com taken; `lyecalculatorpro.com` free.

#### M12. Quilt backing / binding calculators, US — **Score 2.5** (SERP only)
- **SERP:** quiltler, madegooddesigns, yardagewise, calculatorcollection, boneyardtools, quiltysidekick, mega-calculator, stitchandsum (16 tools), justinfabric, qualitysewing, craftcalc, quiltcalcs, calculator.academy, Robert Kaufman app, makersmath, quiltmath, getmakerly → **15+, fails**. quiltbackingcalc.com taken.

*(Knitting yarn amounts, candle fragrance load and epoxy resin were not run in Ahrefs; autocomplete shows demand ("how much yarn for a blanket" + 7 variants; "candle fragrance load calculator" has only 4 suggestions) but given every adjacent craft SERP is swarmed, expect the same.)*

### 3D printing / laser / CNC

#### M13. Laser engraver settings per machine × material (xTool etc.), US — **Score 3**
- **Volume:** "xtool settings for acrylic" `<100`, 1 keyword (autocomplete shows wood, glass, leather, slate, tumblers, 3mm basswood). **SERP:** xTool support (official), machinesformakers (per-machine × material), bonnycreations (per-machine × material, .md versions), cutchart (**0**), craftcloset, engravesettings, Delvie's → **4+ programmatic databases already, fails**. Domain `lasersettingsdb.com` free.

#### M14. Resin printer exposure settings per printer × resin, US — **Score 3**
- **Volume:** "saturn 4 ultra resin settings" `<100` (3 variants incl. "spreadsheet"). **SERP:** Mr Resin, Liqcreate, Siraya Tech (official), powerresins, 4dfiltration (table), layercaliber (**0**, 20 resins/printer), rayformtech, manuals.plus, 3drs (per-printer), denhac wiki → **resin makers publish their own + 3 programmatic sites, fails**. Domain `resinexposure.com` free.

#### M15. CNC router bit feeds & speeds per bit (Amana/Whiteside), US — **Score 3**
- **Volume:** "amana feeds and speeds" `<100`, 1 keyword. **SERP:** Toolstoday/Amana PDFs, grbl.org, AS&T chart, getchipload (**9/mo**, 185 settings), dcpwood (per-bit), mywerkzeug, workshopcalc → **PDF-heavy but 3 programmatic sites already**, tiny volume. bitfeeds.com taken; `cncbitfeeds.com` free.

### Photography / video / music

#### M16. Recording time per card (4K minutes on 128GB, per camera), US — **Score 2**
- **Volume:** "how many minutes of 4k video on 128gb" `<100`, 1 keyword. **SERP:** sugarland, havecamerawilltravel (+ copy), axenworks, dronegearsetup, soberpilots, Panasonic/Fujifilm/Sandisk/Kioxia official tables, howmanyphotos (per-device), intiaudiovisual, 4calculators, toolfoundry, queststudio → **12+, fails**. Domain `cardrecordtime.com` free.

*(Guitar string tension was only autocomplete-checked: D'Addario, Stringjoy and Ernie Ball brand tools own it; not pursued.)*

### Gaming

#### M17. Game calculators (Arc Raiders crafting/recycle; Silksong save editor), US — **Score 2**
- **Volume:** "arc raiders crafting calculator" `<100`; "silksong save editor" `<100` (4 variants).
- **SERP:** Arc Raiders → arctracker, arccalc, metaforge, gamemapa, craftgenie, arcraidertools, wiki, arcscrappy, bestgameboost, arcraidersai, astroboost, raiders companion app, arcraidertrackers, goopgoopgoop (**15+**). Silksong → silksongsaveeditor.org, save-editor.vercel, silksaver, silksongsaveeditor.com, silksongeditor, savegame.org, galama.me, Nexus mods (**10+**). Game hubs launch within days of release; **fails**. Low CPC, short life.

### Fitness niches

#### M18. Swim time conversion (SCY↔SCM↔LCM), US — **Score 3**
- **Volume:** "swim time converter" **>1K Easy**, 25 variants. **SERP:** swimstandards, tryopenlane/usmsdata, swimtimeconverter.com (exact match), clinicaltoolslibrary, myswimsplits, calculator.academy, SwimSwam (old, authoritative), SportsEngine help, yourswimlog, jcalculator, onlineswimtimeconverter, myswimset, padlie, goswimfast, movementrebels, swimnorthwest → **15+ incl. exact-match domain, fails**. swimconvert.com taken; `swimtimeconvert.com` free.

#### M19. Rowing erg split / watts, US — **Score 2.5**
- **Volume:** "rowing split calculator" **>100 Medium**, 3 variants. **SERP:** Concept2 (official, #1), rowingmachinenerd, fitliferegime, calculator.academy, vivito, movementrebels, machars, getwatta, targetsplits, sport-calculator, rowingrelated, rowrowrow, rowergcalc, rowandspin → **14+, fails**. Domain `ergsplit.com` free.

*(Climbing grade conversion only autocomplete-checked; theCrag and Rockfax own the conversion charts.)*

### Pets / aquarium, gardening

#### M20. Aquarium stocking calculator, US — **Score 2.5** (SERP only)
- **SERP:** aquapacity, app-aquatic, reefcalcs, tankstocking, fishauthority, tankmatcher, aquatic-art, stockinglab (1,003 species), guidarium, fishhuddle, tankbud, lagonia, aqulator, theaquagauge, aquariumstockingcalculator.com — at least 8 are explicit "AqAdvisor alternative" pages → **15+, fails**.

#### M21. Seed-starting dates by zone, US — **Score 3**
- **Volume:** "when to start seeds indoors zone 6" **>100 Medium**, 2 variants (zones 5/6/7/6a/6b/8b in autocomplete). **SERP:** calculatemygarden (per-zone, NOAA ZIP data), Mother Earth News, plantanywhere (9,275 ZIPs), vegetableseeds.org, harvestmath (per-zone + ZIP), veglog, botanotes, Johnny's Seeds (official calculator) + blogs → **8+ programmatic per-zone sites, fails**. Domain `seedstartdate.com` free.

### Education / exams

#### M22. UK exam grade boundaries hub (board × subject × year, GCSE + A level), UK — **Score 5**
- **Volume (Ahrefs UK):** "aqa a level biology grade boundaries" **>1K Easy**, **44 variants** (2025/2026 `>100`; per year, "percentage", "per paper" `<100`). The pattern repeats per board (AQA, OCR, Edexcel, WJEC/Eduqas, CIE) × subject × level, so the total long tail is large (likely hundreds of `>100` head terms; **not measured beyond one subject**).
- **SERP (GB):** Oxford Revise, OxfordAQA PDF, **AQA official PDF**, alevelbiologytutor (all years), gradeboundaries.uk (**0**), craft.cloud mirror PDF, AQA archive, cookie.education, sanity.io mirror PDF, **Save My Exams** (big brand), Pearson PDF, pastpapers.com, asteriskrevision, Exeter College PDF, trypolarbear, mathsgenie → **PDF-heavy, but 8+ dedicated pages incl. Save My Exams and Maths Genie**. Fails as a head-term play; long-tail per-paper/percentage/"what grade is my mark" pages are thinner.
- **CPC (estimate):** Low-Medium (UK tutoring/revision). **Seasonality:** strong spike around results days (Aug; Jan for some boards).
- **Programmatic:** 1,000+ pages possible from board PDFs (subject × year × paper), plus a "mark → grade" calculator per subject.
- **Static JS:** yes. **Build:** 12–18 days (PDF extraction + QA). **Domain:** `gradeboundary.com` free (gradeboundaries.com taken).
- **vs HVAC 6.5:** more volume, but strong incumbents and low CPC; below HVAC.

### Nursing / medical

#### M23. IV drip rate calculator, US/UK/AU — **Score 3**
- **Volume:** "drip rate calculator" **>1K Easy**, 46 variants ("iv drip rate calculator" >100). **SERP:** nursingready, sciencequest (per-volume chart), Goterum app, quickmedcalc, **MDCalc**, usitestat, digithelm, infusicalc, thenursingcentral, McGuff DripCount, NIVA, doserightrn, nursingcalc, ecgwaves, clesial, nandaenfermeria, Play Store apps, shobfree, prospyrmed → **15+, YMYL, fails**.

### File-format viewers / converters

#### M24. SPSS .sav viewer, US — **Score 2.5**
- **Volume:** "sav file viewer" `<100` Medium, 5 variants. **SERP:** savquick, pondpilot, datalion (EN+DE), tabulens, savinspector, filepeek, statfile.tools (**0**), spssviewer, viewer.online, vizly, PSPP web service, savtocsv, quickstats → **12+, fails**. Domain `savfileviewer.com` free.

#### M25. Garmin .FIT file viewer, US — **Score 3**
- **Volume:** "fit file viewer" **>100 Easy**, 13 variants. **SERP:** jasonkuperberg, maplity, sport-calculator, fitfileviewer.com (exact match), formatdesk, harryonline, trainingload.ai, wattsup, avomap, fileviewerhub, viewer.online, geodataviewer, therideatlas, GOTOES, pr.run → **15+ incl. exact-match domain, fails**. Domain `fitfileview.com` free.

### Data / dev micro-utilities

#### M26. systemd OnCalendar generator/validator (+ per-expression pages), US — **Score 3.5**
- **Volume:** "systemd oncalendar" `<100` Easy, but **67 phrase variants** (every 5 minutes, daily, hourly, quarterly, syntax questions) → a crontab.guru-style per-expression long tail exists.
- **SERP:** veldica validator, zerosignuptools, heyutils, **systemd.guru (Cronitor)**, getvoroa, GitHub generator, servercake, radiatus, techopt, naviohq, netguide, opscanopy, linuxdork, steadycron, backendbench, bitlvl → **15+, fails**. Dev CPC Medium-High, but the gap is gone. oncalendar.com taken; `systemdtimer.com` free.

---

## 2. Compact table (all candidates)

| # | Candidate (market) | Head volume (Ahrefs est.) | Long-tail | Tools p1–2 / best competitor traffic | CPC (est.) | Static | Build days | .com free (13 Nov) | Score |
|---|---|---|---|---|---|---|---|---|---|
| M1 | **Welding & cutting machine settings hub** (US) | "mig welder settings chart" >100 Easy; "aluminum tig welding settings chart" >100 | 25 + 13 variants; per-machine <100 | **1 tool** (ratedarc, 0) + PDFs/forums | Med | Yes | 14–20 | weldsettingschart.com, welderchart.com, weldcharts.com | **6** |
| M22 | **UK grade boundaries hub** (UK) | "aqa a level biology grade boundaries" >1K Easy | 44 per subject; 1,000+ pages | 8+ incl. Save My Exams; gradeboundaries.uk 0 | Low-Med | Yes | 12–18 | gradeboundary.com | **5** |
| M2 | Gas pipe sizing chart (US) | >1K Easy | 169 | 12+; plumbmath 0 | Med-High | Yes | 4–6 (as section) | gaspipechart.com | **4** (add-on to HVAC hub) |
| M3 | Water heater age by serial (US) | >100 Med; 4 brands >100 | 50 | 12+ incl. intrysys; agebyserialnumber 0 | Med-High | Yes | 3–4 | heaterage.com | **4** (add-on) |
| M26 | systemd OnCalendar (US) | <100 Easy | 67 | 15+ incl. systemd.guru | Med-High | Yes | 5–7 | systemdtimer.com | 3.5 |
| M5 | Joist span pages (US) | "2x8 joist span" >100 Easy | 16 | 12+ | Med | Yes | 4 | joistspans.com | 3 |
| M9 | Crosswind calculator (US) | >1K Easy | 24 | 15+ | Low-Med | Yes | 5 | crosswindcalc.com | 3 |
| M13 | Laser settings per machine × material | <100 | 1 | 4+ programmatic DBs; cutchart 0 | Low-Med | Yes | 12 | lasersettingsdb.com | 3 |
| M14 | Resin exposure per printer × resin | <100 | 3 | official + 3 programmatic; layercaliber 0 | Low-Med | Yes | 10 | resinexposure.com | 3 |
| M15 | CNC bit feeds per bit | <100 | 1 | PDFs + 3 programmatic; getchipload 9 | Med | Yes | 10 | cncbitfeeds.com | 3 |
| M18 | Swim time converter | >1K Easy | 25 | 15+ | Low | Yes | 3 | swimtimeconvert.com | 3 |
| M21 | Seed starting by zone | >100 Med | 2 | 8+ programmatic | Low-Med | Yes | 5 | seedstartdate.com | 3 |
| M23 | IV drip rate | >1K Easy | 46 | 15+, YMYL | Med | Yes | 3 | dripratecalc.com | 3 |
| M25 | .FIT file viewer | >100 Easy | 13 | 15+ | Low | Yes | 6 | fitfileview.com | 3 |
| M4 | Wood movement | >100 Easy | 3 | 15+; timbermath 0 | Low-Med | Yes | 5 | woodmovementcalc.com | 2.5 |
| M6 | Regear for tire size | <100 Easy | 20 | 12+ | Med | Yes | 5 | regearcalc.com | 2.5 |
| M7 | EV charge time per model | not checked | — | 5+ programmatic | Med | Yes | 6 | evchargetimes.com | 2.5 |
| M8 | Prop slip | >100 Easy | 15 | 15+ incl. Mercury | Med | Yes | 3 | propslipcalc.com | 2.5 |
| M11 | Lye / SAP per oil | >100 **Hard** | 115 | 15+ | Low-Med | Yes | 6 | lyecalculatorpro.com | 2.5 |
| M12 | Quilt backing | not checked | — | 15+ | Low | Yes | 3 | (quiltbackingcalc.com taken) | 2.5 |
| M19 | Rowing split | >100 Med | 3 | 14+ incl. Concept2 | Low | Yes | 3 | ergsplit.com | 2.5 |
| M20 | Aquarium stocking | not checked | — | 15+ | Low | Yes | 10 | — | 2.5 |
| M24 | SPSS .sav viewer | <100 Med | 5 | 12+; statfile.tools 0 | Med | Yes | 6 | savfileviewer.com | 2.5 |
| M10 | Dipole length | <100 Easy | 7 | 12+ | Low | Yes | 2 | dipolecalc.com | 2 |
| M16 | 4K minutes per card | <100 | 1 | 12+ | Low | Yes | 3 | cardrecordtime.com | 2 |
| M17 | Game calculators (Arc Raiders, Silksong) | <100 | 1–4 | 10–15+ | Low | Yes | 5 | arccraftcalc.com | 2 |

---

## 3. Top 5 and how each compares with the HVAC hub (6.5)

1. **M1 Welding & cutting machine settings hub — 6.** The only vertical where the SERP is still PDFs, ManualsLib and 2006–2023 forum threads, with one 0-traffic tool site. Demand is real (25 MIG-chart variants, Miller-brand chart >100, aluminium TIG chart >100, forums asking for gauges the door chart skips). Weaker than HVAC because per-machine queries are mostly `<100` or unmeasured and the data must be transcribed by hand from manuals; stronger than HVAC on SERP weakness. Best as part of one trades domain (see below).
2. **M22 UK grade boundaries hub — 5.** Highest raw demand found (>1K per subject head term, 44 variants each, repeated across boards and subjects) and a PDF-heavy SERP, but Save My Exams and Maths Genie already own the head terms and CPC is low. Below HVAC; worth it only as a long-tail "mark → grade per paper" play timed for August.
3. **M2 Gas pipe sizing chart — 4 new / high as an HVAC-hub section.** >1K Easy with 169 variants, but 12+ tools. Same tradesman audience as the HVAC hub, so as pages there it raises the hub rather than competing with it.
4. **M3 Water heater age by serial — 4 new / add-on.** 50 brand variants, four at >100; intrysys (the HVAC benchmark) already ranks for it, which proves trades hubs win these. Only as an HVAC-hub section.
5. **M26 systemd OnCalendar — 3.5.** Dev audience with a crontab.guru-style long tail (67 variants), but 15+ tools including Cronitor's systemd.guru. Below HVAC; skip unless he wants a dev side-project.

**Bottom line:** no new standalone micro-niche beats the HVAC hub. The best move is to **widen the HVAC hub into a US "trades field-reference" hub**: HVAC (A2L PT charts) + gas pipe sizing + water-heater age + welding/plasma machine settings. That one domain would cover 4 proven tradesman query families (the intrysys pattern) and plausibly lifts the HVAC idea from 6.5 to about 7 (my judgement, not measured).

## 4. Lessons to add to the playbook
- **New crowding test result (13 Nov 2026):** across 26 hobby/trade/dev/edu candidates, 23 had 8+ dedicated tools; 10 tool sites checked in Ahrefs were all at 0–9 visits/mo. "Calculator" and "file viewer" ideas are no longer gaps in English.
- **Where gaps still exist:** data that lives in **PDF manuals, door stickers and spec sheets** and needs hand transcription (welder door charts, plasma cut charts). Search for SERPs where pages 1–2 are ManualsLib, PDFs and forums. That is the new "boring formula" signal.
- **Fold, don't spawn:** when a niche fails the crowding rule but shares an audience with a planned hub (gas pipe, water heater → HVAC), add it to the hub instead of a new domain.

## 5. Open items and limits
- Volumes are Ahrefs free buckets; per-machine welding queries partly show "no data". Yasir can confirm the top picks with SBMM or Ahrefs in his own browser.
- Competitor traffic is 0 for young sites; re-check ratedarc.com and gradeboundaries.uk in 2–3 months to see whether anything in these niches is starting to rank.
- SERPs are `web_search` approximations, not a VPN view.
- Not Ahrefs-checked: quilt backing, aquarium stocking, EV charge time. Not checked at all: knitting, candle/epoxy, climbing, concrete/roofing/flooring/paint, Part 107, music/guitar beyond autocomplete.
