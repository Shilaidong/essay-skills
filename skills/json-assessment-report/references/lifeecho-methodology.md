# LifeEcho Methodology Reference

> Single source of truth for LifeEcho-specific facts used by the `json-assessment-report` skill.
> All structures and rules below are derived from <https://github.com/Shilaidong/Life-Echo>.
> When the upstream repo changes, update this file first, then propagate to SKILL.md.

## 1. What is LifeEcho?

**LifeEcho 数字孪生心理测评系统** — a digital-twin psychological assessment platform that uses AI to capture and preserve a person's life story, producing a "digital twin" archive. Built with Next.js + Supabase + Tailwind by 引力坊教育科技有限公司.

Tagline: **"用 AI 留存人生故事，让记忆永恒传承"** / *"一面不仅照见容貌，更映照灵魂旅程的镜子"*.

Live demo: <https://life-echo.vercel.app>.

## 2. Theoretical Foundation

LifeEcho's assessment model is grounded in three well-established frameworks:

| Framework | Purpose | Source |
| --- | --- | --- |
| **LSI-II** (Life Story Interview, 2nd edition) | Structured 7-part interview protocol developed at Stanford; used to elicit chapter structure, key scenes, future script | McAdams, 2008 |
| **Big Five / IPIP-50** | 50-item International Personality Item Pool questionnaire, scored 1–5 with reverse items | IPIP-NEO-50, Goldberg |
| **Life River Visualization** | Chronological timeline of key scenes overlaid on chapter bands | LifeEcho in-house (`LifeRiver.tsx`) |

Additional in-house ingredients:

- 8 standard key-moment types (a subset / adaptation of LSI-II's "key scenes").
- "Future Script" tri-field: dreams / hopes / life-projects.
- Biographical codes (planned v2.0): entity extraction + redemption/contamination labeling.
- AI-driven summarization via the `/api/chat` route (system prompts per module).

## 3. Assessment Modules

Every session carries one client and one of each module type. The user-facing module names in Chinese are official.

| `module_type` (DB) | Display name | UI mode | Storage |
| --- | --- | --- | --- |
| `life-story` | 第二人生模型 | 4-step form (chapters → 8 moments → future script → done) | `messages` table — one `role: "system"` message stringified JSON containing `chapters`, `keyMoments`, `futureScript`, `completedStep` |
| `psychological-profile` | 成长画像探索 | Open chat with LSI-II system prompt (emotions / cognition / actions) | `messages` table — alternating `user` / `assistant` rows |
| `academic-assessment` | 专业方向测评 | Open chat with academic-counselor system prompt | `messages` table — alternating `user` / `assistant` rows |
| `personality` (Big Five test) | 大五人格测试 | 50-item Likert form (1–5 keys) | `personality_tests` table — `answers` (record by item id) + `scores` (record by factor) |

## 4. JSON Shape (raw export)

The "导出原始数据 JSON" button on the report page produces:

```jsonc
{
  "meta": {
    "exported_at": "ISO-8601 timestamp",
    "source": "supabase",
    "client_id": "uuid",
    "session_id": "uuid"
  },
  "client": {
    "id": "uuid",
    "user_id": "uuid",
    "name": "string",
    "age": 0,
    "gender": "string",
    "notes": "string (临床笔记)"
  },
  "assessment_session": {
    "id": "uuid",
    "client_id": "uuid",
    "status": "in_progress | completed",
    "clinical_observations": "string",
    "created_at": "ISO-8601 timestamp",
    "completed_at": "ISO-8601 timestamp or null"
  },
  "personality_test": {
    "id": "uuid",
    "session_id": "uuid",
    "answers": { "1": 1, "2": 5, "...": 0 },
    "scores": {
      "openness": 0,
      "conscientiousness": 0,
      "extraversion": 0,
      "agreeableness": 0,
      "neuroticism": 0
    }
  } | null,
  "interview_modules": [
    { "id": "uuid", "session_id": "uuid", "module_type": "life-story", "status": "completed", "completed_at": "..." },
    { "id": "uuid", "module_type": "psychological-profile", "status": "completed", "completed_at": "..." }
  ],
  "messages": [ /* flat list across modules */ ],
  "messages_by_module": { /* grouped by module id */ }
}
```

### 4.1 Big Five `scores` field

Each factor is the sum of 10 IPIP items, each scored 1–5, with reverse items scored as `6 - raw`. Range: **0–50 per factor**, total possible across factors 250.

| Factor key | Chinese label | Items |
| --- | --- | --- |
| `openness` | 开放性 | 1–10 |
| `conscientiousness` | 尽责性 | 11–20 |
| `extraversion` | 外向性 | 21–30 |
| `agreeableness` | 宜人性 | 31–40 |
| `neuroticism` | 神经质 | 41–50 |

Level thresholds (canonical to LifeEcho report page):

- `< 25` → 低 (low)
- `25 – 34` → 中等 (medium)
- `>= 35` → 高 (high)

### 4.2 `answers` field for IPIP-50

```jsonc
{
  "1": 1,   // raw answer for item id 1 — openness, non-reverse
  "6": 4,   // raw answer for item id 6 — openness, REVERSE → scored as 6 - 4 = 2
  // ...
  "50": 5   // item id 50 — neuroticism, REVERSE → scored as 6 - 5 = 1
}
```

Reverse items use `6 - raw_answer` per `test/page.tsx`. Reverse-item set:

- openness: 6, 7, 8, 9, 10
- conscientiousness: 16, 17, 18, 19, 20
- extraversion: 26, 27, 28, 29, 30
- agreeableness: 36, 37, 38, 39, 40
- neuroticism: 46, 47, 48, 49, 50

Data-quality flags:

- `answers` key missing → Big Five test was never taken.
- Every answer is the same value → uniform response, do not score.
- Answer outside 1–5 → invalid, exclude before scoring.
- If `answers` exists but `scores` does not, recompute and label as "代理重算".

### 4.3 Life-story `system` message payload

The `life-story` module persists its structured form as a single `role: "system"` message in the `messages` table:

```jsonc
{
  "chapters": [
    {
      "chapter_num": 1,
      "title": "string",
      "summary": "string",
      "start_year": "string (may be empty)",
      "end_year": "string (may be empty)"
    }
  ],
  "keyMoments": {
    "high_point":              { "moment_type": "high_point",              "title": "...", "description": "...", "year": "...", "emotions": "...", "lessons_learned": "..." },
    "low_point":               { "moment_type": "low_point",               "...": "..." },
    "turning_point":           { "moment_type": "turning_point",           "...": "..." },
    "childhood_positive":      { "moment_type": "childhood_positive",      "...": "..." },
    "childhood_negative":      { "moment_type": "childhood_negative",      "...": "..." },
    "wisdom_event":            { "moment_type": "wisdom_event",            "...": "..." },
    "challenge":               { "moment_type": "challenge",               "...": "..." },
    "coping":                  { "moment_type": "coping",                  "...": "..." }
  },
  "futureScript": {
    "dreams": "string",
    "hopes": "string",
    "life_projects": "string"
  },
  "completedStep": 3
}
```

Constraints from the upstream form:

- **2–7 chapters** — fewer or more is a data-quality flag.
- **Exactly 8 key moments** by canonical type (above). Empty `title` or `description` means the user did not fill that card; render the card but mark it "未填写".
- **3 fields** in `futureScript`: `dreams`, `hopes`, `life_projects`. Any combination of empty / filled is acceptable.

### 4.4 Chat-based module messages

For `psychological-profile` and `academic-assessment`, `messages` is a chat history:

```jsonc
{
  "module_type": "psychological-profile",
  "messages": [
    { "role": "assistant", "content": "感谢您完成大五人格测试……", "created_at": "..." },
    { "role": "user",      "content": "我叫……",                       "created_at": "..." },
    ...
  ]
}
```

Speaker labels in reports: 学生 (user) / 系统 (assistant).

Length constraint: show the first 20 messages verbatim (per upstream report page), then collapse the remainder with "... 共 N 条对话".

## 5. Color and Visualization Vocabulary (LifeRiver)

The canonical color vocabulary is fixed in `src/components/LifeRiver.tsx`. Re-use these exactly when reproducing the river or rendering moment cards:

| `moment_type` | Chinese label | Color token | Hex |
| --- | --- | --- | --- |
| `high_point` | 高峰时刻 | tertiary | `#3f6353` |
| `low_point` | 低谷时刻 | error | `#ba1a1a` |
| `turning_point` | 转折点 | secondary | `#515f74` |
| `childhood_positive` | 童年正面记忆 | tertiary-container | `#577c6b` |
| `childhood_negative` | 童年负面记忆 | error-container | `#ba1a1a` |
| `wisdom_event` | 智慧事件 | primary | `#00685f` |
| `challenge` | 重大挑战 | purple-500 | `#8b5cf6` |
| `coping` | 应对方式 | cyan-600 | `#0891b2` |

River stream gradient (left → right): `#00685f → #008378 → #89f5e7 → #c3ecd7`.

The chapter color band is read from each chapter's overall emotional tone:

- Green band = overall positive chapter.
- Blue band = neutral / turning chapter.
- Red band = overall difficult chapter.

The moment circle icons and the colors of the moments on the river must match this vocabulary. Do not introduce new colors.

## 6. System Prompts (semantic context)

The LifeEcho app uses these system prompts. Understanding them helps interpret why the user wrote something:

**心理画像 (psychological-profile):**
> 你是 LifeEcho AI 辅助访谈助手，基于斯坦福大学 LSI-II 人生故事访谈协议设计，专门进行心理画像访谈。关键模块：情感模块（关注情绪体验）、思想模块（了解价值观）、行动模块（记录行为模式）。请用中文进行访谈，一次只问一个核心问题，保持温暖共情的语气。

**学业方向 (academic-assessment):**
> 你是 LifeEcho AI 学业规划顾问，专门帮助学生进行学业和职业规划评估。保持鼓励、支持的语气，帮助学生发现潜力。请用中文进行对话，每次回复后问一个问题引导对话继续。

If a quote in the transcript suggests a different framework entirely (e.g., MBTI), the source is not LifeEcho — flag it.

## 7. Report Composition (canonical)

For a complete LifeEcho report, cover these sections in order. Sections in brackets are optional, depending on which modules are present.

1. 封面 / 个人概述 (client name, age, gender, session id, exported_at).
2. 数据质量与方法说明 (数据完整度模块清单, Big Five scoring rule, LSI-II 来源).
3. 核心人格画像 — [optional] 临床观察 (`clinical_observations`).
4. 大五人格五维条形/雷达图 + level label + 单维度解读.
5. [optional] 互动偏好 / 学习韧性 cards (upstream supplies placeholder copy for these; replace or hide if data is missing).
6. 第二人生模型:
   - 人生章节 (cards, 2–7 chapters).
   - 8 关键时刻 (cards or grid).
   - 生命之河 (SVG timeline).
   - 未来愿景 (🌟 梦想 / ✨ 希望 / 📖 生命项目).
7. 探索记录 — psychological-profile / academic-assessment transcripts (first 20 messages verbatim, then collapse).
8. 综合解读 — cross-link Big Five + key moments + future script.
9. 行动建议 — concrete, observable, small steps.
10. 数据来源与限制 — point to upstream repo, list missing fields.

If only one of (Big Five, life-story, chat modules) is present, skip the others gracefully and note which data was not collected.

## 8. Quality Gates (LifeEcho-specific)

- Big Five scoring uses the IPIP-50 reverse rule; recalculated scores must match LifeEcho's `scores` field within ±1 per factor. Mismatches > 1 are flagged.
- Each Big Five dimension must show /50 标尺 + level tag (低 / 中等 / 高). Never show raw 1–5 averages for the total factor.
- Chapter count must be in [2, 7]. Chapters outside this range render with a "数据范围外" badge.
- Each of the 8 moment types has a fixed Chinese label and color. Do not invent or substitute.
- Future script uses exactly the three sub-blocks (梦想 / 希望 / 生命项目) in that order.
- Direct quotes from chat messages are limited to ~30 字. Long messages get paraphrased + a one-line excerpt.
- Never claim the AI "diagnosed" anything. Keep language as observation ("可观察到 / 倾向于 / 在此数据中").
- All numeric claims about years, scores, item counts must trace back to a JSON path. If uncertain, qualify.
- The report must not mention internal agent changes, the agent itself, or "fixed/updated/changed".

## 9. Upstream Change Watchpoints

Re-derive facts from these files whenever upstream changes:

- `src/app/clients/[id]/session/[sessionId]/report/page.tsx` — export shape and level thresholds.
- `src/app/clients/[id]/session/[sessionId]/module/[moduleId]/page.tsx` — life-story form (chapter/moment/future-script fields).
- `src/app/clients/[id]/session/[sessionId]/test/page.tsx` — IPIP-50 questions + reverse items + scoring formula.
- `src/components/LifeRiver.tsx` — moment color vocabulary.
- `src/app/api/chat/route.ts` — system prompts.
- `v2.0-PLAN.md` — 8 moment definitions + LSI-II 7 parts.

If any of these files changes the field name, threshold, or color, update this reference first.
