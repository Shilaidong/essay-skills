# Workflow Reference

## 1. Intake

Collect:

- Raw JSON paths.
- Product or assessment source, such as a GitHub repo, official docs, or paper.
- Student-facing vs counselor-facing audience.
- Required deliverables: website, PDF, DOCX, images, source ledger.
- Orientation and size for PDF: A4 portrait, A4 landscape, or 16:9 screen such as 1920 x 1080.
- Forbidden content, such as debug notes, change summaries, clinical labels, or low-quality/skipped data.

Ask only when the missing answer changes the report. Otherwise proceed with an explicit assumption.

## 2. JSON Audit

Run the audit script first:

```bash
python scripts/inspect_assessment_json.py input-a.json input-b.json --out audit.md
```

Look for:

- Top-level sessions and timestamps.
- Assessment answers, scales, and raw score fields.
- Repeated or uniform responses.
- Nested JSON stored as strings.
- Chat messages and speaker roles.
- Life-story structures: chapters, key moments, future script, projects.
- Sparse answers such as `1`, `unknown`, `none`, empty strings, or repeated filler.

Data-quality rule:

- Completed, varied responses may support main interpretation.
- Skipped or uniform-response blocks should not support conclusions.
- Sparse life-story nodes may be listed as incomplete but not over-interpreted.

## 3. Method Recovery

When a method or product is named:

1. Read the source implementation or primary documentation.
2. Record item count, response scale, reverse-scoring rules, maximum scores, thresholds, and module purpose.
3. Distinguish official method facts from the agent's interpretation.
4. If the method has changed recently or is pulled from a repo/web source, verify the current source.

Example ledger columns:

```csv
claim,evidence,source,confidence,report_use
Big Five openness is high,41/50 score,raw JSON + scoring source,high,personality section
Life-story future project mentions IELTS,"life_projects field",raw JSON,high,life story section
Second response block was skipped,user instruction,user message,high,exclude from analysis
```

## 4. Analysis Structure

Use this default report shape:

1. Overview and data boundaries.
2. Assessment method and data-quality cards.
3. Core scores with radar/polygon and bars.
4. Trait-by-trait interpretation.
5. Interview evidence cards with quote and plain-language reading.
6. Interest/ability map.
7. Life-story timeline or river.
8. Life-story readings and future script.
9. Synthesis.
10. Action plan.
11. Sources and limitations.

Adapt the shape to the user request, but keep evidence and uncertainty visible.

## 5. Evidence Rules

- Quote only short excerpts and paraphrase the rest.
- Prefer exact student wording for key moments.
- Keep score tables and narrative claims consistent.
- Do not infer diagnosis, family dynamics, trauma, or ability limits beyond the data.
- Use "may", "suggests", or "in this data" for inferences.
- Use direct statements for verified facts: scores, dates, item counts, completed modules.

## 6. Deliverable Rules

For a website:

- Create a standalone project folder.
- Keep data in a structured file (`data.js`, JSON, or TypeScript object).
- Use deterministic chart code for score visuals.
- Use real or generated illustrations only as visual support.

For PDF:

- Export from the verified page.
- Use screen-like 16:9 PDF when the user asks for computer-view or 1080P.
- Use A4 only when the user asks for printable documents.
- Render sample pages for QA before final delivery.
