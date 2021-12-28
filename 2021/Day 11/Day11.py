import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day11.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

grid = {} # map from position to (if it flashed this round, power)
for y in range(len(lines)):
    for x in range(len(lines[y])):
        grid[(x,y)] = (False, int(lines[y][x]))

# steps a position on the grid recursively
def step(pos):
    # if position is in the grid:
    if pos in grid:
        (flashed, power) = grid[pos]
        if not flashed:
            power += 1
            if power > 9:
                flashed = True
                grid[pos] = (flashed, power) # update that you flashed
                (x,y) = pos
                [step((x+dx, y+dy)) for dx in [-1,0,1] for dy in [-1,0,1]]
            else:
                grid[pos] = (flashed, power) # just increase your power by 1

def step_grid():
    for p in grid:
        step(p)
    flashed = 0
    for p in grid:
        if grid[p][0]:
            grid[p] = (False, 0)
            flashed += 1
    return flashed

# unfortunately with the way the code is calculated, there is not a great way to have both
# part 1 and part 2 print

# part 1
# total_steps = 100
# total_flashes = sum([step_grid() for _ in range(total_steps)])
# print(total_flashes)

# part 2
num_steps = 1
while step_grid() != len(grid):
    num_steps += 1
print(num_steps)