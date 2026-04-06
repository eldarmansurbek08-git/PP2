import shutil

# Move file
shutil.move("sample.txt", "test_dir/sample.txt")

# Copy back
shutil.copy("test_dir/sample.txt", "sample_copy.txt")