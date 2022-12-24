import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    lines = f.read().split('\n')

elves = {(i,j) for i in range(len(lines)) for j in range(len(lines[i])) 
            if lines[i][j] == '#'}

order = [  # ugly hack to be able to change the order that these are checked
    lambda x, y: [{(x-1,y), (x-1,y-1), (x-1,y+1)}, (x-1,y)],
    lambda x, y: [{(x+1,y), (x+1,y-1), (x+1,y+1)}, (x+1,y)],
    lambda x, y: [{(x,y-1), (x-1,y-1), (x+1,y-1)}, (x,y-1)],
    lambda x, y: [{(x,y+1), (x-1,y+1), (x+1,y+1)}, (x,y+1)],
]

i = 0
moved = True
while moved:
    i += 1
    moved = False
    movements = {}
    for x,y in elves:
        if len({(x+i,y+j) for i in [-1,0,1] for j in [-1,0,1] if i or j}&elves):
            for j in range(4):
                if not len((q := (order[(i+j-1)%4])(x, y))[0]&elves):
                    movements[q[1]] = movements.get(q[1], set()) | {(x,y)}
                    break
    moved = [(elves.add(to), elves.remove(movements[to].pop())) for to in movements 
                if len(movements[to]) == 1]
    if i == 10:
        print('P1:', (max(map(lambda x:x[0], elves))-min(map(lambda x:x[0], elves))+1)
            *(max(map(lambda x:x[1], elves))-min(map(lambda x:x[1], elves))+1)-len(elves))

print('P2:', i)