---
name: overleaf
description: Local LaTeX editor & compiler. 本地 LaTeX 写作/编译/模板/参考文献管理。自动触发关键词：latex、overleaf、tex、编译、pdf、文献、论文、acm、ieee、article、beamer、幻灯片、简历、cv、xelatex、pdflatex、biblatex、bibtex、模板、template、documentclass。
---

# Overleaf Local — LaTeX Skill

## 0. Overview

This skill provides local Overleaf-like LaTeX capabilities through CLI. The agent acts as a LaTeX assistant that can create projects, write documents, compile PDFs, manage bibliographies, and apply templates.

Core workflow:
```
User request → Agent writes/edits .tex → pdflatex/xelatex compile → PDF output → open with default viewer
```

## 1. Environment

| Component | Path |
|---|---|
| MiKTeX bin | `C:\Users\shido\AppData\Local\Programs\MiKTeX\miktex\bin\x64\` |
| LaTeX workspace | `C:\Users\shido\Documents\latex-projects\` |
| Templates | `C:\Users\shido\Documents\latex-projects\templates\` |

Key executables (prepend the MiKTeX bin path):
- `pdflatex.exe` — PDFLaTeX compiler
- `xelatex.exe` — XeLaTeX (Unicode/OpenType font support)
- `lualatex.exe` — LuaLaTeX
- `bibtex.exe` — BibTeX bibliography processor
- `biber.exe` — Biber (for biblatex)

**IMPORTANT:** Always use `$env:PATH = "C:\Users\shido\AppData\Local\Programs\MiKTeX\miktex\bin\x64;$env:PATH"` at the start of any PowerShell command that invokes LaTeX tools. This ensures the MiKTeX bin is in PATH for the session.

## 2. Project Management

### 2.1 Create a new project

To create a new project, create a directory under `C:\Users\shido\Documents\latex-projects\` with the project name, then create the main `.tex` file and any supporting files.

```
project-name/
  main.tex          # entry file
  refs.bib          # bibliography (optional)
  img/              # images (optional)
  chapters/         # multi-file projects (optional)
```

### 2.2 Standard LaTeX template

Use this minimal template when creating a new article/document:

```latex
\documentclass[a4paper,12pt]{article}

% === Encoding & Language ===
\usepackage[UTF8]{ctex}        % Chinese support (remove if not needed)
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage[hidelinks]{hyperref}
\usepackage{geometry}
\geometry{margin=2.5cm}

% === Bibliography ===
\usepackage[backend=biber,style=ieee]{biblatex}
\addbibresource{refs.bib}

% === Metadata ===
\title{Document Title}
\author{Author Name}
\date{\today}

\begin{document}
\maketitle

% content here

\printbibliography
\end{document}
```

For pure English documents, remove `\usepackage[UTF8]{ctex}` and use `\usepackage[english]{babel}`.

### 2.3 Multi-file projects

For large documents (thesis, book, long report), use `\input{}` or `\include{}`:

```latex
\documentclass{report}
% ... packages ...
\begin{document}
\include{chapters/intro}
\include{chapters/methods}
\include{chapters/results}
\include{chapters/conclusion}
\end{document}
```

## 3. Compilation

### 3.1 Single-pass (pdflatex)

```powershell
$env:PATH = "C:\Users\shido\AppData\Local\Programs\MiKTeX\miktex\bin\x64;$env:PATH"
pdflatex -interaction=nonstopmode -output-directory=build main.tex
```

### 3.2 Full compilation cycle (pdflatex → bibtex → pdflatex × 2)

For documents with bibliography:

```powershell
$env:PATH = "C:\Users\shido\AppData\Local\Programs\MiKTeX\miktex\bin\x64;$env:PATH"
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

### 3.3 Full cycle with biber (biblatex)

```powershell
$env:PATH = "C:\Users\shido\AppData\Local\Programs\MiKTeX\miktex\bin\x64;$env:PATH"
pdflatex -interaction=nonstopmode main.tex
biber main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

### 3.4 XeLaTeX (recommended for CJK/multilingual)

```powershell
$env:PATH = "C:\Users\shido\AppData\Local\Programs\MiKTeX\miktex\bin\x64;$env:PATH"
xelatex -interaction=nonstopmode main.tex
```

### 3.5 Clean build artifacts

```powershell
Remove-Item -Force *.aux,*.log,*.out,*.toc,*.bbl,*.blg,*.run.xml,*.bcf -ErrorAction SilentlyContinue
```

### 3.6 Open PDF

After successful compilation, open the PDF with the default viewer:

```powershell
Start-Process main.pdf
```

Or for build output directory:

```powershell
Start-Process build\main.pdf
```

## 4. Document Classes & Templates

### 4.1 Common document classes

| Class | Use |
|---|---|
| `article` | Papers, short docs |
| `report` | Longer reports, thesis chapters |
| `book` | Books, PhD thesis |
| `beamer` | Presentation slides |
| `letter` | Letters |
| `moderncv` | CV/Resume |

### 4.2 Beamer (slides)

```latex
\documentclass{beamer}
\usetheme{Madrid}
\title{Presentation Title}
\author{Author}
\date{\today}

\begin{document}
\begin{frame}
  \titlepage
\end{frame}

\begin{frame}{Frame Title}
  \begin{itemize}
    \item Point 1
    \item Point 2
  \end{itemize}
\end{frame}
\end{document}
```

### 4.3 ACM template

For ACM conference papers, use `\documentclass[sigconf]{acmart}`. The `acmart` class is available in MiKTeX.

### 4.4 IEEE template

For IEEE papers, use `\documentclass[conference]{IEEEtran}`.

### 4.5 Resume/CV

```latex
\documentclass[11pt,a4paper]{moderncv}
\moderncvstyle{banking}
\name{First}{Last}
% ... details ...
\begin{document}
\makecvtitle
\section{Education}
\section{Experience}
\end{document}
```

## 5. Bibliography Management

### 5.1 BibLaTeX (recommended)

In preamble:
```latex
\usepackage[backend=biber,style=ieee]{biblatex}
\addbibresource{refs.bib}
```

Print bibliography:
```latex
\printbibliography
```

### 5.2 refs.bib format

```bibtex
@article{key2024,
  author  = {Author Name},
  title   = {Paper Title},
  journal = {Journal Name},
  year    = {2024},
  volume  = {1},
  pages   = {1--10},
  doi     = {10.xxxx/xxxxx}
}

@book{key2023,
  author = {Author},
  title  = {Book Title},
  year   = {2023},
  publisher = {Publisher}
}
```

### 5.3 Citation commands

| Command | Output |
|---|---|
| `\cite{key}` | [1] |
| `\textcite{key}` | Author [1] |
| `\parencite{key}` | [1] |
| `\citeauthor{key}` | Author |
| `\citeyear{key}` | 2024 |

## 6. Chinese/English Documents

### 6.1 Pure Chinese with ctex

```latex
\documentclass[UTF8]{ctexart}
\begin{document}
中文内容
\end{document}
```

### 6.2 Chinese + English with xeCJK (XeLaTeX)

```latex
\documentclass{article}
\usepackage{xeCJK}
\setCJKmainfont{SimSun}
\begin{document}
中文和English混排
\end{document}
```

## 7. Tables

```latex
\begin{table}[htbp]
  \centering
  \caption{Table caption}
  \begin{tabular}{|l|c|r|}
    \hline
    Left & Center & Right \\
    \hline
    A & 1 & 2.3 \\
    B & 4 & 5.6 \\
    \hline
  \end{tabular}
\end{table}
```

## 8. Figures

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{img/figure.png}
  \caption{Figure caption}
  \label{fig:myfigure}
\end{figure}
```

## 9. Math

```latex
% Inline: $E = mc^2$
% Display:
\begin{equation}
  \sum_{i=1}^{n} x_i = \frac{n(n+1)}{2}
  \label{eq:sum}
\end{equation}
```

Use `align` for multi-line equations:
```latex
\begin{align}
  a &= b + c \\
  d &= e + f
\end{align}
```

## 10. Common Errors & Fixes

| Error | Fix |
|---|---|
| `! LaTeX Error: File 'xxx.sty' not found` | MiKTeX auto-installs packages on first use. If it fails, run `mpm --install=xxx` |
| `! Undefined control sequence` | Typo in command name or missing `\usepackage` |
| `! Missing $ inserted` | Math mode required — wrap in `$...$` |
| `! Extra alignment tab` | Too many `&` in table row |
| `! Misplaced \noalign` | Missing `\\` at end of `\hline` row |
| BibTeX/Biber errors | Check `refs.bib` syntax, re-run full compilation cycle |
| Chinese characters not rendering | Use `ctex` package + xelatex, or `\usepackage[UTF8]{ctex}` |

### Package installation

If MiKTeX doesn't auto-install a package:
```powershell
$env:PATH = "C:\Users\shido\AppData\Local\Programs\MiKTeX\miktex\bin\x64;$env:PATH"
mpm --install=packagename
```

## 11. Workflow Commands (Quick Reference)

For the agent, when a user asks to:
- **Create a new project**: Make directory under `latex-projects/`, write `main.tex` with template, create `refs.bib`
- **Compile**: Run pdflatex/xelatex with PATH set, show errors if any
- **Open PDF**: `Start-Process main.pdf`
- **Add bibliography**: Edit `refs.bib`, run full compile cycle
- **Change template**: Replace `\documentclass` and adjust packages
- **Add figure**: Create `img/` directory, use `\includegraphics`
