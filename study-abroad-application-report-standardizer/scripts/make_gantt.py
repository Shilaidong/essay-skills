#!/usr/bin/env python3
"""Create a PNG Gantt chart from a CSV timeline.

CSV columns:
  section, task, start, end, milestone, notes
Dates must be YYYY-MM-DD. milestone accepts true/false/1/0/yes/no.

Usage:
  python scripts/make_gantt.py assets/timeline_template.csv --output gantt.png --title "Application Timeline"
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


@dataclass
class Item:
    section: str
    task: str
    start: dt.date
    end: dt.date
    milestone: bool
    notes: str = ""


def parse_bool(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"true", "1", "yes", "y", "milestone"}


def parse_date(value: str, field: str, row_number: int) -> dt.date:
    try:
        return dt.datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except Exception as exc:
        raise ValueError(f"Row {row_number}: invalid {field} date {value!r}; expected YYYY-MM-DD") from exc


def read_items(path: Path) -> list[Item]:
    items: list[Item] = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        required = {"section", "task", "start", "end"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
        for i, row in enumerate(reader, start=2):
            if not row.get("task"):
                continue
            start = parse_date(row["start"], "start", i)
            end = parse_date(row["end"], "end", i)
            if end < start:
                raise ValueError(f"Row {i}: end date is before start date")
            items.append(
                Item(
                    section=(row.get("section") or "General").strip(),
                    task=row["task"].strip(),
                    start=start,
                    end=end,
                    milestone=parse_bool(row.get("milestone")),
                    notes=(row.get("notes") or "").strip(),
                )
            )
    if not items:
        raise ValueError("No timeline items found")
    return items


def wrap_label(text: str, max_chars: int = 34) -> str:
    if len(text) <= max_chars:
        return text
    parts: list[str] = []
    current = ""
    for token in text.replace("/", "/ ").split():
        if len(current) + len(token) + 1 > max_chars and current:
            parts.append(current.rstrip())
            current = token + " "
        else:
            current += token + " "
    if current.strip():
        parts.append(current.strip())
    return "\n".join(parts[:2])


def plot_gantt(items: Iterable[Item], output: Path, title: str = "Application Timeline") -> None:
    items = list(items)
    min_date = min(i.start for i in items)
    max_date = max(i.end for i in items)
    fig_height = max(5, 0.42 * len(items) + 1.8)
    fig_width = 14
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    y_positions = list(range(len(items)))[::-1]
    labels = []

    for y, item in zip(y_positions, items):
        labels.append(f"{item.section} | {wrap_label(item.task)}")
        start_num = mdates.date2num(item.start)
        end_num = mdates.date2num(item.end)
        if item.milestone or item.start == item.end:
            ax.scatter([start_num], [y], marker="D", s=60)
            ax.text(start_num, y + 0.18, item.start.strftime("%m-%d"), fontsize=8, ha="center")
        else:
            duration = max(end_num - start_num, 1)
            ax.barh(y, duration, left=start_num, height=0.58, align="center")

    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_title(title, fontsize=16, pad=14)
    ax.xaxis_date()
    total_days = (max_date - min_date).days
    if total_days > 420:
        locator = mdates.MonthLocator(interval=2)
    elif total_days > 180:
        locator = mdates.MonthLocator(interval=1)
    else:
        locator = mdates.WeekdayLocator(interval=2)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.grid(True, axis="x", alpha=0.25)
    ax.set_xlim(mdates.date2num(min_date - dt.timedelta(days=7)), mdates.date2num(max_date + dt.timedelta(days=14)))
    fig.autofmt_xdate(rotation=35, ha="right")
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path, help="Timeline CSV")
    parser.add_argument("--output", "-o", type=Path, default=Path("gantt.png"))
    parser.add_argument("--title", default="Application Timeline")
    args = parser.parse_args()
    items = read_items(args.csv)
    plot_gantt(items, args.output, args.title)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
