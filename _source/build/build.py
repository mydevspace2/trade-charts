"""Trade Charts static site generator.
Usage:  python3 build.py            (writes ../out)
Env:    TC_SITE_URL (default https://mydevspace2.github.io/trade-charts), TC_BASE (default /trade-charts; '' for a custom domain),
        TC_CNAME (custom domain -> writes CNAME), TC_GSV (Google verification token), TC_UPDATED (YYYY-MM-DD)
Data:   run data_ref.py and data_elec.py first when source data changes; qa/test_data.py verifies it.
"""
import os, shutil, json, re
import core
from core import OUT, PAGES, SITE_URL, BASE, CNAME, INDEXNOW_KEY, UPDATED, HERE

def assets():
    a = os.path.join(OUT, 'assets'); os.makedirs(a, exist_ok=True)
    for f in ('site.css', 'app.js', 'theme.js'):
        shutil.copy(os.path.join(HERE, 'assets', f), a)
    # self-hosted heading font (Barlow Condensed, SIL OFL 1.1; Latin subset woff2) - CSP font-src 'self'
    shutil.copytree(os.path.join(HERE, 'assets', 'fonts'), os.path.join(a, 'fonts'))
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">' + core.MARK_SVG.split('focusable="false">', 1)[1])
    open(os.path.join(OUT, 'favicon.svg'), 'w').write(svg)
    from PIL import Image, ImageDraw, ImageFont
    import math
    Y, K = '#ffc20e', '#161b21'
    def font(sz, cond=False):
        cands = ([os.path.join(HERE, 'fonts-src', 'BarlowCondensed-Bold.ttf')] if cond else []) + [
            '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
        for p in cands:
            if os.path.exists(p):
                return ImageFont.truetype(p, sz)
        return ImageFont.load_default()
    def mark(d, cx, cy, R):
        """hex nut + gauge, R = nut circumradius"""
        hexp = [(cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))) for a in range(-90, 270, 60)]
        d.polygon(hexp, fill=Y)
        r = R * .69; d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=K)
        ra = R * .55; w = max(2, int(R * .1))
        for ang in range(135, 406, 30):
            t = math.radians(ang); x1, y1 = cx + ra * math.cos(t), cy + ra * math.sin(t); x2, y2 = cx + (ra - w * 1.3) * math.cos(t), cy + (ra - w * 1.3) * math.sin(t)
            d.line([(x1, y1), (x2, y2)], fill=Y, width=max(2, w // 2 + 1))
        t = math.radians(-45); d.line([(cx, cy), (cx + R * .42 * math.cos(t), cy + R * .42 * math.sin(t))], fill=Y, width=max(3, int(R * .16)))
        h = R * .15; d.ellipse([cx - h, cy - h, cx + h, cy + h], fill=Y)
    for s in (180, 192, 512):
        im = Image.new('RGB', (s, s), K); d = ImageDraw.Draw(im)
        mark(d, s / 2, s / 2, s * .44)
        im.save(os.path.join(a, f'icon-{s}.png'))
    im = Image.new('RGB', (1200, 630), '#1c232a'); d = ImageDraw.Draw(im)
    for x in range(0, 1200, 24):
        d.line([(x, 0), (x, 600)], fill='#222a32' if x % 96 else '#2c3236')
    for y in range(0, 600, 24):
        d.line([(0, y), (1200, y)], fill='#222a32' if y % 96 else '#2c3236')
    for i in range(-40, 1240, 40):
        d.polygon([(i, 630), (i + 20, 630), (i + 50, 600), (i + 30, 600)], fill=Y)
    d.rectangle([0, 596, 1200, 600], fill=Y)
    mark(d, 1010, 250, 150)
    d.text((80, 120), 'TRADE', font=font(120, True), fill='#f4f5f6'); d.text((80 + d.textlength('TRADE ', font=font(120, True)), 120), 'CHARTS', font=font(120, True), fill=Y)
    d.text((80, 290), 'PT charts \u00b7 Superheat & subcooling', font=font(44), fill=Y)
    d.text((80, 360), 'Conduit fill \u00b7 Ampacity \u00b7 Voltage drop', font=font(44), fill='#f4f5f6')
    d.text((80, 430), 'Gas pipe sizing \u00b7 Age by serial number', font=font(44), fill='#f4f5f6')
    d.text((80, 515), 'Free \u00b7 sourced \u00b7 verified', font=font(32), fill='#9aa7b4')
    im.save(os.path.join(a, 'og.png'), optimize=True)
    man = {'name': 'Trade Charts', 'short_name': 'TradeCharts', 'start_url': BASE + '/', 'display': 'standalone', 'background_color': '#1c232a',
           'theme_color': '#1c232a', 'icons': [{'src': BASE + '/assets/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                                                {'src': BASE + '/assets/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]}
    json.dump(man, open(os.path.join(OUT, 'site.webmanifest'), 'w'))

def llms(idx):
    """/llms.txt (llmstxt.org format): what the site is + its main pages, for AI assistants."""
    sec = {}
    for p in idx:
        sec.setdefault(p['section'] or 'site', []).append(p)
    names = dict(core.SECTIONS); names['site'] = 'Site'
    out = ['# Trade Charts', '', '> Free US field reference for HVAC/R, electrical, gas piping and welding: refrigerant PT charts, superheat/subcooling, '
           'NEC conduit fill, ampacity, voltage drop and box fill, IFGC gas pipe sizing, and equipment age by serial number. '
           'Every value comes from a cited source (NEC, IFGC, manufacturer and NIST/CoolProp data) and is checked by automated tests.', '',
           'All calculators run in the browser; no sign-up. Reference only: verify with the adopted code and manufacturer literature.', '']
    for key in [s for s, _ in core.SECTIONS] + ['site']:
        if key not in sec:
            continue
        out.append(f'## {names.get(key, key)}'); out.append('')
        for p in sorted(sec[key], key=lambda x: x['path']):
            out.append(f"- [{p['title']}]({SITE_URL}{p['path']}): {p['desc']}")
        out.append('')
    open(os.path.join(OUT, 'llms.txt'), 'w', encoding='utf-8').write('\n'.join(out))

def finish():
    idx = [p for p in PAGES if not p['noindex']]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in sorted(idx, key=lambda x: (x['path'] != '/', x['path'])):
        sm.append(f'<url><loc>{SITE_URL}{p["path"]}</loc><lastmod>{UPDATED}</lastmod></url>')
    sm.append('</urlset>')
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write('\n'.join(sm) + '\n')
    # Search engines and AI crawlers named explicitly (one group, same rules). Note: crawlers read robots.txt only at the host root,
    # so on mydevspace2.github.io/trade-charts/ this file is informational until a root robots.txt exists (see README).
    bots = ['*', 'Googlebot', 'Bingbot', 'GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot', 'PerplexityBot', 'Google-Extended', 'CCBot']
    open(os.path.join(OUT, 'robots.txt'), 'w').write(''.join(f'User-agent: {b}\n' for b in bots) + f'Allow: /\nDisallow: {BASE}/search/\nDisallow: {BASE}/_source/\n\nSitemap: {SITE_URL}/sitemap.xml\n')
    llms(idx)
    open(os.path.join(OUT, f'{INDEXNOW_KEY}.txt'), 'w').write(INDEXNOW_KEY)
    open(os.path.join(OUT, '.nojekyll'), 'w').write('')
    if CNAME:
        open(os.path.join(OUT, 'CNAME'), 'w').write(CNAME + '\n')
    json.dump([{'u': p['path'], 't': p['title'], 'd': p['desc']} for p in idx], open(os.path.join(OUT, 'assets', 'search.json'), 'w'), separators=(',', ':'))
    json.dump(PAGES, open(os.path.join(HERE, '..', 'pages.json'), 'w'), indent=0)

def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    assets()
    import pages_hvac, pages_elec, pages_misc, pages_site
    pages_hvac.hvac_pages()
    pages_elec.elec_pages()
    pages_misc.gas_pages()
    pages_misc.age_pages()
    pages_misc.welding_pages()
    pages_site.site_pages()
    finish()
    sec = {}
    for p in PAGES:
        sec[p['section'] or 'site'] = sec.get(p['section'] or 'site', 0) + 1
    print(len(PAGES), 'pages', sec)
    short = [(p['path'], p['words']) for p in PAGES if p['words'] < 600 and not p['noindex']]
    print('titles over 60 chars without SEO_TITLES override:', core.LONG_TITLES)
    print('under 600 words:', len(short), short[:60])

if __name__ == '__main__':
    main()
