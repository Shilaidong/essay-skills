# 授课型硕士申请文书系统操作指南
## V1：从“个人故事”切换到“研究生申请论证”

这套系统不是把美本文书 Skill 换成“研究生”三个字。

授课型硕士文书的底层任务完全不同。招生方通常不是在寻找一个最有趣、最有故事感的人，而是在判断：

```text
你为什么进入这个领域？
你是否已经具备完成项目的基础？
你现在缺什么能力？
为什么必须通过这个项目补足？
学完以后，你会把训练用到哪里？
```

所以，本系统的核心不是 SMID、物件回扣或个人成长弧线，而是：

```text
Graduate Rationale Spine（研究生申请主脊柱）
+ Evidence / Readiness Map（证据与准备度地图）
+ Programme Fit Chain（项目匹配因果链）
+ Career Plausibility（职业目标可信度）
```

它适用于英国、美国、香港、新加坡及其他地区的高选择性授课型 / coursework-based 硕士项目，包括 MA、MSc、MEng、MEd、MPH、MPP、MPA、MiM、MFin、LLM，以及带 capstone、practicum、studio 或 dissertation 的授课型项目。

它不适合直接处理 PhD、导师制研究型硕士或完整 research proposal。

---

## 1. 三个文件分别是什么

压缩包中包含：

```text
skill.md
packet_prompt_en.md
operation_guide_cn.md
```

### 1.1 `skill.md`

这是长期能力层，放入 Agent 的：

- skill 文件夹；
- system prompt；
- developer prompt；
- 或长期知识 / 指令层。

它定义 Agent 如何判断授课型硕士申请：

- 先识别项目类型和文书类型；
- 核对官方 prompt、字数、评估标准和 AI 使用政策；
- 从材料包中构建准备度证据；
- 形成 Graduate Rationale Spine；
- 选择两到三个最有说服力的证据单元；
- 将“为什么这个项目”写成因果关系；
- 校准职业目标；
- 区分 SOP、Personal Statement、Personal History、Career Goals、Addendum 等文件的任务；
- 处理跨专业、低分、工作经历不足、中国学生材料同质化等问题。

### 1.2 `packet_prompt_en.md`

这是每个申请项目开始时使用的英文调用 Prompt。

它要求 Agent 默认先输出：

```text
Programme Requirement Card
Application Diagnosis
3 个 Graduate Rationale Spine 候选
Selected GRS
2–3 个核心证据单元
3 个文书角度
推荐结构
项目匹配因果链
待核验内容
```

不会一上来直接生成一篇看似完整但逻辑错误的 SOP。

### 1.3 `operation_guide_cn.md`

这是给顾问、文案老师或申请者看的中文操作手册。

重点不是“复制哪一句 Prompt”，而是：

- 如何判断 Agent 第一轮分析是否合格；
- 什么时候继续写；
- 什么时候退回补证据；
- 什么时候必须换路线；
- 哪些项目不允许使用生成式 AI 起草；
- 多项目申请时如何改写，而不是替换学校名字。

---

## 2. 授课型硕士文书和美本文书的根本差别

### 2.1 美本文书的核心问题

通常是：

```text
这个学生是谁？
他如何看问题、做选择、修正行为？
```

### 2.2 授课型硕士文书的核心问题

通常是：

```text
这个申请者为什么需要更高级的训练？
现有经历是否证明他能完成训练？
这个具体项目为什么是合理的下一步？
```

因此，研究生文书不应机械套用以下美本方法：

- 强制开场场景；
- 强制个人成长故事；
- 强制小物件回扣；
- 强制展现“真实的我”；
- 强制使用幽默或形式实验；
- 将活动写成情绪变化。

研究生文书可以有故事，但故事必须服务于：

```text
问题
方法
责任
局限
能力缺口
项目用途
```

---

## 3. 最推荐的整体工作流

### Step 1：加载 Skill

把 `skill.md` 放到 Agent 的长期指令层。

不要每次只粘贴一小段 Skill。它包含项目路由、证据地图、职业目标、AI 政策和多校改写等相互关联的判断。

### Step 2：准备申请者资料包

不需要让申请者重新填复杂表格。可以直接提供现有资料：

```markdown
## Target Document
- 学校与项目
- 文书类型
- 官方题目
- 字数 / 字符限制
- 项目官网内容
- AI 使用政策（如已知）

## Applicant Profile
个人背景与申请方向

## CV / Resume
完整简历

## Transcript / Relevant Modules
成绩单、相关课程、评分背景

## Thesis / Research / Projects / Portfolio
毕业论文、科研、项目、设计作品、课程作业

## Work and Internship Evidence
实习与工作记录

## Career Goals
短期与中期职业方向

## Counselor / Applicant Conversation
沟通记录

## Existing Draft
旧稿

## Boundaries
不希望写或需要谨慎处理的信息
```

资料不用排版完美，但最好标明来源。

### Step 3：粘贴英文 Prompt

复制 `packet_prompt_en.md` 中：

```text
# COPY-PASTE PROMPT STARTS HERE
```

到：

```text
# COPY-PASTE PROMPT ENDS HERE
```

在最后粘贴资料包。

### Step 4：第一轮只做 Quick Strategy Memo

推荐命令：

```text
Quick Strategy Memo. Do not draft yet.
```

第一轮的目的不是获得正文，而是判断：

- 项目到底在选什么人；
- 申请者最有说服力的准备度是什么；
- 申请者当前真正缺什么；
- 学位为什么现在有必要；
- 哪个写作角度最适合；
- 项目匹配是否真实而具体。

### Step 5：确认主线后再写

例如：

```text
Use GRS 2 and Angle 2. Draft Mode.
```

或者：

```text
Keep the selected GRS, but make the statement more academic and less career-heavy. Draft Mode.
```

### Step 6：做 Line Edit 和 Draft 2

不要把 Draft 1 当最终稿。

第二轮重点检查：

- 是否把 CV 改写成了段落；
- 是否夸大了团队项目中的个人贡献；
- 是否真正解释了方法和判断；
- 项目匹配是不是课程名单；
- 职业目标是否过度承诺；
- 文风是否像咨询公司宣传稿；
- 是否有不准确的项目事实。

### Step 7：完成红黄绿分层自检

只有红色项全部通过，才可以进入人工终审。

---

## 4. 第一轮输出怎么判断好坏

### 4.1 Programme Requirement Card 是否真的做了项目研究

合格的卡片应包含：

- 项目真实教学模式；
- 文书类型；
- 官方题目；
- 字数或字符限制；
- 官方评估重点；
- 核心课程 / pathway / capstone / practicum / dissertation 等；
- AI 使用政策；
- 信息核验日期。

警惕以下问题：

- 把所有 MSc 都当研究型；
- 只写学校排名；
- 使用过期课程名；
- 编造学生能接触某教授；
- 把 optional module 写成必修；
- 忽略字符限制；
- 没有核对 AI 政策。

如果项目资料不足，Agent 应写：

```text
[VERIFY OFFICIAL]
```

而不是猜。

### 4.2 Graduate Rationale Spine 是否完整

一个合格的 GRS 应包含五个环节：

```text
Origin：我已经遇到什么问题
Readiness：我做过什么，证明我有基础
Gap：我当前缺什么能力
Intervention：这个项目如何补足
Next Use：完成项目后会把能力用于什么
```

最实用的判断问题：

```text
为什么现在读？
为什么必须读授课型硕士？
为什么是这个项目？
为什么这个申请者能读下来？
读完具体做什么？
```

有一个问题答不清，主线就不完整。

### 4.3 核心证据单元是否有“个人所有权”

每个核心证据单元必须明确：

- 项目背景；
- 申请者个人负责什么；
- 使用了什么方法或工具；
- 做了什么判断；
- 出现了什么结果或限制；
- 该限制如何连接研究生训练需求。

如果只写：

```text
参与某项目；
服务某客户；
团队获得某结果；
在某知名公司实习；
```

都不够。

可以要求 Agent：

```text
Audit ownership claims. Separate the applicant's contribution from team outcomes.
```

### 4.4 三个角度是否真正不同

合格的三个角度可以是：

```text
Angle 1：直接证据型
Angle 2：方法缺口型
Angle 3：专业责任 / 跨领域问题型
```

不合格情况是：三个角度只是更换开头句，证据顺序、主脊柱和结尾完全一致。

可以回复：

```text
Regenerate the three angles. Make them differ in rationale, evidence order, and programme-fit route—not only in wording.
```

### 4.5 Programme Fit Chain 是否为因果关系

项目匹配必须是：

```text
我的能力缺口
→ 项目资源
→ 我会如何使用
→ 最终获得什么能力或输出
```

例如：

```text
缺口：只能做描述性分析，缺少因果推断能力
资源：高级计量 / epidemiology sequence
使用：重新检验现有项目中的混杂因素
输出：进入政策评估或医疗数据分析岗位所需的判断能力
```

以下表达基本无效：

- world-class faculty；
- prestigious university；
- international environment；
- global city；
- diverse cohort；
- cutting-edge curriculum；
- renowned professors。

除非后面有明确的“如何使用”。

### 4.6 职业目标是否可信

早期申请者不需要写得像已经知道十年后的职位。

推荐结构：

```text
function + sector + problem
```

例如：

```text
在数字医疗公司从事产品分析，负责实验设计与用户留存判断。
```

比以下表达可信：

```text
成为全球医疗科技行业的领军人物。
```

有工作经验的申请者则应说明责任升级：

```text
执行 → 决策
单项目 → 项目组合
分析 → 资源配置
本地执行 → 系统设计
专业角色 → 跨团队责任
```

---

## 5. 什么时候使用不同模式

### 5.1 Quick Strategy Memo

适合：

- 单个项目；
- 材料比较完整；
- 想先快速确定方向；
- 经验丰富的顾问进行人工筛选。

命令：

```text
Quick Strategy Memo. Do not draft yet.
```

### 5.2 Full Application Dossier

适合：

- 跨专业申请；
- 成绩单有明显弱项；
- 工作经验复杂；
- 需要 SOP + Personal History 两份文件；
- 多个项目教学模式差异大；
- 申请 1,000–1,500 词长文书；
- 材料中团队科研和个人贡献难区分。

命令：

```text
Full Application Dossier. Do not draft yet.
```

### 5.3 Draft Mode

方向确认后使用：

```text
Use GRS 1 and Angle 2. Draft Mode.
```

### 5.4 Auto-select and Draft

时间紧，允许 Agent 自动判断：

```text
Auto-select the strongest defensible direction and draft.
```

不建议在材料复杂、跨专业或低分解释型申请中直接使用。

### 5.5 Repair Mode

旧稿存在以下问题时使用：

- 像简历；
- 像本科个人陈述；
- 像 PhD proposal；
- 为什么项目写成课程罗列；
- 职业目标空泛；
- 语言非常 AI 或 corporate；
- 每个项目只替换学校名。

命令：

```text
Repair Mode. Rebuild the GRS before rewriting.
```

### 5.6 Programme Adaptation Mode

已有一篇好基础稿，需要改另一所学校：

```text
Programme Adaptation Mode. Do not perform name-and-module substitution.
```

### 5.7 Coaching-Only Mode

当学校明确禁止 AI 生成申请材料，或者申请者希望自己完成写作时使用：

```text
Coaching-Only Mode. Do not generate a submit-ready statement.
```

此模式只输出：

- 申请诊断；
- GRS 选项；
- 证据问题；
- 段落提纲；
- 对申请者原稿的逐句修改建议；
- 最终合规清单。

---

## 6. AI 使用政策：必须单独核验

授课型硕士项目对生成式 AI 的规定并不统一。

有些学校允许使用 AI 做资料研究或语言辅助，但不允许 AI 生成或构成申请文件基础；有些项目只要求文书是申请者本人真实完成；还有很多项目没有在主页面上清楚说明。

因此，这套系统把 AI 政策放在写作前，而不是最后提醒。

### 实操规则

```text
允许生成辅助
→ 可以进入正常 Draft Mode，但申请者必须逐句核对并能够解释。

只允许编辑
→ 申请者先写，Agent 做诊断和修改，不从零生成。

禁止 AI 生成
→ 进入 Coaching-Only Mode。

政策未知
→ 标记 [VERIFY AI POLICY]，不得称为 submission-ready。
```

不要因为其他学校允许，就推定当前学校允许。

---

## 7. 不同项目类型的写作重点

### 7.1 学术型授课硕士

例如许多人文、社科、自然科学 MA / MSc。

重点：

- 相关课程；
- 学术问题；
- 研究或写作能力；
- 方法基础；
- 当前知识缺口；
- 课程和 dissertation 的匹配。

不要把它写成职业规划书，也不要写成完整 PhD 研究计划。

### 7.2 研究密集型授课硕士

重点：

- 科研所有权；
- 方法选择；
- 数据、实验、文本、档案、田野或设计过程；
- 已发现的限制；
- 需要学习的高级方法；
- thesis / dissertation / research placement。

### 7.3 职业实践型硕士

例如 MPP、MPA、MPH、MEd、规划、医疗、社会工作等。

重点：

- 真实工作或实践问题；
- stakeholders；
- 决策与后果；
- 实施困难；
- practicum、clinic、capstone 等；
- 毕业后的具体职业功能。

### 7.4 跨专业 / Conversion 项目

重点：

- 原专业能带来什么；
- 为什么转向；
- 已经补了哪些先修能力；
- 做过哪些桥梁项目；
- 这个学位补足的精确缺口。

不能只写“我对新领域很感兴趣”。

### 7.5 商科、金融、管理、商业分析

重点：

- 职能和行业；
- 商业或组织决策；
- 定量准备；
- 当前责任；
- 为什么现在读；
- 实践项目和职业路线。

不要堆公司品牌、领导力形容词或管理愿景。

### 7.6 艺术、设计、建筑、媒体

重点：

- portfolio 的内在逻辑；
- 创作或设计问题；
- 材料、媒介、用户、场地、受众；
- critique 和 revision；
- studio / workshop / archive / production fit。

这一类项目可以使用更高的结构创造力，但仍需证明实践发展与项目匹配。

---

## 8. 中国学生材料怎么避免同质化

研究生申请的差异化不主要依赖“不可替代的人生故事”，而依赖：

```text
你实际负责什么；
你为什么选择某种方法；
你做了什么判断；
你遇到什么限制；
这个限制为什么需要研究生训练。
```

### 8.1 去品牌测试

删掉：

- 学校名；
- 公司名；
- 客户名；
- 比赛名；
- 奖项名。

再看这个经历是否仍有说服力。

如果删掉品牌后只剩：

```text
参与项目、完成任务、提升能力
```

说明材料尚未被挖掘。

### 8.2 科研所有权

需要区分：

- 课题由谁提出；
- 申请者负责哪部分；
- 哪种方法是自己使用的；
- 是否写了论文；
- 投稿、录用、发表分别是什么状态；
- 申请者真正发现了什么限制。

不能把导师或实验室成果写成个人成果。

### 8.3 实习含金量

实习段落不看公司名字，而看：

```text
问题
+ 责任
+ 方法
+ 判断
+ 输出
+ 局限
```

短期实习最多支撑一个窄证据点，不应自动承担完整职业主线。

### 8.4 常见无效表达

- 为中国发展作贡献；
- 成为行业领袖；
- 连接中西方；
- 拥有全球视野；
- 在世界级平台提升自己；
- 用科技改变社会；
- 将所学回馈祖国。

应改为：

```text
function + sector + problem + context
```

---

## 9. 特殊情况处理

### 9.1 没有工作经验

可以使用：

- 高阶课程；
- 毕业论文；
- capstone；
- 独立研究；
- 技术项目；
- 客户型课程项目；
- 有实质责任的社团或公益项目；
- portfolio；
- 有证据的职业探索。

不要伪造职业成熟度。重点写学术准备和清晰的下一步。

### 9.2 跨专业申请

先检查：

```text
原专业提供了什么可迁移能力？
新方向由什么具体经历触发？
已经做过什么桥梁准备？
仍缺什么？
为什么必须通过该项目补足？
```

如果没有桥梁证据，应先进入 Evidence Recovery Mode。

### 9.3 GPA 或核心课成绩较弱

优先考虑是否存在单独 Addendum。

解释结构：

```text
事实
→ 有边界的背景
→ 采取的修正行动
→ 当前更能说明能力的证据
```

不要长篇辩解、责怪老师或用情绪掩盖问题。

### 9.4 研究经历很强，但申请授课型项目

要回答：

- 为什么不直接申请研究型学位？
- 需要的是哪种结构化训练？
- taught modules、methods、capstone、placement 或 cohort 如何解决问题？
- 是否把教授和实验室写得过多？

避免“PhD cosplay”。

### 9.5 工作经验很多

不要从第一份工作按时间写到现在。

选择：

- 一次责任升级；
- 一个重复出现的问题；
- 一个方法或判断的天花板；
- 一次职业转向；
- 两到三个最能证明准备度的证据单元。

### 9.6 申请多个相似项目

可以复用：

- 核心证据；
- 部分 GRS；
- 职业方向；
- 基础语气。

必须重算：

- 项目类型；
- 官方题目；
- 项目评估重点；
- programme fit；
- 证据顺序；
- why now 强调；
- career emphasis；
- AI 政策。

不能只替换学校名与课程名。

### 9.7 SOP 与 Personal History 同时要求

分工应为：

```text
SOP：准备度、问题、方法缺口、项目匹配、职业 / 学术目标
Personal History：背景、责任、障碍、视角、对研究生社群的贡献
```

同一个事实可以出现，但解释功能必须不同。

---

## 10. 常用命令

### 10.1 最短分析命令

```markdown
Use the Selective Taught Master's Application Writing Skill V1.
Quick Strategy Memo. Do not draft yet.
Verify the programme requirement, statement type, word limit, and AI policy first.
Build three Graduate Rationale Spine candidates, select one, identify 2–3 evidence units, give three statement angles, and recommend an architecture.

Applicant and programme packet:
[paste]
```

### 10.2 自动写作命令

```markdown
Use the Selective Taught Master's Application Writing Skill V1.
Auto-select the strongest defensible GRS and angle.
Then produce Draft 1, Line Edit, Draft 2, and the Tiered Final Audit.
Do not label the draft submission-ready unless the official prompt, programme facts, and AI policy are verified.

Packet:
[paste]
```

### 10.3 修复旧稿

```markdown
Repair Mode.
Rebuild the Graduate Rationale Spine before rewriting.
Remove CV chronology, verify ownership, repair programme fit using Need → Resource → Use → Output, and calibrate the career goal.

Current draft and packet:
[paste]
```

### 10.4 多校改写

```markdown
Programme Adaptation Mode.
Do not replace names and modules mechanically.
Recalculate the programme type, official prompt, GRS, evidence order, fit chain, career emphasis, and AI policy.

Base statement:
[paste]

New programme materials:
[paste]
```

### 10.5 强化学术性

```text
Go more academic. Increase intellectual and methodological depth, but do not turn this into a research proposal.
```

### 10.6 强化职业性

```text
Go more professional. Clarify responsibility, decisions, stakeholders, why now, and the post-degree function.
```

### 10.7 核验个人贡献

```text
Audit ownership claims. Separate individual actions from team outcomes and flag every unsupported contribution.
```

### 10.8 核验项目匹配

```text
Audit programme facts and rebuild every fit sentence as Need → Resource → Use → Output.
```

---

## 11. 模型参数建议

不同平台对 temperature 的定义不同，不要迷信固定数值。

可参考：

| 任务 | 建议倾向 |
|---|---|
| 材料分析 / GRS 生成 | 中等创造力，较高逻辑性 |
| 三个角度 | 中等创造力 |
| 第一稿 | 适度创造，严控事实 |
| 技术型 / 学术型 SOP | 比本科文书更低的随机性 |
| Line Edit | 低随机性 |
| 项目事实和字数核验 | 很低随机性 |

有参数时，可大致使用：

```text
策略与角度：0.8–1.2
初稿：0.7–1.0
精修：0.3–0.7
最终核验：0.1–0.4
```

没有参数时，使用：

```text
high analytical specificity, moderate structural creativity, strict factual grounding
```

---

## 12. 系统会失效的情况

以下情况必须人工介入：

### 12.1 没有官方项目资料

没有 prompt、字数、项目页面、教学结构时，任何 Why Programme 都只能是临时稿。

### 12.2 职业方向完全未形成

如果申请者只能说“想进入金融 / 咨询 / 数据 / 政策”，需要补充：

- 想做什么功能；
- 面对什么问题；
- 服务什么行业或机构；
- 已经做过什么探索。

### 12.3 所有经历都只有标题

需要进入 Evidence Recovery Mode，补：

- 个人责任；
- 方法；
- 判断；
- 输出；
- 局限。

### 12.4 项目跨度过大

例如同时申请：

- Data Science；
- Public Policy；
- Marketing；
- Environmental Management。

不能用同一套 GRS。必须按项目族群建立不同申请主线。

### 12.5 学校禁止 AI 生成

必须切换 Coaching-Only Mode。不要通过“先生成再让申请者改写”绕过规定。

### 12.6 文书与面试能力严重不匹配

如果申请者无法解释文书里的方法、项目内容或职业选择，文书即使语言优秀也不应提交。

---

## 13. 最终人工终审清单

### 红色：不通过就不能交

- [ ] 官方题目、字数、格式已核验
- [ ] AI 使用政策已核验
- [ ] 项目事实准确
- [ ] 每个个人贡献都有证据
- [ ] 没有把团队成果写成个人成果
- [ ] GRS 五个环节完整
- [ ] 申请者准备度有具体证据
- [ ] Why Programme 是因果链，不是课程名单
- [ ] 职业目标合理
- [ ] 申请者能在面试中解释每一句

### 黄色：强烈建议解决

- [ ] why now 清楚
- [ ] 没有 CV 段落化
- [ ] 开头不是童年兴趣
- [ ] 研究生文风成熟但不 corporate
- [ ] 中国背景说明不过度
- [ ] SOP 和 Personal History 不重复
- [ ] 转专业有桥梁证据
- [ ] 低分解释简短且有后续证据

### 绿色：语言优化

- [ ] 抽象词可否改成方法或动作
- [ ] 项目表扬句可否删除
- [ ] 长句是否影响理解
- [ ] 结尾是否具体
- [ ] 是否存在重复转折

---

## 14. 这套系统最重要的一句话

授课型硕士文书不是证明申请者“很优秀”，而是证明：

> 申请者已经走到一个真实的问题或责任面前，现有能力不足以继续，而这个具体项目能够以一种可验证的方式帮助他完成下一步。

只要这条因果链成立，文书就会比堆叠经历、学校宣传和职业口号更有说服力。

---

## 15. 研究基础与更新原则

本系统参考了多所选择性大学和授课型项目的官方研究生申请指导。官方指导反复强调的共同内容包括：

- 申请动机；
- 学术或职业准备；
- 与具体项目的匹配；
- 未来学术或职业目标；
- 只写与项目相关的内容；
- 按课程页面核对具体要求；
- SOP 与 Personal History 等文件承担不同任务；
- 申请材料必须由申请者真实拥有；
- 部分学校对 AI 生成申请材料有明确限制。

项目要求会随申请季变化。因此：

```text
当前官方项目页面
> 本指南
> 通用写作经验
```

每次申请都要重新核对 prompt、字数、评估标准、课程结构和 AI 政策。
