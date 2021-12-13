import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day13.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

# redoes work, idgaf
largestx = 1+max([int(l.split(',')[0]) for l in lines if ',' in l])
largesty = 1+max([int(l.split(',')[1]) for l in lines if ',' in l])

grid = [[False]*largestx for _ in range(largesty)]
for l in lines:
    if ',' in l:
        a = l.split(',')
        grid[int(a[1])][int(a[0])] = True

# foldx and foldy are basically copies of each other, but idk a good way to
# factor it out
def foldx(grid, xpos):
    xwidth = len(grid[0])

    newgrid = []
    for y in range(len(grid)):
        newgrid.append([])
        for x in range(xpos):
            newgrid[-1].append(grid[y][x] or grid[y][(abs(x-xpos)+xpos)%xwidth])

    return(newgrid)

def foldy(grid, ypos):
    ywidth = len(grid)

    newgrid = []
    for y in range(ypos):
        newgrid.append([])
        for x in range(len(grid[0])):
            newgrid[-1].append(grid[y][x] or grid[((abs(y-ypos)+ypos)%ywidth)][x])

    return(newgrid)

instructions = [l for l in lines if '=' in l]
instructions = [(i.split('=')[0][-1], int(i.split('=')[1])) for i in instructions]

for (a,b) in instructions:
    print(a,b, len(grid), len(grid[0]))
    if a == 'x':
        grid = foldx(grid, b)
    elif a == 'y':
        grid = foldy(grid, b)
for g in grid:
    for p in g:
        if p: print('#', end='')
        else: print('.', end='')
    print()