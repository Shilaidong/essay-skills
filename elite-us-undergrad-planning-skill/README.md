# Elite US Undergraduate Planning Skill

A reusable Codex/Agent skill for producing high-end Chinese planning reports for US undergraduate Top10/Top20 applications. It covers material collection, transcript/interview synthesis, admissions positioning, school/program strategy, standardized testing, research/project planning, core activity and competition pathways with truthful advancement mechanisms, Markdown/Word delivery, and polished Gantt charts.

## Install

Copy this directory into your Codex skills folder or your project-level skills directory, depending on your Codex setup.

```text
elite-us-undergrad-planning-skill/
  SKILL.md
  scripts/
  templates/
  resources/
  examples/
```

The core entry point is `SKILL.md`, which contains the YAML front matter and instructions used by Codex.

## Typical usage prompt

```text
Use the elite-us-undergrad-planning skill.
Read all files in ./input, including transcripts, score reports, research plans, activity materials, and my edited draft.
Produce a client-ready Chinese application planning report in Markdown and Word.
Word must include a rendered Gantt chart image, not Mermaid code.
Focus on Top10/Top20 strategy and design core activity + competition pathways. If a pathway has advancement or selection rounds, write the mechanism clearly; if not, state that its value comes from evidence/impact/output.
```

## Dependencies for scripts

```bash
pip install -r requirements.txt
```

Dependencies are intentionally lightweight:

- python-docx
- matplotlib
- PyYAML

## Basic workflow

```bash
python scripts/scaffold_project.py --project-dir ./project
# Put user files into ./project/input
# Draft report in ./project/output/report.md
python scripts/render_gantt.py --input examples/gantt_tasks.yaml --output ./project/assets/planning_gantt.png --mermaid-output ./project/assets/planning_gantt.mmd
python scripts/build_docx.py --input ./project/output/report.md --output ./project/output/report.docx
python scripts/md_quality_check.py ./project/output/report.md
```

## Important conventions

- Read all user files first.
- Preserve user-edited drafts as base documents.
- Verify current school/test/competition/activity policies on official websites.
- Do not default every student to one competition path.
- For every designed competition/activity path, write the advancement mechanism or state `无正式晋级机制`.
- Mark missing facts as `信息待补齐`.
- Use rendered Gantt charts in Word.

## Chinese font note for Gantt charts

The Gantt renderer automatically tries common Chinese-capable fonts such as Microsoft YaHei, SimHei, PingFang SC, Source Han Sans, WenQuanYi Micro Hei, and Noto CJK. If labels render as boxes, install a CJK font in the runtime environment and re-run `scripts/render_gantt.py`. Do not package or redistribute commercial font files.
