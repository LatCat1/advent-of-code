import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day13.txt", 'r') as file:
    lines = [line.rstrip() for line in file]


grid = set()
for l in lines:
    if ',' in l:
        a = l.split(',')
        grid.add((int(a[1]),int(a[0])))

# foldx and foldy are basically copies of each other, but idk a good way to
# factor it out
def fold(dim, pos):
    newgrid = set()
    for p in grid:
        (x,y) = p
        if dim == 0:
            p2 = (pos-abs(x-pos), y)
        elif dim == 1:
            p2 = (x, pos-abs(y-pos))
        newgrid.add(p2)
    return newgrid

foldx = lambda p:fold(1,p)
foldy = lambda p:fold(0,p)

instructions = [l for l in lines if '=' in l]
instructions = [(i.split('=')[0][-1], int(i.split('=')[1])) for i in instructions]

for (a,b) in instructions:
    if a == 'x':
        grid = foldx(b)
    elif a == 'y':
        grid = foldy(b)
for x in range(6):
    for y in range(39):
        print('#' if (x,y) in grid else '.', end='')
    print()