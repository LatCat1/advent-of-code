from loader import load_data
from functools import lru_cache
from datetime import datetime, timedelta

data = load_data(7, 2025, testing=False).split('\n')

splitters = set()
start = None
for (i, x) in enumerate(data):
    for (j, d) in enumerate(x):
        if d == '^':
            splitters.add(i+j*1j)
        if d == 'S':
            start = i+j*1j

max_vert = len(data) - 1

beam_locs: set[complex] = set()
to_run: list[complex] = [start]

s = datetime.now()
while to_run:
    l: complex = to_run.pop()
    if l in beam_locs: # already checked
        continue
    if l.real > max_vert: # too far down
        continue
    beam_locs.add(l)
    if l in splitters:
        # add left and right
        to_run.append(l + 1j)
        to_run.append(l - 1j)
    else:
        to_run.append(l+1)

c = len(splitters & beam_locs)
print(datetime.now() - s)
print(c)


@lru_cache(10000)
def num_futures(loc : complex):
    if loc.real > max_vert:
        return 1
    if loc in splitters:
        return num_futures(loc+1j) + num_futures(loc-1j)
    return num_futures(loc+1)

s = datetime.now()
c = num_futures(start)
print(datetime.now() - s)
print(c)
