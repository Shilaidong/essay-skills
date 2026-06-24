#!/usr/bin/env python3
"""Validate the basic Agent Skill package structure."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Missing dependency: PyYAML. Run: pip install PyYAML") from exc


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
RECOGNIZED_FRONTMATTER = {"name", "description", "license", "compatibility", "metadata"}


def parse_frontmatter(path: Path) -> tuple[Dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter is not closed")
    raw = text[4:end]
    meta = yaml.safe_load(raw)
    if not isinstance(meta, dict):
        raise ValueError("Frontmatter must be a mapping")
    return meta, text[end + 5 :]


def validate(root: Path) -> List[str]:
    errors: List[str] = []
    skill_path = root / "SKILL.md"
    if not skill_path.exists():
        return ["Missing SKILL.md"]

    try:
        meta, body = parse_frontmatter(skill_path)
    except Exception as exc:  # noqa: BLE001
        return [str(exc)]

    name = str(meta.get("name", ""))
    description = str(meta.get("description", ""))
    if not name:
        errors.append("Missing required frontmatter field: name")
    elif not NAME_RE.fullmatch(name):
        errors.append("name must match ^[a-z0-9]+(-[a-z0-9]+)*$")
    elif name != root.name:
        errors.append(f"name '{name}' must match directory name '{root.name}'")
    if not description:
        errors.append("Missing required frontmatter field: description")
    elif len(description) > 1024:
        errors.append("description exceeds 1024 characters")

    unknown = sorted(set(meta) - RECOGNIZED_FRONTMATTER)
    if unknown:
        errors.append(f"Unknown frontmatter fields: {', '.join(unknown)}")

    metadata = meta.get("metadata")
    if metadata is not None:
        if not isinstance(metadata, dict):
            errors.append("metadata must be a mapping")
        else:
            non_string = [k for k, v in metadata.items() if not isinstance(k, str) or not isinstance(v, str)]
            if non_string:
                errors.append("metadata must contain string-to-string entries")

    for target in LINK_RE.findall(body):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        candidate = (root / target).resolve()
        if not candidate.exists():
            errors.append(f"Broken local link in SKILL.md: {target}")

    manifest = root / "manifest.txt"
    if manifest.exists():
        for line_number, raw in enumerate(manifest.read_text(encoding="utf-8").splitlines(), start=1):
            entry = raw.strip()
            if not entry:
                continue
            if entry.startswith("/") or ".." in Path(entry).parts:
                errors.append(f"Invalid manifest path at line {line_number}: {entry}")
                continue
            if not (root / entry).exists():
                errors.append(f"Manifest entry does not exist: {entry}")

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate an Agent Skill directory.")
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    errors = validate(root)
    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Skill validation passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
