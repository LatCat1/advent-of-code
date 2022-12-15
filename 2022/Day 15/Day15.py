import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    lines = f.read().split('\n')

y = 2000000
valmin = 0
valmax = 4000000

def mdist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

sensors, sdists = {}, {}
for l in lines:
    q = l.split('=')
    sx = int(q[1].split(',')[0])
    sy = int(q[2].split(':')[0])
    bx = int(q[3].split(',')[0])
    by = int(q[4].split(':')[0])
    sensors[(sx, sy)] = (bx, by)
    sdists[(sx, sy)] = mdist((sx, sy), (bx, by))


covered = []
for s in sensors:
    dist_from_sens = sdists[s] #distance for s to beacon
    dist_from_line = mdist(s, (s[0], y))
    if dist_from_sens >= dist_from_line:
        extra = dist_from_sens - dist_from_line
        covered.append((s[0]-extra, s[0] + extra))
covered = sorted(covered, key=lambda x:x[0])
c2, i = [], 0
while i < len(covered):
    s, e = covered[i] # it's the start
    while i+1 < len(covered) and covered[i+1][0] <= e:
        e = max(covered[i+1][1], e)
        i += 1
    c2.append((s, e))
    i += 1
correction = sum(1 for b in set(sensors.values()) for r in c2 if b[1]==y and r[0]<=b[0]<=b[1])
print('P1: ', sum(s[1] - s[0] + 1 for s in c2) - correction)

# part 2
lines = {-1: [], 1:[]}
for d in lines:
    lines[d] = sorted(set(s[1]-s[0]*d+sdists[s]*pm for s in sensors for pm in [-1,1]))
    lines[d] = [lines[d][i]+1 for i in range(len(lines[d])-1) if lines[d][i]+2==lines[d][i+1]]
point = [((n-p)//2, (n+p)//2) for p in lines[1] for n in lines[-1]][0]
print('P2:', point[0]*4000000+point[1])