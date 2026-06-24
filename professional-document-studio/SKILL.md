---
name: professional-document-studio
description: Research, analyze, write, format, and quality-check polished professional documents, especially DOCX files. Use for strategy reports, research briefs, proposals, plans, white papers, case analyses, meeting outputs, and other substantial documents that may require current web research, citations, tables, charts, timelines, or a reusable Word template. The user supplies any domain-specific modules separately; do not assume any industry, topic, document module, or decision structure unless requested.
license: MIT
compatibility: Codex and OpenCode. Core workflow needs file read/write and shell or Python. Current-fact research needs a web-search or browser capability. DOCX automation uses Python 3.10+, python-docx, PyYAML, Pillow, and matplotlib; final visual QA benefits from LibreOffice and Poppler or another DOCX renderer.
metadata:
  author: OpenAI
  version: "2.0.0"
  language: zh-CN
  scope: general-document-authoring
---

# Professional Document Studio

## 1. Mission

把零散需求、原始资料、实时研究和分析判断，转化为一份：

- 结构完整；
- 信息可核验；
- 论证清楚；
- 结论可执行；
- 视觉统一；
- 可继续编辑；
- 经过渲染检查的专业文档。

本 Skill 只定义**标准化的文档生产方法**。主题、行业、报告模块、对象、项目或其他具体内容，必须由用户在调用时另行说明；不得把任何案例专属结构写死为默认要求。

核心链路：

```text
任务要求
→ 输入资料与事实状态
→ 研究与来源台账
→ 分析框架与决策逻辑
→ 信息架构
→ 初稿与编辑
→ 表格 / 图表 / 时间轴
→ DOCX生成
→ 渲染与逐页检查
→ 最终交付
```

## 2. Use boundaries

适合使用本 Skill：

- 从资料、访谈纪要、网页、PDF、表格或笔记生成正式报告；
- 撰写或重构方案书、规划案、研究报告、咨询报告、白皮书、项目计划、案例分析、会议纪要、评估报告；
- 将已有文本改造成结构更专业、版式更成熟的 Word 文件；
- 需要实时检索、来源核验、引用、表格、图表、甘特图或附件台账；
- 需要中文宋体或其他指定字体的可编辑 DOCX；
- 需要同时交付正文、图表、来源台账或可再生成的结构化内容文件。

不应自动使用本 Skill：

- 只需一两段聊天回复；
- 用户只要求翻译、简单改写或单句润色；
- 不需要文档产物的纯讨论；
- 任务需要某个专门领域 Skill，且该 Skill 已经覆盖完整工作流。

## 3. Non-negotiable standards

1. **先定义交付物，再写内容。** 明确读者、目的、格式、长度、必含模块、截止时间和验收标准。
2. **事实、推断、建议、目标和假设必须分开。** 不把未来目标写成既有成果，不把推断写成已证实事实。
3. **时效性事实必须核验。** 政策、价格、人员、规则、产品规格、截止日期等会变化的信息，使用当前官方来源。
4. **优先使用一手来源。** 官方网站、原始文件、研究论文、监管文件、合同、数据集和用户提供的原始材料优先。
5. **先分析，后排版。** 美观不能掩盖逻辑缺口；在信息架构稳定前，不投入大量版式工作。
6. **每个结论要有证据链。** 推荐至少说明：依据、解释、取舍、行动和风险。
7. **图表必须承载信息。** 不为了装饰而加入图表；事实型图表使用真实数据和可复现代码。
8. **不伪造来源或案例。** 可匿名化、重组和概括公开材料，但不得冒充自有案例或虚构验证。
9. **保护隐私与机密。** 只收集必要信息；敏感材料不上传到不受控服务；交付前清理元数据和临时文件。
10. **DOCX 必须经过 render → inspect → revise。** 未渲染逐页检查的 Word 文件不得视为完成。
11. **不给出隐藏思维过程。** 输出可复核的依据、判断标准和简洁决策说明，不暴露私有链式思维。
12. **失败要显式处理。** 搜索不到、文件损坏、字体缺失、渲染失败或工具不可用时，说明限制并采用可验证的替代路径。

## 4. Fact-state model

对重要信息使用以下状态之一：

- `VERIFIED`：有官方来源、原始文件、数据、证书或可核验记录支持；
- `USER-PROVIDED`：由用户提供，尚未独立核验；
- `INFERENCE`：基于已知事实得出的分析判断；
- `RECOMMENDATION`：建议采取的行动；
- `TARGET`：尚未完成的目标或计划；
- `ASSUMPTION`：因信息缺失而暂时采用的前提；
- `MISSING`：需要补充，且可能影响结论。

状态可以保存在内部台账中；正文不必机械标注每一句，但涉及风险、绩效、时间、预算或结果时必须写清。

## 5. Tool routing contract

### 5.1 先检查能力，不假设工具存在

开始任务前，确认当前环境是否具备：

- 本地文件读取与写入；
- Shell / Bash；
- Python；
- Web 搜索与网页抓取；
- PDF 解析或页面截图；
- DOCX 创建、编辑和渲染；
- 图表或图片生成；
- 私有连接器或 MCP 数据源。

只调用实际可用的工具。不要在最终回复中声称使用了未调用的工具。

### 5.2 工具选择原则

| 需求 | 首选方式 | 备用方式 | 禁忌 |
|---|---|---|---|
| 读取本地文本/代码 | 原生 read / shell | Python | 不用截图代替可解析文本 |
| 批量检索文件 | glob / grep / shell | Python pathlib | 不逐个手工打开大量文件 |
| 当前事实检索 | web search + 官方页面 | 官方 API / MCP | 不凭记忆回答易变事实 |
| 私有云文档 | 对应连接器 / MCP | 用户导出本地文件 | 不用公开搜索替代私有链接 |
| PDF 文字 | PDF 解析器 | 页面截图 | OCR 仅作为最后手段 |
| PDF 图表/版式 | 页面截图或渲染 | 图像查看器 | 不只依赖抽取文本判断图表 |
| 数据图表 | Python / matplotlib | 表格或专业可视化工具 | 不用生成式图片伪造数据图 |
| 甘特图 | `scripts/render_gantt.py` | 其他可复现绘图脚本 | 不把 Mermaid 源码直接塞进 Word |
| DOCX 创建 | `scripts/build_docx.py` 或 python-docx | 专门文档工具 | 不用截图拼成不可编辑文档 |
| DOCX 编辑 | python-docx / 专门文档工具 | OOXML 定向修补 | 不直接改压缩包内 XML，除非必要 |
| DOCX 视觉检查 | `scripts/qa_docx.py` 或标准渲染器 | LibreOffice + Poppler | 不凭 XML 或文本抽取判断版式 |
| 装饰性插图 | 图像生成工具，仅在用户需要时 | 授权素材 | 不把装饰图当作事实证据 |

### 5.3 搜索调用规范

- 将问题拆为 2–4 个检索簇：定义、事实、数据、对比或案例；
- 可并行检索互不依赖的主题；依赖前一步实体名称的检索必须顺序执行；
- 先搜索官方/原始来源，再用可靠二手来源补充语境；
- 打开并阅读实际页面，不只依赖搜索摘要；
- 对 PDF 中的表格、图或扫描页，渲染对应页面；
- 每个重要主张记录来源、发布日期或访问日期、适用范围和不确定性；
- 搜索失败时，记录已尝试的关键词和不足，不用猜测填空。

详见 `references/02-research-and-sources.md` 与 `references/05-tool-orchestration.md`。

### 5.4 本地工具调用规范

- 批量操作前先列目录和确认输入文件；
- 生成文件写入明确的输出目录，不覆盖用户原件，除非用户要求；
- 脚本调用使用确定路径和显式参数；
- 记录关键命令、输入和输出；
- 修改 DOCX 后立即渲染一次，不把所有版式问题留到最后；
- 任何脚本失败先读取错误信息，再修复，不盲目重复调用；
- 中间 PNG、PDF、缓存和日志默认仅用于 QA，不随最终交付一起发送。

## 6. Standard workflow

### Phase 0 — Establish the deliverable contract

提取或确认：

- 文档类型；
- 核心目的；
- 目标读者；
- 使用场景；
- 输出语言；
- 文件格式；
- 预计长度；
- 必含与禁用模块；
- 是否需要实时研究；
- 引用方式；
- 图表、时间轴或图片要求；
- 字体、配色、页眉页脚等视觉要求；
- 截止时间；
- 需要交付的附属文件。

只有当缺失信息会改变整体方向时，才提出一个简洁澄清问题；否则采用明确标注的假设继续。

可复制 `assets/document-brief-template.yaml`。

### Phase 1 — Inspect and normalize inputs

1. 列出所有输入文件和链接；
2. 识别格式、页数、时间范围和版本；
3. 提取文本、表格、图片和元数据；
4. 标出重复、冲突、缺失和过期内容；
5. 建立事实状态和来源台账；
6. 不修改原始文件，先在工作副本上操作。

### Phase 2 — Research only what is needed

根据交付目标制定研究清单，而不是无限扩展背景知识。

每个检索问题都要对应至少一个文档用途：

- 支撑事实；
- 比较方案；
- 解释趋势；
- 验证规则；
- 填补数据；
- 提供可执行基准。

输出 `sources.csv` 或同等台账，模板见 `assets/source-ledger-template.csv`。

### Phase 3 — Build the analysis model

先确定文档要解决的决策或问题，再选择分析工具。

常用结构：

- `问题 → 证据 → 解释 → 结论 → 行动`；
- `现状 → 目标 → 差距 → 路径 → 风险`；
- `选项 → 评价标准 → 权衡 → 推荐`；
- `原因 → 机制 → 影响 → 应对`；
- `输入 → 活动 → 产出 → 结果 → 影响`。

当用户要求多个方案时，把每个方案独立写完整，再增加共享条件、比较矩阵和选择门；不要默认文档一定需要固定数量或固定类型的方案。

详见 `references/03-analysis-and-reasoning.md`。

### Phase 4 — Design the information architecture

在写正文前，创建章节蓝图：

- 每章目的；
- 核心问题；
- 关键结论；
- 证据；
- 表格/图表；
- 与下一章的逻辑关系；
- 预计篇幅。

默认采用“决策优先”顺序：

1. 封面与文档说明；
2. 执行摘要；
3. 背景与范围；
4. 事实与分析；
5. 方案、建议或结论；
6. 实施计划、指标与风险；
7. 时间轴或附件；
8. 来源与说明。

这只是默认骨架。用户给出固定目录时，按用户目录执行。

### Phase 5 — Draft in layers

按以下顺序写：

1. 章节结论句；
2. 支撑证据；
3. 分析解释；
4. 行动建议；
5. 过渡与标题；
6. 执行摘要最后写。

每段尽量只承担一个功能。删除无法支持结论、行动或理解的背景信息。

### Phase 6 — Create tables and visuals

使用视觉元素的判断标准：

- 比较多个选项：表格或二维矩阵；
- 表示时间：时间轴或甘特图；
- 表示过程：流程图；
- 表示层级：树状结构；
- 表示真实数值变化：数据图表；
- 强调决策、风险或定义：Callout；
- 展示地点、设计或实物：授权图片或用户素材。

每个图表都必须有：

- 清晰标题；
- 单位；
- 数据来源；
- 时间范围；
- 必要注释；
- 正文中的解释。

### Phase 7 — Edit for logic, accuracy, and style

至少进行三轮编辑：

1. **结构编辑**：章节是否服务目的，是否有重复或缺口；
2. **证据编辑**：事实、数字、引用和表格是否一致；
3. **语言编辑**：句子是否清楚、具体、克制、面向读者。

禁止：

- 空泛形容词堆砌；
- 以“高端”“领先”“无敌”等词代替证据；
- 把相关性写成因果；
- 把目标写成成果；
- 用大量列表掩盖缺少分析；
- 机械重复用户原话。

### Phase 8 — Generate the DOCX

优先采用结构化内容文件：

```bash
cp assets/report-content-template.yaml report.yaml
python scripts/build_docx.py report.yaml --output final-report.docx
```

默认中文排版：

- 东亚字体：宋体 / SimSun；
- 拉丁字体：Times New Roman；
- 正文：10.5–11 pt；
- 行距：1.3–1.45；
- A4；
- 适度页边距；
- 标题层级不超过 3–4 级；
- 表格首行重复；
- 大章节可另起一页；
- 图表使用高清 PNG；
- 不打包或分发字体文件。

用户指定其他样式时，以用户要求为准。

### Phase 9 — Render and inspect

执行：

```bash
python scripts/qa_docx.py final-report.docx --render-dir _rendered --strict
```

逐页检查：

- 中文字体和符号是否正常；
- 是否有裁切、重叠或空白页；
- 表格是否过宽、断裂或字号过小；
- 标题是否孤立在页尾；
- 图片是否模糊、变形或超出边界；
- 页眉、页脚和页码是否一致；
- 甘特图在 100% 缩放下是否可读；
- 是否残留 TODO、TBD、占位符或工具引用标记；
- 引用、编号、数据和目录是否一致。

发现问题后修改并重新渲染，直到通过。

### Phase 10 — Deliver cleanly

默认交付：

- 最终 DOCX；
- 用户明确要求的附属图片或表格；
- 需要时提供来源台账和可再生成的 YAML；
- 一句说明已完成的主要内容。

除非用户要求，不交付内部渲染页、缓存、日志或临时 PDF。

## 7. Content schema

建议将内容建模为：

```yaml
document:
  title: ""
  subtitle: ""
  audience: ""
  purpose: ""
  language: "zh-CN"
  output_format: "docx"
  style_profile: "default-zh"

executive_summary:
  decisions: []
  priorities: []
  risks: []

sections:
  - title: ""
    purpose: ""
    blocks:
      - type: paragraph
        text: ""
      - type: bullets
        items: []
      - type: table
        headers: []
        rows: []
      - type: callout
        label: "结论"
        text: ""
      - type: image
        path: ""
        caption: ""

sources: []
appendices: []
```

完整模板见 `assets/report-content-template.yaml`。

## 8. Output recipes

根据用户要求选择，不默认全部加入：

- 战略/规划报告；
- 研究简报；
- 项目建议书；
- 可行性分析；
- 多方案对比；
- 评估或复盘报告；
- 案例分析；
- 会议纪要与行动清单；
- 白皮书；
- 路线图与实施计划。

对应章节配方见 `references/09-output-recipes.md`。

## 9. Quality gates

交付前全部通过：

### 内容

- 目的、读者和范围明确；
- 关键结论出现在前部；
- 事实与建议分开；
- 每个重要结论有证据；
- 没有未说明的重大假设；
- 建议包含责任人、时间或下一步；
- 风险和限制得到说明。

### 来源

- 易变事实已实时核验；
- 关键来源优先一手；
- 引用与正文主张匹配；
- 没有虚构来源、链接或案例；
- 来源台账包含访问日期或版本。

### 视觉

- 字体、字号、间距和颜色一致；
- 标题层级清楚；
- 表格可读；
- 图表不误导；
- 页面没有裁切、重叠、断裂或缺字；
- 逐页渲染检查完成。

### 文件

- 文件名清楚；
- 原始文件未被意外覆盖；
- 临时标记已删除；
- 元数据和敏感信息已检查；
- 最终链接可访问。

详见 `references/08-qa-and-delivery.md`。

## 10. Quick-start invocation

用户可这样调用：

```text
请使用 $professional-document-studio。

主题：____
文档类型：____
目标读者：____
核心目的：____
必须包含：____
不需要：____
需要实时检索：是 / 否
输入材料：____
输出：中文 Word
字体：宋体
图表：____
引用方式：脚注 / 尾注 / 来源表
长度：____
其他限制：____
```

若用户只写：

```text
请使用 $professional-document-studio，把这些材料整理成一份完整、专业、美观的 Word 报告。
```

则先读取材料，建立交付合同，必要时只问一个会改变结构的关键问题，然后继续。

## 11. File map

- `references/01-brief-and-scope.md`：任务合同、输入检查和缺失信息；
- `references/02-research-and-sources.md`：检索、来源台账和引用；
- `references/03-analysis-and-reasoning.md`：分析框架、决策和风险；
- `references/04-structure-and-writing.md`：信息架构、写作和编辑；
- `references/05-tool-orchestration.md`：工具路由、调用顺序、失败处理；
- `references/06-docx-design-system.md`：Word 版式系统；
- `references/07-visuals-and-timelines.md`：图表、甘特图和图片；
- `references/08-qa-and-delivery.md`：渲染、检查、隐私和交付；
- `references/09-output-recipes.md`：不同文档类型的章节配方；
- `references/10-customization-guide.md`：如何在调用时加入领域模块。

## 12. Minimal commands

```bash
# 校验任务 Brief
python scripts/validate_brief.py brief.yaml

# 生成甘特图
python scripts/render_gantt.py timeline.csv --output gantt.png --title "项目时间轴"

# 生成 Word
python scripts/build_docx.py report.yaml --output report.docx

# 渲染与检查
python scripts/qa_docx.py report.docx --render-dir _rendered --strict

# 校验 Skill 包结构
python scripts/validate_skill.py .
```
