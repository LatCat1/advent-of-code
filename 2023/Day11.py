from loader import load_data
from functools import lru_cache, reduce
from math import lcm
from operator import mul
from bisect import bisect_left, bisect_right

data = load_data(day=11, year=2023, testing=False)
data = data.split('\n')

rows_expanded = []
for i, r in enumerate(data):
    if '#' not in r:
        rows_expanded.append(i)

cols_expanded = []
for j in range(len(data[0])):
    r = ''
    for i in range(len(data)):
        r += data[i][j]
    if '#' not in r:
        cols_expanded.append(j)

rows_expanded = sorted(rows_expanded)
cols_expanded = sorted(cols_expanded)

def count_between(a, b, l):
    # counts the number of elements in l of the form
    a, b = sorted([a,b])
    # a < x < b
    return bisect_left(l, b) - bisect_left(l, a)

def dist(x, y, expansion_amount):
    # get the natural distance
    d = abs(x[0] - y[0]) + abs(x[1] - y[1])
    row_exp = count_between(x[0], y[0], rows_expanded)
    col_exp = count_between(x[1], y[1], cols_expanded)
    d += row_exp * (expansion_amount-1) + col_exp * (expansion_amount-1)
    return d

gals = []
for i in range(len(data)):
    for j in range(len(data[i])):
        if data[i][j] == '#':
            gals.append((i,j))
def run(expansion_amount):
    s = 0
    for i in range(len(gals)):
        for j in range(i+1, len(gals)):
            s += dist(gals[i], gals[j], expansion_amount)
    return s
print(run(2))
print(run(1_000_000))