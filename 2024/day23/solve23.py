import os

input_file = os.path.join(os.path.dirname(__file__), 'input23.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

connections = [x.split('-') for x in lines]
all_nodes = set()
graph = {}
for a, b in connections:
	all_nodes.add(a)
	all_nodes.add(b)
	n = graph.setdefault(a, [])
	n.append(b)
	n = graph.setdefault(b, [])
	n.append(a)

node_to_id = {}
id_to_node = []
for x in all_nodes:
	node_to_id[x] = len(id_to_node)
	id_to_node.append(x)

def solve():
	edges = set()
	for a, b in connections:
		edges.add((a, b))
		edges.add((b, a))
	
	cliques = []
	ans = 0
	for i in range(len(id_to_node)):
		a = id_to_node[i]
		for j in range(i+1, len(id_to_node)):
			b = id_to_node[j]
			for k in range(j+1, len(id_to_node)):
				c = id_to_node[k]
				if (a, b) in edges and (a, c) in edges and (b, c) in edges:
					cliques.append(tuple(sorted([a, b, c])))
					if a[0] == 't' or b[0] == 't' or c[0] == 't':
						ans += 1

	cliques = set(cliques)
	while len(cliques) > 1:
		new_cliques = set()
		for cl in cliques:
			x = cl[0]
			for next in graph[x]:
				if next in cl:
					continue
				good = True
				for other in cl[1:]:
					if (next, other) not in edges:
						good = False
						break
				if good:
					new_cliques.add(tuple(sorted((next, *cl))))

		cliques = new_cliques
	return ans, ','.join(list(cliques)[0])

p1, p2 = solve()

print('Part 1:', p1)
print('Part 2:', p2)
