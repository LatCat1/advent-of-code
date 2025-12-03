from loader import load_data
from collections import defaultdict
from dataclasses import dataclass

data = load_data(2, 2025, testing=False)

# Range of IDs, _inclusive_ [a,b]
@dataclass
class Range:
    start: int
    stop: int

ranges: list[Range] = []

for s in data.split(','):
    a, b = s.split('-')
    ranges.append(Range(int(a), int(b)))

def is_valid(id: int):
    # IF its a sequence of digits repeated exactly twice
    n = len(str(id))
    for k in range(1, n//2+1):
        if n % k == 0 and n != k:
            valid = False
            t = id % 10**k
            for h in range(1, n // k):
                # print(t, k, h, (id // (10**(k*h))) % (10**(k)))
                if t != (id // (10**(k*h))) % (10**(k)):
                    valid = True
                    break
            if not valid:
                return False
    return True

s = 0
for r in ranges:
    for id in range(r.start, r.stop+1):
        if not is_valid(id):
            s += id
print(s)