# Next micro-tool sites: niche plan (research 13 Nov 2026)

Owner: Yasir. Constraints: zero budget, static client-side JS, GitHub Pages + free `.dpdns.org` domain, AdSense later. Method from `work/tool-site-playbook.md`.
Status: **research only.** Nothing was built, bought or posted.

**How the numbers were gathered**
- Volumes come from the Ahrefs free Keyword Generator (per-country buckets: >10K / >1K / >100 / <100). Where a number has no bucket sign (e.g. "4K"), it is the per-keyword volume Ahrefs' free **Traffic Checker** showed for a competitor's ranking keyword. **Every volume is an estimate.**
- Competitor traffic is the Ahrefs free Traffic Checker estimate, checked 13 Nov 2026.
- Autocomplete is Google suggest (`suggestqueries.google.com`, `client=firefox`, correct `hl`/`gl`), with a–z expansion on seeds.
- SERPs come from web_search with a country filter. This is an approximation of the live local Google results (no VPN). Competitor weaknesses come from the result excerpts and pages; **I did not test any tool hands-on.**

**Raw data**
- Autocomplete: `work/niches/raw/*.json|txt`.
- BOE text extracts: `work/niches/raw/rd238.txt`, `raw/orden1028.txt`.
- Ahrefs tables, in `/workspace/web/notes/4d33c9a5-39ad-43fa-885b-d72bfcc6b372/`:
  - `ahrefs-es-tu_yixoh7o4sx3godcrsd35nprkpc/ahrefs-es-b2b.md` (Spain)
  - `ahrefs-de-tu_kflnlkxku2wuqajubvzlirugvn/ahrefs-de.md` (Germany)
  - `ahrefs-befr-tu_5yumkdb6xe7bd3lx5lwsjqwypy/ahrefs-be-fr.md` (Belgium/France)
  - `ahrefs-rohr-tu_zt7ds3klkbpemecqzi67pxslgd/ahrefs-ro-hr.md` (Romania/Croatia)
  - `ahrefs-plgr-tu_gmzdaivr2by525zkeozxkvb3cu/ahrefs-pl-gr-it-sk.md` (Poland/Greece/Italy/Slovakia)
  - `ahrefs-befr-tu_n7it3jugcgvqtqo5ouawqbece5/ahrefs-batch2-a.md`
  - `ahrefs-plgr-tu_7ffo5a7j6sepncxawufarygcyr/ahrefs-batch2-b.md`
  - `ahrefs-rohr-tu_s5rlqnbirkyxraimuanwfgj3g7/ahrefs-batch2-c.md`
  - `ahrefs-es-tu_ftq33w2g2l3pn54plwcwulhdcq/ahrefs-batch3.md`
  - `ahrefs-plgr-tu_7nkboa4a76p5rc7citjde4gueu/ahrefs-batch4.md`
  - Traffic checks: `ahrefs-de-tu_lhks626y4r7wozltyt3dfuzv6z/ahrefs-traffic-batch.md` and `ahrefs-rohr-tu_4hj6zmflhufcwdkz5pyaftcfnr/ahrefs-traffic-batch2.md`

---

## 0. The big finding: the playbook needs a "swarm check"

The Verifactu lesson repeats in every niche tested. **By November 2026, every EU e-invoicing and finance-calculator niche I checked already has 8 to 17 free, single-purpose, client-side tool pages.** They are usually AI-built and multi-language, and many are vendor lead magnets. Most of the new ones get **zero** organic traffic in Ahrefs:

| New-ish tool site | Niche | Ahrefs organic/mo |
|---|---|---|
| verifactuhoy.com | ES Verifactu + B2B checker | 0 |
| facturaobligatoria.es | ES B2B "¿me afecta?" | 0 |
| factulupa.es | ES Verifactu | 0 |
| einvoicechecker.com | multi-country validator | 0 |
| pagamemoroso.com | ES late-interest calc | 0 |
| efacturaspv.ro | RO XML→PDF | 0 |
| usezivo.com | multi-tool, many languages | 0 |
| ksefnarzedzia.pl | PL KSeF (competitor of site 1) | 0 |
| mojauplatnica.com.hr | HR HUB3/OIB | 82 (rising) |
| kalkulatorvat.pl | PL VAT-limit calc | 139 (rising Jul→Oct) |
| peppol-id.eu | Peppol ID lookup | 291 |

The pages that do earn traffic are **old or authority domains**:
- zinsen-berechnen.de: 217K/mo
- qr-platba.cz: 6.1K
- fiskalopedija.hr: 2.4K
- e-invoice.be: 1.5K, down from about 3.8K at the Belgian mandate peak

They are also **guide + tool hubs**, not single tools. For example, fiskalopedija ranks #1 for "paušalni obrt" (4.8K) and "fiskalizacija 2.0" (4.9K) with guide pages.

**What this means for Yasir**
1. "Tool volume small and SERP shows other tools" is no longer enough. Add a **swarm check** to step 4 of the playbook: count the dedicated free tools on page 1–2, and run 3 of them through the Traffic Checker. If there are ≥8 and most show 0, a new domain will probably also sit at 0 for months.
2. **Fewer, deeper sites beat more micro-domains.** Grow site 1 (Polish) and site 2 (Spanish) into country hubs, where every new tool adds topical authority to a domain that is already ageing. Start a new domain only for a new country or language.
3. The only near-empty SERP I found is a **boring accounting calculation** (Spanish *periodo medio de pago a proveedores*, §A.4). It is not a hot mandate keyword. Look for more like it: official formula, PDF/BOE-dominated results, 1–2 tools at most.

---

## A. Spain: mandatory B2B e-invoicing (Ley Crea y Crece, RD 238/2026)

### A.1 Legal facts (verified on the BOE and AEAT, 13 Nov 2026)

| Fact | Source |
|---|---|
| **Ley 18/2022 (Crea y Crece)**, DF 8ª: B2B e-invoicing obligation, deferred until regulatory development | referenced in RD 238/2026 and the Orden text |
| **Real Decreto 238/2026, de 25 de marzo**: BOE núm. 79, 31/03/2026, BOE-A-2026-7295. In force 20 days after publication, but effective application is **deferred** (DF 4ª.1): **(a) 12 months** after the Orden enters into force for businesses with volumen de operaciones **> €8M** in the prior year; **(b) 24 months** for everyone else | https://www.boe.es/diario_boe/txt.php?id=BOE-A-2026-7295 · consolidated: https://www.boe.es/buscar/act.php?id=BOE-A-2026-7295 |
| **Orden HAC/1028/2026, de 2 de octubre** (regulates the Solución Pública de Facturación Electrónica, SPFE): BOE núm. 247, **05/10/2026**, BOE-A-2026-20587, in force the next day, **06/10/2026** | https://www.boe.es/buscar/act.php?id=BOE-A-2026-20587 · PDF: https://www.boe.es/buscar/pdf/2026/BOE-A-2026-20587-consolidado.pdf |
| Resulting dates: **6 Oct 2027** (>€8M) and **6 Oct 2028** (rest). The BOE gives the periods as relative months; the AEAT states these calendar dates explicitly | AEAT calendar: https://sede.agenciatributaria.gob.es/Sede/iva/factura-electronica/calendario-implantacion.html · AEAT news 07/10/2026: https://sede.agenciatributaria.gob.es/Sede/todas-noticias/2026/octubre/7/solucion-publica-facturacion-electronica.html |
| Art. 7: EN 16931 semantic model, in one of **CII, UBL, EDIFACT or Facturae** syntaxes. Private platforms must convert between all of them, and invoices sent through them must carry an advanced e-signature | RD 238/2026 art. 7 |
| Art. 11.2: the **SPFE uses UBL**. Anyone who doesn't issue through the SPFE must send it a **"copia fiel" in UBL**, simultaneously with issuance | RD art. 11; Orden HAC/1028/2026 |
| Art. 4: **simplified invoices are excepted** (unless *cualificadas*) | RD art. 4 |
| Art. 12: the recipient must report **full payment (and date) or rejection**, plus the **due date**, within **4 natural days excluding Saturdays, Sundays and national holidays**. Other invoice statuses (partial rejection, partial payment, assignment) follow the same 4-day rule | RD art. 12 (and art. 10 for statuses) |
| DT 2ª: for its first 12 months, the >€8M group must **attach a legible PDF** to each e-invoice | RD DT 2ª |
| DT 3ª: natural persons/atribución de rentas with ≤€8M get **up to 12 more months** for status/payment reporting, i.e. **6 Oct 2029** (my calculation, also stated by secondary sources) | RD DT 3ª |
| Art. 15: the payment term follows **art. 4 Ley 3/2004** (morosidad). If the invoice has no operation date, the term starts at the issue date | RD art. 15 |
| Orden art. 6: **código único** of an invoice = concatenation of **issuer NIF + series and number + issue date** (format in anexo I). Art. 7: the recipient reports rejection, full-payment date and **fecha de vencimiento** | Orden HAC/1028/2026 |
| AEAT will not publish a production validation service; senders must validate XSD + Schematron themselves (secondary source, **not verified on the AEAT**) | e-invoice.app blog 10/06/2026 |

### A.2 Keywords (Google ES autocomplete, hl=es gl=es; Ahrefs ES)

| Cluster | Autocomplete phrases seen | Ahrefs ES (estimate) |
|---|---|---|
| Dates / am I obliged | factura electronica obligatoria cuando / desde cuando / fecha / plazos / para quien / pymes / autonomos / excepciones / requisitos; factura electronica octubre 2027; factura electronica 2028; calendario ley crea y crece | "factura electrónica obligatoria" >100 (KD Easy); "factura electronica obligatoria" >100 (Hard); "…aeat" >100; "…2026" >100; ~69 phrase-match variants, mostly <100 |
| Ley Crea y Crece | ley crea y crece factura electronica / entrada en vigor / reglamento / boe | "ley crea y crece" **>1K** (Medium); "…factura electrónica" >100 Easy; "reglamento…" >100; "…boe" >100; "entrada en vigor…" >100 |
| Facturae | facturae descargar / online / validar / visor / xml a pdf / vs ubl / b2b | "facturae" **>1K** Easy, but navigational (download the official app: "facturae descargar" >1K, "mi facturae" >1K); "validar facturae" >100 Easy; "visor facturae" <100 |
| XML / UBL viewer | abrir factura xml (online), factura electronica xml a pdf, factura ubl ejemplo, formato ubl factura electronica | "factura electronica xml" <100; viewer/validar/abrir variants all <100 |
| **Periodo medio de pago** (PMP) | calcular periodo medio de pago a proveedores; cálculo PMP memoria abreviada / memoria normal; PMP excel; fórmula PMP; cómo calcular PMP ejemplo; boicac / icac periodo medio de pago; incumplimiento PMP | "periodo medio de pago a proveedores" >100 Easy; 175 phrase-match keywords, the rest <100 (Easy) |
| Morosidad / late interest | ley de morosidad; plazo de pago ley de morosidad; calcular fecha vencimiento factura; intereses de demora | "ley de morosidad" >100 Easy; "intereses de demora" **>1K** Easy; "calculadora intereses de demora" >100; "fecha de vencimiento factura" <100 |

### A.3 Who ranks, and the gaps

| Query family | Ranking now | Gap |
|---|---|---|
| "factura electrónica obligatoria cuándo / 2027 / 2028" | AEAT calendar page; pluginloom.com guide; facturaobligatoria.es (3-question checker + calendar, **0 traffic**); ininvoice.com calendar + "test"; muaytax (one table says "1 de octubre de 2027", which is wrong); onemoneyway; contextualdocs; cleartax; rankia | Crowded with near-identical "dates + checker" pages. The only real gaps are accuracy (DT 3ª's 2029 payment-reporting date is often missing or garbled) and print/export of a personal compliance plan |
| B2B checker + 4-day calculator | verifactuhoy.com (turnover checker **and** "status & payment 4-day calculator" already live, **0 traffic**); angelortegacastro.com (B2B date checker); ininvoice test | My planned "¿cuándo me obliga?" and 4-day deadline tools already exist. Differentiators would be the national-holiday calendar for 2027–2029 shown day by day, a bulk CSV of payment dates, and .ics export |
| UBL / SPFE validation | tembrica.com (in-browser EN 16931/Peppol/XRechnung rules), aidoks, einvoicechecker, validatefin; e-invoicing.org and eu-einvoicing.com explainers | **No dedicated "copia fiel UBL SPFE" validator yet**, but the Orden's anexo I rules aren't published as Schematron; building them by hand is risky. The multi-format validators will add Spain-SPFE as soon as the AEAT publishes artefacts |
| Facturae viewer / validator | aidoks.eu, einvoicechecker.com, facturaview.es, validatefin, viewer.facturadirecta.com (old, beta, up to 3.2.1), virtualges, glosa-e.com, verifactuhoy "abrir facturae", the official FACe validator, mifacturae.face.gob.es | Saturated (10+) |
| **Periodo medio de pago** | **ICAC/BOE PDFs dominate** (BOICAC 146/2026 consulta 2 published 24/09/2026; Resolución ICAC 29/01/2016 on the BOE), supercontable, ineaf, asesor-contable, economistas.es PDF, an ERP help-desk page; **only 2 calculators**: cambiarerp.com (proper ICAC method, paste rows) and fube.es (uses a DSO-style formula, which is **not** the ICAC method) | **The weakest SERP in this whole study.** Gap: an ICAC-exact PMP calculator with CSV/Excel upload, separate memoria normal/abreviada outputs, the Ley 18/2022 extra disclosures (number/amount and % of invoices paid within the legal term), and a printable "nota de la memoria" table |
| Intereses de demora | i24app, eurocompta, openmercantil, lawactive, bataneroabogados, pagamemoroso (0), saldia, kobrux, derechoabogados, fetchdue, legalpilot, AEAT calculator | Saturated (12+) |

### A.4 Client-side tool pages that could work (best first)

All are static JS, need no API, and are in Spanish.

1. **Calculadora del periodo medio de pago a proveedores (método ICAC).** Paste or upload invoices and payments (CSV/XLSX via SheetJS). It outputs PMP, the paid and pending ratios, and the Ley 18/2022 counts and %. It prints the memoria normal / abreviada table and has an Excel template download. *Golden SERP and evergreen, seasonal around cuentas anuales (Mar–Jul).* It ties to B2B e-invoicing, because RD 238 art. 14 feeds the payment data to the morosidad observatory.
2. **Plazo de pago y fecha de vencimiento (Ley 3/2004 art. 4).** Inputs: delivery/receipt date, agreed days (default 30, max 60), acceptance procedure. Outputs: the due date, whether the term is legal, and the date to report in the SPFE. The page should also link to (3) and (4).
3. **Calculadora de plazo de 4 días (estados y pago, art. 10/12 RD 238/2026).** Excludes Saturdays, Sundays and national holidays; covers 2027–2030; bulk CSV; .ics export. (Already exists at verifactuhoy, so it only works as a supporting page.)
4. **Intereses de demora + 40 € (Ley 3/2004), multi-invoice, with a downloadable reclamación letter.** Saturated, so treat it as a supporting page for internal links.
5. **"¿Cuándo me obliga la factura electrónica?"** One question-flow covering emisión, recepción, PDF transition, estados/pago (2027 / 2028 / 2029), and Verifactu's BOE vs announced dates. Exports a personal timeline. (Commodity, but it is the head page for the >1K "ley crea y crece" cluster.)
6. **Código único de factura generator/checker (Orden art. 6).** Low volume, but nobody has it. **Build only once anexo I's exact format is confirmed** from the Orden PDF; I did not extract the exact concatenation rules.
7. Later: **UBL "copia fiel" pre-check against Orden anexo I** (mandatory fields, BT mapping). Wait for official AEAT artefacts.

### A.5 Verdict on Spain B2B

- **As a separate new domain: 4/10.** It follows the Verifactu pattern: a dozen identical checkers already exist (all at 0 traffic), and the volume sits in informational/news queries owned by the AEAT, media and vendors.
- **As a section of site 2 (Verifactu toolkit): 7/10.** Same audience, same language, and the dates rise toward 6 Oct 2027 / 2028, so it grows one Spanish hub instead of two thin ones.
- **Lead with the PMP calculator.** It is the one genuinely weak SERP found.

---

## B. Ranked shortlist: other niches

Score (1–10) = demand + SERP weakness + client-side feasibility + trend, with a heavy penalty for the "swarm".

| # | Niche (market) | Exact local keywords (autocomplete) | Volume (Ahrefs est.) | Top 3 ranking now → weaknesses | SERP difficulty | Client-side free? | Trend (dated facts) | Score |
|---|---|---|---|---|---|---|---|---|
| 1 | **ES PMP calculator** (Spain) | calcular periodo medio de pago a proveedores; cálculo PMP memoria abreviada / normal; PMP excel; fórmula PMP | "periodo medio de pago a proveedores" >100 Easy; 175 variants <100 | ICAC BOICAC 146/2026 PDF; BOE Resolución ICAC 2016; cambiarerp.com calculator → PDFs have no tool; cambiarerp is an ERP-sales blog with a paste box only; fube.es uses the wrong formula | **Easy** (PDFs + gov + blogs) | Yes | Evergreen and seasonal; new ICAC consultas Jan and Sep 2026; RD 238/2026 art. 14 adds payment-term monitoring | **7** (low volume) |
| 2 | **HR KPD 2025 code finder + per-code pages** (Croatia) | kpd 2025 tražilica; kpd šifre; kpd brojevi 2026; kpd najam prostora; kpd građevinske usluge; kpd dostava robe; kpd klasifikacija pdf/excel | "kpd" >100; "kpd pretraživač" >100; "kpd klasifikacija pdf" >100; 278 variants | mojafirma.hr (5,828 codes, single search page); fiskalapi.hr; kpd.informacija.hr → all single-page search UIs. I saw no indexable per-code/per-activity pages (**not fully verified**). kpdinfo is AI and paid | Medium (8+ tools, but thin pages) | Yes (static JSON from DZS KLASUS) | **Rising:** KPD is mandatory on every eRačun line from 1 Jan 2026; non-VAT issuers must issue eRačun from 1 Jan 2027; **KPD 2025 amendments take effect 1 Jan 2027** (porezna.gov.hr) | **6** |
| 3 | **PL VAT white-list bulk checker** (Poland; fits the KSeF site) | biała lista vat sprawdź; wyszukiwarka; masowe sprawdzanie; nip biała lista | "biała lista vat" **>10K** Easy (mostly navigational); "…wyszukiwarka" >1K | podatki.gov.pl (official); nipscan.pl (30 NIP); skanfirmy.pl/bulk (3,000/day) → official site does one at a time; nipscan caps at 30; paid tools (listapodatnikow, nip.waw.pl, vatchecker) gate bulk | Medium-hard (gov + swarm) | **Yes: MF API sends `access-control-allow-origin: *`** (tested 13 Nov 2026); per-IP daily limits | Evergreen since 2019 (15,000 zł payment rule); pairs with KSeF and MPP from 2027 | **5** as a numerksef section, 3 as a new domain |
| 4 | **PT invoice QR / ATCUD reader + SAF-T viewer** (Portugal) | atcud validar / verificar / leitor; ler qr code fatura; validar fatura qr code; saft xml validator; saft online | "atcud" **>1K** Easy; "saft" **>1K** Easy (mostly "enviar saft" navigational); "qr code fatura" <100 | fqrdecoder.pt; eurocompta.eu; faturiza.com (also klarbon, base64encoding, appa8; safts.pt for SAF-T) → mostly single pages on multi-tool sites; no bulk PDF→Excel of many invoices except afatura.pt | Medium (≈7 tools) | Yes (jsQR + pdf.js; SAF-T XML parse) | QES on PDF invoices from **1 Jan 2027**; SAF-T submission delayed to **2028** (e-invoicing.org, secondary) | **5** |
| 5 | **PL limit VAT 2026/2027 + mały podatnik** (Poland) | limit vat 2026; kalkulator limitu vat; limit do vat kalkulator; czy limit vat jest proporcjonalny | "limit vat 2026" **>1K** Easy; "limit do vat kalkulator" 700, "kalkulator limitu vat" 600, "limit vat kalkulator" 400 | kalkulatorvat.pl (new, rising, ranks #2–#10); finwire.pl; infakt.pl → 15+ near-identical calculators | Hard-ish (swarm, yet a new site is rising) | Yes | Spike: limit rose from 200,000 to **240,000 zł on 1 Jan 2026** (Dz.U. 2025 poz. 896); will fade in 2027 | **4** (as a numerksef page: 6) |
| 6 | **RO e-Factura XML→PDF / viewer** (Romania) | transformare xml in pdf (anaf / e factura); xml to pdf anaf; vizualizare e factura; validare e-factura | "transformare xml in pdf" **>1K** Easy; "xml to pdf anaf" >100; viewer/validator <100 | anaf.ro/uploadxml and mfinante (official, flaky, Firefox-only per orbis.ro); efacturaspv.ro (0 traffic; uses the ANAF service); instafactura.ro → official tools are clunky; most third-party tools are server-side | Medium (official + ~6 tools) | Yes (render UBL CIUS-RO in browser, print to PDF) | Mandate live since 2024; from Jan 2026 a unified 5-working-day deadline for B2B/B2C (GEO 89/2025, secondary); flat/steady | **4** |
| 7 | **HR eRačun viewer + HUB3 from eRačun / OIB / uplatnica** (Croatia) | pregled e računa; e račun xml u pdf; generator barkod uplatnica; oib provjera / generator; opća uplatnica | "oib" >1K; "oib generator" 500; "uplatnica" 700; "provjera oib" 300 | eracun.info; fiskai.hr; einvoicechecker.com/hr (viewers); mojauplatnica, fiskalopedija, unitime (HUB3) → 10+ each | Hard (swarm) | Yes | Rising: Fiskalizacija 2.0 since 1 Jan 2026; non-VAT issuers from 1 Jan 2027 | **4** (bundle with #2) |
| 8 | **Late-payment interest, multi-language** (ES/IT/FR) | calcular intereses de demora; calcolo interessi di mora; calcul pénalités de retard | ES "intereses de demora" >1K; IT "calcolo interessi di mora" >1K (Semrush shows "calcolo interessi moratori" 14.8K for sibill.com, 3rd-party estimate); FR "pénalités de retard" >100 | ES: i24app, eurocompta, openmercantil; IT: professionegiustizia, trovanorma, sibill; FR: not checked → 12+ per language | Hard | Yes (BCE + 8 pts semestral table) | Evergreen; rates update every 6 months | **4** (i18n add-on to site 2, not its own site) |
| 9 | **SK e-faktúra 2027 toolkit** (Slovakia) | e faktura xml; efaktura validator; peppol id slovensko; prevod na iban; pay by square | "e faktúra" >100; "e faktúra 2027" >100; "peppol slovensko" >100; "pay by square" >100 | efakturacentrum.sk; epostari.sk; efaktura.tools (also verteco, cpds.sk, efakturuj, 1faktura) → 10+ already, mostly vendor lead magnets | Hard (swarm) | Yes (Peppol Directory has a public API; CORS not verified) | Mandate **1 Jan 2027** (Act 385/2025, secondary); will peak Dec 2026–Mar 2027 | **3** |
| 10 | **CZ QR platba / SK Pay by square generator** | qr platba generátor; platba qr kódem; pay by square qr generator / decoder | CZ "qr platba" >1K; "qr platba generátor" >100 (200); "platba qr kódem" 1.9K | qr-platba.cz (6.1K/mo, the standard's own site); qrgenerator.cz; doklad.ai → plus 8+ more | Hard | Yes | Evergreen | **3** |
| 11 | **GR VAT (ΦΠΑ) calculator / αποφορολόγηση** | υπολογισμος φπα (online / απο τελικο ποσο); αποφορολόγηση φπα | "υπολογισμος φπα" >1K Easy; "αποφορολόγηση φπα" 700 | timologic.gr; helppost.gr; ypologismosfpa.gr (556/mo) → 12+ calculators | Hard | Yes | Evergreen; Greek B2B e-invoicing phase B from 1 Oct 2026 (secondary) | **3** |
| 12 | **BE Peppol ID lookup + OGM generator** | peppol id opzoeken; check peppol id; gestructureerde mededeling berekenen | "peppol id opzoeken" 4K / >1K; "peppol id" >1K; "gestructureerde mededeling" >100 | e-invoice.be (1.5K/mo, falling from ~3.8K); peppol-id.eu; factuursimpel.be → 15+ lookups and 10+ OGM tools | Hard | Partly (Peppol Directory API; CORS not verified) | **Fading**: mandate went live 1 Jan 2026, peak passed | **3** |
| 13 | **DE ZUGFeRD/XRechnung validator/viewer** | zugferd validator (online kostenlos); xrechnung viewer; xrechnung in pdf umwandeln; leitweg-id prüfen | "zugferd validator" >1K Easy; "xrechnung viewer" >100; "e-rechnung prüfen" >100; "leitweg-id" >100 | zugferd-validator.de; erechnungs-validator.de (314K checks); getzugferd.com → 15+, most run the official KoSIT validator server-side | Hard | Partly (full Schematron in browser is heavy: SaxonJS) | Rising toward issuance from **1 Jan 2027** (>€800K turnover) and **1 Jan 2028** (all) | **3** |
| 14 | **DE Verzugszinsen / PL kalkulator odsetek** | verzugszinsen berechnen; kalkulator odsetek ustawowych (za opóźnienie w transakcjach handlowych) | DE **>10K** Easy; PL **>10K** Easy | DE: zinsen-berechnen.de (217K/mo), finanzfluss, jura-rechner; PL: biznes-mapa, kalkulatorvat, e-gotowka (+ fakturownia, gofin) → strong, entrenched | Very hard | Yes | Evergreen | **2–3** |
| 15 | **ES calcular IBAN / PL generator PESEL / OIB generator** | calcular iban (cuenta / santander / bbva); generator pesel; oib generator | ES >1K; PL "generator pesel" >1K; HR "oib generator" 500 | Banks (Santander, BBVA, Unicaja, Bankinter), financlick, qonto; PESEL: peselator, testerzy, calculla | Very hard | Yes | Evergreen | **2** |

Not shortlisted:
- **FR "annuaire facturation électronique"**: >1K, but a lookup needs the PPF directory API. I did not verify whether it is open or CORS-enabled, and SERP saturation was not checked.
- **HU "e számla"**: >1K, but Hard and navigational (NAV/telco logins).
- **PL "kalkulator dni roboczych"**: >1K Easy, SERP not checked beyond multi-tool sites like szeruj.pl.
- **Lithuania/Latvia**: autocomplete was almost empty.

---

## C. Recommended build order (next 3)

1. **Site 2 expansion: a Spanish "factura electrónica B2B + morosidad" section on the Verifactu site, not a new domain.** Lead with the ICAC-exact **PMP calculator** (the only golden SERP found). Then add the Ley 3/2004 due-date tool, the 4-day status/payment deadline calculator, intereses de demora + 40 €, and one "¿cuándo me obliga?" page with BOE-sourced dates (6 Oct 2027 / 2028 / 2029). *Reason:* rising demand to Oct 2027, same audience and language, and every page strengthens one Spanish domain.
2. **Site 3 (new free domain, build in Nov–Dec 2026): Croatian "KPD 2025 + eRačun" hub.**
   - A KPD search over the DZS list, plus **indexable per-activity/per-code pages** that quote Porezna's "pitanja iz prakse" answers.
   - A 2027 KPD-changes table.
   - An eRačun XML viewer → print, with a HUB3 barcode built from the XML.
   - *Reason:* a hard deadline on **1 Jan 2027** (KPD amendments + non-VAT issuers start issuing), plus a programmatic long-tail gap. Croatian CPMs are low, so expect modest AdSense.
3. **Site 1 expansion (numerksef.dpdns.org): Polish accountant tools.** Add a **VAT white-list bulk checker** (MF API, CORS open), a **limit VAT 2026/2027** page, and a **nota odsetkowa** (interest note) generator with transakcje handlowe interest.
   - *Reason:* high-volume Polish queries with the same audience as the KSeF tool. Extending the existing domain avoids another zero-authority start and gives internal links.
   - *Alternative if he insists on a third new domain:* Portugal ATCUD/QR + SAF-T reader (#4), triggered by QES on PDF invoices from 1 Jan 2027.

Before building anything new: run the **swarm check** (§0) on the exact page-1 tools and treat "≥8 tools, most at 0 traffic" as a stop sign for a new domain.

---

## Open items and limits

- SERPs are web_search approximations, not a VPN view of each country's Google.
- KD is Ahrefs' label only.
- Volumes are buckets. A few exact numbers come from the Traffic Checker's per-keyword volumes.
- Not verified:
  - CORS on the Peppol Directory and on the French PPF annuaire.
  - The exact código único format (Orden anexo I).
  - Whether any Croatian KPD site already has per-code pages.
  - Dates for Germany, France, Belgium, Greece, Slovakia, Romania and Portugal come from e-invoicing.org (a secondary source, fetched 13 Nov 2026), not from each official gazette.
- Proposal: add the swarm check (§0) to `micro-tool-website-playbook` as part of step 4. I have not edited the skill.
