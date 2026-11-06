"""DeepSeek's independent search, bounded by the configured venue list."""

import base64
import json
import re
import urllib.error
from datetime import datetime, timedelta, timezone
from urllib.parse import urlsplit

from .core import github_links, now_iso, request, title_key

SEARCH_URL = "https://api.deepseek.com/v1/tools/search"


def search(query, key, count):
    raw = request(SEARCH_URL, {"query": query, "count": count, "need_content": False},
                  {"Authorization": f"Bearer {key}"}, timeout=20)
    results = json.loads(raw)["results"]
    if not isinstance(results, list):
        raise ValueError("Invalid DeepSeek search response")
    return [row for row in results if isinstance(row, dict)]


def search_venues(config, key):
    matches, errors, calls = {}, {}, 0
    year = config["collection_year"]
    for venue, spec in config.get("official_sources", {}).items():
        if spec.get("unavailable"):
            continue
        host = spec.get("search_host") or urlsplit(spec.get("catalog", "")).hostname or "ojs.aaai.org"
        matches[venue] = []
        for terms in ("industrial visual anomaly detection", "MVTec visual inspection defect"):
            try:
                calls += 1
                matches[venue].extend(search(f"{venue} {year} {terms} site:{host}", key, 20))
            except (OSError, ValueError, KeyError) as exc:
                errors[venue] = f"HTTP {exc.code}" if isinstance(exc, urllib.error.HTTPError) else type(exc).__name__
                # Billing and credential errors apply to the entire key.
                if isinstance(exc, urllib.error.HTTPError) and exc.code in (401, 402, 403):
                    return matches, errors, calls
                break
    return matches, errors, calls


def repository_matches(paper, url):
    repo = url.removeprefix("https://github.com/")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
        return False
    endpoint = "https://api.github.com/repos/" + repo
    try:
        project = json.loads(request(endpoint, timeout=8))
        if project.get("fork") or not project.get("size"):
            return False
        readme = json.loads(request(endpoint + "/readme", timeout=8))
        text = base64.b64decode(readme["content"]).decode("utf-8", errors="replace")
    except (OSError, ValueError, KeyError):
        return False
    if not re.search(r"\bofficial (?:implementation|code|repository|pytorch)|\bour paper\b", text, re.I):
        return False
    title = title_key(paper["title"])
    return len(title) >= 18 and title in title_key(text)


def backfill_code_links(papers, key, limit):
    """Revisit a bounded number of accepted records on a rolling schedule."""
    now = datetime.now(timezone.utc)
    cutoff = (now - timedelta(days=28)).isoformat(timespec="seconds")
    candidates = [p for p in papers if p["status"] == "accepted" and not p.get("code_urls")
                  and p.get("code_checked_at", "") <= cutoff]
    candidates.sort(key=lambda paper: paper.get("code_checked_at", ""))
    checked, added, error = 0, 0, ""
    for paper in candidates[:limit]:
        title = paper["title"].replace('"', "")[:103]
        try:
            results = search(f'"{title}" site:github.com', key, 5)
        except (OSError, ValueError, KeyError) as exc:
            error = f"HTTP {exc.code}" if isinstance(exc, urllib.error.HTTPError) else type(exc).__name__
            break
        checked += 1
        paper["code_checked_at"] = now_iso()
        links = {link for result in results for link in github_links(str(result.get("url", "")))}
        for link in sorted(links):
            if repository_matches(paper, link):
                paper["code_urls"] = [link]
                added += 1
                break
    return {"checked": checked, "added": added, "error": error}
