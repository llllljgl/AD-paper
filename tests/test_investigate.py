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

    def test_real_but_insufficient_quotes_trigger_investigation(self):
        config=json.loads((Path(__file__).resolve().parents[1]/'config.json').read_text())
        cases = [
            ('CausalPulse: Root Cause Analysis in Smart Manufacturing', 'We analyze industrial manufacturing time series.'),
            ('Visual anomaly detection', 'We study visual anomaly detection on generic images.'),
            ('DeGlare: Industrial image restoration', 'We remove reflections from industrial images.'),
        ]
        for title, abstract in cases:
            with self.subTest(title=title):
                item=paper(title=title,abstract=abstract)
                result={'decision':'keep','topic':'其他','reason':'相关','summary_zh':'方法简介','tags':['工业','视觉'],
                        'evidence':[{'url':item['url'],'quote':abstract}]}
                response={'choices':[{'finish_reason':'stop','message':{'content':json.dumps(result)}}]}
                with patch('radar.core.request',return_value=json.dumps(response).encode()):
                    agent=Agent(config,Mock())
                    self.assertEqual(agent.decide(item)['decision'],'verify')
                    self.assertEqual(agent.decide(item,verified=True)['decision'],'pending')

    def test_mixed_medical_industrial_and_3d_evidence_are_allowed(self):
        from radar.core import supports_scope
        for quote in ['Anomaly localization evaluated on Real3D-AD and AnomalyShapeNet.',
                      'Anomaly detection on MVTec AD and medical datasets.',
                      'Defect inspection using industrial point clouds.']:
            self.assertTrue(supports_scope(paper(), {'evidence':[{'quote':quote}]}), quote)

    def test_search_failure_does_not_lose_other_evidence(self):
        import urllib.error
        failure=urllib.error.HTTPError('https://api.deepseek.com',500,'error',{},None)
        item=paper(code_urls=['https://github.com/lab/repo'])
        stats={'search_calls':0}
        with patch('radar.investigate.search',side_effect=[failure,[],[]]), patch(
                'radar.investigate.fetch_text',return_value=item['title']+' uses MVTec AD.'):
            result=investigate(item,'test',stats=stats)
        self.assertTrue(result['sources'])
        self.assertEqual(stats,{'search_calls':3,'search_errors':1})
        self.assertEqual(result['failures'][0]['error'],'HTTP 500')
        auth=urllib.error.HTTPError('https://api.deepseek.com',402,'balance',{},None)
        with patch('radar.investigate.search',side_effect=auth):
            with self.assertRaises(urllib.error.HTTPError): investigate(item,'test')

    def test_excerpt_keeps_body_instead_of_repeating_navigation(self):
        from radar.investigate import excerpt, Text
        text='Industrial dataset navigation. '*250+'MVTec experimental evidence. '+'x'*16000
        result=excerpt(text)
        self.assertIn('MVTec experimental evidence.',result)
        self.assertLessEqual(len(result),14000)
        self.assertEqual(''.join(Text('<nav>Hidden navigation</nav><p>Paper body</p>').parts),'Paper body')

    def test_source_ids_and_valid_subset_preserve_supported_decision(self):
        config=json.loads((Path(__file__).resolve().parents[1]/'config.json').read_text())
        result={'decision':'keep','topic':'其他','reason':'相关','summary_zh':'方法简介','tags':['工业','视觉'],
            'evidence':[{'source_id':'S1','quote':'A method for MVTec'},
                        {'source_id':'S1','quote':'fabricated evaluation statement'}]}
        response={'choices':[{'finish_reason':'stop','message':{'content':json.dumps(result)}}]}
        with patch('radar.core.request',return_value=json.dumps(response).encode()):
            reviewed=Agent(config,Mock()).decide(paper())
        self.assertEqual(reviewed['decision'],'keep')
        self.assertEqual(reviewed['evidence'],[{'url':paper()['url'],'quote':'A method for MVTec'}])

    def test_final_verify_means_pending_and_failed_review_preserves_sources(self):
        config=json.loads((Path(__file__).resolve().parents[1]/'config.json').read_text())
        result={'decision':'verify','topic':'其他','reason':'缺证据','summary_zh':'待调查','tags':['工业','视觉'],'evidence':[]}
        response={'choices':[{'finish_reason':'stop','message':{'content':json.dumps(result)}}]}
        agent=Agent(config,Mock())
        with patch('radar.core.request',return_value=json.dumps(response).encode()):
            self.assertEqual(agent.decide(paper(),verified=True)['decision'],'pending')
        item=paper(); investigation={'sources':[{'url':'https://lab.github.io/paper/','text':'Evidence'}]}
        agent.decide=Mock(side_effect=[result,ValueError('bad final response')])
        with patch('radar.investigate.investigate',return_value=investigation):
            with self.assertRaises(ValueError): agent.review(item)
        self.assertEqual(item['investigation'],investigation)

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
