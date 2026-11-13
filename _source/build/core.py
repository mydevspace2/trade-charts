"""Layout, helpers and site registry for Trade Charts (static MPA generator)."""
import os, json, html, re, datetime

SITE_URL = os.environ.get('TC_SITE_URL', 'https://mydevspace2.github.io/trade-charts').rstrip('/')
BASE = os.environ.get('TC_BASE', '/trade-charts').rstrip('/')
GSV = os.environ.get('TC_GSV', 'PBIzVZ_WTR9JENZ2TnCvFsTs3YWHua2ZJY0Cq2uO-6k')
CNAME = os.environ.get('TC_CNAME', '')
SITE_NAME = 'Trade Charts'
UPDATED = os.environ.get('TC_UPDATED', '2026-11-13')
UPDATED_H = datetime.date.fromisoformat(UPDATED).strftime('%B %-d, %Y')
ASSET_V = '1'
INDEXNOW_KEY = '7f3c1e9a2b8d4f60a1c5e7b9d3f2a4c6'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('TC_OUT', os.path.join(HERE, '..', 'out'))

PAGES = []  # registry: dict(path, title, desc, section, words)

def esc(s):
    return html.escape(str(s), quote=True)

def url(path):
    """site-relative link honoring BASE; path like '/r454b-pt-chart/'"""
    return BASE + path

def abs_url(path):
    return SITE_URL + path

SECTIONS = [
    ('/pt-chart/', 'PT Charts'),
    ('/hvac-calculators/', 'HVAC Calcs'),
    ('/electrical/', 'Electrical'),
    ('/gas-pipe-sizing/', 'Gas Pipe'),
    ('/age-by-serial-number/', 'Age by Serial'),
    ('/welding/', 'Welding'),
    ('/blog/', 'Guides'),
]

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>'

def breadcrumb_ld(crumbs):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': abs_url(p)} for i, (n, p) in enumerate(crumbs)]}

def faq_ld(faqs):
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub('<[^>]+>', '', a)}} for q, a in faqs]}

def app_ld(name, desc, path):
    return {'@context': 'https://schema.org', '@type': 'WebApplication', 'name': name, 'description': desc, 'url': abs_url(path),
            'applicationCategory': 'UtilitiesApplication', 'operatingSystem': 'Any (web browser)', 'isAccessibleForFree': True,
            'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'}}

def article_ld(title, desc, path, date_pub=UPDATED):
    return {'@context': 'https://schema.org', '@type': 'Article', 'headline': title[:110], 'description': desc, 'url': abs_url(path),
            'datePublished': date_pub, 'dateModified': UPDATED, 'inLanguage': 'en-US',
            'author': {'@type': 'Organization', 'name': SITE_NAME, 'url': abs_url('/about/')},
            'publisher': {'@type': 'Organization', 'name': SITE_NAME, 'logo': {'@type': 'ImageObject', 'url': abs_url('/assets/icon-512.png')}},
            'image': abs_url('/assets/og.png'), 'mainEntityOfPage': abs_url(path)}

def faq_html(faqs):
    h = ['<section class="faq" id="faq"><h2>Frequently asked questions</h2>']
    for q, a in faqs:
        h.append(f'<details><summary>{esc(q)}</summary><div class="ans">{a}</div></details>')
    h.append('</section>')
    return '\n'.join(h)

DISCLAIMER = ('<aside class="disclaimer" role="note"><strong>Reference only.</strong> Values are for field reference and training. '
              'Always verify against the equipment manufacturer\u2019s literature and the code edition adopted by your local '
              'authority having jurisdiction (AHJ) before charging, wiring or piping. Work on refrigerant, electrical and gas systems '
              'only if you are qualified and licensed to do so.</aside>')

def nav_html(active):
    items = ''.join(f'<li><a href="{url(p)}"{" aria-current=\"page\"" if active == p else ""}>{esc(n)}</a></li>' for p, n in SECTIONS)
    return items

def page(path, title, desc, body, crumbs=None, section=None, schema=(), og_type='website', extra_head='', noindex=False):
    """Write one HTML page. crumbs: list of (name, path) excluding Home."""
    assert len(desc) <= 160, (path, len(desc))
    from extra import EXTRA
    from posts2 import related_html
    x = EXTRA.get(path, '') + related_html(path)
    if x:
        body = body.replace('<section class="faq"', x + '<section class="faq"', 1) if '<section class="faq"' in body else body.replace('</article>', x + '</article>', 1)
    crumbs = crumbs or []
    allc = [('Home', '/')] + crumbs
    schemas = list(schema)
    if crumbs:
        schemas.append(breadcrumb_ld(allc))
    bc = ''
    if crumbs:
        bc = '<nav class="crumbs" aria-label="Breadcrumb"><ol>' + ''.join(
            f'<li><a href="{url(p)}">{esc(n)}</a></li>' if i < len(allc) - 1 else f'<li aria-current="page">{esc(n)}</li>'
            for i, (n, p) in enumerate(allc)) + '</ol></nav>'
    gsv = f'<meta name="google-site-verification" content="{esc(GSV)}">' if (GSV and path == '/') else ''
    robots = '<meta name="robots" content="noindex">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    csp = ("default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; "
           "object-src 'none'; base-uri 'self'; form-action 'self'; upgrade-insecure-requests")
    head = f'''<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
{gsv}
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{csp}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<link rel="canonical" href="{abs_url(path)}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{abs_url(path)}">
<meta property="og:image" content="{abs_url('/assets/og.png')}">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#14202b" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#f4f1ea" media="(prefers-color-scheme: light)">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="{url('/favicon.svg')}" type="image/svg+xml">
<link rel="apple-touch-icon" href="{url('/assets/icon-180.png')}">
<link rel="manifest" href="{url('/site.webmanifest')}">
<link rel="stylesheet" href="{url('/assets/site.css')}?v={ASSET_V}">
<script src="{url('/assets/app.js')}?v={ASSET_V}" defer></script>
{extra_head}
{''.join(ld(s) for s in schemas)}
</head>
<body data-base="{BASE}">
<a class="skip" href="#main">Skip to content</a>
<header class="top">
 <div class="wrap top-in">
  <a class="brand" href="{url('/')}" aria-label="{SITE_NAME} home"><span class="mark" aria-hidden="true">TC</span><span>Trade<b>Charts</b></span></a>
  <button class="navbtn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
  <nav id="nav" class="nav" aria-label="Main"><ul>{nav_html(section)}</ul></nav>
  <form class="search" role="search" action="{url('/search/')}" method="get"><label class="sr" for="q">Search charts</label><input id="q" name="q" type="search" placeholder="Search: r454b, 3/4 emt, 10 awg\u2026" autocomplete="off"><div class="sres" hidden></div></form>
 </div>
</header>
<main id="main" class="wrap">
{bc}
{body}
{DISCLAIMER}
<p class="updated">Last reviewed {UPDATED_H}. Found an error? <a href="{url('/contact/')}">Tell us</a> and we fix it within days.</p>
</main>
<footer class="foot">
 <div class="wrap foot-in">
  <div><strong>{SITE_NAME}</strong><p>Free, fast field reference for US HVAC, refrigeration, electrical, plumbing and welding trades. No sign-up, no tracking.</p></div>
  <ul><li><a href="{url('/pt-chart/')}">Refrigerant PT charts</a></li><li><a href="{url('/superheat-calculator/')}">Superheat calculator</a></li><li><a href="{url('/conduit-fill-calculator/')}">Conduit fill calculator</a></li><li><a href="{url('/gas-pipe-sizing/')}">Gas pipe sizing</a></li><li><a href="{url('/age-by-serial-number/')}">Age by serial number</a></li></ul>
  <ul><li><a href="{url('/about/')}">About &amp; sources</a></li><li><a href="{url('/contact/')}">Contact</a></li><li><a href="{url('/privacy/')}">Privacy</a></li><li><a href="{url('/terms/')}">Terms</a></li><li><a href="{url('/sitemap.xml')}">Sitemap</a></li></ul>
 </div>
 <p class="wrap fine">&copy; 2026 {SITE_NAME}. Reference only &mdash; verify with code and manufacturer data. Not affiliated with any manufacturer, NFPA or ICC; trademarks belong to their owners.</p>
</footer>
</body>
</html>
'''
    words = len(re.sub(r'<[^>]+>', ' ', body).split())
    PAGES.append(dict(path=path, title=title, desc=desc, section=section, words=words, noindex=noindex))
    fn = os.path.join(OUT, path.strip('/'), 'index.html') if path.endswith('/') else os.path.join(OUT, path.strip('/'))
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(head)

def table(headers, rows, cls='data', caption=None):
    h = [f'<div class="tblwrap"><table class="{cls}">']
    if caption:
        h.append(f'<caption>{caption}</caption>')
    h.append('<thead><tr>' + ''.join(f'<th scope="col">{x}</th>' for x in headers) + '</tr></thead><tbody>')
    for r in rows:
        h.append('<tr>' + ''.join((f'<th scope="row">{c}</th>' if i == 0 else f'<td>{c}</td>') for i, c in enumerate(r)) + '</tr>')
    h.append('</tbody></table></div>')
    return ''.join(h)

def links(items):
    return '<ul class="linkgrid">' + ''.join(f'<li><a href="{url(p)}">{esc(n)}</a></li>' for p, n in items) + '</ul>'

def fmt(x, nd=1):
    if x is None:
        return '\u2014'
    return f'{x:,.{nd}f}'
