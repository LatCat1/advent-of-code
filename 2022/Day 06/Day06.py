import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    lines = f.read()

for j in [4, 14]:
    for i in range(j, len(lines)):
        if len(set(lines[i-j:i])) == j:
            print(i)
            break