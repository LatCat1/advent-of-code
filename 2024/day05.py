from loader import load_data
from collections import defaultdict
import re
from functools import lru_cache

data = load_data(5, 2024, testing=True)
data = load_data(5, 2024, testing=False)

data = data.split('\n\n') 

aft = defaultdict(set)
for d in data[0].split('\n'):
    a, b = d.split('|')
    aft[a].add(b)

c = 0
q = 0
for d in data[1].split('\n'):
    l = d.split(',')
    if not any(
        l[i] in aft[l[j]] for i in range(len(l)) for j in range(i+1, len(l))
    ):
        c += int(l[len(l)//2])
    else: # not in the right order
        # now we need to sort it with respec to aft
        # aft[a] is a set of everything that must come after it
        # count edges in
        es = {ll: 0 for ll in l}
        for ll in l:
            for aa in aft[ll]:
                if aa in l:
                    es[aa] += 1
        # brute force

        o = [] 
        ee = None
        while len(es) > len(l)/2:
            for e in es:
                if es[e] == 0:
                    ee = e
                    break
            else:
                assert False, "Didnt find anything"
            es.pop(ee)
            o.append(ee)
            for a in aft[ee]:
                if a in l:
                    es[a] -= 1
        q += int(ee)
print(c)
print(q)


[1,2].sort(cmp=lambda x, y: 0)