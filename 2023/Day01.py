from loader import load_data
from functools import lru_cache

data = load_data(day=1, year=2023)

data = data.split('\n')

nums = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}

def firstnum(s, d):
    if s == '':
        return '0'
    if '0' <= s[0] and s[0] <= '9':
        return s[0]
    for t in nums:
        print(s[:len(t)])
        if s[:len(t)] == t[::d]:
            return str(nums[t])
    return firstnum(s[1:], d)

s = 0
for d in data:
    s += (int(firstnum(d,1) + firstnum(d[::-1], -1)))
print(s)