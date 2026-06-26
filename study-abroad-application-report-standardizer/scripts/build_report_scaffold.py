#!/usr/bin/env python3
"""Generate a Markdown report scaffold from a student intake YAML.

Usage:
  python scripts/build_report_scaffold.py assets/student_intake_template.yaml --output report.md
"""

from __future__ import annotations

import argparse
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def load_yaml(path: Path) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML is required. Install with: pip install pyyaml")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data or {}


def get_nested(data: dict, *keys: str, default: str = "") -> str:
    current = data
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key, default)
    if current is None:
        return default
    return str(current)


def build_markdown(data: dict) -> str:
    name = get_nested(data, "student", "name", default="[Student Name]") or "[Student Name]"
    entry = get_nested(data, "student", "target_entry", default="[Target Entry]") or "[Target Entry]"
    countries = data.get("applications", {}).get("target_countries", []) if isinstance(data.get("applications"), dict) else []
    majors = data.get("applications", {}).get("intended_majors", []) if isinstance(data.get("applications"), dict) else []

    return f"""# {name} Application Planning Report

## Executive Summary

**Target entry:** {entry}

**Target countries:** {', '.join(countries) if countries else '[MISSING]'}

**Intended majors/routes:** {', '.join(majors) if majors else '[MISSING]'}

## Student Information and Missing Items

| Item | Current Information | Status | Implication | Follow-up |
|---|---|---|---|---|
| School | {get_nested(data, 'student', 'current_school', default='[MISSING]')} | STUDENT_REPORTED | Need school context | Confirm school profile |
| Curriculum | {get_nested(data, 'student', 'curriculum', default='[MISSING]')} | STUDENT_REPORTED | Course planning depends on curriculum | Confirm available courses |
| GPA/Rank | {get_nested(data, 'academics', 'gpa', default='[MISSING]')} / {get_nested(data, 'academics', 'rank_or_percentile', default='[MISSING]')} | STUDENT_REPORTED | Academic competitiveness | Upload transcript |
| Budget/Aid | {get_nested(data, 'applications', 'budget_per_year', default='[MISSING]')} / {get_nested(data, 'applications', 'financial_aid_need', default='[MISSING]')} | MISSING | Affects ED and school list | Family cost discussion |

## Admissions-Reader Diagnosis

### Current Read

[Write current profile diagnosis here.]

### Target Read

[Write target application identity here.]

### Core Risks

- [Risk 1]
- [Risk 2]
- [Risk 3]

## Positioning and Route Architecture

[Single-track / dual-track / multi-country route plan.]

## School and Program Strategy

| Tier | Institution | Program | Fit Logic | Requirements | Round | Risks |
|---|---|---|---|---|---|---|
| Reach | [School] | [Program] | [Fit] | [Requirements] | [Round] | [Risk] |

## Academic Plan

[Course, GPA, exam and academic output plan.]

## Testing and Language Plan

[Test targets, prep plan, dates, stop rules.]

## Background Development Plan

### Main Line 1

[Problem, method, milestones, deliverables, metrics, verification, risks.]

### Main Line 2

[Problem, method, milestones, deliverables, metrics, verification, risks.]

### Main Line 3

[Problem, method, milestones, deliverables, metrics, verification, risks.]

### Backup Line

[Low-permission fallback.]

## Essays, Recommendations, and Materials

[Essay map, recommender strategy, evidence packets.]

## Timeline

![Gantt Chart](gantt.png)

## Case / Benchmark Module

[Optional.]

## Risk Register

| Risk | Trigger | Severity | Mitigation | Owner | Deadline |
|---|---|---|---|---|---|
| [Risk] | [Trigger] | [High/Med/Low] | [Mitigation] | [Owner] | [Date] |

## Verification Checklist

- [ ] Verify deadlines.
- [ ] Verify testing policy.
- [ ] Verify English requirements.
- [ ] Verify budget and aid need.
- [ ] Verify achievements with documents.

## Sources Appendix

[Source notes or source ledger summary.]
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("intake_yaml", type=Path)
    parser.add_argument("--output", "-o", type=Path, default=Path("report.md"))
    args = parser.parse_args()
    data = load_yaml(args.intake_yaml)
    md = build_markdown(data)
    args.output.write_text(md, encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
