import pathlib
from math import ceil
from tqdm import tqdm

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    lines = f.read().split('\n')

blueprints = []
# each blueprint is a dict of whatever
for l in lines:
    q = l.split(' ')
    z = {}
    z['id'] = int(q[1][:-1])
    z['ore'] = {'ore': int(q[6])}
    z['clay'] = {'ore': int(q[12])}
    z['obsidian']  = {'ore': int(q[18]), 'clay': int(q[21])}
    z['geode'] = {'ore': int(q[27]), 'obsidian': int(q[30])}
    z['max_ore'] = max(z['ore']['ore'], z['clay']['ore'], z['obsidian']['ore'], z['geode']['ore'])
    z['max_clay'] = z['obsidian']['clay']
    z['max_obsidian'] = z['geode']['obsidian']
    blueprints.append(z)

def calc_best(ore, ore_bots, clay, clay_bots, obsidian, obsidian_bots,
    time_remaining, blueprint, mem):
    if (ore, ore_bots, clay, clay_bots, obsidian, obsidian_bots, time_remaining) in mem or time_remaining <= 0:
        return mem.get((ore, ore_bots, clay, clay_bots, obsidian, obsidian_bots, time_remaining), 0)

    next_ore = ore+ore_bots
    next_clay = clay+clay_bots
    next_obs = obsidian + obsidian_bots
    best = calc_best(next_ore, ore_bots, next_clay, clay_bots, next_obs, obsidian_bots, time_remaining-1, blueprint, mem)  # just do nothing
    if ore_bots < blueprint['max_ore']:
        # time_ore = ceil((blueprint['ore']['ore']-ore)/ore_bots)+1
        # if time_ore <= time_remaining:  # tries to make an ore bot
        #     best = max(best, calc_best(ore+ore_bots*time_ore-blueprint['ore']['ore'], ore_bots+1,clay+clay_bots*time_ore, clay_bots,
        #         obsidian+obsidian_bots*time_ore, obsidian_bots, time_remaining-time_ore, blueprint, mem))
        if ore >= blueprint['ore']['ore']:
            best = max(best, calc_best(next_ore-blueprint['ore']['ore'], ore_bots+1, next_clay, clay_bots,
                next_obs, obsidian_bots, time_remaining-1, blueprint, mem))

    if clay_bots < blueprint['max_clay']:
        # time_clay = ceil((blueprint['clay']['ore']-ore)/ore_bots)+1
        # if time_clay <= time_remaining:
        #     best = max(best, calc_best(ore+ore_bots*time_clay-blueprint['clay']['ore'], ore_bots,clay+clay_bots*time_clay, clay_bots+1,
        #         obsidian+obsidian_bots*time_clay, obsidian_bots, time_remaining-time_clay, blueprint, mem))
        if ore >= blueprint['clay']['ore']:
            best = max(best, calc_best(next_ore-blueprint['clay']['ore'], ore_bots, next_clay, clay_bots+1,
                next_obs, obsidian_bots, time_remaining-1, blueprint, mem))
    if obsidian_bots < blueprint['max_obsidian'] and clay_bots > 0:
        # time_obsid = max(
        #     ceil((blueprint['obsidian']['ore']-ore)/ore_bots)+1,
        #     ceil((blueprint['obsidian']['clay']-clay)/clay_bots)+1
        # )
        # if time_obsid <= time_remaining:
        #     best = max(best, calc_best(ore+ore_bots*time_obsid-blueprint['obsidian']['ore'], ore_bots,clay+clay_bots*time_obsid-blueprint['obsidian']['clay'], clay_bots,
        #         obsidian+obsidian_bots*time_obsid, obsidian_bots+1, time_remaining-time_obsid, blueprint, mem))
        if ore >= blueprint['obsidian']['ore'] and clay >= blueprint['obsidian']['clay']:
            best = max(best, calc_best(next_ore-blueprint['obsidian']['ore'], ore_bots, next_clay-blueprint['obsidian']['clay'], clay_bots,
                next_obs, obsidian_bots+1, time_remaining-1, blueprint, mem))
    if obsidian_bots > 0:
        # time_geo = max(
        #     ceil((blueprint['geode']['ore']-ore)/ore_bots)+1,
        #     ceil((blueprint['geode']['obsidian']-obsidian)/obsidian_bots)+1
        # )
        # if time_geo <= time_remaining:
        #     best = max(best, calc_best(ore+ore_bots*time_geo-blueprint['geode']['ore'], ore_bots,clay+clay_bots*time_geo, clay_bots,
        #         obsidian+obsidian_bots*time_geo-blueprint['geode']['obsidian'], obsidian_bots, time_remaining-time_geo, blueprint, mem) + (time_remaining-time_geo))
        if ore >= blueprint['geode']['ore'] and obsidian >= blueprint['geode']['obsidian']:
            best = max(best, time_remaining-1+calc_best(next_ore-blueprint['geode']['ore'], ore_bots, next_clay, clay_bots,
                next_obs-blueprint['geode']['obsidian'], obsidian_bots, time_remaining-1, blueprint, mem))
    mem[(ore, ore_bots, clay, clay_bots, obsidian, obsidian_bots, time_remaining)] = best
    return best

m = {}
# print(calc_best(0, 1, 0, 0, 0, 0, 24, blueprints[0], m))
t = 1
for bp in tqdm(blueprints[0:3]):
    # print(bp)
    m = {}
    b = calc_best(0, 1, 0, 0, 0, 0, 32, bp, m)
    # print(len(m))
    # print(bp['id'], b)
    t *= bp['id']*b
print(t)