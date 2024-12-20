from loader import load_data
from collections import defaultdict
import re
from functools import lru_cache, reduce, total_ordering
from datetime import datetime
import heapq as hq
from operator import or_

data = load_data(19, 2024, testing=True)
data = load_data(19, 2024, testing=False)

poss, cases = data.split('\n\n')
towels = poss.split(', ')
patterns = cases.split('\n')

@lru_cache
def possible_ways(pattern):
    if not pattern:
        return 1

    return sum(
        possible_ways(pattern[len(t):]) for t in towels if pattern[:len(t)] == t
    )

print('P1:', sum(possible_ways(p) > 0  for p in patterns))
print('P2:', sum(possible_ways(p)  for p in patterns))