from loader import load_data
from functools import lru_cache, reduce
from math import lcm, ceil
from operator import mul
from bisect import bisect_left, bisect_right
import heapq as hq
import queue
from grid import FiniteGrid

data = load_data(day=21, year=2023, testing=False).split('\n')

grid = FiniteGrid(data, default='#')

start = None
for i in range(len(data)):
    for j in range(len(data[i])):
        if data[i][j] == 'S':
            start = (i, j)

# records the min dist
m = len(data)

def adj(l):
    x, y = l
    return [(x+1,y), (x-1, y), (x, y+1), (x, y-1)]

# can't be odd loops
def dists_from(start_loc, extend=None):
    dists = {}
    h = [(0, start_loc)]
    while h != []:
        c, loc = hq.heappop(h)
        sloc = loc
        if extend is not None:
            sloc = (loc[0]%m,loc[1]%m)
        if loc not in dists and grid.get(sloc) != '#' and (True if extend is None else c <= extend):
            dists[loc] = c
            for a in adj(loc):
                hq.heappush(h, (c+1, a))
    return dists

# part 1
def count(from_location, dist, extend=None):
    count_p1 = 0
    dists = dists_from(from_location, extend=extend)
    for l in dists:
        if dists[l] <= dist and dists[l]%2 == (0 if extend is None else extend%2):
            count_p1 += 1
    return count_p1
# things are at most 260 from the corners
print("Part 1", count(start, 64))

steps_2 = 26501365
o = steps_2 % m

def lagrange_interpolate(pairs: list[tuple[int, int]]):
    ys = [t[1] for t in pairs]
    xs = [t[0] for t in pairs]
    return lambda x, xs=xs, ys=ys: sum(
        ys[i]*reduce(mul,((x     - xs[j]) for j in range(len(pairs)) if i != j))//\
              reduce(mul,((xs[i] - xs[j]) for j in range(len(pairs)) if i != j))
        for i in range(len(pairs))
    )

print(
    lagrange_interpolate(
        [(i, count(start, o+i*m, o+i*m)) for i in range(3)]
    )(steps_2//m)
)

# there is an empty border all around; also, S has a direct route
# to the edge

# so lower bound: how many *full squares* are included?
# multiply count_p2 by that for a decent lower bound
# also there is some overlap

# d = steps_2// len(data)
# print(f"{steps_2%len(data)=}")
# print(f"{d=}")
# fully_included_parity = [
#     count(start, float("Inf"), mod=p) for p in (0,1)
# ]

# m = start[0]
width = len(data)

# tot_inside = fully_included_parity[steps_2%2]
# for x in range(0,d-1):
#     tot_inside += fully_included_parity[(steps_2-x*width-1)%2]*(x*4 if x else 1)
# print(f'{tot_inside=}')


# # INNER DIAGONAL. BORDER OF ~D-1?
# diag_len = d-1
# extra_dist_diag = ((steps_2-(2*m+2))%(width))-2+width
# # whats the diagonal parity?
# diag_parity = (steps_2-(d*width+2*m+2-width))%2
# print(f"{diag_parity=}")
# diag_counts = [
#     count(l, extra_dist_diag,mod=diag_parity) for l in [(0,0), (width-1,0), (0,width-1), (width-1, width-1)] 
# ]
# tot_diag = sum(diag_counts)*diag_len

# # OUTER DIAGONAL, of D
# print(f"{width=}")
# diag_len = d
# extra_dist_diag = ((steps_2-(2*m+2))%(width))-2
# print(f"{extra_dist_diag=}")
# # whats the diagonal parity?
# diag_parity = (steps_2-(d*width+2*m+2))%2
# print(f"{diag_parity=}")
# diag_counts = [
#     count(l, extra_dist_diag,mod=diag_parity) for l in [(0,0), (width-1,0), (0,width-1), (width-1, width-1)] 
# ]
# tot_diag += sum(diag_counts)*diag_len

# extra_corner_dist=(steps_2-m-1)%width
# print(f"{extra_corner_dist=}")
# corner_parity = (steps_2-(d*width+m+1))%2
# print(f"{corner_parity=}")
# corners = [
#     count(l, extra_corner_dist, mod=corner_parity) for l in
#     [(m, 0), (0,m), (m,width-1), (width-1, m)]
# ]
# tot_corn = sum(corners)


# print("Part 2:", tot_inside+tot_diag+tot_corn)


# Looked at hints after being increadibly stuck on a couple different
# solution methods that involved trying to intelligently multiply out to
# the number. There i found that it was pointed out:
# f(n), f(n+X), f(n+2X), ... *must* fit a quadratic sequence
# by a rather annoing arguement: the grid is sparse, so it fills up quickly,
# and its a diamond (the corners are constants, and its slope grows linearly)
# this didnt feel good, but honestly after so much frustration with these other
# methods i just want to go to sleep. the tendency this year to rely on
# particular distributions of solutions feels particularly bad




exit()
print('-'*100)
print('Aiden way?')
m = start[0]

orig = dists_from((start))
tl = dists_from((0,0))
top = dists_from((0, m))
tr = dists_from((0, width-1))
left = dists_from((m, 0))
right = dists_from((m, width-1))
bl = dists_from((width-1, 0))
bot = dists_from((width-1, m))
br = dists_from((width-1, width-1))

# ok now for each 'reachable' location, get the parity
# assuming good corridors
steps_2 = 5000#steps_2
half_w = start[0]+1
cnt = 0

# assumes odd grids
p = steps_2%2
for loc in orig:
    d = orig[loc]
    if d > steps_2:
        continue
    parity = d%2 == p
    c = parity if d <= steps_2 else 0
    # directly up/down/left/right
    for dir in (top, left, right, bot):
        d = half_w+1
        # doesnt account for parity
        n = (steps_2-d-dir[loc])//width+(steps_2 > d + dir[loc])
        if n <= 0:
            continue
        # if this is even parity, we want to round up
        # if its odd parity, we want to round down
        if parity: # if we're matching the parity, want to round down to take only the second things
            m = n // 2 # we divide by 2, possibly removing the last
        else: # not matching parity. then we want to take the first out of every pair
            m = (n+1)//2
        c += m
    # diagonals
    for dir in (tl, tr, bl, br):
        d = 2*(half_w+1)
        n = (steps_2-d-dir[loc])//width + (steps_2 > d + dir[loc])
        if n <= 0:
            continue
        # we swap these because its diagonal; so the
        # parity changes twice
        if not parity: # if differing parity, take the second diagonal and so on
            n = (n//2)
            m = n*(n+1) # this is how many right-parity versions
        else:
            # if even parity, take the odds.
            n = ((n+1)//2)*2-1
            q = (n+1)//2
            m = q*(q+1)-ceil(n/2)
        c += m
    cnt += c
print(cnt)