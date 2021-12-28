with open("Day 3/Day3.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

def most_common_bit(index, l):
    x = [i[index] for i in l]
    x.sort()
    return x[int(len(l)/2)]

# gamma is the most common bit, and epsilon is the least common
# epsilon is found by taking the opposite of the most common bit, so its a bit more work
gammma_rate = int(''.join([most_common_bit(i, lines) for i in range(0, len(lines[0]))]), 2)
epsilon_rate = int(''.join(['1' if most_common_bit(i, lines) == '0' else '0' for i in range(0, len(lines[0]))]), 2)

print(f'Power Consumption: {epsilon_rate*gammma_rate}')

oxygen = lines
co2 = lines

i = 0
while len(oxygen) != 1:
    bit = most_common_bit(i, oxygen)
    oxygen = list(filter(lambda x: x[i] == bit, oxygen))
    i+=1

i = 0
while len(co2) != 1:
    bit = most_common_bit(i, co2)
    co2 = list(filter(lambda x: x[i] != bit, co2))
    i+=1

print(f'Life Support Rating: {int(oxygen[0],2) * int(co2[0],2)}')