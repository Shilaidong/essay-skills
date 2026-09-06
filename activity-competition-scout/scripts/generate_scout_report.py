#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
活动与竞赛规划最终交付报告（Word .docx & Markdown）生成引擎
支持：
- 会后正式版 / 客户交付版（去中介化、去公关话术、去排除免责、置顶史老师决策金句）
- 会前准备版 / 内部沟通提纲（包含沟通策略与排除依据）
- 专业 LifeEcho Cream/Teal 风格渲染、6列官方核查表、Common App 10大活动位、双周落地甘特表
"""

import os
import sys
import json
import argparse
from typing import Dict, Any, List

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn

# --- 调色板定义 (LifeEcho / 史老师咨询标准风格) ---
COLOR_PRIMARY_TEAL = RGBColor(0x00, 0x4D, 0x47)    # 标题暗青
COLOR_ACCENT_TEAL  = RGBColor(0x00, 0x68, 0x5F)    # 二级标题明青
COLOR_DARK_TEXT    = RGBColor(0x16, 0x21, 0x1E)    # 正文墨黑
COLOR_MUTED_TEXT   = RGBColor(0x55, 0x66, 0x63)    # 辅助灰
COLOR_WHITE        = RGBColor(0xFF, 0xFF, 0xFF)

HEX_HEADER_BG      = "004D47"                      # 表头背景暗青
HEX_ALT_ROW_BG     = "F7FAF9"                      # 表格交替行浅青灰
HEX_CALLOUT_BG     = "F0F7F6"                      # 金句引用框背景
HEX_CALLOUT_BORDER = "00685F"                      # 金句引用框左竖线
HEX_BORDER         = "D0DCD7"                      # 表格内边框浅灰

def set_cell_background(cell, fill_hex: str):
    """设置单元格背景颜色"""
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    """设置单元格内边距 (单位: dxa)"""
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    cell._tc.get_or_add_tcPr().append(tcMar)

def set_table_styling(table, border_hex=HEX_BORDER):
    """设置表格标准细边框与对齐方式"""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    tblBorders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="{border_hex}"/>
            <w:bottom w:val="single" w:sz="8" w:space="0" w:color="{border_hex}"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_hex}"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    ''')
    table._tbl.tblPr.append(tblBorders)

def add_lead_quote(doc, quote_text: str):
    """插入史老师段首决策金句 (Lead Quote Callout Box)"""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.5)
    
    cell = table.cell(0, 0)
    set_cell_background(cell, HEX_CALLOUT_BG)
    set_cell_margins(cell, top=160, bottom=160, left=240, right=200)
    
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:left w:val="single" w:sz="28" w:space="0" w:color="{HEX_CALLOUT_BORDER}"/>
            <w:top w:val="none"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    cell._tc.get_or_add_tcPr().append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.25
    
    run = p.add_run(quote_text)
    run.font.name = "Microsoft YaHei"
    run.font.size = Pt(10.5)
    run.font.bold = True
    run.font.color.rgb = COLOR_PRIMARY_TEAL
    
    # 增加段后间距
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(0)
    spacer.paragraph_format.space_after = Pt(4)

def style_heading1(p, text: str):
    """一级章节标题"""
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run(text)
    run.font.name = "Microsoft YaHei"
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = COLOR_PRIMARY_TEAL

def style_heading2(p, text: str):
    """二级小节标题"""
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    run.font.name = "Microsoft YaHei"
    run.font.size = Pt(12.5)
    run.font.bold = True
    run.font.color.rgb = COLOR_ACCENT_TEAL

def add_body_p(doc, text: str, bold_prefix: str = "", space_after: int = 5):
    """普通正文段落"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.25
    
    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = "Microsoft YaHei"
        r_bold.font.size = Pt(10.5)
        r_bold.font.bold = True
        r_bold.font.color.rgb = COLOR_DARK_TEXT
        
    r_text = p.add_run(text)
    r_text.font.name = "Microsoft YaHei"
    r_text.font.size = Pt(10.5)
    r_text.font.color.rgb = COLOR_DARK_TEXT
    return p

def populate_table_header(table, headers: List[str], col_widths: List[float]):
    """填充表头样式"""
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        cell = hdr_cells[i]
        cell.width = Inches(col_widths[i])
        set_cell_background(cell, HEX_HEADER_BG)
        set_cell_margins(cell, top=140, bottom=140, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(h)
        run.font.name = "Microsoft YaHei"
        run.font.size = Pt(9.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_WHITE

def populate_table_rows(table, rows_data: List[List[str]], col_widths: List[float], alignments: List[WD_ALIGN_PARAGRAPH] = None):
    """填充表格内容行"""
    for r_idx, row in enumerate(rows_data):
        row_cells = table.add_row().cells
        bg_hex = HEX_ALT_ROW_BG if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            cell = row_cells[c_idx]
            cell.width = Inches(col_widths[c_idx])
            set_cell_background(cell, bg_hex)
            set_cell_margins(cell, top=120, bottom=120, left=120, right=120)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            if alignments:
                p.alignment = alignments[c_idx]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.2
            run = p.add_run(val)
            run.font.name = "Microsoft YaHei"
            run.font.size = Pt(9)
            run.font.color.rgb = COLOR_DARK_TEXT

def build_scout_report(data: Dict[str, Any], output_path: str, mode: str = "post_meeting"):
    """
    构建最终活动与竞赛规划实施方案报告
    mode: 'post_meeting' (会后正式交付版) 或 'pre_meeting' (会前准备版)
    """
    doc = docx.Document()
    
    # 统一页边距为标准 1 英寸
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    student = data.get("student", {})
    s_name = student.get("name", "学生")
    cohort = student.get("cohort", "2028Fall")
    target_field = student.get("target_field", "HCI / 交叉学科")
    
    # --- 1. 标题与头部信息 ---
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run(f"{s_name} · {cohort} 美本顶尖申请活动与竞赛规划实施方案")
    r_title.font.name = "Microsoft YaHei"
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_PRIMARY_TEAL
    
    mode_tag = "【会后正式确认版 · 史老师团队梳理 · 专供落地执行】" if mode == "post_meeting" else "【会前沟通准备版 · 顾问团队核心提纲】"
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run(f"{mode_tag}\n目标专业：{target_field} · 长期专长升维 · 聚焦校内真实事权 · 自主组队与导师后置")
    r_sub.font.name = "Microsoft YaHei"
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = COLOR_ACCENT_TEAL
    
    # 档案元数据表
    meta_table = doc.add_table(rows=2, cols=4)
    set_table_styling(meta_table)
    meta_widths = [1.5, 1.75, 1.5, 1.75]
    meta_cells = meta_table.rows[0].cells
    meta_cells[0].paragraphs[0].add_run("学生姓名").font.bold = True
    meta_cells[1].paragraphs[0].add_run(s_name)
    meta_cells[2].paragraphs[0].add_run("毕业届别").font.bold = True
    meta_cells[3].paragraphs[0].add_run(cohort)
    
    meta_cells2 = meta_table.rows[1].cells
    meta_cells2[0].paragraphs[0].add_run("在读学业/标化").font.bold = True
    meta_cells2[1].paragraphs[0].add_run(student.get("academics", "课内高标、托福已通关"))
    meta_cells2[2].paragraphs[0].add_run("申请冲刺目标").font.bold = True
    meta_cells2[3].paragraphs[0].add_run(student.get("target_tier", "全美 Top 20 顶尖大学"))
    
    for r in meta_table.rows:
        for c in r.cells:
            set_cell_background(c, "FAFCFB")
            set_cell_margins(c, top=80, bottom=80, left=100, right=100)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    
    # --- 第 0 章：全局战略提要与核心决议 ---
    p0 = doc.add_paragraph()
    style_heading1(p0, "0. 全局战略提要与核心决议（Executive Summary）")
    add_lead_quote(doc, data.get("quotes", {}).get("exec_summary", 
        "先说结论：标化省下来的大把时间，咱们全砸在刀刃上。活动坚决不搞疲劳战，绝不碰孩子头疼的硬力学和纯物理。托福通关后，高十一全力死保 GPA 和冲刺 SAT。大项目先由孩子在校内自主发起、带队拉人，顾问团队做幕后智囊出好预案；后续如果遇到硬件和电路卡点，按需匹配外部专业导师进场兜底并全队分摊成本。学术竞赛果断转战 11 月的数学建模论文，避开题海；校园小项目全挂在校内真实事权上，真实接地气，拒绝塑料包装。"))
    
    for item in data.get("executive_decisions", []):
        add_body_p(doc, item.get("desc", ""), bold_prefix=f"• {item.get('title', '')}：")
        
    # --- 第 1 章：学生底牌资产与独一人设定位 ---
    p1 = doc.add_paragraph()
    style_heading1(p1, f"一、 {s_name} 的底牌资产与独一人设定位")
    add_lead_quote(doc, data.get("quotes", {}).get("persona", 
        "名校招生官最反感整套外部生造的塑料履历。孩子坚持了多年的专长、校内的真实职位，这是真金白银的长期积累。咱们要做的是老树发新芽，顺着长板往上带，不造假，也不给自己找别扭。"))
    
    persona_data = data.get("persona_section", {})
    add_body_p(doc, persona_data.get("core_strengths", ""), bold_prefix="1. 长期特长资产（老树发新芽）：")
    add_body_p(doc, persona_data.get("subject_redlines", ""), bold_prefix="2. 学科边界与舒适区保护（坚决不碰硬物理）：")
    add_body_p(doc, persona_data.get("spike_definition", ""), bold_prefix="3. 申请独一人设定位（The Spike Persona）：")
    
    # --- 第 2 章：核心旗舰大项目实施方案 ---
    p2 = doc.add_paragraph()
    style_heading1(p2, "二、 核心旗舰大项目实施方案（自主组队 · 导师后置）")
    add_lead_quote(doc, data.get("quotes", {}).get("big_project", 
        "大项目先由孩子在校内自主发起、带队拉人。顾问团队帮孩子出好项目预提案，孩子自己去找同学聊。复杂的硬件和电路，队伍如果搞得定就自己搞；如果后面遇到卡点，按需引入外部专业导师进场兜底，还能全队一起分摊成本。进退自如，主动权完全在咱们自己手里。"))
    
    bp = data.get("big_project", {})
    add_body_p(doc, bp.get("pain_point", ""), bold_prefix="1. 真实生命痛点定义：")
    add_body_p(doc, bp.get("product_spec", ""), bold_prefix="2. 产品软硬件形态与用户触点：")
    add_body_p(doc, bp.get("team_mechanism", ""), bold_prefix="3. 组队与推进机制（自主先行 · 导师后置）：")
    add_body_p(doc, bp.get("anti_sat_design", ""), bold_prefix="4. 跨年级防撞期设计（确保 3 月 SAT 零风险）：")
    add_body_p(doc, bp.get("matched_competitions", ""), bold_prefix="5. 承接核心赛事：")
    
    # --- 第 3 章：学术与标化竞赛实施方案 ---
    p3 = doc.add_paragraph()
    style_heading1(p3, "三、 学术与标化竞赛实施方案（团队建模论文替代题海笔试）")
    add_lead_quote(doc, data.get("quotes", {}).get("academic_comp", 
        "学术竞赛咱们做重大调整：坚决不打一考定终身、纯靠题海战术的闭卷笔试。孩子高十一还要保核心课 GPA 和冲刺 SAT，精力耗不起。咱们主攻 11 月的数学建模竞赛，论文提交制，结合微积分与计算机专长产出高水准学术论文，11 月彻底结项拿大奖。"))
    
    ac = data.get("academic_competition", {})
    add_body_p(doc, ac.get("rationale", ""), bold_prefix="1. 战略转向依据：")
    add_body_p(doc, ac.get("core_match", ""), bold_prefix="2. 主攻赛事（HiMCM 数学建模）：")
    add_body_p(doc, ac.get("timeline_advantage", ""), bold_prefix="3. 窗口期时间优势：")
    
    # --- 第 4 章：校园落地微项目矩阵 ---
    p4 = doc.add_paragraph()
    style_heading1(p4, "四、 校园落地微项目矩阵（事权绑定 · 1大 + N小闭环）")
    add_lead_quote(doc, data.get("quotes", {}).get("micro_projects", 
        "校园小项目不求虚名，求的是真实、接地气，为文书提供有血有肉的故事。孩子在校内有职务事权，咱们就顺水推舟把事权用透。每个项目仅占一两个周末，全由顾问老师带着做完。"))
    
    for mp in data.get("micro_projects", []):
        add_body_p(doc, mp.get("desc", ""), bold_prefix=f"• {mp.get('name', '')}：")
        
    add_body_p(doc, data.get("micro_projects_value", "作为大项目的真实性反向佐证，彻底粉碎招生官对中学生科创真伪的怀疑；同时填满 Common App 4~6 项活动。"), bold_prefix="★ 微项目的双重战略价值：")
    
    # --- 第 5 章：入选赛事 100% 官方事实核验全景表 ---
    p5 = doc.add_paragraph()
    style_heading1(p5, "五、 精选赛事 100% 官方事实核查与物料直通全景表")
    add_lead_quote(doc, data.get("quotes", {}).get("factcheck_table", 
        "比赛不在多，在准。所有入选比赛 100% 接纳中国大陆学生，没有身份限制陷阱。提交物完全由大项目和校园活动顺手生成，绝不让孩子为了打比赛多写一份作业。"))
    
    fact_table = doc.add_table(rows=1, cols=6)
    set_table_styling(fact_table)
    fact_headers = ["赛事名称与主办方", "参赛依托项目", "官方关键提交内容", "官方报名与赛程", "拿奖月份", "最新官方网址与渠道"]
    fact_widths = [1.2, 1.1, 1.4, 0.9, 0.7, 1.2]
    populate_table_header(fact_table, fact_headers, fact_widths)
    
    fact_rows = []
    for c in data.get("competitions_matrix", []):
        fact_rows.append([
            c.get("name", ""),
            c.get("mapped_project", ""),
            c.get("deliverables", ""),
            c.get("schedule", ""),
            c.get("award_date", ""),
            c.get("official_url", "")
        ])
    populate_table_rows(fact_table, fact_rows, fact_widths, [
        WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT,
        WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT
    ])
    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    
    # --- 第 6 章：Common App 10大活动位与5大荣誉预排 ---
    p6 = doc.add_paragraph()
    style_heading1(p6, "六、 Common App 10大活动位与5大荣誉预排系统")
    add_lead_quote(doc, data.get("quotes", {}).get("common_app", 
        "高三递交申请时，申请表就填这 10 个活动。一个不缺，主线分明。招生官一眼能看出这个孩子既能在全球顶尖科创赛拿大奖，又在校内踏捉实实解决身边同学的真实需求。"))
    
    # 10 大活动表
    style_heading2(doc.add_paragraph(), "1. Common App 10 大活动列表预排（Activities 1-10）")
    act_table = doc.add_table(rows=1, cols=5)
    set_table_styling(act_table)
    act_headers = ["#", "活动类别", "担任角色与职位", "项目名称与组织", "核心成就与贡献 (150字符英文预排)"]
    act_widths = [0.4, 1.1, 1.2, 1.3, 2.5]
    populate_table_header(act_table, act_headers, act_widths)
    act_rows = []
    for a in data.get("common_app_activities", []):
        act_rows.append([
            str(a.get("num", "")),
            a.get("category", ""),
            a.get("role", ""),
            a.get("name", ""),
            a.get("desc", "")
        ])
    populate_table_rows(act_table, act_rows, act_widths, [
        WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT,
        WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT
    ])
    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    
    # 5 大荣誉表
    style_heading2(doc.add_paragraph(), "2. 申请前实打实落袋的 5 大学术荣誉预排（Honors 1-5）")
    hon_table = doc.add_table(rows=1, cols=5)
    set_table_styling(hon_table)
    hon_headers = ["#", "荣誉名称", "级别 (Level)", "预计出奖时间", "获奖定位与含金量"]
    hon_widths = [0.4, 1.8, 1.0, 1.1, 2.2]
    populate_table_header(hon_table, hon_headers, hon_widths)
    hon_rows = []
    for h in data.get("common_app_honors", []):
        hon_rows.append([
            str(h.get("num", "")),
            h.get("name", ""),
            h.get("level", ""),
            h.get("award_time", ""),
            h.get("significance", "")
        ])
    populate_table_rows(hon_table, hon_rows, hon_widths, [
        WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER,
        WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT
    ])
    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    
    # --- 第 7 章：双周落地甘特与行动责任矩阵 ---
    p7 = doc.add_paragraph()
    style_heading1(p7, "七、 双周落地推进甘特与行动责任矩阵（Action Plan）")
    add_lead_quote(doc, data.get("quotes", {}).get("roadmap", 
        "方案在文档里，接下来看执行。谁做、哪天完成，下面每一条清清楚楚。大家各司其职，孩子重点把 9 月 SAT 考好，回校按预案把队友拉好；复杂的硬件电路和后续比赛资源，由我们做坚强后盾随时顶上。"))
    
    road_table = doc.add_table(rows=1, cols=4)
    set_table_styling(road_table)
    road_headers = ["阶段周次与日期", f"{s_name} 具体动作", "顾问老师支持动作", "里程碑交付物与归档"]
    road_widths = [1.2, 2.0, 2.0, 1.3]
    populate_table_header(road_table, road_headers, road_widths)
    road_rows = []
    for w in data.get("roadmap_weeks", []):
        road_rows.append([
            w.get("timeframe", ""),
            w.get("student_action", ""),
            w.get("advisor_action", ""),
            w.get("deliverable", "")
        ])
    populate_table_rows(road_table, road_rows, road_widths, [
        WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT
    ])
    
    # 保存文档
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc.save(output_path)
    print(f"[OK] 成功生成活动与竞赛规划最终报告: {output_path}")

def get_sample_report_data(student_name: str = "陈艾馨") -> Dict[str, Any]:
    """生成内置的示范数据字典"""
    return {
        "student": {
            "name": student_name,
            "cohort": "2028Fall",
            "target_field": "人机交互 (HCI) 与设计科技方向",
            "academics": "GPA 稳健、AP Calc BC 5分、在学 AP CSA、托福 110 (免战标化课)",
            "target_tier": "全美 Top 20 综合性大学 (CMU / 康奈尔 / 华大等)"
        },
        "quotes": {
            "exec_summary": "先说结论：标化省下来的大把时间，咱们全砸在刀刃上。活动坚决不搞疲劳战，绝不碰孩子头疼的硬力学和纯物理。托福 110 彻底通关，高十一全力保 GPA、主精力冲刺 SAT。大项目先由孩子在校内自主发起、带队拉人，顾问团队做幕后智囊出好预案；后续如果遇到硬件和电路卡点，按需匹配外部专业导师进场兜底并全队分摊成本。学术竞赛果断转战 11 月的数学建模论文，避开题海；四个校园小项目全挂在学生会副主席的事权上，真实接地气，拒绝塑料包装。",
            "persona": "名校招生官最反感整套外部生造的塑料履历。孩子跳了 10 年芭蕾、刚升任学生会副主席、短视频单条播放破 10 万，这是真金白银的长期坚持。咱们要做的是老树发新芽，顺着长板往上带，不造假，也不给自己找别扭。",
            "big_project": "大项目先由孩子在校内自主发起、带队拉人。顾问团队帮孩子出好项目预提案，孩子自己去找同学聊。复杂的硬件和电路，队伍如果搞得定就自己搞；如果后面遇到卡点，按需引入外部专业导师进场兜底，还能全队一起分摊成本。进退自如，主动权完全在咱们自己手里。",
            "academic_comp": "学术竞赛咱们做重大调整：坚决不打一考定终身、纯靠题海战术的闭卷笔试。孩子高十一还要保计算机和冲 SAT，精力耗不起。咱们主攻 11 月的 HiMCM 数学建模竞赛，论文提交制，结合微积分 5 分与在读计算机，产出高质量学术论文，11 月彻底结项拿大奖。",
            "micro_projects": "校园小项目不求虚名，求的是真实、接地气，为文书提供有血有肉的故事。孩子既然升了学生会副主席，管着组织部和学习部，咱们就顺水推舟，把事权用透，每个项目仅占一两个周末，全由顾问老师带着做完。",
            "factcheck_table": "比赛不在多，在准。所有比赛 100% 接纳中国大陆学生，没有身份陷阱。提交物完全由大项目和校园活动顺手生成，绝不让孩子为了打比赛多写一份作业。",
            "common_app": "高三递交申请时，申请表就填这 10 个活动。一个不缺，主线分明。招生官一眼能看出这个孩子既能在全球顶尖科创赛拿大奖，又在校内踏踏实实解决身边同学的真实需求。",
            "roadmap": "方案在文档里，接下来看执行。谁做、哪天完成，下面每一条清清楚楚。大家各司其职，孩子重点把 9 月 SAT 考好，回校按预案把队友拉好；复杂的硬件电路和后续比赛资源，由我们做坚强后盾随时顶上。"
        },
        "executive_decisions": [
            {"title": "标化安全垫", "desc": "托福 110 分免除语言培训，高十一死保 GPA，主要精力全力冲刺 SAT 1500+。"},
            {"title": "大项目推进模式", "desc": "校内自主发起组队担任 Captain，顾问团队提供预提案支撑；硬件卡点后置引入外部导师兜底并全队分摊成本。"},
            {"title": "防撞期双保险", "desc": "跨年级组队（弟弟+校内跨年级技术/商科大牛），化解 3 月中旬康莱德决赛与 3 月 SAT 考期冲突。"},
            {"title": "学术竞赛战略转向", "desc": "避开欧几里得闭卷刷题消耗，主攻 11 月中旬 HiMCM 团队建模论文赛，寒假前锁定国际大奖。"},
            {"title": "校园小项目事权绑定", "desc": "全面挂靠学生会副主席事权（组织部+学习部），做透 Career Center、万圣节数字系统、体态工坊与魔方小册子。"}
        ],
        "persona_section": {
            "core_strengths": "芭蕾舞坚持 10 年具备专业水准；新学期升任学生会副主席（统管组织部与学习部）；短视频剪辑与视觉设计能力突出（单条播放破 10 万）；AP 微积分 5 分、AP CSA 在读，数理逻辑扎实。",
            "subject_redlines": "坚决不碰硬物理、力学公式推导与纯算法刷题。将技术重心完全转移至：真实痛点洞察、Figma UI 界面设计、路演短视频出镜拍摄、校园真实需求落地。",
            "spike_definition": "具身交互与运动科技产品官 (Embodied HCI & Somatic Sports-Tech PM)。将芭蕾长年累积的肌肉记忆与体态痛点，升维为可穿戴防伤产品与数字化交互系统，在 Top 20 申请中具备独一无二的辨识度。"
        },
        "big_project": {
            "pain_point": "古典芭蕾要求严苛的“外开”与“立脚尖”，疲劳时极易出现脚踝内翻代偿与假外开，导致跟腱炎与积液。艾馨自身饱受脚后跟积液之苦，第一人称生命体验具备极强说服力。",
            "product_spec": "柔性薄膜压敏传感器内置于鞋垫（采集 COP 足底压力中心）+ 80ms 触觉微震纠偏护踝 + 手机端 Figma 高保真 App 界面 + 3 分钟科技发布会级短视频。",
            "team_mechanism": "艾馨担任 Captain/Founder，拿顾问整理的《预提案》自主回校沟通队友；艾馨负责痛点陈述、Figma 原型、视频剪辑与主答辩；若硬件遇卡点，顾问团队引入专业科创导师把关，全队分摊费用。",
            "anti_sat_design": "康莱德中国决赛（3月中旬）与 3 月 SAT 撞期。队伍吸纳弟弟（滑板兴趣、跨年级粘性）及跨年级队员，确保答辩出勤，给艾馨留出备考安全窗口。",
            "matched_competitions": "主打 Conrad Challenge (Health & Nutrition 赛道)；协同 Plan B Technovation Girls (100% 免费，复用同一套 App 与商业计划书)。"
        },
        "academic_competition": {
            "rationale": "欧几里得需 2.5 小时高压闭卷纯刷题，与高十一冲刺 SAT 形成严重精力冲突；HiMCM 为团队论文赛，容错率高，适合发挥微积分 5 分与 Python 数据清洗优势。",
            "core_match": "HiMCM (美国高中生数学建模竞赛)，11 月中旬开赛，13~14 天开放窗口期，4 人组队全英文论文提交，导师深度把关。",
            "timeline_advantage": "11 月底彻底结项交卷，12 月至 1 月出奖，高十一寒假前奖项实打实落袋，彻底卸下学术竞赛包袱。"
        },
        "micro_projects": [
            {"name": "小项目 ① 校园 Career Center 职业与专业探索中心", "desc": "学习部职能结合引力坊资源，设立学生主任，每周五举办行业大咖与校友专业工坊，第 3 周启动首讲。"},
            {"name": "小项目 ② 万圣节化妆舞会数字化系统", "desc": "组织部职能结合 UX 设计，制作匿名标签匹配、破冰抽奖与人流打卡轻应用原型，根治往年混乱痛点。"},
            {"name": "小项目 ③ BodyTech 校园压力舒缓与体态工坊", "desc": "芭蕾热身动作降维为 3 分钟课间舒缓操，结合 50 名同学筛查数据，直接转化为 CTB 创新行动类结项报告。"},
            {"name": "小项目 ④ AlgoGuide 魔方三维空间图解小册子", "desc": "将魔方还原算法转化为 6 页全彩折页手绘视觉说明书，证明极致的同理心与界面信息架构设计能力。"}
        ],
        "micro_projects_value": "微项目作为大项目动手的反向铁证，面试时拿出网页与小册子直接粉碎造假怀疑；同时真实饱满填满 Common App 4~6 项活动。",
        "competitions_matrix": [
            {
                "name": "Conrad Challenge\n(康莱德创新挑战赛)\n[NASA/帕里斯基金会]",
                "mapped_project": "大项目：BalletSense\n(队长/UI交互与路演短视频)",
                "deliverables": "• 5页 Lean Canvas 商业画布\n• 3分钟路演视频 (Pitch Video)\n• Figma 原型操作录屏 (Demo)",
                "schedule": "2026年9-10月注册\n11月 Phase 2 提交\n次年3月中旬决赛答辩",
                "award_date": "2027年3月公布中国站结果\n4月全球峰会",
                "official_url": "https://www.conradchallenge.org/\n(全球官网直接注册)"
            },
            {
                "name": "HiMCM 数学建模\n(美国高中生数模赛)\n[美国数学及其应用联合会]",
                "mapped_project": "学术基石：数据清洗与\n可视化图表建模",
                "deliverables": "• 20-30页英文科研论文\n• 严谨数学建模过程\n• 灵敏度分析与数据图表",
                "schedule": "2026年11月4日-17日\n(13-14天指定窗口期开题\n全队集中攻关定稿)",
                "award_date": "2026年12月-2027年1月\n(高十一寒假前出奖)",
                "official_url": "https://www.comap.com/contests/himcm\n(指导顾问在 COMAP 注册)"
            },
            {
                "name": "Technovation Girls\n(全球女性科技挑战赛)\n[联合国教科文组织支持]",
                "mapped_project": "大项目复用：BalletSense\n(女性科技/SDG 3 健康赛道)",
                "deliverables": "• Figma 原型导出与录屏\n• 5-10页商业计划书\n• 3-4分钟 Pitch 视频 + 2分钟技术视频",
                "schedule": "2026年10月官网开放\n次年3月中旬注册截止\n4月下旬最终提交",
                "award_date": "2027年5月公布半决赛入围\n6月全球结果",
                "official_url": "https://www.technovationgirls.org/\n(100% 全球公益免费)"
            },
            {
                "name": "CTB 全球青年华人创新大挑战\n(China Thinks Big)\n[哈佛中美国际交流协作机构]",
                "mapped_project": "小项目 ③：BodyTech\n校园体态与压力舒缓工坊",
                "deliverables": "• 开题报告\n• 50名学生调研数据与方案\n• 线下实践记录与答辩展演 PPT",
                "schedule": "2026年10-11月报名组队\n12月黑客马拉松\n次年1月提交成果/2月答辩",
                "award_date": "2027年3-4月全国站/全球站\n(高十一春季彻底拿奖)",
                "official_url": "https://www.chinathinksbig.com/\n(CTB 官方报名系统)"
            }
        ],
        "common_app_activities": [
            {"num": 1, "category": "Science / Tech / Engineering", "role": "Founder & Captain", "name": "BalletSense: Embodied Health Insole", "desc": "Invented smart insole with thin-film pressure sensors & 80ms haptic ankle sleeve to correct pronation; designed Figma App & directed 3-min pitch."},
            {"num": 2, "category": "Academic / Math Modeling", "role": "Core Researcher (Data & Viz)", "name": "HiMCM International Modeling Team", "desc": "Co-authored 25-page modeling research on real-world systems; cleaned dataset using Python, generated predictive visualization plots; awarded Honors."},
            {"num": 3, "category": "Student Government", "role": "Vice President (Overseeing Org & Study)", "name": "High School Student Council", "desc": "Elected VP; directed 2 departments; launched campus-wide Career Center and digital event platforms; coordinated school-wide student initiatives."},
            {"num": 4, "category": "Career Exploration / Leadership", "role": "Student Director & Founder", "name": "Campus Career & Major Discovery Center", "desc": "Founded weekly exploration center under Study Dept; hosted weekly industry guest workshops; connected 200+ students with university insights."},
            {"num": 5, "category": "Community Service / Health", "role": "Project Lead", "name": "BodyTech: Adolescent Posture Workshop", "desc": "Transformed 10-yr ballet warm-up into 3-min stress-relief habits; conducted posture screening on 50 peers; submitted findings to CTB Innovation."},
            {"num": 6, "category": "Computer Science / UI-UX", "role": "Lead UX Designer", "name": "Halloween Gala Digital Matching System", "desc": "Engineered anonymous digital tag matching & raffle UI via Figma, resolving event overcrowding; improved participant satisfaction by 80%."},
            {"num": 7, "category": "Art / Information Design", "role": "Author & Visual Creator", "name": "AlgoGuide: 3D Spatial Algorithmic Booklet", "desc": "Authored 6-page color folded guide translating cube algorithms into beginner-friendly visual cues; demonstrated empathetic communication design."},
            {"num": 8, "category": "Dance", "role": "Principal Dancer & Teaching Assistant", "name": "Classical Ballet (10 Years Commitment)", "desc": "Trained 10+ yrs with RAD certifications; performed lead roles; assisted ballet masters in teaching junior dancers posture stability and alignment."},
            {"num": 9, "category": "Journalism / Media", "role": "Content Creator & Editor", "name": "Visual Storytelling & Video Channel", "desc": "Created short-form videos exploring technology, dance aesthetics, and student life; achieved 100k+ views on flagship video; mastered Premiere & AE."},
            {"num": 10, "category": "School Club", "role": "Active Participant / Peer Mentor", "name": "Mathematics & Computer Science Circle", "desc": "Participated in peer tutoring for AP Calculus & introductory programming; shared visual problem-solving notes with club members."}
        ],
        "common_app_honors": [
            {"num": 1, "name": "Conrad Challenge China Finalist / Innovation Award", "level": "International / National", "award_time": "2027年3月 (高十一)", "significance": "全球顶级高中生航天与健康创新大奖，证明工程产品商业化潜力"},
            {"num": 2, "name": "HiMCM High School Mathematical Contest in Modeling (M/F Award)", "level": "International", "award_time": "2026年12月 (高十一)", "significance": "国际顶级团队建模论文荣誉，证明大学级全英文科研写作与数据能力"},
            {"num": 3, "name": "Technovation Girls Global Semifinalist / Regional Winner", "level": "International", "award_time": "2027年5月 (高十一)", "significance": "联合国支持全球最大女性科技赛，证明科技公益关怀与移动端原型开发实力"},
            {"num": 4, "name": "China Thinks Big (CTB) National Station Award", "level": "National", "award_time": "2027年3月 (高十一)", "significance": "哈佛体系华人顶级创新行动大奖，证明真实的校园落地与社群影响力"},
            {"num": 5, "name": "School Academic Excellence & Leadership Award", "level": "School", "award_time": "2026年-2027年", "significance": "基于学生会副主席突出贡献与顶尖 GPA 授予的全校最高荣誉"}
        ],
        "roadmap_weeks": [
            {
                "timeframe": "第 1 周\n(9月7日 - 9月13日)",
                "student_action": "① 拿顾问给的《预提案要点》，在校内摸排弟弟与何红丽/柴凯文/朱培元意向；\n② 专注 9 月 SAT 模考与心态调节。",
                "advisor_action": "① 协助整理 BalletSense 简明招募要点与沟通指引；\n② 协助校方敲定 Career Center 第 1 讲时间与场地。",
                "deliverable": "校内意向队友名单初定\nSAT 备战状态稳定"
            },
            {
                "timeframe": "第 2 周\n(9月14日 - 9月20日)",
                "student_action": "① 9月18日前敲定 2-4 人团队名单与分工；\n② 出席 Career Center 第 1 讲并做学生代表发言。",
                "advisor_action": "① 引力坊团队进校开展第 1 场职业探索工作坊；\n② 评估队内技能，若硬件有瓶颈启动导师对接方案。",
                "deliverable": "团队正式组建完成\nCareer Center 启动首秀"
            },
            {
                "timeframe": "第 3-4 周\n(9月21日 - 10月5日)",
                "student_action": "① 完成 9 月 SAT 考试；\n② 组织队内第一次会议，梳理芭蕾痛点与 Figma 原型草图。",
                "advisor_action": "① 协助康莱德 Phase 1 注册建档；\n② 搭建队内协作云盘与素材库。",
                "deliverable": "SAT 成绩落袋\nConrad 官方账号注册完毕"
            },
            {
                "timeframe": "第 5-6 周\n(10月6日 - 10月19日)",
                "student_action": "① 绘制 Figma 核心 App 界面高保真原型；\n② 组织万圣节舞会数字化标签系统初版设计。",
                "advisor_action": "① 导师介入传感器硬件联调（若有需求）；\n② 审核 Lean Canvas 商业画布框架。",
                "deliverable": "Figma 交互高保真初稿\n硬件原型联调通电"
            },
            {
                "timeframe": "第 7-8 周\n(10月20日 - 11月2日)",
                "student_action": "① 万圣节舞会系统上线运行；\n② 录制并剪辑 3 分钟 BalletSense Pitch 视频初稿。",
                "advisor_action": "① 逐句精修 5 页商业画布英文文本；\n② 落实 HiMCM 参赛队伍注册与软件环境准备。",
                "deliverable": "万圣节小项目交付成功\nConrad 预提交材料齐备"
            },
            {
                "timeframe": "第 9-10 周\n(11月3日 - 11月17日)",
                "student_action": "① HiMCM 开赛，全队集中 13 天全英文论文冲刺；\n② 负责数据清洗、Python 可视化图表与排版。",
                "advisor_action": "① 康莱德 Phase 2 成果全套提交；\n② 数学建模导师全程指导 HiMCM 论文选题与模型把关。",
                "deliverable": "Conrad Phase 2 正式封箱\nHiMCM 论文提交结项！"
            },
            {
                "timeframe": "第 11-12 周\n(11月18日 - 12月1日)",
                "student_action": "① 在校内开展 BodyTech 芭蕾体态舒缓工坊（50人）；\n② 全力准备 12 月 SAT / 期末考试。",
                "advisor_action": "① 整理体态筛查数据，指导排版 CTB 创新报告；\n② 检查期末 GPA 与 AP 学科进度。",
                "deliverable": "CTB 项目成果初稿\n秋季所有竞赛彻底收官！"
            }
        ]
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成活动与竞赛规划最终实施方案 Word 文档")
    parser.add_argument("--input", "-i", type=str, help="输入 JSON 数据文件路径（若不提供则使用内置高标准数据）")
    parser.add_argument("--output", "-o", type=str, default="scout_planning_report.docx", help="输出 docx 文件路径")
    parser.add_argument("--mode", "-m", type=str, choices=["post_meeting", "pre_meeting"], default="post_meeting", help="版本模式：post_meeting(会后正式交付版) 或 pre_meeting(会前准备版)")
    parser.add_argument("--export-sample", type=str, help="导出标准 JSON 示范数据到指定路径并退出")
    
    args = parser.parse_args()
    
    if args.export_sample:
        sample = get_sample_report_data()
        with open(args.export_sample, "w", encoding="utf-8") as f:
            json.dump(sample, f, ensure_ascii=False, indent=2)
        print(f"[OK] 已导出标准数据模板至: {args.export_sample}")
        sys.exit(0)
        
    if args.input and os.path.exists(args.input):
        with open(args.input, "r", encoding="utf-8") as f:
            report_data = json.load(f)
    else:
        report_data = get_sample_report_data()
        
    build_scout_report(report_data, args.output, mode=args.mode)
