import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    lines = f.read().split('\n\n')

primes = [2, 3, 5, 7, 11, 13, 17, 19]
prod_primes = 1
for p in primes:
    prod_primes *= p
print(prod_primes)

class Monkey:
    def __init__(self, str):
        lines = str.split('\n')
        self.id = int(lines[0][6:-1])
        # self.items = []
        # for i in (map(int, lines[1].split(':')[1].split(','))):
        #     d = {}
        #     for p in primes:
        #         d[p] = i%p
        #     self.items.append(d)
        self.items = list(map(int, lines[1].split(':')[1].split(',')))
        
        #parse operation
        self.operation_str = lines[2].split('= ')[1]
        # if '+' in self.operation_str:
        #     self.operation_num = int(self.operation_str.split('+')[1])
        #     self.operation = lambda x: dict((p, (x[p]+self.operation_num)%p) for p in primes)
        self.operation = lambda x: eval(f'{int(x)}'.join(self.operation_str.split('old'))) % prod_primes # //3
        # elif self.operation_str == 'old * old':
        #     self.operation = lambda x: dict((p, (x[p]*x[p])%p) for p in primes)
        # else:
        #     self.operation_num = int(self.operation_str.split('*')[1])
        #     self.operation = lambda x: dict((p, (x[p]*self.operation_num)%p) for p in primes)

        self.test_val = int(lines[3].split(' ')[-1])
        self.test_func = lambda x: int(lines[4].split(' ')[-1]) if not(x%self.test_val) else int(lines[5].split(' ')[-1])
        self.inspected = 0

def printMonkey(m) -> str:
    print((m.id, m.items)) #, m.operation_str, m.operation(2), m.test_val, m.test_func(m.test_val), m.test_func(m.test_val + 1)))

monkies = []
for l in lines:
    monkies.append(Monkey(l))

rounds = 10000
for _ in range(rounds):
    for m in monkies:
        # print(f'Monkey {m.id}:')
        while len(m.items) != 0:
            item_worry = m.items.pop(0)
            new_worry = (m.operation(item_worry))
            monkies[m.test_func(new_worry)].items.append(new_worry)
            m.inspected += 1
    if not(_%100):
        print(_)

print('After round', rounds)
for i in range(len(monkies)):
    print(f"Monkey {i} inspected items {monkies[i].inspected} times.")

# get max 2
monkeys_by_business = sorted(monkies, key=lambda x: x.inspected, reverse=True)
print(monkeys_by_business[0].inspected*monkeys_by_business[1].inspected)

#no longer solves p1


# monkies = []
# for l in lines:
#     monkies.append(Monkey(l))

# # reset
# # do you track each item through? yeah, that could work. any of this could work if i wasn't fucking braindead
# # test item: 79. starts at 0
# paths = {}
# for orig_loc in range(len(monkies)):
#     for orig_item_worry in monkies[orig_loc].items:
#         loc = orig_loc
#         item_worry = orig_item_worry
#         passed_through = []
#         startloc = loc
#         while loc not in passed_through:
#             new_worry = monkies[loc].operation(item_worry)
#             nextloc = monkies[loc].test_func(item_worry)
#             item_worry = new_worry
#             passed_through.append(loc)
#             loc = nextloc
#         passed_through.append(loc)
#         paths[(orig_loc, orig_item_worry)] = passed_through

# def break_path_into_rounds(path):
#     if path == []:
#         return []
#     new = [[path[0]]]
#     for i in range(1, len(path)):
#         if path[i] < path[i-1]:
#             new.append([])
#         new[-1].append(path[i])
#     return new

# # every path loops eventually. break each path into (preloop, loop).
# for k in paths:
#     # there should be one element repeated twice
#     repeated = max(range(len(monkies)), key=lambda x: len(list(filter(lambda y: y==x, paths[k]))))
#     pre_repeat = []
#     while paths[k][0] != repeated:
#         pre_repeat.append(paths[k].pop(0))
#     post_repeat = paths[k][:-1]
#     paths[k] = (break_path_into_rounds(pre_repeat), break_path_into_rounds(post_repeat))

# steps = 20
# monkey_counts = [0]*len(monkies)
# #assumes that it always gets into the loop. might not always be true
# for k in paths:
#     print(k, paths[k])
#     pre_loop, loop = paths[k]
#     currounds = 0
#     q = None
#     while pre_loop != [] and currounds < steps:
#         for q in pre_loop.pop(0):
#             monkey_counts[q] += 1
#         currounds += 1
#     # this isn't properly counting when a preloop 'runs over' into the start of a loop
#     offset = 0
#     if q is not None and q < loop[0][0]:
#         offset = 1
#         for m in loop[0]:
#             monkey_counts[m] += 1

#     full_loops = (steps-currounds)//len(loop)
#     print(full_loops)
#     for r in loop:
#         for m in r:
#             monkey_counts[m] += full_loops
#     currounds += full_loops*len(loop)
#     for r in range(steps-currounds):
#         for m in loop[(r+offset)%len(loop)]:
#             monkey_counts[m] += 1
# print(monkey_counts)