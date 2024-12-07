from loader import load_data
from collections import defaultdict
import re
from functools import lru_cache

data = load_data(7, 2024, testing=True)
data = load_data(7, 2024, testing=False)

data = data.split('\n')


rs = {}

for d in data:
    a, b = d.split(': ')
    bbs = b.split(' ')
    rs[int(a)] = [int(b) for b in bbs]


def opts(aa, operators, target=1e20):
    s = {aa[0]}
    for i in range(1, len(aa)):
        ss = set()
        for o in operators:
            ss |= {o(q, aa[i]) for q in s if o(q, aa[i]) <= target}
        s = ss
    return s


add = lambda x, y: x + y
mul = lambda x, y: x * y
con = lambda x, y: int(str(x) + str(y))

print("P1: ", sum(
    r for r in rs if r in opts(rs[r], [add, mul], r)
))
print("P2: ", sum(
    r for r in rs if r in opts(rs[r], [add, mul, con], r)
))