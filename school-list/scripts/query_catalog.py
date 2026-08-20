# -*- coding: utf-8 -*-
"""Read-only search over a School Navigator sqlite snapshot."""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

UG_HINTS = (
    "BA", "BS", "BSC", "BENG", "BFA", "BACHELOR", "AB", "BBA", "BM", "BCOM",
    "LLB", "BMUS", "HBSC", "HBA", "BSE", "BSBA", "SB", "BED", "BCOMP",
)
GRAD_HINTS = (
    "MA", "MS", "MSC", "MENG", "MSCI", "MBA", "MPHIL", "PHD", "MFA", "LLM",
    "MARCH", "MPH", "MED", "MASTER",
)


def connect(db: Path) -> sqlite3.Connection:
    if not db.is_file():
        raise SystemExit(f"db not found: {db}")
    uri = f"file:{db.resolve().as_posix()}?mode=ro"
    con = sqlite3.connect(uri, uri=True)
    con.row_factory = sqlite3.Row
    return con


def degree_tokens(raw: str | None) -> list[str]:
    if not raw:
        return []
    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return [str(x).upper() for x in data]
    except json.JSONDecodeError:
        pass
    return [raw.upper()]


def degree_bucket(raw: str | None) -> str:
    ug = False
    grad = False
    for t in degree_tokens(raw):
        compact = t.replace(".", "").replace(" ", "")
        if compact in UG_HINTS or compact.startswith("B") or "BACHELOR" in compact:
            ug = True
        if compact in GRAD_HINTS or "MASTER" in compact or compact == "PHD":
            grad = True
        elif compact.startswith("M") and compact not in UG_HINTS:
            grad = True
    if ug and grad:
        return "both"
    if grad:
        return "grad"
    if ug:
        return "ug"
    return "other"


def country_clause(country: str) -> tuple[str, list]:
    c = (country or "all").upper()
    if c in {"", "ALL"}:
        return "1=1", []
    if c in {"US", "GB", "OTHER"}:
        return "s.country_code = ?", [c]
    city_map = {
        "HK": ["Hong Kong", "Sha Tin", "Kowloon"],
        "SG": ["Singapore"],
        "AU": ["Sydney", "Melbourne", "Canberra", "Brisbane", "Adelaide", "Perth"],
        "CN": ["Beijing", "Shanghai", "Hangzhou", "Guangzhou", "Nanjing", "Shenzhen"],
        "CA": ["Montreal", "Toronto", "Vancouver", "Waterloo"],
    }
    if c in city_map:
        likes = city_map[c]
        ph = " OR ".join(["s.city LIKE ?"] * len(likes))
        return f"(s.country_code = 'OTHER' AND ({ph}))", [f"%{x}%" for x in likes]
    return "1=1", []


def search(con: sqlite3.Connection, queries: list[str], country: str, degree: str, limit: int, city: str | None):
    where = ["p.active = 1"]
    args: list = []
    cc, ca = country_clause(country)
    where.append(cc)
    args.extend(ca)
    if city:
        where.append("(s.city LIKE ? OR s.region LIKE ?)")
        args.extend([f"%{city}%", f"%{city}%"])

    qparts = []
    for q in queries:
        q = q.strip()
        if not q:
            continue
        like = f"%{q}%"
        qparts.append(
            "("
            "p.name_en LIKE ? OR p.name_zh LIKE ? OR "
            "p.college_name_en LIKE ? OR p.college_name_zh LIKE ? OR "
            "IFNULL(p.description_zh,'') LIKE ? OR "
            "IFNULL(p.admission_requirements_zh,'') LIKE ?"
            ")"
        )
        args.extend([like] * 6)
    if qparts:
        where.append("(" + " OR ".join(qparts) + ")")

    sql = f"""
    SELECT
      s.id AS school_id,
      s.name_en AS school_en,
      s.name_zh AS school_zh,
      s.country_code,
      s.city,
      s.ranking,
      s.ranking_system,
      p.id AS program_id,
      p.name_en AS program_en,
      p.name_zh AS program_zh,
      p.college_name_en,
      p.college_name_zh,
      p.degree_types_json,
      p.official_url,
      p.catalog_year
    FROM programs p
    JOIN schools s ON s.id = p.school_id
    WHERE {' AND '.join(where)}
    ORDER BY CASE WHEN s.ranking IS NULL THEN 9999 ELSE s.ranking END, p.name_en
    LIMIT 400
    """
    rows = []
    for r in con.execute(sql, args):
        bucket = degree_bucket(r["degree_types_json"])
        if degree in {"ug", "grad"} and bucket not in {degree, "both"}:
            continue
        rows.append(dict(r) | {"degree_bucket": bucket})
        if len(rows) >= limit:
            break
    return rows


def list_courses(con: sqlite3.Connection, program_id: str, limit: int):
    return [
        dict(r)
        for r in con.execute(
            """
            SELECT course_index, code, title_en, title_zh
            FROM courses
            WHERE program_id = ?
            ORDER BY course_index
            LIMIT ?
            """,
            (program_id, limit),
        )
    ]


def print_table(rows: list[dict]) -> None:
    if not rows:
        print("no matches")
        return
    print(f"matches={len(rows)}")
    for r in rows:
        school = r.get("school_zh") or r["school_en"]
        prog = r.get("program_zh") or r["program_en"]
        print(
            f"- {school} | {prog} | {r.get('country_code')} {r.get('city') or ''} | "
            f"rank={r.get('ranking')} | {r.get('degree_types_json')} | {r.get('official_url') or ''}"
        )


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Read-only School Navigator catalog search")
    ap.add_argument("--db", required=True)
    ap.add_argument("--q", action="append", default=[])
    ap.add_argument("--country", default="all")
    ap.add_argument("--degree", choices=["ug", "grad", "all"], default="all")
    ap.add_argument("--city", default="")
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--courses", default="", help="program_id to list courses")
    args = ap.parse_args()

    con = connect(Path(args.db))
    if args.courses:
        data = list_courses(con, args.courses, args.limit)
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            for c in data:
                print(f"{c['course_index']}\t{c.get('code') or ''}\t{c.get('title_zh') or c.get('title_en')}")
        return

    if not args.q:
        raise SystemExit("pass at least one --q")
    rows = search(con, args.q, args.country, args.degree, args.limit, args.city or None)
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print_table(rows)


if __name__ == "__main__":
    main()
