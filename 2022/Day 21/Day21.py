import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    lines = f.read().split('\n')

monkeys = {l[0:4]: (z[1] if len(z := l.split(' ')) == 2 else z[1:]) for l in lines}
        
def monkey_funkey(name, all):
    if type(all[name]) != list:
        return all[name]
    return f"({monkey_funkey(all[name][0], all)}){all[name][1]}\
             ({monkey_funkey(all[name][2], all)})"

print('P1:', int(eval(monkey_funkey('root', monkeys))))

monkeys['root'][1], monkeys['humn'] = '-', 'x'
f = monkey_funkey('root', monkeys)
y = lambda x: eval(f.replace('x', str(x)))
intercept = y(0)
slope = (y(10000)-intercept)/10000 
print('P2:', int(-intercept/slope))