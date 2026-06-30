#!/usr/bin/env python3
"""Lightweight quality checker for admissions planning Markdown reports."""
from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_SECTIONS = [
    "学生当前情况", "招生官", "目标专业", "学校策略", "AP", "GPA",
    "SAT", "托福", "科研", "核心活动", "竞赛", "时间轴", "风险管理", "官网信息核验", "甘特图"
]

RISKY_PHRASES = [
    "保证录取", "稳进", "必进", "确保进入 ISEF", "科学种子直接晋级 ISEF", "保证晋级", "确保晋级", "随便做",
]

PLACEHOLDER_MARKERS = ["{{", "}}", "TODO", "待写", "xxx", "XXX"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown", type=Path)
    args = parser.parse_args()
    text = args.markdown.read_text(encoding="utf-8")

    warnings = []
    for sec in REQUIRED_SECTIONS:
        if sec not in text:
            warnings.append(f"Missing or weak required section keyword: {sec}")
    for phrase in RISKY_PHRASES:
        if phrase in text:
            warnings.append(f"Risky overclaim phrase found: {phrase}")
    for marker in PLACEHOLDER_MARKERS:
        if marker in text:
            warnings.append(f"Placeholder marker found: {marker}")
    if "信息待补齐" in text:
        warnings.append("Contains 信息待补齐 — acceptable only if truly missing and intentional.")
    if "晋级" not in text and "筛选" not in text and "无正式晋级机制" not in text:
        warnings.append("No obvious advancement/selection mechanism language found for activity or competition pathways.")
    if "对冲" not in text and "替代" not in text:
        warnings.append("No obvious fallback/hedge path found for activities or competitions.")
    if "![" not in text or "甘特" not in text:
        warnings.append("No obvious embedded chart image reference found.")

    if warnings:
        print("Quality check warnings:")
        for w in warnings:
            print(f"- {w}")
    else:
        print("Quality check passed with no obvious warnings.")


if __name__ == "__main__":
    main()
