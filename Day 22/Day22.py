import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day22.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

# returns a (bool, [(int,int), (int,int), (int,int)])
def parse_step(line):
    on = line[0:2] == 'on'
    q = line.split(' ', 1)[1].split(',')
    z = []
    for i in range(3):
        a = q[i].split('..')
        z.append((int(a[0][2:]), int(a[1])))
    s = (on, tuple(z))
    return s
lines = [parse_step(l) for l in lines]

#returns the bounds for the region where two cubes intersect (if they do)
def intersect(c1, c2):
    sect = []
    for i in range(3):
        r = (max(c1[i][0], c2[i][0]), min(c1[i][1], c2[i][1]))
        if r[0] > r[1]: #check if its out of bounds
            return None
        sect.append(r)
    return sect

def legalrect(r):
    return r[0][0] <= r[0][1] and r[1][0] <= r[1][1] and r[2][0] <= r[2][1]

# returns (c1-c2)
def overlap(c1, c2): #this is called 1.7 million times; it's basically the whole runtime
    # first, check if the cubes intersect
    inter = intersect(c1,c2)
    if inter: return ([c1], [])
    # now we can just treat c2 as its intersection with c1
    # print('there is an intersection')
    # there are three possible regions: x1,y1; y1,y2; y2, x2 (the +-1 is because of inclusiveness). generate this for each of them
    regions = []
    for i in range(3): regions.append([(c1[i][0], inter[i][0]-1), inter[i], (c2[i][1]+1, c1[i][1])])

    cubes = []
    for x in range(3):
        for y in range(3):
            for z in range(3):
                # print('checking', (regions[0][x], regions[1][y], regions[2][z]))
                if (x != 1 or y != 1 or z!= 1) and legalrect((regions[0][x], regions[1][y], regions[2][z])):
                    # print('good')
                    cubes.append((regions[0][x], regions[1][y], regions[2][z]))


    return cubes, inter

def volume(r):
    return (1+r[0][1]-r[0][0])*(1+r[1][1]-r[1][0])*(1+r[2][1]-r[2][0])

def filtersize(l):
    for i in range(3):
        for j in range(2):
            if abs(l[1][i][j]) > 50:
                return False
    return True

check = lines
#check = list(filter(filtersize, lines))

def solve(lines):
    ons = []
    for l in lines:
        new = []
        for o in ons:
            new.extend(overlap(o, l[1])[0])
        ons = new
        if l[0]: ons.append(l[1])
    return(sum(map(volume, ons)))

print(solve(check))