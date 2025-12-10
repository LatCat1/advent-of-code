from loader import load_data
from functools import lru_cache
from datetime import datetime, timedelta
from collections import defaultdict
from itertools import combinations, product


data = load_data(9, 2025, testing=False).strip().split('\n')

t = datetime.now()

tiles = []
xs, ys = [], []
for r in data:
    a, b = r.split(',')
    xs.append(int(a))
    ys.append(int(b))
    tiles.append((int(a), int(b)))

def area(t1: tuple[int, int], t2: tuple[int, int]):
    return int((abs((t1[0]-t2[0]))+1)*(abs(t1[1]-t2[1])+1))

# compress coordinates
comp_x_to_x = dict(enumerate(sorted(set(xs))))
x_to_comp_x = {comp_x_to_x[cx]: cx for cx in comp_x_to_x}
comp_y_to_y = dict(enumerate(sorted(set(ys))))
y_to_comp_y = {comp_y_to_y[cy]: cy for cy in comp_y_to_y}

def compress(coord):
    return (x_to_comp_x[coord[0]], y_to_comp_y[coord[1]])

def uncompress(comp_coord):
    return (comp_x_to_x[comp_coord[0]], comp_y_to_y[comp_coord[1]])

def comp_area(c1, c2):
    return area(uncompress(c1), uncompress(c2))

compressed_tiles = [
    compress(c) for c in tiles
]

# print(max(comp_area(c1, c2) for c1, c2 in combinations(compressed_tiles, 2)))

compressed_tiles_red_set = set(compressed_tiles)
compressed_tiles_green_set = set()

# make all green tiles
# first, connect tiles together
for i in range(-1, len(compressed_tiles)-1):
    s, e = compressed_tiles[i], compressed_tiles[i+1]
    for a in range(min(s[0], e[0]), max(s[0], e[0])+1):
        for b in range(min(s[1], e[1]), max(s[1], e[1])+1):
            compressed_tiles_green_set.add((a, b))
# now flood fill. this is done by filling from the outside in from the corner
MIN_X = -1
MAX_X = len(comp_x_to_x) + 1
MIN_Y = -1
MAX_Y = len(comp_y_to_y) + 1

def adj(p):
    x, y = p
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

outside = set()
to_check = [(0,0)]
while to_check:
    x, y = to_check.pop()
    if not MIN_X <= x < MAX_X:
        continue
    if not MIN_Y <= y < MAX_Y:
        continue
    if (x, y) in outside:
        continue
    if (x, y) in compressed_tiles_red_set or (x, y) in compressed_tiles_green_set:
        continue
    outside.add((x, y))
    to_check.extend(adj((x, y)))

def corners(p1, p2):
    return [
        (a, b) for a in (p1[0], p2[0]) for b in (p1[1], p2[1])
    ]

# duplicates the lines /shrug
def all_points(s, e):
    for a in range(min(s[0], e[0]), max(s[0], e[0])+1):
        for b in range(min(s[1], e[1]), max(s[1], e[1])+1):
            yield (a, b)

# simplify grid
grid = []
# s = ''
for y in range(MAX_Y-1):
    grid.append([])
    for x in range(MAX_X-1):
        if (x, y) in compressed_tiles_red_set:
            grid[-1].append(True)
            # s += '#'
        elif (x,y) in outside:
            grid[-1].append(False)
            # s += '.'
        else:
            grid[-1].append(True)
            # s += 'O'
    # s += '\n'

def a1(p):
    return (p[1]+1,p[0]+1)

m = -1
for p1, p2 in combinations(compressed_tiles, 2):
    # print('corners:', [(a1(c), grid[c[1]][c[0]]) for c in corners(p1, p2)])
    if comp_area(p1, p2) <= m: # no point in bothering if its definitely smaller
        continue
    if all(grid[c[1]][c[0]] for c in corners(p1, p2)):
        if all(grid[c[1]][c[0]] for c in all_points(p1, p2)):
            # print(a1(p1), a1(p2), comp_area(p1, p2))
            m = comp_area(p1, p2)
e = datetime.now()
print(m, e - t)


# with open('tmp2.txt', 'w') as f:
#     f.write(s)