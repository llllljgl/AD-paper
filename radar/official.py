"""Official conference catalogs and publisher-deposited journal metadata."""

import html
import json
import re
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from urllib.parse import quote, urlencode, urljoin, urlsplit

from .core import github_links, now_iso, title_key

HOSTS = {
    "openaccess.thecvf.com", "eccv.ecva.net", "neurips.cc", "proceedings.iclr.cc",
    "proceedings.mlr.press", "ijcai.org", "ojs.aaai.org", "api.crossref.org",
    "doi.org", "link.springer.com", "ieeexplore.ieee.org", "www.ebi.ac.uk",
}
MEDIA_TYPES = {"text/html", "application/xhtml+xml", "application/json"}
ANOMALY = re.compile(
    r"\banomal\w*|\bdefects?\b|\bvisual inspection\b|\bindustrial inspection\b"
    r"|\bquality inspection\b|\bsurface flaws?\b|\bmvtec\b"
    r"|\breal[- ]?iad\b|\beyecandies\b|\bbtad\b|\bmmad\b",
    re.I,
)
ARXIV_ID = re.compile(r"https?://arxiv\.org/abs/(\d{4}\.\d{4,5})(?:v\d+)?$")
ANCHOR = re.compile(r'<a\b[^>]*?href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', re.I | re.S)
VOID = {"meta", "link", "img", "input", "hr", "br", "source", "wbr", "area", "base", "col", "embed", "param", "track"}


def plain_text(value):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", value or "")).split())


def metadata_url(url):
    parsed = urlsplit(url)
    return (parsed.scheme == "https" and parsed.hostname in HOSTS and not parsed.username
            and parsed.port in (None, 443)
            and not re.search(r"\.pdf(?:/|$)|/(?:pdf|download)(?:/|$)", parsed.path, re.I))


class MetadataRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not metadata_url(newurl):
            raise ValueError("Redirect does not lead to an allowed metadata page")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def get_metadata(url):
    if not metadata_url(url):
        raise ValueError("Expected an official HTML or JSON metadata URL")
    opener = urllib.request.build_opener(MetadataRedirect())
    request = urllib.request.Request(url, headers={
        "User-Agent": "AD-Paper-Radar/1.0 (+https://github.com/llllljgl/AD-paper)",
        "Accept": "text/html, application/xhtml+xml, application/json",
    })
    for attempt in range(2):
        try:
            with opener.open(request, timeout=12) as response:
                if response.headers.get_content_type() not in MEDIA_TYPES:
                    raise ValueError("Source did not return HTML or JSON metadata")
                data = response.read(24_000_001)
                if len(data) > 24_000_000:
                    raise ValueError("Metadata response exceeded the size limit")
                return data.decode(response.headers.get_content_charset() or "utf-8", errors="replace")
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt or (isinstance(exc, urllib.error.HTTPError) and exc.code not in (429, 500, 502, 503, 504)):
                raise
            time.sleep(2)


def catalog_entries(source, year, kind, raw):
    """Return title and paper-page pairs. Validate the index before filtering."""
    pairs = []
    if kind == "neurips":
        cards = re.findall(r'id="maincard_(\d+)"[^>]*>.*?<div class="maincardBody">(.*?)</div>', raw, re.S)
        pairs = [(title, f"/virtual/{year}/poster/{event}") for event, title in cards]
    elif kind == "pmlr":
        for block in raw.split('<div class="paper">')[1:]:
            title = re.search(r'<p class="title">(.*?)</p>', block, re.S)
            link = re.search(r'<a href="([^"]+\.html)"', block)
            if title and link:
                pairs.append((title[1], link[1]))
    else:
        paths = {
            "cvf": rf"/content/[A-Z]+{year}/html/[^/]+_paper\.html",
            "eccv": rf"/virtual/{year}/(?:poster|oral)/\d+",
            "iclr": rf"/paper_files/paper/{year}/hash/[^/]+-Abstract-Conference\.html",
            "ijcai": rf"/proceedings/{year}/\d+",
        }
        for href, title in ANCHOR.findall(raw):
            path = urlsplit(urljoin(source, html.unescape(href))).path
            if re.fullmatch(paths[kind], path):
                pairs.append((title, href))
    entries = {}
    for title, href in pairs:
        title, url = plain_text(title), urljoin(source, html.unescape(href))
        if len(title) >= 12 and metadata_url(url):
            entries[url] = title
    if not entries:
        raise ValueError("No paper entries recognized in the official catalog")
    return entries


class PaperPage(HTMLParser):
    def __init__(self, raw):
        super().__init__()
        self.meta, self.stack, self.abstract = {}, [], []
        self.feed(raw)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta":
            name = (attrs.get("name") or attrs.get("property") or "").lower()
            self.meta.setdefault(name, []).append(attrs.get("content", ""))
        if tag not in VOID:
            classes = set(attrs.get("class", "").split())
            abstract = (attrs.get("id") in {"abstract", "Abs1"} or attrs.get("data-title") == "Abstract"
                        or bool(classes & {"abstract-text-inner", "paper-abstract", "article__abstract"}))
            self.stack.append((tag, abstract or bool(self.stack and self.stack[-1][1])))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        if self.stack and self.stack[-1][1]:
            self.abstract.append(data)

    def values(self, name):
        return [value for value in self.meta.get(name, []) if value]


def paper_metadata(url, raw, title):
    page = PaperPage(raw)
    page_title = next(iter(page.values("citation_title")), "")
    if page_title and title_key(page_title) != title_key(title):
        raise ValueError("Paper page title does not match its catalog entry")
    abstract = " ".join(" ".join(page.abstract).split())
    if not abstract:
        abstract = next(iter(page.values("citation_abstract") + page.values("dc.description")), "")
    result = {}
    if abstract:
        result["abstract"] = abstract
    if page.values("citation_author"):
        result["authors"] = page.values("citation_author")
    pdf = next(iter(page.values("citation_pdf_url")), "")
    codes = github_links(abstract)
    arxiv_ids = set()
    for href, label in ANCHOR.findall(raw):
        target, label = urljoin(url, html.unescape(href)), plain_text(label).casefold()
        if not pdf and label in {"pdf", "paper pdf", "download pdf"} and urlsplit(target).path.lower().endswith(".pdf"):
            pdf = target
        if label in {"code", "github", "source code", "github repository", "project code"}:
            codes.extend(github_links(target))
        match = ARXIV_ID.fullmatch(target)
        if match and label in {"arxiv", "arxiv preprint", "preprint"}:
            arxiv_ids.add(match[1])
    if pdf.startswith("https://"):
        result["pdf_url"] = pdf
    if len(arxiv_ids) == 1:
        result["arxiv_id"] = arxiv_ids.pop()
    codes = sorted({code for code in codes if "/yourusername/" not in code.lower()})
    if codes:
        result["code_urls"] = codes
    return result


def crossref_entries(year, spec, get):
    start, end = f"{year}-01-01", f"{year}-12-31"
    filters = [f"from-pub-date:{start}", f"until-pub-date:{end}"]
    if "issn" in spec:
        endpoint = f"https://api.crossref.org/journals/{spec['issn']}/works"
        filters.append("type:journal-article")
    else:
        endpoint = "https://api.crossref.org/works"
        filters.append(f"container-title:{spec['crossref_container']}")
    cursor = "*"
    for _ in range(100):
        query = urlencode({
            "filter": ",".join(filters), "rows": 200, "cursor": cursor,
            "select": "DOI,title,published,published-print,author,abstract,relation,resource",
        })
        response = json.loads(get(f"{endpoint}?{query}"))["message"]
        items = response["items"]
        yield from items
        if len(items) < 200:
            return
        cursor = response["next-cursor"]
    raise ValueError("Crossref catalog exceeded the pagination limit")


def publisher_candidate(venue, year, row):
    doi = row.get("DOI", "").lower()
    title = plain_text(next(iter(row.get("title", [])), ""))
    if not doi or not title:
        return None
    date = (row.get("published-print") or row.get("published") or {}).get("date-parts", [[]])[0]
    if not date or date[0] != year:
        return None
    abstract = plain_text(row.get("abstract"))
    url = "https://doi.org/" + quote(doi, safe="/")
    paper = official_candidate(venue, year, url, title, "doi:" + doi)
    paper["abstract"] = abstract
    paper["code_urls"] = github_links(abstract)
    paper["authors"] = [" ".join(author[k] for k in ("given", "family") if author.get(k))
                        for author in row.get("author", [])]
    publisher_url = (row.get("resource") or {}).get("primary", {}).get("URL", "")
    if publisher_url and metadata_url(publisher_url):
        paper["publisher_url"] = publisher_url
    return paper


def official_candidate(venue, year, url, title, paper_id=None):
    return {
        "id": paper_id or f"{venue.lower()}:{urlsplit(url).path}",
        "title": title, "authors": [], "published": str(year), "updated": str(year),
        "source": venue, "venue": f"{venue} {year}", "url": url, "official_url": url,
        "abstract": "", "pdf_url": "", "code_urls": [],
    }


def recent_metadata(paper, now, refresh_days):
    if not paper or not paper.get("metadata_checked_at"):
        return False
    checked = datetime.fromisoformat(paper["metadata_checked_at"])
    interval = refresh_days if paper.get("abstract") or paper.get("status") == "accepted" else 7
    return now - checked < timedelta(days=interval)


def url_key(url):
    parsed = urlsplit(url)
    host, path = parsed.hostname, parsed.path.rstrip("/")
    if host == "neurips.cc":
        path = re.sub(r"(/virtual/\d{4})/loc/[^/]+/", r"\1/", path)
    if host == "doi.org":
        path = path.lower()
    return host, path


def compare_discovery(entries, results):
    """Map external search hits back to official records before considering them."""
    by_url, by_title = {}, {}
    for paper in entries:
        by_url[url_key(paper["url"])] = paper
        if paper.get("publisher_url"):
            by_url[url_key(paper["publisher_url"])] = paper
        by_title[title_key(paper["title"])] = paper
    matched = {}
    for result in results:
        url, title = result.get("url"), result.get("title")
        if not isinstance(url, str) or not isinstance(title, str):
            continue
        try:
            if not metadata_url(url):
                continue
            paper = by_url.get(url_key(url)) or by_title.get(title_key(title.split("|", 1)[0]))
        except ValueError:
            continue
        if paper:
            matched[paper["id"]] = paper
    return matched


class OfficialSources:
    def __init__(self, config, existing, get=None):
        self.config = config
        self.get = get or get_metadata
        self.existing = {title_key(paper["title"]): paper for paper in existing}

    def index(self, venue, spec):
        year = self.config["collection_year"]
        if "catalog" in spec:
            url = spec["catalog"]
            entries = catalog_entries(url, year, spec["format"], self.get(url))
            papers = [official_candidate(venue, year, link, title) for link, title in entries.items()]
            return len(entries), papers
        rows = list(crossref_entries(year, spec, self.get))
        papers = [paper for row in rows if (paper := publisher_candidate(venue, year, row))]
        return len(rows), papers

    def detail(self, paper):
        url = paper.get("publisher_url") or paper["official_url"]
        detail = {}
        try:
            detail = paper_metadata(url, self.get(url), paper["title"])
        except (OSError, ValueError):
            if not paper["id"].startswith("doi:"):
                raise
        if not detail.get("abstract") and not paper.get("abstract") and paper["id"].startswith("doi:"):
            # Europe PMC exposes abstracts for participating publishers, including many IEEE articles.
            doi = paper["id"][4:]
            query = urlencode({"query": f'DOI:"{doi}"', "resultType": "core", "format": "json"})
            result = json.loads(self.get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?{query}"))
            for item in result.get("resultList", {}).get("result", []):
                if item.get("doi", "").casefold() == doi.casefold() and item.get("abstractText"):
                    detail["abstract"] = plain_text(item["abstractText"])
                    detail["code_urls"] = sorted(set(detail.get("code_urls", []) + github_links(detail["abstract"])))
                    break
        return detail

    def collect(self, search_results=None):
        papers, reports = [], {}
        search_results = search_results or {}
        now = datetime.now(timezone.utc)
        refresh = self.config.get("official_metadata_refresh_days", 28)
        limit = self.config.get("official_details_per_source", 12)
        for venue, spec in self.config.get("official_sources", {}).items():
            if "unavailable" in spec:
                reports[venue] = {"status": "skipped", "reason": spec["unavailable"]}
                continue
            try:
                scanned, entries = self.index(venue, spec)
            except (OSError, ValueError, KeyError) as exc:
                reports[venue] = {"status": "failed", "reason": type(exc).__name__}
                continue
            keyword = {p["id"]: p for p in entries if ANOMALY.search(f"{p['title']} {p['abstract']}")}
            matches = compare_discovery(entries, search_results.get(venue, []))
            # Keep refreshing a previously discovered paper even when its
            # title stops appearing in the ranked search results.
            tracked = {p["id"]: p for p in entries if title_key(p["title"]) in self.existing}
            candidates = list({**keyword, **matches, **tracked}.values())
            deepseek_only = [p for pid, p in matches.items() if pid not in keyword]
            for paper in deepseek_only:
                paper["deepseek_only"] = True
            deepseek_new = [p for p in deepseek_only if title_key(p["title"]) not in self.existing]
            needs_detail = []
            for paper in candidates:
                existing = self.existing.get(title_key(paper["title"]), {})
                if recent_metadata(existing, now, refresh):
                    continue
                needs_detail.append((paper, existing))
            # New candidates and missing abstracts go first, then refresh the oldest links.
            needs_detail.sort(key=lambda pair: (not (pair[0].get("deepseek_only") or pair[1].get("deepseek_only")),
                                                bool(pair[1].get("abstract") or pair[0]["abstract"]),
                                                pair[1].get("metadata_checked_at", "")))
            def check_detail(pair):
                paper, existing = pair
                try:
                    detail = self.detail({**paper, "abstract": paper["abstract"] or existing.get("abstract", "")})
                    paper["code_urls"] = sorted(set(paper["code_urls"] + detail.pop("code_urls", [])))
                    paper.update(detail)
                    return True
                except (OSError, ValueError, KeyError):
                    return False
                finally:
                    paper["metadata_checked_at"] = now_iso()
            with ThreadPoolExecutor(max_workers=4) as executor:
                outcomes = list(executor.map(check_detail, needs_detail[:limit]))
            checked, failed = sum(outcomes), len(outcomes) - sum(outcomes)
            papers.extend(candidates)
            reports[venue] = {
                "status": "partial" if failed else "ok", "scanned": scanned, "candidates": len(candidates),
                "details_checked": checked, "details_failed": failed,
                "details_deferred": max(0, len(needs_detail) - limit),
            }
            if venue in search_results:
                reports[venue].update(
                    deepseek_hits=len(matches), catalog_only=len(keyword.keys() - matches.keys()),
                    deepseek_only=len(deepseek_only),
                    deepseek_new=[{"title": p["title"], "url": p["url"]} for p in deepseek_new[:20]],
                )
            print(f"{venue}: scanned {scanned}, {len(candidates)} candidates, {checked} details refreshed", flush=True)
        return papers, reports
