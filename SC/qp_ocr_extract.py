#!/usr/bin/env python3
"""OCR all PDF question papers in SC/QP using pypdfium2 + pytesseract."""

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

    # Basic preprocessing for exam-paper scans.
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
        pages.append(
            {
                "page_number": page_index + 1,
                "text": text,
            }
        )

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
    parser = argparse.ArgumentParser(description="OCR SC question paper PDFs")
    parser.add_argument(
        "--input-dir",
        default="/Users/eric/Documents/StudyCollege/SC/QP",
        help="Directory containing PDF files",
    )
    parser.add_argument(
        "--output-dir",
        default="/Users/eric/Documents/StudyCollege/SC/QP/ocr_output",
        help="Directory for OCR outputs",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=3.0,
        help="Rendering scale for PDF pages",
    )
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(list(input_dir.glob("*.pdf")) + list(input_dir.glob("*.PDF")))
    if not pdfs:
        raise FileNotFoundError(f"No PDFs found in {input_dir}")

    run_summary = []
    for pdf_path in pdfs:
        result = ocr_pdf(pdf_path=pdf_path, output_dir=output_dir, scale=args.scale)
        run_summary.append(result)
        print(
            f"OCR done: {pdf_path.name} | pages={result['page_count']} | output={result['txt_output']}"
        )

    summary_path = output_dir / "ocr_run_summary.json"
    summary_path.write_text(json.dumps(run_summary, indent=2), encoding="utf-8")
    print(f"Summary written to {summary_path}")


if __name__ == "__main__":
    main()
