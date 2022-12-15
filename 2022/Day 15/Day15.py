import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    lines = f.read().split('\n')

def mdist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

real = False

sensors = {}
sdists = {}
for l in lines:
    q = l.split('=')
    sx = int(q[1].split(',')[0])
    sy = int(q[2].split(':')[0])
    bx = int(q[3].split(',')[0])
    by = int(q[4].split(':')[0])
    sensors[(sx, sy)] = (bx, by)
    sdists[(sx, sy)] = mdist((sx, sy), (bx, by))

def ycoverage(y):
    covered = []
    for s in sensors:
        dist_from_sens = sdists[s] #distance for s to beacon
        dist_from_line = mdist(s, (s[0], y))
        if dist_from_sens >= dist_from_line:
            extra = dist_from_sens - dist_from_line
            covered.append((s[0]-extra, s[0] + extra))
    covered = sorted(covered, key=lambda x:x[0])
    new_covered = []
    i = 0
    while i < len(covered):
        s = covered[i][0] # it's the start
        e = covered[i][1]
        while i+1 < len(covered) and covered[i+1][0] <= e:
            e = max(covered[i+1][1], e)
            i += 1
        new_covered.append((s, e))
        i += 1
    return new_covered

y = 2000000 if real else 10
p1_coverage = ycoverage(y)
for b in sensors.values():
    if b[1] == y:
        i = 0
        while i < len(p1_coverage):
            if p1_coverage[i][0] <= b[0] <= p1_coverage[i][1]:
                s, e = p1_coverage.pop(i)
                i -= 1
                for p in [(s, b[0]-1), (b[0]+1, e)]:
                    if p[0] <= p[1]:
                        p1_coverage.append(p)
            i += 1
print('P1: ', sum(s[1] - s[0] + 1 for s in p1_coverage))

# part 2
valmin = 0
valmax = 4000000 if real else 20
possible = []
for y in range(valmin, valmax+1):
    c = ycoverage(y)
    for i in range(len(c)-1):
        if c[i+1][0] - c[i][1] > 1:
            possible.append((c[i][1]+1, y))

for p in possible:
    failed = False
    for s in sensors:
        if mdist(s, p) <= mdist(s, sensors[s]):
            failed=True
    if not failed:
        print('P2:', p[0] * 4000000 + p[1])
        exit()
