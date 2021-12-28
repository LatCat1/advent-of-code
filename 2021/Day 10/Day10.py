import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day10.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

syntax_error_points = {None: 0, ')':3, ']':57, '}': 1197, '>': 25137}
match = {'(':')', '[':']', '{':'}', '<':'>'}
completion_points = {')':1, ']':2, '}':3, '>':4}

# returns a tuple defining the score; second is always the score, (0,x) is syntax error and (1,x) is incomplete error
def score_line(line, score_incomplete = True):
    next_close_needed = []
    for c in line:
        if c not in syntax_error_points:
            # starting a chunk
            next_close_needed.append(match[c])
        else:
            #ending a chunk
            if c != next_close_needed[-1]:
                #found the wrong closing bracket
                return (0, syntax_error_points[c])
            #found the correct closing bracket
            next_close_needed.pop(-1)
    # line is incomplete
    score = 0
    for c in next_close_needed[::-1]:
        score = score * 5 + completion_points[c]
    return (1,score)

scores = [score_line(l) for l in lines]

# could be faster than going through everthing twice, idgaf
p1_score = sum([s[1] for s in scores if s[0] == 0])
p2_score = [s[1] for s in scores if s[0] == 1]
p2_score.sort()
p2_score = p2_score[len(p2_score)//2]

print(f"Part 1: {p1_score}\nPart 2: {p2_score}")