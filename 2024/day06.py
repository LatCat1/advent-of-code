from loader import load_data
from collections import defaultdict
import re
from functools import lru_cache

data = load_data(6, 2024, testing=True)
data = load_data(6, 2024, testing=False)



def run(data):
    data = data.split('\n')


    x = None
    y = None

    def rot(a, b):
        return (b, -a)

    for a in range(len(data)):
        for b in range(len(data[0])):
            if data[a][b] == '^':
                x, y = a, b

    dx = -1
    dy = 0

    s = 0
    while 0 <= x < len(data) and 0 <= y < len(data[0]) and s <= len(data) * len(data[0]) * 4:
        s += 1
        # try to step forward
        data[x] = data[x][:y] + 'X' + data[x][y+1:]
        while 0 <= x+dx < len(data) and 0 <= y+dy < len(data[0]) and data[x+dx][y+dy] == '#':
            dx, dy = rot(dx, dy)
        x += dx
        y += dy 
    if s >= len(data) * len(data[0]) * 4:
        # for d in data:
        #     print(d)
        # # input()
        return 1
    return 0

    # for d in data:
        # print(d)
    # input()

q = 0
for i in range(len(data)):
    print(i, len(data))
    if data[i] != '^' and data[i] != '\n' and data[i] != '#':
        q += run(data[:i] + '#' + data[i+1:])
print(q)
