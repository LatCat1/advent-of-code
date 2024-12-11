from loader import load_data
from collections import defaultdict
import re
from functools import lru_cache
from datetime import datetime
import heapq as hq

data = load_data(9, 2024, testing=True)
data = load_data(9, 2024, testing=False)

data = data.split('\n')[0]

ids = []
for i, d in enumerate(data):
    if i % 2 == 0:
        ids.extend(i//2 for _ in range(int(d)))
    else:
        ids.extend(-1 for _ in range(int(d)))


i = 0
while i < len(ids):
    if ids[i] != -1:
        pass
    else:
        ids[i] = ids.pop()
    i += 1
    while ids[-1] == -1:
        ids.pop()

print(
    sum(l*x for l, x in enumerate(ids))
)

now = datetime.now()
# how long each file is
files = {}
# where each file starts
file_locs = {}
# pairs; where it starts and how long it is
spaces = []


t = 0
for i, d in enumerate(data):
    if i % 2 == 0:
        files[i//2] = int(d)
        file_locs[i//2] = t
    else:
        spaces.append((t, int(d)))
    t += int(d)

# maps each space to locs it appears
# each appearance is a _stack_ with earlier later
b_spaces = defaultdict(list)
for a, b in spaces:
    hq.heappush(b_spaces[b], a)

b_spaces[0] = []
for i in sorted([f for f in files], reverse=True):
    l = files[i]
    spot = None
    spot_len = 0
    for try_l in range(l, 10):
        # print(f"{try_l=}")
        if b_spaces[try_l] != [] and spot is None:
            spot = hq.heappop(b_spaces[try_l])
            spot_len = try_l
        elif b_spaces[try_l] != []:
            # maybe its better
            new_spot = b_spaces[try_l][0]
            if new_spot < spot:
                # found something better
                hq.heappush(b_spaces[spot_len], spot)
                spot = hq.heappop(b_spaces[try_l])
                spot_len = try_l

    if spot is None or spot >= file_locs[i]:
        continue

    # print('moving', i, 'to', spot, try_l)
    new_spot = spot + l
    file_locs[i] = spot
    new_spot_len = spot_len - l
    hq.heappush(b_spaces[new_spot_len], new_spot)
    b_spaces[0] = []
    spot = None

print(
    sum(
        p * sum(x for x in range(file_locs[p], file_locs[p] + files[p]))
        for p in file_locs
    )
)
print(datetime.now() - now)