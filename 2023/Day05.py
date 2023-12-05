from loader import load_data
from functools import lru_cache, reduce

data = load_data(day=5, year=2023, testing=True)
data = data.split('\n\n')

seeds = data[0].split(':')[1].strip().split(' ')
curr = [int(s) for s in seeds]

maps = data[1:]

def pmap(m):
    m = m.split('\n')[1:]
    x = []
    for r in m:
        a, b, c = r.split(' ')
        x.append((int(a), int(b), int(c)))
    return x


def appmap(n, map):
    for (dest, src, l) in map:
        if 0 <= n - src and n - src < l:
            return dest + n - src
    return n

# for m in maps:
    # p = pmap(m)
    # curr = [appmap(c, p) for c in curr]
# print(min(curr))


# does r1 - r2
def diff(r1, r2):
    s1, e1 = r1
    s2, e2 = r2
    return [(s1, s2), (e2, e1)]

def simplify(ranges):
    return [r for r in ranges if r[1] > r[0]]

def appmap2(r, map):
    s, e = r
    for (dest, src, l) in map:
        overlap = (max(s, src), min(e, src+l))
        if overlap[1] > overlap[0]: # if nonempty:
            rm = simplify(diff(r, overlap))
            return [(overlap[0]+dest-src, overlap[1]+dest-src)] + \
                sum((appmap2(z, map) for z in rm), start=[])
    return [r]

rs = [(curr[i], curr[i]+curr[i+1]) for i in range(0, len(curr), 2)]
for m in maps:
    p = pmap(m)
    rs = simplify(sum((appmap2(j, p) for j in rs), start=[]))
print(min(t[0] for t in rs))