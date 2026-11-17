import json
import unittest
from unittest.mock import Mock

from radar.core import merge, source_venue
from radar.official import OfficialSources, metadata_url
from radar.rolling import specs_for


class AcmmmTests(unittest.TestCase):
    def setUp(self):
        self.url = 'https://2026.acmmm.org/site/technical-programme.html'
        self.config = {'collection_year': 2026, 'official_sources': {
            'ACMMM': {'catalog': self.url, 'format': 'acmmm'}}}
        self.rows = [
            {'paper_id': 'mfp1', 'title': 'Industrial anomaly detection with reconstruction',
             'abstract': 'Visual defect detection on MVTec images.',
             'authors': ['A. Author'], 'track': 'Main Track'},
            {'paper_id': 'mfp2', 'title': 'Multi-view industrial defect segmentation',
             'abstract': 'Pixel-level localization on Real-IAD.', 'track': 'Main Track'},
        ]
        self.data = {'entries': [
            {'id': 1, 'type': 'oral', 'papers': self.rows},
            {'id': 2, 'type': 'poster', 'papers': self.rows},
            {'id': 3, 'type': 'workshop', 'papers': [
                {'paper_id': 'ws1', 'title': 'Workshop anomaly detection paper', 'track': 'Main Track'}]},
        ]}
        self.get = Mock(side_effect=lambda url: (
            '<title>ACM Multimedia 2026 Conference — Technical Programme</title>'
            if url == self.url else json.dumps(self.data)))

    def test_aliases_and_submissions(self):
        for name in ['ACMMM 2026', 'ACM MM 2026', 'ACM Multimedia 2026', "ACM Multimedia (MM '26)"]:
            with self.subTest(name=name):
                self.assertEqual(source_venue('Accepted at ' + name), 'ACMMM 2026（作者声明）')
        self.assertEqual(source_venue('Under review at ACM MM 2027'), 'arXiv / 未确认会议')

    def test_official_catalog_preserves_abstracts_deduplicates_and_excludes_workshops(self):
        source = OfficialSources(self.config, [], get=self.get)
        scanned, papers = source.index('ACMMM', self.config['official_sources']['ACMMM'])
        self.assertEqual(scanned, 2)
        self.assertEqual(papers[0]['authors'], ['A. Author'])
        self.assertEqual(papers[0]['abstract'], self.rows[0]['abstract'])
        self.assertEqual(len({p['official_url'] for p in papers}), 2)
        # A programme session is shared by multiple papers; merging must retain both.
        initial = merge([], papers, '2026-11-17T00:00:00+00:00')
        refreshed = merge(initial, papers, '2026-11-18T00:00:00+00:00')
        self.assertEqual(len(refreshed), 2)
        source.collect()
        self.assertEqual(self.get.call_count, 4)  # Two index reads; no HTML detail requests.

    def test_wrong_year_and_empty_catalog_rejected(self):
        source = OfficialSources({**self.config, 'collection_year': 2027}, [], get=self.get)
        with self.assertRaisesRegex(ValueError, 'requested meeting year'):
            source.index('ACMMM', self.config['official_sources']['ACMMM'])
        self.data['entries'] = []
        with self.assertRaisesRegex(ValueError, 'No paper entries'):
            OfficialSources(self.config, [], get=self.get).index('ACMMM', self.config['official_sources']['ACMMM'])

    def test_rolling_year_and_metadata_hosts(self):
        self.assertEqual(specs_for(self.config, 'ACMMM', 2027, self.get), [{
            'catalog': 'https://2027.acmmm.org/site/technical-programme.html', 'format': 'acmmm'}])
        self.assertTrue(metadata_url('https://2027.acmmm.org/site/program-data.json'))
        self.assertFalse(metadata_url('https://2026.acmmm.org.evil.example/site/program-data.json'))
        self.assertFalse(metadata_url('https://2026.acmmm.org/site/file.pdf'))


if __name__ == '__main__':
    unittest.main()
