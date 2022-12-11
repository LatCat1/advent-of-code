import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    lines = f.read().split('\n')

in_progress = sum([[0] + ((l!='noop')*[int((l+' 0').split(' ')[1])]) for l in lines],start=[1])
x = [sum(in_progress[0:i+1]) for i in range(240)] #repeats a lot of work :/

print(sum(x[c-1]*c for c in range(20, 240, 40)))
print(''.join(' #'[abs(x[p]-p%40) <= 1] + '\n'*(not((p+1)%40)) for p in range(240)))