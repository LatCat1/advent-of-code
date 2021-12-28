import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day9.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

heightmap = {}
for y in range(0, len(lines)):
    for x in range(0, len(lines[y])):
        heightmap[(x,y)] = int(lines[y][x])

ymax = len(lines)
xmax = len(lines[0])

def lowest_point_near(pos):
    (x,y) = pos
    return min(map(lambda x : (heightmap.get(x,9), (x,y)), [(x,y), (x-1,y), (x+1,y), (x,y-1), (x,y+1)]))[1][0]

risk_levels_total = 0
for x in range(xmax):
    for y in range(ymax):
        if lowest_point_near((x,y)) == (x,y):
            risk_levels_total += 1 + heightmap[(x,y)]
print(f"Part 1: {risk_levels_total}")

# maps from a location on the map to the x,y of the basin it is part of
basin_map = {}

# recursively follows the flow of water
def flow_water(pos):
    if pos in basin_map:
        return basin_map[pos]
    if heightmap[pos] != 9:
        flows_to = lowest_point_near(pos)
        if flows_to == pos:
            basin_map[pos] = pos
            return flows_to
        basin_map[pos] = flow_water(flows_to)
        return basin_map[flows_to]
    else:
        basin_map[pos] = -1
        return -1

# starts the flow for every point in the map
for x in range(xmax):
    for y in range(ymax):
        basin_map[(x,y)] = flow_water((x,y))

basin_sizes = {}
for pos in basin_map:
    basin_sizes[basin_map[pos]] = 1+basin_sizes.get(basin_map[pos], 0)
basin_sizes.pop(-1) # get rid of the peaks

sizes = [basin_sizes[k] for k in basin_sizes]
sizes.sort()
print(sizes)
print(sizes[-1]*sizes[-2]*sizes[-3])
