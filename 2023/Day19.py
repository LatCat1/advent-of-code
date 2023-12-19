from loader import load_data
from functools import lru_cache, reduce
from math import lcm
from operator import mul
from bisect import bisect_left, bisect_right
import heapq as hq
from grid import FiniteGrid

data = load_data(day=19, year=2023, testing=False).split('\n\n')


workflows = {}
for d in data[0].split('\n'):
    name = d.split('{')[0]
    opts = d.split('{')[1][:-1]
    choices = []
    for o in opts.split(',')[:-1]:
        type = o[0]
        dir = o[1]
        val = int(o.split(':')[0][2:])
        if dir == '>':
            dir = '>='
            val += 1
        res = o.split(':')[1]
        choices.append((type, dir, val, res))
    last_opt = opts.split(',')[-1]
    workflows[name] = (choices, last_opt)

funcs = {
    '<': lambda a,b: a < b,
    '>': lambda a,b: a > b,
    '>=': lambda a,b: a >= b
}

def run(thing):
    curr = 'in'
    while curr not in 'AR':
        moves, back = workflows[curr]
        for m in moves:
            if funcs[m[1]](thing[m[0]], m[2]):
                curr = m[3]
                break
        else:
            curr = back
    return curr

parts = []
for d in data[1].split('\n'):
    v = {}
    for q in  d[1:-1].split(','):
        v[q[0]] = int(q[2:])
    parts.append(v)


print('Part 1:',
    sum(p[i] for p in parts for i in p if run(p) == 'A')
)

# ranges are [include, exclude)
ranges = [
    ('in', {'x':(1,4001),
    'm':(1,4001),
    'a':(1,4001),
    's':(1,4001)})
]

count = 0
while ranges != []:
    current_state, rs = ranges.pop()
    if current_state == 'A':
        count += reduce(
            lambda x, y : x * y,
            (x[1]-x[0] for x in rs.values())
        )
    if current_state in 'AR':
        continue
    wf_moves, wf_back = workflows[current_state]
    for (t, dir, val, res_state) in wf_moves:
        # if we're between the vals
        if rs[t][0] < val < rs[t][1]:
            cp = rs.copy()
            full_range = rs[t]
            rs[t] = (full_range[0], val)
            cp[t] = (val, full_range[1])
            if rs[t][1] > rs[t][0]:
                ranges.append((current_state, rs))
            if cp[t][1] > cp[t][0]:
                ranges.append((current_state, cp))
            break
        elif funcs[dir](rs[t][0], val):
            # move it all together
            ranges.append((res_state, rs))
            break
    else:
        ranges.append((wf_back, rs)) # push everything to next state
print(count)