# -*- coding: utf-8 -*-
"""Copy the school-list xlsx template and fill rows. Never overwrite the template in place."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import date
from pathlib import Path

from openpyxl import load_workbook

GROUP_MAP = {
    "冲": "冲刺",
    "冲刺": "冲刺",
    "reach": "冲刺",
    "稳": "匹配",
    "匹配": "匹配",
    "目标": "匹配",
    "match": "匹配",
    "target": "匹配",
    "保": "保底",
    "保底": "保底",
    "safety": "保底",
    "彩票": "彩票项",
    "彩票项": "彩票项",
    "lottery": "彩票项",
}

DATA_START = 5
HEADER_ROW = 4
COLS = ("group", "school", "program", "degree", "college", "region", "url", "note")


def normalize_group(raw: str) -> str:
    key = (raw or "").strip().lower()
    for k, v in GROUP_MAP.items():
        if key == k.lower():
            return v
    return (raw or "").strip() or "还需要核对"


def copy_row_style(ws, src: int, dest: int) -> None:
    ws.row_dimensions[dest].height = ws.row_dimensions[src].height
    for col in range(1, 9):
        s = ws.cell(src, col)
        d = ws.cell(dest, col)
        if s.has_style:
            d.font = s.font.copy()
            d.border = s.border.copy()
            d.fill = s.fill.copy()
            d.number_format = s.number_format
            d.protection = s.protection.copy()
            d.alignment = s.alignment.copy()


def fill(template: Path, out: Path, student: str, rows: list[dict], export_day: str | None) -> None:
    if not template.is_file():
        raise SystemExit(f"template not found: {template}")
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.resolve() == template.resolve():
        raise SystemExit("refuse to overwrite the source template; pass a work-folder --out")
    shutil.copy2(template, out)
    wb = load_workbook(out)
    if "选校清单" not in wb.sheetnames:
        raise SystemExit(f"missing sheet 选校清单 in {out}")
    ws = wb["选校清单"]
    ws["B2"] = student or "还需要核对"
    ws["D2"] = export_day or date.today().isoformat()

    need = len(rows)
    existing = max(ws.max_row - DATA_START + 1, 0)
    if need > existing:
        ws.insert_rows(ws.max_row + 1, need - existing)
        for r in range(existing + DATA_START, DATA_START + need):
            copy_row_style(ws, DATA_START, r)

    for i, item in enumerate(rows):
        r = DATA_START + i
        values = [
            normalize_group(str(item.get("group", ""))),
            item.get("school") or "还需要核对",
            item.get("program") or "还需要核对",
            item.get("degree") or "还需要核对",
            item.get("college") or "还需要核对",
            item.get("region") or "还需要核对",
            item.get("url") or "还需要核对",
            item.get("note") or "",
        ]
        for c, val in enumerate(values, 1):
            ws.cell(r, c).value = val

    schools = {str(x.get("school") or "").strip() for x in rows if str(x.get("school") or "").strip()}
    ws["F2"] = len(schools)
    ws["H2"] = len(rows)
    wb.save(out)
    print(f"wrote {out} schools={ws['F2'].value} programs={ws['H2'].value}")


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Fill 选校清单模板.xlsx into a student folder")
    ap.add_argument("--template", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--student", default="")
    ap.add_argument("--json", required=True, help="array of row objects")
    ap.add_argument("--date", default="")
    args = ap.parse_args()
    payload = json.loads(Path(args.json).read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise SystemExit("json must be an array")
    fill(Path(args.template), Path(args.out), args.student, payload, args.date or None)


if __name__ == "__main__":
    main()
