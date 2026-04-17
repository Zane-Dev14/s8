import os, json

def clean_text(lines):
    res = []
    for l in lines:
        l = l.strip()
        if not l: continue
        if "Page " in l or l.isdigit() or l.startswith("A ") or l.startswith("B "): continue
        if "Answer all questions" in l or "Answer any one full question" in l: continue
        if l == "OR" or l.startswith("Module"): continue
        res.append(l)
    return " ".join(res).strip()

out_data = {}

def process_file(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        content = f.read()
    
    parts = content.split("PART")
    if len(parts) < 3: return
    
    basename = os.path.basename(filepath)
    out_data[basename] = {"A": [], "B": {}}

    partA_lines = parts[1].split('\n')
    partA_text = "\n".join(partA_lines).replace("A\nAnswer all questions, each carries 3 marks.", "").strip()
    
    pa_filtered = []
    for line in partA_text.split('\n'):
        if line.strip() and not ("Answer all" in line):
            pa_filtered.append(line.strip())
            
    combined = []
    curr = ""
    for l in pa_filtered:
        if curr: curr += " " + l
        else: curr = l
        if l.endswith('?') or l.endswith('.') or "types of blockchain." in l:
            combined.append(curr)
            curr = ""
    if curr: combined.append(curr)

    out_data[basename]["A"] = combined
    
    partB_text = parts[2]
    for mod in ["Module III", "Module IV", "Module V"]:
        if mod in partB_text:
            mod_part = partB_text.split(mod)[1]
            for nxt in ["Module IV", "Module V", "Module VI", "===== PAGE"]:
                if nxt in mod_part:
                    mod_part = mod_part.split(nxt)[0]
            out_data[basename]["B"][mod] = clean_text(mod_part.split(chr(10)))

for file in ["/Users/eric/Documents/StudyCollege/BCT/ocr_work/qp/CST428-QP_May_2024.txt", 
             "/Users/eric/Documents/StudyCollege/BCT/ocr_work/qp/June_2023_Regular.txt", 
             "/Users/eric/Documents/StudyCollege/BCT/ocr_work/qp/October_2023_Supplementary.txt", 
             "/Users/eric/Documents/StudyCollege/BCT/ocr_work/qp/IMG-20250403-WA0007.txt"]:
    process_file(file)

with open("/Users/eric/Documents/StudyCollege/BCT/ocr_work/qp/questions_extracted.json", "w") as f:
    json.dump(out_data, f, indent=2)
