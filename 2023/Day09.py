from loader import load_data
from functools import lru_cache, reduce
from math import lcm
from operator import mul

data = load_data(day=9, year=2023, testing=False)
data = data.split('\n')

histories = [[int(x) for x in r.split()] for r in data]

def lagrance_interpolate(seq, x):
    return sum(
        seq[i]*reduce(mul,((x - j) for j in range(len(seq)) if i != j))//\
               reduce(mul,((i - j) for j in range(len(seq)) if i != j))
        for i in range(len(seq))
    )

p1 = sum(lagrance_interpolate(h, len(h)) for h in histories)
p2 = sum(lagrance_interpolate(h, -1)     for h in histories)
print(f"Part 1: {p1}\nPart 2: {p2}")
    