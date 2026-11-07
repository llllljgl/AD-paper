import json
import unittest
from unittest.mock import Mock, patch
from pathlib import Path
from radar.core import Agent
from radar.official import ANOMALY
from radar.investigate import allowed, fetch_text, investigate, investigation_query
from test_radar import paper

class InvestigationTests(unittest.TestCase):
    def test_blocks_pdf_download_and_private_targets(self):
        for url in ['https://arxiv.org/pdf/1234.12345', 'https://arxiv.org/a.pdf',
                    'https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=1',
                    'https://127.0.0.1/', 'https://arxiv.org@evil.example/',
                    'https://evil.example/pretend.html']:
            self.assertFalse(allowed(url), url)
        self.assertTrue(allowed('https://maticfuc.github.io/anomaly_vfm/'))
        self.assertTrue(allowed('https://arxiv.org/html/2605.28428v1'))

    def test_pdf_content_type_rejected_before_read(self):
        response = Mock(); response.headers.get_content_type.return_value = 'application/pdf'
        context = Mock(); context.__enter__ = Mock(return_value=response); context.__exit__ = Mock(return_value=False)
        opener = Mock(); opener.open.return_value = context
        with patch('radar.investigate.urllib.request.build_opener', return_value=opener):
            with self.assertRaises(ValueError): fetch_text('https://arxiv.org/abs/2605.28428')
        response.read.assert_not_called()

    def test_search_snippet_is_not_evidence_and_wrong_paper_is_rejected(self):
        hits = [{'url':'https://lab.github.io/paper/', 'title':'Industrial anomaly detection', 'snippet':'Uses MVTec'}]
        with patch('radar.investigate.search', return_value=hits), patch('radar.investigate.fetch_text', return_value='Another paper uses MVTec'):
            result = investigate(paper(), 'test')
        self.assertEqual(result['sources'], [])
        self.assertEqual(len(result['searches']), 3)

    def test_invented_evidence_stays_unresolved(self):
        config=json.loads((Path(__file__).resolve().parents[1]/'config.json').read_text())
        agent=Agent(config, Mock())
        result={'decision':'keep','topic':'其他','reason':'相关','summary_zh':'方法简介','tags':['工业','视觉'],
                'evidence':[{'url':paper()['url'],'quote':'invented industrial evaluation'}]}
        response={'choices':[{'finish_reason':'stop','message':{'content':json.dumps(result)}}]}
        with patch('radar.core.request',return_value=json.dumps(response).encode()):
            self.assertEqual(agent.decide(paper())['decision'],'verify')
            self.assertEqual(agent.decide(paper(),verified=True)['decision'],'pending')

    def test_long_queries_preserve_quotes_and_respect_api_limit(self):
        for title in ['LACToS: Local Anomaly Detection via Conditional Typicality of Superpixels', 'Very long title ' * 30]:
            query = investigation_query(title, 'Which industrial datasets and experimental settings are used? ' * 10)
            self.assertLessEqual(len(query), 128)
            self.assertEqual(query.count('"'), 2)

    def test_audit_missed_title_enters_candidates(self):
        self.assertTrue(ANOMALY.search('Unification of Closed-Open Industrial Detection Scenarios: New Large-Scale Benchmarks'))

    def test_investigation_budget_preserves_pending(self):
        config={'max_investigations':0,'max_llm_calls':10}
        agent=Agent(config,Mock())
        agent.decide=Mock(return_value={'decision':'verify','reason':'待查','topic':'其他','summary_zh':'待查','tags':['工业','视觉']})
        with patch('radar.investigate.investigate') as tool:
            self.assertEqual(agent.review(paper())['status'],'pending')
            tool.assert_not_called()
