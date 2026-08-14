---
name: elite-us-undergrad-planning
description: Create high-end Chinese US undergraduate Top10/Top20 application planning reports from student files, transcripts, score reports, research plans, activity materials, and interview transcripts; includes admissions positioning, school/program strategy, core activity and competition pathways with advancement mechanisms, SAT/ACT and TOEFL/IELTS planning, parent-and-student-facing Markdown+Word, LifeEcho cream/teal styling, and polished Gantt charts. Use when the user asks for 美国本科规划案, 招生官诊断, 选校, SAT/托福规划, or a client-ready Word/Markdown report.
version: 1.2.0
---

# Elite US Undergraduate Planning Skill

Use this skill when the user asks for any of the following:

- 美国本科 Top10/Top20 / HYPSM / 工程 / 应用物理 / CS / 商科 / 文社科申请规划案
- 学生当前情况整理、成绩单诊断、招生官视角评估、申请画像定位
- 选校与专业列表、ED/EA/RD 策略、Reach/Target/Safety、主力冲刺学校
- 科研、竞赛、核心活动、旗舰项目、领导力项目、活动主线、晋级路径设计
- SAT/ACT、TOEFL/IELTS/Duolingo、新托福 1–6 分制规划
- 生成 Word、Markdown、Mermaid、甘特图、时间轴图表、申请规划交付件

The deliverable is a finished report for parents and students: accurate, evidence-based, actionable, visually polished. Consultant jargon stays in `working/`. Before writing client files, read [resources/client_facing_delivery.md](resources/client_facing_delivery.md) and [resources/report-voice.md](resources/report-voice.md).

---

## 0. Non-negotiable principles

1. **所有事实先来自材料，再来自官网核验，再来自明确推断。** Do not invent facts. Internal notes may use `信息待补齐` / `需核验`. Client sentences use `还需要补充` / `还需要核对`.
2. **必须读完全部材料。** Do not rely only on interview transcripts. Audit every uploaded transcript, grade report, résumé, PDF, project plan, Word file, image, and prior draft.
3. **用户修改后的文档优先。** If a user uploads a revised Word/MD version, treat it as the new base document and preserve their edits unless explicitly asked to rewrite.
4. **最新政策必须官网核验。** School testing policy, admissions deadlines, SAT dates, TOEFL scoring, competition requirements, advancement mechanisms, scholarship/aid rules, and program details must be verified with official or primary sources whenever current accuracy matters.
5. **每条建议都要能执行。** Every academic, activity, or competition recommendation needs task, owner, timeline, evidence, deliverable, and risk management.
6. **Word 版甘特图必须是图片或图表，不要只放 Mermaid 代码。** Markdown can include Mermaid code, but Word must embed a rendered PNG/SVG chart.
7. **对外表述要克制可信。** Avoid overstating competition pathways, awards, school odds, or “guaranteed” results. Use conditional strategy language.
8. **不要把某个竞赛路径写成所有学生的默认路径。** ISEF, Conrad, Olympiad, hackathon, debate, writing, entrepreneurship, service, or sports pathways should appear only when they match the student’s evidence and goals.
9. **保护隐私。** Do not bake one student's private data into a reusable template. Use provided student data only for the current report.
10. **姓名只写有证据的。** Transcript, passport, official ID, or explicit confirmation. Never invent a Chinese legal name from pinyin. If uncertain, omit it.
11. **给家长和学生看，不给同行看。** First principles, ordinary Chinese. No `招生官式诊断`, `画像`, `库内查询`, or AI filler. Each numbered section starts with `> **这一节的结论。**` in a professional briefing tone, not a pep talk, and never `小白`.
12. **选校来源对外只写内部数据库和学校官网。** If the internal catalog lacks art/conservatory/design schools, add them from official sites. Never write that the catalog is missing them.
13. **配色与 LifeEcho 一致，字必须看得清。** Page `F8F5ED`, ink `16211E`, headings `004D47` / `00685F`, fills `E6F5EE` with dark teal text. Never white or cream text on cream or mist.
14. **终稿无修改痕迹。** Overwrite `output/<EnglishName>_planning_report.md` and `.docx`. No `v2`, `修改版`, or changelog in the filename or body.

---

## 1. Workspace setup

Create a working directory for each project:

```text
project/
  input/          # user files copied here
  working/        # extraction notes, source log, outline
  output/         # final md/docx/png/zip
  assets/         # charts and images
```

Use `scripts/scaffold_project.py` if available:

```bash
python scripts/scaffold_project.py --project-dir ./project
```

Create and maintain these working files:

- `working/source_log.csv` — all files, pages/sections read, key facts, confidence, citation/source status.
- `working/fact_matrix.md` — student facts grouped by academics, tests, AP/IB/A-Level, activities, research, competitions, goals, constraints.
- `working/strategy_notes.md` — admissions positioning and decision logic.
- `working/activity_competition_map.md` — core activity/competition tracks, advancement mechanisms, deliverables, risks, fallback options.
- `working/open_questions.md` — missing facts to ask the user. Internal marker `信息待补齐`; client wording `还需要补充`.

Before drafting `output/`, read [resources/client_facing_delivery.md](resources/client_facing_delivery.md).

---

## 2. Material collection and extraction workflow

### 2.1 File audit checklist

For each user file, record:

- file name and type
- whether it is user-provided, prior draft, transcript, grade report, research plan, competition plan, score report, interview transcript, or image
- pages/sections reviewed
- key facts extracted
- conflicts with other materials
- confidence level: high / medium / low

### 2.2 How to read source types

- **成绩单/成绩报告：** Extract school, grade, class, course names, grades, component scores, teacher comments, attendance, and trends. Teacher comments can become recommendation-letter evidence.
- **录音逐字稿：** Extract goals, concerns, self-discipline issues, parent/advisor comments, planned tests, course intentions, activity details, competition plans, and direct corrections from the student.
- **科研计划/PDF/Word：** Extract project name, objectives, hardware/software stack, deliverables, competition timeline, mentor involvement, cost/scope boundaries, technical risks, and student contribution boundaries.
- **活动/竞赛材料：** Extract eligibility, team size, level, deliverables, deadline, judging rubric, advancement mechanism, expected output, and what evidence the student can collect.
- **图片/截图：** Extract test scores and visible tables. If OCR is unreliable, inspect visually or render page images.
- **用户修改后的 Word：** Treat as base. Preserve wording where it already fits the standard; patch gaps surgically.

### 2.3 Conflict resolution

When files conflict:

1. Prefer the most recently uploaded user-edited document for intentional wording.
2. Prefer official score reports/transcripts for scores.
3. Prefer the interview transcript for “what was actually discussed.”
4. Prefer official websites for current policy.
5. If unresolved, write `需核验` and explain the implication.

---

## 3. Required research behavior

### 3.1 What must be researched online

Search current official/primary sources for:

- SAT/ACT dates, registration deadlines, test policies
- TOEFL/IELTS/Duolingo score scale and test content
- each main school’s standardized testing policy, admissions plan restrictions, relevant majors/programs
- school program pages for Engineering Physics, Applied Physics, ECE, Mechanical Engineering, Energy, Materials, CS, business, humanities, etc. depending on the student
- each proposed competition/activity pathway’s eligibility, timeline, materials, judging criteria, team rules, advancement/qualification mechanism, and official organizer
- compliance rules for projects involving humans, minors, data privacy, biological materials, batteries/electrical systems, AI, hardware safety, or public-facing claims
- financial aid policies if budget/need-based aid is mentioned

### 3.2 Source quality hierarchy

1. Official school admissions and department websites
2. Official testing organizations: College Board, ACT, ETS, IELTS, Duolingo English Test
3. Official competition/activity organizers and rulebooks
4. Government or recognized education bodies
5. Reputable secondary sources only when official pages do not provide the needed context

### 3.3 Citation/source handling

In the report, include a final `官网信息核验摘要` or footnote-style source section with official URLs. In user-facing ChatGPT responses, cite official sources when web research was used.

---

## 4. Planning report structure

Client report sequence (parent/student titles). Each numbered section starts with `> **这一节的结论。**`

1. `学生当前情况，以及大学会怎么看`
2. `目标专业与学校策略`
3. `课程、AP/IB/A-Level 与 GPA 规划`
4. `SAT/ACT 与语言成绩规划`
5. `科研、核心活动与竞赛`（艺术方向可写成 `作品、核心活动与竞赛`）
6. `申请材料怎么写`
7. `时间轴安排`
8. `风险管理，以及还缺哪些材料`
9. `官网信息核验摘要`
10. `规划甘特图`
11. `接下来怎么做`（可选短节）
12. `附录：主要官网链接`

For shorter assignments, keep the same logic but compress sections. Do not use `招生官式诊断` or `画像` as client headings. Full title and wording rules: [resources/client_facing_delivery.md](resources/client_facing_delivery.md).

---

## 5. Admissions diagnosis standard

### 5.1 Basic profile table

Always include a table with:

- 姓名
- 学校/体系
- 当前年级/预计毕业/入学季
- 目标方向
- GPA/排名/课程难度
- TOEFL/IELTS/Duolingo
- SAT/ACT
- AP/IB/A-Level/高级课程
- 科研/项目
- 竞赛/奖项
- 领导力/影响力
- 管理特点/学习习惯
- 预算/奖学金/ED 意愿/地理偏好

### 5.2 Internal diagnosis vs client writing

Do the admissions-reader diagnosis in `working/strategy_notes.md` using [resources/admissions_strategy_rubric.md](resources/admissions_strategy_rubric.md):

- academic spike / impact spike / intellectual vitality
- under-verified or risky claims
- recommendation-letter evidence
- the story that can tie academics, activities, and personality together

The client report translates that diagnosis into ordinary Chinese: what the transcript shows, what it means for this student’s chances, and what to do next. Do not paste the rubric labels into client headings.

### 5.3 Required client summary blocks

In the first section, after the opening conclusion, include:

- 目前情况（table）
- 成绩单在说什么
- 我们怎么理解这份材料（one paragraph, specific, not generic）
- 现在最需要盯住的三件事
- 已经有的有利条件

Missing facts: `还需要补充`, not `信息待补齐`.

---

## 6. School and major strategy standard

### 6.1 Major positioning

Do not default to “pure CS” unless the evidence supports it. For engineering/physics students, consider:

- Engineering Physics
- Applied Physics
- Electrical Engineering
- Mechanical Engineering
- Materials Science
- Energy Systems / Sustainable Energy
- Data for Physical Systems / AI Control
- Systems Engineering / Operations Research

For other students, choose major labels based on evidence, not aspiration alone. Examples:

- Economics / Business / Entrepreneurship only if there is quantitative, venture, finance, policy, or leadership evidence.
- Psychology / Cognitive Science / Education only if there are research, service, writing, or community evidence lines.
- Humanities / social science only if there is writing, debate, publication, archive, history, philosophy, language, policy, or civic evidence.
- Arts/design/media only if there is a portfolio, audience, exhibition, publication, or technical creative output.

Explain why the major label matches the student’s actual evidence.

### 6.2 Main target schools

When the user asks for “主力冲刺学校 3 所,” provide exactly 3 main schools plus 1–2 backups.

For each main school include:

- 学校
- 推荐学院/专业
- 申请策略: ED/REA/EA/RD/test-optional/test-required logic
- 为什么适配该学生
- 触发条件: scores, GPA, AP/IB/A-Level, project, competition/activity outcomes
- 风险点

### 6.3 Extended school table

Include a broader school/program list with parent-readable tiers, for example:

- 可以冲、但很难
- 重点准备
- 较难
- 作为补充
- 相对更稳
- 最后备选

Internal notes may still use Reach / Target / Safety. For each school, include program options and strategy comments.

### 6.4 Batch strategy

Always include 2–3 scenarios:

- 考试分数达到可提交线之后
- 分数中等、作品或活动更完整时
- 分数仍低、决定不交时

Tie ED/EA/RD choices to the student’s actual future score thresholds. On first mention in the client report, explain 提前绑定 / 非绑定提前申请 / 常规申请.

### 6.5 Where the school list comes from

Use the internal school database when the user points to one, and always check official program pages. If the database is national-university / QS scoped and misses art, conservatory, or design schools, add those from official sites.

Client sentence: `学校名单来自我们的内部数据库和各校官网。` Never write 库没有, SQLite, subagent, or query mechanics.

---

## 7. Course, AP/IB/A-Level, GPA planning standard

Correctly distinguish:

- exams/courses already taken
- scores pending
- planned but not yet finalized courses/exams
- school courses vs external exams

For each future course/exam:

- priority: 必选 / 强烈建议 / 可选 / 不建议
- reason
- risk control
- target grade/score

GPA planning must include:

- target GPA trend
- no-B policy for core courses when targeting Top10/Top20, if appropriate
- weekly review mechanism
- quiz/test 48-hour intervention rule
- teacher communication plan
- use of teacher comments as recommendation evidence

---

## 8. Test planning standard

### 8.1 SAT/ACT

Include:

- current diagnostic baseline
- target score bands: submit baseline, Top20 line, Top10 line
- section thresholds
- test dates and registration-decision rule
- weekly training structure
- score-use logic for test-optional/test-required schools

Do not encourage low-value “practice official tests” if the first score will be strategically weak. Use a decision threshold based on mock scores.

### 8.2 TOEFL / IELTS / Duolingo

Use the current score scale relevant to the student. If the student uses TOEFL 1–6 scale plus 0–120 concordance, plan in both:

- current overall and sub-scores
- first target
- final target
- subskill gaps
- weekly training load
- when language prep should give way to SAT/ACT or schoolwork

Write mechanisms, not just goals:

- Listening: note structure and retelling
- Speaking: timed recordings and re-recording loop
- Writing: task-specific feedback and authentic example bank
- Reading: accuracy/speed and transfer to SAT/ACT reading

---

## 9. Research/project planning standard

For each research/project track, include:

- project name
- current basis from materials
- why the project is strategically useful
- research question or product problem
- method and tools
- input variables/data
- control experiments or evaluation criteria
- measurable indicators
- deliverables
- milestone table
- mentor/student contribution boundary
- risks and compliance
- how it supports school/major narrative

### 9.1 Project credibility test

A project is not ready for Top10/Top20 presentation unless the student can explain:

- what problem is being solved
- why it is not generic
- what data/evidence were collected
- what the comparison/control group or evaluation benchmark is
- what failed or changed
- what the result proves and does not prove
- what the student personally did

### 9.2 AI project rule

If adding AI to a student project, require:

- clear prediction/classification/generation target
- input features and data source
- baseline model or non-AI comparison
- performance metrics
- output connected to a decision or action
- responsible AI disclosure and non-fabricated citations

Do not write “加入 AI” as a decorative label.

---

## 10. Core activity and competition pathway standard

### 10.1 Pathway truthfulness

Every designed activity or competition track should be treated as an evidence channel, not a guaranteed outcome. Never imply that participating in one local activity automatically yields a national/international result.

For each pathway, write the chain explicitly:

```text
preparation/output -> submission/selection -> possible advancement -> final/recognition -> application evidence
```

If the activity has **no formal advancement mechanism**, say so and explain its value instead: audience, measurable impact, publication, third-party evaluation, portfolio, recommendation evidence, or leadership proof.

If the activity has **formal advancement**, name the mechanism:

- score threshold or cutoff, such as AMC -> AIME -> USAMO-style pathways
- local/regional/national/international rounds
- affiliated fair or official representative selection
- application review plus interview
- nomination/recommendation pool
- invitation based on prior results
- team-based regional qualifier
- judges’ award leading to a final round
- publication/editorial review
- showcase/demo day selection

### 10.2 Required pathway table

For each core pathway include:

| 字段 | 要求 |
|---|---|
| 主线定位 | working notes may use spike labels; client table uses ordinary Chinese |
| 活动/竞赛名称 | Use official name if known; otherwise mark as still needing a check |
| 为什么适配 | Tie to student evidence and target major |
| 晋级/筛选机制 | Explain exact path, or state there is no formal advancement |
| 学生策略 | What the student should do differently to be competitive |
| 交付材料 | paper, poster, video, code, portfolio, pitch deck, data book, essay, training log, etc. |
| 时间窗口 | months/weeks and decision points |
| 背书/证据 | award, finalist status, publication, users, partners, judges, mentor letter, analytics |
| 风险点 | eligibility, team dependence, time cost, policy, safety, oversaturation |
| 做不成时怎么办 | alternate competitions, public release, local showcase, school club, independent output |

### 10.3 Pathway examples by field

Use only the examples that match the student. Details and field-specific chains: [resources/core_activity_competition_pathways.md](resources/core_activity_competition_pathways.md).

Do not list too many random competitions. Depth and evidence matter more than activity count.

### 10.4 If ISEF/science fair is explicitly relevant

Only include ISEF-specific detail when the user or materials explicitly point to a science-fair/ISEF-style target. Frame the path conditionally:

- local/science society/affiliated fair or recognized selection is the possible entry channel if supported by official rules
- international participation depends on official selection and compliance review
- prepare local-language materials and official English materials if needed
- include category selection, research year/continuation rules, team rules, SRC/IRB/risk assessment, display/safety, AI use disclosure, and booth interview training
- include fallback competitions/outputs if the student does not advance

### 10.5 Competition/activity table

For every report, include at least one table that makes the student’s core activity and competition architecture visible. A strong table usually has 3–5 pathways:

1. one primary academic or research/project pathway
2. one subject-depth pathway
3. one leadership/impact pathway
4. one fallback or breadth pathway
5. one personal dimension if it strengthens narrative

Do not list too many random competitions. Depth and evidence matter more than activity count.

---

## 11. Leadership and impact planning standard

Convert activities into impact systems. For sports, arts, service, clubs, internships, family responsibility, or community activity, write:

- current evidence
- role progression
- what system the student can improve
- measurable indicators
- evidence to collect
- narrative use
- whether there is a competition/showcase/advancement path or whether value comes from impact evidence

Avoid writing “参加志愿/实习/社团” without measurable outputs.

---

## 12. Application narrative standard

Include:

- activity list priority order
- recommendation-letter strategy
- essay narrative direction
- possible main personal statement theme
- why-major evidence bank
- additional information strategy when needed

The narrative should explain both strengths and growth areas without sounding defensive.

---

## 13. Timeline and Gantt chart standard

### 13.1 Timeline

Write timelines at three levels:

- month-level from now to enrollment
- week-level for summer, Sep–Nov, Dec–Jan
- milestone-level for tests, competition submissions, project publication, school deadlines, and advancement decisions

### 13.2 Gantt chart

Use `scripts/render_gantt.py` when possible.

Example:

```bash
python scripts/render_gantt.py \
  --input examples/gantt_tasks.yaml \
  --output output/planning_gantt.png \
  --mermaid-output output/planning_gantt.mmd
```

Chart requirements:

- Chinese labels readable
- grouped by section with parent-facing labels (SAT与托福, 12年级成绩, 作品, not 标化 / SlideRoom)
- milestones marked with diamonds or stars
- cream page `#F8F5ED`, dark ink labels, no pale text
- x-axis dates readable and rotated if needed
- activity/competition advancement windows clearly shown when relevant
- embedded in Word as image
- included in Markdown as `![规划甘特图](assets/planning_gantt.png)` plus optional Mermaid code

---

## 14. Output generation standard

Produce at least these finished names (no `v2` / `修改版`):

```text
output/<EnglishName>_planning_report.md
output/<EnglishName>_planning_report.docx
output/assets/planning_gantt.png
```

Optional:

```text
output/<student>_planning_package.zip
output/source_log.csv
output/gantt_tasks.yaml
```

### 14.1 Markdown output

Markdown should be clean and readable:

- Each numbered section starts with `> **这一节的结论。**`
- Names in the report are evidenced; no pinyin-guessed Chinese legal name
- No `库内`, SQLite, subagent, `招生官式`, `画像`, `小白`, `v2`, or `修改版`
- Use compact tables where helpful.
- Include image references for charts.
- Include Mermaid code only if the user wants renderable code or if useful as appendix.
- Avoid raw HTML unless necessary.

### 14.2 Word output

Word should be client-ready:

- LifeEcho palette from `templates/docx_style_config.yaml` (page `F8F5ED`)
- dark ink / teal headings; table and summary fills `E6F5EE` with dark teal text, never white on mist
- section summaries rendered as callout boxes, not faint italic quotes
- tables should not overflow page width
- embed Gantt PNG/SVG image instead of Mermaid code
- include captions under charts
- Microsoft YaHei + Georgia, inspect the rendered document if possible

Use `scripts/build_docx.py` if available:

```bash
python scripts/build_docx.py \
  --input output/<student>_planning_report.md \
  --output output/<student>_planning_report.docx \
  --style templates/docx_style_config.yaml
```

If using Pandoc/LibreOffice or any other converter, inspect the result and fix table/figure overflow.

---

## 15. Quality gate before final delivery

Before returning files, verify:

- All uploaded files were reviewed or explicitly marked as unreadable.
- Key facts match source materials.
- Current policies have official-source verification.
- Missing facts in the client report are `还需要补充`, not guessed.
- No invented Chinese name; uncertain names omitted.
- Each section has `这一节的结论`.
- Client file has no `库内` / SQLite / subagent / `v2` / `修改版`.
- School strategy contains main 3 schools if requested.
- Core activity and competition pathways are truthful, conditional, and include advancement/selection mechanisms where applicable.
- Research/project plan includes data, controls/evaluation, outputs, and compliance.
- SAT/TOEFL plan matches the conversation and current format.
- Timeline is actionable and not vague.
- Word contains a rendered Gantt chart image.
- Markdown and Word are consistent.
- File names are clean and user-ready.

Run:

```bash
python scripts/md_quality_check.py output/<student>_planning_report.md
```

Treat warnings as items to review, not as automatic failures.
