import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day5.txt", 'r') as file:
    lines = [line.rstrip() for line in file]


# segment = ((a,b), (c,d))
def interpret_segment(line):
    line = line.split('->')
    start = line[0].split(',')
    end = line[1].split(',')

    start = (int(start[0]), int(start[1]))
    end = (int(end[0]), int(end[1]))

    return (start, end)

# sees if a segment goes directly horizontally or vertically
def is_hoz_or_vert(segment):
    ((a,b), (c,d)) = segment
    return a == c or b == d

def draw_segment(board, segment):
    ((a,b), (c,d)) = segment
    (x,y) = (a,b)
    d_x = int((c-a)/max(abs(c-a), 1))
    d_y = int((d-b)/max(abs(d-b), 1))

    while (x,y) != (c,d):
        board[x][y] += 1
        x += d_x
        y += d_y

    board[c][d] += 1

    return board

# the commented-out version is for part 1
segments = list(filter(lambda s: is_hoz_or_vert(s), [interpret_segment(l) for l in lines]))
# segments = [interpret_segment(l) for l in lines]

# get the largest coordinate in a segment; the grid doesn't need to be any larger
n = max(map(lambda x: max(x[0][0], x[0][1], x[1][0], x[1][1]), segments)) + 1

# create the grid, and draw each line segment on it
grid = [[0 for _ in range(n)] for _ in range(n)]
[draw_segment(grid, s) for s in segments]

# count the number of places there are more than one intersection
count = len([v for row in grid for v in row if v >= 2])

print(count)