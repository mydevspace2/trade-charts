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
    for f in ('site.css', 'app.js'):
        shutil.copy(os.path.join(HERE, 'assets', f), a)
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="10" fill="#14202b"/>'
           '<rect x="6" y="6" width="52" height="52" rx="6" fill="none" stroke="#d9480f" stroke-width="4"/>'
           '<text x="32" y="42" font-family="monospace" font-weight="700" font-size="24" text-anchor="middle" fill="#d9480f">TC</text></svg>')
    open(os.path.join(OUT, 'favicon.svg'), 'w').write(svg)
    from PIL import Image, ImageDraw, ImageFont
    def font(sz):
        for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'):
            if os.path.exists(p):
                return ImageFont.truetype(p, sz)
        return ImageFont.load_default()
    for s in (180, 192, 512):
        im = Image.new('RGB', (s, s), '#14202b'); d = ImageDraw.Draw(im)
        m = s // 10; d.rounded_rectangle([m, m, s - m, s - m], radius=s // 12, outline='#d9480f', width=max(3, s // 22))
        f = font(int(s * .38)); d.text((s / 2, s / 2), 'TC', font=f, fill='#d9480f', anchor='mm')
        im.save(os.path.join(a, f'icon-{s}.png'))
    im = Image.new('RGB', (1200, 630), '#14202b'); d = ImageDraw.Draw(im)
    d.rectangle([0, 600, 1200, 630], fill='#d9480f')
    d.text((80, 150), 'Trade Charts', font=font(96), fill='#f4f1ea')
    d.text((80, 290), 'PT charts \u00b7 Superheat & subcooling', font=font(44), fill='#ff7a3d')
    d.text((80, 360), 'Conduit fill \u00b7 Ampacity \u00b7 Voltage drop', font=font(44), fill='#f4f1ea')
    d.text((80, 430), 'Gas pipe sizing \u00b7 Age by serial number', font=font(44), fill='#f4f1ea')
    d.text((80, 520), 'Free \u00b7 sourced \u00b7 verified', font=font(32), fill='#9aa7b4')
    im.save(os.path.join(a, 'og.png'), optimize=True)
    man = {'name': 'Trade Charts', 'short_name': 'TradeCharts', 'start_url': BASE + '/', 'display': 'standalone', 'background_color': '#14202b',
           'theme_color': '#14202b', 'icons': [{'src': BASE + '/assets/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                                                {'src': BASE + '/assets/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]}
    json.dump(man, open(os.path.join(OUT, 'site.webmanifest'), 'w'))

def finish():
    idx = [p for p in PAGES if not p['noindex']]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in sorted(idx, key=lambda x: (x['path'] != '/', x['path'])):
        sm.append(f'<url><loc>{SITE_URL}{p["path"]}</loc><lastmod>{UPDATED}</lastmod></url>')
    sm.append('</urlset>')
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write('\n'.join(sm) + '\n')
    open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nDisallow: {BASE}/search/\nDisallow: {BASE}/_source/\n\nSitemap: {SITE_URL}/sitemap.xml\n')
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
    print('under 600 words:', len(short), short[:60])

if __name__ == '__main__':
    main()
