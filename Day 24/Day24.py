import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day24.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

# returns a two or three tuple
f = lambda x: int(lines[x].split(' ')[2])
blocks = [(f(b+4), f(b+5), f(b+15)) for b in range(0, len(lines), 18)]

# pair up the inputs and get their relative difference.
pairs, stack = {},[]
for i in range(len(blocks)):
    if blocks[i][0] == 1:
        stack.append((i, blocks[i][2]))
    else:
        pairs[stack.pop(-1)[0]] = (i, stack[-1][1]+blocks[i][1])

for diffunc in [lambda d: (min(9-d, 9), min(9, 9+d)), lambda d: (max(1-d,1), max(1, 1+d))]:
    num = [None]*len(blocks)

    for i in range(len(num)):
        if num[i] is None:
            num[i], num[pairs[i][0]] = diffunc(pairs[i][1])

    print(''.join(map(str, num)))