from pathlib import Path

file_path = Path("sample.txt")

with open(file_path, "r") as f:
    print("Full content:")
    print(f.read())

with open(file_path, "r") as f:
    print("Line by line:")
    print(f.readline())

with open(file_path, "r") as f:
    print(f.readlines())