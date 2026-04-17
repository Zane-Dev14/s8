import re
with open("October_2023_Supplementary.txt", "r") as f:
    text = f.read()
    partA = text.split("PART")[1]
    print(partA)
