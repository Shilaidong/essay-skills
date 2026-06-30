#!/usr/bin/env python3
"""Create a clean project workspace for an admissions planning report."""
from __future__ import annotations

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", required=True, type=Path)
    args = parser.parse_args()
    root = args.project_dir
    for sub in ["input", "working", "output", "assets"]:
        (root / sub).mkdir(parents=True, exist_ok=True)
    (root / "working" / "source_log.csv").write_text(
        "file_name,file_type,status,pages_or_sections_reviewed,key_facts,conflicts_or_questions,confidence\n",
        encoding="utf-8",
    )
    (root / "working" / "fact_matrix.md").write_text("# Fact Matrix\n\n", encoding="utf-8")
    (root / "working" / "strategy_notes.md").write_text("# Strategy Notes\n\n", encoding="utf-8")
    (root / "working" / "open_questions.md").write_text("# Open Questions\n\n", encoding="utf-8")
    print(f"Created planning workspace at {root}")


if __name__ == "__main__":
    main()
