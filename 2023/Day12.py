from loader import load_data
from functools import lru_cache, reduce
from math import lcm
from operator import mul
from bisect import bisect_left, bisect_right

data = load_data(day=12, year=2023, testing=False)
data = data.split('\n')


def process_row(row, reps=1):
    # get nums
    nums = tuple(int(n) for n in row.split(' ')[1].split(','))
    r = row.split(' ')[0]
    r = '?'.join([r]*reps)
    nums = tuple(list(nums)*reps)
    return count_possible(r, nums)

@lru_cache(maxsize=1000)
def count_possible(row, lengths):
    # base case
    if len(row) == 0: 
        return len(lengths) == 0
    if len(lengths) == 0:
        return '#' not in row
    # if we start with ., then recurse taking as many '.' as possible
    if row[0] == '.':
        return count_possible(row[1:], lengths)
    # if we start with ?,
    if row[0] == '?':
        return sum(count_possible(c+row[1:], lengths) for c in '.#')
    # so we start with #. if it is illegal, we vail
    c = lengths[0]
    s = row[:c+1]
    lengths = lengths[1:]
    if len(s) == c+1 and '.' not in s[:-1] and s[-1] != '#' :
        return count_possible(row[c+1:],lengths)
    if len(row) == c and '.' not in row and len(lengths) == 0:
        return 1
    return 0

print("part 1:", sum(process_row(r) for r in data))
print("part 2:", sum(process_row(r, 5) for r in data))