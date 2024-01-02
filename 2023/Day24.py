from loader import load_data
from functools import lru_cache, reduce
from math import lcm
from operator import mul
from bisect import bisect_left, bisect_right
import heapq as hq
from queue import Queue
from grid import FiniteGrid
import sys
from z3 import *

sys.setrecursionlimit(100000)

data = load_data(day=24, year=2023, testing=False)
data = data.split('\n')


hailstones = []
for d in data:
    xs = d.split('@')
    q = []
    for x in xs:
        x = x.strip()
        zs = x.split(',')
        n = []
        for z in zs:
            n.append(int(z))
        n = tuple(n)
        q.append(n)
    q = tuple(q)
    hailstones.append(q)


min_r = 200000000000000
max_r = 400000000000000 + 1
def intersect_xy(hs1, hs2):
    p1, v1 = hs1
    p2, v2 = hs2
    x1, y1, _ = p1
    x2, y2, _ = p2
    dx1, dy1, _ = v1
    dx2, dy2, _ = v2
    m1 = dy1/dx1
    m2 = dy2/dx2
    if m1 != m2:
        b1 = y1 - x1 * m1 
        b2 = y2 - x2 * m2
        int_x = (b2-b1)/(m1-m2)
        int_y1 = m1 * int_x + b1
        int_y = int_y1
        x_t1 = (int_x - x1) / dx1
        if x_t1 < 0:
            return False
        x_t2 = (int_x - x2) / dx2
        if x_t2 < 0:
            return False 
        if min_r <= int_x < max_r and min_r <= int_y < max_r:
            return True
    return False

print('Part 1:',
    sum(
        intersect_xy(h1, h2) for i, h1 in enumerate(hailstones) for h2 in hailstones[i+1:]
    )      
)

# unknown 3-vector for position
x = Real('x')
y = Real('y')
z = Real('z')
p = [x, y, z]

dx = Real('dx')
dy = Real('dy')
dz = Real('dz')
v = [dx, dy, dz]

eqns = [] # [ts[i] >= 0 for i in range(num_check)]
for i, h in enumerate(hailstones[:3]):
    hp, hd = h
    t = Real(f't{i}')
    eqns.append(t > 0)
    eqns.extend(
        hp[i]+hd[i]*t == p[i]+v[i]*t for i in range(3)
    )
s = Solver()
s.add(*eqns)
s.check()
m = s.model()
print("Part 2:", sum([
    m[p[i]].as_long() for i in range(3)
]))
