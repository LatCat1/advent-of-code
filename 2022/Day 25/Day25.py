import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    lines = f.read().split('\n')
    
def snafu(x):
    d = {
        '0': 0,
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '-': -1,
        '=': -2
    }
    t = 0
    for c in x:
        t = t*5 + d[c]
    return t

def un_snafu(i):
    q = ''
    while i != 0:
        r = i%5
        if r == 0:
            q = '0' + q
        elif r == 1:
            q = '1' + q
        elif r == 2:
            q = '2' + q
        elif r == 3:
            q = '=' + q
            i += 2
        elif r == 4:
            q = '-' + q
            i += 1
        i = i//5
    return q

print('P1:', un_snafu(sum(map(snafu, lines))))