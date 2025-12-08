from loader import load_data
from collections import defaultdict
import re
from functools import lru_cache
from datetime import datetime
import heapq as hq

data = load_data(11, 2024, testing=True)
# data = load_data(11, 2024, testing=False)

data = data.split(' ')


stones = [int(n) for n in data]


def blink(stones):
    new = []
    for s in stones:
        if s == 0:
            new.append(1)
        elif len(g := str(s)) % 2 == 0:
            new.extend([int(g[:len(g)//2]), int(g[len(g)//2:])])
        else:
            new.append(s * 2024)
    return new


initials = set(stones)


def blink2(stone_counts):
    counts = defaultdict(int)
    for s in stone_counts:
        if s == 0:
            counts[1] += stone_counts[s]
        elif len(g := str(s)) % 2 == 0:
            counts[int(g[:len(g)//2])] += stone_counts[s]
            counts[int(g[len(g)//2:])] += stone_counts[s]
        else:
            counts[s*2024] += stone_counts[s]
    return counts

stones = defaultdict(int)
for i in initials:
    stones[i] += 1
asdf = []
for _ in range(600):
    stones = blink2(stones)
    asdf.append((_, len(stones)))

print(len(stones))
# print([i for i in range(3813) if i not in stones])

exit()

    # print(_, stones)
print(sum(stones[s] for s in stones))
print(max(s for s in stones))
print(len(stones))


def count(n):
    c = 0
    while len(str(n)) % 2 != 0:
        c += 1
        n *= 2024
    return c

twos = {}
for n in range(1, 10_000_000):
    c = count(n)
    if c >= 2:
        twos[n] = c
print(f"{len(twos):_}")