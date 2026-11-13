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
