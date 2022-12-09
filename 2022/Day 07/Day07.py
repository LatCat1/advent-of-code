import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    lines = f.read().split('\n')


tree = {}
loc = tree
back = []
i = 0
while i < len(lines):
    l = lines[i].split(' ')
    if l[0] == '$':
        if l[1] == 'cd':
            if l[2] == '..':
                loc = back[-1]
                back = back[0:-1]
            elif l[2] == '/':
                loc = tree
                back = []
            # command
            else:
                back.append(loc)
                loc = loc[l[2]]
        elif l[1] == 'ls':
            i += 1
            while i < len(lines) and lines[i][0] != '$':
                q = lines[i].split(' ')
                if q[0] == 'dir':
                    loc[q[1]] = {}
                else:
                    loc[q[1]] = int(q[0])
                i += 1
            i -= 1
    i += 1

def size(dir):
    if type(dir) == dict:
        return sum(size(dir[q]) for q in dir)
    else:
        return dir

def s2(dir):
    if type(dir) == dict:
        z = size(dir)
        if z > 100000:
            z = 0
        for _ in dir:
            z += s2(dir[_])
        return z
    else:
        return 0

# print(tree)
# print(s2(tree))

total_space_taken = size(tree)
free = 70000000 - total_space_taken
print('unused', free)
need_to_free = 30000000 - free
print('need to free', need_to_free)
best_so_far = size(tree)

sizes = []
def s3(dir):
    if type(dir) == dict:
        z = sum(s3(dir[q]) for q in dir)
        sizes.append(z)
        return z
    else:
        return dir
s3(tree)

z = sorted(sizes)
print(z)
for _ in z:
    if _ >= need_to_free:
        print(_)
        break
# print(need_to_free)