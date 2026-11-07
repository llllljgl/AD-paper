import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, Mock
from radar.rolling import RollingSources, specs_for
from radar.official import official_candidate
from radar.core import source_venue, filter_collection_year

class RollingTests(unittest.TestCase):
    def setUp(self):
        self.now=datetime(2026,11,8,tzinfo=timezone.utc)
        self.config={'collection_start_year':2026,'official_sources':{'CVPR':{}},'rolling':{'enabled':True}}
    def index(self, venue, spec):
        year=2027 if '2027' in spec['catalog'] else 2026
        p=official_candidate(venue,year,f'https://openaccess.thecvf.com/content/CVPR{year}/html/a_paper.html','Industrial anomaly detection')
        return 1,[p]
    def collect(self, *args):
        return [],{'CVPR':{'status':'ok'}}
    def test_next_year_appears_and_unchanged_skips_llm_search(self):
        state={}
        with patch('radar.rolling.OfficialSources.index',side_effect=self.index), patch('radar.rolling.OfficialSources.collect',side_effect=self.collect), patch('radar.rolling.search_venues',return_value=({}, {}, 2)) as search:
            RollingSources(self.config,[],state,now=self.now).collect_with_search('key')
            self.assertEqual(search.call_count,2)
            self.assertIn('CVPR 2027',state['source_lifecycle'])
            RollingSources(self.config,[],state,now=self.now+timedelta(days=8)).collect_with_search('key')
            self.assertEqual(search.call_count,2)
    def test_stable_source_sleeps_but_can_reopen_on_change(self):
        state={}
        with patch('radar.rolling.OfficialSources.index',side_effect=self.index), patch('radar.rolling.OfficialSources.collect',side_effect=self.collect):
            for days in [0,30,60,91]:
                RollingSources(self.config,[],state,now=self.now+timedelta(days=days)).collect_with_search()
            self.assertEqual(state['source_lifecycle']['CVPR 2026']['phase'],'dormant')
            before=state['source_lifecycle']['CVPR 2026']['fingerprint']
            _,reports,_,_=RollingSources(self.config,[],state,now=self.now+timedelta(days=98)).collect_with_search()
            self.assertEqual(reports['CVPR 2026']['status'],'skipped')
            self.assertEqual(state['source_lifecycle']['CVPR 2026']['fingerprint'],before)
    def test_closure_requires_evidence_and_permanently_skips(self):
        self.config['rolling']['overrides']={'CVPR 2026':{'closed':True,'reason':'Final archive','evidence_url':'https://openaccess.thecvf.com/CVPR2026'}}
        with patch('radar.rolling.OfficialSources.index',side_effect=self.index), patch('radar.rolling.OfficialSources.collect',side_effect=self.collect):
            _,reports,_,_=RollingSources(self.config,[],{},now=self.now).collect_with_search()
        self.assertEqual(reports['CVPR 2026']['status'],'skipped')
        del self.config['rolling']['overrides']['CVPR 2026']['evidence_url']
        with patch('radar.rolling.OfficialSources.index',side_effect=ValueError('empty')):
            _,reports,_,_=RollingSources(self.config,[],{},now=self.now).collect_with_search()
        self.assertEqual(reports['CVPR 2026']['status'],'failed')
    def test_unpublished_does_not_close_and_failure_keeps_checkpoint(self):
        state={}
        with patch('radar.rolling.OfficialSources.index',side_effect=ValueError('empty')):
            RollingSources(self.config,[],state,now=self.now).collect_with_search()
        self.assertEqual(state['source_lifecycle']['CVPR 2027']['phase'],'awaiting_catalog')
        state['source_lifecycle']['CVPR 2026']={'fingerprint':'old'}
        with patch('radar.rolling.OfficialSources.index',side_effect=ValueError('empty')):
            _,reports,_,_=RollingSources(self.config,[],state,now=self.now).collect_with_search()
        self.assertEqual(reports['CVPR 2026']['status'],'failed')
        self.assertEqual(state['source_lifecycle']['CVPR 2026']['fingerprint'],'old')
    def test_future_url_serving_old_meeting_is_rejected(self):
        from radar.official import catalog_entries
        raw='<title>NeurIPS 2026 Schedule</title><div id="maincard_1"><div class="maincardBody">Industrial anomaly detection</div></div>'
        with self.assertRaisesRegex(ValueError,'requested meeting year'):
            catalog_entries('https://neurips.cc/Conferences/2027/AcceptedPapersInitial',2027,'neurips',raw)
        self.assertTrue(catalog_entries('https://neurips.cc/Conferences/2026/AcceptedPapersInitial',2026,'neurips',raw))

    def test_due_date_ignores_scheduler_second_jitter(self):
        state={'source_lifecycle':{'CVPR 2026':{'next_check_at':(self.now+timedelta(seconds=30)).isoformat()}}}
        with patch('radar.rolling.OfficialSources.index',side_effect=self.index), patch('radar.rolling.OfficialSources.collect',side_effect=self.collect):
            _,reports,_,_=RollingSources(self.config,[],state,now=self.now).collect_with_search()
        self.assertEqual(reports['CVPR 2026']['status'],'ok')

    def test_pmlr_resolves_real_volume_and_excludes_workshops(self):
        cfg={'official_sources':{'ICML':{}}}
        get=Mock(return_value='<li><a href="/v999/"><b>Volume 999</b></a> Proceedings of ICML 2027</li><li><a href="/v998/">Volume 998</a> ICML 2027 Workshop</li>')
        self.assertEqual(specs_for(cfg,'ICML',2027,get),[{'catalog':'https://proceedings.mlr.press/v999/','format':'pmlr'}])
    def test_history_retained_and_submissions_not_labeled_accepted(self):
        papers=[{'published':'2026','venue':'CVPR 2026'},{'published':'2027','venue':'ICLR 2027'}]
        self.assertEqual(filter_collection_year(papers,None),papers)
        self.assertEqual(source_venue('Submitted to ICLR 2027'),'arXiv / 未确认会议')
