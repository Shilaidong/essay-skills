# Tool-Calling Playbook

## General rule

Use tools to increase accuracy, structure, and visual quality. Do not use tools to create unsupported claims.

## Web/search tools

Use when:

- Information may have changed.
- The exact school/program rule matters.
- The user asks for latest, examples, sources, or citations.
- You are unsure about a term, school, program, or policy.
- The plan affects money, deadlines, legal/visa issues, or high-stakes choices.

Process:

1. Search broad enough to find the official page.
2. Open the official page.
3. Capture the relevant claim, not just the page title.
4. Record date checked.
5. Add the source to the source ledger.
6. In the report, cite or source-note only the facts that depend on research.

Avoid:

- Relying on AI summaries of school policies.
- Using forums as final authority.
- Copying long text from source pages.
- Assuming last year's policy still applies.

## File tools

Use for uploaded:

- Transcripts.
- Score reports.
- Certificates.
- Resumes.
- Essays.
- School lists.
- Spreadsheets.
- Screenshots.
- PDFs.
- Meeting transcripts.

Process:

1. Save original.
2. Extract content using native parsing when possible.
3. Use OCR only if no text layer exists and the content is necessary.
4. Build a structured intake table.
5. Mark uncertain reads.
6. Do not infer beyond the file.

## Python tools

Use for:

- Creating and validating ledgers.
- Cleaning school matrices.
- Date arithmetic.
- Gantt chart images.
- Word document generation.
- Consistency checks.
- Converting structured data into tables.

Recommended output files:

```text
/report.md
/source_ledger.csv
/evidence_ledger.csv
/school_matrix.csv
/timeline.csv
/gantt.png
/final_report.docx
```

## Document-generation tools

Use styles, not one-off formatting.

For Chinese reports:

- East Asian font: 宋体 / SimSun when available.
- Latin font: Times New Roman unless requested otherwise.
- Avoid sharing font files.
- Use restrained headings, callout boxes, and readable tables.
- Use Gantt images, not Mermaid code blocks, inside Word.

QA:

1. Generate the file.
2. Render to PDF or page images if tools allow.
3. Inspect every page.
4. Fix overflow, split tables, missing glyphs, orphan headings, and image quality.
5. Re-render.

## Spreadsheet tools

Use CSV/XLSX for matrices. Keep files machine-readable:

- No merged cells in data files.
- Stable column headers.
- One record per row.
- ISO dates: YYYY-MM-DD.
- Separate current facts from target milestones.

## Connector tools

When using connectors such as Google Drive, Gmail, Calendar, or GitHub:

- Prefer connector tools for connector URLs.
- Do not use public web tools for private connector links.
- Read only the files or threads the user requests.
- Preserve privacy and avoid unnecessary data extraction.

## If a tool is unavailable

Do not pretend it was used. Write:

```text
当前环境未能核验/渲染/读取该项，已标注为待核验。
```
