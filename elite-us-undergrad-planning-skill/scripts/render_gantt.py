#!/usr/bin/env python3
"""Render a polished admissions-planning Gantt chart from YAML.

Input schema:

title: My Gantt
tasks:
  - section: 标化
    label: SAT 暑期集训
    start: 2026-07-06
    end: 2026-08-10
  - section: 标化
    label: SAT 报名决策
    date: 2026-08-07
    type: milestone
"""
from __future__ import annotations

import argparse
import datetime as dt
import textwrap
from pathlib import Path
from typing import Any, Dict, List

import matplotlib.dates as mdates
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import yaml


def parse_date(value: Any) -> dt.datetime:
    if isinstance(value, dt.datetime):
        return value
    if isinstance(value, dt.date):
        return dt.datetime.combine(value, dt.time())
    return dt.datetime.strptime(str(value), "%Y-%m-%d")


def choose_font() -> str | None:
    preferred = [
        "Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Source Han Sans SC",
        "PingFang SC", "Arial Unicode MS", "WenQuanYi Micro Hei", "Noto Sans CJK JP", "Noto Serif CJK JP", "DejaVu Sans"
    ]
    available = {f.name for f in fm.fontManager.ttflist}
    for name in preferred:
        if name in available:
            return name
    # Fallback: any installed CJK font is better than DejaVu for Chinese labels.
    for f in fm.fontManager.ttflist:
        if "CJK" in f.name or "Han" in f.name or "Hei" in f.name or "Song" in f.name:
            return f.name
    return None


def wrap_label(label: str, width: int = 18) -> str:
    # textwrap does not handle CJK perfectly, but this keeps long English labels readable.
    if len(label) <= width:
        return label
    return "\n".join(textwrap.wrap(label, width=width, break_long_words=False)) or label


def load_tasks(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def write_mermaid(data: Dict[str, Any], output: Path) -> None:
    lines = ["gantt", f"    title {data.get('title', 'Planning Gantt')}", "    dateFormat  YYYY-MM-DD", "    axisFormat  %Y-%m"]
    current_section = None
    for i, task in enumerate(data.get("tasks", []), start=1):
        section = task.get("section", "General")
        if section != current_section:
            lines.append("")
            lines.append(f"    section {section}")
            current_section = section
        label = str(task.get("label", f"task{i}"))
        safe_label = label.replace(":", "：")
        if task.get("type") == "milestone" or "date" in task:
            date = str(task.get("date"))
            lines.append(f"    {safe_label} :milestone, m{i}, {date}, 0d")
        else:
            start = str(task.get("start"))
            end = str(task.get("end"))
            lines.append(f"    {safe_label} :t{i}, {start}, {end}")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def render(data: Dict[str, Any], output: Path, width: float, height: float, dpi: int) -> None:
    font = choose_font()
    if font:
        plt.rcParams["font.family"] = font
    plt.rcParams["axes.unicode_minus"] = False

    raw_tasks: List[Dict[str, Any]] = data.get("tasks", [])
    tasks = []
    for t in raw_tasks:
        item = dict(t)
        if item.get("type") == "milestone" or "date" in item:
            item["date_dt"] = parse_date(item["date"])
        else:
            item["start_dt"] = parse_date(item["start"])
            item["end_dt"] = parse_date(item["end"])
        tasks.append(item)

    if not tasks:
        raise ValueError("No tasks found in YAML")

    sections = []
    for t in tasks:
        sec = t.get("section", "General")
        if sec not in sections:
            sections.append(sec)

    # Determine y positions with section gaps.
    y_positions = []
    y_labels = []
    y = 0
    section_y = {}
    for sec in sections:
        section_tasks = [t for t in tasks if t.get("section", "General") == sec]
        section_y[sec] = y + (len(section_tasks) - 1) / 2
        for t in section_tasks:
            y_positions.append((t, y))
            y_labels.append(wrap_label(str(t.get("label", "")), 16))
            y += 1
        y += 0.65

    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)

    palette = [
        "#4E79A7", "#F28E2B", "#59A14F", "#E15759", "#B07AA1", "#9C755F",
        "#EDC948", "#76B7B2", "#FF9DA7", "#BAB0AC", "#6B6ECF", "#17BECF"
    ]
    section_color = {sec: palette[i % len(palette)] for i, sec in enumerate(sections)}

    for t, ypos in y_positions:
        sec = t.get("section", "General")
        color = section_color[sec]
        if t.get("type") == "milestone" or "date_dt" in t:
            x = mdates.date2num(t["date_dt"])
            ax.scatter(x, ypos, marker="D", s=48, color=color, edgecolors="white", linewidths=0.8, zorder=4)
        else:
            start = mdates.date2num(t["start_dt"])
            end = mdates.date2num(t["end_dt"])
            ax.barh(ypos, end - start, left=start, height=0.48, color=color, alpha=0.92, edgecolor="white", linewidth=0.8)

    # Section labels on left margin inside the plot.
    xmin_candidates = []
    xmax_candidates = []
    for t in tasks:
        if t.get("type") == "milestone" or "date_dt" in t:
            xmin_candidates.append(t["date_dt"])
            xmax_candidates.append(t["date_dt"])
        else:
            xmin_candidates.append(t["start_dt"])
            xmax_candidates.append(t["end_dt"])
    xmin = parse_date(data.get("start")) if data.get("start") else min(xmin_candidates)
    xmax = parse_date(data.get("end")) if data.get("end") else max(xmax_candidates)
    ax.set_xlim(mdates.date2num(xmin) - 10, mdates.date2num(xmax) + 10)

    ax.set_yticks([pos for _, pos in y_positions])
    ax.set_yticklabels(y_labels, fontsize=8)
    ax.invert_yaxis()

    locator = mdates.AutoDateLocator(minticks=6, maxticks=12)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
    for tick in ax.get_xticklabels():
        tick.set_rotation(35)
        tick.set_horizontalalignment("right")
        tick.set_fontsize(8)

    ax.grid(axis="x", linestyle="-", alpha=0.20, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.set_title(data.get("title", "Planning Gantt"), fontsize=12, pad=12, fontweight="bold")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0)

    # Section legend. A legend is more robust than drawing section labels in the left margin,
    # because long Chinese task labels can otherwise overlap with group names.
    handles = [Patch(facecolor=section_color[sec], edgecolor="white", label=sec) for sec in sections]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.13),
              ncol=min(len(handles), 5), frameon=False, fontsize=8)

    fig.tight_layout(pad=1.2)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a polished Gantt chart from YAML")
    parser.add_argument("--input", required=True, type=Path, help="YAML file with tasks")
    parser.add_argument("--output", required=True, type=Path, help="Output PNG/SVG/PDF path")
    parser.add_argument("--mermaid-output", type=Path, help="Optional Mermaid .mmd output path")
    parser.add_argument("--width", type=float, default=10.5)
    parser.add_argument("--height", type=float, default=6.0)
    parser.add_argument("--dpi", type=int, default=220)
    args = parser.parse_args()

    data = load_tasks(args.input)
    render(data, args.output, args.width, args.height, args.dpi)
    if args.mermaid_output:
        write_mermaid(data, args.mermaid_output)


if __name__ == "__main__":
    main()
