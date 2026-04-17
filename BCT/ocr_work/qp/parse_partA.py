import re
with open("CST428-QP_May_2024.txt", "r") as f:
    text = f.read()
    partA = text.split("PART")[1]
    print(partA)
