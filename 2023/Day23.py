from loader import load_data
from functools import lru_cache, reduce
from math import lcm
from operator import mul
from bisect import bisect_left, bisect_right
import heapq as hq
from queue import Queue
from grid import FiniteGrid
import sys

sys.setrecursionlimit(100000)



data = load_data(day=23, year=2023, testing=False)
data = data.split('\n')

grid = FiniteGrid(data, default='#')

start = None
end = None
for i in range(len(data[0])):
    if data[0][i] == '.':
        start = (0, i)
    if data[-1][i] == '.':
        end = (len(data)-1, i)


dirs = {
    '>': (0, 1),
    '<': (0, -1),
    '^': (-1, 0),
    'v': (1, 0)
}


def adj(l, slopes=True):
    t = grid.get(l)
    if t == '#':
        return []
    if t in dirs and slopes:
        ops = [dirs[t]]
    else:
        ops = dirs.values()
    x, y = l
    for (dx, dy) in ops:
        nx, ny = x + dx, y + dy
        if grid.get((nx, ny)) != '#':
            yield (nx, ny)

junctions = [start, end]
for i in range(grid.height):
    for j in range(grid.width):
        if len(list(adj((i, j)))) > 2:
            junctions.append((i, j))

junc_to_id = {l: v for v, l in enumerate(junctions)}

def get_longest_dist(slopes):
    compressed = [[] for _ in enumerate(junctions)]
    for j in junctions:
        j_id = junc_to_id[j]
        for a in adj(j, slopes=slopes):
            prev = j
            d = 1
            while a not in junc_to_id:
                d += 1
                p = [a_ for a_ in adj(a,slopes=slopes) if a_ != prev] 
                if len(p) == 0:
                    break
                a, prev = p.pop(), a
            else:
                a_id = junc_to_id[a]
                compressed[j_id].append((d, a_id))

    start_id = junc_to_id[start]
    end_id   = junc_to_id[end]

    mem = {}
    def max_to_end(loc, visited):
        if loc == end_id:
            return 0
        if (loc, visited) in mem:
            return mem[(loc, visited)]
        i = loc
        if visited & (1 << i):
            return float('-inf')
        new_visited = visited | (1 << i)
        m = float('-inf')
        for (d, n) in compressed[loc]:
            m = max(m, max_to_end(n, new_visited) + d)
        mem[(loc, visited)] = m
        return m

    return max_to_end(start_id, 0)

# takes ~30s to run for me
print("Part 1:", get_longest_dist(True))
print("Part 2:", get_longest_dist(False))