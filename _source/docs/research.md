# Trade Charts — competitor audit (2026-11-13)

Sources: Ahrefs free Traffic Checker + Keyword Generator (US), notes in `/workspace/web/notes/<proj>/ahrefs-tc-trades-*` and `ahrefs-kw-trades-*`; manual review of competitor pages during data research.

## Demand (Ahrefs KW generator, US)
| Seed | Volume / KD | Notes |
|---|---|---|
| pt chart | >1K, Easy | 410a, r22, 404a, 134a, 454b, 407c, r32 each >1K; r290, 448a >100; "how to read a pt chart" |
| conduit fill chart | >10K, Easy | pvc, emt >1K; nec, sch 40, flex, 3/4 >100 |
| voltage drop calculator | >10K, Medium | southwire >1K; dc, 3 phase |
| wire ampacity chart | >1K, Medium | copper, aluminum, nec |
| offset multiplier | >100, Easy | 45/10/15/22/22.5 >100 |
| gas pipe sizing chart | >1K, Easy | natural gas, btu, 2 psi, propane |
| superheat calculator | >100 | target, per refrigerant <100 |
| water heater age | >100 | Bradford White / AO Smith / Whirlpool >1K |
| hvac age by serial number | <100 | brand variants |
| tig welding amperage chart | >100, Easy | |

## Competitors (traffic = Ahrefs estimate, organic/month)
| Site | Traffic | What they do | Gaps we beat |
|---|---|---|---|
| building-center.org | 18.3K (96% US) | Age-by-serial pages (Goodman 2.8K, Bradford White 1.6K, Carrier 1.6K, AO Smith 1.2K, Lennox 1.2K) | No live decoder on most pages, heavy ads, sources rarely linked. We add an instant decoder, per-year example table, cited manufacturer source, no ads/trackers. |
| intrysys | 476 | Generic calculators | Thin, no sources |
| hvacptcharts | 42 (mostly India) | Static PT images | Images not searchable, no dew/bubble, no °C, no lookup |
| ptcharts / refrigerantpt.com / hvactoolkit.org / mepcalcs / ownerspec / specmyhouse / howoldismyunit / ratedarc | ~0 | Various charts | New/weak; we out-scope them |
| Manufacturer apps/charts (Chemours, Honeywell, Arkema, Danfoss Ref Tools) | n/a (brand) | Authoritative PT data, one brand's refrigerants each | Apps/PDFs, no cross-brand comparison, no SEO pages per question; we combine all 32 in one fast site with verification shown |
| Southwire / Cerrowire calculators | brand | Voltage drop, conduit fill apps | App-centric; no per-size answer pages, no offset or box fill hub |

## Our differentiators (all live)
1. Every PT chart shows how it was verified (points compared, max deviation; ≤1.0 °F gate in CI).
2. Two-way P↔T lookup, °F/°C, psig/kPa/bar, vacuum in inHg, dew/bubble for blends, print view.
3. One site across HVAC, electrical, gas, age decoders, welding with internal linking between them.
4. Code table numbers on every page (NEC 310.16, Ch. 9 Tables 1/4/5/8, 314.16, IFGC 402.4(x)).
5. Static, mobile-first, dark mode, strict CSP, no trackers/ads/cookies — fast in the field.
