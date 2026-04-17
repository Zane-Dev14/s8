import os, json

def clean_text(lines):
    res = []
    for l in lines:
        l = l.strip()
        if not l: continue
        res.append(l)
    return "\n".join(res).strip()

out_data = {}

filepath = "/Users/eric/Documents/StudyCollege/BCT/ocr_work/qp/CST428-SCHEME_May_2024.txt"
if os.path.exists(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    parts = content.split("PART")
    if len(parts) >= 3:
        partB_text = parts[2]
        mods = {}
        for mod in ["Module III", "Module IV", "Module V"]:
            if mod in partB_text:
                mod_part = partB_text.split(mod)[1]
                for nxt in ["Module IV", "Module V", "Module VI", "===== PAGE 5"]:
                    if nxt in mod_part:
                        mod_part = mod_part.split(nxt)[0]
                mods[mod] = clean_text(mod_part.split(chr(10)))
        out_data["Scheme_B"] = mods

    if len(parts) >= 2:
        partA_text = parts[1]
        out_data["Scheme_A"] = partA_text

with open("/Users/eric/Documents/StudyCollege/BCT/ocr_work/qp/scheme_extracted.json", "w") as f:
    json.dump(out_data, f, indent=2)
