---
name: qwen-image-lan
description: 通用 agent skill：通过 HTTP 调用局域网 Qwen-Image-2.1 出图服务器（RTX 5080）生成写实/概念图/产品图。当用户要求生成图片、批量出图（变体、对比组），或提到"局域网出图"、"调用本机 GPU"、"qi21" 时自动调用。服务端 IP/Token 见本目录 qwen_image_lan_config.json。
whenToUse: 用户要求生成图片（写实、概念图、产品图等）；需要批量出图（5 个变体、对比组）；用户提到"局域网出图"、"调用本机 GPU"、"qi21"。
allowed-tools: Bash(curl *), Bash(python3 *)
---

# qwen-image-lan — Qwen-Image-2.1 局域网出图调用

> 通用 agent skill：通过 HTTP 调用局域网 Qwen-Image-2.1 出图服务器。
> 服务端跑在带 RTX 5080 的机器上（IP/Token 在 `qwen_image_lan_config.json`）。
> 调用端是任何能发 HTTP 请求的环境（agent / 脚本 / 其他机器的 agent）。

## 何时使用

- 用户要求生成图片（写实、概念图、产品图等）
- 需要批量出图（5 个变体、对比组）
- 用户提到"局域网出图"、"调用本机 GPU"、"qi21"

## 调用方式（任何 agent 都用同一套）

读取本目录的 `qwen_image_lan_config.json` 拿到 `base_url`（默认 `http://<server_ip>:18765`）和 `token`，然后：

```http
POST {base_url}/v1/generate
Authorization: Bearer {token}
Content-Type: application/json

{
  "prompt": "...",        // 必填，英文为主
  "width": 1024,           // 默认 1024，最大 2048
  "height": 1024,
  "steps": 40,             // 默认 40
  "seed": 42               // -1 表示随机
}
```

返回：

```json
{
  "job_id": "...",
  "image_b64": "iVBOR...",
  "elapsed_sec": 102.1,
  ...
}
```

把 `image_b64` base64 解码即得 PNG。落盘由调用端决定。

## 健康检查（先 ping 再生成，避免冷启动阻塞调用端）

```http
GET {base_url}/health
```

返回 `warm: true/false`、`queue_size`、`running`。

## 客户端实现（参考）

直接调本目录的 `qwen_image_lan_client.py`（路径 `~/.agents/skills/qwen-image-lan/qwen_image_lan_client.py`，可 `import` 或复制逻辑）：

```python
from qwen_image_lan_client import generate, health
print(health())                              # 检查服务
result = generate(prompt="...", width=1024,  # 出图
                  height=1024, steps=40,
                  seed=42, out_path="out.png")
print(f"saved {result['out_path']} ({result['elapsed_sec']}s)")
```

## 错误码

| 状态码 | 含义 | 处理 |
|---|---|---|
| 401 | 没带 token | 读 config 补上 |
| 403 | token 错 | 重新读 config（可能改了） |
| 503 | 服务没起 / 冷启动 | 等几秒重试 / 提示用户启动 |
| 500 | 服务端 OOM | 降分辨率或步数 |

## 性能预期（RTX 5080 17GB VRAM）

- 1024² × 40 步 ≈ 100-110 秒（首张含冷启动 +20 秒）
- 2048² × 40 步 ≈ 5-8 分钟（建议先 1024 验证 prompt）
- 单卡同时只能跑一张，调用端可以并发请求，服务器自动排队

## 不该做的事

- ❌ 不要发 4K+ 分辨率（会 OOM）
- ❌ 不要把图片存到调用端之外的地方（服务器只返回 base64）
- ❌ 不要泄露 token 到日志或对话中
