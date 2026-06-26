---
name: study-abroad-application-report-standardizer
description: Standardized workflow for researching, analyzing, and producing study-abroad application strategy reports for any student profile, destination country, degree level, target tier, major direction, or document format. Use when asked to evaluate applicant competitiveness, plan majors and school lists, design academic/activity/research roadmaps, create timelines, prepare application materials, or generate polished Word/PDF consulting reports. Always verify current admissions facts with sources; never fabricate credentials, outcomes, cases, partnerships, or admission guarantees.
version: "2.0.0"
language: zh-CN
compatibility: Codex, OpenCode, and agent runtimes with optional web, file, Python, spreadsheet, and document-rendering tools.
license: MIT
---

# Study-Abroad Application Report Standardizer

## Mission

Convert scattered student materials, uploaded files, current admissions research, and counselor judgment into a complete, evidence-based, visually polished application planning report.

This skill is **universal**. It is not tied to one student, one country, one major, one school tier, or one format. Use it for undergraduate, graduate, transfer, boarding-school, foundation, pre-college, and multi-country planning when the task requires structured admissions analysis and client-ready documentation.

Default working language is the user's language. If the user writes in Chinese, write the report in Chinese while preserving precise English names for schools, colleges, majors, tests, programs, and policies.

## What to produce

Depending on the user request, produce one or more of:

- A polished application strategy report in `.docx`, `.pdf`, or Markdown.
- A school/program matrix with admissions requirements and strategic fit.
- A student diagnosis with academic, activity, research, leadership, writing, testing, and risk assessment.
- A major/route decision framework for one-track, dual-track, or multi-track applicants.
- A background-building plan with project/research/activity designs, milestones, evidence, and verification paths.
- A standardized testing and language-exam plan.
- A month-by-month and week-by-week timeline.
- A rendered Gantt chart image for Word/PDF delivery.
- A source ledger, evidence ledger, risk register, and next-step checklist.

## Trigger boundaries

Use this skill when the user asks for:

- 留学申请规划、选校定位、专业定位、活动规划、科研规划、竞赛规划、文书规划、申请时间轴、申请报告、顾问版方案、Word排版报告。
- U.S., U.K., Canada, Australia, Singapore, Hong Kong, Europe, or multi-country admissions planning.
- Undergraduate, graduate, transfer, high-school, summer program, or scholarship applications.
- Converting uploaded notes, transcripts, resumes, certificates, essays, meeting transcripts, or school lists into a coherent plan.

Do not use this skill to:

- Promise or imply guaranteed admission.
- Invent awards, scores, publications, impact numbers, student roles, recommender opinions, admissions cases, internships, partnerships, media coverage, or school policies.
- Misrepresent public online cases as proprietary internal cases.
- Hide paid, family, or agency involvement when it materially affects a project.
- Provide legal, tax, medical, immigration, or financial advice beyond general planning information.

## Core principles

1. **Evidence before strategy.** Build an evidence ledger before writing recommendations.
2. **Current facts require current sources.** Deadlines, testing policy, English requirements, tuition, aid, portfolio rules, course names, and admissions rounds must be checked from official or primary sources when tools permit.
3. **Separate status types.** Label claims as `VERIFIED`, `STUDENT_REPORTED`, `TARGET`, `ASSUMPTION`, or `MISSING`.
4. **One final identity.** Exploration can be multi-track; the final application must read as coherent.
5. **Specificity beats branding.** Exact majors, exact colleges, exact requirements, exact milestones, and exact evidence are stronger than vague school prestige.
6. **Depth beats cosmetic scale.** Original work, rigorous method, iteration, adoption, and verification matter more than logos, websites, chapters, or follower counts.
7. **No unsupported causality.** A successful applicant case can illustrate a pattern; it does not prove that one activity caused admission.
8. **Client-ready documents need visual QA.** Word/PDF reports must be rendered and inspected when document tools are available.
9. **Transparent uncertainty.** If a fact is unverified or unstable, mark it and provide a verification action.
10. **Protect privacy.** Use the minimum necessary personal data; handle minors, grades, scores, locations, health, family finances, and identifying photos conservatively.

## Standard workflow

### Phase 0 — Scope and deliverable contract

Extract and restate:

- Student name, grade, graduation year, target entry year.
- Current school, city, curriculum, school type, grading system, and class context.
- GPA/rank/course rigor/subject strengths/weaknesses.
- Tests: SAT/ACT, TOEFL/IELTS/Duolingo, AP/IB/A-Level/other national exams.
- Activities: research, projects, competitions, leadership, athletics, arts, service, work, internships, family resources.
- Intended countries, degrees, major directions, target tier, budget, aid need, ED/EA/REA willingness, geographic constraints.
- Existing materials uploaded: transcripts, resumes, awards, essays, school lists, PDFs, spreadsheets, screenshots, meeting notes.
- Output requirements: language, length, Word/PDF/Markdown, font, visual style, citations, case modules, Gantt chart, tables.

If a missing item changes strategy materially—especially citizenship, budget, aid need, curriculum, graduation year, GPA/rank, or ED feasibility—ask one concise clarification question. If the user wants immediate output, proceed with assumptions clearly marked.

### Phase 1 — Intake diagnosis and evidence ledger

Create an internal or external ledger with fields:

- Claim or data point.
- Category: academic, testing, activity, award, school, policy, deadline, budget, essay, recommender, family constraint.
- Status: `VERIFIED`, `STUDENT_REPORTED`, `TARGET`, `ASSUMPTION`, `MISSING`.
- Source or proof.
- Date checked.
- Strategic implication.
- Follow-up action, owner, and deadline.

Use `assets/evidence_ledger_template.csv` when a file deliverable is needed.

Never write future targets as completed achievements. Replace “has impacted 500 students” with “target: reach 500 students by [date]” unless verified.

### Phase 2 — Current research

Research only what is necessary for the strategy. Prioritize:

1. Official admissions pages.
2. Official school, department, catalog, and program pages.
3. Official testing organizations.
4. Government or institution pages for visas, work rules, and costs.
5. Reputable first-person profiles, university news, competition pages, or project sites for benchmark cases.
6. Secondary sources only when primary sources are unavailable, and mark their lower confidence.

Capture:

- Exact institution, college/faculty/school, major/program name.
- Whether applicants apply to the university, college, school, department, or major.
- Required or recommended subjects.
- Testing and English-language policy.
- Portfolio, audition, writing sample, interview, prescreen, or supplemental material rules.
- Application rounds and restrictions.
- Financial-aid or scholarship posture if relevant.
- Deadline date and date checked.
- Source URL or citation note.

Use `assets/source_ledger_template.csv` for traceability.

### Phase 3 — Admissions-reader diagnosis

Write the profile as an admissions reader would see it **today**, not as the family hopes it will be.

Include:

- One-sentence applicant archetype.
- Current strengths.
- Current weaknesses.
- Academic evidence.
- Activity/impact evidence.
- Intellectual vitality or professional maturity evidence.
- Writing/storytelling assets.
- Three to five core risks.
- Missing information list.
- Confidence level for recommendations.

Useful archetypes include:

- Academic/research-oriented applicant.
- Impact/leadership-oriented applicant.
- Creative/portfolio applicant.
- Professional/career-applied applicant.
- Entrepreneurial applicant.
- Humanistic writing/social-science applicant.
- STEM builder/engineering applicant.
- Balanced high-achiever needing sharper differentiation.

### Phase 4 — Route architecture

Use the user's actual situation:

- **Single-track:** one dominant major/career direction.
- **Dual-track:** two plausible directions that share evidence temporarily but require a decision gate.
- **Multi-country:** same student translated differently for different admissions systems.
- **Portfolio vs non-portfolio:** creative/design/art/architecture/music/theatre tracks require separate evidence standards.
- **Direct-entry vs flexible-entry:** some systems require exact major fit at application; others allow exploration.
- **Graduate/professional:** emphasize prerequisite courses, research/professional experience, faculty fit, statement of purpose, and recommendations.

For each track, define:

- Academic field and exact program families.
- Core question or professional problem.
- Required academic preparation.
- Evidence needed before submission.
- Flagship activities/research/projects.
- School/program fit logic.
- Essay narrative.
- Recommendation evidence.
- Risks and pivot path.
- Decision gate date and measurable criteria.

Do not force a dual-track structure when the student has one clear direction. Do not maintain multiple tracks past the point where they dilute the final application.

### Phase 5 — School/program strategy

For each recommended school/program, include:

- School and location.
- College/faculty/school and exact major/program.
- Why it fits the student's route.
- Evidence chain linking student profile to curriculum, research, studio, co-op, clinical, fieldwork, career, or community opportunities.
- Application round recommendation.
- Testing/portfolio/interview/writing-sample implications.
- Financial or procedural cautions.
- Risk level.

Use tiers the user requests. If the user excludes safeties, state that no school in a selective tier is a true safety. If budget is unknown, do not treat a school as financially safe.

### Phase 6 — Background-development design

Build no more than three main lines plus one backup line unless the user explicitly requests more.

Each main line must include:

1. Student origin: why this student, not a generic applicant.
2. Target population/problem.
3. Research or project question.
4. Method and tools.
5. 4-week, 8-week, and 12-week milestones.
6. Deliverables.
7. Quantitative and qualitative metrics.
8. Verification and third-party evidence path.
9. Student ownership and team roles.
10. Risks: ethics, minors, data, safety, permission, budget, publicity, sustainability.
11. Fallback scope if approvals or resources fail.
12. How it translates into activity lists, essays, recommendations, portfolios, interviews, or statements.

Reject or redesign activities that are only:

- One-off volunteering.
- Paid participation with no independent output.
- A website/archive with no original work.
- Inflated founder title with weak operations.
- Unverified large-scale chapters.
- Publication without clear authorship and methods.
- Family-resource access without student contribution.

### Phase 7 — Academic and testing plan

Plan backward from deadlines and school requirements:

- Course selection and course rigor.
- GPA/rank protection.
- Prerequisite subjects by country/major.
- AP/IB/A-Level/national exam strategy.
- SAT/ACT or alternative testing strategy.
- TOEFL/IELTS/Duolingo or English waiver strategy.
- Portfolio, writing sample, research abstract, audition, interview, or SOP requirements.
- Stop rules: when to stop testing and prioritize applications.

Use target score ranges, not false precision. Mark whether target scores are official minimums, competitive internal goals, or assumptions.

### Phase 8 — Essays, recommendations, and materials

Map each application story to evidence:

- Main personal statement or Common App essay.
- Why major / why school.
- Activity essay.
- Community/diversity/belonging essay.
- Intellectual vitality essay.
- Career goal / SOP.
- Portfolio artist/designer statement.
- Additional information.
- Recommendation strategy and recommender evidence packets.

Never let the essay claim an outcome that the evidence ledger cannot support.

### Phase 9 — Timeline and Gantt chart

Build a timeline with:

- Monthly structure from current date to enrollment.
- Weekly granularity for high-risk windows: summer build phase, September–November submission phase, December–January RD phase, exam months, portfolio months.
- Milestones for tests, grades, project releases, essays, recommendation requests, school-list lock, application submissions, interviews, financial forms, enrollment.
- Workload limits and stop rules.

Use a rendered Gantt image for Word/PDF. Do not place raw Mermaid code in client-facing Word unless requested.

Use `assets/timeline_template.csv` and `scripts/make_gantt.py` when generating a visual timeline.

### Phase 10 — Draft report

Default report order:

1. Cover and use note.
2. Executive summary.
3. Student information and missing items.
4. Admissions-reader diagnosis.
5. Positioning and route architecture.
6. Track/program plans.
7. School/program matrix and application-round strategy.
8. Academic and testing plan.
9. Background-development plan.
10. Essay, recommendation, and materials strategy.
11. Timeline and Gantt chart.
12. Optional benchmark/case module.
13. Risk register and verification checklist.
14. Sources and appendices.

Adapt order to the user's requested template, but keep diagnosis, source basis, strategy, execution plan, timeline, and risk management visible.

### Phase 11 — Document production

For Word reports:

1. Draft content in Markdown or YAML first.
2. Generate tables and figures programmatically when possible.
3. Render Gantt as PNG.
4. Generate DOCX using a consistent style system.
5. Apply requested fonts. For Chinese reports, default East Asian font is `宋体`/`SimSun`; do not include or distribute font files.
6. Render DOCX to page images or PDF when tools are available.
7. Inspect every page for clipping, broken tables, missing glyphs, inconsistent heading spacing, low-resolution images, orphan headings, and oversized tables.
8. Revise and re-render until clean.

Use `scripts/build_docx.py` and `scripts/make_gantt.py` as starting utilities. Use a stronger local document toolchain if available.

### Phase 12 — Quality gate and delivery

Before final delivery, verify:

- Current admissions facts are sourced or marked as needing verification.
- Student achievements are separated from targets.
- School/program names are exact.
- Program fit is evidence-based, not prestige-based.
- Activities have methods, deliverables, milestones, verification, and risks.
- Early-application strategy respects restrictions and budget.
- Timelines are feasible with coursework.
- Cases, if included, are ethically anonymized and not falsely proprietary.
- DOCX/PDF is visually clean.
- Final response links only final deliverables unless the user asks for working files.

## Tool-use protocol

### Web or browser tools

Use web research when facts may change or when official details matter:

- Admissions deadlines and rounds.
- Testing policies.
- English requirements.
- Course prerequisites.
- Major/program structure.
- Portfolio/interview/audition/writing sample rules.
- Tuition, financial aid, scholarship, cost of attendance.
- Visa or work rules.
- Recent school policy changes.
- Public benchmark cases.

Rules:

- Prefer official pages.
- Capture date checked.
- Keep a source ledger.
- Do not over-rely on rankings or forum claims.
- If web is unavailable, mark items `NEEDS CURRENT VERIFICATION`.

### File tools

When the user uploads files:

- Preserve originals.
- Extract text/tables before summarizing.
- Use OCR only when necessary and flag uncertainty.
- Cross-check transcript/screenshots carefully.
- Do not infer grades, ranks, or awards beyond what the file shows.
- Convert messy notes into structured ledgers.

### Python/data tools

Use Python for:

- Cleaning source/evidence ledgers.
- Generating school matrices.
- Creating Gantt charts.
- Producing DOCX files.
- Rendering tables and simple charts.
- Validating date ranges and milestones.
- Running consistency checks.

Keep generated files deterministic and reproducible. Store reusable inputs in CSV/YAML.

### Document tools

For DOCX/PDF:

- Use styles instead of manual formatting everywhere.
- Keep table widths within page margins.
- Use repeating table headers for long tables.
- Convert web citations into readable endnotes or source tables.
- Use Gantt images rather than code blocks for timelines.
- Render and inspect before delivery when possible.

### Spreadsheet tools

Use spreadsheets for structured matrices and ledgers. Keep columns stable and avoid merging cells in machine-readable files. When exporting into Word, simplify columns to avoid unreadable wide tables.

## Reference files

Read these only when needed:

- `references/workflow.md` — detailed end-to-end process.
- `references/research_and_sources.md` — source hierarchy, citation, and verification rules.
- `references/tool_calling.md` — operational tool-use playbook.
- `references/strategy_frameworks.md` — route architecture, applicant positioning, and activity frameworks.
- `references/report_blueprint.md` — reusable report section templates.
- `references/document_style_guide.md` — Word/PDF visual design standards.
- `references/case_benchmarking.md` — ethical use of public successful-applicant cases.
- `references/quality_gates.md` — final QA rubric.

## Assets and scripts

Templates:

- `assets/student_intake_template.yaml`
- `assets/evidence_ledger_template.csv`
- `assets/source_ledger_template.csv`
- `assets/school_matrix_template.csv`
- `assets/timeline_template.csv`
- `assets/report_outline.md`
- `assets/document_style_tokens.yaml`

Scripts:

- `scripts/make_gantt.py` — CSV timeline to PNG Gantt chart.
- `scripts/build_docx.py` — Markdown report to styled DOCX.
- `scripts/validate_ledgers.py` — basic ledger and date validation.
- `scripts/build_report_scaffold.py` — generate a Markdown report skeleton from intake YAML.

## Standard final response behavior

When delivering artifacts, provide concise links and mention only material limitations, such as missing current verification or files that could not be rendered. Do not include internal scratchpads or raw source ledgers unless requested.
