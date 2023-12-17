from loader import load_data
from functools import lru_cache, reduce
from math import lcm
from operator import mul
from bisect import bisect_left, bisect_right
import heapq as hq
from grid import FiniteGrid

data = load_data(day=17, year=2023, testing=False)
data = data.split('\n')
grid = FiniteGrid(data)



def adj(l, dir, dist, min_dist=4, max_dist=10):
    # if moved less than 4, go forward again
    if 0 < dist < min_dist:
        x, y = l
        dx, dy = dir
        return [((x+dx,y+dy), dir, dist+1)]
    x, y = l
    dirs = [(0,1), (0,-1), (1,0), (-1,0)]
    # can't turn around
    dx, dy = dir
    illegal_dir = (-dx, -dy)
    dirs = [d for d in dirs if d != illegal_dir]
    if dist == max_dist:
        dirs = [d for d in dirs if d != dir]
    ns = []
    for d in dirs:
        dx, dy = d
        nl = (x+dx, y+dy)
        if d == dir:
            ns.append((nl, d, dist+1))
        else:
            ns.append((nl, d, 1))
    return ns

# actually, imagine this as a higher-dimensional thing
# there are a few layers: location * direction * dist
# dist can be in [0,1,2,3]

def run(min_dist, max_dist):
    queue = [(0, ((0,0), (2,2), 0))]
    costs = {}
    checked_already = set()
    while queue != []:
        cost, loc_data = hq.heappop(queue)
        if grid.in_bounds(loc_data[0]) and loc_data not in checked_already:
            checked_already.add(loc_data)
            loc, dir, dist = loc_data
            if dist >= min_dist:
                if loc in costs:
                    costs[loc] = min(cost, costs[loc])
                else:
                    costs[loc] = cost
            for nextL in adj(loc, dir, dist, min_dist, max_dist):
                hq.heappush(queue, (cost+int(grid.get(loc)), nextL))

    goal = (len(data)-1, len(data[0])-1) 
    return costs[goal] + int(grid[goal]) - int(grid[(0,0)])

print("Part 1:", run(0, 3))
print("Part 2:", run(4, 10))