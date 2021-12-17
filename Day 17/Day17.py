# import pathlib

# with open(f"{pathlib.Path(__file__).parent.resolve()}/Day17.txt", 'r') as file:
#     line = [line.rstrip() for line in file][0]

# b = line.split(' ')
xmin = 155
xmax = 215
ymin = -132
ymax = -72

#test input, this works
# xmin = 20
# xmax = 30
# ymin = -10
# ymax = -5

probes = [(x,y) for x in range(0,xmax+1) for y in range(ymin,1000)]

def probsuccess(probe):
    dx,dy = probe
    x,y = 0,0
    maxy = -99999
    while x <= xmax and y >= ymin:
        x += dx
        y += dy
        dy -= 1
        dx = max([dx-1,0])
        if y > maxy:
            maxy = y
        if xmin <= x and x <= xmax and ymin <= y and y <= ymax:
            return 1
    return False

print(sum(map(probsuccess, probes)))