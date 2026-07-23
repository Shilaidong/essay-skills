# Workflow Reference

> Combines the generic JSON assessment pipeline with the **LifeEcho** specialized branch.
> For upstream LifeEcho facts (field names, color tokens, scoring rules, level thresholds), see `references/lifeecho-methodology.md`.

## 1. Intake

Collect:

- Raw JSON paths.
- Whether the JSON is a **LifeEcho raw-data export** (`*-raw-data.json` with the `meta` / `client` / `interview_modules` / `messages_by_module` shape). If yes, branch to the LifeEcho path below.
- Student-facing vs counselor-facing audience.
- Required deliverables: website, PDF, DOCX, images, source ledger.
- Orientation and size for PDF: A4 portrait, A4 landscape, or 16:9 screen such as 1920 x 1080.
- Forbidden content, such as debug notes, change summaries, clinical labels, or low-quality/skipped data.
- Working language: **中文** is the default for LifeEcho. Switch only when the user asks.

Ask only when the missing answer changes the report. Otherwise proceed with an explicit assumption.

## 2. JSON Audit

Run the audit script first.

For **LifeEcho JSON**:

```bash
python scripts/inspect_assessment_json.py session-raw-data.json --lifeecho --out audit.md
```

For **generic JSON**:

```bash
python scripts/inspect_assessment_json.py input-a.json input-b.json --out audit.md
```

Look for:

- Top-level sessions and timestamps.
- Assessment answers, scales, and raw score fields.
- Repeated or uniform responses.
- Nested JSON stored as strings (LifeEcho `messages[].content` for `role="system"` in the `life-story` module).
- Chat messages and speaker roles.
- **LifeEcho-specific**: chapters (2–7 expected), 8 standard key-moment types (`high_point`, `low_point`, `turning_point`, `childhood_positive`, `childhood_negative`, `wisdom_event`, `challenge`, `coping`), `futureScript` tri-field, Big Five `scores` 0–50 per factor.
- Sparse answers such as `1`, `unknown`, `none`, empty strings, or repeated filler.

Data-quality rule:

- Completed, varied responses may support main interpretation.
- Skipped or uniform-response blocks should not support conclusions.
- Sparse life-story nodes may be listed as incomplete but not over-interpreted.
- A `life-story` module with `< 2` or `> 7` chapters → render with "数据范围外" badge; do not silently drop.
- A Big Five factor with all-same item answers → mark "作答一致性异常，避免引用该维度结论".

## 3. Method Recovery

When a method or product is named:

1. Read the source implementation or primary documentation.
2. Record item count, response scale, reverse-scoring rules, maximum scores, thresholds, and module purpose.
3. Distinguish official method facts from the agent's interpretation.
4. If the method has changed recently or is pulled from a repo/web source, verify the current source.

For **LifeEcho**, the canonical sources are the files listed at the bottom of `lifeecho-methodology.md`. Quick facts to lock down:

- Big Five: 50 IPIP items, 10 per factor, reverse `6 - raw_answer`, range 0–50 per factor, levels < 25 / 25–34 / ≥ 35.
- Life-story chapters: 2–7 chapters, fields `chapter_num` / `title` / `summary` / `start_year` / `end_year`.
- 8 关键时刻: vocabulary in the table in `lifeecho-methodology.md` § 5; same colors as `LifeRiver.tsx`.
- Future script: `dreams` / `hopes` / `life_projects`.
- Chat-based modules use the system prompts in § 6 of `lifeecho-methodology.md`.

Example ledger columns:

```csv
claim,evidence,source,confidence,report_use
大五开放性高,41/50 score,personality_test.scores.openness + IPIP scoring rule,high,personality section
正在筹备 8 大关键时刻关键事实,life-story system message,messages_by_module[life-story][0].content,high,life story section
心理画像访谈仅 4 条消息,user message count,messages_by_module[psychological-profile],high,expand to "数据有限" note
```

## 4. Analysis Structure

Use this default report shape for **LifeEcho**:

1. 封面 / 个人信息 + 数据完整度。
2. 方法与数据说明 (IPIP-50 / LSI-II 来源)。
3. [optional] 临床观察 (`assessment_session.clinical_observations`)。
4. 核心人格画像 (大五人格五维可视化 + level + 单维度解读)。
5. [optional] 互动偏好 + 学习韧性 cards (placeholder copy from upstream; replace or hide).
6. **第二人生模型**:
   - 人生章节 cards (2–7)。
   - 8 关键时刻 cards / grid (颜色用 LifeRiver § 5)。
   - 生命之河 (SVG / stream 颜色 + 高低标记)。
   - 未来愿景 (🌟 梦想 / ✨ 希望 / 📖 生命项目)。
7. 探索记录 — psychological-profile / academic-assessment transcript cards (前 20 条全量, 之后折叠为 "共 N 条对话")。
8. 综合解读 — Big Five + 关键时刻 + 未来剧本 交叉解读。
9. 行动建议 — 小、可观察、可执行。
10. 数据来源与限制 — 指向 <https://github.com/Shilaidong/Life-Echo>, 列出缺失字段。

For **non-LifeEcho** JSON the generic shape stays:

1. Overview and data boundaries.
2. Assessment method and data-quality cards.
3. Core scores with radar/polygon and bars.
4. Trait-by-trait interpretation.
5. Interview evidence cards with quote and plain-language reading.
6. Interest/ability map.
7. Life-story timeline or river (if present).
8. Life-story readings and future script (if present).
9. Synthesis.
10. Action plan.
11. Sources and limitations.

Adapt the shape to the user request, but keep evidence and uncertainty visible.

## 5. Evidence Rules

- Quote only short excerpts (≤ 30 字) and paraphrase the rest.
- Prefer exact student wording for key moments and short chat turns.
- Keep score tables and narrative claims consistent.
- Do not infer diagnosis, family dynamics, trauma, or ability limits beyond the data.
- Use "可能", "倾向于", "在此数据中观察到" for inferences.
- Use direct statements for verified facts: scores, dates, item counts, completed modules.
- For each Big Five dimension, list at least one evidence point (raw item pattern, interview quote, or chapter content). If none exists, soften the claim rather than invent.

## 6. Deliverable Rules

For a website:

- Create a standalone project folder.
- Keep data in a structured file (`data.js`, JSON, or TypeScript object).
- Use deterministic chart code for score visuals.
- Use real or generated illustrations only as visual support.
- Re-use the LifeRiver color tokens from `lifeecho-methodology.md` § 5 when rendering 8 关键时刻 UI.

For PDF:

- Export from the verified page.
- Use screen-like 16:9 PDF when the user asks for computer-view or 1080P.
- Use A4 only when the user asks for printable documents.
- On Linux, rely on `export_landscape_pdf.mjs` to auto-apply `scripts/print-fix.linux.css` when blur/glass/gradient-text artifacts appear in the PDF.
- Render sample pages for QA before final delivery.
