from loader import load_data
from functools import lru_cache, reduce
from math import lcm
from operator import mul
from bisect import bisect_left, bisect_right
import heapq as hq
from grid import FiniteGrid

data = load_data(day=16, year=2023, testing=False)
data = data.split('\n')
grid = FiniteGrid(data)


def find_count(start_loc,dir):
    energized = set()
    checked_already = set()
    heads = [(start_loc, dir)]
    while heads != []:
        l, d = heads.pop()
        if grid.in_bounds(l) and (l,d) not in checked_already:
            energized.add(l)
            checked_already.add((l,d))
            # calculate what happens
            y, x = l
            dy, dx = d
            tile = grid.get(l)
            if tile == '.':
                heads.append(((y+dy, x+dx), d)) # step
            elif tile == '\\':
                if d == (0,1):
                    heads.append(((y+1, x), (1, 0)))
                elif d == (0,-1):
                    heads.append(((y-1, x), (-1, 0)))
                elif d == (1,0):
                    heads.append(((y, x+1), (0, 1)))
                elif d == (-1,0):
                    heads.append(((y, x-1), (0, -1)))
            elif tile == '/':
                if d == (0,1):
                    heads.append(((y-1, x), (-1, 0)))
                elif d == (0,-1):
                    heads.append(((y+1, x), (1, 0)))
                elif d == (1,0):
                    heads.append(((y, x-1), (0, -1)))
                elif d == (-1,0):
                    heads.append(((y, x+1), (0, 1)))
            elif tile == '-':
                if d == (0,1) or d == (0,-1):
                    heads.append(((y+dy, x+dx), d))
                else:
                    heads.append(((y, x+1), (0,1)))
                    heads.append(((y, x-1), (0,-1)))
            elif tile == '|':
                if d == (1, 0) or d == (-1,0):
                    heads.append(((y+dy, x+dx), d))
                else:
                    heads.append(((y+1, x), (1, 0)))
                    heads.append(((y-1, x), (-1, 0)))
            else:
                assert False, "illegal tile"
    return len(energized)

    # for i in range(len(data)):
    #     for j in range(len(data[0])):
    #         if (i,j) in energized:
    #             print('#', end='')
    #         else:
    #             print(grid.get((i,j)),end='')
    #     print()
    # print(heads)

m = max(
    max( # left side
        find_count((i, 0), (0,1)) for i in range(len(data))
    ),
    max( # right side
        find_count((i, len(data[0])-1), (0,-1)) for i in range(len(data))
    ),
    max( # top
        find_count((0, i), (1,0)) for i in range(len(data[0]))
    ),
    max( # bottom
        find_count((len(data)-1, i), (0,-1)) for i in range(len(data[0]))
    ),
)
print(m)
