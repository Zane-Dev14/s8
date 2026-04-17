import re
with open("October_2023_Supplementary.txt", "r") as f:
    text = f.read()
    print(" ".join(text.split("Module III")[1].split("Module IV")[0].split()))
