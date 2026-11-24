# Trade Charts — project notes

- Site: https://mydevspace2.github.io/trade-charts/ (repo mydevspace2/trade-charts, Pages main/root). Base URL configurable (TC_SITE_URL/TC_BASE/TC_CNAME).
- Generator: `work/trades/build/` (python3 build.py → `work/trades/out/`), tests in `work/trades/qa/`, deploy copy in `work/trades/repo/` via `sync-repo.sh`.
- Browser tests: NODE_PATH=work/verifactu/.tools/node_modules PLAYWRIGHT_BROWSERS_PATH=work/verifactu/.tools/browsers node qa/test-browser.js
  (sandbox needed `sudo apt-get install libatk1.0-0 libatk-bridge2.0-0 libcups2 libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libnss3 libxfixes3`).
- Push: `git push` and the Git Data API both return 403 "Resource not accessible by integration" for trade-charts — the Hark GitHub app is not installed on this new repo (works for herramientas-verifactu). Fix: Configure GitHub → add trade-charts. Then run `python3 api_push.py repo "<msg>"` or `git push` from `repo/`.
- GSC: URL-prefix property added in browser session "google-gsc"; HTML tag token PBIzVZ_WTR9JENZ2TnCvFsTs3YWHua2ZJY0Cq2uO-6k is on the home page; VERIFY not clicked yet (needs deploy first). Then submit sitemap, import into Bing Webmaster.
- IndexNow key: 7f3c1e9a2b8d4f60a1c5e7b9d3f2a4c6 (file at site root). Optional workflow: `ci/indexnow.yml` (copy to .github/workflows; needs workflow scope).

## Data decisions
- 32 refrigerants published; all pass ≤1.0 °F vs ≥1 published chart (see build/data/verification.json).
- Excluded: R-454C (CoolProp off by 1.26 °F vs Hudson/ASHRAE), R-452B, R-502 (not verified), R-408A/409A/401A/402A/414B/424A (not in CoolProp; no chart transcribed), R-463A (CoolProp glitch).
- R-438A from DuPont MO99 chart (interpolated to °F grid); R-466A verified only on 3 Honeywell points (thin but within 0.12 °F).
- Electrical: NEC 2017 Ch. 9 text (same values 2020/2023), 310.16 from NFPA TIA 1691 (NEC 2023), 314.16 from Steel City catalog reprint.
- Gas: 12 IFGC 2021 tables (Seattle chapter 4 text; 402.4(2) cross-checked with ICC CodeNotes). Copper tubing tables not parsed (different header) – skipped.
- Age decoders: 9 water-heater + 5 HVAC brand families with cited formats. Skipped Rinnai, Navien, York (no published format found).
- Skipped: breaker interchange (needs UL classified-component listings per panel; no reliable free source), small-engine age (not verified this session), welding machine door-chart pages (manual transcription per machine; deferred).

## Suggested (not created) scheduled tasks
- Monthly: GSC/Bing coverage + CTR review and data-correction inbox check.
- Weekly for 15 weeks: publish 2 posts from blog-calendar.md.
- Yearly: re-verify serial-format sources and code-cycle tables.

## Daily build-out task (scheduled, "Trade Charts: 10-day completion, then daily management")
- Method is in the task runbook. New posts, FAQs for all posts, launch-post expansions and RELATED_GUIDES (tool page → guide links) live in build/posts2.py.
- 2026-11-13 run: posts #7 R-454B service basics, #8 A2L tools, #9 temperature glide live (commit e0ae994/0d7b8fd); 5 launch posts expanded to 600+ words; FAQ + FAQPage schema on all 9 posts; related-guide links on 18 tool pages. 138 pages. Still under 600 words: ~43 pages (calculators, conduit-size, ampacity, offset, hubs, Home, legal).
- Other agents also commit to repo/ (AI-HANDOVER.md, _source/docs via sync-repo.sh). Pull before syncing; check the commit for unexpected deletions.

## UX pass (2026-11-13, from work/ux-audit/report.md)
- Home hero cut to H1 + one line; the 3 big buttons became one row of small chips; the long intro paragraph moved below the Quick PT lookup.
- Every tool: live results kept, plus a Calculate button (Enter/Go runs it, blurs the keyboard, scrolls the result into view), Copy result and Reset.
  Markup is injected in `core.page()` (TOOL_UI replaces the `<output class="res" data-out>` tag); wiring in `app.js` (each tool sets `root._run`; fill/box have `_reset`/`_after`).
- Share (navigator.share, else copies a link) on PT chart, home/hub PT lookup, superheat and subcooling. Links carry values: `?m=p2t&v=118.8&tu=F&pu=psig` (PT), `?ref=r410a&p=118&t=60&pu=psig&tu=F` (SH/SC); pages read them on load. Print chart kept on PT pages.
- Light/dark toggle in the header: `assets/theme.js` (external, loaded in head before CSS; CSP stays script-src 'self') applies the saved choice (localStorage `tc.theme`), default follows the OS. CSS: `html[data-theme=dark]` + `@media (prefers-color-scheme:dark){html:not([data-theme=light])}`.
- Light accent #d9480f -> #b8430b (links 4.84:1 on bg, white on button 5.46:1). Header/logo orange uses `--accent-hd:#ff7a3d` (7.3:1 on the dark header). Placeholder #aeb6c0. Dark accent unchanged (#ff7a3d, 6.4:1+).
- Tap targets >= 44px (nav, crumbs, chips, link grids, footer links, search, menu, toggle); search input 16px; footer fine print 14px. ASSET_V=2.
- New test `qa/test-fold.js` (375x812 first-screen + no sideways scroll after Calculate); `test-browser.js` gained UX checks and TC_SLICE / TC_NOPAGES split (sandbox 120 s limit).

## Run 2026-11-16 (Mon)
- Posts #16-18 live (posts5.py): derating, detached garage subpanel, box fill. 147 pages. Expanded 8 ampacity pages, 4 PVC fill pages, 2 in. EMT page to 600+ via extra.py. ~22 pages still under 600 (hubs, offset chart, welding, age hubs, legal, Home).
- Browser tests: install libs with `sudo apt-get update` first; run in slices (TC_SLICE=0:50, 50:100, 100:150, then TC_NOPAGES=1).
- GSC (Mon check): 0 impressions/clicks; Indexing 1 indexed/0 not; sitemap shows "Couldn't fetch" (submitted Nov 13, read empty) - Bing sitemap Success 133 URLs.

## Visual identity redesign (2026-11-16, commit dbee137)
- Job-site look: charcoal header (#1c232a, 3px safety-yellow #ffc20e rule), hex-nut + pressure-gauge logo (`core.MARK_SVG`, also favicon/icons/og via build.py), "TRADE CHARTS" wordmark.
- Headings/nav/buttons in Barlow Condensed (SIL OFL, self-hosted Latin-subset woff2 in `build/assets/fonts/`, copied by build.py; TTF for the OG image in `build/fonts-src/`). Body stays system sans, numbers mono.
- Home hero is a full-width band: `page(..., hero=...)` renders it at the top of `<main class="has-hero">` with the page content in an inner `.wrap`. Blueprint grid + hazard stripe; chips PT charts / Conduit fill / Ampacity / Box fill / Gas pipe sizing. Decorative gauge on >700px.
- Tokens: `--cta`/`--cta-ink` (yellow buttons, pressed segs, first chip), `--accent` = link colour (light #8a4f00, dark #ffc20e), `--slate` (hero/card headers), `--hazard` stripe. Light bg #f0f1ee, dark bg #111519 (test-browser.js asserts these). ASSET_V=3.
- Tool boxes: yellow top bar + diamond-bullet uppercase title; results have yellow left rule; category cards have charcoal title strips; footer/disclaimer use the hazard stripe.

## Run 2026-11-17
- Posts #19,20,23 live (posts6.py, commit 83a220e), 150 pages. Posts are ~600-900 words (short of 900 target). No page expansions this run; 23 pages still under 600 words. Browser tests need apt libs installed first (see 11-16 note).

## SEO settings pass (2026-11-17 evening, commit 1162cb5; Action lastmod commit a2c1749)
- theme-color now single #1c232a (was #14202b/#f4f1ea); hreflang en-us + x-default on indexable pages; title fix "American Water Heater Age…" (word was doubled); how-to-read-a-pt-chart desc <160. Audit clean otherwise (canonical, 1 H1, OG/Twitter, JSON-LD, alts, no orphans/broken links, 404 noindex). 8 titles are 66-69 chars (left as is).
- GSC sitemap still "Couldn't fetch" after resubmit 17 Nov, but URL Inspection live test of sitemap.xml = 200 OK, application/xml, crawl allowed: file is fine, GSC-side lag on github.io sub-folder properties. Request Indexing: /conduit-fill-calculator/ accepted; /pt-chart/ and /r410a-pt-chart/ "Oops! Something went wrong" (retry another day). Bing sitemap resubmitted (Processing). IndexNow 148 URLs HTTP 200 (Bing dashboard for the sub-folder property shows no IndexNow data).

## Run 2026-11-19
- Posts #25,26,27 live (build/posts8.py): how-old-is-my-ac-unit-serial-number, bradford-white-serial-number-year-letter-code, r22-systems-repair-retrofit-or-replace. 156 pages. (Run 11-18 posts 21,22,24 are in posts7.py.)
- Expanded to 600+ words via extra.py (_run1119/_run1119b): conduit-fill-calculator, 2-emt-conduit-fill, target-superheat-calculator, conduit-offset-multiplier-chart, electrical hub, hvac-calculators, 4 PVC fill pages, saddles post, r513a-vs-r134a. Still under 600: water-heater-age, hvac-age-by-serial-number, age-by-serial-number hubs, mig/tig/welding pages, Home, About, Contact, Privacy, Terms.
- SEO: RELATED_GUIDES from age/serial pages, R-22/R-407C/R-422D/R-438A charts to the new posts.
- TO VERIFY: the Trane HVAC age page claims residential serials start YYWW but cites only the Trane *light commercial* help page; HVACBase (Nov 2026) says Trane/Goodman/Carrier do not publish a residential format (fits to CPSC recalls only). Post #25 hedges this; consider softening /trane-age-by-serial-number/ and /carrier-age-by-serial-number/ wording.
- Browser tests need apt libs: sudo apt-get update && install (see 11-16 note); run slices 0:55, 55:110, 110:160, then TC_NOPAGES=1.

## Run 2026-11-21
- Posts #28-30 live (build/posts9.py, commit f26c0db): all 30 calendar posts now published. 159 pages. Expanded welding hub, MIG calc, TIG chart via extra.py (_run1121). Still under 600: water-heater-age, hvac-age-by-serial-number, age-by-serial-number hubs, Home, About, Contact, Privacy, Terms. Next runs: expand those; Phase 2 posts need new topics from Google autocomplete.

## Run 2026-11-22
- Calendar exhausted (30/30), no new posts (need Google-autocomplete topics + sourced research). Expanded water-heater-age, hvac-age-by-serial-number, age-by-serial-number, TIG chart via extra.py _run1122 (still 429-494 words). Still under 600: welding hub, Home, About, Contact, Privacy, Terms.

## Run 2026-11-23 — Phase 1 completion report
- Live: 159 pages (sitemap lists 158 URLs), 30/30 calendar posts published (+6 launch posts). Live checks (home, sitemap, 4 pages) all 200.
- Still under 600 words: welding hub, Home, About, Contact, Privacy, Terms (legal/utility pages, left short on purpose).
- Skipped for lack of a verified source: copper tubing gas tables, small-engine age; Trane/Carrier residential serial wording flagged TO VERIFY (see 11-19).
- GSC (11-23): 0 clicks, 23 impressions, avg pos 32.7; indexed 1, not indexed 1 (Crawled - not indexed); sitemap "Couldn't fetch" (Bing: Success, 148 URLs, 0 impressions).
- Phase 2: 1 post/day from Google-autocomplete topics.

## Run 2026-11-24
- Post #31 live: wire-size-for-50-amp-breaker (build/posts10.py). 161 pages. Browser libs need apt install first.
