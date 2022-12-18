import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    lines = f.read().split('\n')

grid = set(tuple(map(int, l.split(','))) for l in lines)  #3D grid

dirs = [
    (1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)
]

min_limit = min(sum(map(list, grid), [])) - 1
max_limit = max(sum(map(list, grid), [])) + 1
limits = [min_limit, max_limit]
outside = set()
to_check = [(min_limit, min_limit, min_limit)]

while len(to_check) > 0:
    (x,y,z) = to_check.pop(0)
    if (x,y,z) not in outside:
        outside.add((x,y,z))
        for dx, dy, dz in dirs:
            if (x+dx,y+dy,z+dz) not in grid and min_limit<=x+dx<=max_limit and min_limit<=y+dy<=max_limit and min_limit<=z+dz<=max_limit and (x+dx,y+dy,z+dz) not in outside:
                to_check.append((x+dx,y+dy,z+dz))

p1_count = 0
p2_offset = 0
for (x,y,z) in grid:
    for dx, dy, dz in dirs:
        if (x+dx,y+dy,z+dz) not in grid:
            p1_count += 1
            if not (x+dx,y+dy,z+dz) in outside:
                p2_offset += 1
print(f'P1: {p1_count}\nP2: {p1_count-p2_offset}')