# Trade Charts — maintenance guide

> Continuing with another AI? Start with [AI-HANDOVER.md](AI-HANDOVER.md).

Free US trades reference: refrigerant PT charts, HVAC calculators, NEC conduit fill / ampacity / voltage drop / offsets / box fill,
IFGC gas pipe sizing, age-by-serial decoders and welding starting points. Static multi-page site, no trackers, no build server.

Live: https://mydevspace2.github.io/trade-charts/  ·  Repo: https://github.com/mydevspace2/trade-charts (GitHub Pages, `main` / root)

## Layout (repo)
- Site files at the root (generated — do not hand-edit).
- `_source/build/` — Python generator: `build.py` (entry), `core.py` (layout, SEO, schema), `pages_hvac.py`, `pages_elec.py`,
  `pages_misc.py` (gas, age, welding), `pages_site.py` (home, blog, legal), `extra.py` (editorial add-ons), `assets/` (CSS, JS),
  `data/` (generated JSON), `data_ref.py` (refrigerant tables), `data_elec.py` (NEC + IFGC tables).
- `_source/qa/` — `test_data.py` (data vs sources), `test_static.py` (links, SEO, schema, sitemap), `test-browser.js` (Playwright/Chromium: pages, calculators, Calculate/Enter/Copy/Reset/Share, theme toggle, contrast, tap targets), `test-fold.js` (mobile first screen). On a slow machine split the page loop: `TC_SLICE=0:70`, `TC_SLICE=70:200`, then `TC_NOPAGES=1` (run them one after another; they share port 8811).
- `_source/src/` — parsed reference data used by the data tests. `_source/ci/indexnow.yml` — optional GitHub Action.

## Rebuild and test
```sh
pip install CoolProp==8.0.0 pillow            # CoolProp only needed when regenerating refrigerant data
cd _source/build
python3 data_ref.py && python3 data_elec.py    # only when source data changes
python3 ../qa/test_data.py                     # must print ALL DATA CHECKS PASSED
python3 build.py                               # writes ../out (or set TC_OUT)
python3 ../qa/test_static.py                   # links, titles/meta, canonical, CSP, JSON-LD, sitemap
cd ../qa && npm i && npx playwright install chromium && node test-browser.js
node test-fold.js ../out                        # 375x812: tool box + first input above the fold, no sideways scroll after a result
```
Environment: `TC_SITE_URL`, `TC_BASE` (use `''` for a custom domain at the root), `TC_CNAME` (writes CNAME), `TC_GSV`
(Google verification token, home page only), `TC_UPDATED` (date shown on pages and used for sitemap lastmod).

**Moving to a custom domain:** `TC_SITE_URL=https://example.com TC_BASE= TC_CNAME=example.com python3 build.py`, add the domain in
GitHub Pages settings, then add the new property in Search Console / Bing and resubmit the sitemap.

## Data rules (do not break)
- Never publish a value that is not from a cited source or computed from one. Skip a page instead of guessing.
- A refrigerant goes live only if `test_data.py` shows ≤ 1.0 °F deviation against ≥ 1 published chart (R-454C failed and is excluded).
- Code tables are compared with the parsed source text on every test run.

## Routine maintenance (≈ 15 min / month)
1. Check Search Console + Bing Webmaster: coverage errors, queries with impressions but low CTR (rewrite those titles/meta).
2. Read the contact inbox for corrections; fix data in `data_*.py` or page modules, rebuild, run all three tests, push.
3. Publish 1–2 posts from the blog calendar (`work/trades/blog-calendar.md`): add to `POSTS` + `post_bodies()` in `pages_site.py`.
4. Every NEC cycle (2026 adoption by states) re-check Tables 310.16 / Chapter 9 / 314.16; every IFGC cycle (2024) re-check 402.4 tables.
5. When manufacturers publish new PT charts (new A2L blends), add the refrigerant to `data_ref.py` and its reference points to `test_data.py`.
6. Once a year: re-verify the serial-number source URLs (formats change) and update `TC_UPDATED`.
