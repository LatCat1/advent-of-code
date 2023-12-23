from loader import load_data
from functools import lru_cache, reduce
from math import lcm, ceil
from operator import mul
from bisect import bisect_left, bisect_right
import heapq as hq
import queue
from grid import FiniteGrid

data = load_data(day=22, year=2023, testing=False)

data = data.split('\n')


bricks = []
for d in data:
    start, end = d.split('~')
    sx, sy, sz = [int(v) for v in start.split(',')]
    ex, ey, ez = [int(v) for v in end.split(',')]
    sx, ex = min(sx, ex), max(sx, ex)
    sy, ey = min(sy, ey), max(sy, ey)
    sz, ez = min(sz, ez), max(sz, ez)
    bricks.append(
        ((sz, sx, sy), (ez, ex, ey))
    )

def settle(bricks, limit_falls=False):
    # repeatedly settle them, in order.
    taken_by = {} # maps a location to the _index_ of the brick its in
    dissolvable = set() # tracks if a brick is dissolvable
    new_bricks = []
    num_fall = 0
    for i, b in enumerate(bricks):
        dissolvable.add(i)
        start, end = b
        sz, sx, sy = start
        ez, ex, ey = end
        fell = False
        while sz > 0 and \
            all((sz-1, x, y) not in taken_by for x in range(sx, ex+1) for y in range(sy, ey+1)):
            sz -= 1
            ez -= 1
            fell = True
            if limit_falls:
                break
        num_fall += fell
        for x in range(sx, ex+1):
            for y in range(sy, ey+1):
                taken_by[(ez, x, y)] = i
        # see if its lying on exactly 1
        on_top = {taken_by.get((sz-1, x, y), -1) for x in range(sx, ex+1) for y in range(sy, ey+1)} - {-1}
        if len(on_top) == 1:
            dissolvable -= on_top
        new_bricks.append(((sz, sx, sy), (ez, ex, ey)))
    return len(dissolvable), new_bricks, num_fall

# get 'lowest' bricks first 
bricks = sorted(bricks)
cnt1, settled, _ = settle(bricks)
print("Part 1:", cnt1)

settled = sorted(settled)
cnt2 = sum(
    settle(settled[:i] + settled[i+1:], True)[2] for i in range(len(settled))
)
print('Part 2:', cnt2)