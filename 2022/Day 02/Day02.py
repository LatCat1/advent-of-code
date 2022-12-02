import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day02.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

rounds = [l.split(' ') for l in lines]

loop = 'rps'
c1 = {
    'A': 'r',
    'B': 'p',
    'C': 's'
}

c2 = {
    'X': 'r',
    'Y': 'p',
    'Z': 's'
}

beats = {
    'r': 's',
    'p': 'r',
    's': 'p'
}

loses = {
    's': 'r',
    'r': 'p',
    'p': 's'
}

m = {
    'r': 1,
    'p': 2,
    's': 3
}

score = 0
for (a, b) in rounds:
    a = c1[a]
    play = None
    if b == 'Y': #draw
        play = a
        score += 3
    elif b == 'X': # lose
        play = beats[a]
    else:
        play = loses[a]
        score += 6
    score += m[play]


print(score)