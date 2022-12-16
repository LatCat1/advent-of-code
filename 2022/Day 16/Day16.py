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
mem = {}
def solve(loc, time_remaining, visited):
    if visited == all[0] or time_remaining <= 0:
        return 0
    if (loc, time_remaining, visited) in mem:
        return mem[(loc, time_remaining, visited)]
    val = max(solve(loc2[0], time_remaining-loc2[1], visited) for loc2 in simplegrid[loc])
    if not(rates[loc] == 0 or (visited >> map_thingy[loc]) & 1 == 1):
        new_visited = visited | (1 << map_thingy[loc])
        val = max(val, rates[loc]*(time_remaining-1) + solve(loc, time_remaining-1, new_visited))
    mem[(loc, time_remaining, visited)] = val
    return val

print('P1:', solve('AA', 30, 0))

# part 2 yay. can take ~3 min to run on actual inputs
print('P2:', max(solve('AA', 26, d) + solve('AA', 26, all[0]-d) 
            for d in range(2**(len(nonzero_flow)-1))))