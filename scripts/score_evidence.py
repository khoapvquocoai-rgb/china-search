#!/usr/bin/env python3
"""Score a China public-source evidence item.

This script is deterministic and offline. It does not fetch URLs.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict


@dataclass
class EvidenceScore:
    score: int
    grade: str
    risk_flags: list[str]
    recommendation: str


def score_evidence(
    source_type: str,
    official: bool = False,
    has_date: bool = False,
    has_download: bool = False,
    has_original_chinese: bool = False,
    has_translation: bool = False,
    cross_checked: bool = False,
    requires_login: bool = False,
    captcha_or_antibot: bool = False,
    community_only: bool = False,
) -> EvidenceScore:
    score = 0
    flags: list[str] = []

    if official:
        score += 30
    if source_type in {"official_docs", "api_docs", "regulator", "vendor_datasheet"}:
        score += 25
    elif source_type in {"github", "gitee", "modelscope", "technical_whitepaper"}:
        score += 18
    elif source_type in {"news", "wechat_public", "marketplace"}:
        score += 10
    elif source_type in {"forum", "blog", "community"}:
        score += 5
        community_only = True

    if has_date:
        score += 8
    else:
        flags.append("missing_date")

    if has_download:
        score += 8
    if has_original_chinese:
        score += 7
    if has_translation:
        score += 7
    if cross_checked:
        score += 12
    else:
        flags.append("not_cross_checked")

    if requires_login:
        score -= 15
        flags.append("requires_login")
    if captcha_or_antibot:
        score -= 25
        flags.append("captcha_or_antibot")
    if community_only:
        score -= 10
        flags.append("community_or_secondary_source")

    score = max(0, min(score, 100))
    if score >= 80:
        grade = "strong"
        rec = "usable as primary evidence if claim matches source content"
    elif score >= 60:
        grade = "moderate"
        rec = "use as supporting evidence and verify key claims"
    elif score >= 40:
        grade = "weak"
        rec = "use only as discovery signal"
    else:
        grade = "do_not_use_for_conclusion"
        rec = "do not use for final conclusion"

    return EvidenceScore(score, grade, flags, rec)


def main() -> None:
    parser = argparse.ArgumentParser(description="Score a China research evidence item.")
    parser.add_argument("--source-type", required=True, choices=[
        "official_docs", "api_docs", "regulator", "vendor_datasheet", "github", "gitee",
        "modelscope", "technical_whitepaper", "news", "wechat_public", "marketplace",
        "forum", "blog", "community"
    ])
    parser.add_argument("--official", action="store_true")
    parser.add_argument("--has-date", action="store_true")
    parser.add_argument("--has-download", action="store_true")
    parser.add_argument("--has-original-chinese", action="store_true")
    parser.add_argument("--has-translation", action="store_true")
    parser.add_argument("--cross-checked", action="store_true")
    parser.add_argument("--requires-login", action="store_true")
    parser.add_argument("--captcha-or-antibot", action="store_true")
    parser.add_argument("--community-only", action="store_true")
    args = parser.parse_args()

    result = score_evidence(
        source_type=args.source_type,
        official=args.official,
        has_date=args.has_date,
        has_download=args.has_download,
        has_original_chinese=args.has_original_chinese,
        has_translation=args.has_translation,
        cross_checked=args.cross_checked,
        requires_login=args.requires_login,
        captcha_or_antibot=args.captcha_or_antibot,
        community_only=args.community_only,
    )
    print(json.dumps(asdict(result), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
