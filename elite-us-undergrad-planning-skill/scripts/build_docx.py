#!/usr/bin/env python3
"""Enhanced Markdown-to-DOCX builder for parent-facing Chinese admissions reports.

Extends the elite-us-undergrad-planning builder with LifeEcho contrast rules:
cream page, dark ink, teal headings, readable table headers, and section
summaries rendered as callout tables rather than italic quotes.

CLI (same as the original):
  python build_docx.py --input md --output docx --style yaml
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import List, Optional

import yaml
from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Emu, Pt, RGBColor


FOOTER_PAGE_COLOR = "66756F"
INLINE_SPLIT = re.compile(r"(\*\*[^*]+?\*\*|\*[^*]+?\*)")
IMAGE_RE = re.compile(r"^!\[(.*?)\]\((.*?)\)\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
BULLET_RE = re.compile(r"^[-*+]\s+(.*)$")
NUMBER_RE = re.compile(r"^\d+[.)]\s+(.*)$")

DEFAULT_STYLE = {
    "font": {
        "east_asia": "Microsoft YaHei",
        "latin": "Georgia",
        "body_size_pt": 11,
        "title_size_pt": 20,
        "heading1_size_pt": 16,
        "heading2_size_pt": 13,
    },
    "page": {"margin_cm": 2.0, "background": "F8F5ED"},
    "colors": {
        "ink": "16211E",
        "heading": "004D47",
        "heading2": "00685F",
        "muted": "3A4C47",
        "gold": "8A6A2F",
        "table_header": "E6F5EE",
        "table_header_text": "004D47",
        "table_border": "D6CEBF",
        "table_cell_text": "16211E",
        "summary_fill": "E6F5EE",
        "summary_text": "004D47",
        "quote_border": "00685F",
    },
    "paragraph": {"line_spacing": 1.32, "space_after_pt": 8},
    "header": {"text": "美国本科申请规划", "color": "00685F"},
}


def hex_color(value: Optional[str], fallback: str = "16211E") -> str:
    raw = str(value or fallback).strip().lstrip("#").upper()
    if len(raw) != 6 or any(ch not in "0123456789ABCDEF" for ch in raw):
        return fallback.lstrip("#").upper()
    return raw


def readable_text_color(value: Optional[str], fallback: str = "16211E") -> str:
    """Reject white/cream text that disappears on LifeEcho page or teal-mist fills."""
    raw = hex_color(value, fallback)
    if raw in {"FFFFFF", "FFFDF8", "F4F0E6", "F8F5ED", "F7F4EC", "E6F5EE"}:
        return fallback.lstrip("#").upper()
    return raw


def header_text_color(value: Optional[str]) -> str:
    """Table header text must stay dark on #E6F5EE. Never white."""
    raw = str(value or "004D47").strip().lstrip("#").upper()
    if len(raw) != 6 or raw in {"FFFFFF", "FFF", "F4F0E6", "F8F5ED", "F7F4EC", "FFFDF8", "E6F5EE"}:
        return "004D47"
    return raw


def deep_merge(base: dict, override: dict) -> dict:
    out = dict(base)
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], value)
        else:
            out[key] = value
    return out


def load_style(path: Path | None) -> dict:
    style = dict(DEFAULT_STYLE)
    if path and path.exists():
        loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if isinstance(loaded, dict):
            style = deep_merge(style, loaded)
    return style


def east_font(style: dict) -> str:
    return str(style.get("font", {}).get("east_asia", "Microsoft YaHei"))


def latin_font(style: dict) -> str:
    return str(style.get("font", {}).get("latin", "Georgia"))


def color_of(style: dict, key: str, fallback: str) -> str:
    return hex_color(style.get("colors", {}).get(key), fallback)


def text_color_of(style: dict, key: str, fallback: str) -> str:
    return readable_text_color(style.get("colors", {}).get(key), fallback)


def set_run_font(
    run,
    east_asia: str,
    latin: str,
    size_pt: float | None = None,
    bold: bool | None = None,
    color: str | None = None,
    italic: bool | None = None,
):
    run.font.name = latin
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), latin)
    rFonts.set(qn("w:hAnsi"), latin)
    rFonts.set(qn("w:eastAsia"), east_asia)
    rFonts.set(qn("w:cs"), east_asia)
    if size_pt:
        run.font.size = Pt(size_pt)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(hex_color(color))


def set_style_font(doc_style, east_asia: str, latin: str, size_pt: float, bold: bool = False, color: str | None = None):
    doc_style.font.name = latin
    rPr = doc_style._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    rFonts.set(qn("w:ascii"), latin)
    rFonts.set(qn("w:hAnsi"), latin)
    rFonts.set(qn("w:eastAsia"), east_asia)
    rFonts.set(qn("w:cs"), east_asia)
    doc_style.font.size = Pt(size_pt)
    doc_style.font.bold = bold
    if color:
        doc_style.font.color.rgb = RGBColor.from_string(hex_color(color))


def set_cell_shading(cell, fill: str):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color(fill, "E6F5EE"))


def set_cell_margins(cell, top: int = 60, start: int = 80, bottom: int = 60, end: int = 80):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for name, value in (("top", top), ("left", start), ("bottom", bottom), ("right", end), ("start", start), ("end", end)):
        node = tc_mar.find(qn(f"w:{name}"))
        if node is None:
            node = OxmlElement(f"w:{name}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def _set_border_edge(parent, tag: str, color: str, sz: str):
    element = parent.find(qn(tag))
    if element is None:
        element = OxmlElement(tag)
        parent.append(element)
    element.set(qn("w:val"), "single")
    element.set(qn("w:sz"), str(sz))
    element.set(qn("w:space"), "0")
    element.set(qn("w:color"), hex_color(color, "D6CEBF"))


def set_cell_border(cell, color: str = "D6CEBF", *, left_color: str | None = None, left_sz: str = "12", sz: str = "4"):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_borders = tc_pr.first_child_found_in("w:tcBorders")
    if tc_borders is None:
        tc_borders = OxmlElement("w:tcBorders")
        tc_pr.append(tc_borders)
    for edge in ("top", "left", "bottom", "right"):
        tag = "w:" + edge
        if edge == "left" and left_color:
            _set_border_edge(tc_borders, tag, left_color, left_sz)
        else:
            _set_border_edge(tc_borders, tag, color, sz)


def repeat_table_header(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    if tr_pr.find(qn("w:tblHeader")) is None:
        flag = OxmlElement("w:tblHeader")
        flag.set(qn("w:val"), "true")
        tr_pr.append(flag)


def to_twips(value) -> int:
    """python-docx Length is EMU; some versions expose .twips, others return int."""
    twips = getattr(value, "twips", None)
    if twips is not None and not callable(twips):
        return int(twips)
    return int(value) // 635


def usable_width_twips(doc: Document) -> int:
    section = doc.sections[0]
    return to_twips(section.page_width) - to_twips(section.left_margin) - to_twips(section.right_margin)


def set_table_full_width(table, doc: Document):
    width = usable_width_twips(doc)
    table.autofit = True
    tbl = table._tbl
    tbl_pr = tbl.tblPr
    tbl_w = tbl_pr.find(qn("w:tblW"))
    if tbl_w is None:
        tbl_w = OxmlElement("w:tblW")
        tbl_pr.append(tbl_w)
    tbl_w.set(qn("w:w"), str(width))
    tbl_w.set(qn("w:type"), "dxa")
    lookup = tbl_pr.find(qn("w:tblLook"))
    if lookup is None:
        lookup = OxmlElement("w:tblLook")
        tbl_pr.append(lookup)
    lookup.set(qn("w:firstRow"), "1")
    lookup.set(qn("w:noHBand"), "1")
    lookup.set(qn("w:noVBand"), "1")


def set_document_background(doc: Document, color: str) -> None:
    fill = hex_color(color, "F8F5ED")
    existing = doc.element.find(qn("w:background"))
    if existing is not None:
        existing.set(qn("w:color"), fill)
    else:
        background = OxmlElement("w:background")
        background.set(qn("w:color"), fill)
        doc.element.insert(0, background)
    settings = doc.settings.element
    if settings.find(qn("w:displayBackgroundShape")) is None:
        node = OxmlElement("w:displayBackgroundShape")
        node.set(qn("w:val"), "true")
        settings.append(node)


def add_paragraph_bottom_border(paragraph, color: str, sz: str = "8"):
    p_pr = paragraph._p.get_or_add_pPr()
    p_bdr = p_pr.find(qn("w:pBdr"))
    if p_bdr is None:
        p_bdr = OxmlElement("w:pBdr")
        p_pr.append(p_bdr)
    bottom = p_bdr.find(qn("w:bottom"))
    if bottom is None:
        bottom = OxmlElement("w:bottom")
        p_bdr.append(bottom)
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), sz)
    bottom.set(qn("w:space"), "4")
    bottom.set(qn("w:color"), hex_color(color, "00685F"))


def add_page_number(paragraph, east: str, latin: str, color: str, size_pt: float = 9.0):
    run = paragraph.add_run()
    set_run_font(run, east, latin, size_pt=size_pt, color=color)
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run._r.extend([fld_begin, instr, fld_end])


def apply_header_footer(doc: Document, style: dict) -> None:
    east = east_font(style)
    latin = latin_font(style)
    header_cfg = style.get("header", {}) or {}
    header_text = str(header_cfg.get("text", "") or "")
    header_color = readable_text_color(header_cfg.get("color"), "00685F")
    footer_color = readable_text_color((style.get("footer") or {}).get("color"), FOOTER_PAGE_COLOR)

    for section in doc.sections:
        section.header_distance = Cm(1.0)
        section.footer_distance = Cm(1.0)
        section.different_first_page_header_footer = False

        hp = section.header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        hp.clear()
        if header_text:
            run = hp.add_run(header_text)
            set_run_font(run, east, latin, size_pt=9.0, bold=True, color=header_color)
            add_paragraph_bottom_border(hp, header_color, sz="6")

        fp = section.footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fp.clear()
        add_page_number(fp, east, latin, footer_color, size_pt=9.0)


def apply_doc_style(doc: Document, style: dict):
    east = east_font(style)
    latin = latin_font(style)
    body_size = float(style.get("font", {}).get("body_size_pt", 11))
    title_size = float(style.get("font", {}).get("title_size_pt", 20))
    h1_size = float(style.get("font", {}).get("heading1_size_pt", 16))
    h2_size = float(style.get("font", {}).get("heading2_size_pt", 13))
    margin = Cm(float(style.get("page", {}).get("margin_cm", 2.0)))
    ink = text_color_of(style, "ink", "16211E")
    heading = text_color_of(style, "heading", "004D47")
    heading2 = text_color_of(style, "heading2", "00685F")
    line_spacing = float(style.get("paragraph", {}).get("line_spacing", 1.32))
    space_after = float(style.get("paragraph", {}).get("space_after_pt", 8))
    background = hex_color(style.get("page", {}).get("background"), "F8F5ED")

    set_document_background(doc, background)

    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = margin
        section.bottom_margin = margin
        section.left_margin = margin
        section.right_margin = margin

    normal = doc.styles["Normal"]
    set_style_font(normal, east, latin, body_size, color=ink)
    para_format = normal.paragraph_format
    para_format.line_spacing = line_spacing
    para_format.space_after = Pt(space_after)
    para_format.space_before = Pt(0)

    if "Title" in doc.styles:
        set_style_font(doc.styles["Title"], east, latin, title_size, bold=True, color=heading)
        doc.styles["Title"].paragraph_format.space_after = Pt(10)
        doc.styles["Title"].paragraph_format.space_before = Pt(0)
        doc.styles["Title"].paragraph_format.keep_with_next = True

    heading_specs = (
        ("Heading 1", h1_size, heading, 14, 8),
        ("Heading 2", h2_size, heading2, 12, 6),
        ("Heading 3", max(body_size, 12), heading2, 10, 4),
        ("Heading 4", body_size, heading2, 8, 4),
    )
    for name, size, color, before, after in heading_specs:
        if name not in doc.styles:
            continue
        set_style_font(doc.styles[name], east, latin, size, bold=True, color=color)
        pf = doc.styles[name].paragraph_format
        pf.space_before = Pt(before)
        pf.space_after = Pt(after)
        pf.keep_with_next = True

    for list_name in ("List Bullet", "List Number"):
        if list_name in doc.styles:
            set_style_font(doc.styles[list_name], east, latin, body_size, color=ink)
            doc.styles[list_name].paragraph_format.space_after = Pt(3)
            doc.styles[list_name].paragraph_format.line_spacing = line_spacing

    apply_header_footer(doc, style)


def add_inline_runs(
    paragraph,
    text: str,
    style: dict,
    *,
    size_pt: float | None = None,
    color: str | None = None,
    bold: bool | None = None,
):
    east = east_font(style)
    latin = latin_font(style)
    ink = readable_text_color(color or color_of(style, "ink", "16211E"), "16211E")
    body_size = size_pt or float(style.get("font", {}).get("body_size_pt", 11))
    parts = INLINE_SPLIT.split(text)
    for part in parts:
        if not part:
            continue
        is_bold = part.startswith("**") and part.endswith("**") and len(part) >= 4
        is_italic = (not is_bold) and part.startswith("*") and part.endswith("*") and len(part) >= 2
        clean = part[2:-2] if is_bold else (part[1:-1] if is_italic else part)
        run = paragraph.add_run(clean)
        set_run_font(
            run,
            east,
            latin,
            size_pt=body_size,
            bold=True if (is_bold or bold) else False,
            italic=True if is_italic else False,
            color=ink,
        )
    return paragraph


def add_paragraph_with_inline(doc: Document, text: str, style_dict: dict, style_name: str | None = None):
    p = doc.add_paragraph(style=style_name)
    add_inline_runs(p, text, style_dict)
    return p


def add_summary_box(doc: Document, lines: List[str], style: dict):
    """Render markdown blockquotes as a parent-facing section summary callout."""
    chunks = [ln.strip() for ln in lines if ln.strip()]
    if not chunks:
        return
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_full_width(table, doc)
    cell = table.cell(0, 0)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    set_cell_shading(cell, color_of(style, "summary_fill", "E6F5EE"))
    set_cell_border(
        cell,
        color_of(style, "quote_border", "00685F"),
        left_color=color_of(style, "quote_border", "00685F"),
        left_sz="16",
        sz="8",
    )
    set_cell_margins(cell, top=100, start=140, bottom=100, end=140)

    summary_color = text_color_of(style, "summary_text", "004D47")
    body_size = float(style.get("font", {}).get("body_size_pt", 11))
    cell.text = ""
    for idx, chunk in enumerate(chunks):
        p = cell.paragraphs[0] if idx == 0 else cell.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.line_spacing = 1.25
        add_inline_runs(p, chunk, style, size_pt=body_size, color=summary_color, bold=False)
        for run in p.runs:
            run.italic = False
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(4)


def is_table_separator(line: str) -> bool:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c or "") for c in cells)


def parse_table(lines: List[str], start: int):
    table_lines = []
    i = start
    while i < len(lines) and lines[i].strip().startswith("|") and "|" in lines[i].strip()[1:]:
        table_lines.append(lines[i])
        i += 1
    if len(table_lines) < 2 or not is_table_separator(table_lines[1]):
        return None, start
    rows = []
    for j, line in enumerate(table_lines):
        if j == 1:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    return rows, i


def add_table(doc: Document, rows: List[List[str]], style_dict: dict):
    if not rows:
        return
    cols = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    set_table_full_width(table, doc)

    header_fill = hex_color(style_dict.get("colors", {}).get("table_header"), "E6F5EE")
    header_text = header_text_color(style_dict.get("colors", {}).get("table_header_text"))
    border = hex_color(style_dict.get("colors", {}).get("table_border"), "D6CEBF")
    body_text = readable_text_color(style_dict.get("colors", {}).get("table_cell_text"), "16211E")
    east = east_font(style_dict)
    latin = latin_font(style_dict)
    cell_size = 9.5 if cols <= 3 else 9.0

    for r_idx, row in enumerate(rows):
        if r_idx == 0:
            repeat_table_header(table.rows[0])
        for c_idx in range(cols):
            cell = table.cell(r_idx, c_idx)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            text = row[c_idx] if c_idx < len(row) else ""
            cell.text = ""
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(text)
            is_header = r_idx == 0
            set_run_font(
                run,
                east,
                latin,
                size_pt=cell_size,
                bold=is_header,
                color=header_text if is_header else body_text,
            )
            if is_header:
                set_cell_shading(cell, header_fill)
            set_cell_border(cell, border)
            set_cell_margins(cell, top=50, start=70, bottom=50, end=70)
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(4)


def add_image(doc: Document, md_path: Path, image_ref: str, caption: str | None, style: dict):
    image_path = Path(image_ref)
    if not image_path.is_absolute():
        image_path = (md_path.parent / image_path).resolve()
    east = east_font(style)
    latin = latin_font(style)
    muted = color_of(style, "muted", "3A4C47")
    if not image_path.exists():
        p = doc.add_paragraph()
        run = p.add_run(f"[图片缺失：{image_ref}]")
        set_run_font(run, east, latin, size_pt=10, color=muted)
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run()
    width = Emu(int((doc.sections[0].page_width - doc.sections[0].left_margin - doc.sections[0].right_margin) * 0.98))
    try:
        run.add_picture(str(image_path), width=width)
    except Exception:
        run.add_picture(str(image_path), width=Cm(15.5))
    if caption:
        cp = doc.add_paragraph()
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap_run = cp.add_run(caption)
        set_run_font(cap_run, east, latin, size_pt=9.0, color=muted, italic=False)


def add_heading_styled(doc: Document, text: str, md_level: int, style: dict):
    east = east_font(style)
    latin = latin_font(style)
    title_size = float(style.get("font", {}).get("title_size_pt", 20))
    h1_size = float(style.get("font", {}).get("heading1_size_pt", 16))
    h2_size = float(style.get("font", {}).get("heading2_size_pt", 13))
    heading = text_color_of(style, "heading", "004D47")
    heading2 = text_color_of(style, "heading2", "00685F")

    if md_level == 1:
        p = doc.add_heading(text, level=0)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        size, color = title_size, heading
    elif md_level == 2:
        p = doc.add_heading(text, level=1)
        size, color = h1_size, heading
    elif md_level == 3:
        p = doc.add_heading(text, level=2)
        size, color = h2_size, heading2
    else:
        p = doc.add_heading(text, level=min(md_level - 1, 4))
        size, color = max(float(style.get("font", {}).get("body_size_pt", 11)), 12), heading2

    for run in p.runs:
        set_run_font(run, east, latin, size_pt=size, bold=True, color=color)
    return p


def collect_blockquote(lines: List[str], start: int) -> tuple[List[str], int]:
    collected: List[str] = []
    i = start
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith(">"):
            collected.append(stripped.lstrip(">").strip())
            i += 1
            continue
        if not stripped and i + 1 < len(lines) and lines[i + 1].strip().startswith(">"):
            collected.append("")
            i += 1
            continue
        break
    return collected, i


def build(md_path: Path, output: Path, style_path: Path | None):
    style_dict = load_style(style_path)
    doc = Document()
    apply_doc_style(doc, style_dict)
    east = east_font(style_dict)
    latin = latin_font(style_dict)
    ink = text_color_of(style_dict, "ink", "16211E")
    lines = md_path.read_text(encoding="utf-8").splitlines()
    i = 0
    in_code = False
    code_buf: List[str] = []
    skip_code = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            if not in_code:
                in_code = True
                lang = stripped[3:].strip().lower()
                skip_code = lang in {"mermaid", "mmd"}
                code_buf = []
            else:
                in_code = False
                if code_buf and not skip_code:
                    p = doc.add_paragraph()
                    run = p.add_run("\n".join(code_buf))
                    set_run_font(run, "Consolas", "Consolas", size_pt=8.5, color=ink)
                code_buf = []
                skip_code = False
            i += 1
            continue
        if in_code:
            if not skip_code:
                code_buf.append(line)
            i += 1
            continue

        if not stripped:
            i += 1
            continue

        if stripped in {"---", "***", "___"}:
            i += 1
            continue

        table_rows, next_i = parse_table(lines, i)
        if table_rows is not None:
            add_table(doc, table_rows, style_dict)
            i = next_i
            continue

        img_match = IMAGE_RE.match(stripped)
        if img_match:
            alt, ref = img_match.groups()
            add_image(doc, md_path, ref, alt or None, style_dict)
            i += 1
            continue

        heading = HEADING_RE.match(stripped)
        if heading:
            add_heading_styled(doc, heading.group(2).strip(), len(heading.group(1)), style_dict)
            i += 1
            continue

        if stripped.startswith(">"):
            quote_lines, next_i = collect_blockquote(lines, i)
            add_summary_box(doc, quote_lines, style_dict)
            i = next_i
            continue

        bullet = BULLET_RE.match(stripped)
        if bullet:
            add_paragraph_with_inline(doc, bullet.group(1), style_dict, style_name="List Bullet")
            i += 1
            continue

        numbered = NUMBER_RE.match(stripped)
        if numbered:
            add_paragraph_with_inline(doc, numbered.group(1), style_dict, style_name="List Number")
            i += 1
            continue

        add_paragraph_with_inline(doc, stripped, style_dict)
        i += 1

    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output)


def main():
    parser = argparse.ArgumentParser(description="Build a DOCX from a Markdown report")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--style", type=Path, default=None)
    args = parser.parse_args()
    build(args.input, args.output, args.style)


if __name__ == "__main__":
    main()

