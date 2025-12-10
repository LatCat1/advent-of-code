from loader import load_data
from functools import lru_cache
from datetime import datetime, timedelta
from collections import defaultdict
from itertools import combinations, product
from dataclasses import dataclass
from math import inf
from tqdm import tqdm
from scipy.optimize import milp, LinearConstraint
import numpy as np

data = load_data(10, 2025, testing=False, force_refresh=True).split('\n')


@dataclass(eq=True, frozen=True)
class Machine:
    light_diagram: tuple[str]
    wiring_schematic: tuple[tuple[int]]
    joltage_requirements: tuple[int]

ms = []
for row in data:
    items = row.split(' ')
    d = tuple('#' == i for i in items[0][1:-1])
    jolts = tuple(map(int, items[-1][1:-1].split(',')))
    wires = []
    for w in items[1:-1]:
        x = tuple(map(int, w[1:-1].split(',')))
        wires.append(x)
    ms.append(Machine(d, tuple(wires), jolts))

def min_presses(m: Machine):
    # there is no point in pressing a button twice
    num_lights = len(m.light_diagram)
    # go through all options in order
    for i in range(1, num_lights+1):
        for hits in combinations(m.wiring_schematic, i):
            lights = [False] * num_lights
            for h in hits:
                for l in h:
                    lights[l] = not lights[l]
            if all(a == b for a, b in zip(lights, m.light_diagram)):
                return i

print('P1:', sum(min_presses(m) for m in ms))


def press_button(button: tuple[int], js):
    # create a new machine that represents this one after the button has been pressed
    return tuple(x - (1 if i in button else 0) for i, x in enumerate(js))

# print(press_button(ms[0].wiring_schematic[0], ms[0]))

def min_presses_2(m: Machine):
    num_lights = len(m.joltage_requirements)
    num_buts = len(m.wiring_schematic)
    c = np.array([1]*num_buts) # Optimizing just the sum of button presses
    b = np.array(m.joltage_requirements) # Bounds are the number of times numbers must be pressed
    A = np.array([[
        int(i in b) for b in m.wiring_schematic
    ] for i in range(num_lights)]) # Matrix is button -> lights it activates
    constraint = LinearConstraint(A, b, b) # constrain so that b <= Ax <= b <=> Ax=b
    result = milp(c, constraints=constraint, integrality=1) # integrality = 1 means only integer solutions
    assert result.success # Assert that it succeeded
    return int(result.fun)

t = datetime.now()
s = sum(min_presses_2(m) for m in ms)
print(datetime.now() - t)