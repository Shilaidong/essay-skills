# Overleaf Local Environment Setup Guide

This guide explains how to set up a local LaTeX development environment that replicates Overleaf's functionality on Windows.

## Prerequisites

- Windows 10/11
- About 2-3 GB free disk space (for MiKTeX + packages)
- Internet connection for package downloads

---

## Step 1: Install MiKTeX

MiKTeX is the LaTeX distribution that provides the compiler (`pdflatex`, `xelatex`, etc.) and all LaTeX packages.

1. Go to [https://miktex.org/download](https://miktex.org/download)
2. Download the **MiKTeX Net Installer** (Windows)
3. Run the installer
4. Choose **"Complete MiKTeX"** installation (recommended) or "Basic MiKTeX"
5. Set install path (default: `C:\Users\<username>\AppData\Local\Programs\MiKTeX`)
6. **Important:** During installation, the option "Install missing packages on-the-fly" should be set to **"Yes"** or **"Ask me first"**
7. Complete the installation

### Verify MiKTeX installation

Open PowerShell and run:

```powershell
$env:PATH = "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64;$env:PATH"
pdflatex --version
```

If you see version info, MiKTeX is installed correctly.

---

## Step 2: (Optional) Install VS Code with LaTeX Workshop

VS Code + LaTeX Workshop extension provides an Overleaf-like editing experience with live preview, auto-complete, and one-click compilation.

1. Download VS Code: [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. Install and launch VS Code
3. Press `Ctrl+Shift+X` to open Extensions panel
4. Search and install **"LaTeX Workshop"** by James Yu
5. (Optional) Install **"vscode-pdf"** for viewing PDFs inside VS Code

### VS Code settings.json

To integrate LaTeX Workshop with MiKTeX, add this to your VS Code settings (`Ctrl+Shift+P` → "Preferences: Open Settings (JSON)"):

```json
{
  "latex-workshop.latex.recipes": [
    {
      "name": "pdflatex -> bibtex -> pdflatex * 2",
      "tools": ["pdflatex", "bibtex", "pdflatex", "pdflatex"]
    },
    {
      "name": "xelatex",
      "tools": ["xelatex"]
    },
    {
      "name": "latexmk",
      "tools": ["latexmk"]
    }
  ],
  "latex-workshop.latex.tools": [
    {
      "name": "pdflatex",
      "command": "pdflatex",
      "args": ["-interaction=nonstopmode", "-synctex=1", "%DOC%"]
    },
    {
      "name": "bibtex",
      "command": "bibtex",
      "args": ["%DOCFILE%"]
    },
    {
      "name": "xelatex",
      "command": "xelatex",
      "args": ["-interaction=nonstopmode", "-synctex=1", "%DOC%"]
    },
    {
      "name": "latexmk",
      "command": "latexmk",
      "args": ["-pdflatex", "-interaction=nonstopmode", "-synctex=1", "%DOC%"]
    }
  ],
  "latex-workshop.view.pdf.viewer": "tab"
}
```

---

## Step 3: Verify the Full Chain

Create a test project and compile it to verify everything works.

```powershell
# Create workspace directory
New-Item -ItemType Directory -Path "$env:USERPROFILE\Documents\latex-projects\test" -Force

# Create main.tex
@'
\documentclass[a4paper,12pt]{article}
\usepackage[UTF8]{ctex}
\usepackage{amsmath}
\title{Test Document}
\author{Test}
\begin{document}
\maketitle
\section{Hello}
中文测试 \LaTeX\ 编译成功。
\begin{equation}
  E = mc^2
\end{equation}
\end{document}
'@ | Set-Content -Path "$env:USERPROFILE\Documents\latex-projects\test\main.tex" -Encoding UTF8

# Compile with xelatex
$env:PATH = "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64;$env:PATH"
Set-Location "$env:USERPROFILE\Documents\latex-projects\test"
xelatex -interaction=nonstopmode main.tex

# Open PDF
Start-Process main.pdf
```

If you see a PDF with Chinese and English text, everything is working.

---

## Step 4: Directory Structure

Recommended project layout:

```
~/Documents/latex-projects/
  templates/               # reusable templates
    article-template.tex
    beamer-template.tex
  project-a/               # one folder per project
    main.tex
    refs.bib
    img/
      figure1.png
    chapters/
      intro.tex
      methods.tex
    build/                 # compiled output (optional)
  project-b/
    ...
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `'pdflatex' is not recognized` | MiKTeX not in PATH. Run: `$env:PATH = "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64;$env:PATH"` |
| `File 'xxx.sty' not found` | Package not installed. Run: `mpm --install=xxx` |
| Chinese characters show as blanks | Use `xelatex` instead of `pdflatex`, or add `\usepackage[UTF8]{ctex}` |
| `! LaTeX Error: Too many symbols` | Missing math mode `$...$` |
| PDF not updating | Delete `.aux` and `.log` files, recompile twice |
| Font not found | Use system fonts: `\setCJKmainfont{SimSun}` with `xeCJK` package |
| `biber` not found | Install biblatex package: `mpm --install=biblatex` |

---

## Quick Reference

```powershell
# Set PATH (run once per session)
$env:PATH = "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64;$env:PATH"

# Compile (simple)
xelatex -interaction=nonstopmode main.tex

# Compile with bib (full cycle)
pdflatex -interaction=nonstopmode main.tex
biber main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex

# Open PDF
Start-Process main.pdf

# Install a package
mpm --install=packagename

# Clean temp files
Remove-Item -Force *.aux,*.log,*.out,*.toc,*.bbl,*.blg,*.run.xml,*.bcf -ErrorAction SilentlyContinue
```
