with open("sample.txt", "a") as f:
    f.write("New line added\n")

# verify
with open("sample.txt", "r") as f:
    print(f.read())