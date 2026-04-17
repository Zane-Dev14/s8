# Automated Blockchain Notes Generator: Prompt Guide

This file provides the explicit instructions, python tools, and prompts required to reproduce the exact pipeline used to generate the "Important Notes All Modules" PDFs from raw University Question Paper and Syllabus PDFs. 

## 1. Prerequisites
Ensure you have the following installed in your VS Code terminal (or Python Virtual Environment):
```bash
# Python dependencies for PDF OCR and Regex parsing
pip install pypdfium2 pytesseract
# Tesseract engine (on macOS)
brew install tesseract
# LaTeX Engine (for compiling .tex to .pdf)
brew install --cask mactex
```

## 2. Directory Structure Setup
Your workspace should ideally look like this:
```text
CST428/
  ├── qp/                     # Put raw Question Paper PDFs here
  ├── syllabus.pdf            # Your course syllabus
  ├── ocr_work/               # Temporary folder for text extraction
  │   └── extract_qp.py       # The python OCR script
  └── Important Notes All Modules/  # Output folder for LaTeX + PDFs
```

## 3. The OCR Text Extraction Script (`extract_qp.py`)
Save this as `ocr_work/extract_qp.py`. This reads every PDF in your `qp/` folder and saves text files.
```python
import os
import pypdfium2 as pdfium
import pytesseract
from PIL import Image
import io

def pdf_to_text(pdf_path):
    text = ""
    pdf = pdfium.PdfDocument(pdf_path)
    for i in range(len(pdf)):
        page = pdf.get_page(i)
        # Render page to image (scale 2 for better OCR)
        pil_image = page.render(scale=2).to_pil()
        # Extract text via Tesseract
        text += pytesseract.image_to_string(pil_image) + "\n\n"
        page.close()
    pdf.close()
    return text

qp_dir = "../qp"
for file in os.listdir(qp_dir):
    if file.endswith(".pdf"):
        path = os.path.join(qp_dir, file)
        out_path = f"{file}_ocr.txt"
        print(f"Extracting {file}...")
        txt = pdf_to_text(path)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(txt)
        print(f"Saved {out_path}")
```
Run `python ocr_work/extract_qp.py` to generate the `.txt` Question corpus.

## 4. The Subagent / AI Prompt
Once you have the text files, pass the following **exact prompt** to your AI Coding Assistant (e.g., GitHub Copilot, using the Subagent or standard chat window):

> **Prompt:**
> "I have a folder `ocr_work/` containing OCR text data of my university question papers. I also have my `syllabus.pdf`. 
> 
> My goal is to generate extremely high-quality, professional LaTeX study guides (using the `article` class) for each Module (Module 1 through 5).
> 
> **Instructions for the AI:**
> 1. Use an internal subagent or robust reading tool to parse all the `.txt` files in `ocr_work/` and extract every 3-mark and 14-mark question mapped by their Module. Include the Scheme/Answers if available.
> 2. Create individual `.tex` files (e.g., `Module1_Topic_Notes.tex`) in `Important Notes All Modules/`.
> 3. Each document must have a `\section{Module X Topic Map From Previous Questions}`.
> 4. Then, a `\section{Core Theory}` explaining the syllabus concepts clearly in bolded bullet points.
> 5. Finally, a `\section{Solved Question Papers}`. Divide this into `\subsection{Part A: 3-Mark Questions}` and `\subsection{Part B: 14-Mark Questions}`.
> 6. Under each question heading (e.g., `\subsubsection*{What is...}`), write the answer purely as a `\begin{itemize}` bulleted list. 
> 7. Do **NOT** include any meta-text like 'write minimum 18 bullet points'. Just naturally list out the detailed points. 
> 8. If a diagram is required, DO NOT say 'Refer to Section 3'. Instead, draw the diagram inline right under the answer using LaTeX text boxes (`\begin{center}\framebox[0.9\linewidth]{ ... }\end{center}`).
> 9. Finally, run `pdflatex -interaction=batchmode` in the terminal to compile all 5 PDFs for me."

## 5. Post-Generation Check
If the AI accidentally includes meta-instructions (like "Write 18 bullet points"), you can use this quick python regex command in the terminal to strip them from all files without manually editing everything:

```bash
python -c "import re, glob; [open(f, 'w').write(re.sub(r'\\\\textbf\{Write[^}]*bullet points:?\}', '', open(f).read())) for f in glob.glob('Important Notes All Modules/*.tex')]"
```

Then recompile:
```bash
cd "Important Notes All Modules" && for f in *.tex; do pdflatex -interaction=batchmode "$f"; done
```