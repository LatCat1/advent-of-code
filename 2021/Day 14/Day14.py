import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day14.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

p = lines[0]
pairs = {}
for l in lines[2:]:
    q = l.split(' -> ')
    pairs[q[0]] = [q[0][0]+q[1], q[1]+q[0][1]]

start_pair_count = {}
for i in range(len(p)-1):
    start_pair_count[p[i:i+2]] = start_pair_count.get(p[i:i+2], 0) + 1

def step(polymer):
    new_polymer = {}
    for pair in polymer:
        for new_pair in pairs[pair]:
            new_polymer[new_pair] = new_polymer.get(new_pair,0) + polymer[pair]
    return new_polymer

def get_diff(polymer):
    letters_count = {}
    for k in start_pair_count:
        for i in k:
            letters_count[i] = letters_count.get(i, 0) + start_pair_count[k]
    z = [letters_count[k] for k in letters_count]
    return((max(z)-min(z))//2)

# part 1
for i in range(10): start_pair_count = step(start_pair_count)
print(f"Part 1: {get_diff(start_pair_count)}")

# part 2
for i in range(30): start_pair_count = step(start_pair_count)
print(f"Part 2: {get_diff(start_pair_count)}")
