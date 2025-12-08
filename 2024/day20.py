from loader import load_data
from collections import defaultdict
import re
from functools import lru_cache, reduce, total_ordering
from datetime import datetime
import heapq as hq
from operator import or_

# data = load_data(20, 2024, testing=True)
data = load_data(20, 2024, testing=False)

locs = set()

start = None
end = None
for i, r in enumerate(data.split('\n')):
    for j, l in enumerate(r):
        if l != '#':
            locs.add(i+j*1j)
        if l == 'S':
            start = i+j*1j
        if l == 'E':
            end = i+j*1j

def adj(l):
    return [l+d for d in (1, -1, 1j, -1j)]

dist = {}
q = end
d = 0
while q != start:
    dist[q] = d
    d += 1
    for l in adj(q):
        if l in locs and l not in dist:
            q = l
            break
dist[start] = d

cheats = defaultdict(set)
for l in locs:
    # double adjacent
    cheatstops = [h for k in adj(l) for h in adj(k)]
    for c in cheatstops: 
        if c in locs and (save := dist[c] - dist[l] - 2) > 0:
            cheats[save].add((l, c))

print('P1:', sum(
    len(cheats[s]) for s in cheats if s >= 100
))


def di(a, b):
    return abs(a.real-b.real) + abs(a.imag - b.imag)

cheats = defaultdict(int)
path = sorted(locs, key=lambda l:dist[l], reverse=True)

for i, l in enumerate(path):
    for l_ in path[i+1:]:
        if (d := di(l, l_)) <= 20 and (save := dist[l] - dist[l_] - d) > 0:
            cheats[(l, l_)] = max(cheats[(l, l_)], save)

print('P2:', 
    sum(cheats[c] >= 100 for c in cheats)
)
    