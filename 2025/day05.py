from loader import load_data

data = load_data(5, 2025, testing=False)

data = data.split('\n\n')


# [a, b)
ranges = []
for l in data[0].split('\n'):
    a, b = l.split('-')
    ranges.append((int(a), int(b)+1))

ids = []
for l in data[1].split('\n'):
    ids.append(int(l))


print(
    sum(
        any(
            a <= id < b for (a, b) in ranges
        ) for id in ids
    )
)

# now count total safe
ranges = sorted(ranges)
merged = []
i = 1
a, b = ranges[0]
while i < len(ranges):
    # if it overlaps, continue:
    c, d = ranges[i]
    if c <= b:
        b = max(b, d)
    else:
        merged.append((a, b))
        a, b = c, d
    i += 1
merged.append((a, b))
print(sum(b - a for a, b in merged))