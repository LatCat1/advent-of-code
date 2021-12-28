import pathlib
import heapq

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day15.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

grid = {}
for l in range(len(lines)):
    for l2 in range(len(lines[l])):
        grid[(l2,l)] = int(lines[l][l2])
xmax = len(lines)
ymax = len(lines[0])

# for p2 ew
quintuplegrid = {}
for x in range(xmax):
    for y in range(ymax):
        for i in range(5):
            for i2 in range(5):
                quintuplegrid[(x+i*xmax,y+i2*ymax)] = 1+ (grid[(x,y)]+i+i2-1)%9
grid = quintuplegrid
xmax *= 5
ymax *= 5
def shortestpathalgo(start,grid, adjacent, end):
    heap = [(0, start)]
    found = {}
    while end not in found:
        weight, loc = heapq.heappop(heap)
        # print(weight, loc)
        if loc not in found:
            found[loc] = weight #add it to the 'founds'
            for e in adjacent(loc):
                if e in grid and e not in found:
                    heapq.heappush(heap, (weight+grid[e], e))

    return found[end]

adjacent = lambda p: [(p[0]+a,p[1]+b) for (a,b) in [(1,0),(-1,0),(0,1),(0,-1)]]
print(shortestpathalgo((0,0),grid,adjacent,(xmax-1, ymax-1)))