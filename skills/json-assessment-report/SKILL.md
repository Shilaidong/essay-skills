---
name: json-assessment-report
description: Generate evidence-grounded, student-facing assessment reports from raw JSON exports. Use when a user provides assessment JSON, survey JSON, interview transcripts, LifeEcho-style exports, learning/personality data, or asks Codex to create a polished interpretation website/PDF with charts, narrative analysis, data-quality checks, and student-safe language.
---

# JSON Assessment Report

## Overview

Turn raw assessment JSON into a polished report package: evidence audit, student-facing interpretation, data-driven web page, and optional 16:9 landscape PDF that keeps text and images together.

Use this skill for report production, not for quick one-paragraph summaries.

## Workflow

1. **Confirm the deliverable.**
   - Identify audience, language, output folder, final format, privacy limits, and whether the PDF should be A4/print or 16:9 landscape screen style.
   - If the user gives a concrete folder, put the project there; otherwise create a dedicated output folder and avoid scattering files.

2. **Inspect the JSON before interpreting it.**
   - Run `scripts/inspect_assessment_json.py <json...>` to map structure, long text fields, nested JSON strings, likely Likert answer blocks, and uniform-response patterns.
   - Treat skipped, placeholder, uniform, empty, or low-information data as data-quality notes only. Do not use them as the main interpretation.
   - Parse embedded JSON strings inside chat messages or content fields when present.

3. **Recover the scoring and evidence basis.**
   - If the report references a specific product, repo, paper, or assessment method, inspect the primary source before writing claims.
   - Separate scoring facts from interpretation. Example: item count, reverse scoring, score range, and thresholds are scoring facts; personality meaning is interpretation.
   - Keep a compact evidence ledger: data point, source path/message, confidence, and how it supports the report.

4. **Build the analysis model.**
   - Prefer this chain: `data quality -> scores -> interview evidence -> life story/future script -> synthesis -> actions`.
   - Preserve direct quotes, but use short excerpts. Paraphrase the rest.
   - Convert sensitive constructs into student-safe labels. Example: use "emotional sensitivity" instead of clinical-sounding labels when appropriate.

5. **Write for the student.**
   - Use clear, warm, concrete language. Avoid diagnosis, horoscope-style labels, exaggerated praise, and "AI/meta" wording.
   - Every important claim needs visible support from a score, answer pattern, quote, or life-story node.
   - If a section is incomplete, say what can and cannot be inferred. Do not over-read blanks.
   - See `references/report-voice.md`.

6. **Create the report interface.**
   - Build an actual usable report, not a landing page.
   - Include text equivalents for charts: score bars, cards, legends, and captions.
   - Use data-driven charts for measurements. Do not use generated images as evidence.
   - If illustration is requested, use it as a supporting visual, not as proof.
   - See `references/frontend-and-pdf.md`.

7. **Export and verify.**
   - For landscape screen PDFs, use a 16:9 page such as 1920 x 1080 CSS pixels.
   - Keep text and images in one PDF; do not deliver a folder of screenshots unless the user asks.
   - Render or preview representative pages. Check for clipping, orphaned headings, blank pages, chart overlap, broken images, and forbidden/meta wording.
   - Use `scripts/export_landscape_pdf.mjs` when a webpage is ready and Playwright is available.

## File Map

- `scripts/inspect_assessment_json.py`: quick structural audit for raw JSON exports.
- `scripts/export_landscape_pdf.mjs`: export an HTML page or local URL to a 16:9 PDF.
- `references/workflow.md`: detailed production process and data-quality rules.
- `references/report-voice.md`: student-facing writing standards.
- `references/frontend-and-pdf.md`: web, chart, and PDF QA rules.

## Quality Gates

Before delivery:

- The final report contains no notes about what the agent changed.
- Skipped or low-quality data are not treated as valid conclusions.
- Charts are backed by numeric data and have readable labels.
- Interview and life-story claims connect to specific evidence.
- The page has no obvious overflow on desktop and mobile if a website is delivered.
- The PDF has the requested orientation and page size.
- Text remains selectable in the PDF unless the user explicitly wants image-only slides.
- Images are embedded in the same PDF and not split into separate deliverables.
- Console errors, missing assets, and broken links are resolved or disclosed.

## Minimal Commands

```bash
python scripts/inspect_assessment_json.py raw-1.json raw-2.json --out audit.md
node scripts/export_landscape_pdf.mjs --input ./index.html --output report-1080p.pdf --screen-report
```
