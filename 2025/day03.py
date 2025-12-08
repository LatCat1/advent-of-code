from loader import load_data

data = load_data(3, 2025, testing=False)

type Bank = list[int]

banks: list[Bank] = [
    [int(x) for x in row] for row in data.split('\n')
]

# Determine the max joltage from turning on n batteries in a bank
def max_joltage(bank: Bank, n):
    # each time through, you find the earliest, largest number remaining
    # that is _not_ so late in the bank that it prevents enough batteries
    # from being turned on
    indexes = []
    for m in range(n-1, -1, -1):
        new_index = 0 if not indexes else indexes[-1] + 1
        for i in range(new_index+1, len(bank) - m):
            if bank[i] > bank[new_index]:
                new_index = i
        indexes.append(new_index)

    s = 0
    for i in indexes:
        s = s * 10 + bank[i]

    return s

print(sum(max_joltage(b, 2) for b in banks))
print(sum(max_joltage(b, 12) for b in banks))