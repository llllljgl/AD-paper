"""Read-only, full-candidate comparison against a frozen production snapshot.

Uses production search queries, parsers, scope and model prompt. Audit deliberately
reviews all available abstracts, including records excluded by the lexical gate,
so a gate disagreement is visible. Model decisions are not ground-truth labels.
"""

import argparse
import hashlib
import json
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .core import Agent, Arxiv, has_industrial_visual_evidence, load_json, now_iso, save_json, title_key, venue_and_year
from .deepseek import search_venues
from .official import ANOMALY, OfficialSources, compare_discovery

ROOT = Path(__file__).resolve().parent.parent


def render(result):
    lines = ["# DeepSeek collection audit", "",
             f"Baseline commit: `{result['baseline_commit']}`", "",
             f"Model: `{result['model']}`; year: {result['year']}", "",
             "Same production search and review prompt; all candidates refreshed, with the scope gate recorded but bypassed for diagnostic review.",
             "Model disagreements require independent adjudication and are not measured false positives or false negatives.", "",
             "| Venue | Catalog | Existing accepted | Candidates | Abstracts | Model keep | Potential omissions | Accepted/model reject | Unresolved accepted |",
             "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for venue, source in result['sources'].items():
        rows = [r for r in result['records'] if r['venue'] == venue]
        accepted = [r for r in rows if r['baseline_status'] == 'accepted']
        verdict = lambda r: (r.get('review') or {}).get('decision')
        vals = [source.get('scanned', 0), len(accepted), len(rows),
                sum(bool(r['paper'].get('abstract')) for r in rows),
                sum(verdict(r) == 'keep' for r in rows),
                sum(verdict(r) == 'keep' and r['baseline_status'] != 'accepted' for r in rows),
                sum(verdict(r) == 'reject' for r in accepted),
                sum(verdict(r) is None for r in accepted)]
        lines.append('| ' + venue + ' | ' + ' | '.join(map(str, vals)) + ' |')
    lines.extend(['', f"Search calls: {result['search_calls']}; review calls: {result['review_calls']}",
                  f"Search errors: {json.dumps(result['search_errors'])}", '', '## Disagreements / unresolved accepted', ''])
    for row in result['records']:
        review = row.get('review') or {}
        decision = review.get('decision')
        if (row['baseline_status'] == 'accepted' and decision != 'keep') or (row['baseline_status'] != 'accepted' and decision == 'keep'):
            p = row['paper']
            lines.extend([f"- [{p['title']}]({p['url']}) — {row['venue']}; baseline={row['baseline_status']}; model={decision or 'unresolved'}; gate={row['passes_scope_gate']}",
                          '  ' + review.get('reason', row.get('review_error', 'No public abstract.'))])
    return '\n'.join(lines) + '\n'


def audit(venues, output):
    config = load_json(ROOT / 'config.json', {})
    unknown = set(venues) - config['official_sources'].keys()
    if unknown:
        raise ValueError(f'Unknown venues: {sorted(unknown)}')
    key = os.environ.get('DEEPSEEK_API_KEY')
    if not key:
        raise ValueError('DEEPSEEK_API_KEY is required')
    baseline_bytes = (ROOT / 'data/papers.json').read_bytes()
    baseline = json.loads(baseline_bytes)
    selected = [p for p in baseline if venue_and_year(p) in {(v, str(config['collection_year'])) for v in venues}]
    config['official_sources'] = {v: config['official_sources'][v] for v in venues}
    # Higher diagnostic budget, without changing production configuration.
    config['max_llm_calls'] = 300
    output.mkdir(parents=True, exist_ok=True)
    (output / 'baseline-papers.json').write_bytes(baseline_bytes)
    save_json(output / 'audit-config.json', config)
    result = dict(started_at=now_iso(), baseline_commit=os.environ.get('GITHUB_SHA', 'local'),
                  baseline_sha256=hashlib.sha256(baseline_bytes).hexdigest(),
                  model=os.environ.get('DEEPSEEK_MODEL') or config['model'],
                  year=config['collection_year'], sources={}, records=[], review_calls=0)
    found, errors, calls = search_venues(config, key)
    save_json(output / 'search-results.json', found)
    result.update(search_errors=errors, search_calls=calls)
    official = OfficialSources(config, selected)

    def checkpoint():
        save_json(output / 'audit.json', result)
        (output / 'summary.md').write_text(render(result), encoding='utf-8')

    for venue, spec in config['official_sources'].items():
        try:
            scanned, entries = official.index(venue, spec)
        except (OSError, ValueError, KeyError) as exc:
            result['sources'][venue] = dict(error=type(exc).__name__)
            checkpoint()
            continue
        save_json(output / f'catalog-{venue}.json', entries)
        keyword = {p['id']: p for p in entries if ANOMALY.search(f"{p['title']} {p.get('abstract', '')}")}
        matches = compare_discovery(entries, found.get(venue, []))
        old = {title_key(p['title']): p for p in selected if venue_and_year(p)[0] == venue}
        tracked = {p['id']: p for p in entries if title_key(p['title']) in old}
        candidates = {title_key(p['title']): p for p in {**keyword, **matches, **tracked}.values()}
        # Retain old records missing from today's catalog for explicit verification.
        for title, p in old.items():
            candidates.setdefault(title, p)
        indexed = {title_key(p['title']) for p in entries}
        rows = []
        for title, candidate in candidates.items():
            previous = old.get(title, {})
            paper = {**previous, **{k: v for k, v in candidate.items() if v}}
            rows.append(dict(venue=venue, baseline_status=previous.get('status', 'absent'),
                             in_official_catalog=title in indexed,
                             keyword_hit=candidate['id'] in keyword,
                             deepseek_hit=candidate['id'] in matches,
                             baseline=previous, paper=paper))

        def refresh(row):
            try:
                detail = official.detail(row['paper'])
                row['paper'].update({k: v for k, v in detail.items() if v})
                row['detail_status'] = 'ok'
            except (OSError, ValueError, KeyError) as exc:
                row['detail_status'] = type(exc).__name__
            row['passes_scope_gate'] = has_industrial_visual_evidence(row['paper'])
            return row

        with ThreadPoolExecutor(max_workers=4) as pool:
            rows = list(pool.map(refresh, rows))
        result['records'].extend(rows)
        result['sources'][venue] = dict(scanned=scanned, candidates=len(rows), keyword_hits=len(keyword),
                                        search_matched=len(matches), search_results=len(found.get(venue, [])))
        checkpoint()
        print(f'{venue}: {scanned} catalog entries, {len(rows)} candidates refreshed', flush=True)

    agent = Agent(config, Arxiv())
    for index, row in enumerate(result['records']):
        if not row['paper'].get('abstract'):
            row['review_error'] = 'No public abstract'
        else:
            try:
                # Deliberately no lexical gate: compare its exclusions with the same model prompt.
                row['review'] = agent.decide(row['paper'], verified=True)
            except (OSError, ValueError, KeyError, IndexError, TypeError, RuntimeError) as exc:
                row['review_error'] = type(exc).__name__
                if isinstance(exc, OSError) or agent.calls >= config['max_llm_calls']:
                    result['review_blocked'] = True
                    result['review_calls'] = agent.calls
                    checkpoint()
                    break
        result['review_calls'] = agent.calls
        checkpoint()
        print(f"Review {index + 1}/{len(result['records'])}: {row['venue']} {(row.get('review') or {}).get('decision', 'unresolved')}", flush=True)
    result['finished_at'] = now_iso()
    result['unreviewed'] = sum(not r.get('review') for r in result['records'])
    checkpoint()
    # Never write production papers, state or README.
    if (ROOT / 'data/papers.json').read_bytes() != baseline_bytes:
        raise RuntimeError('Production baseline changed during audit')
    if errors or result.get('review_blocked') or any('error' in s for s in result['sources'].values()):
        raise RuntimeError('Audit incomplete; inspect saved evidence')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--venues', default='CVPR,ICLR,TPAMI,TIP')
    parser.add_argument('--output', type=Path, default=ROOT / 'audit-output')
    args = parser.parse_args()
    audit([v.strip() for v in args.venues.split(',') if v.strip()], args.output)
