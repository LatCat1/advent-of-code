from loader import load_data
from collections import defaultdict
import re
from functools import lru_cache, reduce
from datetime import datetime
import heapq as hq
from operator import or_

# data = load_data(17, 2024, testing=True)
data = load_data(17, 2024, testing=False)


pattern = r"^Register A: (?P<A>[0-9]+)\nRegister B: (?P<B>[0-9]+)\nRegister C: (?P<C>[0-9]+)\n\nProgram: (?P<program>[0-7](,[0-7])+)"
match = re.match(pattern, data)

parsed = match.groupdict()


mem = [int(d) for d in parsed['program'].split(',')]

A = 4
B = 5
C = 6
state = [0, 1, 2, 3] + [int(parsed[c]) for c in 'ABC']


def step(instruction, mem, registers, output: list[int]):
    # runs 
    code = mem[instruction]
    operand = mem[instruction+1] if instruction < len(mem) else None
    instruction += 2
    match code:
        case 0: # adv
            registers[A] >>= registers[operand]
        case 1: # bxl
            registers[B] ^= operand
        case 2: # bst
            registers[B] = registers[operand] % 8
        case 3: # jnz
           if registers[A]:
                instruction = operand
        case 4: # bcx
            registers[B] ^= registers[C]
        case 5: # out
            output.append(registers[operand]%8)
        case 6: # bdv
            registers[B] = registers[A] >> registers[operand]
        case 7: # cdv
            registers[C] = registers[A] >> registers[operand]
    return instruction

def show(registers):
    print(f"A: {registers[A]}, B: {registers[B]}, C: {registers[C]}")

def run(state: list[int]):
    output = []
    state = state.copy()
    instruction = 0
    while instruction < len(mem):
        instruction = step(instruction, mem, state, output)
    return output


def simul(n):
    state[A] = n
    return run(state)

print('P1:', ','.join(str(d) for d in run(state)))
a = datetime.now()
nums = []
for n in range(8**4):
    # if the first digit matches
    if simul(n)[:1] == mem[:1]:
        nums.append(n)

for k in range(2, len(mem)):
    n2 = []
    # for each number
    for n in nums:
        for ext in range(8):
            # for each extra digit we can add
            ext <<= 3*(k+2) # by an extra digit?
            if simul(ext+n)[k-1:k] == mem[k-1:k]:
                n2.append(ext+n)
    nums = n2


print('P2:', min( n for n in nums if mem == simul(n)))