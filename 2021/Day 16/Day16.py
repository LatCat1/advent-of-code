import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day16.txt", 'r') as file:
    line = [line.rstrip() for line in file][0]

# convert the line to binary
binary = bin(int(line, 16))[2:]
binary = '0'*((4-len(binary))%4) + binary

int2 = lambda x: int(x, 2)

# returns a (int,int) pair representing the *returned value* and the *length eaten*
def parse(line):
    version = int2(line[0:3]) # used for p1, not p2
    typeid = int2(line[3:6])

    #parse a value
    if typeid == 4:
        value = ''
        index = 6
        loop = True
        while loop:
            value += line[index+1:index+5]
            loop = line[index] != '0'
            index += 5
        return (int(value, 2), index)
        # return (version, index)
    
    # parse the subs
    length_type_id = int2(line[6])
    values = []
    total_travelled = 0
    if length_type_id == 0:
        total_subpackets_length = int2(line[7:22])
        total_travelled=22
        while total_travelled < 22+total_subpackets_length:
            (v,d) = parse(line[total_travelled:])
            values.append(v)
            total_travelled+= d
    else:
        total_travelled=18
        num_subpackets = int2(line[7:18])
        for _ in range(num_subpackets):
            (v,d) = parse(line[total_travelled:])
            values.append(v)
            total_travelled+= d
    returnval = 0
    
    #handle according to typeid
    if typeid == 0: returnval = sum(values)
    elif typeid == 1:
        returnval = 1
        for v in values: returnval *= v
    elif typeid == 2:returnval = min(values)
    elif typeid == 3:returnval = max(values)
    #already did 4
    elif typeid == 5:returnval = 1 if values[0]>values[1] else 0
    elif typeid == 6:returnval = 1 if values[1]>values[0] else 0
    elif typeid == 7:returnval = 1 if values[0]==values[1] else 0

    return (returnval, total_travelled)
    
print(parse(binary))
