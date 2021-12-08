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

days = 256
[proceed_day(condensed) for _ in range(days)]

total = sum(condensed)

print(total)