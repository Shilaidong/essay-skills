# Professional Document Studio

一个面向 **Codex、OpenCode 及兼容 Agent Skills 的通用文档生产 Skill**。

它不预设任何行业、主题、对象或固定方案结构。每次调用时，用户单独说明主题和必含模块；Skill 负责标准化地完成：

```text
资料盘点
→ 必要研究
→ 来源核验
→ 分析与结构
→ 专业写作
→ 表格 / 图表 / 甘特图
→ DOCX 排版
→ 逐页渲染检查
→ 文件交付
```

## 适用场景

- 战略与规划报告；
- 研究简报与白皮书；
- 项目建议书和可行性分析；
- 多方案比较；
- 案例分析；
- 评估、复盘和会议纪要；
- 将笔记、网页、PDF、表格和已有 Word 重构为正式文档；
- 需要宋体 Word、来源台账、图表或甘特图的任务。

具体业务内容由调用者提供，不写死在 Skill 内。

## 目录

```text
professional-document-studio/
├── SKILL.md
├── README.md
├── LICENSE
├── requirements.txt
├── manifest.txt
├── agents/
│   └── openai.yaml
├── references/
│   ├── 01-brief-and-scope.md
│   ├── 02-research-and-sources.md
│   ├── 03-analysis-and-reasoning.md
│   ├── 04-structure-and-writing.md
│   ├── 05-tool-orchestration.md
│   ├── 06-docx-design-system.md
│   ├── 07-visuals-and-timelines.md
│   ├── 08-qa-and-delivery.md
│   ├── 09-output-recipes.md
│   └── 10-customization-guide.md
├── scripts/
│   ├── validate_skill.py
│   ├── validate_brief.py
│   ├── render_gantt.py
│   ├── build_docx.py
│   └── qa_docx.py
├── assets/
│   ├── document-brief-template.yaml
│   ├── report-content-template.yaml
│   ├── source-ledger-template.csv
│   ├── timeline-template.csv
│   ├── style-config-template.yaml
│   └── AGENTS-snippet.md
└── examples/
    ├── sample-brief.yaml
    ├── sample-report.yaml
    ├── sample-timeline.csv
    ├── sample-gantt.png
    └── sample-report.docx
```

## 安装

### Codex

项目级：

```bash
mkdir -p .agents/skills
cp -R professional-document-studio .agents/skills/
```

用户级：

```bash
mkdir -p ~/.agents/skills
cp -R professional-document-studio ~/.agents/skills/
```

Codex 会按需加载 `SKILL.md`；可在提示词中显式写：

```text
$professional-document-studio
```

官方说明：<https://developers.openai.com/codex/skills>

### OpenCode

项目级可放：

```bash
mkdir -p .opencode/skills
cp -R professional-document-studio .opencode/skills/
```

也可复用通用路径：

```bash
mkdir -p .agents/skills
cp -R professional-document-studio .agents/skills/
```

用户级：

```bash
mkdir -p ~/.config/opencode/skills
cp -R professional-document-studio ~/.config/opencode/skills/
```

官方说明：<https://opencode.ai/docs/skills/>

## 依赖

```bash
python -m pip install -r requirements.txt
```

核心 Python 依赖：

- `python-docx`
- `PyYAML`
- `Pillow`
- `matplotlib`

Word 视觉 QA 建议安装：

- LibreOffice / `soffice`
- Poppler / `pdftoppm`

本包不会附带或分发字体文件。Word 样式可以指定宋体；本机没有宋体时，渲染器可能使用可用 CJK 字体替代。

## 最简使用

```text
请使用 $professional-document-studio。

主题：某项目年度战略规划
文档类型：战略报告
目标读者：管理层
核心目的：确定未来12个月优先级和资源投入
必须包含：现状、三个方案、比较矩阵、推荐、预算、风险、甘特图
输入材料：notes.md、data.xlsx、两份PDF
需要实时检索：是，只用官方和原始来源
输出：中文 Word
字体：宋体
附属文件：来源台账CSV、甘特图PNG、可再生成YAML
```

Skill 会把“多个方案、案例、时间轴或其他专题模块”视为本次任务要求，而不是默认模板的一部分。

## 结构化工作流

### 1. 复制 Brief

```bash
cp assets/document-brief-template.yaml brief.yaml
python scripts/validate_brief.py brief.yaml
```

### 2. 维护来源台账

```bash
cp assets/source-ledger-template.csv sources.csv
```

对易变事实记录来源、核验日期、适用周期和重新核验要求。

### 3. 生成甘特图

```bash
cp assets/timeline-template.csv timeline.csv
python scripts/render_gantt.py timeline.csv \
  --output gantt.png \
  --title "项目时间轴"
```

### 4. 生成 Word

```bash
cp assets/report-content-template.yaml report.yaml
python scripts/build_docx.py report.yaml \
  --output report.docx
```

### 5. 渲染与检查

```bash
python scripts/qa_docx.py report.docx \
  --render-dir _rendered \
  --json-output qa-report.json \
  --strict
```

必须查看：

- `_rendered/contact-sheet.png`
- 每张 `page-*.png`

脚本只能准备 QA，不能替代逐页视觉判断。

### 6. 校验 Skill

```bash
python scripts/validate_skill.py .
```

## 工具使用特点

`SKILL.md` 使用能力导向的工具路由，而不是把某个平台的工具名写死：

- 当前事实：Web 搜索和官方页面；
- 私有材料：对应连接器或 MCP；
- PDF 文字：优先原生解析；
- PDF 图表：页面渲染；
- 数据图表：Python；
- 甘特图：可复现脚本；
- DOCX：结构化生成；
- 版式：渲染为 PNG 后逐页检查。

这使其可在 Codex、OpenCode 或其他兼容 Agent 环境中迁移。

## 设计原则

- 结论前置；
- 事实、推断、建议、目标和假设分开；
- 每项重要建议有证据链、行动和风险；
- 视觉元素必须服务信息；
- 不伪造来源、案例或结果；
- 不把网站、浏览量或头衔自动当作影响力；
- 不把 Mermaid 代码直接放进 Word；
- DOCX 未通过渲染检查不得交付。

## 版本

- `2.0.0`：重构为通用专业文档 Skill；删除所有案例专属业务结构；强化工具路由、研究、DOCX、视觉与 QA。
