#!/usr/bin/env python3
"""Extract module-wise unique Part A / Part B questions from DataMining_combined OCR."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path


PART_A_MODULE_MAP = {
    1: "Module 1",
    2: "Module 1",
    3: "Module 2",
    4: "Module 2",
    5: "Module 3",
    6: "Module 3",
    7: "Module 4",
    8: "Module 4",
    9: "Module 5",
    10: "Module 5",
}

MODULES = [f"Module {i}" for i in range(1, 6)]


PART_B_MODULE_MAP = {
    11: "Module 1",
    12: "Module 1",
    13: "Module 2",
    14: "Module 2",
    15: "Module 3",
    16: "Module 3",
    17: "Module 4",
    18: "Module 4",
    19: "Module 5",
    20: "Module 5",
}


@dataclass
class QItem:
    module: str
    part: str
    qno: int
    text: str
    page: int


def clean_line(line: str) -> str:
    line = line.replace("\t", " ").replace("|", " ")
    line = re.sub(r"\s+", " ", line).strip()
    return line


def is_noise_line(line: str) -> bool:
    low = line.lower()
    noise_tokens = [
        "apj abdul kalam",
        "course code",
        "course name",
        "max. marks",
        "duration",
        "reg no",
        "page",
        "scheme of valuation",
        "answer key",
        "downloaded by",
        "studocu",
    ]
    if any(tok in low for tok in noise_tokens):
        return True
    if re.fullmatch(r"[0-9a-z]{8,}", low):
        return True
    if re.fullmatch(r"[\W_]+", line):
        return True
    return False


def normalize(s: str) -> str:
    s = s.lower()
    s = s.replace("\u2019", "'")
    s = re.sub(r"\b(part\s*[ab]|module\s*[ivx0-9]+|or)\b", " ", s)
    s = re.sub(r"\(\d+\)", " ", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def similar(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()


def detect_module(line: str) -> str | None:
    low = line.lower()
    if "module" not in low:
        return None
    if re.search(r"module\s*i\b", low) or re.search(r"module\s*1\b", low):
        return "Module 1"
    if re.search(r"module\s*ii\b", low) or re.search(r"module\s*2\b", low):
        return "Module 2"
    if re.search(r"module\s*iii\b", low) or re.search(r"module\s*3\b", low):
        return "Module 3"
    if re.search(r"module\s*iv\b", low) or re.search(r"module\s*4\b", low):
        return "Module 4"
    if re.search(r"module\s*v\b", low) or re.search(r"module\s*5\b", low):
        return "Module 5"
    return None


def preprocess_text(raw: str) -> str:
    text = raw.replace("\r\n", "\n")
    text = re.sub(r"PARTA", "PART A", text, flags=re.I)
    text = re.sub(r"PARTB", "PART B", text, flags=re.I)

    # Question number can appear in the same OCR line after marks (e.g. "(3) 2 Explain...").
    text = re.sub(r"(\(\d+\)|Marks)\s+((?:[1-9]|1\d|20))\s+", r"\1\n\2 ", text, flags=re.I)

    # Also split lines where next question starts after a sentence-ending punctuation.
    text = re.sub(r"([\.:;\)])\s+((?:[1-9]|1\d|20))\s+(?=[A-Za-z])", r"\1\n\2 ", text)
    return text


def clean_question_text(text: str) -> str:
    s = clean_line(text)
    s = re.sub(r"\s*\(\d+\)\s*", " ", s)
    s = re.sub(r"\bOR\b", " ", s, flags=re.I)
    s = re.sub(r"\bModule\s+[IVX0-9]+\b", " ", s, flags=re.I)
    s = re.sub(r"\bPART\s+[AB]\b", " ", s, flags=re.I)
    s = re.sub(r"\s+", " ", s).strip(" .:-")
    return s


def valid_question_text(text: str) -> bool:
    low = text.lower()
    if len(text) < 15:
        return False
    if sum(ch.isalpha() for ch in text) < 8:
        return False
    if "answer any one full question" in low:
        return False
    if "scheme of valuation" in low:
        return False
    if "one mark each" in low:
        return False
    if "page" in low and "downloaded" in low:
        return False
    return True


def parse_pages(text: str) -> list[tuple[int, list[str]]]:
    pages: list[tuple[int, list[str]]] = []
    chunks = re.split(r"^===== PAGE\s+(\d+)\s+=====$", text, flags=re.M)
    if len(chunks) <= 1:
        lines = [clean_line(x) for x in text.splitlines()]
        pages.append((1, lines))
        return pages

    # chunks format: [prefix, page_no, page_text, page_no, page_text, ...]
    i = 1
    while i < len(chunks):
        page_no = int(chunks[i])
        page_text = chunks[i + 1]
        lines = [clean_line(x) for x in page_text.splitlines()]
        pages.append((page_no, lines))
        i += 2
    return pages


def extract_questions(pages: list[tuple[int, list[str]]]) -> list[QItem]:
    out: list[QItem] = []
    section = ""
    current_module = ""

    all_lines: list[tuple[int, str]] = []
    for page_no, lines in pages:
        for line in lines:
            all_lines.append((page_no, line))

    i = 0
    while i < len(all_lines):
        page_no, line = all_lines[i]
        if not line or is_noise_line(line):
            i += 1
            continue

        low = line.lower()
        if low.startswith("parta") or low.startswith("part a"):
            section = "Part A"
            i += 1
            continue
        if low.startswith("partb") or low.startswith("part b"):
            section = "Part B"
            i += 1
            continue

        mod = detect_module(line)
        if mod:
            current_module = mod
            i += 1
            continue

        m = re.match(r"^[\'\"._-]*\s*(\d{1,2})[\.,]?\s*(.*)$", line)
        if not m:
            i += 1
            continue

        qno = int(m.group(1))
        tail = m.group(2).strip()
        if not tail:
            i += 1
            continue

        # Collect wrapped question lines.
        parts = [tail]
        j = i + 1
        while j < len(all_lines):
            _, nxt = all_lines[j]
            if not nxt:
                j += 1
                continue
            if is_noise_line(nxt):
                j += 1
                continue
            if re.match(r"^[\'\"._-]*\s*\d{1,2}[\.,]?\s+", nxt):
                break
            if nxt.lower().startswith("part a") or nxt.lower().startswith("part b"):
                break
            if detect_module(nxt):
                break
            parts.append(nxt)
            j += 1

        qtext = clean_question_text(" ".join(parts))

        if section == "Part A" and 1 <= qno <= 10 and valid_question_text(qtext):
            module = PART_A_MODULE_MAP.get(qno, "Module 1")
            out.append(QItem(module=module, part="Part A", qno=qno, text=qtext, page=page_no))
        elif section == "Part B" and 11 <= qno <= 20 and valid_question_text(qtext):
            module = PART_B_MODULE_MAP.get(qno, current_module if current_module else "Module 1")
            out.append(QItem(module=module, part="Part B", qno=qno, text=qtext, page=page_no))

        i = j

    return out


def dedupe(items: list[QItem], threshold: float) -> tuple[dict, dict]:
    data = {m: {"Part A": [], "Part B": []} for m in MODULES}
    source = {m: {"Part A": {}, "Part B": {}} for m in MODULES}

    for item in items:
        bucket = data[item.module][item.part]
        merged = None
        for existing in bucket:
            if similar(existing, item.text) >= threshold:
                merged = existing
                break

        if merged is None:
            bucket.append(item.text)
            source[item.module][item.part][item.text] = [
                {"qno": item.qno, "page": item.page}
            ]
        else:
            source[item.module][item.part][merged].append({"qno": item.qno, "page": item.page})

    return data, source


def question_markdown(data: dict) -> str:
    lines: list[str] = []
    lines.append("# DataMiningCombined Unique Questions (Module-wise)")
    lines.append("")
    for module in MODULES:
        lines.append(f"## {module}")
        lines.append("")
        lines.append("### Part A")
        if data[module]["Part A"]:
            for i, q in enumerate(data[module]["Part A"], 1):
                lines.append(f"{i}. {q}")
        else:
            lines.append("- None")
        lines.append("")
        lines.append("### Part B")
        if data[module]["Part B"]:
            for i, q in enumerate(data[module]["Part B"], 1):
                lines.append(f"{i}. {q}")
        else:
            lines.append("- None")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract unique questions from DataMining_combined OCR")
    parser.add_argument(
        "--input",
        default="/Users/eric/Documents/StudyCollege/DM/ocr_output/DataMining_combined.txt",
        help="Path to OCR txt",
    )
    parser.add_argument(
        "--output-dir",
        default="/Users/eric/Documents/StudyCollege/DM/build",
        help="Directory for outputs",
    )
    parser.add_argument("--threshold", type=float, default=0.89, help="Dedup similarity threshold")
    args = parser.parse_args()

    input_path = Path(args.input)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_text = input_path.read_text(encoding="utf-8", errors="ignore")
    text = preprocess_text(raw_text)
    pages = parse_pages(text)
    items = extract_questions(pages)
    data, source = dedupe(items, args.threshold)

    json_path = out_dir / "DataMiningCombined_unique_questions.json"
    src_path = out_dir / "DataMiningCombined_question_sources.json"
    md_path = out_dir / "DataMiningCombined_unique_questions.md"

    json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    src_path.write_text(json.dumps(source, indent=2), encoding="utf-8")
    md_path.write_text(question_markdown(data), encoding="utf-8")

    print(f"Wrote {json_path}")
    print(f"Wrote {src_path}")
    print(f"Wrote {md_path}")
    for module in MODULES:
        print(
            f"{module}: Part A={len(data[module]['Part A'])}, Part B={len(data[module]['Part B'])}"
        )


if __name__ == "__main__":
    main()
