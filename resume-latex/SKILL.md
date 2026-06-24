---
name: resume-latex
description: LaTeX 简历/CV 生成与修改。使用 Charter 字体、紧凑排版的单页简历模板，支持 Accounting/Marketing/Finance 等多方向定制。自动触发关键词：简历、CV、resume、LaTeX简历、修改简历、生成简历、CV模板。
---

# LaTeX Resume Skill

## 0. Overview

基于经典美式简历模板（Charter 字体、紧凑单页），通过 LaTeX 生成专业简历 PDF。支持多方向（Accounting、Marketing、Finance 等）定制，输出 LaTeX 工程文件夹 + 命名 PDF 双格式。

## 1. Template Reference

完整的 LaTeX 模板（以此为基准，不允许偏离）：

```latex
\documentclass[a4paper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[T1]{fontenc}
\usepackage{charter}
\usepackage[left=0.4in, right=0.4in, top=0.6in, bottom=0.4in]{geometry}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Section formatting
\titleformat{\section}{
  \vspace{-10pt}\scshape\raggedright\large\bfseries
}{}{0em}{}[\color{black}\titlerule \vspace{-6pt}]

%-------------------------
% Custom commands
\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeItemWithTitle}[2]{
  \item\small{
    \textbf{#1}{: #2 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-1pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & \textbf{#2} \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-6pt}
}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}\vspace{-12pt}}

\newcommand{\resumeItemListStart}{\begin{itemize}[leftmargin=0.15in, label={\tiny$\bullet$}, labelsep=3pt, itemsep=0pt, topsep=0pt, parsep=0pt]}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-6pt}}
```

## 2. Standard Sections

简历按以下顺序组织，按需增减 section：

| Section | 说明 |
|---|---|
| **HEADING** | 姓名（\Huge \scshape）+ 城市/电话/邮箱 |
| **Education** | 学校、学位、GPA、核心课程、奖学金、MOI |
| **Professional Experience** | 实习/工作经历，每条含公司、职位、时间、bullet points |
| **Academic Projects** | 课程项目，含项目名、角色、时间、bullet points |
| **Leadership & Skills** | 领导力活动 + 技术/语言技能 |

## 3. Spacing & Layout Rules

### 3.1 单页约束
简历必须控制在 **1 页以内**。当内容自然高度小于页面可用高度时，调整以下参数使内容均匀填满页面：

```latex
% === 紧凑版 (当内容接近满页时) ===
\documentclass[a4paper,10pt]{article}          % 降字号到 10pt
\usepackage[left=0.35in, right=0.35in, top=0.5in, bottom=0.35in]{geometry}  % 收窄边距

% 调整段间距（基础值）
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}\vspace{-8pt}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-4pt}}
\newcommand{\resumeSubheading}[4]{...\end{tabular*}\vspace{-4pt}}

% Section title 间距
\titleformat{\section}{
  \vspace{-6pt}\scshape\raggedright\large\bfseries
}{}{0em}{}[\color{black}\titlerule \vspace{-4pt}]
```

### 3.2 垂直居中（内容偏短时）
当内容较少、底部留白过大时，使用 `\flushbottom` + 双 `\vfill` 精确居中：

```latex
\flushbottom          % 替代 \raggedbottom：强制页面填满 \textheight

\begin{document}

\vspace*{\fill}       % 顶部弹性空白（starred: 页面顶部不消失）

% ... 所有简历内容 ...

\vspace*{\fill}       % 底部弹性空白

\end{document}
```

**原理**：两个 `\vfill`（无限胶水）平分剩余空间，实现精确垂直居中。`\flushbottom` 确保页面底部不留死空间。

### 3.3 微调间距（消除局部空白）
当某 section 内子项间隙不均匀时，使用 rubber lengths：

```latex
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}\vspace{-2pt plus 8pt}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-1pt plus 4pt}}
\titleformat{\section}{...}{}{0em}{}[\color{black}\titlerule \vspace{-2pt plus 6pt}]
```

`plus` 分量允许 LaTeX 在需要时拉伸间距，但内容满页时不会额外撑开。

## 4. File Naming & Output

### 4.1 命名规范

| 文件类型 | 命名格式 | 示例 |
|---|---|---|
| LaTeX 源文件 | `main.tex` | 放在项目文件夹内 |
| 编译 PDF | `main.pdf` | 自动生成 |
| 最终输出 PDF | `Resume_{Track}_{Name}.pdf` | `Resume_Accounting_KaidiGUO.pdf` |
| 项目文件夹 | `resume-{track}-{name}` | `resume-accounting-kaidi` |

### 4.2 输出结构

最终交付两个东西，放在同一目标目录：

```
目标目录/
├── resume-{track}-{name}/    ← LaTeX 工程文件夹
│   ├── main.tex              ← 可编辑源文件
│   └── main.pdf              ← 编译结果
└── Resume_{Track}_{Name}.pdf ← 命名输出（方便直接使用）
```

## 5. Compilation

```powershell
$env:PATH = "C:\Users\shido\AppData\Local\Programs\MiKTeX\miktex\bin\x64;$env:PATH"
pdflatex -interaction=nonstopmode main.tex
```

编译后清理辅助文件：`Remove-Item *.aux,*.log,*.out -Force`

## 6. Content Style Rules

### 6.1 商科简历原则
- **量化优先**：增加百分比、数字、规模（+40%、2,000+、18,000 words）
- **不写目标/目的陈述**：商科简历看结果不看意图，不写 overview/purpose 段落
- **动词开头**：每条 bullet 以强动词开头（Led、Built、Managed、Conducted）
- **一页原则**：宁可删细节也不跨页，细节留给文书

### 6.2 Bullet 写作模板
```
\resumeItemWithTitle{技能/职责领域}
  {动词 + 具体做了什么 + 量化结果/影响。}
```

示例：
```latex
\resumeItemWithTitle{Confirmation Letters}
  {Managed end-to-end external audit confirmation workflows for the prior-year cohort (30+ confirmations across bank, AR, and AP); developed working judgement on alternative procedures and escalation triggers.}
```

### 6.3 常用内容短语
- GPA: `GPA & Classification (UK 1st-class threshold ≥70%): Y1 73; Y2 74; Y3 fall semester 78`
- Scholarship: `UNNC Dean's Scholarship (Academic Year 2024–25, top 10%)`
- IELTS: `English (IELTS 7.5 – L 8.5 / R 8 / W 6.5 / S 6)`
- Dates: `Sept. 2023 -- Jun. 2027 (expected)`

## 7. Workflow

### 7.1 新建简历
1. 创建项目文件夹 `resume-{track}-{name}` 于 `C:\Users\shido\Documents\latex-projects\`
2. 写入 `main.tex`，基于模板 + 用户内容
3. 编译 → 检查页数 → 调间距（遵循 Section 3 规则）
4. 确认 1 页后，复制 PDF 到目标目录并重命名
5. 复制整个工程文件夹到目标目录

### 7.2 修改已有简历
1. 读取目标目录中的 `resume-{track}-{name}/main.tex`
2. 根据用户要求编辑 `.tex` 文件
3. 重新编译 → 检查页数 → 必要时调间距
4. 更新 `main.pdf` 和命名 PDF

### 7.3 多方向简历
同一学生申请多个方向时，为每个方向创建独立工程文件夹 + 独立 PDF：
- `resume-accounting-kaidi/` → `Resume_Accounting_KaidiGUO.pdf`
- `resume-marketing-kaidi/` → `Resume_Marketing_KaidiGUO.pdf`

Education 部分保持相同，Professional Experience / Academic Projects / Leadership 按方向调整内容侧重和排序。

## 8. Common Fixes

| 问题 | 修复 |
|---|---|
| 内容溢到第 2 页 | 降字号 10pt、收边距、缩简文本，不成功则删除次要 bullet |
| 底部大量留白 | 启用 `\flushbottom` + 双 `\vfill`（Section 3.2） |
| 上下留白不对称 | 同上 |
| Charter 字体中文不显示 | 纯英文简历不使用中文；如需中英混排改用 xeCJK + XeLaTeX |
| `\&` / `\%` / `\_` 编译报错 | 特殊字符必须转义 |
| `L'Oréal` 编译报错 | 写作 `L'Or\'{e}al` |
| 页脚空白警告 | 添加 `\setlength{\footskip}{8pt}` |
