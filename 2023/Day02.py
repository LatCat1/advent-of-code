from loader import load_data
from functools import lru_cache, reduce

data = load_data(day=2, year=2023, testing=False)

data = data.split('\n')

poss = {
    'red': 12,
    'green': 13,
    'blue': 14
}


s1 = 0
s2 = 0
for r in data:
    if r != '':
        p = True
        id = int(r.split(':')[0].split(' ')[1])
        m = { 'red': 0, 'green': 0, 'blue': 0 }
        for a in r.split(':')[1].split(';'):
            for t in a.split(','):
                _, n, col = t.split(' ')
                n = int(n)
                if n > poss[col]:
                    p = False
                m[col] = max(m[col], n)
        s1 += id if p else 0
        s2 += reduce(lambda a, b: a * b, m.values())
print(f"Part 1: {s1}\nPart 2: {s2}")