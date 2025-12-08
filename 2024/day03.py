from loader import load_data
from collections import defaultdict
import re
from functools import lru_cache

# data = load_data(3, 2024, testing=True)
data = load_data(3, 2024, testing=False)


p = r'mul\(([0-9]+),([0-9]+)\)'
p2 = r'do\(\)'
p3 = r"don't\(\)"

s = 0
enabled = 1
while(data):
    if match := re.match(p, data):
        s += enabled* int(match.group(1)) * int(match.group(2))
    if re.match(p2, data):
        enabled = 1
    if re.match(p3, data):
        enabled = 0
    data = data[1:]
print(s)