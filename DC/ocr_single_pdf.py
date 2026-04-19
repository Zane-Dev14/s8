#!/usr/bin/env python3
"""OCR a single PDF using pypdfium2 + pytesseract."""

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
    if len(text.strip()) < 40:
        text = pytesseract.image_to_string(gray, config="--oem 3 --psm 11")
    return text


def ocr_pdf(pdf_path: Path, output_dir: Path, scale: float) -> dict:
    doc = pdfium.PdfDocument(str(pdf_path))
    page_count = len(doc)

    pages = []
    txt_parts = []

    for page_index in range(page_count):
        page = doc[page_index]
        text = ocr_page(page, scale=scale)
        pages.append({"page_number": page_index + 1, "text": text})
        txt_parts.append(f"\n===== PAGE {page_index + 1} =====\n")
        txt_parts.append(text.rstrip() + "\n")

    safe_name = pdf_path.stem.replace(" ", "_")
    txt_path = output_dir / f"{safe_name}.txt"
    json_path = output_dir / f"{safe_name}.json"

    txt_path.write_text("".join(txt_parts), encoding="utf-8")
    json_path.write_text(
        json.dumps(
            {
                "source_pdf": str(pdf_path),
                "page_count": page_count,
                "pages": pages,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    return {
        "pdf": str(pdf_path),
        "page_count": page_count,
        "txt_output": str(txt_path),
        "json_output": str(json_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="OCR one PDF")
    parser.add_argument("--pdf", required=True, help="Absolute path to source PDF")
    parser.add_argument(
        "--output-dir",
        default="/Users/eric/Documents/StudyCollege/DC/ocr_output",
        help="Directory for OCR outputs",
    )
    parser.add_argument("--scale", type=float, default=3.0, help="Rendering scale")
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    result = ocr_pdf(pdf_path=pdf_path, output_dir=output_dir, scale=args.scale)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
