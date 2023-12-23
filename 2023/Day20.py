from loader import load_data
from functools import lru_cache, reduce
from math import lcm
from operator import mul
from bisect import bisect_left, bisect_right
import heapq as hq
import queue
from grid import FiniteGrid

data = load_data(day=20, year=2023, testing=False)


# maps a module to a pair (type, downstrem)
modules = {}
# sends something to a state.
states = {}

rx_feeder = None
for d in data.split('\n'):
    to = d.split('>')[1].strip().split(', ')
    if d[0] in '&%':
        t = d[0]
        name = d.split(' ')[0][1:]
        modules[name] = (d[0], to)
        if d[0] == '&':
            states[name] = {}
        else:
            states[name] = False
        if 'rx' in to:
            rx_feeder = name
    else:
        name = d.split(' ')[0]
        modules[name] = (None, to)
# initialize all to LOW
for m in modules:
    for t in modules[m][1]:
        if t in modules and modules[t][0] == '&':
            states[t][m] = False

def push_broadcast():
    q = queue.Queue()
    low_count = 1 # button to broadcaster
    high_count = 0
    low_to = {}
    for ds in modules['broadcaster'][1]:
        q.put(('broadcaster', ds, False))
    while not q.empty():
        todo = q.get()
        from_, to, sig = todo
        if sig == False:
            low_to[to] = low_to.get(to, 0) + 1
        # print(from_, 'High' if sig else 'Low','->', to)
        if todo[2]:
            high_count += 1
        else:
            low_count += 1
        if to not in modules:
            continue
        if modules[to][0] == '&':
            states[to][from_] = sig
            if all(states[to][f] for f in states[to]):
                for dw in modules[to][1]:
                    q.put((to, dw, False))
            else:
                for dw in modules[to][1]:
                    q.put((to, dw, True))
        elif modules[to][0] == '%':
            if sig == False:
                states[to] = not states[to]
                for dw in modules[to][1]:
                    q.put((to, dw, states[to]))
    return low_count, high_count, low_to


# find everything rx cares about
cares = list(states[rx_feeder].keys())
bests = {}
t = 0
lows = 0
highs = 0
while len(bests) != len(cares) or t < 1000:
    t += 1
    a, b, c = push_broadcast()
    lows += a
    highs += b
    for c_ in cares:
        if c_ in c and c_ not in bests:
            bests[c_] = t
    if t == 1000:
        print('Part 1:', lows*highs)

print('Part 2:', lcm(*bests.values())) 