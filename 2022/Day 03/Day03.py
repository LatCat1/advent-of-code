import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    ls = f.read().split('\n')

s = lambda c: ord(c)-(38 if c.isupper() else 96)
print(sum([s((set(l[:len(l)//2]) & set(l[len(l)//2:])).pop()) for l in ls]))
print(sum([s((set(a) & set(b) & set(c)).pop()) for (a,b,c) in zip(*[iter(ls)]*3)]))