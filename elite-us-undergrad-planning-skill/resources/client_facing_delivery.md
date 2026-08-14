# Client-Facing Delivery Rules

The Markdown and Word in `output/` are read by parents and students. `working/` may use consultant terms. Client files may not.

Read this file before drafting the client report.

## 1. Names

- Use only names with documentary evidence: transcript, passport, official ID, or explicit confirmation in a meeting/email.
- A preferred or English name is allowed if teachers, the student, or a completed interview actually use it.
- Never reverse-engineer a Chinese legal name from pinyin. Pinyin is not a legal name.
- If the Chinese legal name is unknown, omit it. Write that the application form follows the passport, and that the family should confirm it before anything is entered into a system.
- If a name is uncertain, delete it from client files. Do not present a guess. A wrong name causes more harm than a blank.

## 2. First principles, parent voice

Write from what is true and what the family must do next. Do not write from admissions-office jargon.

Client section titles use ordinary Chinese, for example:

- `学生当前情况，以及大学会怎么看`
- `目标专业与学校策略`
- `课程、AP 与 GPA 规划`
- `SAT 与托福规划`
- `作品、核心活动与竞赛` or `科研、核心活动与竞赛`
- `申请材料怎么写`
- `时间轴安排`
- `风险管理，以及还缺哪些材料`
- `官网信息核验摘要`
- `规划甘特图`

Do the Academic Spike / Impact Spike / Intellectual Vitality diagnosis in `working/strategy_notes.md`. Do not put those labels, or `招生官式诊断`, `当前画像`, `画像结论`, in the client report.

On first use, explain application rounds in plain language:

- 提前绑定（ED）：录了原则上要去，全家只能绑一所
- 非绑定提前申请（EA）：可以早知道结果，录了不必一定去
- 常规申请（RD）：大多数学校的正常轮次

School-list tiers in the client table should be readable, not Reach/Target/Safety jargon. Prefer: 可以冲、但很难 / 重点准备 / 较难 / 作为补充 / 相对更稳 / 最后备选.

Gantt labels should be equally plain. Avoid `标化`, `G12政策`, `SlideRoom`, `复盘窗口` as the only wording.

## 3. Section summaries

Every numbered client section starts with a professional two-to-four-sentence summary:

```markdown
> **这一节的结论。** ……
```

Tone: a counselor briefing a family. Direct, specific, adult. Not cheerful, not simplified-for-children, not pep-talk.

Never write `小白`, `通俗易懂`, `给家长科普`, or similar.

## 4. Words that do not belong in client files

Do not use these as headings or as the report’s working vocabulary:

- 招生官式诊断、当前画像、画像结论、Academic Spike、Impact Spike、Intellectual Vitality
- 库内、库外、SQLite、subagent、子代理、查询目录、catalog
- 闭环、抓手、赛道、长板、短板
- 对冲路径（client text: 备选 / 替代）
- 信息待补齐（client text: 还需要补充 / 家里还需要补）
- 小白、温馨提示、综上所述、赋能、落地执行、颗粒度、全方位、深度赋能

`招生官` may appear once, only to explain who reads the transcript, e.g. `大学招生办公室的老师（招生官）`. It is not a section title.

Do not invent awards, odds, or “一定能进”. Do not write `稳进`.

## 5. How school lists are sourced

Research may use an internal school database plus official websites. Specialized schools missing from the database (art, conservatory, design, etc.) must still be added from official sites when they fit the student.

Client wording:

> 学校名单来自我们的内部数据库和各校官网。

Never write that the database lacks a school type, that a query missed, or that a subagent filled a gap.

## 6. Visual theme

Match the LifeEcho report palette. Cream page, dark ink, teal headings. Text and background must stay readable.

| Role | Hex |
|---|---|
| Page | `F8F5ED` |
| Ink | `16211E` |
| Heading | `004D47` |
| Heading 2 / header | `00685F` |
| Table / summary fill | `E6F5EE` |
| Text on that fill | `004D47` |
| Gold | `8A6A2F` |
| Line | `D6CEBF` |
| Muted | `3A4C47` |

Never use white, cream, or teal-mist as font color. Table headers and section summaries are dark teal on mist, never white on mist.

Use `templates/docx_style_config.yaml`, `scripts/build_docx.py`, and `scripts/render_gantt.py`. Word must embed the Gantt PNG.

Per-student YAML may set `header.text` to `{English or preferred name} 美国本科申请规划`. The script default header is generic.

## 7. Final files have no revision trace

Overwrite:

```text
output/<EnglishName>_planning_report.md
output/<EnglishName>_planning_report.docx
output/assets/planning_gantt.png
```

Do not put `v2`, `修改版`, `revised`, `draft`, or a changelog in the filename or the document body. The family should receive one finished report.

## 8. Missing facts

Internal notes may use `信息待补齐` / `需核验`. Client sentences use `还需要补充` / `还需要核对`, and say what the family should send.
