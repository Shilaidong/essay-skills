---
name: json-assessment-report
description: Generate evidence-grounded, student-facing assessment reports from raw JSON exports. Specialized for LifeEcho (数字孪生心理测评系统) raw-data JSON dumps — handles Big Five (IPIP-50), the LSI-II based "第二人生模型" life-story module (chapters + 8 key moments + future script), and chat-based 成长画像探索 / 专业方向测评 modules. Use when a user provides LifeEcho raw-data JSON, IPIP-50 personality answers, LSI-II structured life-story exports, or asks for an interpretation website/PDF that explains LifeEcho scores, life chapters, and future vision.
---

# JSON Assessment Report (LifeEcho Specialized)

## Overview

Turn raw assessment JSON into a polished report package: evidence audit, student-facing interpretation, data-driven web page, and optional 16:9 landscape PDF that keeps text and images together.

This skill is **LifeEcho-first**. It treats the JSON export from the [LifeEcho](https://github.com/Shilaidong/Life-Echo) raw-data export button (`导出原始数据 JSON`) as the canonical input and recovers the scoring facts (IPIP-50, LSI-II 结构) directly from the upstream source. For non-LifeEcho JSON, the same workflow still applies — see "Non-LifeEcho fallbacks" below.

Use this skill for report production, not for quick one-paragraph summaries.

## When to use

Trigger this skill when:

- The user attaches or references a LifeEcho `*-raw-data.json` (or `*-report.json`) export.
- The user mentions LifeEcho modules: `life-story`, `psychological-profile`, `academic-assessment`, or the Big Five IPIP-50 test.
- The user provides personality answers, life-story chapters, key moments, future-script text, or interview transcripts from a LifeEcho session.
- The user wants the standard LifeEcho report shapes: 生命之河 visualization, 大五人格 score bars, 成长画像 / 专业方向 module summaries.

Do not trigger this skill for unrelated assessments (MBTI, DISC, 16PF unrelated). The skill is generic enough to handle other formats, but the LifeEcho tooling (scoring thresholds, schema, voice rules) is its first-class case.

## Workflow

1. **Confirm the deliverable.**
   - Identify audience, language, output folder, final format, privacy limits, and whether the PDF should be A4/print or 16:9 landscape screen style.
   - If the user gives a concrete folder, put the project there; otherwise create a dedicated output folder named after the client or session and avoid scattering files.
   - Default working language: **中文 (zh-CN)** for LifeEcho (the upstream app is Chinese-only). Switch to English only when the user explicitly asks.

2. **Inspect the JSON before interpreting it.**
   - Run `scripts/inspect_assessment_json.py <json...>` with the `--lifeecho` flag to map structure, long text fields, nested JSON strings inside `messages`, and detect LifeEcho-shaped payloads.
   - For non-LifeEcho JSON, drop the flag and use the generic audit.
   - Treat skipped, placeholder, uniform, empty, or low-information data as data-quality notes only. Do not use them as the main interpretation.
   - For LifeEcho `life-story` modules, the structured data (`chapters`, `keyMoments`, `futureScript`) is stored as a `role: "system"` message stringified JSON inside `messages` — the inspector auto-flattens that field.

3. **Recover the scoring and evidence basis.**
   - Always verify the assessment method against the upstream source before writing claims. The LifeEcho references live in `references/lifeecho-methodology.md` and point back to [github.com/Shilaidong/Life-Echo](https://github.com/Shilaidong/Life-Echo).
   - Separate scoring facts from interpretation. Example for Big Five: item count (50), reverse-scoring rule (`6 - raw_answer`), 0–50 range, the <25 / 25–34 / ≥35 thresholds are scoring facts; trait meaning is interpretation.
   - For LSI-II modules: chapter count bounds (2–7), moment-type vocabulary (8 standard types), future-script tri-field (`dreams` / `hopes` / `life_projects`) are scoring facts.
   - Keep a compact evidence ledger: data point, source path/message, confidence, and how it supports the report.

4. **Build the analysis model.**
   - Prefer this chain for LifeEcho reports: `data quality -> Big Five scores -> interview evidence (心理画像/学业方向) -> life-story (chapters + 8 key moments) -> future script -> synthesis -> 行动建议`.
   - Preserve direct quotes from messages, but use short excerpts (≤ 30 字). Paraphrase the rest.
   - When the user only has the Big Five without LSI-II: omit the life-story / future-script sections entirely and focus on the personality report.
   - When the user only has LSI-II without Big Five: keep the chapter/moment narrative and personality-interview evidence only.
   - Convert sensitive constructs into student-safe labels. Example for Big Five: use "情绪敏感度 (emotional sensitivity)" instead of "神经质", unless the audience is the counselor.

5. **Write for the student.**
   - Use clear, warm, concrete language. Avoid diagnosis, horoscope-style labels, exaggerated praise, and "AI/meta" wording.
   - Every important claim needs visible support from a score, answer pattern, quote, or life-story node.
   - Use the **八类关键时刻词汇** verbatim when summarizing LSI-II: 高峰时刻 / 低谷时刻 / 转折点 / 童年正面记忆 / 童年负面记忆 / 智慧事件 / 重大挑战 / 应对方式. Do not invent new moment-type names.
   - Work strictly from available data. Do not over-read blanks, and never fabricate content for empty sections.
   - See `references/report-voice.md`.

6. **Create the report interface.**
   - Build an actual usable report, not a landing page.
   - Required visuals for a full LifeEcho report:
     - **大五人格五维条形 / 雷达图** with /50 标尺 + level tag (低 / 中等 / 高).
     - **8 个关键时刻卡片网格** in the canonical color vocabulary (高峰 绿, 低谷 红, 转折 蓝灰, 童年正面 绿, 童年负面 红, 智慧 翠绿, 挑战 紫, 应对 青). Colors come from upstream `LifeRiver.tsx`.
     - **生命之河 (Life River)** SVG using the 8 moment years along an x-axis with chapter color bands (Green = positive / Blue = neutral / Red = difficult chapters).
     - **未来愿景区块** with three sub-blocks: 🌟 梦想 / ✨ 希望 / 📖 生命项目.
     - Optional **心理画像 / 专业方向** module summary cards with quote excerpts.
   - Include text equivalents for every chart: score bars, cards, legends, and captions.
   - Use data-driven charts for measurements. Do not use generated images as evidence.
   - See `references/frontend-and-pdf.md`.

7. **Export and verify.**
   - For landscape screen PDFs, use a 16:9 page such as 1920 x 1080 CSS pixels.
   - Keep text and images in one PDF; do not deliver a folder of screenshots unless the user asks.
   - Render or preview representative pages. Check for clipping, orphaned headings, blank pages, chart overlap, broken images, and forbidden/meta wording.
   - Use `scripts/export_landscape_pdf.mjs` when a webpage is ready and Playwright is available.

## Non-LifeEcho fallbacks

If the JSON is not LifeEcho-shaped, fall back to the generic JSON assessment pipeline:

- IPIP-50 detected via exact 50-item Likert answers → apply scoring (default range 1–5, reverse half).
- Generic Likert blocks → treat as trait scores and label with the field key.
- Chat transcripts → parse speaker turns, extract representative quotes, do not assume LSI-II structure.

Always show the audit script output before committing to a structure so the data shape is transparent.

## File Map

- `scripts/inspect_assessment_json.py`: structural audit; with `--lifeecho`, also annotates LifeEcho-shaped payloads (chapters, key moments, big-five scores).
- `scripts/export_landscape_pdf.mjs`: export an HTML page or local URL to a 16:9 PDF. On Linux, auto-injects `scripts/print-fix.linux.css` to avoid headless Chromium PDF artifacts (gray blocks behind blur/glass/gradient text).
- `scripts/print-fix.linux.css`: PDF-only CSS overrides for Linux headless Chromium; inject via `--css` or the exporter's Linux auto-fix, never via `<link>` in HTML.
- `references/lifeecho-methodology.md`: LifeEcho data model, scoring rules, module semantics, color vocabulary, and quality gates (single source of truth for LifeEcho-specific knowledge).
- `references/workflow.md`: detailed production process and data-quality rules.
- `references/report-voice.md`: student-facing writing standards.
- `references/frontend-and-pdf.md`: web, chart, and PDF QA rules.

## Quality Gates

Before delivery:

- The final report contains no notes about what the agent changed.
- Skipped or low-quality data are not treated as valid conclusions.
- Charts are backed by numeric data and have readable labels.
- Interview and life-story claims connect to specific evidence (chapter number, moment type, message timestamp, or score).
- Big Five scoring uses the LSI-II / IPIP-50 reverse rule (`6 - raw_answer`); unverified scoring sources are flagged.
- 8 关键时刻 用其官方中文标签，不用自创别名。
- The page has no obvious overflow on desktop and mobile if a website is delivered.
- The PDF has the requested orientation and page size.
- Text remains selectable in the PDF unless the user explicitly wants image-only slides.
- Images are embedded in the same PDF and not split into separate deliverables.
- Console errors, missing assets, and broken links are resolved or disclosed.

## Minimal Commands

```bash
# LifeEcho raw-data JSON audit
python scripts/inspect_assessment_json.py session-raw-data.json --lifeecho --out audit.md

# Generic audit (any JSON)
python scripts/inspect_assessment_json.py input-a.json input-b.json --out audit.md

# Export landscape PDF (Linux auto-applies print-fix.linux.css)
node scripts/export_landscape_pdf.mjs --input ./index.html --output report-1080p.pdf --screen-report

# Optional: pass the Linux fix manually on any OS
node scripts/export_landscape_pdf.mjs --input ./index.html --output report-1080p.pdf --screen-report --css scripts/print-fix.linux.css
```

## Source of truth

All LifeEcho-specific facts in this skill are derived from:

- Repository: <https://github.com/Shilaidong/Life-Echo>
- Key files:
  - `src/app/clients/[id]/session/[sessionId]/report/page.tsx` (导出原始数据 JSON + Markdown)
  - `src/app/clients/[id]/session/[sessionId]/module/[moduleId]/page.tsx` (life-story / psychological-profile / academic-assessment)
  - `src/app/clients/[id]/session/[sessionId]/test/page.tsx` (50-item IPIP Big Five)
  - `src/components/LifeRiver.tsx` (moment type color vocabulary, river layout)
  - `v2.0-PLAN.md` (LSI-II 7-part structure, 8 关键时刻 definition)

Before quoting or scoring rules, cross-check against the current source in case the upstream schema has moved.

---

## Big Five (IPIP-50) 原题与理论参考

> 以下内容从 LifeEcho 仓库 v2.0 分支的 `src/app/clients/[id]/session/[sessionId]/test/page.tsx` 提取，为报告中大五人格部分提供题项和计分依据。

### 五因子简述

| 因子 | IPIP 英文名 | 中文名 | 高分含义 | 低分含义 |
|---|---|---|---|---|
| `openness` | Openness to Experience | 开放性 | 想象力丰富、好奇、审美敏感 | 务实、传统、偏爱常规 |
| `conscientiousness` | Conscientiousness | 尽责性 | 有条理、勤奋、可靠 | 随性、易拖延、不够细心 |
| `extraversion` | Extraversion | 外向性 | 善于社交、精力充沛、活跃 | 内向、安静、偏好独处 |
| `agreeableness` | Agreeableness | 宜人性 | 信任他人、乐于助人、有同情心 | 怀疑、竞争性强、不轻易信任 |
| `neuroticism` | Neuroticism | 神经质 (情绪稳定性) | 容易焦虑、情绪波动大、敏感 | 情绪稳定、冷静、不易担忧 |

> 报告中建议将 `neuroticism` 转化为正面表述（如"情绪敏感度"），详见 Workflow 第 4 步。

### 50 道原题列表

每道题采用 1–5 Likert 量表：1=强烈不同意、2=不同意、3=中立、4=同意、5=强烈同意。

| # | 因子 | 题目 | 反向 |
|---|---|---|---|
| 1 | openness | 我有丰富的想象力 | 否 |
| 2 | openness | 我对抽象概念很感兴趣 | 否 |
| 3 | openness | 我有创造性的头脑 | 否 |
| 4 | openness | 我欣赏艺术和音乐 | 否 |
| 5 | openness | 我好奇心强 | 否 |
| 6 | openness | 比起变化，我更喜欢按部就班的生活 | 是 |
| 7 | openness | 比起抽象概念，我更偏好实际具体的想法 | 是 |
| 8 | openness | 我对新事物不太感兴趣 | 是 |
| 9 | openness | 我不喜欢艺术活动 | 是 |
| 10 | openness | 我思想保守 | 是 |
| 11 | conscientiousness | 我做事有条理 | 否 |
| 12 | conscientiousness | 我信守承诺 | 否 |
| 13 | conscientiousness | 我工作勤奋 | 否 |
| 14 | conscientiousness | 我按时完成任务 | 否 |
| 15 | conscientiousness | 我注重细节 | 否 |
| 16 | conscientiousness | 我做事有些懒散 | 是 |
| 17 | conscientiousness | 我经常迟到 | 是 |
| 18 | conscientiousness | 我做事不够细心 | 是 |
| 19 | conscientiousness | 我容易拖延 | 是 |
| 20 | conscientiousness | 我对目标不够坚持 | 是 |
| 21 | extraversion | 我喜欢与人交谈 | 否 |
| 22 | extraversion | 我在社交场合很活跃 | 否 |
| 23 | extraversion | 我喜欢成为关注的焦点 | 否 |
| 24 | extraversion | 我有很多朋友 | 否 |
| 25 | extraversion | 我精力充沛 | 否 |
| 26 | extraversion | 我性格内向 | 是 |
| 27 | extraversion | 我不喜欢社交活动 | 是 |
| 28 | extraversion | 我喜欢独处 | 是 |
| 29 | extraversion | 我在人群中感到不自在 | 是 |
| 30 | extraversion | 我不擅长发起对话 | 是 |
| 31 | agreeableness | 我相信他人是善意的 | 否 |
| 32 | agreeableness | 我愿意帮助需要帮助的人 | 否 |
| 33 | agreeableness | 我对他人有同情心 | 否 |
| 34 | agreeableness | 我信任我的朋友 | 否 |
| 35 | agreeableness | 我乐于助人 | 否 |
| 36 | agreeableness | 我对他人的意图持怀疑态度 | 是 |
| 37 | agreeableness | 我有时不太体贴 | 是 |
| 38 | agreeableness | 我不太关心他人感受 | 是 |
| 39 | agreeableness | 我对人不够友好 | 是 |
| 40 | agreeableness | 我不太信任别人 | 是 |
| 41 | neuroticism | 我容易焦虑 | 否 |
| 42 | neuroticism | 我容易担心 | 否 |
| 43 | neuroticism | 我情绪波动大 | 否 |
| 44 | neuroticism | 我容易感到沮丧 | 否 |
| 45 | neuroticism | 我对压力敏感 | 否 |
| 46 | neuroticism | 我情绪稳定 | 是 |
| 47 | neuroticism | 我很少感到沮丧 | 是 |
| 48 | neuroticism | 我面对压力很冷静 | 是 |
| 49 | neuroticism | 我不容易担心 | 是 |
| 50 | neuroticism | 我很少焦虑 | 是 |

### 计分规则

- **评分范围**：每题 1–5 分
- **正向题**：直接取原始分值
- **反向题**：`得分 = 6 - 原始分值`（1↔5, 2↔4, 3 不变）
- **各维度总分范围**：0–50（每题满分 5 × 10 题）
- **层面划分**：

| 得分区间 | 层面标签 |
|---|---|
| < 25 | 低 |
| 25–34 | 中等 |
| ≥ 35 | 高 |

### 数据来源说明

本参考数据直接取自 LifeEcho 前端代码库 v2.0 分支：

- **题目与计分**：`src/app/clients/[id]/session/[sessionId]/test/page.tsx`（`bigFiveQuestions` 数组 + `submitTest` 函数中的计分逻辑）
- **因子中文名**：`factorNames` 映射表
- **理论背景**：基于 Goldberg (1990) 的 IPIP (International Personality Item Pool) Big-Five Factor Markers
