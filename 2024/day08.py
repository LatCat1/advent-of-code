from loader import load_data
from collections import defaultdict
import re
from functools import lru_cache
from datetime import datetime
import heapq as hq

data = load_data(8, 2024, testing=True)
data = load_data(8, 2024, testing=False)

data = data.split('\n')

nodes = defaultdict(set)

grid = {}
for i in range(len(data)):
    for j in range(len(data[i])):
        grid[i + j*1j] = data[i][j]

for g in grid:
    if grid[g] != '.':
        nodes[grid[g]].add(g)


antinodes = set()
for id in nodes:
    locs = list(nodes[id])
    for i in range(len(locs)):
        n1 = locs[i]
        for n2 in locs[i+1:]:
            # calculate the two spots
            if False:
                dx = n1[0]-n2[0]
                dy = n1[1]-n2[1]
                news = [
                    (n1[0]+dx, n1[1]+dy),
                    (n2[0]-dx, n2[1]-dy)
                ]
                for n in news:
                    if n in grid:
                        antinodes.add(n)
            if True:
                d = n1 - n2
                p = n1
                while p in grid:
                    antinodes.add(p)
                    p += d
                p = n2
                while p in grid:
                    antinodes.add(p)
                    p -= d
                
print(len(antinodes))
exit()
for i in range(len(data)):
    for j in range(len(data[i])):
        if data[i][j] != '.':
            print(data[i][j], end='')
        elif (i,j) in antinodes:
            print('#', end='')
        else:
            print('.', end='')
    print()
