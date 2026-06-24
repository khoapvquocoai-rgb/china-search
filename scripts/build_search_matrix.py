#!/usr/bin/env python3
"""Build a no-budget Chinese search matrix for public China research.

This script does not call paid APIs or scrape websites. It creates source-specific
Chinese query strings and optional manual search URLs that the user can open.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from urllib.parse import quote_plus


@dataclass
class QueryRow:
    group: str
    query_zh: str
    source: str
    purpose: str
    manual_url: str
    notes: str


SOURCE_URLS = {
    "baidu": "https://www.baidu.com/s?wd={q}",
    "360": "https://www.so.com/s?q={q}",
    "sogou_wechat": "https://weixin.sogou.com/weixin?type=2&query={q}",
    "github": "https://github.com/search?q={q}&type=repositories",
    "gitee": "https://search.gitee.com/?q={q}",
    "bing": "https://cn.bing.com/search?q={q}",
}


def url_for(source: str, query: str) -> str:
    template = SOURCE_URLS.get(source, "")
    return template.format(q=quote_plus(query)) if template else ""


def build_queries(topic: str, entity: str | None = None) -> list[QueryRow]:
    base = entity.strip() if entity else topic.strip()
    topic_clean = topic.strip()

    patterns = [
        ("official_docs", f"{base} 官方文档", "baidu", "find official documentation", "prefer vendor/regulator domains"),
        ("official_docs", f"{base} 开发者文档 API SDK", "baidu", "find API/SDK docs", "verify on official site"),
        ("official_docs", f"site:cloud.baidu.com {base} API 文档", "bing", "find Baidu Cloud docs", "use when Baidu/BCE is relevant"),
        ("official_docs", f"site:help.aliyun.com {base} API SDK", "bing", "find Alibaba Cloud docs", "use when Alibaba/Qwen/cloud is relevant"),
        ("official_docs", f"site:cloud.tencent.com {base} API SDK", "bing", "find Tencent Cloud docs", "use when Tencent/WeChat is relevant"),
        ("vendor_product", f"{base} 产品 技术规格书", "baidu", "find product specification", "download only public docs"),
        ("vendor_product", f"{base} 解决方案 白皮书", "baidu", "find whitepapers and solutions", "treat marketing claims cautiously"),
        ("files", f"{base} 技术规格书 filetype:pdf", "baidu", "find PDF datasheets", "verify source domain"),
        ("files", f"{base} 白皮书 PDF", "360", "find alternate PDF results", "cross-check with Baidu"),
        ("code_repo", f"{base} Python SDK GitHub", "github", "find GitHub repos", "check official org, license, releases"),
        ("code_repo", f"{base} 开源 SDK", "gitee", "find Gitee repos", "cross-check mirrors with upstream"),
        ("code_repo", f"{base} 示例代码", "baidu", "find example code", "community code is secondary"),
        ("developer_forums", f"{base} CSDN 教程", "baidu", "find Chinese tutorials", "do not treat as final proof"),
        ("developer_forums", f"{base} OSChina", "baidu", "find OSChina discussions", "secondary source"),
        ("wechat_public", f"{base} 微信公众号", "sogou_wechat", "find public WeChat articles", "manual only; do not bypass expired signatures"),
        ("wechat_public", f"{base} 案例 发布", "sogou_wechat", "find product launch/case articles", "manual public articles only"),
        ("risk", f"{base} 行政处罚", "baidu", "find administrative penalties", "verify official notices"),
        ("risk", f"{base} 诉讼 投诉", "baidu", "find litigation/complaints", "verify with official/legal sources"),
        ("risk", f"{base} 漏洞 CVE 数据泄露", "bing", "find security issues", "verify CVE/advisories"),
        ("broad_cn", f"{topic_clean} 中国大陆", "baidu", "broad mainland discovery", "use native Chinese variants after first pass"),
    ]

    rows: list[QueryRow] = []
    for group, query, source, purpose, notes in patterns:
        rows.append(QueryRow(group, query, source, purpose, url_for(source, query), notes))
    return rows


def write_csv(rows: list[QueryRow], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def write_json(rows: list[QueryRow], path: Path) -> None:
    path.write_text(json.dumps([asdict(r) for r in rows], ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a Chinese public-source search matrix.")
    parser.add_argument("topic", help="Vietnamese/English/Chinese research topic")
    parser.add_argument("--entity", help="Specific company/product/API/repo name", default=None)
    parser.add_argument("--output", help="Output path (.csv or .json)", default="search_matrix.csv")
    args = parser.parse_args()

    rows = build_queries(args.topic, args.entity)
    output = Path(args.output)
    if output.suffix.lower() == ".json":
        write_json(rows, output)
    else:
        write_csv(rows, output)
    print(f"Wrote {len(rows)} query rows to {output}")


if __name__ == "__main__":
    main()
