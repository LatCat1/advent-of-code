import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as file:
    ls = [line.rstrip() for line in file]

s = lambda c: ord(c) - (ord('A') - 27 if c.isupper() else ord('a') - 1)
print(sum([s((set(l[:len(l)//2]) & set(l[len(l)//2:])).pop()) for l in ls]))
print(sum([s((set(ls[i]) & set(ls[i+1]) & set(ls[i+2])).pop()) 
    for i in range(0, len(ls), 3)]))