import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day19.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

scanners = []
for l in lines:
    if l[0:3] == '---':
        scanners.append([]) 
    elif l == '':
        pass
    else:
        scanners[-1].append(eval(f'({l})'))
for s in range(len(scanners)):
    scanners[s] = (s, scanners[s])

commonneeded = 12
def findcommon(s1, s2):
    scanner1 = scanners[s1]
    scanner2 = scanners[s2]
    #finds two points that have the same 'distance' away from each other
    incommonpoints = []
    for s1 in scanner1[1]:
        for s2 in scanner2[1]:
            #now we look for *12* commonalitis
            common = 0
            for i in scanner1[1]:
                for j in scanner2[1]:
                    if dist(s1,i) == dist(s2,j):
                        common += 1
            if common >= commonneeded:
                incommonpoints.append((s1,s2))
                if len(incommonpoints) == 2:
                    return incommonpoints

def dist(p1,p2):
    x1,y1,z1 = p1
    x2,y2,z2 = p2
    b = [abs(x1-x2), abs(y1-y2), abs(z1-z2)] #this is for rotation
    b.sort() #needs to be here, just casting it to a set fails for some reason
    return b

dists = {}
for s in range(len(scanners)):
    dists[s] = set()
    for p1 in range(len(scanners[s][1])):
        for p2 in range(p1+1, len(scanners[s][1])):
            dists[s].add(tuple(dist(scanners[s][1][p1],scanners[s][1][p2])))

#all the way to reorder the points
orderings = [
    [0,1,2],
    [0,2,1],
    [1,0,2],
    [1,2,0],
    [2,0,1],
    [2,1,0]]
transformations = [] # a list of functions for rotating a point
for o in orderings:
    for x in [-1,1]:
        for y in [-1,1]:
            for z in [-1,1]:
                transformations.append(
                    eval(f"lambda p: (p[{o[0]}]*({x}), p[{o[1]}]*({y}), p[{o[2]}]*({z}))")
                )

paircommons = {}
locations = {0:(0,0,0)}

def add(p1,p2):
    return (p1[0]+p2[0],p1[1]+p2[1],p1[2]+p2[2])

def subtract(p1,p2):
    return (p1[0]-p2[0],p1[1]-p2[1],p1[2]-p2[2])

# s1 is known, all its points are know, *and are saved as their absolute location*
def combine(s1,s2):
    matched = paircommons[(s1,s2)]

    diff1 = subtract(matched[0][0], matched[1][0])
    diff2 = subtract(matched[0][1], matched[1][1])

    for t in transformations:
        if diff1 == t(diff2):
            #ok we found the right transformation function
            for i in range(len(scanners[s2][1])):
                scanners[s2][1][i] = add(matched[0][0], t(subtract(scanners[s2][1][i], matched[0][1])))
            locations[s2] = add(matched[0][0], t(subtract((0,0,0), matched[0][1])))
            return
    
disconnected = set(range(1,len(scanners)))
newfound = [0]
while len(disconnected) != 0:
    temp = []
    for f in newfound: 
        for b in range(len(scanners)): #check every scanner
            if b in disconnected:
                if len(dists[f].intersection(dists[b])) >= 66:
                    paircommons[(f,b)] = paircommons.get((f,b), findcommon(f,b))
                    disconnected = disconnected - set([b])
                    combine(f,b)
                    if f not in temp:
                        temp.append(b)
    newfound = temp

allpoints = set()
for (_,ps) in scanners:
    allpoints = allpoints.union(set(ps))

print(len(allpoints))

def mandistance(a,b):
    x1,y1,z1 = a
    x2,y2,z2 = b
    return abs(x1-x2) + abs(y1-y2) + abs(z1-z2)

print(max([mandistance(x,y) for _,x in locations.items() for _,y in locations.items()]))