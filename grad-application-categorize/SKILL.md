---
name: grad-application-categorize
description: 港新硕博申请材料分类整理。将零散的原始材料按「证件与成绩」「简历与实习」「申请材料」三大类别归档，文件统一命名英文+姓名后缀。自动触发关键词：材料分类、整理材料、归档、文件归类、申请材料整理。
---

# 研究生申请材料分类整理 Skill

## 分类逻辑

所有材料归入以下 3 个文件夹（"文件夹不要太多"）：

| 文件夹 | 内容 | 说明 |
|---|---|---|
| **证件与成绩** | 身份证、护照、雅思/托福成绩单、证件照、成绩单、在读证明、学位证、毕业证、奖学金证书、学历认证等 | 身份 + 学术资质类官方文件 |
| **简历与实习** | 简历/CV（各版本）、实习证明、工作证明、推荐信、实习/工作内容描述、课程项目/Coursework 等 | 经历 + 能力证明类 |
| **申请材料** | 个人陈述/PS/SOP、选校确认书、各校文书要求、申请信息收集表、材料清单、文书收集表、会议记录等 | 申请文书 + 表格 |

## 文件命名规范

- **语言**：英文
- **格式**：`描述性名称_姓名后缀.扩展名`
- **姓名后缀示例**：`KaidiGUO`
- **命名样例**：
  - `ID_Card_KaidiGUO.pdf`
  - `Transcript_KaidiGUO.pdf`
  - `Resume_Accounting_KaidiGUO.pdf`
  - `HKU_Master_of_Accounting_PS_KaidiGUO.docx`
  - `School_Selection_KaidiGUO.docx`

## 文件 → 文件夹映射

### 证件与成绩
```
ID_Card_KaidiGUO.pdf           身份证
Passport_KaidiGUO.pdf          护照
IELTS_Score_KaidiGUO.pdf       雅思/语言成绩
Portrait_Photo_KaidiGUO.pdf    证件照/护照照片
Transcript_KaidiGUO.pdf        成绩单
Enrollment_Certificate_KaidiGUO.pdf  在读证明
Scholarship_Certificate_KaidiGUO.pdf 奖学金证书
```

### 简历与实习
```
Resume_Accounting_KaidiGUO.pdf      简历-会计方向
Resume_Marketing_KaidiGUO.pdf       简历-市场方向
Internship_Certificates_and_Recommendation_KaidiGUO.pdf  实习证明+推荐信
XRStudio_Intern_Certificate_KaidiGUO.pdf     校内实习补充证明
Audit_Internship_KaidiGUO.docx               审计实习工作内容
Investment_Company_Internship_KaidiGUO.docx  投资公司实习内容
Database_Design_Coursework_KaidiGUO.docx     课程项目
```

### 申请材料
```
School_Selection_KaidiGUO.docx         选校确认书
HK_SG_Materials_Checklist_KaidiGUO.docx       材料收集表
HK_SG_Application_Info_KaidiGUO.docx         申请信息收集表
HK_SG_Documents_Checklist_KaidiGUO.docx       文书收集表
Meeting_Minutes_KaidiGUO.txt                  会议记录
HKU_Master_of_Accounting_PS_KaidiGUO.docx     HKU 会计 PS
HKU_MSc_Marketing_PS_KaidiGUO.docx            HKU 市场营销 PS
HKU_MSc_Marketing_PS_KaidiGUO_v5.docx         HKU 市场营销 PS v5
文书要求/                                      各校文书要求（子文件夹）
  Nanyang Technological University_MSc_Accountancy.docx
  Nanyang Technological University_MSc_Marketing_Science.docx
  National University of Singapore_MSc_in_Accounting_and_Financial_Analytics.docx
  National University of Singapore_MSc_in_Marketing_Analytics_and_Insights.docx
  The Chinese University of Hong Kong_Master_of_Accountancy.docx
  The Chinese University of Hong Kong_MSc_in_Marketing.docx
  The Hong Kong University of Science and Technology_MSc_in_Accounting.docx
  The Hong Kong University of Science and Technology_MSc_in_Marketing.docx
  The University of Hong Kong_Master_of_Accounting.docx
  The University of Hong Kong_MSc_in_Marketing.docx
```

## 使用约束

1. **原始资料不动** — 原始照片/扫描件所在的 `原始资料` 文件夹保持原样，不做任何分类操作
2. **文件夹不超过 4 个** — 避免层级过深，用户不好找
3. **图片直接转 PDF** — 手机拍的照片直接用 PIL 转换，不做任何图像处理（不裁切、不透视校正、不 OCR、不加白底 A4）
4. **多页合并** — 正反面（如身份证、护照各页）合并为一个 PDF 文件，每页一页
5. **旧文件覆盖** — 同名旧 PDF 先删除再生成新文件，不留重复
