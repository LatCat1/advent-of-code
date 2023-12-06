from loader import load_data
from functools import lru_cache, reduce
from math import ceil, floor

data = load_data(day=6, year=2023, testing=False)
data = data.replace(' ', '')
data = data.split('\n')
data = [d.split(':')[1].split() for d in data]

ps = [(int(data[0][i]), int(data[1][i])) for i in range(len(data[0]))]

def count_ways(time, dist):
    dist = dist + 0.0001
    disc = (time**2 - 4*dist)**0.5
    ma =(time + disc) / 2.0
    mi = (time - disc) / 2.0

    return max(floor(ma) - ceil(mi), -1) + 1

d = [count_ways(*p) for p in ps]
x = 1
for n in d:
    x *= n
print(x)