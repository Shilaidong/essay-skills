---
name: sensenova
description: |
  SenseNova 多模态 AI 技能聚合入口。涵盖信息图/海报/简历/风格模仿等视觉生成、深度研究与报告撰写、文档转换。所有子 skill 由 sn-image-base 底层工具链驱动。触发关键词：sensenova、商汤、日日新、信息图、infographic、研究报告、深度研究、简历、模仿风格。
compatibility: Requires Python 3.10+ with httpx, pillow, python-dotenv, openai. API key configured via environment variables.
allowed-tools: Bash(pip *)
---

# SenseNova Skills

聚合入口。安装后按任务类型路由到对应子 skill。

## 安装

### Windows
```powershell
setup.ps1
```
### macOS / Linux
```bash
bash setup.sh
```

---

## 体系架构

```
sn-image-base (tier 0 底层)
├── sn-image-generate   → 图片生成 (sensenova-u1-fast)
├── sn-text-optimize    → 文本分析 (sensenova-6.7-flash-lite)
└── sn-image-recognize  → 图片理解/审查 (sensenova-6.7-flash-lite)

tier 1 场景 skill：
├── 视觉创作
│   ├── sn-infographic      → 信息图生成
│   ├── sn-image-imitate    → 风格模仿
│   └── sn-image-resume     → 简历图生成
├── 深度研究
│   ├── sn-deep-research         → 多 agent 深度研究
│   ├── sn-report-format-discovery → 报告格式发现
│   └── sn-prepare-citations     → 引用处理
└── 文档工具
    └── sn-md-to-html-report    → Markdown 转 HTML 报告
```

## 路由规则

| 用户需求 | 子 skill |
|----------|---------|
| 信息图/海报/知识卡片/菜谱图 | `sn-infographic` |
| 模仿风格/风格迁移 | `sn-image-imitate` |
| 简历图 | `sn-image-resume` |
| 深度研究/调研/行业分析 | `sn-deep-research` |
| 研究报告撰写/格式 | `sn-report-format-discovery` |
| 引用格式化/参考文献 | `sn-prepare-citations` |
| Markdown 转 HTML 报告 | `sn-md-to-html-report` |
| 普通图片生成 | MiniMax CLI (`mmx image`) |
| 通用搜索 | Tavily CLI (`tvly search`) |
