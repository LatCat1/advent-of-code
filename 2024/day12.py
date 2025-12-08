from loader import load_data
from collections import defaultdict
import re
from functools import lru_cache
from datetime import datetime
import heapq as hq

data = load_data(12, 2024, testing=True)
data = load_data(12, 2024, testing=False)

data = data.split('\n')

grid = {}
for i in range(len(data)):
    for j in range(len(data[i])):
        grid[i+j*1j] = (data[i][j])

g2 = grid.copy()


regions = []

def adj(l):
    return [l+1,l-1,l+1j,l-1j]

def collect(loc, type):
    if loc not in grid or grid[loc] != type:
        return {}
    g = [loc]
    grid.pop(loc)
    for a in adj(loc):
        g.extend(collect(a, type))
    return g

while grid:
    l = None
    for g in grid :
        l = g
        break
    regions.append((grid[l], collect(l, grid[l])))

def area(region):
    return len(region[1])

def perim(region):
    return sum(
        1 if a not in g2 or g2[a] != region[0] else 0 for l in region[1] for a in adj(l)
    )

def sides(region):
    # maps from a point to a side object
    sides = []
    inside = set(region[1])
    # a set of points _and_ directions
    checked = set()

    for i in inside:
        for d in [1,-1,1j,-1j]:
            if i+d not in inside and (i, d) not in checked:
                checked.add((i, d))
                side = {i+d}
                # we've found something outside
                r = d * 1j # rotate it
                # move it up
                l = i
                # input()
                while l+d+r not in inside and l+r in inside:
                    checked.add((l, d))
                    side.add(l+d+r)
                    l += r
                # input()
                l = i
                while l+d-r not in inside and l-r in inside:
                    checked.add((l, d))
                    side.add(l+d-r)
                    l -= r
                sides.append((d, side))
                # input()

    clean_sides = []
    while sides:
        s = sides.pop()
        if len(s) == 1:
            clean_sides.append(s)
        # ohterwise is repeat
        if s not in sides:
            clean_sides.append(s)

    return len(clean_sides)



# print(sum(area(r)*perim(r) for r in regions))
print(sum(sides(r)*area(r) for r in regions))
# for r in regions:
    # print(r[0], sides(r))
    # print(len(sides(r)))
    # exit()