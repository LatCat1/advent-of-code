from loader import load_data
from collections import defaultdict, Counter
import re
from functools import lru_cache, reduce, total_ordering
from datetime import datetime
import heapq as hq
from operator import or_

data = load_data(23, 2024, testing=True)
data = load_data(23, 2024, testing=False)

edges: list[tuple[str, str]] = [list(d.split('-')) for d in data.split('\n')]

computers = defaultdict(set)
for a, b in edges:
    computers[a].add(b)
    computers[b].add(a)

triangles: set[tuple] = set()
for c1, c2 in edges:
    for mutual in computers[c1] & computers[c2]:
        triangles.add(tuple(sorted((c1, c2, mutual))))

# filter to only with t in one of them
historian_computers = list(filter(lambda t: any(c[0] == 't' for c in t), triangles))
print('P1:', len(historian_computers)) 


def bron_kerbosch(p: set, r: set = set(), x: set = set(), rets: list[set] = []):
    if len(x) == 0 and len(p) == 0:
        rets.append(r.copy())
    for v in list(p):
        bron_kerbosch(p & computers[v], r | {v}, x & computers[v])
        p.remove(v)
        x.add(v)
    return rets
        
print('P2:', ','.join( sorted( max( bron_kerbosch({c for c in computers}), key=len))))