import pathlib

with open(f"{pathlib.Path(__file__).parent.resolve()}/Day23.txt", 'r') as file:
    lines = [line.rstrip() for line in file]

# part 1 dynamic, p2 ugly
rooms = [
    [lines[3][3], 'D', 'D', lines[2][3]],
    [lines[3][5], 'B', 'C', lines[2][5]],
    [lines[3][7], 'A', 'B', lines[2][7]],
    [lines[3][9], 'C', 'A', lines[2][9]]
]
start_hallway = [None if i == '.' else i for i in lines[1][1:12]]

rooms = [[r for r in rooms[i] if r != '.'] for i in range(len(rooms))]

#bunch of constants to make life easier
let_to_room = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
room_to_let = ['A', 'B', 'C', 'D']
room_to_hallway_connect = {0:2, 1: 4, 2: 6, 3: 8}  #2+2*n
let_to_cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
legal_hallway_spots = [0,1,3,5,7,9,10]

class State:

    #each room works like a stack; the item at end is the only one that should be accessed (unless checking for something)
    ROOM_SIZE = 4

    def __init__(self, rooms, hallway):
        self.rooms = rooms
        self.hallway = hallway

    def __str__(self):
        return str(self.rooms) +' ' +  str(self.hallway)

    def get_possible_moves(self):
        #returns a list of all possible later states.
        moves = []
        #first, let's see if there are any moves among the hallway ones. these *cannot move past something else* and
        # *must go to their final location*
        for i in range(11): #fixed hallway length
            if self.hallway[i]: # check if its not none
                r = let_to_room[self.hallway[i]]
                loc = room_to_hallway_connect[r]
                # print(self.hallway[i+1:loc+1] + self.hallway[loc:i] != [None]*(abs(loc-i)))
                #combine the two directions bc it could be travelling either direction, and make sure it's empty
                if self.hallway[i+1:loc+1] + self.hallway[loc:i] == [None]*(abs(loc-i)) \
                    and sum([x == self.hallway[i] for x in self.rooms[r]]) == len(self.rooms[r]): #every item in the room is of the same type
                    new_hallway = self.hallway[:i] + [None] + self.hallway[i+1:] #replace the ith with a None
                    new_rooms = [q.copy() for q in self.rooms]
                    new_rooms[r].append(self.hallway[i])
                    cost_increase = (abs(loc-i)+(self.ROOM_SIZE - len(self.rooms[r])))*let_to_cost[self.hallway[i]]
                    moves.append((cost_increase, State(new_rooms, new_hallway)))

        #now get all of the moves for items at the ends of rooms (only move if their room *is bad*)
        for r in range(4):
            # if the room is nonempty AND any item doesn't fit (otherwise there's no reason to move)
            if len(self.rooms[r]) > 0 and sum([x == room_to_let[r] for x in self.rooms[r]]) != len(self.rooms[r]):
                # find what hallway spots you can go to
                loc = room_to_hallway_connect[r] #get the location we pop out on
                for i in legal_hallway_spots: #for each possible hallway location to move to
                    if self.hallway[i] is None:
                        #same conditional as before to make sure the path is clear
                        if self.hallway[i:loc] + self.hallway[loc+1:i+1] == [None]*(abs(loc-i)):
                            new_rooms = [q.copy() for q in self.rooms]
                            new_hallway = self.hallway[:i] + [self.rooms[r][-1]] + self.hallway[i+1:]
                            cost_increase = (abs(loc-i)+(self.ROOM_SIZE - len(self.rooms[r])+1))*let_to_cost[new_rooms[r].pop(-1)]
                            moves.append((cost_increase, State(new_rooms, new_hallway)))
        return moves

    # turns it into a tuplized version of itself to be used for checking against memory
    def to_key(self):
        rs = tuple([tuple(r) for r in self.rooms])
        h = tuple(self.hallway)
        return (rs, h)

    def end_state(self):
        return State([['A']*4, ['B']*4, ['C']*4, ['D']*4], [None]*11)

start = State(rooms, start_hallway)
memory = {start.to_key(): 0}

unchecked_states = [start]
while len(unchecked_states) != 0:
    # print('checking', len(unchecked_states), 'new states')
    new_reached = []
    for s in unchecked_states:
        s_key = s.to_key()
        for (cost_increase, next) in s.get_possible_moves():
            k = next.to_key()
            if k not in memory or memory[k] > memory[s_key] + cost_increase:
                memory[k] = memory[s_key] + cost_increase
                new_reached.append(next)
    unchecked_states = new_reached.copy()

print(memory[start.end_state().to_key()])

print(len(memory))