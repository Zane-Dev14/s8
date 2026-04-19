#!/usr/bin/env python3
"""Extract module-wise unique Part A/Part B questions from OCR text."""

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


@dataclass
class QItem:
    part: str
    module: str
    qno: int
    text: str


def normalize_text(text: str) -> str:
    text = text.lower()
    text = text.replace("|", " ")
    text = re.sub(r"\(\d+\)", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-z0-9 ]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def similar(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize_text(a), normalize_text(b)).ratio()


def clean_line(line: str) -> str:
    line = line.replace("\t", " ")
    line = re.sub(r"\s+", " ", line).strip()
    return line


def detect_module(line: str, current: str) -> str:
    s = line.lower().replace("|", "i")
    if "module" not in s:
        return current
    if re.search(r"module\s*i\b", s):
        return "Module 1"
    if re.search(r"module\s*ii\b", s):
        return "Module 2"
    if re.search(r"module\s*iii\b", s) or re.search(r"module\s*ill\b", s):
        return "Module 3"
    if re.search(r"module\s*iv\b", s):
        return "Module 4"
    if re.search(r"module\s*v\b", s):
        return "Module 5"
    return current


def extract_questions(lines: list[str]) -> list[QItem]:
    items: list[QItem] = []
    section = ""
    current_module = ""

    i = 0
    while i < len(lines):
        line = clean_line(lines[i])
        if not line:
            i += 1
            continue

        low = line.lower()
        if low.startswith("parta") or low.startswith("part a"):
            section = "A"
            i += 1
            continue
        if low.startswith("partb") or low.startswith("part b"):
            section = "B"
            i += 1
            continue

        current_module = detect_module(line, current_module)

        # Match question starts: 1 ..., 11 a) ..., 14. a) ...
        m = re.match(r"^[\'\"._-]*\s*(\d{1,2})[\.,]?\s*(.*)$", line)
        if not m:
            i += 1
            continue

        qno = int(m.group(1))
        tail = m.group(2).strip()

        if section == "A" and 1 <= qno <= 10:
            text_parts = [tail]
            j = i + 1
            while j < len(lines):
                nxt = clean_line(lines[j])
                if not nxt:
                    j += 1
                    continue
                if re.match(r"^[\'\"._-]*\s*\d{1,2}[\.,]?\s+", nxt):
                    break
                if nxt.lower().startswith("part b") or nxt.lower().startswith("module"):
                    break
                if "page" in nxt.lower() and "of" in nxt.lower():
                    break
                text_parts.append(nxt)
                if re.search(r"\(\d+\)\s*$", nxt):
                    break
                j += 1
            text = clean_line(" ".join(text_parts))
            mod = PART_A_MODULE_MAP.get(qno, "Module 1")
            items.append(QItem(part="Part A", module=mod, qno=qno, text=text))
            i = j
            continue

        if section == "B" and 11 <= qno <= 20:
            text_parts = [tail]
            j = i + 1
            while j < len(lines):
                nxt = clean_line(lines[j])
                if not nxt:
                    j += 1
                    continue
                if re.match(r"^[\'\"._-]*\s*(1[1-9]|20)[\.,]?\s+", nxt):
                    break
                if nxt.lower().startswith("module"):
                    break
                if nxt.lower() == "or" or nxt.lower().startswith("or"):
                    text_parts.append("OR")
                    j += 1
                    continue
                if "page" in nxt.lower() and "of" in nxt.lower():
                    break
                # Keep subparts and wrapped lines.
                text_parts.append(nxt)
                j += 1
            text = clean_line(" ".join(text_parts))
            mod = current_module if current_module else "Module 1"
            items.append(QItem(part="Part B", module=mod, qno=qno, text=text))
            i = j
            continue

        i += 1

    return items


def dedupe(items: list[QItem], threshold: float = 0.9) -> dict[str, dict[str, list[str]]]:
    out: dict[str, dict[str, list[str]]] = {
        "Module 1": {"Part A": [], "Part B": []},
        "Module 2": {"Part A": [], "Part B": []},
        "Module 3": {"Part A": [], "Part B": []},
        "Module 4": {"Part A": [], "Part B": []},
        "Module 5": {"Part A": [], "Part B": []},
    }

    for item in items:
        bucket = out[item.module][item.part]
        exists = False
        for existing in bucket:
            if similar(existing, item.text) >= threshold:
                exists = True
                break
        if not exists:
            # Remove ending mark tag for cleaner list.
            cleaned = re.sub(r"\s*\(\d+\)\s*$", "", item.text).strip()
            bucket.append(cleaned)

    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract unique questions from OCR text")
    parser.add_argument("--input", required=True, help="OCR TXT input path")
    parser.add_argument("--output", required=True, help="Output JSON path")
    parser.add_argument("--threshold", type=float, default=0.9, help="Similarity threshold")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    lines = input_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    items = extract_questions(lines)
    data = dedupe(items, threshold=args.threshold)

    output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
