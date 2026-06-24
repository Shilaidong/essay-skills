#!/usr/bin/env python3
"""Render a readable Gantt chart PNG from a CSV timeline."""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List

try:
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: matplotlib. Run: pip install matplotlib") from exc


@dataclass
class Task:
    section: str
    task: str
    start: datetime
    end: datetime
    status: str
    milestone: bool
    owner: str
    notes: str


def parse_bool(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "是"}


def parse_date(value: str) -> datetime:
    return datetime.strptime(value.strip(), "%Y-%m-%d")


def load_tasks(path: Path) -> List[Task]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"section", "task", "start", "end"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing CSV columns: {', '.join(sorted(missing))}")
        tasks: List[Task] = []
        for row_number, row in enumerate(reader, start=2):
            if not (row.get("task") or "").strip():
                continue
            try:
                start = parse_date(row["start"])
                end = parse_date(row["end"])
            except Exception as exc:  # noqa: BLE001
                raise ValueError(f"Invalid date at row {row_number}: {exc}") from exc
            if end < start:
                raise ValueError(f"End date before start date at row {row_number}")
            tasks.append(
                Task(
                    section=(row.get("section") or "未分类").strip(),
                    task=(row.get("task") or "").strip(),
                    start=start,
                    end=end,
                    status=(row.get("status") or "planned").strip(),
                    milestone=parse_bool(row.get("milestone") or "false"),
                    owner=(row.get("owner") or "").strip(),
                    notes=(row.get("notes") or "").strip(),
                )
            )
    if not tasks:
        raise ValueError("No tasks found in timeline CSV")
    return tasks


def choose_font() -> str:
    # Matplotlib may not index TTC collections in minimal containers. Register a
    # known CJK font file when present, then fall back to installed family names.
    known_paths = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
        "/usr/share/fonts/truetype/arphic-gbsn00lp/gbsn00lp.ttf",
    ]
    for raw in known_paths:
        path = Path(raw)
        if path.exists():
            try:
                font_manager.fontManager.addfont(str(path))
                return font_manager.FontProperties(fname=str(path)).get_name()
            except Exception:
                pass

    available = {f.name for f in font_manager.fontManager.ttflist}
    candidates = [
        "SimSun",
        "宋体",
        "Noto Sans CJK SC",
        "Noto Serif CJK SC",
        "Noto Sans CJK JP",
        "Noto Serif CJK JP",
        "AR PL SungtiL GB",
        "Source Han Sans SC",
        "Source Han Serif SC",
        "Microsoft YaHei",
        "Arial Unicode MS",
        "DejaVu Sans",
    ]
    for candidate in candidates:
        if candidate in available:
            return candidate
    return "DejaVu Sans"


def render(tasks: List[Task], output: Path, title: str, subtitle: str, dpi: int) -> None:
    plt.rcParams["font.family"] = choose_font()
    plt.rcParams["axes.unicode_minus"] = False

    # Keep the supplied order; it often encodes the user's intended workstream sequence.
    sections: List[str] = []
    for task in tasks:
        if task.section not in sections:
            sections.append(task.section)
    section_index = {name: idx for idx, name in enumerate(sections)}
    default_colors = plt.rcParams["axes.prop_cycle"].by_key().get("color", [])

    row_height = 0.58
    fig_height = max(4.8, 1.8 + len(tasks) * 0.48)
    fig_width = 13.5
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    min_date = min(t.start for t in tasks)
    max_date = max(t.end for t in tasks)

    y_positions = list(range(len(tasks)))[::-1]
    labels: List[str] = []
    for y, task in zip(y_positions, tasks):
        start_num = mdates.date2num(task.start)
        end_num = mdates.date2num(task.end)
        duration = max(end_num - start_num, 0.8)
        color = default_colors[section_index[task.section] % len(default_colors)] if default_colors else None
        if task.milestone:
            ax.scatter(start_num, y, marker="D", s=42, zorder=3, color=color)
        else:
            ax.barh(y, duration, left=start_num, height=row_height, alpha=0.82, color=color)
        label = task.task
        if task.owner:
            label += f"  ·  {task.owner}"
        labels.append(label)

    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels, fontsize=9.2)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=2))
    ax.grid(axis="x", which="major", linewidth=0.8, alpha=0.28)
    ax.grid(axis="x", which="minor", linewidth=0.4, alpha=0.12)
    ax.set_xlim(mdates.date2num(min_date) - 3, mdates.date2num(max_date) + 5)
    ax.tick_params(axis="x", labelrotation=35, labelsize=8.7)
    ax.tick_params(axis="y", length=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # Section labels are placed at the right edge to avoid widening the y-axis labels.
    for section in sections:
        indices = [i for i, t in enumerate(tasks) if t.section == section]
        if not indices:
            continue
        ys = [y_positions[i] for i in indices]
        y_mid = sum(ys) / len(ys)
        ax.text(
            mdates.date2num(max_date) + 4.2,
            y_mid,
            section,
            va="center",
            ha="right",
            fontsize=8.6,
            fontweight="bold",
            alpha=0.72,
        )

    fig.suptitle(title, fontsize=16, fontweight="bold", y=0.985)
    if subtitle:
        ax.set_title(subtitle, fontsize=9.5, pad=16, alpha=0.72)
    ax.set_xlabel("时间", fontsize=9.5)
    fig.tight_layout(rect=(0.04, 0.04, 0.98, 0.95))

    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=dpi, bbox_inches="tight")
    plt.close(fig)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a Gantt chart PNG from a timeline CSV.")
    parser.add_argument("timeline", type=Path, help="CSV with section, task, start, end columns")
    parser.add_argument("--output", required=True, type=Path, help="Output PNG path")
    parser.add_argument("--title", default="项目时间轴")
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--dpi", type=int, default=220)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.timeline.exists():
        print(f"ERROR: timeline file not found: {args.timeline}", file=sys.stderr)
        return 2
    if args.output.exists() and not args.force:
        print(f"ERROR: output already exists: {args.output}. Use --force to overwrite.", file=sys.stderr)
        return 2
    try:
        tasks = load_tasks(args.timeline)
        render(tasks, args.output, args.title, args.subtitle, args.dpi)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
