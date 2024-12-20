from loader import load_data
from collections import defaultdict
import re
from functools import lru_cache
from datetime import datetime
import heapq as hq

# data = load_data(13, 2024, testing=True)
data = load_data(13, 2024, testing=False)

data = data.split('\n\n')

# a 3-list of compex nums
# button A, button B, and prize
machines = []
for d in data:
    h = d.split('\n')
    reg = r' X(\+|=)([0-9]+), Y(\+|=)([0-9]+)'
    l= []
    for hh in h:
        m = re.match(reg, hh.split(':')[1])
        l.append((int(m.group(2)), int(m.group(4))))
    machines.append(l)

OFFSET = 10000000000000 
def min_cost_for_prize(mach, p1=True):
    # we try to solve mach[0]*a + mach[1]*b = mach[2]
    # this gives two unknows and 2 coordinates so its solvable
    q, w, e, = mach
    a, c = q
    b, d = w
    e, f = e

    if not p1:
        e += OFFSET
        f += OFFSET

    det = a*d - b * c
    if det == 0:
        return 9

    # otherwise invert it?
    apress = (e * d - b * f) / det
    if apress != int(apress):
        return 0
    apress = int(apress)

    bpress = e-q[0]*apress
    if bpress % b != 0:
        return 0
    bpress = bpress // b

    if (apress > 100 or bpress > 100) and p1:
        return 0

    return apress*3 + bpress
     

for p in [1,2]:
    print(f'P{p}: { sum(min_cost_for_prize(m, p == 1) for m in machines) }')