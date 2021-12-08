import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day8.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

# (set(inputs), list(outputs))
def parse(line):
    s = line.split(' | ')
    inputs = [set(x) for x in s[0].split(' ')]
    outputs = s[1].split(' ')
    return (inputs, outputs)

count = 0
for line in lines:
    for val in parse(line)[1]:
        if len(val) in [2, 4, 3, 7]:
            count += 1
print(f"Part 1: {count}")

# inputs should be a list of sets of characters
def determine_map(inputs):
    # maps from the length of the input to a 
    num_to_input = {}
    determined_map = {} # maps a known value to a set of just that value

    #get the values with known lengths
    known_lengths = {2: 1, 4: 4, 3: 7, 7: 8}
    for x in inputs:
        if len(x) in known_lengths:
            num_to_input[known_lengths[len(x)]] = x

    # now using the difference between the one and the seven, the top of the display is known
    determined_map['a'] = num_to_input[7] - num_to_input[1]

    # 8 - 4 - 7 gives {e,g}. now, consider the inputs of length 6. only one lacks e, c
    eg: set = num_to_input[8] - num_to_input[4] - num_to_input[7]
    for x in inputs:
        if len(x) == 6:
            if len(x - eg) == len(x)-1:
                determined_map['e'] = eg - x
            if len(num_to_input[1] - x) == 1:
                determined_map['c'] = num_to_input[1] - x
    determined_map['g'] = eg-determined_map['e']

    # 3 - 7 - {g} = {d}
    for x in inputs:
        if len(x) == 5:
            if len(x-num_to_input[7]-determined_map['g']) == 1: # this uses g, so it can't be found before g
                num_to_input[3] = x

    # get the rest from diffrences
    determined_map['d'] = num_to_input[3] - num_to_input[7] - determined_map['g']
    determined_map['b'] = num_to_input[4] - num_to_input[3]
    determined_map['f'] = num_to_input[1] - determined_map['c']

    # now reverse the determined map, to go from unknown->known (and move awya from sets)
    flipped = {list(v)[0]:k for k,v in determined_map.items()}

    return flipped


def interpret(m, num: str) -> str:
    converted = [m[i] for i in num]
    converted.sort()
    converted = ''.join(converted)

    digit_segment_number = \
        {'abcefg': '0', 'cf':'1', 'acdeg':'2', 'acdfg':'3', 'bcdf':'4', 'abdfg':'5', 'abdefg':'6', 'acf':'7', 'abcdefg':'8', 'abcdfg':'9'}

    return digit_segment_number[converted]
    

def get_val(inputs, outputs):
    m = determine_map(inputs)
    return int(''.join(map(lambda x: interpret(m, x), outputs)))

print(f"Part 2: {sum(map(lambda x: get_val(*parse(x)), lines))}")