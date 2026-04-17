from pathlib import Path

import pypdfium2 as pdfium
import pytesseract
from PIL import Image

ROOT = Path("/Users/eric/Documents/StudyCollege/BCT")
OCR_DIR = ROOT / "ocr_work"
(OCR_DIR / "qp").mkdir(parents=True, exist_ok=True)
(OCR_DIR / "module1").mkdir(parents=True, exist_ok=True)
(OCR_DIR / "module2").mkdir(parents=True, exist_ok=True)

QP_FILES = [
    ROOT / "qp" / "CST428-QP May 2024.pdf",
    ROOT / "qp" / "June 2023 Regular.pdf",
    ROOT / "qp" / "October 2023 Supplementary.pdf",
    ROOT / "qp" / "CST428-SCHEME May 2024.pdf",
]

MODULE1_FILES = [
    ROOT / "CST428-M1-Ktunotes.in.pdf",
    ROOT / "Module 1.pdf",
]

MODULE2_FILES = [
    ROOT / "CST428-M2-Ktunotes.in.pdf",
    ROOT / "Module II-1.pdf",
]


def ocr_pdf(pdf_path: Path, out_txt: Path, dpi: int = 250) -> None:
    pdf = pdfium.PdfDocument(str(pdf_path))
    chunks: list[str] = []
    for i in range(len(pdf)):
        page = pdf[i]
        bitmap = page.render(scale=dpi / 72)
        image = bitmap.to_pil()
        text = pytesseract.image_to_string(image, lang="eng")
        chunks.append(f"\n\n===== PAGE {i + 1} =====\n{text}")
    out_txt.write_text("".join(chunks), encoding="utf-8")


for pdf_file in QP_FILES:
    out_path = OCR_DIR / "qp" / f"{pdf_file.stem.replace(' ', '_')}.txt"
    ocr_pdf(pdf_file, out_path)
    print(f"OCR done: {pdf_file.name} -> {out_path.name}")

for pdf_file in MODULE1_FILES:
    out_path = OCR_DIR / "module1" / f"{pdf_file.stem.replace(' ', '_')}.txt"
    ocr_pdf(pdf_file, out_path)
    print(f"OCR done: {pdf_file.name} -> {out_path.name}")

for pdf_file in MODULE2_FILES:
    out_path = OCR_DIR / "module2" / f"{pdf_file.stem.replace(' ', '_')}.txt"
    ocr_pdf(pdf_file, out_path)
    print(f"OCR done: {pdf_file.name} -> {out_path.name}")

img_path = ROOT / "qp" / "IMG-20250403-WA0007.jpg"
img_text = pytesseract.image_to_string(Image.open(img_path), lang="eng")
img_out = OCR_DIR / "qp" / "IMG-20250403-WA0007.txt"
img_out.write_text(img_text, encoding="utf-8")
print(f"OCR done: {img_path.name} -> {img_out.name}")

print("All OCR completed.")
