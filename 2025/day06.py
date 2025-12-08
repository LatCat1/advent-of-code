from loader import load_data

data = load_data(6, 2025, testing=True)

data = [d for d in data.split('\n') if d]
problems = []

for d in data[:-1]:
    l = []
    for q in d.split():
        # print(q)
        if q:
            l.append(int(q))
    problems.append(l)

s = 0
for i, o in enumerate(data[-1].split()):
    if o == '+':
        s += sum(l[i] for l in problems)
    if o == '*':
        z = 1
        for l in problems:
            z *= l[i]
        s += z
print(s)

# pivot it
h = []
for i in range(len(data[0])):
    h.append(
        ''.join(data[a][i] if i < len(data[a]) else '' for a in range(len(data)))
    )
q = ' '.join(h)
q = q.split()

# sometimes there was whitespace directly before '*' or '+'; remove it
qq = []
for z in q:
    if z == '*' or z == '+':
        qq[-1] += z
    else:
        qq.append(z)
q = qq


# simple reduciton
def f(op, ns):
    if op == '+':
        return sum(ns)
    z = 1
    for n in ns:
        z *= n
    return z

s = 0 # sum
c = [] # current stack
op = '+' # current op
for h in q:
    if ('+' in h) or ('*' in h): # this detects starting a new computation so clear buffer
        s += f(op, c)
        c = []
        op = h[-1]
        h = h[:-1]
    c.append(int(h)) # add to stack
s += f(op, c) # trailing operation
print(s)
