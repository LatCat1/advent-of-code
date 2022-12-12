import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    lines = f.read().split('\n')

heightmap = {}
start = None
end = None
for i in range(len(lines)):
    for j in range(len(lines[i])):
        heightmap[(i,j)] = ord(lines[i][j])-ord('a')
        if lines[i][j] == 'S':
            start = (i,j)
            heightmap[(i,j)] = 0
        elif lines[i][j] == 'E':
            end = (i,j)
            heightmap[(i,j)] = 25

adj = lambda x, y: [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]

best_so_far = {}
to_check = {(end, 0)}
while len(to_check) > 0:
    next = min(to_check, key=lambda x: x[1])
    to_check.remove(next)
    loc, cost = next
    best_so_far[loc] = cost
    for new in adj(*loc):
        if new in heightmap and heightmap[new] + 1 >= heightmap[loc] and new not in to_check and new not in best_so_far:
            to_check.add((new, cost+1))

print('S -> E:', best_so_far[start])
print('E -> a:', min((best_so_far[e] for e in best_so_far if not(heightmap[e]))))
