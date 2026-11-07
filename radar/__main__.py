import argparse
import html
import re
import sys
from pathlib import Path
from urllib.parse import quote, urlsplit
from .core import filter_collection_year, load_json, run, venue_and_year

ROOT = Path(__file__).resolve().parent.parent
LIST_START = "<!-- PAPER-LIST:START -->"
LIST_END = "<!-- PAPER-LIST:END -->"


def markdown_text(value):
    text = html.escape(" ".join(value.split()), quote=False).replace("|", "&#124;")
    return re.sub(r"([\\`*_{}\[\]~])", r"\\\1", text)


def markdown_link(label, url):
    try:
        parsed = urlsplit(url)
        if parsed.scheme == "https" and parsed.hostname:
            safe_url = quote(url, safe=":/?&=%#@+;,$-_.!~*'")
            return f"[{label}]({safe_url})"
    except ValueError:
        pass
    return label


def build(root=ROOT):
    target = root / "README.md"
    readme = target.read_text(encoding="utf-8")
    if readme.count(LIST_START) != 1 or readme.count(LIST_END) != 1 or readme.index(LIST_START) > readme.index(LIST_END):
        raise ValueError("README must contain one ordered pair of paper list markers")

    config = load_json(root / "config.json", {})
    papers = filter_collection_year(load_json(root / "data/papers.json", []), config.get("collection_year"))
    groups = {}
    for paper in papers:
        if paper["status"] == "accepted":
            groups.setdefault(venue_and_year(paper), []).append(paper)

    total = sum(len(group) for group in groups.values())
    pending = sum(paper["status"] == "pending" for paper in papers)
    lines = [f"已收录 **{total} 篇** · 待筛选 **{pending} 篇**"]
    ordered_groups = sorted(groups, key=lambda group: (group[0] == "arXiv", group[0].casefold(), -int(group[1])))
    for venue, year in ordered_groups:
        lines.extend(["", f"### {markdown_text(venue)} {year}", "",
                      "| 论文 | 标签 | 链接 | Tip |", "| --- | --- | --- | --- |"])
        entries = sorted(groups[venue, year], key=lambda paper: (paper["published"], paper["id"]), reverse=True)
        for paper in entries:
            title = markdown_link(markdown_text(paper["title"]), paper["url"])
            links = [markdown_link("论文", paper["url"])]
            if paper.get("pdf_url"):
                links.append(markdown_link("PDF", paper["pdf_url"]))
            elif paper.get("official_url"):
                preprint = paper.get("arxiv_id") or paper["id"]
                if re.fullmatch(r"\d{4}\.\d{4,5}", preprint):
                    links.append(markdown_link("arXiv", f"https://arxiv.org/abs/{preprint}"))
            links.extend(markdown_link("代码", url) for url in paper.get("code_urls", []))
            # Old reviewed records may only have a topic. Keep it as a fallback label.
            tags = paper.get("tags") or [paper.get("topic", "待补充")]
            labels = " ".join(f"<code>{markdown_text(tag)}</code>" for tag in tags)
            tip = markdown_text(paper.get("summary_zh", "")) or "待补充"
            details = f"<details><summary>查看 Tip</summary><p>{tip}</p></details>"
            lines.append(f"| {title} | {labels} | {' · '.join(links)} | {details} |")

    before, remainder = readme.split(LIST_START)
    _, after = remainder.split(LIST_END)
    updated = before + LIST_START + "\n\n" + "\n".join(lines) + "\n\n" + LIST_END + after
    if updated != readme:
        temp = target.with_suffix(".md.tmp")
        temp.write_text(updated, encoding="utf-8")
        temp.replace(target)
    print(f"Updated {target} ({total} accepted papers)")


def report(root=ROOT):
    state = load_json(root / "data/state.json", {})
    print("## 论文采集状态\n")
    if state.get("review_only"):
        print("本轮仅复核已保存候选，没有重新采集，也没有推进采集时间。\n")
        for name, row in state.get("last_collection_sources", {}).items():
            if row.get("status") == "failed":
                print(f"上次完整采集仍有异常：{name} · {row.get('reason', 'failed')}。\n")
    print("| 来源 | 状态 | 扫描 | 候选 | DeepSeek 已核对 | 仅 DeepSeek 命中 | 仅目录关键词命中 | 详情失败 | 延后复查 |")
    print("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for name, row in state.get("sources", {}).items():
        status = row["status"]
        if row.get("reason"):
            status += f" ({row['reason']})"
        print(f"| {name} | {status} | {row.get('scanned', '—')} | {row.get('candidates', '—')} | "
              f"{row.get('deepseek_hits', '—')} | {row.get('deepseek_only', '—')} | "
              f"{row.get('catalog_only', '—')} | {row.get('details_failed', 0)} | {row.get('details_deferred', 0)} |")
    print(f"\n待筛选 {state.get('pending', 0)} 篇，其中缺摘要 {state.get('missing_abstract', 0)} 篇，"
          f"摘要未命中范围词 {state.get('missing_scope_evidence', 0)} 篇（仍进入模型判断）。")
    print(f"DeepSeek 搜索 {state.get('deepseek_search_calls', 0)} 次，"
          f"模型筛选 {state.get('llm_calls', 0)} 次，筛选失败 {state.get('review_errors', 0)} 次。")
    print(f"\n深入调查 {state.get('investigations', 0)} 篇，调查搜索 {state.get('investigation_search_calls', 0)} 次。")
    if state.get('investigation_search_errors'):
        print(f"其中调查搜索失败 {state['investigation_search_errors']} 次，失败原因已按论文保存，仍缺证据的条目继续待核实。")
    search_errors = state.get("deepseek_search_errors", {})
    for venue, reason in search_errors.items():
        print(f"\nDeepSeek 搜索失败 · {venue} · {reason}")
    for venue, row in state.get("sources", {}).items():
        for hit in row.get("deepseek_new", []):
            title = markdown_link(markdown_text(hit["title"]), hit["url"])
            print(f"\n- {venue} · DeepSeek 新候选 · {title}")
    compared = state.get("deepseek_only_reviewed", {})
    if any(compared.values()):
        print(f"\n仅 DeepSeek 命中的候选累计收录 {compared['accepted']} 篇，"
              f"待筛 {compared['pending']} 篇，排除 {compared['rejected']} 篇。")
    code = state.get("code_backfill", {})
    if code:
        print(f"\n代码仓库复查 {code['checked']} 篇，补充 {code['added']} 篇。")
        if code.get("error"):
            print(f"\n代码搜索失败 · {code['error']}")
    missing_key = state.get("llm_status") == "missing_key"
    if missing_key:
        print("\n缺少仓库 Secret `DEEPSEEK_API_KEY`。本轮已保存官方来源候选。")
    failed_sources = any(row["status"] == "failed" for row in state.get("sources", {}).values())
    return int(missing_key or failed_sources or bool(search_errors) or bool(state.get("review_blocked")))


def main():
    parser = argparse.ArgumentParser(description="Industrial anomaly detection paper radar")
    parser.add_argument("command", choices=["collect", "build", "report"])
    parser.add_argument("--since", help="Inclusive start date YYYY-MM-DD (manual backfill)")
    parser.add_argument("--until", help="Inclusive end date YYYY-MM-DD")
    parser.add_argument("--no-llm", action="store_true", help="Collect as pending without LLM calls")
    parser.add_argument("--review-only", action="store_true", help="Review saved candidates without fetching catalogs or advancing checkpoints")
    args = parser.parse_args()
    if args.command == "collect":
        run(ROOT, args.since, args.until, args.no_llm, review_only=args.review_only)
    elif args.command == "build":
        build()
    else:
        sys.exit(report())


if __name__ == "__main__":
    main()
