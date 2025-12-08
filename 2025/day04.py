from loader import load_data

data = load_data(4, 2025, testing=False)

locs = set()

for (i, l) in enumerate(data.split('\n')):
    for (j, p) in enumerate(l):
        if p == '@':
            locs.add((i,j))

def adj(x, y):
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx or dy:
                yield (x+dx, y+dy)

removed_counts = []
removed_any = True
while removed_any:
    removed_any = False
    new_locs = set()
    s = 0
    for l in locs:
        if 4 > sum(1 if p in locs else 0 for p in adj(*l)):
            s += 1
            removed_any = True
        else:
            new_locs.add(l)
    locs = new_locs
    removed_counts.append(s)

print(removed_counts[0])
print(sum(removed_counts))