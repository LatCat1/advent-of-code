import pathlib
from math import ceil

with open(f"{pathlib.Path(__file__).parent.resolve()}/input.txt", 'r') as f:
    lines = f.read().split('\n')

file = list(map(int, lines))
# locations = list(range(len(file)))  #locations[i] holds where the ith of the original list currently is. starts out at i

class Node:   # could be captured by a Nx3 array
    def __init__(self, id: int, value: int, prev=None, next=None):
        self.id = id
        self.value = value
        self.prev = prev
        self.next = next

    def __str__(self):
        return str((self.id, self.value))

chain = []   # chain[i] is the node with id i
for i, f in enumerate(file):
    chain.append(Node(i, f))

for i in range(len(chain)):
    chain[i].prev = chain[(i-1)%len(chain)]
    chain[i].next = chain[(i+1)%len(chain)]

step_size = ceil(len(chain)**0.5)
waypoints = {}
# find 0, set it at waypoint 0
curr = chain[file.index(0)]
i = 0
while i < len(chain):
    waypoints[i] = curr
    for _ in range(step_size):
        curr = curr.next
        i += 1

def pw(waypoints):
    print([(v, str(waypoints[v])) for v in waypoints])

def pc(chain):
    x = chain[0].prev
    print([(x := x.next).value for _ in range(len(chain))])

def get_index(node: Node, chain, waypoints):
    offset = 0
    while True:
        for i in waypoints:
            if waypoints[i].id == node.id:
                return i + offset
        offset += 1
        node = node.prev

for _ in range(10):
    for node in chain:
        ind = get_index(node, chain, waypoints)
        to = (ind+node.value)%(len(chain)-1)
        # print(ind, to)
        if ind < to:
            d = 1
        else:
            d = -1
        mi = min(ind, to)
        ma = max(ind, to)
        p, n = node.prev, node.next  # remove it from the chain
        p.next = n
        n.prev = p
        for v in waypoints:
            if waypoints[v].id == node.id:
                waypoints[v] = waypoints[v].next
        # now place it back. first find closest waypoint
        d = (to//step_size)*step_size
        curr = waypoints[d]
        while d < to:
            d += 1
            curr = curr.next
        if to == 0:
            curr = waypoints[0].prev
        # insert after curr?
        cn = curr.next
        curr.next = node
        node.next = cn
        node.prev = curr
        cn.prev = node
        for v in waypoints:
            if mi<=v<=ma and v != 0:
                if ind<to:
                    waypoints[v] = waypoints[v].next
                else:
                    waypoints[v] = waypoints[v].prev
        # pc(chain)
        # pw(waypoints)
print('done')