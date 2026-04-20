#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from pathlib import Path

FILES = [
    Path("/Users/eric/Documents/StudyCollege/SC/QP/ocr_output/CST444_SOFT_COMPUTING,_JUNE_2023.txt"),
    Path("/Users/eric/Documents/StudyCollege/SC/QP/ocr_output/CST444_SOFT_COMPUTING,_MAY_2024.txt"),
]

ROMAN_TO_INT = {"i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5}


def norm(s: str) -> str:
    s = s.lower()
    s = re.sub(r"\(\d+\)", " ", s)
    s = s.replace("—", " ").replace("-", " ")
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def similar(a: str, b: str) -> float:
    return SequenceMatcher(None, norm(a), norm(b)).ratio()


def clean(line: str) -> str:
    return " ".join(line.split())


def main() -> None:
    questions = {f"Module {i}": {"Part A": [], "Part B": []} for i in range(1, 6)}

    for fp in FILES:
        lines = fp.read_text(encoding="utf-8", errors="ignore").splitlines()
        section = None
        current_module = None
        i = 0
        while i < len(lines):
            line = clean(lines[i])
            low = line.lower()
            if not line:
                i += 1
                continue

            if low.startswith("part a"):
                section = "A"
                i += 1
                continue
            if low.startswith("part b"):
                section = "B"
                i += 1
                continue

            m_module = re.search(r"module\s+([ivx]+)", low)
            if m_module:
                current_module = ROMAN_TO_INT.get(m_module.group(1), current_module)
                i += 1
                continue

            if section == "A":
                m_a = re.match(r"^[\'\"._-]*\s*(\d{1,2})\s+(.*)$", line)
                if m_a:
                    qno = int(m_a.group(1))
                    if 1 <= qno <= 10:
                        text = m_a.group(2).strip()
                        j = i + 1
                        while j < len(lines):
                            nxt = clean(lines[j])
                            low_nxt = nxt.lower()
                            if not nxt:
                                j += 1
                                continue
                            if re.match(r"^\d{1,2}\s+", nxt):
                                break
                            if low_nxt.startswith("part b"):
                                break
                            if "module" in low_nxt:
                                break
                            if "page" in low_nxt and "of" in low_nxt:
                                break
                            text += " " + nxt
                            j += 1
                        module_id = ((qno - 1) // 2) + 1
                        questions[f"Module {module_id}"]["Part A"].append(text.strip().rstrip("."))
                        i = j
                        continue

            if section == "B":
                m_b = re.match(r"^[\'\"._-]*\s*(1[1-9]|20)\s*(.*)$", line)
                if m_b:
                    qno = int(m_b.group(1))
                    text = m_b.group(2).strip()
                    j = i + 1
                    while j < len(lines):
                        nxt = clean(lines[j])
                        low_nxt = nxt.lower()
                        if not nxt:
                            j += 1
                            continue
                        if re.match(r"^(1[1-9]|20)\s+", nxt):
                            break
                        if re.search(r"module\s+[ivx]+", low_nxt):
                            break
                        if "page" in low_nxt and "of" in low_nxt:
                            break
                        text += " " + nxt
                        j += 1

                    if current_module is None:
                        current_module = ((qno - 11) // 2) + 1
                    questions[f"Module {current_module}"]["Part B"].append(text.strip().rstrip("."))
                    i = j
                    continue

            i += 1

    deduped = {f"Module {i}": {"Part A": [], "Part B": []} for i in range(1, 6)}
    for module, data in questions.items():
        for part in ("Part A", "Part B"):
            for q in data[part]:
                if not q:
                    continue
                if any(similar(q, existing) >= 0.88 for existing in deduped[module][part]):
                    continue
                deduped[module][part].append(q)

    out_path = Path("/Users/eric/Documents/StudyCollege/SC/build/sc_unique_pyq_2023_2024.json")
    out_path.write_text(json.dumps(deduped, indent=2), encoding="utf-8")

    print(str(out_path))
    for module in deduped:
        a_count = len(deduped[module]["Part A"])
        b_count = len(deduped[module]["Part B"])
        print(f"{module}: Part A={a_count}, Part B={b_count}")


if __name__ == "__main__":
    main()
