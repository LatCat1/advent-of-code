with open("Day4.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

order = list(map(int, lines[0].split(',')))

boards = []
for i in range(2, len(lines), 6):
    b = []
    for l in lines[i:i+5]:
        b.append(list(map(int, l.split())))
    boards.append(b)
    
def bingo(board, called_nums):
    for i in range(0, len(board)):
        hoz = True
        vert = True
        for j in range(0, len(board)):
            hoz = hoz and board[i][j] in called_nums
            vert = vert and board[j][i] in called_nums
        if hoz or vert: return True
    return False

# def foldl(base, func, iter):
#     for i in iter:
#         base = func(base, i)
#     return base

i = 0
winners = []
prev_winners = []
while(len(winners) != len(boards)): # to do part 1 just put a 1 instead of len(boards)
    i += 1 
    prev_winners = winners # save whoever had previously won
    winners = list(filter(lambda b: bingo(b, order[0:i]), boards))  # get all the boards that have now won


last_winner = list(filter(lambda x: x not in prev_winners, winners))[0] # the last winner is whatever just now showed up in 'winners'
called = order[0:i]

# sum of all not called
won_list = [x for y in last_winner for x in y] # flatten the winning board down
s = sum(filter(lambda v: v not in called, won_list))  # now get the sum of everything *not* already called

print(s*called[-1])