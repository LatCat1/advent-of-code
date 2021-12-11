with open("Day 1/Day1.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

depth = [int(depth) for depth in lines]

def num_increasing(window_size):
    count = 0
    for i in range(0, len(depth)-window_size):
        if depth[i] < depth[i+window_size]:
            count += 1
    return count

print(f"Window size 1: {num_increasing(1)}\nWindow size 3: {num_increasing(3)}")