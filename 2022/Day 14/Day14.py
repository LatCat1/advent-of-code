import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    lines = f.read().split('\n')

paths = []
for l in lines:
    paths.append([])
    for z in l.split('->'):
        paths[-1].append(tuple(map(int, z.split(','))))

sand_start = (500, 0)
grid = set()
for pth in paths:
    for i in range(len(pth)-1):
        start = pth[i]
        end = pth[i+1]
        # add everything between them to grid as #
        sx, sy = start
        ex, ey = end
        for tx in range(min(sx, ex), max(sx,ex)+1):
            for ty in range(min(sy, ey), max(sy, ey)+1):
                grid.add((tx, ty))

rock_size = len(grid)
floory = max(map(lambda x: x[1], grid)) + 2
p1_done = False
path = [sand_start]
while sand_start not in grid:
    # spawn a sand and keep moving it
    sx, sy = path[-1]
    while True:
        path.append((sx, sy))
        if (sx, sy+1) not in grid:
            sy += 1
        elif (sx-1, sy+1) not in grid:
            sx -= 1
            sy += 1
        elif (sx+1, sy+1) not in grid:
            sx += 1
            sy += 1
        else:
            break
        # check if on ground. stop it
        if floory == sy + 1:
            if not p1_done:
                print('p1:', len(grid) - rock_size)
            p1_done = True
            break
        # print(path)
    # done moving
    path.pop(-1)
    path.pop(-1)
    grid.add((sx, sy))

print('p2:', len(grid) - rock_size)