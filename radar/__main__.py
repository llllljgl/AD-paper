import argparse
import html
import re
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
            elif paper.get("official_url") and re.fullmatch(r"\d{4}\.\d{4,5}", paper["id"]):
                links.append(markdown_link("arXiv", f"https://arxiv.org/abs/{paper['id']}"))
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


def main():
    parser = argparse.ArgumentParser(description="Industrial anomaly detection paper radar")
    parser.add_argument("command", choices=["collect", "build"])
    parser.add_argument("--since", help="Inclusive start date YYYY-MM-DD (manual backfill)")
    parser.add_argument("--until", help="Inclusive end date YYYY-MM-DD")
    parser.add_argument("--no-llm", action="store_true", help="Collect as pending without LLM calls")
    args = parser.parse_args()
    if args.command == "collect":
        run(ROOT, args.since, args.until, args.no_llm)
    else:
        build()


if __name__ == "__main__":
    main()
