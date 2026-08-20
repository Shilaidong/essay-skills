# -*- coding: utf-8 -*-
"""Find catalog sqlite and list template without hardcoded machine paths."""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path

SKIP_DIR = {
    ".git", "node_modules", ".venv", "venv", "AppData", "Library",
    "$Recycle.Bin", "Windows", "Program Files", "Program Files (x86)",
}

DB_PREFIX = "school-navigator-catalog-"
DB_SUFFIX = ".sqlite"
TPL_NAME = "选校清单模板.xlsx"
MAX_DEPTH = 8


def stdout_utf8() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def existing(p: str | Path | None) -> Path | None:
    if not p:
        return None
    path = Path(p).expanduser()
    return path if path.is_file() else None


def search_roots(work: str | None) -> list[Path]:
    roots: list[Path] = []
    for raw in (
        work,
        os.getcwd(),
        os.environ.get("SCHOOL_LIST_ROOT"),
        os.environ.get("OneDriveCommercial"),
        os.environ.get("OneDriveConsumer"),
        os.environ.get("OneDrive"),
        str(Path.home() / "OneDrive"),
    ):
        if not raw:
            continue
        p = Path(raw).expanduser()
        if p.exists() and p not in roots:
            roots.append(p)
    return roots


def walk_files(root: Path, want_db: bool, want_tpl: bool) -> tuple[list[Path], list[Path]]:
    dbs: list[Path] = []
    tpls: list[Path] = []
    root = root.resolve()
    for dirpath, dirnames, filenames in os.walk(root):
        rel = Path(dirpath).resolve().relative_to(root)
        depth = 0 if str(rel) == "." else len(rel.parts)
        if depth >= MAX_DEPTH:
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR and not d.startswith(".")]
        for name in filenames:
            if want_db and name.startswith(DB_PREFIX) and name.endswith(DB_SUFFIX):
                dbs.append(Path(dirpath) / name)
            if want_tpl and name == TPL_NAME:
                tpls.append(Path(dirpath) / name)
        if (not want_db or dbs) and (not want_tpl or tpls) and depth <= 2:
            # keep walking; catalogs may sit deeper
            pass
    return dbs, tpls


def newest(paths: list[Path]) -> Path | None:
    if not paths:
        return None
    return max(paths, key=lambda p: p.stat().st_mtime)


def catalog_meta(db: Path) -> dict:
    try:
        con = sqlite3.connect(f"file:{db.resolve().as_posix()}?mode=ro", uri=True)
        rows = con.execute("SELECT key, value FROM meta").fetchall()
        return {k: v for k, v in rows}
    except Exception as e:
        return {"error": str(e)}


def main() -> None:
    stdout_utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="")
    ap.add_argument("--template", default="")
    ap.add_argument("--work", default="")
    args = ap.parse_args()

    db = existing(args.db) or existing(os.environ.get("SCHOOL_NAVIGATOR_DB"))
    tpl = existing(args.template) or existing(os.environ.get("SCHOOL_LIST_TEMPLATE"))
    found_dbs: list[Path] = []
    found_tpls: list[Path] = []

    if db is None or tpl is None:
        for root in search_roots(args.work or None):
            more_db, more_tpl = walk_files(root, db is None, tpl is None)
            found_dbs.extend(more_db)
            found_tpls.extend(more_tpl)
            if (db or found_dbs) and (tpl or found_tpls):
                # still scan all roots so we can pick newest
                continue

    if db is None:
        db = newest(found_dbs)
    if tpl is None:
        tpl = newest(found_tpls)

    out = {
        "db": str(db) if db else None,
        "template": str(tpl) if tpl else None,
        "db_candidates": [str(p) for p in sorted(set(found_dbs), key=lambda p: p.stat().st_mtime, reverse=True)[:8]],
        "template_candidates": [str(p) for p in sorted(set(found_tpls), key=lambda p: p.stat().st_mtime, reverse=True)[:8]],
        "meta": catalog_meta(db) if db else {},
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if not db or not tpl:
        sys.exit(2)


if __name__ == "__main__":
    main()
