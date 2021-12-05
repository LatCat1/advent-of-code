with open("Day1.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

depth = [int(depth) for depth in lines]

count = 0
for i in range(0, len(depth)-3):
    if sum(depth[i:i+3]) < sum(depth[(i+1):(i+4)]):
        count += 1

print(count)