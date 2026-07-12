#!/usr/bin/env python3
"""Inspect raw assessment JSON exports and report useful structure signals.

Pass `--lifeecho` to enable LifeEcho specialization: detect the raw-export
shape from the LifeEcho app, score-verify Big Five (IPIP-50), and surface
life-story chapters / 8 key moments / future-script contents found in the
`role: "system"` message inside `messages_by_module["life-story"]`.

Generic behavior (no flag) is unchanged from the original implementation.
"""

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

# --- LifeEcho-specific knowledge ---
LIFEECHO_BIG_FIVE_FACTORS = (
    "openness",
    "conscientiousness",
    "extraversion",
    "agreeableness",
    "neuroticism",
)

# IPIP item ids that are reverse-scored (1-indexed, per upstream test/page.tsx).
LIFEECHO_IPIP_REVERSE_IDS = {6, 7, 8, 9, 10, 16, 17, 18, 19, 20, 26, 27, 28, 29, 30,
                             36, 37, 38, 39, 40, 46, 47, 48, 49, 50}

LIFEECHO_KEY_MOMENT_TYPES = (
    "high_point",
    "low_point",
    "turning_point",
    "childhood_positive",
    "childhood_negative",
    "wisdom_event",
    "challenge",
    "coping",
)


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


# ---------- LifeEcho helpers ----------

def looks_like_lifeecho(data: Any) -> bool:
    """Return True when the JSON shape matches a LifeEcho raw-data export."""
    if not isinstance(data, dict):
        return False
    keys = set(data.keys())
    return {"client", "assessment_session", "interview_modules", "messages_by_module"}.issubset(keys)


def detect_lifeecho(data: Any) -> dict[str, Any]:
    """Return LifeEcho-specific structural findings for the audit report."""
    info: dict[str, Any] = {"detected": False}

    if not isinstance(data, dict):
        return info

    info["detected"] = looks_like_lifeecho(data)
    if not info["detected"]:
        return info

    # Modules present
    modules = data.get("interview_modules") or []
    info["module_types"] = sorted({
        m.get("module_type") for m in modules
        if isinstance(m, dict) and m.get("module_type")
    })

    # Big Five presence + reverse-score verification
    pt = data.get("personality_test")
    info["personality_test_present"] = pt is not None
    info["big_five_factors"] = {}
    info["big_five_mismatch"] = []
    if isinstance(pt, dict):
        scores = pt.get("scores") or {}
        answers = pt.get("answers") or {}
        recalculated = recalc_big_five(answers)
        for factor in LIFEECHO_BIG_FIVE_FACTORS:
            value = scores.get(factor)
            info["big_five_factors"][factor] = {
                "value": value,
                "level": level_tag(value),
                "recalculated": recalculated.get(factor),
            }
            if isinstance(value, int) and recalculated.get(factor) is not None:
                if abs(value - recalculated[factor]) > 1:
                    info["big_five_mismatch"].append({
                        "factor": factor,
                        "stored": value,
                        "recalculated": recalculated[factor],
                    })

    # Life-story structured data
    life_story = extract_life_story(data)
    if life_story:
        chapters = life_story.get("chapters") or []
        moments = life_story.get("keyMoments") or {}
        future = life_story.get("futureScript") or {}
        info["life_story"] = {
            "chapter_count": len(chapters),
            "chapter_count_ok": 2 <= len(chapters) <= 7,
            "chapter_titles": [
                (c.get("title") or "(未命名)") for c in chapters if isinstance(c, dict)
            ],
            "moments_present": sorted(moments.keys()),
            "moments_filled": sorted(
                k for k, v in moments.items()
                if isinstance(v, dict) and (v.get("title") or v.get("description"))
            ),
            "future_script_present": bool(
                future.get("dreams") or future.get("hopes") or future.get("life_projects")
            ),
        }

    # Module message counts
    counts: dict[str, int] = {}
    grouped = data.get("messages_by_module") or {}
    if isinstance(grouped, dict):
        # group messages by parent module's type via interview_modules lookup
        module_id_to_type = {
            m.get("id"): m.get("module_type")
            for m in modules
            if isinstance(m, dict) and m.get("id")
        }
        for module_id, msgs in grouped.items():
            t = module_id_to_type.get(module_id, module_id)
            counts[str(t)] = len(msgs) if isinstance(msgs, list) else 0
    info["module_message_counts"] = counts

    return info


def recalc_big_five(answers: Any) -> dict[str, int]:
    """Re-derive the Big Five factor sums from raw IPIP-50 answers."""
    out: dict[str, int] = {f: 0 for f in LIFEECHO_BIG_FIVE_FACTORS}
    if not isinstance(answers, dict):
        return out
    for key, raw in answers.items():
        try:
            qid = int(key)
        except (TypeError, ValueError):
            continue
        if not (1 <= qid <= 50):
            continue
        if not is_likert_number(raw):
            continue
        score = int(raw)
        if qid in LIFEECHO_IPIP_REVERSE_IDS:
            score = 6 - score
        # Factor mapping by qid range
        if 1 <= qid <= 10:
            factor = "openness"
        elif 11 <= qid <= 20:
            factor = "conscientiousness"
        elif 21 <= qid <= 30:
            factor = "extraversion"
        elif 31 <= qid <= 40:
            factor = "agreeableness"
        else:
            factor = "neuroticism"
        out[factor] += score
    return out


def level_tag(value: Any) -> str:
    """LifeEcho Big Five level label."""
    if not isinstance(value, int):
        return "未知"
    if value >= 35:
        return "高"
    if value >= 25:
        return "中等"
    return "低"


def extract_life_story(data: Any) -> dict[str, Any] | None:
    """Find the structured life-story payload stored inside a system message."""
    if not isinstance(data, dict):
        return None
    modules = data.get("interview_modules") or []
    target_id = None
    for m in modules:
        if isinstance(m, dict) and m.get("module_type") == "life-story":
            target_id = m.get("id")
            break
    if not target_id:
        return None
    grouped = data.get("messages_by_module") or {}
    msgs = grouped.get(target_id) or []
    for msg in msgs:
        if not isinstance(msg, dict):
            continue
        if msg.get("role") == "system":
            content = msg.get("content")
            if isinstance(content, str):
                try:
                    parsed = json.loads(content)
                    if isinstance(parsed, dict):
                        return parsed
                except Exception:
                    return None
    return None


# ---------- Rendering ----------


def render_markdown(results: list[dict[str, Any]], lifeecho_results: list[dict[str, Any]] | None = None) -> str:
    lines: list[str] = ["# Assessment JSON Audit", ""]
    for idx, item in enumerate(results):
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
        if lifeecho_results and idx < len(lifeecho_results) and lifeecho_results[idx].get("detected"):
            lines += render_lifeecho_section(lifeecho_results[idx])
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


def render_lifeecho_section(info: dict[str, Any]) -> list[str]:
    lines = ["### LifeEcho specialization", ""]
    if not info["detected"]:
        lines.append("- Shape does not match a LifeEcho raw-data export; skipping specialized checks.")
        lines.append("")
        return lines

    lines.append(f"- Detected: yes (client + session + interview_modules + messages_by_module)")
    if info.get("module_types"):
        lines.append(f"- Module types: {', '.join(info['module_types'])}")
    if info.get("module_message_counts"):
        lines.append("- Module message counts:")
        for k, v in sorted(info["module_message_counts"].items()):
            lines.append(f"  - `{k}`: {v}")
    lines.append("")

    if info["personality_test_present"]:
        lines.append("#### Big Five (IPIP-50) verification")
        lines.append("")
        lines.append("| Factor | Stored | Level | Recalculated | OK |")
        lines.append("| --- | --- | --- | --- | --- |")
        for factor, blob in info["big_five_factors"].items():
            stored = blob["value"]
            level = blob["level"]
            recalc = blob["recalculated"]
            mismatched = any(m["factor"] == factor for m in info["big_five_mismatch"])
            ok = "✅" if not mismatched and stored is not None else ("⚠️" if mismatched else "—")
            lines.append(f"| {factor} | {stored if stored is not None else '(none)'} | {level} | {recalc if recalc is not None else '(n/a)'} | {ok} |")
        lines.append("")
        if info["big_five_mismatch"]:
            lines.append("**Recalculation mismatch**: stored scores deviate from IPIP-50 reverse scoring by more than 1.")
            for m in info["big_five_mismatch"]:
                lines.append(f"- {m['factor']}: stored={m['stored']} recalc={m['recalculated']}")
            lines.append("")
    else:
        lines.append("- Big Five test not present (no `personality_test` block).")
        lines.append("")

    if info.get("life_story"):
        ls = info["life_story"]
        lines.append("#### 第二人生模型 — life-story payload")
        lines.append("")
        badge = "✅" if ls["chapter_count_ok"] else "⚠️"
        lines.append(f"- Chapters: {ls['chapter_count']} ({badge} expected 2–7)")
        if ls["chapter_titles"]:
            for i, title in enumerate(ls["chapter_titles"], 1):
                lines.append(f"  - 第{i}章: {title}")
        else:
            lines.append("  - (no chapter titles captured)")
        lines.append(f"- Key moments present: {', '.join(ls['moments_present']) or '(none)'}")
        lines.append(f"- Key moments filled: {', '.join(ls['moments_filled']) or '(none)'}")
        canonical = set(LIFEECHO_KEY_MOMENT_TYPES)
        extra = set(ls["moments_present"]) - canonical
        missing = canonical - set(ls["moments_present"])
        if extra:
            lines.append(f"- Non-canonical moment types detected: {', '.join(sorted(extra))}")
        if missing:
            lines.append(f"- Missing canonical moment types: {', '.join(sorted(missing))}")
        lines.append(f"- Future script present: {ls['future_script_present']}")
        lines.append("")

    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect raw assessment JSON files.")
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--out", type=Path, help="Write the audit to this file.")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument(
        "--lifeecho",
        action="store_true",
        help="Enable LifeEcho specialization: detect raw-data shape, verify Big Five reverse scoring, surface life-story payload.",
    )
    args = parser.parse_args()

    results = [inspect_file(path) for path in args.files]
    lifeecho_results = None
    if args.lifeecho:
        lifeecho_results = []
        for path in args.files:
            try:
                data = load_json(path)
            except Exception:
                lifeecho_results.append({"detected": False, "error": "could not parse"})
                continue
            lifeecho_results.append(detect_lifeecho(data))

    if args.format == "json":
        payload = {
            "generic": results,
            "lifeecho": lifeecho_results if args.lifeecho else None,
        }
        output = json.dumps(payload, ensure_ascii=False, indent=2)
    else:
        output = render_markdown(results, lifeecho_results)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
