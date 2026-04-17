from pathlib import Path
import json
import pypdfium2 as pdfium
import pytesseract
from PIL import ImageOps

PDF_PATH = Path('/Users/eric/Documents/StudyCollege/SC/SC - M3 -Ktunotes.in.pdf')
OUT_TXT = Path('/Users/eric/Documents/StudyCollege/SC/build/M3_pdf_source.txt')
OUT_JSON = Path('/Users/eric/Documents/StudyCollege/SC/build/M3_pdf_source.json')


def ocr_page(page, scale=2.0):
    bitmap = page.render(scale=scale)
    image = bitmap.to_pil()
    gray = ImageOps.grayscale(image)
    text = pytesseract.image_to_string(gray, config='--oem 3 --psm 6')
    if len(text.strip()) < 60:
        text = pytesseract.image_to_string(gray, config='--oem 3 --psm 11')
    return text


def main():
    doc = pdfium.PdfDocument(str(PDF_PATH))
    pages = []
    parts = []

    for i in range(len(doc)):
        text = ocr_page(doc[i], scale=2.0)
        pages.append({"page_number": i + 1, "text": text})
        parts.append(f"\n===== PAGE {i + 1} =====\n")
        parts.append(text.rstrip() + "\n")
        if (i + 1) % 10 == 0:
            print(f"Processed {i + 1}/{len(doc)} pages")

    OUT_TXT.write_text("".join(parts), encoding="utf-8")
    OUT_JSON.write_text(
        json.dumps(
            {
                "source_pdf": str(PDF_PATH),
                "page_count": len(doc),
                "pages": pages,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {OUT_TXT}")
    print(f"Wrote {OUT_JSON}")


if __name__ == '__main__':
    main()
