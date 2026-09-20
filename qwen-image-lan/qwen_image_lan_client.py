"""通用 HTTP 客户端：调用局域网 Qwen-Image-2.1 出图（qwen-image-lan）。

任何 agent / 脚本只要能 import 这个文件（或直接复制逻辑）就能用：
    从 qwen_image_lan_client 加载 generate / health 即可
依赖：仅标准库（无外部包要求）。
"""
import base64
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

_SKILL_DIR = Path(__file__).parent
_CONFIG_PATH = _SKILL_DIR / "qwen_image_lan_config.json"


def _load_config():
    """从 qwen_image_lan_config.json 读 base_url + token。允许环境变量覆盖：
    QWEN_IMAGE_LAN_BASE_URL / QWEN_IMAGE_LAN_TOKEN。
    这样不同机器上只需要换环境变量，无需改文件。"""
    base_url = os.environ.get("QWEN_IMAGE_LAN_BASE_URL")
    token = os.environ.get("QWEN_IMAGE_LAN_TOKEN")
    if base_url and token:
        return base_url.rstrip("/"), token
    if _CONFIG_PATH.exists():
        cfg = json.loads(_CONFIG_PATH.read_text(encoding="utf-8-sig"))
        return cfg["base_url"].rstrip("/"), cfg["token"]
    raise FileNotFoundError(
        f"qwen-image-lan config not found at {_CONFIG_PATH}; "
        "set QWEN_IMAGE_LAN_BASE_URL + QWEN_IMAGE_LAN_TOKEN env vars, "
        "or copy qwen_image_lan_config.example.json"
    )


def _post_json(url, payload, token, timeout=600):
    req = urllib.request.Request(
        url, method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        data=json.dumps(payload).encode("utf-8"),
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"connection failed: {e.reason}")


def health(base_url=None, token=None):
    base_url, token = base_url or _load_config()[0], token or _load_config()[1]
    req = urllib.request.Request(f"{base_url}/health")
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode("utf-8"))


def generate(prompt, width=1024, height=1024, steps=40, seed=42,
             image_b64=None, rgba=False,
             out_path=None, base_url=None, token=None):
    """出图。out_path 不传就只返回 dict（含 image_b64）；传了自动落盘 PNG。"""
    base_url, token = base_url or _load_config()[0], token or _load_config()[1]
    payload = dict(prompt=prompt, width=width, height=height,
                   steps=steps, seed=seed, image_b64=image_b64, rgba=rgba)
    t0 = time.time()
    result = _post_json(f"{base_url}/v1/generate", payload, token)
    result["round_trip_sec"] = round(time.time() - t0, 2)
    if out_path:
        Path(out_path).write_bytes(base64.b64decode(result["image_b64"]))
        result["out_path"] = str(out_path)
    return result


if __name__ == "__main__":
    # 简单自测：先健康检查再出 1 张 512² 测试图
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", default="A cute cat wearing sunglasses, pop art style")
    ap.add_argument("--out", default="qwen_image_lan_out.png")
    ap.add_argument("--w", type=int, default=512)
    ap.add_argument("--h", type=int, default=512)
    ap.add_argument("--steps", type=int, default=20)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    print("health:", health())
    r = generate(args.prompt, args.w, args.h, args.steps, args.seed, out_path=args.out)
    print(f"saved {r.get('out_path')} elapsed={r['elapsed_sec']}s round_trip={r['round_trip_sec']}s")