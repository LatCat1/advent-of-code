from loader import load_data
from collections import defaultdict
import re
from functools import lru_cache
from datetime import datetime
import heapq as hq

data = load_data(10, 2024, testing=True)
# data = load_data(10, 2024, testing=False)

data = data.split('\n')

grid = {}
for i in range(len(data)):
    for j in range(len(data[i])):
        grid[i+j*1j] = int(data[i][j])


# counts how many ends are reachable from each location
dirs = [1, -1, 1j, -1j]

def adj(l):
    return [l+d for d in dirs if l+d in grid]

reachable = {} # how many starts can reach this spot

# my issue is with adjacent same numbers

def find(loc):
    found = set()

    def q(l):
        if grid[l] == 9:
            return 1
        r = 0
        for a in adj(l):
            if grid[a] == grid[l] + 1:
                r += q(a)
        return r

    return q(loc)

print(
    sum(find(l) for l in grid if grid[l] == 0)
)