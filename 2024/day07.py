from loader import load_data
from collections import defaultdict
import re
from functools import lru_cache
from datetime import datetime

data = load_data(7, 2024, testing=True)
data = load_data(7, 2024, testing=False)

data = data.split('\n')


rs = {}

for d in data:
    a, b = d.split(': ')
    bbs = b.split(' ')
    rs[int(a)] = [int(b) for b in bbs]


def opts(aa, operators, target=1e20):
    s = {aa[0]}
    for i in range(1, len(aa)):
        ss = set()
        for o in operators:
            ss |= {o(q, aa[i]) for q in s if o(q, aa[i]) <= target}
        s = ss
    return s


add = lambda x, y: x + y
mul = lambda x, y: x * y
con = lambda x, y: int(str(x) + str(y))

n1 = datetime.now()
print("P1:", sum(
    r for r in rs if r in opts(rs[r], [add, mul], r)
))
print("P2:", sum(
    r for r in rs if r in opts(rs[r], [add, mul, con], r)
))
span1 = datetime.now() - n1
print('Method 1 (forward generative) time:', span1)

# Neg 1 is what we choose to use for anything 'invalid'
unadd = lambda acc, y: max(acc - y, -1)
unmul = lambda acc, y: acc // y if acc >= 0 and acc % y == 0 else -1
uncon = lambda acc, y: int(str(acc)[:-len(str(y))]) if acc >= 0 and len(str(acc)) > len(str(y)) and str(acc)[-len(str(y)):] == str(y) else -1

def backwards(target, nums, ops):
    s = {target}
    for i in range(len(nums)-1, -1, -1):
        ss = set()
        for o in ops:
            ss |= {o(acc, nums[i]) for acc in s}
        s = ss
    s.discard(-1)
    return s

tot = []
def checkback(target, nums, ops):
    first = nums[0]
    b = backwards(target, nums[1:], ops)
    tot.append(len(b))
    return first in b

n = datetime.now()
print('P1:', sum(
    r for r in rs if checkback(r, rs[r], [unadd, unmul])
))
print('P2:', sum(
    r for r in rs if checkback(r, rs[r], [unadd, unmul, uncon])
))
span2 = datetime.now() - n
print('Method 2 (backward) time:', span2)


def rec_backwards(nums, targets, ops, so_far, ind=None):
    if ind is None:
        ind = len(nums) - 1
    if ind < 0:
        return so_far in targets
    for op in ops:
        s = op(so_far, nums[ind])
        if s != -1 and rec_backwards(nums, targets, ops, so_far=s, ind=ind-1):
            return True
    return False 

n = datetime.now()
print('P1:', sum(
    r for r in rs if rec_backwards(rs[r][1:], rs[r][0:1], [unadd, unmul], r)
))
print('P2:', sum(
    r for r in rs if rec_backwards(rs[r][1:], rs[r][0:1], [unadd, unmul, uncon], r)
))
span3 = datetime.now() - n
print('Method 3 (backward recursive) time:', span3)


n = datetime.now()
split = 3
print('P1:', sum(
    r for r in rs if rec_backwards(rs[r][split:], opts(rs[r][0:split], [add, mul]), [unadd, unmul], r)
))
print('P2:', sum(
    r for r in rs if rec_backwards(rs[r][split:], opts(rs[r][0:split], [add, mul, con]), [unadd, unmul, uncon], r)
))
span4 = datetime.now() - n
print('Method 4 (meet in middle, recursive) time:', span4)

print((1-span4/span1) * 100)