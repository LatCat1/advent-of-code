from loader import load_data
import networkx as nx

data = load_data(day=25, year=2023, testing=False)
data = data.split('\n')

edges = []
for d in data:
    a, b = d.split(':')
    b = b.strip()
    ns = b.split(' ')
    for n in ns:
        edges.append((a, n))

g = nx.Graph(edges)
_, a = nx.stoer_wagner(g)
print(len(a[0])*len(a[1]))