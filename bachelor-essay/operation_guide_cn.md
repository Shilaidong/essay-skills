# Top 20 College Essay Creative Offense Skill 操作指南
## V3：执行轻量化 + SMID 结构可行性验证

V3 是在 V2 基础上的一次“实操减重”。V2 已经解决了创造力哲学问题：从防御性写作升级成主动创意发现。V3 主要解决执行层问题：第一轮输出太重、SMID 与 Angle Storm 有循环依赖、Risk Ladder 使用时机不清楚、Final Self-Audit 没有优先级。

V3 的核心变化：

```text
Quick Dossier 默认模式
+ SMID 结构可行性验证
+ Awards-Removed 强制过滤
+ Risk Ladder 明确触发点
+ 红黄绿分层自检
```

---

## 1. 三个文件分别是什么

压缩包里有三个文件：

```text
skill.md
packet_prompt_en.md
operation_guide_cn.md
```

### 1.1 `skill.md`

长期能力层。放在 Agent 的 skill 文件夹、system prompt 或 developer prompt 里。

它定义 Agent 的底层写作方法：

- creative offense；
- Single Most Irreplaceable Detail；
- SMID Structural Feasibility Gate；
- Quick Dossier / Full Dossier 双模式；
- Voice Construction；
- China-Context Differentiation；
- Formal Play Decision Matrix；
- Creative Risk Ladder；
- tiered final audit。

### 1.2 `packet_prompt_en.md`

每个学生项目开始时复制使用的英文 prompt。

它告诉 Agent：

- 不让学生重新填表；
- 直接读取素材表、沟通文本、成绩单、活动列表、旧稿；
- 默认只输出 Quick Dossier；
- 先找 SMID，再验证它能不能写，再给三个角度；
- 你确认方向后再进入 Draft 1 → Line Edit → Draft 2 → Self-Audit。

### 1.3 `operation_guide_cn.md`

给你或顾问团队看的中文操作指南。

重点是判断标准，不只是复制粘贴方法。

---

## 2. 最推荐的使用方式

### Step 1：先加载 skill

把 `skill.md` 放进 Agent 的 skill / system / developer 层。

### Step 2：每个学生项目复制英文 prompt

打开 `packet_prompt_en.md`，复制：

```text
# COPY-PASTE PROMPT STARTS HERE
```

到：

```text
# COPY-PASTE PROMPT ENDS HERE
```

然后在 `Student Packet` 下面粘贴学生资料。

### Step 3：第一轮默认用 Quick Dossier

不要一上来让 Agent 输出完整大报告。默认让它输出：

```text
Quick Source Snapshot
SMID Candidates with Structural Feasibility
Selected SMID
Three Angles
Recommended Direction and Blueprint
Verification Needs
```

这一步的目标不是写正文，而是选方向。

---

## 3. Quick Dossier 怎么判断好坏

第一轮你只看五件事。

### 3.1 SMID 是否真的不可替代

问：

```text
这个细节能不能直接放到另一个学生身上？
```

如果能，这个 SMID 不够好。

好的 SMID 通常是：

- 一个物件；
- 一个动作；
- 一个私人系统；
- 一个错误分类；
- 一个表格、日志、笔记、翻译选择、错题本、座位图、调试记录；
- 一个学生反复做但自己没觉得重要的动作；
- 一个能在结尾回扣、且回扣时意义改变的细节。

弱的 SMID 通常是：

- “my passion for biology”；
- “helping others”；
- “my leadership experience”；
- “winning the competition”；
- “overcoming challenges”；
- “environmental protection”；
- “community service”。

### 3.2 SMID 是否能支撑结构

V3 新增了一个强制测试：

```text
这个细节能不能支撑至少一个 Level 2+ 的叙事结构？
```

Level 2+ 不是说文章一定要花哨，而是这个细节至少能写成 object-driven / behavior-driven narrative。

一个 SMID 如果只是“独特”，但不能带出开头、冲突、纠错、结尾回扣，就不能作为核心。

合格输出里必须有：

```text
Opening use
Friction or pressure
Method change
Ending callback
```

如果没有，回复：

```text
Rerun the SMID Structural Feasibility Gate. Do not select a detail until it can support opening, friction, method change, and ending callback.
```

### 3.3 Awards-Removed 是否通过

对中国学生、高成就学生、活动同质化学生，这个问题必须问：

```text
如果把所有奖项、排名、机构背书删掉，这篇文书还成立吗？
```

如果不成立，说明它还是简历扩写。

你可以回复：

```text
This direction is still award-dependent. Rerun SMID selection with the awards removed. Find a private system, misread, ordinary object, method change, or care-without-performance detail.
```

### 3.4 三个 Angle 是否真的有差异

V3 要求三个角度分别是：

```text
Safer
Recommended
Riskier
```

它们不应该只是同一个故事换标题，而应该在结构风险上不同。

例如：

```text
Safer = clean narrative
Recommended = object-driven narrative
Riskier = braided montage / soft formal play
```

如果三个方向听起来差不多，回复：

```text
Regenerate the three angles. Make them differ by Creative Risk Ladder level, not just by wording.
```

### 3.5 Recommended Blueprint 是否轻而准确

Common App 650 词默认 5–6 段，不要强迫 7–8 段。

好的 blueprint 每段应该说明：

```text
这一段的功能
具体名词 / 动作
新增信息
素材来源
```

如果每段都像任务清单，回复：

```text
Simplify the blueprint to 5–6 paragraphs. Remove checklist pressure. Let each paragraph do one narrative job.
```

---

## 4. 什么时候触发 Insufficient Scene Evidence Alert

V3 给了具体标准。以下情况满足两个以上，就应该触发：

1. 少于两个有地点 + 动作 + 物件/材料的场景；
2. 没有学生做出微选择的时刻；
3. 没有纠错、改方法、道歉、修订、行为改变；
4. 素材主要是奖项、成绩、课程、机构名、活动总结；
5. 70% 以上内容可以无损套给类似学生；
6. 最强细节无法支撑 Level 2 结构；
7. 题目要求个人反思，但素材只有学术/技术总结。

触发后，不要让 Agent 长采访。只问最多五个小问题，例如：

```text
What object, document, screen, or tool was in your hand during this activity?
What was one small choice you made that another student might not have made?
What did you first misread, over-control, rush, or ignore?
What did you stop doing after the experience?
What ordinary scene repeats in this story?
```

---

## 5. Risk Ladder 什么时候用

V2 的 Risk Ladder 好用，但时机不清楚。V3 固定三个触发点。

### 5.1 第一次：SMID 选择阶段

检查这个细节能支撑什么结构：

```text
Level 1 = clean narrative only
Level 2 = object-driven narrative
Level 3 = braided / montage
Level 4 = soft formal play
Level 5 = hard formal play / high-concept
```

SMID 至少要能支撑 Level 2，除非素材特别薄。

### 5.2 第二次：三个主线候选之后

每个 Angle 都要标风险等级。

默认组合：

```text
一个安全方向
一个推荐方向
一个更冒险方向
```

### 5.3 第三次：当你说 Go riskier / Go safer

如果你说：

```text
Go riskier.
```

Agent 不应该夸张事实，而应该增加结构风险，比如：

- 单线叙事 → object-driven；
- 单场景 → montage；
- 普通回扣 → motif；
- 按时间写 → time cut；
- 直接解释 → 让 callback 承载意义。

如果素材不支持，它应该拒绝硬上更花哨的形式。

---

## 6. Full Dossier 什么时候用

默认不用 Full Dossier。

适合以下情况：

- 学生素材很多，方向复杂；
- 需要 Common App + UC + 多校小文书整体规划；
- 第一次 Quick Dossier 的方向都很普通；
- 学生的 Chinese-context 同质化问题严重；
- 你想比较 voice；
- 你考虑 formal play，但不确定风险。

调用命令：

```text
Full Creative Dossier.
```

Full 模式会输出更多内容：Evidence Ledger、至少 5 个 SMID、China Audit、Voice Bootstrap、Formal Play Matrix、10 个角度等。

---

## 7. Voice Construction 怎么看

V3 保留了 Voice Construction，但 Quick 模式只输出 Voice Capsule。

Voice Capsule 应该包含：

```text
Attention lens
Decision tempo
Emotional temperature
Sentence tendency
Vocabulary domains
What to avoid
```

如果你要求 Full Voice Bootstrap，三个 80 词声音样本必须在至少两个轴上明显不同，尤其是：

```text
Attention lens
Sentence engine
```

如果三个样本听起来都是“流畅优秀高中生”，回复：

```text
The three voice samples are not meaningfully different. Re-run Voice Bootstrap. Make them diverge on attention lens and sentence engine.
```

不要让 Agent 用 slang 假装高中生。

---

## 8. 中国学生素材怎么处理

同质化素材不是问题本身，写法才是问题。

### 8.1 常见素材不要这样写

| 素材 | 不要写 | 应该找 |
|---|---|---|
| 竞赛 | 我努力后获奖 | 错误分类、私下系统、优化陷阱、失败后的方法改变 |
| 科研 | 我发现专业热情 | 具体问题、失败测量、尴尬数据、人与问题的关系 |
| MUN / Debate | 我学会沟通 | 赢了但没听懂人的时刻、停止抢答、改变提问方式 |
| 支教 / 公益 | 我帮助别人 | 自己一开始的误判、当地知识、具体调整，避免救世主叙事 |
| 考试压力 | 我坚持不懈 | 小型反抗、私下标准、对 rank 的重新处理 |
| 中西文化 | 我融合两种文化 | 一个翻译选择、一个家庭词汇、一个课堂误解 |

### 8.2 必答问题

```text
Would the essay still work if all awards were removed?
```

这不是检查清单里的可选项，而是 SMID 阶段的强制过滤。

### 8.3 常用修复命令

```text
Run China-context differentiation again. Remove the achievement arc. Find the private system, misread, institutional friction, anti-rank choice, or quiet care that makes this student specific.
```

---

## 9. 方向确认后怎么让它写正文

当你喜欢某个方向时，直接说：

```text
Use Angle 2. Keep the selected SMID. Draft now.
```

或者：

```text
Use the recommended direction. Draft 1, Line Edit, Draft 2, and Tiered Final Self-Audit.
```

如果你赶时间：

```text
Auto-select the strongest direction and continue to Draft 1, Line Edit, Draft 2, and Tiered Final Self-Audit.
```

---

## 10. 红黄绿 Final Self-Audit 怎么用

V3 不再把所有检查项平铺。它分成三层。

### 🔴 必须修复

只要有一个失败，就不能交：

- Truth support；
- Prompt and word limit；
- SMID centrality；
- Method change；
- No résumé dependence；
- Safety / admissions risk。

### 🟡 强烈建议修复

这些不一定致命，但会明显影响质量：

- Voice；
- Scene density；
- China-context differentiation；
- Ending；
- Portfolio value。

### 🟢 可选优化

这些是最后润色：

- Rhythm；
- Anti-AI language；
- Formal play；
- Compression；
- Callback precision。

你审稿时先看红项，不要被绿色小问题分散注意力。

---

## 11. 常用命令模板

### 11.1 最短启动模板

```markdown
Use the Top 20 College Essay Creative Offense Skill V3.
Quick Dossier only. Do not draft yet.
Find the SMID, verify structural feasibility, give 3 angles, and recommend one direction.

Student packet:
[paste all materials]
```

### 11.2 直接写作模板

```markdown
Use the Top 20 College Essay Creative Offense Skill V3.
Auto-select the strongest direction and continue to Draft 1, Line Edit, Draft 2, and Tiered Final Self-Audit.
Use only packet-supported facts. Keep the prose vivid, human, and high-school-senior voiced.

Student packet:
[paste all materials]
```

### 11.3 重跑 SMID

```text
Rerun SMID. Ignore awards and activities. Look for objects, private systems, misreads, repeated actions, embarrassing small choices, method changes, and ordinary scenes. Apply Structural Feasibility Gate before selecting.
```

### 11.4 更冒险

```text
Go riskier by one Creative Risk Ladder level, but do not exaggerate facts. Increase structural risk only if the packet supports it.
```

### 11.5 更稳妥

```text
Go safer. Keep the SMID, but reduce structural risk and make the chronology clearer.
```

### 11.6 输出太重

```text
Compress this into Quick Dossier mode. Keep only selected SMID, structural feasibility, 3 angles, recommended direction, and verification needs.
```

### 11.7 素材太薄

```text
Trigger Insufficient Scene Evidence Alert if needed. Ask no more than five tiny scene questions. Do not conduct a long interview.
```

---

## 12. 什么时候这套系统会失效

这套系统不是魔法。以下情况要人工介入：

1. **素材全是活动名和奖项**：需要补场景，否则只能写出简历扩写。
2. **学生没有任何可公开个人材料**：只能写保守版本，不能假装有 personal voice。
3. **核心故事涉及高风险敏感话题**：需要人工判断是否值得写。
4. **Agent 的三个角度都依赖奖项**：重跑 SMID，不要进入正文。
5. **SMID 不能回扣**：换细节或降级为普通 motif。
6. **形式太花哨但内容不支撑**：降级为普通叙事。

一个简单判断：

```text
如果把活动名、奖项、机构名全部遮住，这篇文书还像这个学生吗？
```

如果不像，方向不对。

---

## 13. 建议参数

| 任务 | temperature 建议 |
|---|---:|
| Quick Dossier / 角度探索 | 1.2–1.7 |
| Full Dossier | 1.0–1.5 |
| Draft 1 | 1.0–1.4 |
| Draft 2 / 去 AI 味 | 0.7–1.1 |
| UC PIQ | 0.6–1.0 |
| Why School / Why Major | 0.4–0.8 |
| Final Self-Audit | 0.2–0.5 |

如果平台不能设置 temperature，就在 prompt 里写：

```text
Write with high structural creativity but strict factual grounding.
```

---

## 14. 一句话总结

V3 的目标不是让 Agent 输出更多，而是让它在最关键的判断点输出更准：

```text
先找不可替代细节，验证它能不能写，再给三个结构上有差异的方向。
```

只要第一轮 SMID 和结构可行性判断正确，后面的正文质量会稳定很多。
