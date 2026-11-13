// Headless Chromium checks: every page loads with no console/CSP errors, no horizontal overflow at 375 px,
// dark mode applies, and each calculator produces the expected value.
// Run: NODE_PATH=<verifactu qa>/node_modules PLAYWRIGHT_BROWSERS_PATH=<.tools/browsers> node qa/test-browser.js
const { chromium } = require('playwright'); const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '../out'); const robots = fs.readFileSync(path.join(ROOT, 'robots.txt'), 'utf8');
const BASE = new URL(/Sitemap: (\S+)\/sitemap\.xml/.exec(robots)[1] + '/').pathname.replace(/\/$/, '');
const T = { '.html': 'text/html; charset=utf-8', '.js': 'application/javascript', '.css': 'text/css', '.svg': 'image/svg+xml', '.png': 'image/png', '.json': 'application/json', '.webmanifest': 'application/manifest+json' };
const srv = http.createServer((q, r) => { let p = decodeURIComponent(q.url.split('?')[0]).slice(BASE.length); if (p.endsWith('/')) p += 'index.html'; const f = path.join(ROOT, p);
  if (!fs.existsSync(f)) { r.writeHead(404, { 'content-type': 'text/html' }); return r.end(fs.readFileSync(path.join(ROOT, '404.html'))); } r.writeHead(200, { 'content-type': T[path.extname(f)] || 'text/plain' }); r.end(fs.readFileSync(f)); }).listen(8811);
const U = 'http://127.0.0.1:8811' + BASE;
const pages = JSON.parse(fs.readFileSync(path.join(__dirname, '../pages.json'))).map(p => p.path);
const fails = []; const ok = (c, m) => { if (!c) fails.push(m); };
(async () => {
  const b = await chromium.launch();
  const mob = await b.newContext({ viewport: { width: 375, height: 800 }, isMobile: true, deviceScaleFactor: 1 });
  const p = await mob.newPage(); let errs = [];
  p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); }); p.on('pageerror', e => errs.push(String(e)));
  for (const pg of pages) {
    errs = [];
    await p.goto(U + pg, { waitUntil: 'networkidle' });
    const ov = await p.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    ok(ov <= 1, `${pg}: horizontal overflow ${ov}px at 375`);
    const res = await p.$$eval('output.res', os => os.map(o => o.textContent.trim()));
    ok(res.every(t => t && !/Loading|Could not load/.test(t)), `${pg}: tool output empty/failed: ${JSON.stringify(res).slice(0, 120)}`);
    ok(errs.length === 0, `${pg}: console errors ${errs.join(' | ').slice(0, 200)}`);
  }
  // functional checks
  const val = async (sel) => (await p.textContent(sel)).replace(/\s+/g, ' ');
  await p.goto(U + '/r410a-pt-chart/', { waitUntil: 'networkidle' });
  ok(/118\.8 psig/.test(await val('[data-tool="pt"] output')), 'R-410A 40F should be 118.8 psig: ' + await val('[data-tool="pt"] output'));
  await p.click('[data-mode="p2t"]'); await p.fill('[data-tool="pt"] [data-in]', '118.8');
  ok(/40\.0 °F/.test(await val('[data-tool="pt"] output')), 'R-410A 118.8 psig -> 40.0F: ' + await val('[data-tool="pt"] output'));
  await p.selectOption('[data-tool="pt"] [data-tu]', 'C'); ok(/4\.4 °C/.test(await val('[data-tool="pt"] output')), 'C conversion');
  await p.selectOption('[data-tool="pt"] [data-tu]', 'F');
  await p.goto(U + '/r454b-pt-chart/', { waitUntil: 'networkidle' });
  const o454 = await val('[data-tool="pt"] output'); ok(/Dew/.test(o454) && /Bubble/.test(o454), 'R-454B shows dew+bubble');
  await p.goto(U + '/superheat-calculator/', { waitUntil: 'networkidle' });
  await p.selectOption('[data-tool="sh"] [data-ref]', 'r410a'); const dew40 = JSON.parse(fs.readFileSync(path.join(ROOT, 'assets/pt-all.json'))).r410a.d[100]; await p.fill('[data-tool="sh"] [data-p]', String(dew40)); await p.fill('[data-tool="sh"] [data-t]', '52');
  ok(/12\.0 °F/.test(await val('[data-tool="sh"] output')), 'superheat 12.0: ' + await val('[data-tool="sh"] output'));
  await p.goto(U + '/conduit-fill-calculator/', { waitUntil: 'networkidle' });
  await p.selectOption('[data-tool="fill"] [data-cs]', '3/4');
  const rows = await p.$$('[data-tool="fill"] .wire'); for (const r of rows.slice(1)) await (await r.$('.x')).click();
  await p.fill('[data-tool="fill"] .wire [data-n]', '16');
  ok(/OK/.test(await val('[data-tool="fill"] output')) && /max \(Note 7 round-up\): 16/.test(await val('[data-tool="fill"] output')), '16 x 12 THHN in 3/4 EMT: ' + await val('[data-tool="fill"] output'));
  await p.fill('[data-tool="fill"] .wire [data-n]', '17'); ok(/TOO FULL/.test(await val('[data-tool="fill"] output')), '17 should be too full');
  await p.goto(U + '/voltage-drop-calculator/', { waitUntil: 'networkidle' });
  ok(/5\.95 V/.test(await val('[data-tool="vd"] output')), 'VD 10AWG 100ft 24A: ' + await val('[data-tool="vd"] output'));
  await p.goto(U + '/natural-gas-pipe-sizing-chart/', { waitUntil: 'networkidle' });
  await p.fill('[data-tool="gas"] [data-btu]', '120000'); await p.fill('[data-tool="gas"] [data-len]', '50');
  ok(/1"/.test(await val('[data-tool="gas"] output')) || /3\/4"/.test(await val('[data-tool="gas"] output')), 'gas pick: ' + await val('[data-tool="gas"] output'));
  ok(/3\/4"/.test(await val('[data-tool="gas"] output')), 'gas 120 CFH @50ft -> 3/4 (151): ' + await val('[data-tool="gas"] output'));
  await p.goto(U + '/bradford-white-water-heater-age/', { waitUntil: 'networkidle' });
  await p.fill('[data-sn]', 'HK16433183'); ok(/October 2011/.test(await val('[data-tool="age"] output')), 'BW HK -> Oct 2011');
  await p.goto(U + '/carrier-age-by-serial-number/', { waitUntil: 'networkidle' });
  await p.fill('[data-sn]', '3112U12345'); ok(/week 31 of 2012/.test(await val('[data-tool="age"] output')), 'Carrier 3112');
  await p.goto(U + '/goodman-age-by-serial-number/', { waitUntil: 'networkidle' });
  await p.fill('[data-sn]', '1306123456'); ok(/June 2013/.test(await val('[data-tool="age"] output')), 'Goodman 1306');
  await p.goto(U + '/22-5-degree-offset-multiplier/', { waitUntil: 'networkidle' });
  ok(/15\.68 in/.test(await val('[data-tool="off"] output')), 'offset 22.5 x 6: ' + await val('[data-tool="off"] output'));
  await p.goto(U + '/box-fill-calculator/', { waitUntil: 'networkidle' });
  ok(/15\.75 in³ of 21\.0/.test(await val('[data-tool="box"] output')), 'box fill: ' + await val('[data-tool="box"] output'));
  await p.goto(U + '/mig-welding-settings-calculator/', { waitUntil: 'networkidle' });
  ok(/125 A/.test(await val('[data-tool="mig"] output')) && /200 ipm/.test(await val('[data-tool="mig"] output')), 'MIG 0.125/.035');
  await p.goto(U + '/search/?q=r454b', { waitUntil: 'networkidle' }); await p.waitForTimeout(200);
  ok((await p.$$('[data-r] li a')).length > 0, 'search results');
  await p.goto(U + '/does-not-exist/'); ok(/Page not found/.test(await p.textContent('h1')), '404 page');
  // dark mode
  const dk = await b.newContext({ viewport: { width: 1280, height: 900 }, colorScheme: 'dark' }); const d = await dk.newPage();
  await d.goto(U + '/r454b-pt-chart/'); const bg = await d.evaluate(() => getComputedStyle(document.body).backgroundColor);
  ok(bg === 'rgb(15, 22, 29)', 'dark background ' + bg);
  const lt = await (await b.newContext({ colorScheme: 'light' })).newPage(); await lt.goto(U + '/');
  ok((await lt.evaluate(() => getComputedStyle(document.body).backgroundColor)) === 'rgb(244, 241, 234)', 'light background');
  // CSP enforcement: an injected inline script must be blocked
  const cspErr = []; d.on('console', m => { if (/Content Security Policy/i.test(m.text())) cspErr.push(m.text()); });
  await d.goto(U + '/'); await d.evaluate(() => { const s = document.createElement('script'); s.textContent = 'window.__x=1'; document.body.appendChild(s); });
  ok((await d.evaluate(() => window.__x)) === undefined, 'CSP should block inline script'); ok(cspErr.length > 0, 'CSP violation reported');
  // print: tools hidden
  await d.emulateMedia({ media: 'print' }); await d.goto(U + '/r22-pt-chart/');
  ok(await d.evaluate(() => getComputedStyle(document.querySelector('.tool')).display === 'none' && getComputedStyle(document.querySelector('.chart')).display !== 'none'), 'print view hides tool, keeps chart');
  await b.close(); srv.close();
  console.log(`${pages.length} pages loaded at 375px; functional, dark-mode, CSP and print checks run.`);
  if (fails.length) { console.log(fails.join('\n')); console.log(fails.length + ' BROWSER FAILURES'); process.exit(1); }
  console.log('BROWSER QA PASSED');
})();
