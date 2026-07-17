---
name: infographic-generation
description: |
  使用 SenseNova U1 Fast 模型生成信息图（Infographics）。适用于海报、知识卡片、菜谱、简历、演示文稿、数据可视化等含文字的高密度视觉布局。触发关键词：信息图、infographic、海报、知识卡片、菜谱图、简历图、信息图表、图文排版、视觉布局。不要用于普通图片生成（用 MiniMax 的 mmx image）。
compatibility: Requires Python with `openai` and `requests` packages, and a Sensenova API key from platform.sensenova.cn.
allowed-tools: Bash(python scripts/generate.py *)
---

# Infographic Generation

使用 SenseNova U1 Fast 模型生成高质量信息图（Infographics）。

## 前置条件

```bash
pip install openai requests
```

API Key 需设置环境变量 `SENSENOVA_API_KEY`，或在 `scripts/generate.py` 中直接填入。

## 使用方法

```bash
python scripts/generate.py --prompt "<信息图描述>" --output "<输出文件>"
```

### 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--prompt` | 信息图描述（必填） | - |
| `--output` | 输出文件路径 | `infographic.png` |
| `--size` | 图片尺寸 | `2752x1536` |

## Prompt 编写指南

信息图生成的关键是详细的 prompt。建议包含以下要素：

1. **风格**：清新明亮 / 深色科技 / 手绘扁平 / 工程蓝图 / 国风水墨
2. **布局**：垂直分层 / 中心辐射 / 左右分栏 / 横向爆炸分解
3. **配色**：指定主色调和点缀色
4. **内容结构**：各级标题、文本、数据
5. **背景**：渐变 / 网格 / 纹理 / 纯色

### 示例

```
生成一张"超级水果：柠檬万能指南"信息图。
风格：清新明亮的青绿色渐变背景，点缀白色星星、气泡和云朵元素，扁平化卡通插画风格
布局：垂直分层结构
配色：青绿渐变主色，白色点缀
内容：
  LEVEL 0: 营养核心 - 柠檬是维生素C的发电站...
  LEVEL 1: 烹饪艺术 - 去腥增鲜...
  LEVEL 2: 家居清洁 - 天然去污...
```

## API 说明

- Endpoint: `POST /v1/images/generations`
- Model: `sensenova-u1-fast`
- Base URL: `https://token.sensenova.cn/v1`
- Auth: Bearer token in `Authorization` header
