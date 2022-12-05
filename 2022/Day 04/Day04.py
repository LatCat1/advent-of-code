import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    ls = f.read().split('\n')

t = 0
t2 = 0
for l in ls:
    z,y = tuple(l.split(','))
    (a,b) = tuple(z.split('-'))
    (c,d) = tuple(y.split('-'))
    a = int(a)
    b = int(b)
    c = int(c)
    d = int(d)

    if a >= c and b <= d or c>=a and d <= b:
        t += 1

    # a-b, c-d
    if c <= a and a <= d or a <= c and c <= b or c <= b and b <= d or a <= d and d <= a:
        t2 += 1

print(t)
print(t2)