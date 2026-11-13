# Premium-country micro-tool niches (US / UK / CA / AU, DE secondary)

Owner: Yasir. Research date: **13 Nov 2026**. Status: **research only. Nothing was bought, built or posted.**
Constraints: zero budget, static client-side JS, GitHub Pages + free or cheap domain, AdSense later. Method: `micro-tool-website-playbook` + the crowding rule in `work/knowledge-base/niche-pipeline.md`.

## How the numbers were gathered (read this first)
- **Volumes:** Ahrefs free Keyword Generator, per country, 13 Nov 2026. The free tool only shows buckets (`<100`, `>100`, `>1K`, `>10K`) and a KD label. **Every volume here is an estimate.** Where a number has no bucket sign (e.g. "200"), it is the per-keyword volume the free **Traffic Checker** showed for a competitor's ranking keyword.
- **Competitor traffic:** Ahrefs free Traffic Checker ("domain incl. subdomains"), 13 Nov 2026. DR is not shown in the free tool.
- **SERPs:** `web_search` with a country filter (US/GB/AU/CA). An approximation of local Google, not a VPN view. Weaknesses come from the result pages/excerpts; **no competitor tool was tested by hand.**
- **CPC tier:** **estimate only.** No free tool we used shows CPC. Tiers are judged from the niche (insurance / tax / benefits / CRE = High; trades / HVAC = Medium-High; agriculture = Low-Medium; hobby = Low).
- **Domains:** `.com` checked with `curl https://rdap.verisign.com/com/v1/domain/NAME` (404 = unregistered) on 13 Nov 2026. Availability can change any time.
- **Raw data:** autocomplete in `work/niches/raw/premium/{us,uk,de}.json`; Ahrefs notes in `/workspace/web/notes/4d33c9a5-39ad-43fa-885b-d72bfcc6b372/` folders `ahrefs-p1-*` … `ahrefs-p6-*` (keyword generator: p1, p2, p3, p4, second p1 run; traffic checker: p5 ×2, p6).

---

## 0. The headline finding: fresh-trigger single tools are already swarmed in English markets

The plan's §0 finding (EU e-invoicing swarm) is **even stronger in US/UK/AU**. Every 2025–2027 regulation-driven calculator I checked already has **8–17 dedicated free, client-side tool pages**, mostly AI-built, and nearly all of them get **0 organic traffic**:

| Trigger (date) | Dedicated tools on page 1 | Sample checked in Ahrefs (organic/mo) |
|---|---|---|
| US OBBBA car-loan interest deduction + "final assembly VIN check" (2025–2028) | 12+ (doesmycarqualify, assemblyalert, whobuiltmycar, carloancheckup, carloandeduction, overtimekept, tools-berry…) | carloancheckup.com **0**, doesmycarqualify.com **0** |
| UK eVED pay-per-mile EV tax (1 Apr 2028) | 10+ (taxcalcuk, logbook, kalqlater, calculatetax, autochain, calks, carcomparison…) | Ahrefs has **no keyword data** for "pay per mile ev tax calculator" (UK) |
| UK salary-sacrifice £2,000 NI cap (6 Apr 2029) | 12+ (richify, utilhub, taxfly, webcalculator, multicalify, ukcalculator, The Times…) | keyword `<100` |
| UK MTD for Income Tax qualifying income (Apr 2026/27/28) | 15+ (taxquarters, taptax, nomorejanuary, accountingstack, quarterwise, countify…) | taxquarters.co.uk **0** |
| UK Renters' Rights Act notice periods (1 May 2026) | 12+ (periodictenancy, landlordgauge, letsentry, landlord-ready, tenancypilot, rentdocs…) | periodictenancy.co.uk **13** (falling) |
| UK unfair-dismissal 6-month qualifying period (1 Jan 2027) | 5+ (notice-period-calculator.uk, workerscalc, shahzebspeaks, toolswebpro…) | workerscalc.com **0** |
| AU Payday Super (1 Jul 2026) | 15+ | keyword `<100` (AU) |
| AU Division 296 $3M super tax (1 Jul 2026) | 15+ incl. the ATO and SuperGuide | keyword `<100` (AU) |
| US state paid leave (MN Jan 2026, ME May 2026) | 8+ per state (paidleavecalc, leavecalc, figuremytax, dashcalculator, state calculators) | paidleavecalc.com **0** |
| US ICHRA affordability 9.96% (2026) | 10+ (insureichra, getprescience, insurf, takecommand, acawise…) | keyword `>100` Medium |
| UK Companies House software-only accounts (1 Apr 2027) | FRC viewer + 5 viewers | accessiblefiling.co.uk **0** |
| Gaussian-splat `.spz` / `.sog` formats (2025) | 10+ viewers | not checked (low CPC) |

**What does earn traffic in premium markets right now:**

| Site | Model | Organic/mo (Ahrefs est.) | Countries | What ranks |
|---|---|---|---|---|
| **intrysys.com** | Trades hub (HVAC + electrical) with **one page per variant** | **476**, ~50 (Jul) → ~1,050 (Sep) → ~450 (Nov) | **US 99%** | "multiplier for 22.5 degree offset" #1 (200), "how many #10 thhn in 3/4 emt" #1 (500), "multiplier for 15 degree offset" #1 (350), ICP serial-number lookup #6 (1.1K), R-449A PT chart page |
| **dealwiseai.com** | Commercial real estate calculator hub | **103**, rising since Aug | US 99% | "tenant improvement allowance calculator" #3 (100), "cap rate calculator for rental property" #6 (200), TI amortization #5 (80) |
| coraa.ai | Compliance calculators + guides | 5.8K, rising | **India 96%** (not premium) | proves the "boring professional formula" model works, but in INR markets |
| fastcalc.us / figuremytax.com | Big multi-calculator sites | 81 / 57 | — | thin; big-site breadth isn't enough either |

**Conclusion for Yasir:** in US/UK/AU, a brand-new domain should not chase a hot regulation with one calculator. What is working is a **topical hub of many programmatic long-tail pages** (one page per angle / size / refrigerant / form variant), aimed at **professionals** whose exact-match queries are too small for the AI swarm to target. Single-keyword volumes are mostly `<100`, so the plan has to be "40–150 pages × small volumes", not "one 10K keyword".

---

## 1. Candidates (15)

Score (1–10) = demand + SERP weakness + client-side feasibility + premium CPC + trend, with a heavy crowding penalty. The crowding rule was applied to each.

### C1. HVAC + electrical field-reference hub (A2L refrigerant PT charts, superheat/subcool, conduit bending and fill), US — **Score 6.5**
- **Keyword cluster (Ahrefs US):** "r454b pt chart" **>1K, KD Easy**, plus 14 variants `<100` (pdf, fahrenheit, honeywell, vs r410a, calculator, dew bubble, r32 vs r454b). Intrysys's ranking keywords (Traffic Checker volumes): "multiplier for 22.5 degree offset" 200, "multiplier for 15 degree offset" 350, "22.5 degree offset multiplier" 150, "how many #10 thhn in 3/4 emt" 500, "icp warranty lookup" 1.1K. Autocomplete confirms many per-size/per-angle variants. UK volume: not checked (US-centric trade).
- **Top-5 SERP ("r-454b pt chart superheat calculator", US):**
  1. intrysys.com R-454B PT chart. Strong page, the real competitor (476/mo).
  2. intrysys.com superheat/subcooling chart. Same site.
  3. ptcharts.com superheat & subcooling calculator. **0 traffic** in Ahrefs.
  4. hvactoolkit.org PT chart. Duplicate `?refrigerant=` parameter URLs for one page; thin.
  5. hvacptcharts.com R454B PT chart. **42/mo, 85% India**; SEO aimed at the wrong market.
  Also: signedbid, unitskit, hvacprocalculator, bigworks, liventolife (92 refrigerants), calcpanel, plus manufacturer PDFs (Honeywell/Chemours) for the "pdf" variants.
- **Crowding check:** 8+ tools for the generic PT-chart query, so **a generic PT chart alone fails the rule.** The gap is breadth plus programmatic pages: one page per refrigerant × use (PT, superheat target, charging), per conduit size × wire type, per offset angle, per brand serial-number age decoder. Intrysys proves those long-tail pages reach #1.
- **Competitor traffic:** intrysys 476 (US 99%); hvacptcharts 42 (India); ptcharts 0.
- **CPC tier (estimate):** Medium-High. Home-services/HVAC advertisers, but much of the traffic is techs rather than homeowners.
- **Why now:** the EPA Technology Transitions rule moved new ducted residential AC/heat-pump systems to A2L refrigerants (R-454B, R-32) from 2025. Techs need new PT tables with bubble/dew columns. NEC 2026 renumbered Article 220 → 120, which is a reason to refresh electrical tables.
- **Build effort:** 10–14 days for a 60–120 page static generator (JSON tables → HTML pages), PT data from public tables. **Accuracy risk:** PT data must be sourced and cross-checked; cite sources per page.
- **Domain ideas:** `a2lptchart.com` (free), `a2lcharts.com` (free), `hvacpt.com` (free). `tradecalcs.com` is taken.

### C2. Commercial insurance + commercial-lease worksheet hub (business income worksheet, coinsurance, TI allowance, percentage rent, CAM true-up, EMR), US — **Score 5.5**
- **Keyword cluster (Ahrefs US):** "business income worksheet" **>100, KD Easy**, plus 30 variants `<100` (chubb / acord / iso / travelers / liberty mutual business income worksheet, template, pdf, manufacturing, non manufacturing); "coinsurance calculator" **>100, Easy** (15 variants, mostly health); "tenant improvement allowance calculator" `<100` Easy; "percentage rent calculator" `<100` Easy; "experience mod calculator" `<100`; "cam reconciliation calculator": no data. UK "business income worksheet" `<100`.
- **Top-5 SERP ("business income insurance worksheet calculator", US):**
  1. countfolk.com BI coinsurance calculator. **32/mo**, multi-topic calculator site.
  2. icsc.com PDF. A conference handout, not a tool.
  3. chubbweb PDF FAQ. Insurer PDF.
  4. marshallsterling blog. An agency blog post, no tool.
  5. icat.com PDF brochure.
  Further down: 4calculators.com, IRMI glossary, Great American worksheet PDF, quizlet. **Mostly PDFs and agency blogs. Only 2 tools.** This passes the crowding rule.
  Coinsurance SERP: 15+ calculators (fails as a standalone). Percentage rent SERP: ~8 tools (dealwiseai, justincrowcre, bizleasecheck, leaselineage, serviceagent…) plus forum and glossary pages. CAM: 12+ tools.
- **Competitor traffic:** dealwiseai.com 103 (US 99%, rising); countfolk.com 32; 4businessinsurance.com 0.
- **CPC tier (estimate):** **High.** Commercial insurance and CRE are among the most expensive ad verticals.
- **Why now:** evergreen. Renewal season (Q4/Q1) drives BI-worksheet searches; the insurer-branded worksheet variants (Chubb, ACORD, ISO, Travelers) are a programmatic page set no tool covers.
- **Build effort:** 7–10 days for 8–12 calculators plus the insurer-worksheet explainer pages (forms are public; recreate the math, do not copy PDFs).
- **Domain ideas:** `coveragecalcs.com` (free), `businessincomecalc.com` (free), `crecalcs.com` (free). `businessincomeworksheet.com` is also free but exact-match and too narrow for a hub. Taken: `insurancecalcs.com`, `biworksheet.com`, `leasecalcs.com`.

### C3. Retirement-plan & benefits compliance tests (401(k) top-heavy, ADP/ACP, ICHRA affordability), US — **Score 5**
- **Keyword cluster (Ahrefs US):** "top heavy test" `<100` Easy, 14 variants (401k top heavy test, 416 top heavy test, key employee definition, calculation), all `<100`; "ichra affordability calculator" **>100, Medium**.
- **Top-5 SERP ("401k top heavy test calculator"):**
  1. coraa.ai. Traffic is 96% India; not focused on US plans.
  2. kinetiplan.net. **0 traffic.**
  3. ePlan Services article. No tool.
  4. scotttuckersolutions. A raw HTML file under wp-uploads.
  5. employeefiduciary blog. No tool.
  Then the IRS page, Human Interest, Gusto help, an IRS PDF. **About 2–3 tools.** The top-heavy test passes the crowding rule; ICHRA (10+ tools) does not.
- **Competitor traffic:** kinetiplan 0; coraa 5.8K but India.
- **CPC tier (estimate):** **High** (401(k) providers, PEOs, benefits brokers).
- **Why now:** annual testing season Jan–Mar for calendar-year plans. 2026 key-employee threshold $235K (per Gusto help). SECURE 2.0 changes keep the rules moving.
- **Build effort:** 6–8 days (top-heavy, ADP/ACP with correction amounts, key-employee/HCE determiner, 410(b) ratio %, ICHRA affordability as a supporting page).
- **Domain ideas:** `topheavytest.com` (free), `401ktestcalc.com` (free), `planteststack.com` (free).

### C4. IRS Form 2210 / Schedule AI underpayment-penalty calculator, US — **Score 4.5**
- **Keyword cluster (Ahrefs US):** "form 2210 calculator" `<100` Easy; "irs form 2210 calculator" `<100` Medium; year variants 2022–2025 `<100`. Autocomplete shows annualized-income variants.
- **Top-5 SERP ("form 2210 annualized income installment method calculator"):**
  1. Intuit ProConnect help. Software docs, no tool.
  2. acceptproof.com scenarios. A guide page.
  3. IRS Form 2210 PDF.
  4. Lacerte help. Docs.
  5. IRS instructions PDF.
  Then taxguidepro.com (a tool), clearmoneyguide, filed.com, estimatedtax.medha.vin (a tool). **PDF and doc dominated, about 3 tools.** Passes the crowding rule.
- **Competitor traffic:** taxguidepro.com 10 (spiked ~50 in Oct, US 100%).
- **CPC tier (estimate):** High (tax prep).
- **Why now:** filing season (Jan–Apr 2027 for TY2026). OBBBA 2025 changed brackets and deductions, so old calculators are stale.
- **Build effort:** 5–7 days (Schedule AI with 4 annualization periods, SE tax, the 90%/100%/110% safe harbors, daily penalty by quarter using IRS rates). **Accuracy risk:** high. Must be tested against IRS worked examples.
- **Domain ideas:** `underpaymentcalc.com` (free), `schedaicalc.com` (free). Taken: `form2210calculator.com`, `estimatedtaxpenalty.com`.

### C5. Farm application calibration hub (anhydrous NH3 rate, center-pivot application rate/timer, sprayer GPA, grain bin), US — **Score 4.5**
- **Keyword cluster (Ahrefs US):** "anhydrous ammonia calculator" `<100` Easy (only 1 keyword); "center pivot calculator" `<100` Easy (1 keyword). Grain-bin and sprayer clusters are bigger by autocomplete but swarmed.
- **Top-5 SERP ("anhydrous ammonia application rate calibration calculator"):**
  1. LSU AgCenter page. Extension text, no tool.
  2. micro-trak.com. A manufacturer page with a simple form.
  3. Hiniker. Manufacturer marketing.
  4. UW soils PDF.
  5. Hiniker blog.
  Then NMSU PDF, UNL PDF, roughlogic.com (**0 traffic**), Nutrien, forum (newagtalk). **PDF dominated.**
  Center-pivot SERP: UTIA PDF, bytes.engineer (**0**), fastcalc, calcbee, K-State PDF, USDA PDF, Texas A&M PDFs. Also **PDF dominated.**
  Grain bin: 15+ tools (fails). Sprayer: 15+ tools (fails).
- **Competitor traffic:** roughlogic 0; bytes.engineer 0; agcalculator.com 0.
- **CPC tier (estimate):** Low-Medium (ag inputs, equipment).
- **Why now:** none (evergreen, seasonal spring/fall). Weak SERPs but tiny volume.
- **Build effort:** 6–8 days for 10–15 calculators.
- **Domain ideas:** `agcalcs.com` (free), `nh3calc.com` (free), `pivotcalcs.com` (free). Taken: `farmcalcs.com`, `fieldcalcs.com`, `pivotcalculator.com`.

### C6. Hospice / home-health Medicare payment calculators (aggregate cap, inpatient cap), US B2B — **Score 4**
- **Keyword cluster (Ahrefs US):** "hospice cap calculator" `<100`; "palmetto hospice cap calculator" `<100`. That is all.
- **Top-5 SERP ("hospice aggregate cap calculator"):**
  1. CMS MM14557 PDF.
  2. HHS guidance page.
  3. eCFR 418.309.
  4. CMS transmittal PDF.
  5. Conference handout PDF.
  Tools: hhvbp.com (**0**), soriagacpa.com (**4/mo**, rising, US 96%). **Government PDFs dominate.** Passes the crowding rule.
- **CPC tier (estimate):** High (healthcare B2B), but the audience is tiny.
- **Why now:** FY2027 cap amount $36,174.75 (CMS MM14557, effective 1 Oct 2026). It resets every year.
- **Build effort:** 3–4 days.
- **Domain:** `hospicecapcalculator.com` (free). Taken: `hospicecap.com`.

### C7. UK iXBRL accounts viewer / pre-filing checker, UK — **Score 4**
- **Keyword cluster (Ahrefs UK):** "ixbrl viewer" `<100` (1 keyword).
- **Top-5 SERP ("ixbrl viewer online free companies house accounts", GB):**
  1. ukixbrlviewer.org.uk. The official FRC beta; searches the register only.
  2. stechanalytics.com (Graffiti). Freemium + AI.
  3. Companies House XBRL validator. Official; upload only.
  4. Companies House FAQ.
  5. closeandfile.co.uk validator. **Server-side upload.**
  Then accessiblefiling.co.uk (client-side viewer, **0 traffic**), wemigrate.co.uk viewer.
- **CPC tier (estimate):** Medium-High (accounting software).
- **Why now:** from **1 Apr 2027** all Companies House accounts must be filed through commercial software (ICAS stakeholder guide; GOV.UK says the joint HMRC/CH online service closed 31 Mar 2026). Every micro-company director will meet iXBRL.
- **Build effort:** 8–12 days (client-side iXBRL parse + FRC tag labels + basic balance checks). A full taxonomy validation in-browser is heavy.
- **Domain:** `ixbrlcheck.com` (free). Taken: `ixbrlviewer.com`.

### C8. Davis-Bacon fringe annualization + certified-payroll (WH-347) checks, US — **Score 3.5**
- **Keyword cluster:** Ahrefs US returned **"No keyword ideas"** for "davis bacon fringe calculator" (two runs). Demand unproven.
- **Top-5 SERP:**
  1. govcontractcalcs.com. **0 traffic.**
  2. supreminders.com.
  3. spreadrun.com guide. **0 traffic.**
  4. eCFR 5.25.
  5. spreadrun.com tool.
  Then prevailingwageindex, levelwage, Cornell LII, miragemetrics, DOL. About 6 tools.
- **CPC tier (estimate):** High (construction payroll software).
- **Why now:** the 2023 DBRA rule (29 CFR 5.25 annualization) is fully in force. Evergreen.
- **Build effort:** 4–5 days.
- **Domain:** `fringecalc.com` (free), `davisbaconcalculator.com` (free).

### C9. US "no tax on overtime" deduction calculator (OBBBA, TY2025–2028) — **Score 3**
- **Keyword cluster (Ahrefs US):** "no tax on overtime calculator" **>10K, KD Medium**; 35 variants `<100` (2025, 2026, turbotax, irs, texas, california, refund, married filing jointly).
- **Top SERP:** big brands (TurboTax, H&R Block, Paycom-type payroll sites, the White House page per autocomplete) plus a swarm of new tool sites (overtimekept.com, taxlumo.com, tools-berry…).
- **Crowding check:** fails, and brands sit on top. **Expires** after TY2028.
- **CPC tier (estimate):** High (tax software).
- **Build effort:** 3–4 days.
- **Domain:** `otdeductioncalc.com` (free), `overtimedeductioncalc.com` (free). Taken: `overtimetaxcalc.com`, `qualifiedovertime.com`, `overtimededuction.com`.

### C10. Form 1099-DA reconciler (exchange CSV → Form 8949), US — **Score 3**
- **Keyword cluster (Ahrefs US):** "1099-da" **>1K Medium**; "form 1099-da" **>1K Hard**; 806 phrase-match keywords ("coinbase 1099-da" >100, "kraken 1099-da" >100, "1099-da instructions" >100).
- **Top SERP:** 1099bconverter.com, fixmycryptotax.com (a client-side reconciler already exists), TaxSlayer support, thetradetaxdesk, cryptotaxedge, Koinly/CoinTracker-type vendors.
- **Crowding check:** borderline; vendors are strong. First 1099-DA *with basis* arrives early 2027 (TY2026), so there is a real spike in Jan–Apr 2027.
- **CPC tier (estimate):** High (crypto tax software). This is tax reporting, not an on-chain action.
- **Build effort:** 8–10 days (per-exchange CSV parsers, FIFO/specific-ID, Form 8949 box G–L mapping). Accuracy risk high.
- **Domain:** `1099dacalc.com` (free). Taken: `form1099da.com`.

### C11. US car-loan-interest deduction + "final assembly VIN check" — **Score 2.5**
- **Ahrefs US:** "car loan interest deduction calculator" **>100**; "…2025" `<100`.
- **SERP:** 12+ tools (doesmycarqualify, assemblyalert, whobuiltmycar, carloancheckup 0, carloandeduction, zerocarbondrive, overtimekept, tools-berry, vehicleloaninterest blog…).
- **Crowding:** fails (≥8 tools, the 2 checked are at 0).
- CPC est.: High (auto finance). Trigger: OBBBA, TY2025–2028. Effort: 3 days (NHTSA vPIC has a public API, CORS not verified). Domain: `loaninterestcheck.com` (free).

### C12. UK Renters' Rights Act notice / Section 13 calculators — **Score 2.5**
- **Ahrefs UK:** "renters rights act notice period" **>100**; for tenants / for landlords `<100`.
- **SERP:** 12+ tools (periodictenancy **13/mo** falling, landlordgauge, letsentry, landlord-ready, rentersrightstoolkit, thesentry, rentdocs, tenancypilot, letsafeuk, landlord-os…).
- **Crowding:** fails. CPC est.: Medium-High (landlord insurance, letting software). Trigger: 1 May 2026 (s21 abolished). Effort: 3 days. Domain: `rentnoticecalc.com` / `ukrentnotice.com` (free).

### C13. UK MTD for Income Tax qualifying-income / start-date checker — **Score 2.5**
- **Ahrefs UK:** "mtd qualifying income" **>100**; calculator / definition / gross or net `<100`.
- **SERP:** 15+ tools (taxquarters **0**, taptax, nomorejanuary, accountingstack, quarterwise, brittaxcalc, makingtaxdigitalcalculator.co.uk, ismytaxdigital, quarterfile, countify…).
- **Crowding:** fails. CPC est.: High (accounting software). Trigger: Apr 2027 £30K and Apr 2028 £20K thresholds. Effort: 2 days. Domain: `mtdtest.com` (free). Taken: `mtdcheck.com`.

### C14. AU Payday Super due-date + Division 296 calculators — **Score 2**
- **Ahrefs AU:** "payday super calculator" `<100`; "division 296 calculator" `<100`.
- **SERP:** 15+ tools each, including the ATO, SuperGuide, Reckon and accountants.
- **Crowding:** fails. CPC est.: High. Trigger: 1 Jul 2026. Effort: 2–3 days. Domains: `paydaysupercalc.com`, `div296calc.com` (both free).

### C15. UK eVED pay-per-mile + salary-sacrifice £2,000 cap calculators — **Score 2**
- **Ahrefs UK:** "pay per mile ev tax calculator": **no keyword data**; "salary sacrifice cap calculator" `<100`.
- **SERP:** 10+ tools each, plus logbook.co.uk and The Times.
- **Crowding:** fails. CPC est.: Medium-High. Triggers: 1 Apr 2028 / 6 Apr 2029 (far off; demand comes later and the swarm is already there). Effort: 2 days. Domain: `evedcalc.com` (free).

**Not shortlisted:** ADIF ham-radio log viewer ("adif viewer" US `<100`; 6+ viewers incl. plainfolder **0**; low CPC). MN/ME paid-leave calculators (`<100`, 8+ tools). Workers' comp EMR (15+ tools). Coinsurance alone (15+). Grain bin and sprayer (15+ each). Gaussian-splat viewers (10+, low CPC). CAM reconciliation alone (12+, Ahrefs no data). Federal post-judgment interest (8+ tools).

---

## 2. Compact table

| # | Niche (market) | Volume (Ahrefs, est.) | SERP (crowding) | Best competitor traffic | CPC tier (est.) | Trigger | Effort | Domain (.com free) | Score |
|---|---|---|---|---|---|---|---|---|---|
| C1 | HVAC/electrical field-reference hub (US) | r454b pt chart >1K Easy; long-tail 150–500 each (TC) | Generic: 8+ (fails); per-variant pages: proven #1s | intrysys 476 (US 99%) | Med-High | EPA A2L transition 2025; NEC 2026 | 10–14 d | a2lptchart.com | **6.5** |
| C2 | Commercial insurance + CRE worksheets (US) | BI worksheet >100 Easy (+30); coinsurance >100 Easy | BI: PDFs + 2 tools (passes) | dealwiseai 103 ↑; countfolk 32 | **High** | Renewal season; evergreen | 7–10 d | coveragecalcs.com | **5.5** |
| C3 | 401(k) top-heavy / ADP-ACP / ICHRA (US) | top heavy test <100 Easy (+13); ICHRA >100 Med | Top-heavy: 2–3 tools (passes) | kinetiplan 0 | **High** | Jan–Mar testing; SECURE 2.0 | 6–8 d | topheavytest.com | **5** |
| C4 | Form 2210 Schedule AI (US) | <100 Easy (+5) | PDFs/docs + ~3 tools (passes) | taxguidepro 10 | **High** | TY2026 season; OBBBA | 5–7 d | underpaymentcalc.com | **4.5** |
| C5 | Farm calibration hub: NH3, pivot (US) | <100 each | PDFs + 1–3 tools (passes) | roughlogic 0; bytes.engineer 0 | Low-Med | none (seasonal) | 6–8 d | agcalcs.com | **4.5** |
| C6 | Hospice cap (US B2B) | <100 | CMS PDFs + 2 tools (passes) | soriagacpa 4 ↑ | High | FY2027 cap 1 Oct 2026 | 3–4 d | hospicecapcalculator.com | **4** |
| C7 | UK iXBRL viewer/checker | <100 | Official + 5 viewers | accessiblefiling 0 | Med-High | **1 Apr 2027** software-only filing | 8–12 d | ixbrlcheck.com | **4** |
| C8 | Davis-Bacon fringe (US) | no data | ~6 tools | govcontractcalcs 0 | High | DBRA rule | 4–5 d | fringecalc.com | **3.5** |
| C9 | No tax on overtime (US) | **>10K Medium** | brands + swarm (fails) | — | High | TY2025–28 | 3–4 d | otdeductioncalc.com | **3** |
| C10 | 1099-DA reconciler (US) | >1K Med/Hard (806 kws) | vendors + 1 client-side tool | — | High | first basis 1099-DA early 2027 | 8–10 d | 1099dacalc.com | **3** |
| C11 | Car-loan interest VIN check (US) | >100 | 12+ (fails) | carloancheckup 0 | High | TY2025–28 | 3 d | loaninterestcheck.com | **2.5** |
| C12 | UK Renters' Rights notices | >100 | 12+ (fails) | periodictenancy 13 ↓ | Med-High | 1 May 2026 | 3 d | rentnoticecalc.com | **2.5** |
| C13 | UK MTD qualifying income | >100 | 15+ (fails) | taxquarters 0 | High | Apr 2027/28 | 2 d | mtdtest.com | **2.5** |
| C14 | AU Payday Super / Div 296 | <100 each | 15+ (fails) | — | High | 1 Jul 2026 | 2–3 d | paydaysupercalc.com | **2** |
| C15 | UK eVED / salary-sacrifice cap | no data / <100 | 10+ (fails) | — | Med-High | 2028 / 2029 | 2 d | evedcalc.com | **2** |

---

## 3. Top 3 picks and why

1. **C1: HVAC + electrical field-reference hub (US).** It is the only premium-market model where I saw a **new site grow from ~0 to ~500–1,000 US visits/month within 3–5 months** (intrysys.com, 99% US), on exactly the page type a static generator makes: one page per refrigerant, per offset angle, per conduit size, per brand serial-number decoder. The head term "r454b pt chart" is `>1K` with **KD Easy**, and the A2L transition (2025) means techs need new bubble/dew tables. Most PT-chart competitors sit at 0 or serve India. Build it as **breadth plus accuracy**: cite the source table on every page, include bubble/dew columns, add printable truck cards. *Main risk:* intrysys is ahead; accuracy errors in PT data hurt trust.
2. **C2: Commercial insurance + CRE worksheet hub (US).** It has the highest CPC tier, and the "business income worksheet" SERP is mostly **PDFs and agency blogs with only 2 tools** (countfolk 32/mo, 4calculators). It also has a programmatic set no one covers: insurer-branded worksheets (Chubb, ACORD, ISO, Travelers, Liberty Mutual) explained and calculated. dealwiseai.com shows a CRE calculator hub can reach ~100 US visits in months. Add coinsurance, TI allowance, percentage rent, CAM, and EMR as supporting pages; each of those alone is crowded, but together they build topical authority. *Main risk:* low volumes (`>100` head, the rest `<100`), so the income ceiling is set by CPC, not traffic.
3. **C3: 401(k) plan-testing toolkit (US),** with **C4 (Form 2210)** as a sister section if Yasir wants one "small-business tax & benefits compliance" domain. The top-heavy test SERP has only 2–3 real tools (kinetiplan at 0, coraa serving India) and is otherwise IRS/vendor articles. The audience (owners, TPAs, payroll) is high-CPC, and the Jan–Mar testing season lines up with a Nov–Dec build. *Main risk:* volumes are `<100` per keyword; ADP/ACP correction math must be exact.

**What to avoid:** every 2026–2029 regulation calculator in C9–C15. They fail the crowding rule today, and the tools already there (carloancheckup, taxquarters, paidleavecalc, workerscalc, ptcharts…) show 0 traffic.

## 4. Open items and limits
- Volumes are Ahrefs free buckets (US mostly; UK/AU only where noted). CA and DE were **not** volume-checked in this pass. A DE/Nordic pass would need its own swarm check (the earlier plan found `zinsen-berechnen.de`-style incumbents).
- CPC tiers are judgement, not data. Yasir can confirm with the SBMM extension or Google Keyword Planner.
- SERPs are web_search approximations, not a VPN view; positions can differ on live Google.
- Conduit-bending/fill SERPs were not searched directly; their strength is inferred from intrysys ranking #1 (Traffic Checker).
- Domain availability is a point-in-time RDAP check (13 Nov 2026).
- Proposal (not applied): add to the playbook that in US/UK/AU, single "hot regulation" tools should be skipped and the default plan should be a 60–150-page programmatic professional hub.
