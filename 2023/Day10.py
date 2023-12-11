from loader import load_data
from functools import lru_cache, reduce
from math import lcm
from operator import mul


data = load_data(day=10, year=2023, testing=False)
data = data.split('\n')

pipe_adj = {
    '|': [(-1, 0), (1, 0)],
    '-': [(0, -1), (0, 1)],
    'F': [(0, 1), (1, 0)],
    'J': [(0, -1), (-1, 0)],
    'L': [(0, 1), (-1, 0)],
    '7': [(0, -1), (1, 0)],
    '.': [],
    'S':[(-1, 0), (1, 0), (0,1), (0,-1)] 
}
# pad data with '.' everywhere around
data = ['.' + d + '.' for d in data]
data = ['.'*len(data[0])] + data + ['.'*len(data[0])]
grid = {
}
for y in range(len(data)):
    for x in range(len(data[0])):
        if data[y][x] == 'S':
            start = (y, x)
        grid[(y, x)] = data[y][x]

def get_adj(loc, t=None):
    y, x = loc
    if t is None:
        dnext = pipe_adj[grid.get(loc, '.')]
    else:
        dnext = pipe_adj[t]
    return [(y+dy, x+dx) for (dy, dx) in dnext]

def follow_path(loc, prev):
    path = [prev]
    while grid[loc] != 'S':
        ops = get_adj(loc)
        if len(ops) != 2:
            return None
        next = ops[0] if ops[0] != prev else ops[1]
        if loc not in get_adj(next):
            return None
        loc, prev = next, loc
        path.append(prev) 
    return path

# find the start
loop = None
for attempt in get_adj(start):
    if loop is not None:
        break
    loop = follow_path(attempt, start)
print('Part 1:', len(loop)//2)

connected = {}
for l in loop:
    c = set()
    adj = get_adj(l)
    for a in adj:
        if l in get_adj(a):
            c.add(a)
    connected[l] = c

dual = {}
for l in grid:
    up, down, right, left = get_adj(l, 'S')
    (x, y) = l
    up_l, up_r, dw_l, dw_r = \
        [(x+i, y+j) for i in range(2) for j in range(2)]
    # reorder them to be related rotationally
    next = [up, right, down, left]
    check = [up_l, up_r, dw_r, dw_l]
    poss = [next[i] for i in range(4) 
            if check[i] not in connected.get(check[(i+1)%4], [])]
    # print(poss)
    dual[l] = poss

# flood fill
outside = set()
to_check = {(0,0)}
while to_check != set():
    l = to_check.pop()
    if l in outside or l not in dual:
        continue
    outside.add(l)
    for a in dual[l]:
        to_check.add(a)

inside = set(grid.keys()) - set(
    (x+dx, y+dy) for (x,y) in outside for (dx, dy) in [(0,0),(1,0),(0,1),(1,0)]
) - set(loop)

print("Part 2:", len(inside))