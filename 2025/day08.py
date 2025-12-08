from loader import load_data
from functools import lru_cache
from datetime import datetime, timedelta
from collections import defaultdict


testing = False
N = 1000 if not testing else 10

data = load_data(8, 2025, testing=testing).strip().split('\n')

junctions = [
    [x for x in map(int, d.split(','))] for d in data
]
junctions = [tuple(j) for j in junctions]

junc_to_circuit = { j: None for i, j in enumerate(junctions) }

def dist(j1, j2):
    return sum((a - b)**2 for a, b in zip(j1, j2)) ** 0.5

dists = []
for i in range(len(junctions)):
    for i2 in range(i+1, len(junctions)):
        dists.append((dist(junctions[i], junctions[i2]), junctions[i], junctions[i2]))

dists = sorted(dists, reverse=True)
dists2 = dists[:]
circuit_count = len(junctions)
for i in range(N):
    _, j1, j2 = dists.pop() # pop the back
    # make sure j1 and j2 aren't in the same circuit
    # print(j1, j2)
    j1_ = j1
    while junc_to_circuit[j1_] is not None:
        j1_ = junc_to_circuit[j1_]
        junc_to_circuit[j1] = j1_
    j1 = j1_
    j2_ = j2
    while junc_to_circuit[j2_] is not None:
        j2_ = junc_to_circuit[j2_]
        junc_to_circuit[j2] = j2_
    j2 = j2_
    if j1 == j2:
        continue
    junc_to_circuit[max(j1, j2)] = min(j1, j2)
    circuit_count -= 1

# maps each circuit to its size
circuits = defaultdict(lambda : 0)

for j in junc_to_circuit:
    while junc_to_circuit[j] is not None:
        j = junc_to_circuit[j]
    circuits[j] += 1

circuits_sizes = sorted(
    (circuits[j] for j in circuits), reverse=True
)
print(circuits_sizes[0]*circuits_sizes[1]*circuits_sizes[2])

# add the shortests
while circuit_count > 2:
    _, j1, j2 = dists.pop() # pop the back
    # make sure j1 and j2 aren't in the same circuit
    # print(j1, j2)
    j1_ = j1
    while junc_to_circuit[j1_] is not None:
        j1_ = junc_to_circuit[j1_]
        junc_to_circuit[j1] = j1_
    j1 = j1_
    j2_ = j2
    while junc_to_circuit[j2_] is not None:
        j2_ = junc_to_circuit[j2_]
        junc_to_circuit[j2] = j2_
    j2 = j2_
    if j1 == j2:
        continue
    junc_to_circuit[max(j1, j2)] = min(j1, j2)
    circuit_count -= 1 

# now find the next one that will make a 'new' connection
while True:
    _, j1, j2 = dists.pop() # pop the back
    a, b = j1, j2
    # make sure j1 and j2 aren't in the same circuit
    # print(j1, j2)
    j1_ = j1
    while junc_to_circuit[j1_] is not None:
        j1_ = junc_to_circuit[j1_]
        junc_to_circuit[j1] = j1_
    j1 = j1_
    j2_ = j2
    while junc_to_circuit[j2_] is not None:
        j2_ = junc_to_circuit[j2_]
        junc_to_circuit[j2] = j2_
    j2 = j2_
    if j1 == j2:
        continue
    print(a[0]*b[0])
    break