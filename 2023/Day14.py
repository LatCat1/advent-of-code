from loader import load_data
from functools import lru_cache, reduce
from math import lcm
from operator import mul
from bisect import bisect_left, bisect_right
from heapq import *

data = load_data(day=14, year=2023, testing=False)
data = data.split('\n')


grid = {}
for i in range(len(data)):
    for j in range(len(data[i])):
        grid[(i,j)] = data[i][j]

width = len(data[0])
height = len(data)

def show():
    for y in range(height):
        for x in range(width):
            print(grid[(y,x)],end='')
        print()
def roll_north():
    for y in range(height):
        for x in range(width):
            # get whatever is sitting there
            y_temp = y
            l = grid[(y,x)]
            if l == 'O':
                while grid.get((y-1,x), '#') == '.':
                    grid[(y-1,x)] = 'O'
                    grid[(y,x)] = '.'
                    y -= 1
            y = y_temp
    return grid


def eval():
    s = 0
    for l in grid:
        if grid[l] == 'O':
            s += height - l[0]
    return s

def rot(grid, height, width):
    new = {}
    for l in grid:
        new_l = (l[1],width-l[0]-1)
        new[new_l] = grid[l]
    grid = new
    return width, height, grid

def state(grid, height, width):
    s = ''
    for i in range(height):
        for j in range(width):
            s += grid[(i,j)]
    return s




states = {}
for c in range(1000000000):
    curr = state(grid, height, width)
    if curr not in states:
        states[curr] = c
    else:
        p = c - states[curr]
        in_loop = 1000000000 - states[curr]
        to_do = in_loop % p
        for _ in range(to_do):
            for __ in range(4):
                roll_north()
                height, width, grid = rot(grid, height, width)
        print(eval())
        exit()

    for __ in range(4):
        roll_north()
        height, width, grid = rot(grid, height, width)
