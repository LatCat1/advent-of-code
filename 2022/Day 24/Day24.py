import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    lines = f.read().split('\n')
    
startloc = (-1, 0)
locs = set()
height = len(lines) - 2
width = len(lines[0]) - 2
endloc = (height, width-1)
left = set()
right = set()
up = set()
down = set()
blizzards_by_time = []
for i in range(1, len(lines)-1):
    for j in range(1, len(lines[i])-1):
        p = (i-1, j-1)
        locs.add(p)
        if lines[i][j] == '>':
            right.add(p)
        elif lines[i][j] == '<':
            left.add(p)
        elif lines[i][j] == '^':
            up.add(p)
        elif lines[i][j] == 'v':
            down.add(p)
locs.add(startloc)
locs.add(endloc)

time_wraparound = height*width # should do lcm
for t in range(0, time_wraparound):
    blizzards_by_time.append({
        (i,(j+t)%width) for (i,j) in right
    } | {
        (i,(j-t)%width) for (i,j) in left
    } | {
        ((i-t)%height,j) for (i,j) in up
    } | {
        ((i+t)%height,j) for (i,j) in down
    })


def run(start, start_time_offset, end, time_max):
    choices = {  # each element of choices is a tuple (cost, location, timestate)
        (0, start, start_time_offset%time_max)
    }
    costs = {  # maps a location to a dict that maps timestates to costs
        p: {} for p in locs
    }

    while len(costs[end]) == 0 and len(choices) > 0: # need a better condition maybe
        c, p, ts = min(choices)
        choices.remove((c,p,ts))
        if ts not in costs[p]:
            costs[p][ts] = c
            # ok now we check everything near
            (i,j) = p
            nt = (ts+1)%time_max
            adj = ({(i,j), (i+1,j), (i-1,j), (i,j+1),(i,j-1)} & locs) - blizzards_by_time[nt]
            for a in adj:
                choices.add((c+1, a, nt))
                
    return list(costs[end][i] for i in costs[end])[0]

c1 = run(startloc, 0, endloc, time_wraparound)
print('P1:',c1)
c2 = run(endloc, c1, startloc, time_wraparound)
c3 = run(startloc, c1+c2, endloc, time_wraparound)
print('P2:', sum([c1, c2, c3]))