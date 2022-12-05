import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    lines = f.read().split('\n\n')

def run(lines, dir=True):
    stack_count = int(lines[0].split('\n')[-1].split('  ')[-1])
    stacks = [[] for _ in range(stack_count)]
    for r in lines[0].split('\n')[:-1]:
        for i in range(1, len(r), 4):
            if r[i] != ' ':
                stacks[(i-1)//4] = [r[i]] + stacks[(i-1)//4]

    stacks = [None] + stacks

    for r in lines[1].split('\n'):
        count, f, t = tuple(map(int, r.split(' ')[1::2]))
        stacks[t] += stacks[f][-count:][::dir]
        stacks[f] = stacks[f][:-count]

    print(''.join(map(lambda _: _[-1], stacks[1:])))

run(lines)
run(lines, -1)