import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day6.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

lanternfish = [int(x) for x in lines[0].split(',')]

spawn_age = 8
recover_time = 6

condensed = [0]*(spawn_age+1)
for i in range(spawn_age):
    condensed[i] = len([1 for x in lanternfish if x == i])

def proceed_day(fish: list):
    extras = fish[0]
    for x in range(spawn_age):
        fish[x] = fish[x+1]
    fish[spawn_age] = extras
    fish[recover_time] += extras

days = 0
# average of max and min weight from http://www.ijichthyol.org/index.php/iji/article/download/4-2-7/188
body_weight_g = 1.230+0.381/2 
mass_earth_g = 5.9722 * 10**24 * 1000
num_search = mass_earth_g/body_weight_g
while sum(condensed) <  num_search:
    proceed_day(condensed)
    days += 1

print(days)