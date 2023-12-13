from loader import load_data
from functools import lru_cache, reduce
from math import lcm
from operator import mul
from bisect import bisect_left, bisect_right

data = load_data(day=13, year=2023, testing=False)
data = data.split('\n\n')


def find_symmetry(pattern):
    # look for horizontal pattern
    sym = set()
    for i in range(1, len(pattern)):
        # i is where the fold happens
        start = pattern[:i][::-1]
        end = pattern[i:]
        o = min(len(start), len(end))
        if o > 0 and end[:o] == start[:o]:
            # found a horizontal with i lines above
            sym.add(100*i)
        
    # transpose it
    z = ['']*len(pattern[0])
    for j in range(len(pattern[0])):
        for i in range(len(pattern)):
            z[j] += pattern[i][j]
    pattern = z

    # look for vertical pattern
    for i in range(1, len(pattern)):
        # i is where the fold happens
        start = pattern[:i][::-1]
        end = pattern[i:]
        o = min(len(start), len(end))
        if o > 0 and end[:o] == start[:o]:
            # found a vertical with i lines above
            sym.add(i)
    return sym
        
print("Part 1:", sum(find_symmetry(p.split('\n')).pop() for p in data))

def smudge_finder(pattern):
    correct_val = find_symmetry(pattern)

    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            sym = pattern[i][j]
            swap_sym = '#' if sym == '.' else '.'
            new_pattern = pattern[:i] + [pattern[i][:j] + swap_sym + pattern[i][j+1:]] + pattern[i+1:]
            new_val = find_symmetry(new_pattern) - correct_val
            if len(new_val) != 0:
                return new_val.pop()
            
print("Part 2:", sum(smudge_finder(p.split('\n')) for p in data))