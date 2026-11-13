# QA results (2026-11-13, UX pass)

- Data: ALL DATA CHECKS PASSED (see data-check.log)
- Static: STATIC QA PASSED (138 html, 136 sitemap URLs, links/meta/canonical/CSP/JSON-LD)
- Browser (Chromium headless, 375px + dark + CSP + print + UX: Calculate/Enter/Copy/Reset/Share, theme toggle, contrast >= 4.5:1 both themes, tap targets >= 44px, inputs >= 16px): BROWSER QA PASSED (run in 3 parts: TC_SLICE=0:70, TC_SLICE=70:200, TC_NOPAGES=1)
- Fold (375x812, 18 pages, light + dark): FOLD QA PASSED - tool box and first input above 812px; no sideways scroll after a result
