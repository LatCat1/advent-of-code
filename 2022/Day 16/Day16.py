import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    lines = f.read().split('\n')
grid = {}
rates = {}
for l in lines:
    q = l.split(' ')
    start, rate, later = q[1], int(q[4][5:-1]), q[9:]
    for l in range(len(later)-1):
        later[l] = later[l][:-1]
    later = set(later)
    grid[start] = later
    rates[start] = rate

nonzero_flow = {g for g in rates if rates[g] != 0}
bitmap_guide = {g: i for (i,g) in enumerate(nonzero_flow)}
bitmap_guide['AA'] = len(nonzero_flow) + 1

# ok we need to 'simplify' grid (maybe, this seems to make p1 slower actually). also, it doesn't help p2 
#   because things can be 'in progress' to a location. saving how far in that progress is slower
shortest = {n:{n:0} for n in grid}
for n in grid:
    for n2 in grid[n]:
        shortest[n][n2] = 1
ordered_nodes = list(rates.keys())
for i, pivot in enumerate(ordered_nodes):
    for a in ordered_nodes:
        for b in ordered_nodes:
            if pivot in shortest[a] and b in shortest[pivot]:
                detour = shortest[a][pivot] + shortest[pivot][b]
                if b not in shortest[a] or shortest[a][b] > detour:
                    shortest[a][b] = detour
simplegrid = {g:{d:shortest[g][d] for d in nonzero_flow-{g}} for g in nonzero_flow | {'AA'}}

all = [2**len(nonzero_flow)-1]
mem = {k:[[None]*(2**len(nonzero_flow)) for _ in range(31)] for k in nonzero_flow | {'AA'}}
def solve(loc, time_remaining, visited):
    if visited == all[0] or time_remaining <= 0:
        return 0
    if mem[loc][time_remaining][visited] is not None:
        return mem[loc][time_remaining][visited]
    val = max((solve(loc2, time_remaining-simplegrid[loc][loc2]-1, visited | (1<<bitmap_guide[loc2]))+
            (time_remaining-simplegrid[loc][loc2]-1)*rates[loc2] for loc2 in simplegrid[loc] 
            if (visited >> bitmap_guide[loc2]) & 1 == 0), default=0)
    mem[loc][time_remaining][visited] = val
    return val

print('P1:', solve('AA', 30, 0))

# part 2 yay. usually < min on my laptop, should be much faster elsewhere
print('P2:', max(solve('AA', 26, d) + solve('AA', 26, all[0]-d) 
            for d in range(2**(len(nonzero_flow)-1))))