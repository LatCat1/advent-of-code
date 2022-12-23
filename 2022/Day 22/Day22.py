import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    lines = f.read().split('\n\n')

q = lines[0].split('\n')
width = max(map(len, q))
height = len(q)
start = None
grid = {}
for i in range(len(q)):
    for j in range(len(q[i])):
        if q[i][j] != ' ':
            grid[(i,j)] = q[i][j]
    # for j in range(len(q[i]), width):
    #     grid[(i,j)] = ' '
ci = 0
cj = 0
while q[ci][cj] != '.':
    cj += 1

side_len = print(width//3)
meta = [0]
def in_front(x, y, dx, dy, grid, width, height):
    cx, cy = (x+dx)%height, (y+dy)%width
    if (cx, cy) not in grid:
        if (dx, dy) == (-1, 0):  # going up
            if x == 0 and 50<=y<100:  # 1 up is the left side of 6
                a, b, c, d = y-50+150, 0, 0, 1
            elif x == 0 and 100<=y<150:  # 2 up is the bottom of 6
                a, b, c, d = 199, y-100, -1, 0
            elif x == 100 and 0<=y<50:  # 5 up is the left of 3
                a, b, c, d = y+50, 50, 0, 1
            else:
                # print(x, y, dx, dy)
                print('oh no')
        if (dx, dy) == (1,0):
            if x == 49 and 100<=y<150:  # 2 down is right 3
                a, b, c, d = y-100+50, 99, 0, -1
            elif x == 149 and 50<=y<100: # 4 down is right 6
                a, b, c, d = y-50+150, 49, 0, -1
            elif x == 199 and 0<=y<50:  # 6 down is top 2
                a, b, c, d = 0, y+100, 1, 0
            else:
                print('oh no 2')
        if (dx, dy) == (0, -1):
            if y == 50 and 0<=x<50:  # 1 left to 5 left
                a, b, c, d = 149-x, 0, 0, 1
            elif y == 50 and 50<=x<100:  # 3 to top 5
                a, b, c, d = 100, x-50, 1, 0
            elif y == 0 and 100<=x<150:  # 5 left to 1 left
                a, b, c, d = 149-x, 50, 0, 1
            elif y == 0 and 150<=x<200: # 6 left to top 1
                a, b, c, d = 0, x-150+50, 1, 0
            else:
                print('oh no 3')
        if (dx, dy) == (0, 1):
            if y == 149 and 0<=x<50: # 2 right is 4 right
                a, b, c, d = 149-x, 99, 0, -1
            elif y == 99 and 50<=x<100:  # 3 right is 2 bottom
                a, b, c, d = 49, x-50+100, -1, 0
            elif y == 99 and 100<=x<150:  # 4 right is 2 right
                a, b, c, d = 49-(x-100), 149, 0, -1
            elif y == 49 and 150<=x<200:  # 6 right is 4 bottom
                a, b, c, d = 149, x-150+50, -1, 0
            else:
                print('oh no 4')
        # print(x, y, dx, dy, 'to', a, b, c, d)
        # input()
        meta[0] += 1
        return a, b, c, d
    return cx, cy, dx, dy

def fscore(di, dj):
    f_score = 0
    if (di,dj) == (1,0):
        f_score = 1
    elif (di,dj) == (0,-1):
        f_score = 2
    elif (di,dj) == (-1, 0):
        f_score = 3
    return f_score


# print(in_front(30, 149, 0, 1, grid, width, height))
# print(in_front(119, 99, 0, 1, grid, width, height))
# exit()
di,dj = 0, 1
ind = 0
record = []
while ind<len(lines[1]):
    q = False
    if lines[1][ind] == 'L':
        di, dj = -dj, di
        record.append('L')
    elif lines[1][ind] == 'R':
        di, dj = dj, -di
        record.append('R')
    else:
        passed_through = {}
        cn = ''
        while ind<len(lines[1]) and lines[1][ind] not in ['L', 'R']:
            cn += lines[1][ind]
            ind += 1
        ind -= 1
        cd = cn
        cn = int(cn)
        # take cn steps
        z = in_front(ci, cj, di, dj, grid, width, height)
        if z is None:
            print(ci, cj, di, dj)
        ni, nj, ndi, ndj = z
        while cn > 0 and grid[(ni, nj)] != '#':
            passed_through[(ci, cj)] = (di, dj)
            cn -= 1
            ci, cj = ni, nj
            if (di, dj) != (ndi, ndj):
                q = True
            di, dj = ndi, ndj
            ni, nj, ndi, ndj = in_front(ci, cj, di, dj, grid, width, height)
            if (ci, cj, -di, -dj) != in_front(ni, nj, -ndi, -ndj, grid, width, height):
                print(ci, cj, di, dj)
            # print(ci, cj, di, dj)
        record.append((int(cd)-ci, (ci, cj)))
        if (ci, cj) not in grid:
            print(record)
            exit()
    if q is True and False:
        p = ""
        for i in range(200):
            for j in range(150):
                if (i,j) == (ci, cj):
                    p += '?'
                elif (i,j) in passed_through:
                    p += str(fscore(*passed_through[(i, j)]))
                else:
                    p += grid.get((i,j), ' ')
            print(p)
            p = ""
        print(passed_through)
        print(di, dj)
        print(lines[1][ind], cd)
        input()
    ind += 1

print(1000*(1+ci) + 4*(1+cj) + fscore(di, dj))