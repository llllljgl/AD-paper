"""Bounded public-text investigation. Never fetch PDFs or execute page content."""
import base64
import json
import re
import urllib.error
import urllib.request
from urllib.parse import urlsplit
from html.parser import HTMLParser

from .core import now_iso, request, title_key
from .deepseek import search
from .official import HOSTS


def allowed(url):
    try:
        p = urlsplit(url)
        host = p.hostname or ''
        return (p.scheme == 'https' and not p.username and p.port in (None, 443)
                and (host in HOSTS | {'arxiv.org', 'github.com', 'api.github.com'}
                     or host.endswith('.github.io'))
                and not re.search(r'\.pdf|/(?:pdf|download|stamp)(?:/|\.|$)|embedded_pdf', p.path + '?' + p.query, re.I))
    except ValueError:
        return False


class Redirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowed(newurl):
            raise ValueError('Not an allowed public text redirect')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class Text(HTMLParser):
    def __init__(self, raw):
        super().__init__(); self.parts = []; self.hidden = 0; self.feed(raw)
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'nav'): self.hidden += 1
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'nav'): self.hidden = max(0, self.hidden - 1)
    def handle_data(self, text):
        if not self.hidden: self.parts.append(text)


def fetch_text(url):
    if not allowed(url):
        raise ValueError('Only allowed public text pages may be fetched')
    p = urlsplit(url)
    if p.hostname == 'github.com':
        parts = p.path.strip('/').split('/')
        if len(parts) != 2:
            raise ValueError('Only repository README endpoints are supported')
        raw = json.loads(request('https://api.github.com/repos/' + '/'.join(parts) + '/readme', timeout=12))
        return base64.b64decode(raw['content']).decode('utf-8', errors='replace')
    opener = urllib.request.build_opener(Redirect())
    req = urllib.request.Request(url, headers={'User-Agent': 'AD-Paper-Radar/2.0', 'Accept': 'text/html, text/plain'})
    with opener.open(req, timeout=12) as response:
        if response.headers.get_content_type() not in ('text/html', 'application/xhtml+xml', 'text/plain'):
            raise ValueError('Not HTML or text; body not read')
        raw = response.read(2_000_001)
        if len(raw) > 2_000_000: raise ValueError('Page too large')
        text = raw.decode('utf-8', errors='replace')
        return ' '.join(Text(text).parts) if response.headers.get_content_type() != 'text/plain' else text


def excerpt(text):
    text = ' '.join(text.split())
    if len(text) <= 14000: return text
    # Keep task/benchmark context even when navigation or references are lengthy.
    chunks = [text[:3000]]
    last_end = 3000
    for m in re.finditer(r'industrial|manufactur|mvtec|visa\b|real.?3d|eyecandies|benchmark|dataset', text, re.I):
        if m.start() < last_end:
            continue
        start, last_end = max(last_end, m.start()-250), m.end()+950
        chunks.append(text[start:last_end])
        if sum(map(len, chunks)) >= 13000: break
    return '\n'.join(chunks)[:14000]


def investigation_query(title, suffix):
    suffix = ' '.join(suffix.split())[:45]
    budget = 128 - len(suffix) - 3
    title = title.replace('"', '')
    if len(title) > budget:
        title = title[:budget].rsplit(' ', 1)[0]
    return f'"{title}" {suffix}'


def investigate(paper, key, question='', stats=None):
    title = paper['title'].replace('"', '')
    queries = [investigation_query(title, suffix) for suffix in
               ('industrial datasets', 'site:github.com', question or 'site:arxiv.org')]
    urls = list(paper.get('code_urls', []))
    if paper.get('url', '').startswith('https://arxiv.org/abs/'):
        urls.insert(0, paper['url'])
    if paper.get('arxiv_id'): urls.insert(0, 'https://arxiv.org/abs/' + paper['arxiv_id'])
    # Follow explicit author project links found in the public abstract.
    urls.extend(re.findall(r'https://[^\s<>"\\]+', paper.get('abstract', '')))
    searches, failures = [], []
    for query in queries:
        if stats is not None: stats["search_calls"] += 1
        try:
            results = search(query, key, 8)
        except (OSError, ValueError, KeyError) as exc:
            if isinstance(exc, urllib.error.HTTPError) and exc.code in (401, 402, 403):
                raise
            reason = f'HTTP {exc.code}' if isinstance(exc, urllib.error.HTTPError) else type(exc).__name__
            failures.append({'query': query, 'error': reason})
            if stats is not None:
                stats['search_errors'] = stats.get('search_errors', 0) + 1
            continue
        searches.append({'query': query, 'results': [{'title': r.get('title'), 'url': r.get('url')} for r in results]})
        urls.extend(r.get('url', '') for r in results)
    sources, seen = [], set()
    for url in urls:
        url = url.rstrip('.,;)')
        if url in seen or not allowed(url): continue
        seen.add(url)
        if url.startswith('https://arxiv.org/abs/'):
            urls.insert(urls.index(url) + 1, url.replace('/abs/', '/html/'))
        if len(seen) > 6 or len(sources) >= 3: break
        try:
            text = fetch_text(url)
            if title_key(paper['title']) not in title_key(text):
                failures.append({'url': url, 'error': 'paper_title_not_found'}); continue
            sources.append({'url': url, 'text': excerpt(text), 'retrieved_at': now_iso()})
        except (OSError, ValueError, KeyError) as exc:
            failures.append({'url': url, 'error': type(exc).__name__})
    return {'sources': sources, 'searches': searches, 'failures': failures, 'checked_at': now_iso()}
