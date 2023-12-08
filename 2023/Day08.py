from loader import load_data
from functools import lru_cache, reduce
from math import lcm

data = load_data(day=8, year=2023, testing=False)
data = data.split('\n')

asdf = data[0]

ords = {}
for r in data[2:]:
    home = r.split(' ')[0]
    l, r = r.split(' = ')[1][1:-1].split(', ')
    ords[home] = l, r

locs = []
for o in ords:
    if o[-1] == 'A':
        locs.append(o)
def run(l, target='Z'):
    steps = 0
    while l[-len(target):] != target:
        dir = asdf[steps % len(asdf)]
        dir = 0 if dir == 'L' else 1
        steps += 1
        l = ords[l][dir]
    return steps
print(run('AAA', target='ZZZ'))
print(reduce(lcm, (run(x) for x in locs)))