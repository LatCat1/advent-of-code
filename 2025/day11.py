from loader import load_data
from functools import lru_cache
from datetime import datetime, timedelta
from collections import defaultdict
from itertools import combinations, product
from dataclasses import dataclass
from math import inf
from tqdm import tqdm
from scipy.optimize import milp, LinearConstraint
import numpy as np

data = load_data(11, 2025, testing=False).split('\n')

t = datetime.now()

devices = defaultdict(set)

for d in data:
    ps = d.split(' ')
    s = ps[0][:-1]
    for q in ps[1:]:
        devices[s].add(q)


@lru_cache(len(devices))
def paths_to_out(l):
    if l == 'out':
        return 1
    return sum(
        paths_to_out(n) for n in devices[l]
    )

print(paths_to_out('you'))

@lru_cache(len(devices)*4)
def paths_to_out_2(l, reached_dac=False, reached_fft=False):
    if l == 'out':
        return 1 if reached_dac and reached_fft else 0
    return sum(
        paths_to_out_2(n, reached_dac or l == 'dac', reached_fft or l == 'fft') for n in devices[l]
    )

print(paths_to_out_2('svr'))
print(datetime.now() - t)

# this is made significantly easier by that fact that we are given a directed graph
# Let d = len(devices)
# p1 is O(d^2); it's linear in the number of connections which has this trivial upper bound
# p2 is _also_ O(d^2); it just hides a slightly larger constant of 4 times the previous
#                      part, where the 4 comes from which of dac and fft it has/has not reached
# actually, some quick checks of cache hit rate shows that p1 cache only has 70 items, so p1 is 
# a tiny portion of the overall space. p2 has 1262 items, and 2348 are allocated, for a better
# 50% usage and no overflow. in fact using the lru_cache with hashing overhead, etc is overkill
# and having an array with index offsets etc would be significantly faster, but this runs in 
# 1ms so why bother