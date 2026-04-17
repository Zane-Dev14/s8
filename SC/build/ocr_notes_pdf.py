from __future__ import annotations

import argparse
import json
from pathlib import Path

import pypdfium2 as pdfium
import pytesseract
from PIL import ImageOps


def ocr_page(page: pdfium.PdfPage, scale: float) -> str:
    bitmap = page.render(scale=scale)
    image = bitmap.to_pil()
    gray = ImageOps.grayscale(image)

    text = pytesseract.image_to_string(gray, config="--oem 3 --psm 6")
    if len(text.strip()) < 60:
        text = pytesseract.image_to_string(gray, config="--oem 3 --psm 11")
    return text


def ocr_pdf(pdf_path: Path, out_txt: Path, out_json: Path, scale: float) -> None:
    doc = pdfium.PdfDocument(str(pdf_path))
    pages = []
    chunks = []

    for i in range(len(doc)):
        text = ocr_page(doc[i], scale=scale)
        pages.append({"page_number": i + 1, "text": text})
        chunks.append(f"\n===== PAGE {i + 1} =====\n")
        chunks.append(text.rstrip() + "\n")
        if (i + 1) % 10 == 0:
            print(f"Processed {i + 1}/{len(doc)} pages for {pdf_path.name}")

    out_txt.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_txt.write_text("".join(chunks), encoding="utf-8")
    out_json.write_text(
        json.dumps(
            {
                "source_pdf": str(pdf_path),
                "page_count": len(doc),
                "pages": pages,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="OCR a notes PDF to text/json")
    parser.add_argument("--pdf", required=True, help="Absolute path to source PDF")
    parser.add_argument("--out-txt", required=True, help="Absolute path to output TXT")
    parser.add_argument("--out-json", required=True, help="Absolute path to output JSON")
    parser.add_argument("--scale", type=float, default=2.0)
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    out_txt = Path(args.out_txt)
    out_json = Path(args.out_json)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    ocr_pdf(pdf_path=pdf_path, out_txt=out_txt, out_json=out_json, scale=args.scale)
    print(f"Wrote {out_txt}")
    print(f"Wrote {out_json}")


if __name__ == "__main__":
    main()
