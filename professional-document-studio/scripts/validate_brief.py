#!/usr/bin/env python3
"""Validate a document brief YAML/JSON and report missing critical fields."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: PyYAML. Run: pip install PyYAML") from exc


PLACEHOLDER_RE = re.compile(r"^(?:\s*|todo|tbd|xx+|待补充|信息待补齐|\[.*\]|<.*>)$", re.I)


def load_data(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    data = json.loads(text) if path.suffix.lower() == ".json" else yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError("Brief top level must be a mapping")
    return data


def get_path(data: Dict[str, Any], dotted: str) -> Any:
    current: Any = data
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return bool(PLACEHOLDER_RE.match(value.strip()))
    if isinstance(value, (list, tuple, dict, set)):
        return len(value) == 0
    return False


def walk_placeholders(value: Any, path: str = "") -> Iterable[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            yield from walk_placeholders(child, child_path)
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            child_path = f"{path}[{idx}]"
            yield from walk_placeholders(child, child_path)
    elif isinstance(value, str) and value.strip() and PLACEHOLDER_RE.match(value.strip()):
        yield path


def validate(data: Dict[str, Any]) -> Dict[str, Any]:
    critical = {
        "deliverable.document_type": "文档类型",
        "deliverable.objective": "核心目的",
        "deliverable.target_audience": "目标读者",
        "deliverable.output_formats": "输出格式",
    }
    recommended = {
        "deliverable.language": "输出语言",
        "content_requirements.mandatory_sections": "必含模块",
        "inputs.local_files": "输入文件",
        "inputs.urls": "输入链接",
        "research.live_web_required": "是否需要实时研究",
        "style.east_asian_font": "中文字体",
    }

    missing_critical: List[Dict[str, str]] = []
    missing_recommended: List[Dict[str, str]] = []
    for path, label in critical.items():
        if is_empty(get_path(data, path)):
            missing_critical.append({"path": path, "label": label})
    for path, label in recommended.items():
        value = get_path(data, path)
        # Empty input files and URLs are fine if notes exist.
        if path in {"inputs.local_files", "inputs.urls"}:
            continue
        if is_empty(value):
            missing_recommended.append({"path": path, "label": label})

    inputs = data.get("inputs", {}) if isinstance(data.get("inputs"), dict) else {}
    if not any([inputs.get("local_files"), inputs.get("urls"), str(inputs.get("notes", "")).strip()]):
        missing_recommended.append({"path": "inputs", "label": "至少一种输入材料或说明"})

    placeholders = list(walk_placeholders(data))
    return {
        "valid": not missing_critical,
        "missing_critical": missing_critical,
        "missing_recommended": missing_recommended,
        "placeholder_paths": placeholders,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a document brief YAML/JSON.")
    parser.add_argument("brief", type=Path)
    parser.add_argument("--json-output", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.brief.exists():
        print(f"ERROR: brief not found: {args.brief}", file=sys.stderr)
        return 2
    try:
        result = validate(load_data(args.brief))
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    if result["valid"]:
        print("Brief validation passed.")
    else:
        print("Brief validation failed. Missing critical fields:")
        for item in result["missing_critical"]:
            print(f"- {item['path']}: {item['label']}")

    if result["missing_recommended"]:
        print("Recommended fields to review:")
        for item in result["missing_recommended"]:
            print(f"- {item['path']}: {item['label']}")
    if result["placeholder_paths"]:
        print("Placeholder-like values found:")
        for path in result["placeholder_paths"]:
            print(f"- {path}")

    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
