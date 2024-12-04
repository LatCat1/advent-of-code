from loader import load_data
from collections import defaultdict
import re
from functools import lru_cache

data = load_data(4, 2024, testing=True)
data = load_data(4, 2024, testing=False)

data = data.split('\n')

g = defaultdict(lambda: ' ')

dirs = [
    (1, 0),
    (1,1),
    (0,1),
    (-1,1)
]

for i in range(len(data)):
    for j in range(len(data[i])):
        g[(i, j)] = data[i][j]

c = 0    
for i in range(len(data)):
    for j in range(len(data[i])):
        for (a,b) in dirs:
            for q in [-1,1]:
                h = ""
                for _ in range(4):
                    h = h + g[(i+q*a*_, j+q*b*_)]
                if h == "XMAS":
                    c += 1
print(c)

c = 0
q = ["MAS", "SAM"]
for i in range(len(data)):
    for j in range(len(data[i])):
        d1 = g[(i-1,j-1)] + g[(i,j)] + g[(i+1,j+1)] 
        d2 = g[(i+1,j-1)] + g[(i,j)] + g[(i-1,j+1)] 

        if d1 in q and d2 in q:
            c += 1

print(c)