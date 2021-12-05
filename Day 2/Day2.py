with open("Day2.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

commands = [line.split(' ') for line in lines]
commands = [(c[0], int(c[1])) for c in commands]

hoz = 0
depth = 0

# for (dir, dist) in commands:
#     if dir == 'forward': hoz += dist
#     elif dir == 'down': depth += dist
#     elif dir == 'up': depth -= dist

aim = 0
for (dir, dist) in commands:
    if dir == 'down': aim += dist
    elif dir == 'up': aim -= dist
    elif dir == 'forward':
        hoz += dist
        depth += aim*dist

print(hoz * depth)