with open("Day3.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

gammma_rate = ''
epsilon_rate = ''
for i in range(len(lines[0])):
    zeroes = 0
    for l in lines:
        if l[i] == '0': zeroes += 1
    if zeroes > len(lines)/2:
        gammma_rate += '0'
        epsilon_rate += '1'
    else:
        gammma_rate += '1'
        epsilon_rate += '0'

# gammma_rate = int(gammma_rate, 2)
# epsilon_rate = int(epsilon_rate, 2)
# print(gammma_rate*epsilon_rate)

def most_common_bit(index, l):
    x = [i[index] for i in l]
    x.sort()
    return x[int(len(l)/2)]

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

print(int(oxygen[0],2) * int(co2[0],2))