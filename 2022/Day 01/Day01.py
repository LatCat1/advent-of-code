import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day01.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

elves = [0]

for l in lines:
    if l == "":
        elves.append(0)
    else:
        elves[-1] += int(l)
elves = sorted(elves)[::-1]
print(elves[0] + elves[1] + elves[2])
print(max(elves))