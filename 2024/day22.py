from loader import load_data
from collections import defaultdict, Counter
import re
from functools import lru_cache, reduce, total_ordering
from datetime import datetime
import heapq as hq
from operator import or_

data = load_data(22, 2024, testing=True)
data = load_data(22, 2024, testing=False)

P = 16777216

secrets = list(map(int, data.split('\n')))

# there is power of 2 shenanigans going on here
def step(secret):
    secret = (secret ^ (secret * 64)) % P
    secret = (secret ^ (secret // 32)) % P
    secret = (secret ^ (secret * 2048)) % P
    return secret

def rep(val, func, times):
    for _ in range(times):
        val = func(val)
    return val

print(sum(
    rep(s, step, 2000) for s in secrets
))


# Ok now for p2
change_prices = defaultdict(int)
for s in secrets:
    # get the first five?
    a = s
    b = step(a)
    c = step(b)
    d = step(c)
    e = d

    c1, c2, c3, c4 = None,  (b%10)-(a%10), (c%10-b%10), (d%10)-(c%10)
    already_seen = set()
    for i in range(2000-3):
        a, b, c, d, e = b, c, d, e, step(e) # shift over
        c1, c2, c3, c4 = c2, c3, c4, (e%10)-(d%10)
        tup = (c1, c2, c3, c4)

        if tup not in already_seen:
            change_prices[(c1, c2, c3, c4)] += e%10
        already_seen.add(tup)

print(max(change_prices.values()))