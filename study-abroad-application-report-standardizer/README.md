# Study-Abroad Application Report Standardizer

A universal Agent Skill for turning student materials into rigorous study-abroad application planning reports.

This version is intentionally **not tied to one student, school tier, country, major, or case**. It standardizes the workflow, research discipline, strategy logic, document writing, Gantt image generation, and Word output process. After installing the skill, provide a new student's background and uploaded materials in the session; the agent should apply this framework to that specific case.

## Install

### Codex-style skills

Place the folder in a skill directory supported by your agent runtime, for example:

```text
.agents/skills/study-abroad-application-report-standardizer/
  SKILL.md
  references/
  assets/
  scripts/
```

### OpenCode-style use

Place the folder where OpenCode can discover Agent Skills, or keep it inside the project and explicitly ask the agent to load/use the skill.

## Quick usage prompt

```text
请使用 study-abroad-application-report-standardizer 这个 Skill。
我会上传学生成绩单、活动表、学校清单和会议纪要。
请先做信息诊断和缺失项清单，再检索最新学校/专业信息，最后输出一份中文 Word 规划报告，要求包含选校、专业路线、活动规划、标化、文书、推荐信、时间轴、甘特图图片和风险清单。
```

## Package structure

```text
SKILL.md                         Core skill instructions
references/                      Detailed playbooks
assets/                          Reusable CSV/YAML/Markdown templates
scripts/                         Utilities for Gantt charts, DOCX generation, validation, scaffolding
examples/                        Empty placeholder area for your own examples
```

## Optional Python dependencies

```bash
pip install python-docx pyyaml matplotlib pillow
```

LibreOffice is recommended for rendering Word files to PDF/PNG for visual QA, but the skill can still draft Markdown/DOCX without it.

## What was removed from the earlier case-specific version

- Specific student name and profile.
- Specific MIT/Cornell/Penn/Columbia planning content.
- Fixed dual-major assumptions.
- Fixed Top10/Top20-only language.
- Specific case-study examples.
- Case-specific Gantt timeline.
- Case-specific Word output.

## What remains

- Standard intake and evidence-ledger workflow.
- Current-source research process.
- Admissions-reader diagnosis framework.
- Single/dual/multi-track route architecture.
- School/program matrix logic.
- Activity/research/project design methodology.
- Timeline and Gantt chart workflow.
- Word/PDF document style guide.
- Ethical case benchmarking process.
- Tool-calling and QA rules.
