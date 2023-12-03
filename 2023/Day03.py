from loader import load_data
from functools import lru_cache, reduce

data = load_data(day=3, year=2023, testing=False)


def adj(x, y):
    return [(x+i, y+j) for i in range(-1,2) for j in range(-1, 2)
            if i or j]
data = data.split('\n')

data = [r + '.' for r in data]

rows = len(data)
cols = len(data[0])

m = {}
for i in range(len(data)):
    for j in range(len(data[i])):
        m[(i,j)] = data[i][j]
data = m

gears = {l: [] for l in data if data[l] == '*'}

p1 = 0
for r in range(rows):
    i = 0
    curr_pnum = ''
    adj_gears = []
    good = False
    while i < cols:
        l = (r,i)
        if data[l].isdigit():
            curr_pnum += data[l]
            for l_ in adj(*l):
                good = good or data.get(l_) != '.' and not data.get(l_, '.').isdigit() 
                if data.get(l_, '.') == '*':
                    adj_gears.append(l_)
        else:
            if good:
                p1 += int(curr_pnum)
                for g in set(adj_gears):
                    gears[g].append(int(curr_pnum))
            curr_pnum = ''
            good = False
            adj_gears = []
        i += 1

p2 = sum(gears[g][0] * gears[g][1] 
         for g in gears if len(gears[g]) == 2)
print(f"Part 1: {p1}\nPart 2: {p2}")

