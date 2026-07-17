---
name: sensenova
description: |
  SenseNova 多模态 AI 技能聚合入口。通过 sn-image-base（底层工具链）驱动 28 个子技能，覆盖信息图/海报生成、PPT 生成、深度研究、报告撰写、数据分析、学术/代码/金融/社交搜索、图片搜索、简历生成、风格模仿等。触发关键词：sensenova、商汤、日日新、SenseNova、信息图、infographic、PPT、演示文稿、研究报告、深度研究、deep research、数据分析、搜索、简历、resume、模仿风格、风格迁移、图片搜索、学术搜索、代码搜索、金融搜索、年报、更新技能。
  Use ONLY for SenseNova-related tasks. For general image generation use MiniMax CLI.
compatibility: Requires Python 3.10+ with httpx, pillow, python-dotenv, openai. API key configured via environment variables.
allowed-tools: Bash(pip *), Bash(python scripts/*.py *), Bash(git clone https://github.com/OpenSenseNova/SenseNova-Skills *)
---

# SenseNova Skills

聚合入口。安装后自动配置所有子 skill，按任务类型路由到对应子 skill。

## 安装

### Windows (PowerShell)
```powershell
scripts/setup.ps1
```

### macOS / Linux
```bash
bash scripts/setup.sh
```

安装流程：克隆官方 SenseNova-Skills → 复制全部 28 个 skill → 安装 Python 依赖 → 配置 API Key。

---

## 能力总览

### 1. 信息图与视觉创作（依赖 sn-image-base + sn-infographic）

| 子 Skill | 用途 |
|----------|------|
| `sn-infographic` | 信息图生成。87 种布局 × 66 种风格，自动内容分析 → 选布局/风格 → 扩写 prompt → 多轮生成 → VLM 质量审查 |
| `sn-image-imitate` | 风格模仿。给定参考图，生成风格一致但内容不同的新图 |
| `sn-image-resume` | 简历图生成。从对话内容提取信息，生成设计感简历图片 |
| `sn-image-doctor` | 环境诊断。检查 sn-image-base 安装和 API 配置是否正常 |

**触发示例：**
- "帮我生成一张 python 学习路线信息图"
- "模仿这张图的风格，内容换成无人机结构"
- "帮我生成一张简历图，我是前端工程师"

### 2. PPT 演示（依赖 sn-image-base + sn-ppt-*）

| 子 Skill | 用途 |
|----------|------|
| `sn-ppt-entry` | PPT 入口。让用户选模式：快速 / 标准 / 创意 |
| `sn-ppt-standard` | 标准/快速模式。一键生成完整 PPT（16:9 PNG 每页） |
| `sn-ppt-creative` | 创意模式。精美排版，每页独立设计 |
| `sn-ppt-doctor` | PPT 诊断。检查 PPT 相关依赖 |

**触发示例：**
- "帮我生成一份关于AI发展的PPT"
- "用创意模式做一份产品发布会PPT"

### 3. 搜索（依赖 sn-search-*）

| 子 Skill | 用途 |
|----------|------|
| `sn-search-academic` | 学术论文搜索 |
| `sn-search-code` | 代码/技术搜索 |
| `sn-search-finance` | 金融数据搜索 |
| `sn-search-image` | 图片搜索（Google 图片，需 Serper.dev API） |
| `sn-search-market-cn` | 中国市场/行业搜索 |
| `sn-search-social-cn` | 中国社交媒体搜索 |
| `sn-search-social-en` | 英文社交媒体搜索 |
| `sn-search-social-media` | 通用社交媒体搜索 |
| `sn-search-year-report` | 年报/财报搜索 |

**触发示例：**
- "搜索最近关于transformer的论文"
- "查一下最新的AI芯片行业报告"

### 4. 深度研究与报告（依赖 sn-deep-research + sn-*）

| 子 Skill | 用途 |
|----------|------|
| `sn-deep-research` | 深度研究。多轮搜索 + 分析，生成结构化研究报告 |
| `sn-research-report` | 研究报告撰写。将研究成果整理为正式报告 |
| `sn-report-format-discovery` | 报告格式发现。自动适配最佳报告格式 |
| `sn-prepare-citations` | 引用准备。格式化参考文献 |
| `sn-md-to-html-report` | Markdown 转 HTML 报告 |

**触发示例：**
- "帮我深度研究一下2025年AI市场趋势"
- "把这篇Markdown转成HTML报告"

### 5. 数据分析（依赖 sn-da-*）

| 子 Skill | 用途 |
|----------|------|
| `sn-da-excel-workflow` | Excel 工作流自动化 |
| `sn-da-image-caption` | 图片标注/说明生成 |
| `sn-da-large-file-analysis` | 大文件分析处理 |
| `sn-da-non-spreadsheet-analysis` | 非表格数据分析（PDF、文本等） |

**触发示例：**
- "分析这个Excel文件"
- "给这张图片生成说明文字"

### 6. 其他

| 子 Skill | 用途 |
|----------|------|
| `sn-update` | 更新 SenseNova Skills 到最新版本 |
| `sn-image-base` | 底层工具链（tier 0），提供 image-generate / image-recognize / text-optimize 三个基础工具 |

---

## 底层工具（sn-image-base）

所有上层 skill 通过 sn-image-base 的三个工具调用 API：

| 工具 | 用途 | 默认模型 |
|------|------|---------|
| `sn-image-generate` | 图片生成 | `sensenova-u1-fast` |
| `sn-image-recognize` | VLM 图片理解/审查 | `sensenova-6.7-flash-lite` |
| `sn-text-optimize` | LLM 文本分析/优化 | `sensenova-6.7-flash-lite` |

---

## 配置

安装脚本自动配置以下环境变量：

| 变量 | 值 |
|------|-----|
| `SN_API_KEY` | (已嵌入 setup 脚本) |
| `SN_BASE_URL` | `https://token.sensenova.cn/v1` |
| `SN_CHAT_MODEL` | `sensenova-6.7-flash-lite` |
| `SN_IMAGE_GEN_MODEL` | `sensenova-u1-fast` |
| `SN_IMAGE_GEN_MODEL_TYPE` | `sensenova` |

## 更新

运行 `sn-update` skill 或重新执行 setup 脚本。
