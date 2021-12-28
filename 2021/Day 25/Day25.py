import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day25.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

blockedE = set()
blockedS = set()
movE = set()
movS = set()
height = len(lines)
width = len(lines[0])

for y in range(height):
    for x in range(width):
        if lines[y][x] == '>':
            if lines[y][(x+1)%width] == '.':
                movE.add((x,y))
            else:
                blockedE.add((x,y))
        elif lines[y][x] == 'v':
            if lines[(y+1)%height][x] == '.':
                movS.add((x,y))
            else:
                blockedS.add((x,y))
print(movE)
print(blockedE)
print(movS)
print(blockedS)
print()
print(sum([len(movE), len(movS), len(blockedS), len(blockedE)]))
steps = 0
while len(movE) or len(movS): #while both lengths are nonzero
    newMovE = set()
    for (x,y) in movE: #it can definitely move
        blockloc = ((x+2)%width,y) #the location where something blocking this guy would go
        if blockloc in blockedE or blockloc in blockedS: #if there's something that isn't moving there
            blockedE.add(((x+1)%width, y)) #add it to the blocked
        else: 
            newMovE.add(((x+1)%width, y))
        #now, free up anything it may be blocking & block anything it may have gotten in front of
        above = (x,(y-1)%height)
        if above in blockedS:  #if the point above where it started was blocked, then set it to move
            movS.add(above)
            blockedS.remove(above)
        else: #if nothing above was trying to move, check to the left
            left = ((x-1)%width, y)
            if left in blockedE:
                newMovE.add(left)
                blockedE.remove(left)
        #is it blocking anything from moving down in its new position?
        aboveright = ((x+1)%width, (y-1)%height)
        if aboveright in movS:
            blockedS.add(aboveright)
            movS.remove(aboveright)
    movE = newMovE
    newMovS = set()
    for (x,y) in movS: #it can definitely move
        blockloc = (x,(y+2)%height) #the location where something blocking this guy would be
        if blockloc in blockedE or blockloc in blockedS: #if there's something that isn't moving there
            blockedS.add((x, (y+1)%height)) #add it to the blocked
        else: 
            newMovS.add((x, (y+1)%height))
        #now, free up anything it may be blocking & block anything it may have gotten in front of
        left = ((x-1)%height,y)
        if left in blockedE:  #if the point left is blocked
            movE.add(left)
            blockedE.remove(left)
        else: #if nothing above was trying to move, check above
            above = (x,(y-1)%height)
            if above in blockedS:
                newMovS.add(above)
                blockedS.remove(above)
        #is it blocking anything from moving right in its new position?
        downleft = ((x-1)%width, (y+1)%height)
        if downleft in movE:
            blockedE.add(downleft)
            movE.remove(downleft)
    movS = newMovS
    steps += 1
    if steps > 2:
        print(len(movE), len(movS), len(blockedS), len(blockedE))
        exit()

print(steps)