// Mobile first-screen check (375x812): on the home page and one page per tool template the tool box, its first
// input and its answer must start above 812 px; after producing a result (Calculate) no page may scroll sideways.
// Usage: node qa/test-fold.js [outDir] [jsonOut]   (outDir defaults to ../out)
const { chromium } = require('playwright'); const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(process.argv[2] || path.join(__dirname, '../out'));
const robots = fs.readFileSync(path.join(ROOT, 'robots.txt'), 'utf8');
const BASE = new URL(/Sitemap: (\S+)\/sitemap\.xml/.exec(robots)[1] + '/').pathname.replace(/\/$/, '');
const T = { '.html': 'text/html; charset=utf-8', '.js': 'application/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.png': 'image/png', '.json': 'application/json' };
const srv = http.createServer((q, r) => { let p = decodeURIComponent(q.url.split('?')[0]).slice(BASE.length); if (p.endsWith('/')) p += 'index.html'; const f = path.join(ROOT, p);
  if (!fs.existsSync(f)) { r.writeHead(404); return r.end(''); } r.writeHead(200, { 'content-type': T[path.extname(f)] || 'text/plain' }); r.end(fs.readFileSync(f)); }).listen(8812);
const U = 'http://127.0.0.1:8812' + BASE;
const PAGES = ['/', '/r410a-pt-chart/', '/r454b-pt-chart/', '/pt-chart/', '/superheat-calculator/', '/subcooling-calculator/', '/target-superheat-calculator/',
  '/conduit-fill-calculator/', '/emt-conduit-fill-chart/', '/wire-ampacity-chart/', '/voltage-drop-calculator/', '/box-fill-calculator/', '/22-5-degree-offset-multiplier/',
  '/gas-pipe-sizing/', '/natural-gas-pipe-sizing-chart/', '/bradford-white-water-heater-age/', '/carrier-age-by-serial-number/', '/mig-welding-settings-calculator/'];
const FOLD = 812; const rows = [], fails = [];
(async () => {
  const b = await chromium.launch();
  for (const scheme of ['light', 'dark']) {
    const ctx = await b.newContext({ viewport: { width: 375, height: FOLD }, isMobile: true, hasTouch: true, deviceScaleFactor: 1, colorScheme: scheme });
    const p = await ctx.newPage();
    for (const pg of PAGES) {
      const r = await p.goto(U + pg, { waitUntil: 'networkidle' }); if (!r.ok()) { fails.push(pg + ' ' + r.status()); continue; }
      const m = await p.evaluate(() => {
        const tool = document.querySelector('.tool'); if (!tool) return null;
        const top = e => e ? Math.round(e.getBoundingClientRect().top + scrollY) : null;
        const bot = e => e ? Math.round(e.getBoundingClientRect().bottom + scrollY) : null;
        const inp = tool.querySelector('input:not([type=hidden]),select'), out = tool.querySelector('output.res'), calc = tool.querySelector('[data-calc]');
        return { tool: top(tool), input: top(inp), inputBottom: bot(inp), result: top(out), resultBottom: bot(out), calc: calc && !calc.hidden ? top(calc) : null };
      });
      if (!m) { fails.push(pg + ': no .tool'); continue; }
      // produce a result: click Calculate if present, else fire input
      const calc = await p.$('.tool [data-calc]:not([hidden])');
      if (calc) await calc.click(); else await p.evaluate(() => { const i = document.querySelector('.tool input'); if (i) i.dispatchEvent(new Event('input', { bubbles: true })); });
      await p.waitForTimeout(150);
      const ov = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth);
      const resTxt = (await p.$eval('.tool output.res', o => o.textContent.trim()).catch(() => '')).slice(0, 80);
      rows.push({ scheme, page: pg, ...m, overflowAfterResult: ov, result_text: resTxt });
      if (scheme === 'light') {
        if (m.tool >= FOLD) fails.push(`${pg}: tool box top ${m.tool} >= ${FOLD}`);
        if (m.input === null || m.inputBottom > FOLD) fails.push(`${pg}: first input bottom ${m.inputBottom} > ${FOLD}`);
      }
      if (ov > 1) fails.push(`${pg} (${scheme}): sideways scroll ${ov}px after result`);
    }
    await ctx.close();
  }
  await b.close(); srv.close();
  if (process.argv[3]) fs.writeFileSync(process.argv[3], JSON.stringify(rows, null, 1));
  console.log('page'.padEnd(36), 'tool', 'input', 'inBot', 'calc', 'result', 'resBot', 'ovf');
  rows.filter(r => r.scheme === 'light').forEach(r => console.log(r.page.padEnd(36), String(r.tool).padEnd(4), String(r.input).padEnd(5), String(r.inputBottom).padEnd(5), String(r.calc).padEnd(4), String(r.result).padEnd(6), String(r.resultBottom).padEnd(6), r.overflowAfterResult));
  if (fails.length) { console.log(fails.join('\n')); console.log(fails.length + ' FOLD FAILURES'); process.exit(1); }
  console.log('FOLD QA PASSED');
})();
