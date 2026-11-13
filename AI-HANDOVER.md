# AI handover: Trade Charts (US trades reference)

Live site: https://mydevspace2.github.io/trade-charts/
Owner: Yasir Ali (GitHub mydevspace2). Everything here belongs to the owner and runs free on GitHub Pages, with or without any AI subscription.

## What this site is
Free US reference for trades: 32 refrigerant PT charts and comparisons, superheat/subcooling calculators, NEC conduit fill, ampacity, voltage drop, box fill, IFGC gas pipe sizing, water heater and HVAC age by serial number, welding settings. Language: US English.

Other sites by the same owner, built the same way: mydevspace2/numer-ksef, mydevspace2/herramientas-verifactu, mydevspace2/trade-charts.

## Rules (always follow)
- Zero budget. Never buy anything (domains, tools, ads) without the owner's explicit "yes".
- Never post anywhere outside this site (Facebook, forums, Reddit) without the owner's OK for that exact post. Drafts live in `_source/docs/` or `_source/seo/promo-drafts.md`.
- Never invent data: every figure, date, legal rule, chart value or rate must come from a cited official or published source. If it can't be verified, leave it out.
- Run every test in `_source/qa/` before pushing. Push only when all pass.
- Never put passwords or tokens in this repo. Logins belong to the owner.
- Keep the Google `google-site-verification` meta tag on the home page.

## How to continue with any AI (ChatGPT, Claude, Gemini, Cursor, Copilot)
1. Give the AI this file, `README.md`, and the notes in `_source/docs/` (start with `project-notes.md` if present, then `knowledge-base/README.md`).
2. Paste the daily routine below as your request.
3. The AI edits files in `_source/build/`, rebuilds, runs `_source/qa/`, and copies the output to the repo root. Then commit and push to `main`. GitHub Pages publishes in 1–2 minutes.
4. With no coding tool: open a file on github.com, tap the pencil, paste the AI's edited version, then commit.

## Daily routine (paste to the AI)
Publish 1–3 new posts from `_source/docs/blog-calendar.md` (900–1,400 words, FAQ, link to the matching tool, cite the source: NEC table numbers, IFGC tables, manufacturer documents). Expand pages under 600 words with worked examples and FAQs. One SEO fix. Add skipped items from `_source/docs/project-notes.md` only when a published source verifies them. Run all tests (data, static, Chromium), then push. IndexNow: the key file is at the site root.

## Weekly / yearly
- Mondays: Google Search Console (search.google.com/search-console, account topelitemindset1@gmail.com) and Bing Webmaster. Check coverage errors, sitemap status and top queries. Rewrite titles of pages with impressions but low CTR.
- After each new page: Search Console → URL Inspection → Request Indexing (a few a day; quota is limited).
- Each NEC/IFGC code cycle: re-check the code tables.
- Once a year: re-check serial-number formats against manufacturer sources.

## Where things are
- `_source/build/`: site generator (Python). `_source/qa/`: tests.
- `_source/docs/` (and `_source/seo/`): blog calendar, keywords, research, project notes, SEO knowledge base and playbook.
- Repo root: the published site (HTML, sitemap.xml, robots.txt).
