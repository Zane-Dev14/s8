import re
with open("June_2023_Regular.txt", "r") as f:
    text = f.read()
    partA = text.split("PART")[1]
    print(partA)
