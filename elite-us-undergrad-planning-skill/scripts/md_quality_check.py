#!/usr/bin/env python3
"""Lightweight quality checker for parent-facing admissions planning Markdown."""
from __future__ import annotations

import argparse
from pathlib import Path

REQUIRED_SECTIONS = [
    "学生当前情况", "目标专业", "学校策略", "AP", "GPA",
    "SAT", "托福", "科研", "核心活动", "竞赛", "时间轴", "风险管理", "官网信息核验", "甘特图",
    "这一节的结论",
]

# 招生官 is allowed once as an explanation, not required as a section title.
READER_ALIASES = ("招生官", "大学招生办公室")

RISKY_PHRASES = [
    "保证录取", "稳进", "必进", "确保进入 ISEF", "科学种子直接晋级 ISEF", "保证晋级", "确保晋级", "随便做",
]

CLIENT_BANNED = [
    "招生官式", "当前画像", "画像结论", "库内", "库外", "sqlite", "SQLite",
    "subagent", "子代理", "小白", "修改版", "信息待补齐",
    "闭环", "抓手", "赛道", "颗粒度", "赋能", "综上所述",
]

PLACEHOLDER_MARKERS = ["{{", "}}", "TODO", "待写", "xxx", "XXX"]

AI_FILLER = ["全方位", "深度赋能", "落地执行", "温馨提示"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown", type=Path)
    args = parser.parse_args()
    text = args.markdown.read_text(encoding="utf-8")

    warnings = []
    for sec in REQUIRED_SECTIONS:
        if sec not in text:
            warnings.append(f"Missing or weak required section keyword: {sec}")
    if not any(alias in text for alias in READER_ALIASES):
        warnings.append("No 大学招生办公室 / 招生官 explanation found; add once in parent language if discussing who reads the file.")
    for phrase in RISKY_PHRASES:
        if phrase in text:
            warnings.append(f"Risky overclaim phrase found: {phrase}")
    for phrase in CLIENT_BANNED:
        if phrase in text:
            warnings.append(f"Client-facing banned phrase found: {phrase}")
    for phrase in AI_FILLER:
        if phrase in text:
            warnings.append(f"AI-typical filler found: {phrase}")
    if "v2" in text or "v3" in text:
        warnings.append("Revision trace found (v2/v3). Client files must look like a finished report.")
    for marker in PLACEHOLDER_MARKERS:
        if marker in text:
            warnings.append(f"Placeholder marker found: {marker}")
    if "晋级" not in text and "筛选" not in text and "无正式晋级机制" not in text:
        warnings.append("No obvious advancement/selection mechanism language found for activity or competition pathways.")
    if "对冲" not in text and "替代" not in text and "做不成" not in text:
        warnings.append("No obvious fallback/hedge path found for activities or competitions.")
    if "![" not in text or "甘特" not in text:
        warnings.append("No obvious embedded chart image reference found.")
    if "内部数据库" not in text and "学校官网" not in text:
        warnings.append("School-list sourcing sentence missing; client text should cite 内部数据库 and 学校官网.")

    if warnings:
        print("Quality check warnings:")
        for w in warnings:
            print(f"- {w}")
    else:
        print("Quality check passed with no obvious warnings.")


if __name__ == "__main__":
    main()
