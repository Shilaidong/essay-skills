#!/usr/bin/env python3
"""Inspect raw assessment JSON exports and report useful structure signals."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


LIKERT_VALUES = {1, 2, 3, 4, 5}
TEXT_KEYS = {"content", "message", "text", "summary", "description", "quote", "value"}
STRUCTURE_KEYS = {
    "answers",
    "responses",
    "scores",
    "chapters",
    "keyMoments",
    "futureScript",
    "messages",
    "sessions",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def maybe_nested_json(value: str) -> Any | None:
    s = value.strip()
    if len(s) < 2 or s[0] not in "[{" or s[-1] not in "]}":
        return None
    try:
        return json.loads(s)
    except Exception:
        return None


def is_likert_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and int(value) == value and int(value) in LIKERT_VALUES


def summarize_likert(values: list[Any]) -> dict[str, Any] | None:
    if len(values) < 10 or not all(is_likert_number(v) for v in values):
        return None
    ints = [int(v) for v in values]
    counts = dict(sorted(Counter(ints).items()))
    return {
        "n": len(ints),
        "uniform": len(counts) == 1,
        "counts": counts,
    }


def inspect_node(
    node: Any,
    path: str,
    result: dict[str, Any],
    depth: int = 0,
    max_depth: int = 18,
) -> None:
    if depth > max_depth:
        return

    if isinstance(node, dict):
        keys = list(node.keys())
        if any(k in STRUCTURE_KEYS for k in keys):
            result["structure_hits"].append({"path": path, "keys": [k for k in keys if k in STRUCTURE_KEYS]})

        numeric_values = list(node.values())
        likert = summarize_likert(numeric_values)
        if likert:
            result["likert_blocks"].append({"path": path, **likert})

        for key, value in node.items():
            child_path = f"{path}.{key}" if path else str(key)
            if isinstance(value, str):
                collect_string(key, value, child_path, result)
                nested = maybe_nested_json(value)
                if nested is not None:
                    result["nested_json_strings"].append(child_path)
                    inspect_node(nested, child_path + ".__json__", result, depth + 1, max_depth)
            else:
                inspect_node(value, child_path, result, depth + 1, max_depth)
        return

    if isinstance(node, list):
        likert = summarize_likert(node)
        if likert:
            result["likert_blocks"].append({"path": path, **likert})
        for index, value in enumerate(node[:500]):
            child_path = f"{path}[{index}]"
            if isinstance(value, str):
                collect_string("", value, child_path, result)
                nested = maybe_nested_json(value)
                if nested is not None:
                    result["nested_json_strings"].append(child_path)
                    inspect_node(nested, child_path + ".__json__", result, depth + 1, max_depth)
            else:
                inspect_node(value, child_path, result, depth + 1, max_depth)


def collect_string(key: str, value: str, path: str, result: dict[str, Any]) -> None:
    stripped = value.strip()
    if not stripped:
        result["empty_strings"] += 1
        return
    if len(stripped) <= 2 and stripped in {"1", "0", "-", "na", "NA"}:
        result["sparse_strings"].append({"path": path, "value": stripped})
    if len(stripped) >= 20 or key in TEXT_KEYS:
        result["long_text"].append({"path": path, "chars": len(stripped), "sample": stripped[:180]})


def inspect_file(path: Path) -> dict[str, Any]:
    data = load_json(path)
    result: dict[str, Any] = {
        "file": str(path),
        "top_type": type(data).__name__,
        "top_keys": list(data.keys())[:50] if isinstance(data, dict) else [],
        "structure_hits": [],
        "nested_json_strings": [],
        "likert_blocks": [],
        "long_text": [],
        "sparse_strings": [],
        "empty_strings": 0,
    }
    inspect_node(data, "", result)
    return result


def render_markdown(results: list[dict[str, Any]]) -> str:
    lines: list[str] = ["# Assessment JSON Audit", ""]
    for item in results:
        lines += [
            f"## {item['file']}",
            "",
            f"- Top type: `{item['top_type']}`",
            f"- Top keys: {', '.join(map(str, item['top_keys'])) if item['top_keys'] else '(none)'}",
            f"- Nested JSON strings: {len(item['nested_json_strings'])}",
            f"- Likert-like blocks: {len(item['likert_blocks'])}",
            f"- Long text fields: {len(item['long_text'])}",
            f"- Sparse short strings: {len(item['sparse_strings'])}",
            "",
        ]
        if item["likert_blocks"]:
            lines += ["### Likert-like blocks", ""]
            for block in item["likert_blocks"][:20]:
                warning = " UNIFORM" if block["uniform"] else ""
                lines.append(f"- `{block['path']}` n={block['n']} counts={block['counts']}{warning}")
            lines.append("")
        if item["structure_hits"]:
            lines += ["### Structure hits", ""]
            for hit in item["structure_hits"][:30]:
                lines.append(f"- `{hit['path']}` keys={hit['keys']}")
            lines.append("")
        if item["nested_json_strings"]:
            lines += ["### Nested JSON strings", ""]
            for p in item["nested_json_strings"][:20]:
                lines.append(f"- `{p}`")
            lines.append("")
        if item["long_text"]:
            lines += ["### Long text samples", ""]
            for text in item["long_text"][:25]:
                sample = text["sample"].replace("\n", " ")
                lines.append(f"- `{text['path']}` ({text['chars']} chars): {sample}")
            lines.append("")
        if item["sparse_strings"]:
            lines += ["### Sparse strings", ""]
            for sparse in item["sparse_strings"][:25]:
                lines.append(f"- `{sparse['path']}` = {sparse['value']!r}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect raw assessment JSON files.")
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--out", type=Path, help="Write the audit to this file.")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    results = [inspect_file(path) for path in args.files]
    if args.format == "json":
        output = json.dumps(results, ensure_ascii=False, indent=2)
    else:
        output = render_markdown(results)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
