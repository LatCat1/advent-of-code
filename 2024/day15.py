from loader import load_data
from collections import defaultdict
import re
from functools import lru_cache
from datetime import datetime
import heapq as hq

data = load_data(15, 2024, testing=True)
data = load_data(15, 2024, testing=False)

data = data.split('\n\n')
g_data, m_data = data
g_data = g_data.split('\n')

m_data = ''.join(m_data.split('\n'))

p = {
    'O': '[]',
    '#': '##',
    '.': '..'
}

grid = {}
robot = None
for i in range(len(g_data)):
    for j in range(len(g_data[0])):
        if g_data[i][j] == '@':
            robot=(i, 2*j)
            grid[(i,2*j)] = '.'
            grid[(i,2*j+1)] = '.'
        else:
            grid[(i,2*j)] = p[g_data[i][j]][0]
            grid[(i,2*j+1)] = p[g_data[i][j]][1]        

dirs = {
    '<': (0, -1),
    '>': (0, 1),
    '^': (-1, 0),
    'v': (1, 0)
}


# steps the grid by a bit
def move(dir, robot):
    rx, ry = robot
    dx, dy = dirs[dir]

    # things we are trying to push
    moving = {robot}
    possible = True
    move_layers = []
    already_set_moving_all = set()
    already_set_moving_all |= moving
    moving_into = {}
    # maps a location into __what moves into it__
    while possible and all(grid[m] != '#' for m in moving) and len(moving) != 0: # while we aren't trying to move a #
        move_layers.append(moving)
        next_move = set()
        for (mx,my) in moving:
            nx, ny = mx+dx, my+dy
            n = (nx, ny)
            if grid[n] == '#':
                possible = False
                break
            elif grid[n] == '[':
                if dx != 0:
                    next_move.add((nx, ny+1))
            elif grid[n] == ']':
                if dx != 0:
                    next_move.add((nx, ny-1))
            if grid[n] != '.': # don't add empty
                next_move.add(n)
        next_move -= already_set_moving_all
        already_set_moving_all |= next_move
        moving = next_move

    nx, ny = rx, ry
    if possible:
        nx, ny = rx+dx, ry+dy
        # move everything over, from the end of the push to the front
        for group in reversed(move_layers):
            for (gx, gy) in group:
                grid[(gx+dx, gy+dy)] = grid[(gx, gy)] # bump it!
                grid[(gx, gy)] = '.'

    return (nx, ny)

def show(robot):
    for i in range(len(g_data)):
        for j in range(2*len(g_data[i])):
            if (i,j) == robot:
                print('@', end='')
            else:
                print(grid[(i,j)],end='')
        print()

# show(robot)
for m in m_data:
    # print(m)
    robot = move(m, robot)
    # show(robot)
    # input()
show(robot)

# score it
print(sum(
    s[0]*100+s[1] for s in grid if grid[s] == '['
))