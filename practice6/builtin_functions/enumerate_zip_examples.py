names = ["Ali", "Aruzhan", "Dias"]
scores = [90, 85, 88]

# enumerate
for i, name in enumerate(names):
    print(i, name)

# zip
for name, score in zip(names, scores):
    print(name, score)