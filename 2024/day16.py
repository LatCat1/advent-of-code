from loader import load_data
from collections import defaultdict
import re
from functools import lru_cache, reduce
from datetime import datetime
import heapq as hq
from operator import or_

data = load_data(16, 2024, testing=True)
data = load_data(16, 2024, testing=False)

data = data.split('\n')

grid = {}
for i in range(len(data)):
    for j in range(len(data[i])):
        grid[(i,j)] = (data[i][j])


start = None
end = None
for g in grid:
    if grid[g] == 'S':
        start = g
    if grid[g] == 'E':
        end = g

dirs = [(1,0), (-1,0), (0,1), (0,-1)] # facing direction

q = []
# for (dx, dy) in dirs:
#     hq.heappush(q, (0, (start, (dx, dy))))
hq.heappush(q, (0, (start, (0, 1)), {start}))

def rotl(l):
    return (-l[1], l[0])

def rotr(l):
    return rotl(rotl(rotl(l)))

dists = {}
while q:
    cost, state, before = hq.heappop(q)
    # if we don't have a better cost and its a valid location
    if state in dists and dists[state][0] == cost:
        dists[state][1].update(before)

    if state not in dists and grid[state[0]] != '#' :
        loc, d = state
        inc = before | {loc}
        dists[state] = (cost, inc)
        # add in all the adjacent
        # step forward
        hq.heappush(q, (cost+1, ((loc[0]+d[0], loc[1]+d[1]), d), inc))
        # and potential turns
        hq.heappush(q, (cost+1000, (loc, rotl(d)), inc))
        hq.heappush(q, (cost+1000, (loc, rotr(d)), inc))


best = min(dists[(end, d)][0] for d in dirs if (end, d) in dists)
print(best)
print(
    len(reduce(or_, (dists[(end, d)][1] for d in dirs if (end, d) in dists and dists[(end, d)][0] == best)))
)