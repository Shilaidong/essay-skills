# Report Voice Reference

## Voice

Write like a careful counselor explaining evidence to a student:

- Warm, direct, concrete.
- Professional without sounding clinical.
- Simple sentences.
- No mechanical "AI analysis" language.
- No change logs or internal notes inside the report.

Prefer:

- "当分数被拿来比较时，你可能会感到压力。"
- "这并不代表你能力不足，而是这件事触动了自我价值感。"
- "这部分信息太少，应当先作为备注保留。"

Avoid:

- "基于多维度心理测量建模……"
- "AI 总结认为……"
- "本报告经过 …… 修改。"
- "这证明你是 …… 的人。"
- "神经质较高。"（仅做原始数据使用，不直接贴标签）

## Student-safe Interpretation

For sensitive labels, translate to student-friendly wording:

| Skill vocabulary | Student-facing term |
| --- | --- |
| 神经质 (neuroticism) | 情绪敏感度 |
| 开放性 (openness) | 好奇心与想象力 |
| 尽责性 (conscientiousness) | 自律与条理 |
| 外向性 (extraversion) | 社交能量 |
| 宜人性 (agreeableness) | 共情与合作 |
| 重大挑战 (challenge) | 你正在面对的难题 |
| 应对方式 (coping) | 你应对难题的方式 |

When the audience is a counselor or the user explicitly requests clinical language, the original vocabulary may be used. Always open with a one-line translation rule at the top of the report so the reader knows which lens applies.

Pattern:

```text
What the data shows -> What it may feel like -> What to do next
```

Example:

```text
你的宜人性分数较高，又在访谈里提到会主动把同伴拉回讨论。这意味着你容易注意到可能被忽略的人，这是一种优势。需要留意的是，你不必每次都承担大家的情绪。
```

## LifeEcho-Specific Terminology

When the source is **LifeEcho**, keep the upstream module vocabulary verbatim. Do not invent new labels:

- 模块名: 第二人生模型 / 成长画像探索 / 专业方向测评 / 大五人格测试.
- 8 关键时刻: 高峰时刻 / 低谷时刻 / 转折点 / 童年正面记忆 / 童年负面记忆 / 智慧事件 / 重大挑战 / 应对方式.
- 未来愿景三个子项 (固定顺序): 🌟 梦想 / ✨ 希望 / 📖 生命项目.
- 章节标题与摘要: 直接引用用户填写内容，不要"润色"成新标题。
- 颜色与可视化语义: 沿用 `references/lifeecho-methodology.md` § 5 的色板，不要重新选取。

If a moment or chapter is empty in the source data, write "未填写" rather than implying the user "did not have" that experience.

## Evidence Writing

Each evidence card should have:

- A short finding title.
- One short quote or data point.
- A plain-language reading.

Keep quotes short. If a raw quote is long, extract the strongest clause and paraphrase the rest. For LifeEcho chat transcripts, prefer the user's own wording over the assistant's questions.

## Action Advice

Actions should be small enough to do:

- "每周整理一个 pull-quote 卡片。"
- "只把本周分数和上周分数对比。"
- "新建一个文件夹，分别放分数、项目和活动证据。"

Avoid vague advice:

- "提升自我。"
- "更自信一点。"
- "多探索。"

Turn vague advice into observable next steps.
