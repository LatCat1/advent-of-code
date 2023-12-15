from loader import load_data
from functools import lru_cache, reduce
from math import lcm
from operator import mul
from bisect import bisect_left, bisect_right
import heapq as hq

data = load_data(day=15, year=2023, testing=False)
data = data.replace('\n', '')
data = data.split(',')


def HASH(string):
    cval = 0
    for s in string:
        cval += ord(s)
        cval *= 17
        cval %= 256
    return cval

print("Part 1:", sum(HASH(s) for s in data))

boxes = { i:{} for i in range(256) }

for s in data:
    if '=' in s:
        label, amt = s.split('=')
        box = HASH(label)
        boxes[box][label] = int(amt)
    elif '-':
        label = s[:-1]
        box = HASH(label)
        if label in boxes[box]:
            boxes[box].pop(label)

print("Part 2:", sum(
    (b+1) * (i+1) * boxes[b][lens] 
    for b in boxes 
    for i, lens in enumerate(boxes[b])
))