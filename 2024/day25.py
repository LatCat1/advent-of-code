from loader import load_data
from collections import defaultdict, Counter
import re
from functools import lru_cache, reduce, total_ordering
from datetime import datetime
import heapq as hq
from operator import and_, or_, xor

data = load_data(25, 2024, testing=True)
data = load_data(25, 2024, testing=False)


data = data.split('\n\n')


locks = []
keys = []

for item in data:
    heights = [-1] * 5
    rs = item.split('\n')
    if item[0] == '#':
        rs = rs[::-1]

    for i, r in enumerate(rs):
        for j in range(5):
            if r[j] == '#' and heights[j] == -1:
                heights[j] = 6-i 
                
    if item[0] == '#':
        locks.append(heights)
    else:
        keys.append(heights)


def opens(key, lock):
    # check if key opens lock
    return all(
        key[i] + lock[i] <= 5 for i in range(5)
    )
    

print(sum(opens(k, l) for k in keys for l in locks))