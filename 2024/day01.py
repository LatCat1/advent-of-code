from loader import load_data
from collections import defaultdict

data = load_data(1, 2024, testing=False)

l = []
r = []
for d in data.split('\n'):
    x = d.split('   ')
    l.append(int(x[0]))
    r.append(int(x[1]))

l = sorted(l)
r = sorted(r)

print(sum(abs(ll-rr) for (ll,rr) in zip(l, r)))

counts = defaultdict(int)
for rr in r:
    counts[rr] += 1

print(sum(ll*counts[ll] for ll in l))