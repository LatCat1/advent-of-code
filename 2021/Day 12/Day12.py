import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day12.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

m = {}
for l in lines:
    z = l.split('-')
    m[z[0]] = m.get(z[0], []) + [z[1]]
    m[z[1]] = m.get(z[1], []) + [z[0]]

def path(memory, loc, prev_small, require_minor=True):
    if loc in memory and loc == loc.lower():
        if prev_small == False:
            prev_small = True
        else:
            return 0
    if loc == 'start' and memory != []:
        return 0
    if loc == 'end':
        if require_minor:
            for step in memory:
                if step == step.lower():
                    return 1
        else:
            return 1
    return sum([path(memory + [loc], n, prev_small, require_minor)\
         for n in m[loc]])

#part 1
print(f"Part 1: {path([], 'start', True)}")

#part 2
print(f"Part 2: {path([], 'start', False, False)}")
