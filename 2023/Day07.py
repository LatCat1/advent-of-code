from loader import load_data
from functools import lru_cache, reduce

data = load_data(day=7, year=2023, testing=False)
data = data.split('\n')


m1 = { 'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, }
m2 = { 'A': 14, 'K': 13, 'Q': 12, 'J':  0, 'T': 10, }

def cts(s):
    z = {}
    for n in s:
        z[n] = z.get(n, 0) + 1
    return tuple(sorted(z.values(), reverse=True))

part_1 = []
part_2 = []
for d in data:
    hand, bid = d.split(' ')
    cts_no_j = list(cts(hand.replace('J', '')))
    if len(cts_no_j) == 0:
        cts_no_j = [0]
    cts_no_j[0] += hand.count('J')
    hand_rank = tuple(cts_no_j)

    hand_vals_1 = tuple(int(m1.get(a, a)) for a in hand)
    hand_vals_2 = tuple(int(m2.get(a, a)) for a in hand)
    bid = int(bid)
    part_1.append((cts(hand), hand_vals_1, bid))
    part_2.append((hand_rank, hand_vals_2, bid))

part_1 = sorted(part_1)
part_2 = sorted(part_2)
p1 = 0
p2 = 0
for i in range(len(part_1)):
    p1 += (i+1) * part_1[i][2]
    p2 += (i+1) * part_2[i][2]
print(p1)
print(p2)