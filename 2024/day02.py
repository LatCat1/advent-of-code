from loader import load_data
from collections import defaultdict

# data = load_data(2, 2024, testing=True)
data = load_data(2, 2024, testing=False)

data = data.split('\n')


def issafe(x):
    if x == sorted(x) or x == sorted(x, reverse=True):
        for r in range(len(x)-1):
            if not (1 <= abs(x[r] - x[r+1]) <= 3):
                return False
        return True
    return False

def issafe2(x):
    return any(issafe(x[:a] + x[a+1:]) for a in range(len(x))) or issafe(x)

s = 0
for d in data:
    levels = [int(l) for l in d.split(' ')]
    if issafe(levels) != issafe2(levels):
        print(levels, issafe(levels), issafe2(levels))
    if issafe2(levels):
        s += 1

print(s)