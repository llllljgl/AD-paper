"""DeepSeek's independent search, bounded by the configured venue list."""

import json
import re
import urllib.error
from urllib.parse import urlsplit

from .core import request

SEARCH_URL = "https://api.deepseek.com/v1/tools/search"


def search(query, key, count):
    if not 1 <= len(query.strip()) <= 128:
        raise ValueError("DeepSeek search query must be 1 to 128 characters")
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



def backfill_code_links(papers, key, limit=100, config=None):
    from .codecheck import backfill
    return backfill(papers, key, config or {"model": "deepseek-flash"}, limit)
