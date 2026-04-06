import os

# Create directory
os.mkdir("test_dir")

# Create nested directories
os.makedirs("parent/child/grandchild", exist_ok=True)

# List files
print(os.listdir("."))

# Current directory
print(os.getcwd())