import shutil
import os

# Copy file
shutil.copy("sample.txt", "backup.txt")

# Delete file safely
if os.path.exists("backup.txt"):
    os.remove("backup.txt")
    print("Deleted backup.txt")
else:
    print("File not found")