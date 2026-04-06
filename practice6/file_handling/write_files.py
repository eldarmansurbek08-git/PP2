from pathlib import Path

file_path = Path("sample.txt")

# Write (creates file or overwrites)
with open(file_path, "w") as f:
    f.write("Hello\n")
    f.write("This is Python practice\n")