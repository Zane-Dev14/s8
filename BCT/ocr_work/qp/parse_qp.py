import os, glob

def parse_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    # Very basic print for now
    print(f"=== {filename} ===")
    
    parts = content.split("PART")
    
    for i, p in enumerate(parts):
        print(f"--- Part index {i} ---")
        lines = p.split('\n')
        # print first few lines of each part
        print('\n'.join(lines[:10]))
        print("...")

for file in ["CST428-QP_May_2024.txt", "June_2023_Regular.txt", "October_2023_Supplementary.txt", "IMG-20250403-WA0007.txt", "CST428-SCHEME_May_2024.txt"]:
    if os.path.exists(file):
        parse_file(file)

