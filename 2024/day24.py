from loader import load_data
from collections import defaultdict, Counter
import re
from functools import lru_cache, reduce, total_ordering
from datetime import datetime
import heapq as hq
from operator import and_, or_, xor

data = load_data(24, 2024, testing=True)
data = load_data(24, 2024, testing=False)

initial_values_info, gate_info = data.split("\n\n")

wires = {
    s[:3]: bool(int(s[5:])) for s in initial_values_info.split('\n')
}

gates = {}
exp = r'(...) (AND|OR|XOR) (...) -> (...)'
for g in gate_info.split('\n'):
    match = re.match(exp, g)

    func = {
        'AND': and_,
        'OR': or_,
        'XOR': xor
    }

    gates[match.group(4)] = (func[match.group(2)], match.group(1), match.group(3))

def run(wires, gates):

    saved = {w: wires[w] for w in wires}
    def compute(wire):
        if wire not in saved:
            gate, in1, in2 = gates[wire]
            saved[wire] = gate(compute(in1), compute(in2))
        return saved[wire]

    for g in gates:
        compute(g)    
    return saved

# now get the output

def get_output(wires):
    final_values = run(wires, gates)
    return int(
        ''.join(str(int(final_values[w])) for w in sorted(
            (h for h in final_values.keys() if re.match(exp, h)), reverse=True
        )),
        base=2
    )

exp = r'z\d\d'
print('P1:', get_output(wires))

def test(a, b):
    # turn a, b into 45-digit binary numbers
    test_wires = {f"x{n:02}": 1 if a & (1 << n) else 0 for n in range(45)} \
            | {f"y{n:02}": 1 if b & (1 << n) else 0 for n in range(45)}

    return(get_output(test_wires))


# something is happening with 5 and 6, 10 and 11, 15 and 16, 36 
def swap(g1, g2):
    gates[g1], gates[g2] = gates[g2], gates[g1]

swaps = [
    ('vwr', 'z06'),
    ('tqm', 'z11'),
    ('kfs', 'z16'),
    ('hcm', 'gfv')
]
# for s in swaps:
#     swap(*s)


print(','.join(
    sorted([*swaps[0], *swaps[1], *swaps[2], *swaps[3]])
))