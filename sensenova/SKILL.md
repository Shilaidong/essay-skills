---
name: sensenova
description: |
  SenseNova 多模态 AI 技能聚合入口。涵盖信息图/海报/简历/风格模仿等视觉生成、PPT 演示、深度研究与报告撰写、Excel/图片/大文件数据分析、学术/代码/金融/社交/年报等多维度搜索。所有 sn-* 子 skill 由 sn-image-base 底层工具链驱动。触发关键词：sensenova、商汤、日日新、SenseNova、信息图、infographic、PPT、演示文稿、研究报告、深度研究、数据分析、搜索、简历、模仿风格。普通图片生成走 MiniMax CLI。
compatibility: Requires Python 3.10+ with httpx, pillow, python-dotenv, openai. API key configured via environment variables.
allowed-tools: Bash(pip *), Bash(python scripts/*.py *), Bash(git clone https://github.com/OpenSenseNova/SenseNova-Skills *)
---

# SenseNova Skills

聚合入口。安装后按任务类型路由到对应子 skill。

**子 skill 是动态发现的** — 每次用到时先扫描 skills 目录下已安装的 `sn-*` skill，根据任务匹配最合适的那个。官方新增 skill 后重新跑 setup 即可自动纳入。

## 安装

### Windows
```powershell
scripts/setup.ps1
```
### macOS / Linux
```bash
bash scripts/setup.sh
```

流程：克隆官方仓库 → 复制所有 sn-* skill → 安装 Python 依赖 → 配置 API Key。

## 更新

重新跑 setup 脚本，或直接说"更新 SenseNova skills"。

---

## 体系架构

```
sn-image-base (tier 0 底层)
├── sn-image-generate   → 图片生成 (sensenova-u1-fast)
├── sn-text-optimize    → 文本分析 (sensenova-6.7-flash-lite)
└── sn-image-recognize  → 图片理解/审查 (sensenova-6.7-flash-lite)

tier 1 场景 skill（按需调用以上工具）：
├── 视觉创作  → sn-infographic, sn-image-imitate, sn-image-resume
├── PPT       → sn-ppt-entry → sn-ppt-standard / sn-ppt-creative
├── 搜索      → sn-search-academic, -code, -finance, -social-*, -market-*, -year-report
├── 深度研究  → sn-deep-research, sn-research-report, sn-report-format-discovery
├── 数据分析  → sn-da-excel-workflow, -image-caption, -large-file, -non-spreadsheet
├── 文档工具  → sn-md-to-html-report, sn-prepare-citations
└── 诊断与更新 → sn-image-doctor, sn-ppt-doctor, sn-update
```

## 路由规则

当用户提出需求时，按以下优先级匹配：

| 用户需求 | 匹配 skill |
|----------|-----------|
| 信息图/海报/知识卡片/菜谱图 | 扫描是否有 `sn-infographic` |
| 模仿风格/风格迁移 | 扫描是否有 `sn-image-imitate` |
| 简历图 | 扫描是否有 `sn-image-resume` |
| PPT/演示文稿 | 扫描是否有 `sn-ppt-entry` |
| 深度研究/调研/行业分析 | 扫描是否有 `sn-deep-research` |
| 学术论文搜索 | 扫描是否有 `sn-search-academic` |
| 代码/GitHub/HuggingFace 搜索 | 扫描是否有 `sn-search-code` |
| 金融/股票/年报搜索 | 扫描是否有 `sn-search-finance` |
| Excel/数据清洗/统计分析 | 扫描是否有 `sn-da-excel-workflow` |
| 图片标注/提取图片数据 | 扫描是否有 `sn-da-image-caption` |
| 大文件/大数据量 Excel | 扫描是否有 `sn-da-large-file-analysis` |
| Word/PDF/PPT 文档分析 | 扫描是否有 `sn-da-non-spreadsheet-analysis` |
| 更新 SenseNova skills | 扫描是否有 `sn-update` |
| 普通图片生成 | 走 MiniMax CLI (`mmx image`) |
| 通用搜索 | 走 Tavily CLI (`tvly search`) |

> 扫描不到对应 skill 时，回退到通用能力处理。
