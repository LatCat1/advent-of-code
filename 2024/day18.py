from loader import load_data
from collections import defaultdict
import re
from functools import lru_cache, reduce, total_ordering
from datetime import datetime
import heapq as hq
from operator import or_

size = 70
steps = 1024
data = load_data(18, 2024, testing=False)
# size = 6
# steps = 12
# data = load_data(18, 2024, testing=True)


corrupted = set()

bytes = [
    int(b[0]) + 1j*int(b[1]) for b in (x.split(',') for x in data.split('\n'))
]


def show():
    for i in range(size+1):
        for j in range(size+1):
            print('#' if i*1j+j in corrupted else '.', end='')
        print()



class HeapObj:
    def __init__(self, weight, val):
        self.weight = weight
        self.val = val

    @total_ordering
    def __lt__(self, other):
        return self.weight < other.weight

    def __iter__(self):
        return iter((self.weight, self.val))


def check_steps(step):
    corrupted = set(bytes[:step])

    def adj(l):
        return [l+d for d in (1, -1, 1j, -1j) if l+d not in corrupted and 0 <= (l+d).real <= size and 0 <= (l+d).imag <= size]

    q = [HeapObj(0, 0+0j)]
    dists = {}
    while (size+1j*size) not in dists and q:
        # pop the first object
        d, v = hq.heappop(q)
        if v in dists:
            continue
        dists[v] = d
        for a in adj(v):
            hq.heappush(q, HeapObj(d+1, a))

    return dists.get((size+size*1j), -1)

# i can binary search
# but I can also brute foce which is easier
print('P1:', check_steps(steps))


low = 0
high = len(bytes)-1

while high - low > 1:
    t = (high + low) // 2
    if check_steps(t) == -1:
        high = t
    else:
        low = t

print(f"{int(bytes[t].real)},{int(bytes[t].imag)}")