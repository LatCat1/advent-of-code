from loader import load_data
from functools import lru_cache, reduce

data = load_data(day=4, year=2023, testing=False)
data = data.split('\n')

def score_copy(r):
    wins = r.split('|')[0].split(':')[1].strip().split(' ')
    mine = r.split('|')[1].split(' ')

    i_wins = set(int(w) for w in wins if w != '')
    i_mine = set(int(n) for n in mine if n != '')

    return len(i_wins & i_mine)

def val(n):
    return int(2 ** (n-1) * min(1, n))

s = sum(val(score_copy(r)) for r in data)
print(s)

copies = [1] * len(data)
for i in range(len(data)):
    h_wins = score_copy(data[i])
    # ok because you never win more than 2^4 = 16 boards at a time
    for j in range(i+1, min(i+h_wins+1, len(data))):
        copies[j] += copies[i]
s = sum(copies[i] for i in range(len(data)))
print(s)