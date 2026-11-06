import json
import os
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import Mock, patch

from radar.core import Agent, Arxiv, canonical_id, merge, parse_feed, run, save_json, validate_review
from radar.__main__ import LIST_END, LIST_START, build
from radar.official import OfficialSources, metadata_url, publisher_candidate

ROOT = Path(__file__).resolve().parent.parent


def paper(**changes):
    return {"id": "2601.00001", "version": "2601.00001v1", "title": "Industrial anomaly detection",
            "published": "2026-01-01T00:00:00Z", "updated": "2026-01-01T00:00:00Z", "abstract": "A method for MVTec",
            "authors": ["Researcher"], "status": "pending", "topic": "待分类", "summary_zh": "", "reason": "等待",
            "url": "https://arxiv.org/abs/2601.00001", "pdf_url": "https://arxiv.org/pdf/2601.00001",
            "code_urls": [], "venue": "arXiv / 未确认会议", "added_at": "2026-01-02T00:00:00Z", **changes}


class RadarTests(unittest.TestCase):
    def test_id_versions_and_old_style(self):
        self.assertEqual(canonical_id("http://arxiv.org/abs/2601.00001v12"), "2601.00001")
        self.assertEqual(canonical_id("http://arxiv.org/abs/cs/9901001v2"), "cs/9901001")

    def test_feed_source_fields_and_no_fabricated_code(self):
        raw = b'''<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom" xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/"><opensearch:totalResults>1</opensearch:totalResults><entry><id>http://arxiv.org/abs/2601.00001v2</id><title>A title</title><summary>Code https://github.com/lab/repo.</summary><published>2026-01-01T00:00:00Z</published><updated>2026-01-02T00:00:00Z</updated><author><name>A</name></author><arxiv:comment>CVPR 2026</arxiv:comment><category term="cs.CV"/></entry></feed>'''
        items, total = parse_feed(raw)
        self.assertEqual(total, 1)
        self.assertEqual(items[0]["code_urls"], ["https://github.com/lab/repo"])
        self.assertEqual(items[0]["id"], "2601.00001")
        self.assertEqual(items[0]["comment"], "CVPR 2026")

    def test_duplicate_preserves_review_and_first_seen(self):
        old = paper(status="accepted", summary_zh="简介")
        result = merge([old], [paper(), paper()], "2026-02-01T00:00:00Z")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["status"], "accepted")
        self.assertEqual(result[0]["summary_zh"], "简介")
        self.assertEqual(result[0]["added_at"], old["added_at"])

    def test_arxiv_scan_preserves_official_record_with_same_title(self):
        official = paper(id="cvpr:example", title="Industrial Anomaly Detection!", status="accepted",
                         venue="CVPR 2026", official_url="https://example.org/proceedings/1")
        result = merge([official], [paper()], "2026-02-01T00:00:00Z")
        self.assertEqual(result, [official])

    def test_revision_requires_new_review(self):
        result = merge([paper(status="accepted", summary_zh="Old")], [paper(updated="2026-02-02T00:00:00Z")], "today")
        self.assertEqual(result[0]["status"], "pending")
        self.assertEqual(result[0]["summary_zh"], "")

    def test_pagination_and_incomplete_feed(self):
        source = Arxiv()
        config = {"arxiv_query": "all:industrial", "page_size": 1, "max_candidates": 10}
        date = datetime(2026, 1, 1, tzinfo=timezone.utc)
        source.get = Mock(side_effect=[([paper()], 2), ([paper(id="other")], 2)])
        self.assertEqual(len(source.collect(config, date, date)), 2)
        source.get = Mock(side_effect=[([paper()], 2), ([], 2)])
        with self.assertRaisesRegex(ValueError, "Incomplete"):
            source.collect(config, date, date)
        source.get = Mock(return_value=([paper()], 20))
        with self.assertRaisesRegex(ValueError, "Too many"):
            source.collect(config, date, date)

    def test_bounded_agent_verifies_once(self):
        config = json.loads((ROOT / "config.json").read_text())
        source = Mock()
        source.verify.return_value = paper(abstract="Verified abstract")
        agent = Agent(config, source)
        agent.decide = Mock(side_effect=[{"decision": "verify", "reason": "含糊"},
            {"decision": "keep", "reason": "工业评估", "topic": "其他", "summary_zh": "中文简介", "tags": ["工业视觉", "定位"]}])
        result = agent.review(paper())
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(result["abstract"], "Verified abstract")
        self.assertEqual(agent.decide.call_count, 2)
        source.verify.assert_called_once()

    def test_review_validation_rejects_bad_model_output(self):
        with self.assertRaises(ValueError):
            validate_review({"decision": "verify", "topic": "其他", "summary_zh": "简介", "reason": "含糊"}, ["其他"], False)
        with self.assertRaises(ValueError):
            validate_review({"decision": "keep", "topic": "invented"}, ["其他"], True)

    def test_deepseek_payload_and_output(self):
        config = json.loads((ROOT / "config.json").read_text())
        agent = Agent(config, Mock())
        decision = {"decision": "keep", "topic": "其他", "reason": "相关", "summary_zh": "方法简介", "tags": ["工业视觉", "定位"]}
        response = {"choices": [{"finish_reason": "stop", "message": {"content": json.dumps(decision)}}]}
        empty = {"choices": [{"finish_reason": "stop", "message": {"content": " "}}]}
        replies = [json.dumps(result).encode() for result in (empty, response)]
        with patch("radar.core.request", side_effect=replies) as req:
            self.assertEqual(agent.decide(paper()), decision)
            self.assertEqual(req.call_count, 2)
            self.assertEqual(req.call_args.args[0], "https://api.deepseek.com/chat/completions")
            self.assertEqual(req.call_args.args[1]["response_format"], {"type": "json_object"})

    def test_checkpoint_backfill_and_provider_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            save_json(root / "config.json", json.loads((ROOT / "config.json").read_text()))
            source = Mock()
            source.collect.return_value = [
                paper(published="2025-12-01T00:00:00Z", venue="CVPR 2026（作者声明）"),
                paper(id="future", title="Future venue", venue="WACV 2027（作者声明）"),
            ]
            with patch.dict(os.environ, {"DEEPSEEK_API_KEY": ""}):
                state = run(root, source=source)
                checkpoint = state["last_collected_until"]
                run(root, since="2026-01-01", until="2026-01-31", no_llm=True, source=source)
            saved = json.loads((root / "data/state.json").read_text())
            self.assertEqual(saved["last_collected_until"], checkpoint)
            collected = json.loads((root / "data/papers.json").read_text())
            self.assertEqual([p["id"] for p in collected], ["2601.00001"])
            source.collect.side_effect = RuntimeError("offline")
            before = (root / "data/papers.json").read_bytes()
            with self.assertRaises(RuntimeError):
                run(root, source=source)
            self.assertEqual((root / "data/papers.json").read_bytes(), before)
            source.collect.side_effect = None
            with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test"}), patch.object(Agent, "review", side_effect=ValueError("refusal")):
                result = run(root, source=source)
            self.assertEqual(result["pending"], 1)
            self.assertEqual(result["review_errors"], 1)
            self.assertFalse(result["review_blocked"])

    def test_review_continues_after_an_isolated_bad_reply(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            save_json(root / "config.json", json.loads((ROOT / "config.json").read_text()))
            source = Mock()
            source.collect.return_value = [paper(), paper(id="second", title="Second paper")]
            with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test"}), patch.object(
                    Agent, "review", side_effect=[ValueError("empty"), {"status": "accepted"}]):
                state = run(root, source=source)
            saved = json.loads((root / "data/papers.json").read_text())
            self.assertEqual({p["id"]: p["status"] for p in saved},
                             {"2601.00001": "pending", "second": "accepted"})
            self.assertEqual(state["review_errors"], 1)
            self.assertFalse(state["review_blocked"])

    def test_readme_groups_reviewed_entries_and_collapses_tip(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            readme = root / "README.md"
            readme.write_text(f"# Paper list\n{LIST_START}\nOld content\n{LIST_END}\nKeep this text.\n", encoding="utf-8")
            save_json(root / "data/papers.json", [
                paper(title="A | B", status="accepted", venue="CVPR 2026（作者声明）", tags=["视觉", "定位"], summary_zh="一句 Tip"),
                paper(id="old", title="Older entry", status="accepted", venue="CVPR 2025（作者声明）", topic="原分类"),
                paper(id="journal", title="Journal entry", status="accepted", journal_ref="Pattern Recognition, vol. 100, 2025"),
                paper(id="pending", title="Pending entry"),
                paper(id="rejected", title="Rejected entry", status="rejected"),
            ])
            build(root)
            result = readme.read_text(encoding="utf-8")
            self.assertEqual(result.count("### CVPR 2026\n"), 1)
            self.assertEqual(result.count("### CVPR 2025\n"), 1)
            self.assertIn("### Pattern Recognition 2025\n", result)
            self.assertLess(result.index("A &#124; B"), result.index("Older entry"))
            self.assertIn("<details><summary>查看 Tip</summary><p>一句 Tip</p></details>", result)
            self.assertIn("<code>原分类</code>", result)
            self.assertNotIn("Pending entry", result)
            self.assertNotIn("Rejected entry", result)
            self.assertTrue(result.endswith("Keep this text.\n"))
            build(root)
            self.assertEqual(readme.read_text(encoding="utf-8"), result)
            save_json(root / "config.json", {"collection_year": 2026})
            build(root)
            result = readme.read_text(encoding="utf-8")
            self.assertIn("### CVPR 2026\n", result)
            self.assertNotIn("### CVPR 2025\n", result)
            self.assertNotIn("### Pattern Recognition 2025\n", result)

    def test_catalog_comparison_enriches_reviewed_record_and_rejects_unverified_search_hit(self):
        base = "https://openaccess.thecvf.com"
        catalog = f"{base}/CVPR2026?day=all"
        known = f"{base}/content/CVPR2026/html/known_paper.html"
        other = f"{base}/content/CVPR2026/html/other_paper.html"
        pages = {
            catalog: f'<a href="{known}">Industrial anomaly detection</a><a href="{other}">Learning from Sparse Normal Samples</a>',
            known: '<div id="abstract">MVTec evaluation. Code at https://github.com/lab/repo.</div>',
            other: '<meta name="citation_title" content="Learning from Sparse Normal Samples"><p class="paper-abstract">We test on MVTec AD.</p>',
        }
        existing = paper(status="accepted", venue="CVPR 2026", url=known, official_url=known, summary_zh="已核实")
        config = {"collection_year": 2026, "official_sources": {"CVPR": {"catalog": catalog, "format": "cvf"}}}
        hits = {"CVPR": [
            {"title": "Learning from Sparse Normal Samples", "url": other},
            {"title": "Fabricated industrial paper", "url": base + "/invalid"},
        ]}
        incoming, reports = OfficialSources(config, [existing], get=pages.__getitem__).collect(hits)
        saved = {p["title"]: p for p in merge([existing], incoming, "today")}
        self.assertEqual(set(saved), {"Industrial anomaly detection", "Learning from Sparse Normal Samples"})
        self.assertEqual(saved["Industrial anomaly detection"]["summary_zh"], "已核实")
        self.assertEqual(saved["Industrial anomaly detection"]["code_urls"], ["https://github.com/lab/repo"])
        self.assertEqual(saved["Learning from Sparse Normal Samples"]["status"], "pending")
        self.assertEqual(reports["CVPR"]["deepseek_only"], 1)
        self.assertEqual(reports["CVPR"]["catalog_only"], 1)

    def test_official_metadata_blocks_pdf_and_preserves_print_year(self):
        self.assertFalse(metadata_url("https://openaccess.thecvf.com/content/papers/file.pdf"))
        self.assertFalse(metadata_url("https://ojs.aaai.org/index.php/AAAI/article/download/123"))
        self.assertFalse(metadata_url("https://openaccess.thecvf.com@example.org/"))
        item = {"DOI": "10.1234/example", "title": ["Example anomaly detection"],
                "published": {"date-parts": [[2025, 11, 12]]}, "published-print": {"date-parts": [[2026, 2]]}}
        self.assertEqual(publisher_candidate("TIP", 2026, item)["venue"], "TIP 2026")
        self.assertIsNone(publisher_candidate("TIP", 2025, item))


if __name__ == "__main__":
    unittest.main()
