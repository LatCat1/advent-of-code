"""
the location is always the median for p1, and the mean for p2
"""

import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day7.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

hoz_positions = [int(l) for l in lines[0].split(',')]

def fuel_cost(positions, final, dist):
    return sum([dist(abs(x-final)) for x in positions])

def dist_triangle(n):
    return int(n*(n+1)/2)

hoz_positions.sort()

# for part 1 use no distance function, for part 2 use the dist_triangle
optimal_p1_location = hoz_positions[len(hoz_positions)//2]
positions_cost_p1 = fuel_cost(hoz_positions, optimal_p1_location, lambda x:x)

optimal_p2_location = sum(hoz_positions)//len(hoz_positions)
positions_cost_p2 = fuel_cost(hoz_positions, optimal_p2_location, dist_triangle)

print(f"Part 1: {positions_cost_p1}\nPart 2: {positions_cost_p2}")