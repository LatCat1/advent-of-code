from loader import load_data
from collections import defaultdict
import re
from functools import lru_cache
from datetime import datetime
import heapq as hq

# w = 11
# h = 7
# data = load_data(14, 2024, testing=True)
w = 101
h = 103
data = load_data(14, 2024, testing=False)

data = data.split('\n')



s = 100

robots = []
for ha in data:
    r = r'p=([0-9]+),([0-9]+) v=(-?[0-9]+),(-?[0-9]+)'
    m = re.match(r, ha)
    a = []
    for _ in range(1, 5):
        a.append(int(m.group(_)))
    robots.append(a)

def jump(s):
    af100locs = defaultdict(int)
    for r in robots:
        x, y, dx, dy = r
        x = (int(x) + dx*s) % w
        y = (int(y) + dy*s) % h
        af100locs[(x, y)] += 1
    return af100locs


midx = (w - 1) / 2
midy = (h - 1) / 2


def visualize(step):
    af100locs = jump(step)
    o = []
    for i in range(h):
        for j in range(w):
            o.append(('#' if (j,i) in af100locs else ' '))
    pretty_print(''.join(str(c) for c in o))

def pretty_print(asdf):
    # spliti n to chunchs of width w
    for _ in range(h):
        print(asdf[_*w:(_+1)*w])

def danger(step):
    af100locs = jump(step)
    q1, q2, q3, q4 = 0, 0, 0, 0
    for l in af100locs:
        x, y = l
        if x < midx:
            if y < midy:
                q1 += af100locs[l]
            if y > midy:
                q4 += af100locs[l]
        if x > midx:
            if y < midy:
                q2 += af100locs[l]
            if y > midy:
                q3 += af100locs[l]
    return q1*q2*q3*q4
            

print(danger(100))

min_danger = min(range(10_000), key=danger)
print(min_danger)
