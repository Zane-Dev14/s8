from pathlib import Path
import pypdfium2 as pdfium
import pytesseract

ROOT = Path("/Users/eric/Documents/StudyCollege/BCT")
OCR_DIR = ROOT / "ocr_work"
(OCR_DIR / "module2").mkdir(parents=True, exist_ok=True)

MODULE2_FILES = [
    ROOT / "CST428-M2-Ktunotes.in.pdf",
    ROOT / "Module II-1.pdf",
]

def ocr_pdf(pdf_path: Path, out_txt: Path, dpi: int = 250) -> None:
    pdf = pdfium.PdfDocument(str(pdf_path))
    chunks = []
    for i in range(len(pdf)):
        page = pdf[i]
        bitmap = page.render(scale=dpi / 72)
        image = bitmap.to_pil()
        text = pytesseract.image_to_string(image, lang="eng")
        chunks.append(f"\n\n===== PAGE {i + 1} =====\n{text}")
    out_txt.write_text("".join(chunks), encoding="utf-8")
    print(f"✓ {pdf_path.name} -> {out_txt.name}")

for pdf_file in MODULE2_FILES:
    if pdf_file.exists():
        out_path = OCR_DIR / "module2" / f"{pdf_file.stem.replace(' ', '_')}.txt"
        ocr_pdf(pdf_file, out_path)
    else:
        print(f"✗ File not found: {pdf_file}")

print("Module 2 OCR extraction complete!")
