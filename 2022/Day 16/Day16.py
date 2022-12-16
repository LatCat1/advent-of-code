import pathlib
from tqdm import tqdm

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    lines = f.read().split('\n')
grid = {}
rates = {}
for l in lines:
    q = l.split(' ')
    start = q[1]
    rate = int(q[4][5:-1])
    later = q[9:]
    for l in range(len(later)-1):
        later[l] = later[l][:-1]
    later = set(later)
    grid[start] = later
    rates[start] = rate

nonzero_flow = [g for g in rates if rates[g] != 0]
map_thingy = {}
for i in range(len(nonzero_flow)):
    map_thingy[nonzero_flow[i]] = i
map_thingy['AA'] = len(nonzero_flow) + 1

# ok we need to 'simplify' grid (maybe, this seems to make p1 slower actually). also, it doesn't help p2 
#   because things can be 'in progress' to a location. saving how far in that progress is slower
simplegrid = {}
for g in set(nonzero_flow) | {'AA'}: # starting
    # get the minimum distance from g to everything
    min_dists_from_g = {}
    to_check = {(0,g)}
    while len(to_check) != 0:
        cst, curr = min(to_check)
        to_check.remove((cst, curr))
        if curr not in min_dists_from_g:
            min_dists_from_g[curr] = cst
            for n in grid[curr]:
                to_check.add((cst+1, n))
    # got all min distances
    min_dists_from_g[g] = 1
    simplegrid[g] = set()
    for g2 in set(nonzero_flow):
        simplegrid[g].add((g2, min_dists_from_g[g2]))

all = [2**len(nonzero_flow)-1]
def solve(loc, time_remaining, visited, disallowed = 0, mem=None):
    if (visited + disallowed) == all[0] or time_remaining <= 0:
        return 0
    if (loc, time_remaining, visited) in mem:
        return mem[(loc, time_remaining, visited)]
    # this is failing because it can't go anywhere?
    val = max(p1(loc2[0], time_remaining-loc2[1], visited, disallowed, mem=mem) for loc2 in simplegrid[loc] 
        if (disallowed>>map_thingy[loc2[0]]) & 1 == 0)
    if not(rates[loc] == 0 or (visited >> map_thingy[loc]) & 1 == 1):
        new_visited = visited | (1 << map_thingy[loc])
        val = max(val, rates[loc]*(time_remaining-1) + p1(loc, time_remaining-1, new_visited, disallowed, mem=mem))
    mem[(loc, time_remaining, visited)] = val
    return val

# print('P1:', p1('AA', 30, 0, 0, mem={}))

# part 2 yay
# exit()
best = 0

for d in tqdm(range(2**(len(nonzero_flow)-1))):
    best = max(best, p1('AA', 26, 0, d, {}) + p1('AA', 26, 0, all[0]-d, {}))
print(best)
# i hope that gives it

# all_open_val = sum(rates[g] for g in rates)
# mem2 = {}

# def p2(mloc, eloc, time_remaining, visited):
#     if visited == 2**len(nonzero_flow)-1:
#         return 0
#     mloc, eloc = min(mloc, eloc), max(mloc, eloc)  # locations are interchangable. should lower memory burden
#     if (mloc, eloc, time_remaining, visited) in mem2:
#         return mem2[(mloc, eloc, time_remaining, visited)]
#     if time_remaining <= 0:
#         return 0

#     val = max(p2(mloc2, eloc2, time_remaining-1, visited) for mloc2 in grid[mloc] for eloc2 in grid[eloc])
#     if not (rates[mloc] == 0 or (visited >> map_thingy[mloc]) & 1 == 1) and \
#         ((rates[eloc] == 0 or (visited >> map_thingy[eloc]) & 1 == 1) or mloc == eloc):
#         new_visited = visited | (1<<map_thingy[mloc])
#         val = max(val, rates[mloc]*(time_remaining-1)+max(p2(mloc, eloc2, time_remaining-1, new_visited) for eloc2 in grid[eloc]))
#     elif (rates[mloc] == 0 or (visited >> map_thingy[mloc]) & 1 == 1) and \
#         not (rates[eloc] == 0 or (visited >> map_thingy[eloc]) & 1 == 1):
#         new_visited = visited | (1<<map_thingy[eloc])
#         val = max(val, rates[eloc]*(time_remaining-1)+max(p2(mloc2, eloc, time_remaining-1, new_visited) for mloc2 in grid[mloc]))
#     elif not (rates[mloc] == 0 or (visited >> map_thingy[mloc]) & 1 == 1) and \
#         not (rates[eloc] == 0 or (visited >> map_thingy[eloc]) & 1 == 1):
#         # they both can open, different ones
#         new_visited = visited | (1<<map_thingy[eloc]) | (1<<map_thingy[mloc])
#         val = max(val, (rates[eloc]+rates[mloc])*(time_remaining-1)+p2(mloc, eloc, time_remaining-1, new_visited))
#     mem2[(mloc, eloc, time_remaining, visited)] = val
#     if len(mem2) % 1000000 == 0:
#         print(len(mem2))
#     return val

# print(p2('AA', 'AA', 26, 0))
# print(len(mem2))