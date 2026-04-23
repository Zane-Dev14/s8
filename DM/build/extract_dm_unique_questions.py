#!/usr/bin/env python3
"""Build module-wise unique question bank and topic map from DM OCR corpus."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path


MODULES = [f"Module {i}" for i in range(1, 6)]

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


KEYWORD_MODULE_MAP = {
    "Module 1": [
        "data warehouse",
        "olap",
        "oltp",
        "kdd",
        "star schema",
        "snowflake",
        "multidimensional",
        "rolap",
        "molap",
        "holap",
    ],
    "Module 2": [
        "preprocessing",
        "normalization",
        "z-score",
        "min-max",
        "sampling",
        "discretization",
        "pca",
        "missing data",
        "numerosity",
        "bin",
    ],
    "Module 3": [
        "decision tree",
        "id3",
        "sliq",
        "clustering",
        "k-means",
        "pam",
        "dbscan",
        "gain ratio",
        "confusion matrix",
        "precision",
        "recall",
    ],
    "Module 4": [
        "apriori",
        "association rule",
        "support",
        "confidence",
        "fp growth",
        "fp-growth",
        "pincer",
        "dynamic itemset",
        "partition algorithm",
        "market basket",
    ],
    "Module 5": [
        "web mining",
        "web usage",
        "web structure",
        "web content",
        "focused crawling",
        "clever",
        "hits",
        "text retrieval",
        "text mining",
        "tf-idf",
    ],
}


@dataclass
class QItem:
    module: str
    part: str
    text: str
    source: str


def clean_line(line: str) -> str:
    line = line.replace("\t", " ").replace("|", " ")
    line = re.sub(r"\s+", " ", line).strip()
    return line


def normalize(text: str) -> str:
    text = text.lower()
    text = text.replace("\u2019", "'")
    text = re.sub(r"\(\d+\)", " ", text)
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def similar(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()


def strip_noise(text: str) -> str:
    text = re.sub(r"\s*\(\d+\)\s*$", "", text)
    text = re.sub(r"\s+", " ", text).strip(" .:-")
    return text


def detect_module_from_heading(line: str) -> str | None:
    s = line.lower()
    if "module" not in s:
        return None
    if re.search(r"module\s*i\b", s) or re.search(r"module\s*1\b", s):
        return "Module 1"
    if re.search(r"module\s*ii\b", s) or re.search(r"module\s*2\b", s):
        return "Module 2"
    if re.search(r"module\s*iii\b", s) or re.search(r"module\s*3\b", s):
        return "Module 3"
    if re.search(r"module\s*iv\b", s) or re.search(r"module\s*4\b", s):
        return "Module 4"
    if re.search(r"module\s*v\b", s) or re.search(r"module\s*5\b", s):
        return "Module 5"
    return None


def infer_module_from_text(text: str) -> str:
    t = normalize(text)
    scores: dict[str, int] = {m: 0 for m in MODULES}
    for module, keys in KEYWORD_MODULE_MAP.items():
        for key in keys:
            if key in t:
                scores[module] += 1
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return "Module 3"
    return best


def extract_exam_questions(lines: list[str], source: str) -> list[QItem]:
    items: list[QItem] = []
    section = ""
    current_module = ""
    i = 0
    while i < len(lines):
        line = clean_line(lines[i])
        low = line.lower()
        if not line:
            i += 1
            continue

        if low.startswith("parta") or low.startswith("part a"):
            section = "Part A"
            i += 1
            continue
        if low.startswith("partb") or low.startswith("part b"):
            section = "Part B"
            i += 1
            continue

        mod = detect_module_from_heading(line)
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

        text_parts = [tail]
        j = i + 1
        while j < len(lines):
            nxt = clean_line(lines[j])
            if not nxt:
                j += 1
                continue
            if re.match(r"^[\'\"._-]*\s*\d{1,2}[\.,]?\s+", nxt):
                break
            if nxt.lower().startswith("part a") or nxt.lower().startswith("part b"):
                break
            if detect_module_from_heading(nxt):
                break
            if "page" in nxt.lower() and "of" in nxt.lower():
                break
            text_parts.append(nxt)
            j += 1

        text = strip_noise(" ".join(text_parts))
        if not text:
            i = j
            continue

        if section == "Part A" and 1 <= qno <= 10:
            module = PART_A_MODULE_MAP.get(qno, infer_module_from_text(text))
            items.append(QItem(module=module, part="Part A", text=text, source=source))
        elif section == "Part B" and 11 <= qno <= 20:
            module = current_module if current_module else infer_module_from_text(text)
            items.append(QItem(module=module, part="Part B", text=text, source=source))

        i = j

    return items


def extract_bulleted_questions(lines: list[str], source: str) -> list[QItem]:
    items: list[QItem] = []

    filename = source.lower()
    module_hint = None
    if "module-1" in filename:
        module_hint = "Module 1"
    elif "module-2" in filename:
        module_hint = "Module 2"
    elif "module-3" in filename or "mod3" in filename:
        module_hint = "Module 3"
    elif "module-4" in filename:
        module_hint = "Module 4"
    elif "module-5" in filename:
        module_hint = "Module 5"

    for raw in lines:
        line = clean_line(raw)
        if not line:
            continue

        # Bulleted numbered prompts near top of module/series notes.
        m = re.match(r"^(?:e\s+)?(\d{1,2})\.\s+(.+)$", line)
        if not m:
            continue

        txt = strip_noise(m.group(2))
        if len(txt) < 8:
            continue

        low = txt.lower()
        if low.startswith("step ") or low.startswith("example"):
            continue
        if low.startswith("what is") or "?" in txt or low.startswith("describe") or low.startswith("explain") or low.startswith("compare") or low.startswith("differentiate") or low.startswith("list") or low.startswith("state"):
            module = module_hint if module_hint else infer_module_from_text(txt)
            items.append(QItem(module=module, part="Part B", text=txt, source=source))

    return items


def dedupe(items: list[QItem], threshold: float = 0.89) -> tuple[dict, dict]:
    bank = {m: {"Part A": [], "Part B": []} for m in MODULES}
    sources = {m: {"Part A": defaultdict(list), "Part B": defaultdict(list)} for m in MODULES}

    for item in items:
        bucket = bank[item.module][item.part]
        duplicate = False
        for existing in bucket:
            if similar(existing, item.text) >= threshold:
                duplicate = True
                sources[item.module][item.part][existing].append(item.source)
                break

        if not duplicate:
            bucket.append(item.text)
            sources[item.module][item.part][item.text].append(item.source)

    return bank, sources


def build_topic_map(bank: dict[str, dict[str, list[str]]]) -> dict[str, list[dict[str, int]]]:
    topic_map: dict[str, list[dict[str, int]]] = {}
    for module in MODULES:
        counter: Counter[str] = Counter()
        for part in ("Part A", "Part B"):
            for q in bank[module][part]:
                n = normalize(q)
                for key in KEYWORD_MODULE_MAP[module]:
                    if key in n:
                        counter[key] += 1
        topic_map[module] = [
            {"topic": topic, "count": count}
            for topic, count in counter.most_common()
        ]
    return topic_map


def markdown_report(bank: dict[str, dict[str, list[str]]], topic_map: dict[str, list[dict[str, int]]]) -> str:
    lines: list[str] = []
    lines.append("# DM OCR Unique Question Bank and Topic Map")
    lines.append("")
    lines.append("Generated from DM OCR text corpus (modules, series, and PYQ papers).")
    lines.append("")

    for module in MODULES:
        lines.append(f"## {module}")
        lines.append("")
        lines.append("### Part A Unique Questions")
        part_a = bank[module]["Part A"]
        if part_a:
            for idx, q in enumerate(part_a, 1):
                lines.append(f"{idx}. {q}")
        else:
            lines.append("- None extracted")

        lines.append("")
        lines.append("### Part B Unique Questions")
        part_b = bank[module]["Part B"]
        if part_b:
            for idx, q in enumerate(part_b, 1):
                lines.append(f"{idx}. {q}")
        else:
            lines.append("- None extracted")

        lines.append("")
        lines.append("### Topic Frequency")
        topics = topic_map[module]
        if topics:
            for item in topics:
                lines.append(f"- {item['topic']}: {item['count']}")
        else:
            lines.append("- No keyword topics matched")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract DM unique questions and topic map from OCR outputs")
    parser.add_argument(
        "--ocr-dir",
        default="/Users/eric/Documents/StudyCollege/DM/ocr_output",
        help="Directory containing OCR .txt files",
    )
    parser.add_argument(
        "--output-dir",
        default="/Users/eric/Documents/StudyCollege/DM/build",
        help="Directory to write generated outputs",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.89,
        help="Similarity threshold for de-duplication",
    )
    args = parser.parse_args()

    ocr_dir = Path(args.ocr_dir)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    txt_files = sorted(ocr_dir.glob("*.txt"))
    if not txt_files:
        raise FileNotFoundError(f"No OCR txt files in {ocr_dir}")

    items: list[QItem] = []
    for fp in txt_files:
        lines = fp.read_text(encoding="utf-8", errors="ignore").splitlines()
        items.extend(extract_exam_questions(lines, source=fp.name))
        items.extend(extract_bulleted_questions(lines, source=fp.name))

    bank, sources = dedupe(items, threshold=args.threshold)
    topic_map = build_topic_map(bank)

    bank_path = out_dir / "dm_unique_questions.json"
    topic_path = out_dir / "dm_topic_map.json"
    src_path = out_dir / "dm_question_sources.json"
    md_path = out_dir / "DM_OCR_Unique_Question_Map.md"

    bank_path.write_text(json.dumps(bank, indent=2), encoding="utf-8")
    topic_path.write_text(json.dumps(topic_map, indent=2), encoding="utf-8")
    src_path.write_text(
        json.dumps(
            {
                module: {
                    part: {q: sorted(set(srcs)) for q, srcs in sources[module][part].items()}
                    for part in ("Part A", "Part B")
                }
                for module in MODULES
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    md_path.write_text(markdown_report(bank, topic_map), encoding="utf-8")

    print(f"Wrote {bank_path}")
    print(f"Wrote {topic_path}")
    print(f"Wrote {src_path}")
    print(f"Wrote {md_path}")
    for module in MODULES:
        print(
            f"{module}: Part A={len(bank[module]['Part A'])}, Part B={len(bank[module]['Part B'])}"
        )


if __name__ == "__main__":
    main()
