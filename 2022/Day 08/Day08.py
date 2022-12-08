import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    lines = f.read().split('\n')

grid = {}
visible = set()

for i in range(len(lines)):
    for j in range(len(lines[i])):
        grid[(i,j)] = int(lines[i][j])


# coming in from the sides
for i in range(0, len(lines)):
    best_so_far = -1
    for j in range(len(lines[i])):
        if grid[(i, j)] > best_so_far:
            visible.add((i,j))
        best_so_far = max(best_so_far, grid[(i,j)])

    best_so_far = -1
    for j in range(len(lines[i])-1, -1, -1):
        if grid[(i, j)] > best_so_far:
            visible.add((i,j))
        best_so_far = max(best_so_far, grid[(i,j)])


# coming from the top/bottom
for j in range(0, len(lines[0])):
    best_so_far = -1
    for i in range(len(lines)):
        if grid[(i, j)] > best_so_far:
            visible.add((i,j))
        best_so_far = max(best_so_far, grid[(i,j)])

    best_so_far = -1
    for i in range(len(lines)-1, -1, -1):
        if grid[(i, j)] > best_so_far:
            visible.add((i,j))
        best_so_far = max(best_so_far, grid[(i,j)])

print(f'There are {len(visible)} visible trees')

def viewdistance(x,y):
    t = 1
    for dirx, diry in [(1,0), (-1,0), (0,1), (0,-1)]:
        tx = x + dirx
        ty = y + diry
        while (tx,ty) in grid and grid[(tx,ty)] < grid[(x,y)]:
            tx += dirx
            ty += diry
        t *= ((abs(x - tx)) + (abs(y-ty)) - (1 if (tx,ty) not in grid else 0))
        # print(t)
    return t

# print(viewdistance(3,2))

print(f'The best tree has a visibility score of {max(viewdistance(*p) for p in grid)}')