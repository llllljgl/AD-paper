import json
import unittest
from unittest.mock import patch
from radar.codecheck import verify, visible_codes, paper_key, judge, backfill, snapshot
from test_radar import paper

class CodeTests(unittest.TestCase):
    def test_awesome_list_never_calls_model_or_api(self):
        with patch('radar.codecheck.snapshot') as api,patch('radar.codecheck.judge') as llm:
            result=verify(paper(),'https://github.com/M-3LAB/awesome-3d-anomaly-detection','key',{}, {})
        self.assertEqual(result['status'],'rejected');api.assert_not_called();llm.assert_not_called()
    def test_accept_requires_second_review_and_exact_evidence(self):
        data={'readme':'Official implementation of Industrial anomaly detection','url':'https://github.com/lab/repo'}
        good={'decision':'accept','kind':'official_implementation','reason':'相关','evidence':[{'quote':data['readme']}]}
        stats={'model_calls':0}
        with patch('radar.codecheck.snapshot',return_value=data),patch('radar.codecheck.judge',side_effect=[good,{**good,'decision':'reject','kind':'unofficial'}]) as llm:
            row=verify(paper(),data['url'],'key',{},stats)
        self.assertEqual(llm.call_count,2);self.assertEqual(row['status'],'rejected')
        p=paper(code_urls=[data['url']],code_checks={data['url']:row})
        self.assertEqual(visible_codes(p),[])
        row['status']='verified';self.assertEqual(visible_codes(p),[data['url']])
        p['title']='Another paper';self.assertEqual(visible_codes(p),[])
    def test_hallucinated_quote_prevents_acceptance(self):
        result={'decision':'accept','kind':'official_implementation','reason':'相关','evidence':[{'quote':'Invented official implementation claim'}]}
        response={'choices':[{'finish_reason':'stop','message':{'content':json.dumps(result)}}]}
        with patch('radar.codecheck.request',return_value=json.dumps(response).encode()):
            checked=judge(paper(),{'readme':'Unrelated text'},'key',{'model':'test'},{'model_calls':0})
        self.assertEqual(checked['decision'],'uncertain')
    def test_placeholder_and_fork_fail_without_model(self):
        with patch('radar.codecheck.request',return_value=b'{"fork":true,"size":1}'):
            with self.assertRaises(ValueError):snapshot('https://github.com/lab/repo')
    def test_missing_identity_never_reaches_model(self):
        with patch('radar.codecheck.snapshot',return_value={'readme':'Implementation of some other paper'}),patch('radar.codecheck.judge') as judge_mock:
            row=verify(paper(),'https://github.com/lab/repo','key',{}, {})
        self.assertEqual(row['status'],'pending');judge_mock.assert_not_called()
    def test_rejected_list_is_removed_and_alternative_is_searched(self):
        item=paper(status='accepted',code_urls=['https://github.com/lab/awesome-list'])
        with patch('radar.deepseek.search',return_value=[]),patch('radar.codecheck.search',return_value=[]) as search_mock:
            result=backfill([item],'key',{'model':'test'},1)
        self.assertEqual(item['code_urls'],[])
        self.assertEqual(search_mock.call_count,2)
        self.assertEqual(result['removed'],1)
        self.assertIn('https://github.com/lab/awesome-list',item['code_candidates'])
    def test_valid_readme_without_source_files_is_placeholder(self):
        import base64
        replies=[{'full_name':'lab/repo','size':3,'default_branch':'main'},
                 {'content':base64.b64encode(b'Official implementation Industrial anomaly detection').decode()},
                 {'tree':[{'path':'README.md','type':'blob'}]}]
        with patch('radar.codecheck.request',side_effect=[json.dumps(x).encode() for x in replies]):
            with self.assertRaisesRegex(ValueError,'no implementation'):snapshot('https://github.com/lab/repo')
