from loader import load_data
from collections import defaultdict
import re
from functools import lru_cache, reduce, total_ordering
from datetime import datetime
import heapq as hq
from operator import or_

data = load_data(21, 2024, testing=False)
# data = load_data(21, 2024, testing=True)

numpad = {c: x*1j+y*1 for x, r in enumerate('789\n456\n123\n 0A'.split('\n')) for y, c in enumerate(r)}
dirpad = {c: x*1j+y*1 for x, r in enumerate(' ^A\n<v>'.split('\n')) for y, c in enumerate(r)}


# find a path between x and y 
@lru_cache
def path(x, y):
    pad = numpad if x in numpad and y in numpad else dirpad
    diff = pad[y] - pad[x]
    dx, dy = int(diff.real), int(diff.imag)
    yy = ("^"*-dy) + ("v"*dy)
    xx = ("<"*-dx) + (">"*dx)


    # this is some black magic for preferring a certain
    # direction sometimes. i dont get it
    bad = pad[' '] - pad[x]
    prefer_yy_first = (dx>0 or bad==dx) and bad!=dy*1j
    ret = (yy+xx if prefer_yy_first else xx+yy) + "A"
    return ret



@lru_cache
def length( asdf, robots):
    if robots == 0:
        return len(asdf)
    return sum(
        length(path(asdf[i-1], c), robots-1) for i, c in enumerate(asdf) 
    )


print(
    sum(int(d[:-1]) * length(d, 26) for d in data.split('\n'))
)