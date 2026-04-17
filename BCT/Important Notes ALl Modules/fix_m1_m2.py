import re
from pathlib import Path

DIR = Path("/Users/eric/Documents/StudyCollege/BCT/Important Notes ALl Modules")
m1_path = DIR / "Module1_Blockchain_Technologies_Notes.tex"
m2_path = DIR / "Module2_Blockchain_Architecture_Notes.tex"

for path in [m1_path, m2_path]:
    if not path.exists(): continue
    content = path.read_text()
    
    # Remove instructional texts
    content = re.sub(r'\\textbf\{Write these 6 bullet points:\}\n*', '', content)
    content = re.sub(r'\\textbf\{Write these 6 bullet points:\s*\}\n*', '', content)
    content = re.sub(r'\\textbf\{Write minimum 18 bullet points:\}\n*', '', content)
    content = re.sub(r'\\textbf\{Write minimum 18 bullet points.*\}\n*', '', content)
    content = re.sub(r'\\textbf\{Write minimum 18 bullet points.*\]\n*', '', content) # just in case
    
    path.write_text(content)
print("Removed instructional texts.")
