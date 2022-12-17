import pathlib
from tqdm import tqdm

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    jets = f.read()

shapes = list("""####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##""".split('\n\n'))

shapes_sets = []
for s in shapes:
    q = set()
    r = 0
    for l in list(s.split('\n'))[::-1]:
        for i in range(len(l)):
            if l[i] == '#':
                q.add((r, i+2))
        r += 1
    shapes_sets.append(q)
# print(shapes_sets)

default_row = [' ']*7
board = set((-1, i) for i in range(7))  # start with a row below everything
def print_board(board, piece=set(), maxs=100000000000, mins=0):
    for _ in range(min(maxs, max(board | piece, key=lambda x:x[0])[0]), mins-1, -1):
        print('|', end='')
        for _2 in range(7):
            if (_, _2) in piece:
                print('@', end='')
            elif (_, _2) in board:
                print('#', end='')
            else:
                print('.', end='')
        print('|')
    print('+-------+')

loop_info = []
def run_steps(maxstep=2022, starttime=0):
    board = set((-1, i) for i in range(7))  # start with a row below everything
    time=starttime
    high_by_step = [0]
    step = 0
    found_loop = False
    while step < maxstep and found_loop is False:
        p = {(r+4+high_by_step[-1], c) for (r,c) in shapes_sets[step%5]}
        farleft = min(p, key=lambda x:x[1])[1]
        farright = max(p, key=lambda x:x[1])[1]
        while True:
            # print_board(board, p)
            d = 1 if jets[time%len(jets)] == '>' else -1
            jet_p = {(r, c+d) for (r,c) in p}
            time += 1
            # make sure it's not inside anything or off
            if jet_p & board == set() and farleft+d>=0 and farright+d<= 6:
                p = jet_p
                farleft += d
                farright += d
            down_p = {(r-1, c) for (r,c) in p}
            if down_p & board == set():
                p = down_p
            else:
                break
        board |= p
        step += 1
        newhigh = max(p, key=lambda x:x[0])[0]
        high_by_step.append(max(newhigh, high_by_step[-1]))
        if step % 5 == 1 and time%len(jets) == 9271:
            r = p.pop()[0]
            if sum((r,i) in board for i in range(7)) == 7:
                hash = 0
                for r2 in range(r+1, r+4):
                    for d2 in range(0, 7):
                        hash = (hash << 1) + (1 if (r2, d2) in board else 0)
                loop_info.append((step, time%len(jets), high_by_step[-1], high_by_step[-1] - r, hash))
                if len(loop_info) == 2:
                    found_loop == True
    # print_board(board, maxs = 100)
    return high_by_step
high_by_step = run_steps(100000)
print('P1: ', high_by_step[2022])

a = loop_info[0]
b = loop_info[1]

first_occur_step = a[0]
second_occur_step = b[0]

dist_between = second_occur_step-first_occur_step
loop_value = high_by_step[second_occur_step] - high_by_step[first_occur_step]

total_steps = 1000000000000
starts_looping_at = total_steps - first_occur_step

num_loops = starts_looping_at//dist_between
extra_steps = starts_looping_at - num_loops*dist_between
print(
    num_loops*loop_value + high_by_step[extra_steps+first_occur_step]
)