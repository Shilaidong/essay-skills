#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
活动与竞赛 100% 官方事实核查核对表生成器
用法: python factcheck_checklist.py --name "Conrad Challenge" --url "https://www.conradchallenge.org/"
"""

import argparse

def generate_checklist(name, url):
    print(f'''
# 【竞赛官方核查核对表】: {name}
- 官方主站 URL: {url}

## 1. 资格与身份核实 (Eligibility & Citizenship)
- [ ] 参赛者国籍限制: 是否仅限 U.S. Citizen / Permanent Resident (Green Card)? (是/否)
- [ ] 学籍与地域限制: 是否必须在美高在读? 是否接受中国大陆国际学校在读? (是/否)
- [ ] 年龄/年级窗口: Senior 组 / Junior 组确切年龄要求: ______
- [ ] 组队与领队限制: 人数限制 (___-___ 人); 是否必须有成年教练/顾问? (是/否)

## 2. 赛道与赛题设置 (Tracks & Themes)
- [ ] 本季最新开放赛道名称: ______
- [ ] 赛道对口度: 是否契合学生专长? 是否避开了学生讨厌的学科偏科? (是/否)

## 3. 报名渠道与费用 (Channels & Costs)
- [ ] 报名平台: 全球官网直投 / ASDAN 阿思丹代理 / 其他独立门户: ______
- [ ] 费用情况: 100% 免费 / 评审费收取额度: ______

## 4. 关键赛程节点 (Timeline & Deadlines)
- [ ] 注册/开题截止日: ______
- [ ] 核心成果 (Phase 1 / Phase 2) 提交截止日: ______
- [ ] 现场答辩/全国站/全球峰会月份: ______
- [ ] 官方公布获奖名单月份: ______ (能否赶在高三 Common App 递交前落袋?)

## 5. 提交物与评审规范 (Deliverables & Rubrics)
- [ ] 视频要求: 严格时长限制 (不超过 ___ 分钟); 横屏/竖屏要求: ______
- [ ] 书面材料: 商业画布 / 报告页数限制 (不超过 ___ 页); PDF 格式要求
- [ ] 原型要求: 允许 Figma / 概念原型，还是必须有实体硬件 / 商业级代码?

## 6. 历史变动排查 (Reorganizations & Risks)
- [ ] 近 2 年是否存在代理权变更、中国赛区暂停等风险? (如 FBLA 停摆情况)
''')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='生成竞赛官方事实核查清单')
    parser.add_argument('--name', default='示例竞赛', help='竞赛名称')
    parser.add_argument('--url', default='https://example.org', help='官方网站 URL')
    args = parser.parse_args()
    generate_checklist(args.name, args.url)
