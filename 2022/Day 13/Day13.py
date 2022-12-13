import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    lines = f.read().split('\n\n')

pairs = [list(map(eval, l.split('\n'))) for l in lines]

# -1 if a<b; 0 if a==b; 1 if a<b
def compare(a, b, inda=0, indb=0):
    if len(a) == inda and len(b) == indb:
        return 0
    if len(a) == inda:
        return -1
    if len(b) == indb:
        return 1
    i = a[inda]
    j = b[indb]

    if type(i) == int and type(j) == int: # if both are integers, lower comes first; else compare the rest
        if i == j:
            return compare(a, b, inda+1, indb+1)
        return -1 if i < j else 1
    if type(i) == int: #if one is an integer, then cast it to a list so it can be compared against a list
        i = [i]
    if type(j) == int:
        j = [j]
    z = compare(i, j)
    if z == 0: #tied, move onto later
        return compare(a, b, inda + 1, indb+1)
    return z

print(sum(i+1 for i,p in enumerate(pairs) if compare(*p)==-1))

dividers = [[[2]],[[6]]]
counts = [1,2]
for p in sum(pairs, start=[]):
    for i in range(len(counts)):
        if compare(p,dividers[i]) == -1:
            counts[i] += 1
print(counts[0]*counts[1])
