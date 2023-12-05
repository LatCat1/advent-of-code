from loader import load_data
from functools import lru_cache, reduce

data = load_data(day=5, year=2023, testing=False)
data = data.split('\n\n')

Range = (int, int)

# A common pattern I used was sum(iter, start=[]). This 
# just concatinates a list of lists down to a list.

# Helper functions for intervals; specifi
######################################################

# does r1 \cap r2. 
def intersect(r1: Range, r2: Range) -> Range:
    s1, e1 = r1
    s2, e2 = r2
    return (max(s1, s2), min(e1, e2))

# does r1 - r2
def diff(r1: Range, r2: Range) -> [Range]:
    s1, e1 = r1
    s2, e2 = r2
    return simplify([(s1, s2), (e2, e1)])

# removes all empty ranges from the list
# possibly could merge overlaps
def simplify(ranges: [Range]) -> [Range]:
    return [r for r in ranges if r[1] > r[0]]

# Now for parsing and applying
######################################################
# maps could be represented better, but this works
def parse_map(m):
    m = m.split('\n')[1:]
    x = []
    for r in m:
        a, b, c = r.split(' ')
        x.append((int(a), int(b), int(c)))
    return x

# This recursive structure works, and never causes an infinite loop, because
# if we ever have an overlap, then resulting two-piece difference won't ever
# match on that exact same overlap again. this could definitely be faster -
# there's no need to check everything again - but this was easier to write
def apply_map(r: Range, map) -> [Range]:
    # try to appl
    for (dest, src, l) in map:
        overlap = intersect(r, (src, src+l))
        if overlap[1] > overlap[0]: # if the overlap is real, split it
            rm = simplify(diff(r, overlap))
            return [(overlap[0]+dest-src, overlap[1]+dest-src)] + \
                   sum((apply_map(z, map) for z in rm), start=[])
    # base case, do nothing
    return [r]

seeds = data[0].split(':')[1].strip().split(' ')
seeds = [int(s) for s in seeds]

maps = [parse_map(m) for m in data[1:]]
# For part 1, we just take the options as the given list - so ranges [i, i+1)
part_1_options = [(s, s+1) for s in seeds]
# For part 2, we read the input as a bunch of ranges (start, length)
part_2_options = [(seeds[i], seeds[i]+seeds[i+1]) for i in range(0, len(seeds), 2)]
for (i, opts) in enumerate([part_1_options, part_2_options]):
    for m in maps:
        opts = sum((apply_map(r, m) for r in opts), start=[])
    print(f"Part {i+1}: {min(t[0] for t in simplify(opts))}")