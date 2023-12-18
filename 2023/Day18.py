from loader import load_data
from functools import lru_cache, reduce
from math import lcm
from operator import mul
from bisect import bisect_left, bisect_right
import heapq as hq
from grid import FiniteGrid

data = load_data(day=18, year=2023, testing=False).split('\n')


x,y = [0,0], [0,0]
s = [0,0]
tot_dist = [0,0]
for r in data:
    dir, dist, info = r.split(' ')
    dist = int(dist)
    info = info[2:-1]
    for i in range(2):
        if i == 1:
            dist = int(info[:-1], base=16)
            dir= ['R', 'D', 'L', 'U'][int(info[-1])]
        dx, dy = [(1,0), (0,1), (-1,0), (0,-1)][
            {'R':0,'D':1,'L':2,'U':3}[dir] ]
        x[i] += + dx * dist
        y[i] += + dy * dist
        s[i] += x[i] * dy * dist
        tot_dist[i] += dist
for i in range(2):
    print(int(s[i] + tot_dist[i]/2 + 1))
