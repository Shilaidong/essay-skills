#!/usr/bin/env python3
"""Basic validation for source/evidence ledgers and timeline CSV files."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
from pathlib import Path

VALID_STATUSES = {"VERIFIED", "STUDENT_REPORTED", "TARGET", "ASSUMPTION", "MISSING"}


def check_csv_columns(path: Path, required: set[str]) -> list[str]:
    errors: list[str] = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = required - set(reader.fieldnames or [])
        if missing:
            errors.append(f"{path}: missing columns {sorted(missing)}")
    return errors


def validate_evidence(path: Path) -> list[str]:
    errors = check_csv_columns(path, {"claim", "status"})
    if errors:
        return errors
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        for i, row in enumerate(csv.DictReader(f), start=2):
            status = (row.get("status") or "").strip().upper()
            if status and status not in VALID_STATUSES:
                errors.append(f"{path}: row {i} has invalid status {status!r}")
            if status == "VERIFIED" and not (row.get("source_or_proof") or "").strip():
                errors.append(f"{path}: row {i} is VERIFIED but has no source_or_proof")
    return errors


def validate_timeline(path: Path) -> list[str]:
    errors = check_csv_columns(path, {"section", "task", "start", "end"})
    if errors:
        return errors
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        for i, row in enumerate(csv.DictReader(f), start=2):
            for field in ["start", "end"]:
                try:
                    dt.datetime.strptime((row.get(field) or "").strip(), "%Y-%m-%d")
                except Exception:
                    errors.append(f"{path}: row {i} invalid {field} date")
            try:
                start = dt.datetime.strptime(row["start"], "%Y-%m-%d")
                end = dt.datetime.strptime(row["end"], "%Y-%m-%d")
                if end < start:
                    errors.append(f"{path}: row {i} end before start")
            except Exception:
                pass
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--timeline", type=Path)
    args = parser.parse_args()
    errors: list[str] = []
    if args.evidence:
        errors.extend(validate_evidence(args.evidence))
    if args.timeline:
        errors.extend(validate_timeline(args.timeline))
    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        raise SystemExit(1)
    print("Validation passed")


if __name__ == "__main__":
    main()
