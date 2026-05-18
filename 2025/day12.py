from loader import load_data
from functools import lru_cache
from datetime import datetime, timedelta
from collections import defaultdict
from itertools import combinations, product, permutations
from dataclasses import dataclass
from math import inf
from tqdm import tqdm
from scipy.optimize import milp, LinearConstraint
import numpy as np

data = load_data(12, 2025, testing=False).strip().split('\n\n')

shape_sizes = []
for d in data[:-1]:
    shape_sizes.append(d.count('#'))

regions = []
for d in data[-1].split('\n'):
    a, b = d.split(':')[0].split('x')
    r = list(map(int, (d.split(':')[1].strip().split(' '))))
    regions.append((int(a), int(b), r))

# if they aren't immediately too big we are good
print(
    sum(
        sum(n*shape_sizes[i] for i, n in enumerate(r[2])) <= r[0]*r[1]
        for r in regions
    )
)