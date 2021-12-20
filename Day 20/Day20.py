import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day20.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

image_enhancement = list(map(lambda y: int(y=='#'), list(lines[0])))
lines = lines[2:]

image = {}
for y in range(len(lines)):
    for x in range(len(lines[y])):
        image[(x,y)] = 1 if lines[y][x] == '#' else 0

def recalcpixel(pos,grid, unknown):
    x,y = pos
    num = 0
    for y1 in range(y-1,y+2):
        for x1 in range(x-1,x+2):
            num = num*2+grid.get((x1,y1), unknown)
    
    return image_enhancement[num]

def recalcimage(image, unknown):
    newim = {}
    keys = [k for k in image]
    xs = list(map(lambda a:a[0], keys))
    ys = list(map(lambda a:a[1], keys))

    for x in range(min(xs)-1, max(xs)+2):
        for y in range(min(ys)-1, max(ys)+2):
            newim[(x,y)] = recalcpixel((x,y),image, unknown)
    return newim

# z = recalcimage(image)

def printm(z):
    for y in range(-6,10):
        for x in range(-6,10):
            print('#' if z.get((x,y), 0) else '.', end='')
        print()

for i in range(50):
    image = recalcimage(image, i%2)
z = image
print(sum([z[k] for k in z]))