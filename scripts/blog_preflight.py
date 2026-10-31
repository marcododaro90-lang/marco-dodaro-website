#!/usr/bin/env python3
"""Checks tailored to marcododaro.it. Standard library only; no SEO scores."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import Request, HTTPRedirectHandler, build_opener
import xml.etree.ElementTree as ET

BASE = 'https://marcododaro.it/'

class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.meta, self.canonical, self.headings, self.links = {}, [], [], []
        self.schemas, self.schema_errors, self.title, self.lang = [], [], '', ''
        self._heading, self._title, self._json = None, False, None
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html': self.lang = a.get('lang', '')
        if tag == 'meta':
            key = a.get('name', a.get('property', '')).lower()
            self.meta.setdefault(key, []).append(a.get('content', ''))
        if tag == 'link' and 'canonical' in a.get('rel', '').split():
            self.canonical.append(a.get('href', ''))
        if tag == 'a': self.links.append(a.get('href', ''))
        if re.fullmatch('h[1-6]', tag):
            self.headings.append([int(tag[1]), '']); self._heading = self.headings[-1]
        if tag == 'title': self._title = True
        if tag == 'script' and a.get('type') == 'application/ld+json': self._json = ''
    def handle_data(self, value):
        if self._heading is not None: self._heading[1] += value
        if self._title: self.title += value
        if self._json is not None: self._json += value
    def handle_endtag(self, tag):
        if re.fullmatch('h[1-6]', tag): self._heading = None
        if tag == 'title': self._title = False
        if tag == 'script' and self._json is not None:
            try: self.schemas.append(json.loads(self._json))
            except ValueError as e: self.schema_errors.append(str(e))
            self._json = None
    def one(self, key):
        values = self.meta.get(key, [])
        return values[0] if len(values) == 1 else None

def entities(obj):
    if isinstance(obj, list):
        for value in obj: yield from entities(value)
    elif isinstance(obj, dict):
        yield obj
        for value in obj.values(): yield from entities(value)

def image_url(value):
    if isinstance(value, list): return image_url(value[0]) if value else ''
    if isinstance(value, dict): return value.get('url', value.get('contentUrl', ''))
    return value or ''

def normalized_image(value):
    u = urlsplit(image_url(value))
    return (u.netloc.lower(), unquote(u.path))  # ignore transform parameters

def article_body(source):
    match = re.search(r'<div\s+class="article-body">', source)
    if not match: return ''
    return source[match.end():].split('<div class="article-cta">', 1)[0].strip()

class SafeRedirect(HTTPRedirectHandler):
    max_redirections = 3
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        u = urlsplit(newurl)
        if u.scheme != 'https' or u.hostname not in {'marcododaro.it', 'images.unsplash.com'}:
            raise ValueError('Unexpected redirect destination')
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def remote(path, binary=False):
    url = urljoin(BASE, path)
    if urlsplit(url).hostname not in {'marcododaro.it', 'images.unsplash.com'}:
        raise ValueError('Unexpected remote host')
    request = Request(url, headers={'User-Agent': 'MarcoDodaroBlogPreflight/1.0'})
    with build_opener(SafeRedirect()).open(request, timeout=20) as response:
        final = urlsplit(response.url)
        if final.scheme != 'https' or final.hostname not in {'marcododaro.it', 'images.unsplash.com'}:
            raise ValueError('Unexpected redirect destination')
        data = response.read(5_000_001)
        if len(data) > 5_000_000: raise ValueError('Response exceeds size limit')
        if response.status != 200: raise ValueError('HTTP ' + str(response.status))
        return (data if binary else data.decode('utf-8')), response.headers

def run(root, article, live=False):
    root = root.resolve(); target = (root / article).resolve()
    if not target.is_relative_to(root) or target.suffix != '.html':
        raise ValueError('Article must be an HTML file inside the repository')
    rel = target.relative_to(root).as_posix(); source = target.read_text(); page = Page(source)
    errors, warnings, checks = [], [], []
    def check(name, ok, detail=''):
        checks.append({'check': name, 'status': 'pass' if ok else 'fail', 'detail': detail})
        if not ok: errors.append(name + (': ' + detail if detail else ''))
    expected = urljoin(BASE, rel)
    check('Italian language', page.lang.lower().startswith('it'))
    check('Title', bool(page.title.strip()))
    check('Single description', bool(page.one('description')))
    check('Single H1', sum(level == 1 for level, _ in page.headings) == 1)
    check('Heading order', all(b[0] <= a[0] + 1 for a, b in zip(page.headings, page.headings[1:])))
    check('Self canonical', page.canonical == [expected])
    robots = page.one('robots') or ''
    check('Indexable robots', bool(page.one('robots')) and 'noindex' not in robots.lower() and 'max-image-preview:large' in robots.lower())
    check('No placeholders', not re.search(r'{{|\[(?:IMAGE|CHART|INTERNAL-LINK|CALLOUT|VIDEO)(?:\]|:)', source))
    check('Single shared analytics', len(re.findall(r'<script\b[^>]*src=[\'"]assets/site-analytics\.js\?', source)) == 1)
    check('No direct Google snippet', 'googletagmanager.com/gtag/js' not in source)
    check('JSON-LD parses', not page.schema_errors, '; '.join(page.schema_errors))
    nodes = list(entities(page.schemas))
    articles = [n for n in nodes if n.get('@type') in ('Article', 'BlogPosting', 'NewsArticle')]
    crumbs = [n for n in nodes if n.get('@type') == 'BreadcrumbList']
    check('Single article entity', len(articles) == 1)
    check('Breadcrumb entity and visible trail', len(crumbs) == 1 and 'class="article-breadcrumb"' in source)
    for key in ('og:type', 'og:title', 'og:description', 'og:url', 'og:image', 'og:image:alt', 'twitter:card', 'twitter:title', 'twitter:description', 'twitter:image'):
        check('Metadata ' + key, bool(page.one(key)))
    check('OG canonical', page.one('og:url') == expected)
    check('Article OG type', page.one('og:type') == 'article')
    check('Large Twitter card', page.one('twitter:card') == 'summary_large_image')
    if not page.one('og:site_name'): warnings.append('og:site_name is absent; add to future templates')
    cover = page.one('og:image') or ''
    check('Social cover consistency', bool(cover) and page.one('twitter:image') == cover)
    cover_tag = re.search(r'<div\b[^>]*class="article-cover"[^>]*>', source)
    from html import unescape
    visible_cover = re.search(r"background-image:url\(['\"]?([^)'\"]+)", unescape(cover_tag[0])) if cover_tag else None
    check('Visible article cover matches metadata', bool(visible_cover) and visible_cover[1] == cover)
    check('Cover accessible label', bool(re.search(r'class="article-cover"[^>]*role="img"[^>]*aria-label="[^"\s]', source)))
    if articles:
        a = articles[0]
        check('Headline matches H1', a.get('headline') == next((text for level, text in page.headings if level == 1), ''))
        check('Author Marco Dodaro', any(n.get('@type') == 'Person' and n.get('name') == 'Marco Dodaro' for n in entities(a.get('author'))))
        check('Published date present', bool(a.get('datePublished')))
        check('Schema cover consistency', image_url(a.get('image')) == cover)
        check('Publication metadata consistency', page.one('article:published_time') == a.get('datePublished'))
    bad_links = []
    for link in page.links:
        u = urlsplit(link)
        if u.scheme in ('mailto', 'tel') or (u.netloc and u.hostname != 'marcododaro.it'): continue
        path = unquote(u.path)
        if not path: continue
        dest = (root / path.lstrip('/')) if path.startswith('/') else target.parent / path
        if path == '/': dest = root / 'index.html'
        if not dest.exists(): bad_links.append(link)
    check('Local links exist', not bad_links, ', '.join(bad_links))
    meta = json.loads((root / 'articles_meta.json').read_text())
    archive = {v['file'] for v in meta.values()}
    archive.update(p.name for p in root.glob('*.html') if 'class="article-body"' in p.read_text() and not p.name.startswith('template'))
    check('Article metadata exists', rel in {v['file'] for v in meta.values()})
    blog = (root / 'blog.html').read_text()
    section = blog.split('<section class="blog-page-list">', 1)[1].split('<footer', 1)[0]
    listing = Page(section); counts = Counter(listing.links)
    check('Archive complete and unique', set(counts) == archive and all(v == 1 for v in counts.values()))
    featured = re.findall(r'<a\b[^>]*class="blog-featured"[^>]*>', section)
    check('Single featured', len(featured) == 1)
    entry = next((v for v in meta.values() if v.get('file') == rel), {})
    check('Metadata cover consistency', entry.get('image') == cover)
    check('Cover credited and license recorded', bool(entry.get('image_source')) and 'unsplash.com/photos/' in entry.get('image_source', '') and bool(entry.get('image_credit')) and entry.get('image_license') == 'Unsplash License')
    duplicate_images = [v['file'] for v in meta.values() if v.get('file') != rel and normalized_image(v.get('image')) == normalized_image(cover)]
    check('Cover URL distinct in metadata', not duplicate_images, ', '.join(duplicate_images))
    sitemap = (root / 'sitemap.xml').read_text(); tree = ET.fromstring(sitemap)
    locations = [n.text for n in tree.iter() if n.tag.rsplit('}', 1)[-1] == 'loc']
    check('Sitemap contains all articles once', all(locations.count(urljoin(BASE, f)) == 1 for f in archive))
    robots_text = (root / 'robots.txt').read_text()
    check('Robots sitemap reference', 'Sitemap: ' + BASE + 'sitemap.xml' in robots_text)
    check('Robots no site-wide block', not re.search(r'^Disallow:\s*/\s*$', robots_text, re.M | re.I))
    for p in root.glob('*.html'):
        if p == target or p.name.startswith('template'): continue
        other = Page(p.read_text())
        if other.title == page.title: warnings.append('Duplicate title: ' + p.name)
        if other.one('description') and other.one('description') == page.one('description'):
            warnings.append('Duplicate description: ' + p.name)
    if live:
        for path in (rel, 'blog.html', 'sitemap.xml', 'robots.txt'):
            try:
                data, headers = remote(path)
                if path == rel:
                    check('Live X-Robots-Tag', 'noindex' not in headers.get('X-Robots-Tag', '').lower())
                    live_page = Page(data)
                    check('Live title and article body match', live_page.title == page.title and article_body(data) == article_body(source))
                    check('Live canonical and cover', live_page.canonical == page.canonical and live_page.one('og:image') == cover)
                elif path == 'blog.html': check('Live blog matches', data == blog)
                elif path == 'sitemap.xml': check('Live sitemap matches', data == sitemap)
                else: check('Live robots matches', data == robots_text)
            except Exception as e: check('Live ' + path, False, str(e))
        try:
            data, headers = remote(cover, binary=True)
            check('Live cover serves image', headers.get('Content-Type', '').startswith('image/') and len(data) > 1000)
        except Exception as e: check('Live cover', False, str(e))
    return {'article': rel, 'checked_at': datetime.now(timezone.utc).isoformat(), 'status': 'fail' if errors else 'pass',
            'checks': checks, 'errors': errors, 'warnings': warnings,
            'not_checked': ['Factual accuracy and source independence', 'Perceptual uniqueness and photo license page', 'Rendered mobile/tablet/desktop layout', 'Full Schema.org and rich-results eligibility', 'Search Console indexing/ranking and real Core Web Vitals', 'Editorial judgment and AI-detector outcomes'],
            'live': live, 'article_sha256': sha256(source.encode()).hexdigest()}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument('--article', required=True)
    ap.add_argument('--live', action='store_true')
    args = ap.parse_args()
    try: report = run(args.root, args.article, args.live)
    except Exception as e: report = {'status': 'fail', 'errors': [str(e)]}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['status'] == 'pass' else 1

if __name__ == '__main__': sys.exit(main())
