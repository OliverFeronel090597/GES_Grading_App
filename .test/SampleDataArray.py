data = [
    [ "Math", "Mr. Cruz"],
    [ "English", "Ms. Santos"],
    [ "Science", "Mr. Lim"],
]
print(list(enumerate(data)))


for i, row in enumerate(data):
    print(f"Row {i}: {row}")