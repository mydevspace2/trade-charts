"""Static QA: internal link checker, SEO tags, schema validation, sitemap. Run after build: python3 qa/test_static.py"""
import os, re, json, sys, html
from html.parser import HTMLParser
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('TC_OUT', os.path.join(HERE, '..', 'out'))
BASE = os.environ.get('TC_BASE', '/trade-charts')
SITE = os.environ.get('TC_SITE_URL', 'https://mydevspace2.github.io/trade-charts')
errs = []

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.links = []; s.ids = set(); s.h1 = 0; s.meta = {}; s.ld = []; s._ld = False; s.title = ''; s._t = False; s.canon = None; s.buf = ''
    def handle_starttag(s, t, a):
        a = dict(a)
        if 'id' in a: s.ids.add(a['id'])
        if t == 'a' and 'href' in a: s.links.append(a['href'])
        if t in ('link', 'script', 'img') and (a.get('href') or a.get('src')):
            if not (t == 'link' and a.get('rel') == 'canonical'): s.links.append(a.get('href') or a.get('src'))
        if t == 'h1': s.h1 += 1
        if t == 'meta': s.meta[a.get('name') or a.get('property') or a.get('http-equiv') or 'charset'] = a.get('content', '')
        if t == 'link' and a.get('rel') == 'canonical': s.canon = a.get('href')
        if t == 'script' and a.get('type') == 'application/ld+json': s._ld = True; s.buf = ''
        if t == 'title': s._t = True
    def handle_endtag(s, t):
        if t == 'script' and s._ld: s.ld.append(s.buf); s._ld = False
        if t == 'title': s._t = False
    def handle_data(s, d):
        if s._ld: s.buf += d
        if s._t: s.title += d

def check_schema(path, obj):
    t = obj.get('@type')
    if obj.get('@context') != 'https://schema.org': errs.append(f'{path}: bad @context')
    if t == 'FAQPage':
        me = obj.get('mainEntity') or []
        if not me: errs.append(f'{path}: FAQPage empty')
        for q in me:
            if q.get('@type') != 'Question' or not q.get('name') or q.get('acceptedAnswer', {}).get('@type') != 'Answer' or not q['acceptedAnswer'].get('text'):
                errs.append(f'{path}: bad FAQ item')
    elif t == 'BreadcrumbList':
        for i, it in enumerate(obj['itemListElement']):
            if it.get('position') != i + 1 or not it.get('name') or not str(it.get('item', '')).startswith(SITE): errs.append(f'{path}: bad breadcrumb')
    elif t == 'WebApplication':
        for k in ('name', 'url', 'applicationCategory', 'offers'):
            if not obj.get(k): errs.append(f'{path}: WebApplication missing {k}')
    elif t == 'Article':
        for k in ('headline', 'datePublished', 'dateModified', 'author', 'publisher', 'image', 'mainEntityOfPage'):
            if not obj.get(k): errs.append(f'{path}: Article missing {k}')
        if len(obj.get('headline', '')) > 110: errs.append(f'{path}: headline too long')
    elif t in ('WebSite', 'Organization'):
        pass
    else:
        errs.append(f'{path}: unknown schema type {t}')
    return t

files = []
for root, _, fs in os.walk(OUT):
    for f in fs:
        if f.endswith('.html'): files.append(os.path.join(root, f))
types = {}
titles = {}
nlinks = 0
for fn in files:
    rel = '/' + os.path.relpath(fn, OUT).replace('index.html', '')
    src = open(fn, encoding='utf-8').read()
    p = P(); p.feed(src)
    noindex = 'noindex' in p.meta.get('robots', '')
    if p.h1 != 1: errs.append(f'{rel}: {p.h1} h1')
    d = p.meta.get('description', '')
    if not d or len(d) > 160: errs.append(f'{rel}: description length {len(d)}')
    if not p.title or len(p.title) > 75: errs.append(f'{rel}: title length {len(p.title)}')
    if not noindex:
        if p.title in titles: errs.append(f'{rel}: duplicate title with {titles[p.title]}')
        titles[p.title] = rel
        if p.canon != SITE + rel: errs.append(f'{rel}: canonical {p.canon}')
    for k in ('og:title', 'og:description', 'og:url', 'og:image', 'Content-Security-Policy', 'viewport'):
        if k not in p.meta: errs.append(f'{rel}: missing meta {k}')
    if "script-src 'self'" not in p.meta.get('Content-Security-Policy', ''): errs.append(f'{rel}: weak CSP')
    if 'class="disclaimer"' not in src: errs.append(f'{rel}: no disclaimer')
    # inline <script>/<style> allowed only when its sha256 is in the page CSP (strict CSP kept, no 'unsafe-inline')
    _csp = p.meta.get('Content-Security-Policy', '')
    if "'unsafe-inline'" in _csp: errs.append(f'{rel}: unsafe-inline in CSP')
    for _tag, _body in re.findall(r'<(script|style)(?![^>]*(?:src=|type="application/(?:ld\+)?json"))[^>]*>(.*?)</\1>', src, re.S):
        import hashlib, base64
        _h = "'sha256-" + base64.b64encode(hashlib.sha256(_body.encode('utf-8')).digest()).decode() + "'"
        if _h not in _csp: errs.append(f'{rel}: inline {_tag} not hashed in CSP')
    if re.search(r'\sstyle="|\son[a-z]+="', src): errs.append(f'{rel}: inline style/handler (CSP)')
    for b in p.ld:
        try:
            o = json.loads(b)
        except Exception as e:
            errs.append(f'{rel}: invalid JSON-LD {e}'); continue
        t = check_schema(rel, o); types[t] = types.get(t, 0) + 1
    # keyword: the H1's main words appear in title and meta description
    h1 = re.search(r'<h1>(.*?)</h1>', src, re.S)
    if h1 and not noindex:
        h = html.unescape(re.sub('<[^>]+>', '', h1.group(1))).lower()
        key = re.sub(r'[^a-z0-9 ]', ' ', h).split()[:2]
        tl = re.sub(r'[^a-z0-9 ]', ' ', html.unescape(p.title).lower())
        if not all(k in tl.split() or k in tl for k in key): errs.append(f'{rel}: H1 keyword {key} not in title')
    for l in p.links:
        if l.startswith(('http://', 'https://', 'mailto:', 'tel:', 'data:')):
            if l.startswith(SITE): l = BASE + l[len(SITE):]
            else: continue
        nlinks += 1
        if l.startswith('#'):
            if l[1:] and l[1:] not in p.ids: errs.append(f'{rel}: missing anchor {l}')
            continue
        if not l.startswith(BASE + '/'): errs.append(f'{rel}: link not under base {l}'); continue
        pth = l[len(BASE):].split('?')[0].split('#')[0]
        tgt = os.path.join(OUT, pth.lstrip('/'))
        if pth.endswith('/'): tgt = os.path.join(tgt, 'index.html')
        if not os.path.exists(tgt): errs.append(f'{rel}: broken link {l}')
# sitemap
sm = open(os.path.join(OUT, 'sitemap.xml')).read()
locs = re.findall(r'<loc>(.*?)</loc>', sm)
for u in locs:
    pth = u[len(SITE):]
    tgt = os.path.join(OUT, pth.lstrip('/'), 'index.html') if pth.endswith('/') else os.path.join(OUT, pth.lstrip('/'))
    if not os.path.exists(tgt): errs.append(f'sitemap: missing {u}')
robots = open(os.path.join(OUT, 'robots.txt')).read()
if 'Sitemap: ' + SITE + '/sitemap.xml' not in robots: errs.append('robots: sitemap line')
print(f'{len(files)} html files, {len(locs)} sitemap URLs, {nlinks} internal links checked, schema blocks: {types}')
if errs:
    print('\n'.join(errs[:80])); print(f'{len(errs)} ERRORS'); sys.exit(1)
print('STATIC QA PASSED')
