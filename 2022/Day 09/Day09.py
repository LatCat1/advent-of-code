import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    lines = f.read().split('\n')


def adj(l1, l2):
    a, b = l1
    c, d, = l2
    return abs(a-c) <= 1 and abs(b-d) <= 1

dir_to_d = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, 1),
    'D': (0, -1)
}

locs = [(0,0) for _ in range(10)]
tail_passed = set([(0,0)])

for l in lines:
    dir, dist = tuple(l.split(' '))
    dx, dy = dir_to_d[dir]
    for _ in range(int(dist)):
        # step head position
        hx, hy = locs[0]
        hx += dx
        hy += dy
        locs[0] = (hx, hy)
        #check if tail is *not* adj or under
        for i in range(1, len(locs)):
            if not adj(locs[i], locs[i-1]):
                deltax = locs[i-1][0] - locs[i][0]
                deltay = locs[i-1][1] - locs[i][1]
                if deltax != 0 and deltay != 0:
                    deltax = deltax//abs(deltax)
                    deltay = deltay//abs(deltay)
                else:
                    deltax = deltax//2
                    deltay = deltay//2
                locs[i] = (locs[i][0] + deltax, locs[i][1] + deltay)
        tail_passed.add(locs[-1])

print(len(tail_passed))
