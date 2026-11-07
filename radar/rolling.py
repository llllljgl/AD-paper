"""Year-aware source lifecycle. Never infer permanent closure from silence."""
import hashlib
import json
import re
import urllib.error
from datetime import datetime, timedelta, timezone
from urllib.parse import urljoin

from .official import OfficialSources, get_metadata, ANCHOR, plain_text, metadata_url
from .deepseek import search_venues

TEMPLATES = {
    'CVPR': ('https://openaccess.thecvf.com/CVPR{year}?day=all', 'cvf'),
    'ICCV': ('https://openaccess.thecvf.com/ICCV{year}?day=all', 'cvf'),
    'ECCV': ('https://eccv.ecva.net/Conferences/{year}/AcceptedPapers', 'eccv'),
    'NeurIPS': ('https://neurips.cc/Conferences/{year}/AcceptedPapersInitial', 'neurips'),
    'ICLR': ('https://proceedings.iclr.cc/paper_files/paper/{year}', 'iclr'),
    'IJCAI': ('https://ijcai.org/proceedings/{year}/', 'ijcai'),
}


def specs_for(config, venue, year, get):
    base = config['official_sources'][venue]
    if 'issn' in base or 'crossref_container' in base:
        return [dict(base)]
    if (venue == 'ICCV' and year % 2 == 0) or (venue == 'ECCV' and year % 2):
        return []
    if venue == 'ICML':
        # PMLR volume numbers are not calendar years. Resolve from the publisher index.
        raw = get('https://proceedings.mlr.press/')
        specs = []
        for block in re.findall(r'<li\b[^>]*>(.*?)</li>', raw, re.S):
            label = plain_text(block)
            links = ANCHOR.findall(block)
            if not links:
                continue
            href = links[0][0]
            url = urljoin('https://proceedings.mlr.press/', href)
            if re.fullmatch(rf'(?:Volume \d+\s+)?Proceedings of ICML {year}', label) and metadata_url(url):
                specs.append({'catalog': url.rstrip('/')+'/', 'format': 'pmlr'})
        return specs
    url, kind = TEMPLATES[venue]
    specs = [{'catalog': url.format(year=year), 'format': kind}]
    if venue == 'ICLR':
        specs.append({'catalog': f'https://iclr.cc/Conferences/{year}/AcceptedPapers', 'format': 'neurips'})
    return specs


class RollingSources:
    def __init__(self, config, existing, state, get=None, now=None):
        self.config, self.existing, self.state = config, existing, state
        self.get = get or get_metadata
        self.now = now or datetime.now(timezone.utc)

    def collect_with_search(self, key=''):
        rows, reports, errors, calls = [], {}, {}, 0
        registry = self.state.setdefault('source_lifecycle', {})
        first = self.config.get('collection_start_year', 2026)
        settings = self.config.get('rolling', {})
        # Cache shared publisher index within one run.
        pages = {}
        def get(url):
            if url not in pages:
                pages[url] = self.get(url)
            return pages[url]
        for year in range(first, self.now.year + 2):
            for venue, base in self.config['official_sources'].items():
                name = f'{venue} {year}'
                old = registry.get(name, {})
                override = settings.get('overrides', {}).get(name, {})
                if override.get('closed'):
                    if not override.get('evidence_url') or not override.get('reason'):
                        reports[name] = {'status': 'failed', 'reason': 'Closure requires evidence_url and reason'}
                    else:
                        registry[name] = {**old, 'phase': 'closed', **override}
                        reports[name] = {'status': 'skipped', 'reason': '明确关闭：' + override['reason']}
                    continue
                # Compare dates: scheduler jitter must not turn a weekly scan into fortnightly.
                if old.get('next_check_at') and self.now.date() < datetime.fromisoformat(old['next_check_at']).date():
                    reports[name] = {'status': 'skipped', 'reason': old.get('phase', '') + '，下次检查 ' + old['next_check_at']}
                    continue
                source, snapshot, spec = None, None, None
                try:
                    choices = specs_for(self.config, venue, year, get)
                    for candidate in choices:
                        cfg = {**self.config, 'collection_year': year, 'official_sources': {venue: candidate}}
                        trial = OfficialSources(cfg, self.existing, get=get)
                        try:
                            snapshot = trial.index(venue, candidate)
                            if snapshot[1]:
                                source, spec = trial, candidate
                                break
                        except urllib.error.HTTPError as exc:
                            if exc.code not in (404, 410):
                                raise
                        except ValueError:
                            # A previously valid source becoming unparseable is a failure below.
                            continue
                    if source is None:
                        if old.get('fingerprint'):
                            raise ValueError('Previously published catalog disappeared or changed format')
                        phase = 'not_scheduled' if not choices and venue in ('ICCV', 'ECCV') else 'awaiting_catalog'
                        registry[name] = {**old, 'phase': phase, 'last_checked_at': self.now.isoformat(),
                                          'next_check_at': (self.now + timedelta(days=14)).isoformat()}
                        reports[name] = {'status': 'skipped', 'reason': phase}
                        continue
                    fingerprint = hashlib.sha256(json.dumps([(p['id'], p['title'], p.get('abstract','')) for p in sorted(snapshot[1], key=lambda p:p['id'])], ensure_ascii=False).encode()).hexdigest()
                    changed = fingerprint != old.get('fingerprint')
                    stable_since = self.now.isoformat() if changed else old.get('stable_since', self.now.isoformat())
                    checks = 0 if changed else old.get('unchanged_checks', 0) + 1
                    stable = (not changed and checks >= 3 and
                              (self.now-datetime.fromisoformat(stable_since)).days >= 90)
                    journal = 'issn' in base
                    # Journals retain a weekly previous-year correction window.
                    dormant = stable and (not journal or year < self.now.year-1)
                    interval = 90 if dormant else 7
                    hits, search_errors, search_calls = {}, {}, 0
                    search_due = changed or not old.get('last_search_at') or old.get('search_failed')
                    if key and search_due:
                        hits, search_errors, search_calls = search_venues(source.config, key)
                    calls += search_calls
                    errors.update({name: value for value in search_errors.values()})
                    # Reuse the validated catalog; collect still refreshes pending details.
                    source.index = lambda *_args, snap=snapshot: snap
                    found, result = source.collect(hits)
                    rows.extend(found)
                    reports[name] = {**result[venue], 'phase': 'dormant' if dormant else 'active',
                                     'catalog_changed': changed, 'search_skipped_unchanged': not search_due}
                    record = {**old, 'phase': 'dormant' if dormant else 'active', 'fingerprint': fingerprint,
                              'stable_since': stable_since, 'unchanged_checks': checks,
                              'last_checked_at': self.now.isoformat(),
                              'next_check_at': (self.now+timedelta(days=interval)).isoformat(),
                              'catalog': spec.get('catalog', 'Crossref'), 'search_failed': bool(search_errors)}
                    # Partial detail refresh must not sleep for a quarter.
                    if reports[name].get('details_deferred') or reports[name].get('details_failed'):
                        record['next_check_at'] = (self.now+timedelta(days=7)).isoformat()
                    if key and search_due and not search_errors:
                        record['last_search_at'] = self.now.isoformat()
                    registry[name] = record
                except (OSError, ValueError, KeyError) as exc:
                    reports[name] = {'status': 'failed', 'reason': f'HTTP {exc.code}' if isinstance(exc, urllib.error.HTTPError) else str(exc)[:160]}
                    # Preserve the last successful fingerprint and retry next run.
        return rows, reports, errors, calls
