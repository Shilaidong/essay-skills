---
name: grok-cli
description: 个人专用的 Grok 文生图命令行工具（grok-cli），对接自用 Grok2API 中继站，Key 已内置仅供本机使用。当用户需要 Grok 生图能力时自动调用：生成图片、文生图、画一张图、画图、绘图、画一张、帮我画、生成图像、做张图、图片生成。注意：仅本机个人使用，不与他人共享。
compatibility: 需要 Node.js 18+（自带 fetch），本机可用。
allowed-tools: Bash(grok-cli *)
---

# grok-cli — Grok 文生图

通过 `scripts/grok-cli` 调用自用 Grok2API 中继站生成图片。API Key 已内置在 `scripts/config.json`，仅供本机个人使用。

## 用法

```bash
grok-cli "一只雪地里的红狐狸，数字艺术"
grok-cli image "赛博朋克城市夜景" --model quality --size 1024x1024 --count 2
```

描述可以是任意自然语言，中文英文均可。`image` 子命令可省略。

## 参数

| 参数 | 说明 |
|------|------|
| `--model image|quality|lite|2.0` | 图片模型，默认 `image`；`quality` 质量更高、`lite` 更快 |
| `--size 1024x1024` | 尺寸 |
| `--count n` | 一次生成 n 张 |
| `--out <目录>` | 输出目录，默认 `./grok-output/` |
| `--json` | 输出完整 JSON（调试用） |

## 输出

图片自动下载到 `./grok-output/`（可用环境变量 `GROK_OUT_DIR` 覆盖），文件名含提示词和时间戳。命令会打印保存路径。

## 注意事项

- **Key 内置，仅本机个人使用**：`config.json` 内含 API Key，不要把该文件或本 Skill 目录外传/分享。
- 上游偶尔超时（Cloudflare 524），脚本会自动重试一次。
- 报错信息来自服务端原样透传（如配额用尽、模型不可用等）。
