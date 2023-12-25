import os

input_file = os.path.join(os.path.dirname(__file__), 'input25.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

name_map = {}
graph = []
def make_graph():
	next_idx = 0
	for l in lines:
		name, conn = l.split(':')
		conn = conn.split()
		for n in [name] + conn:
			if n not in name_map.keys():
				name_map[n] = next_idx
				graph.append([])
				next_idx += 1
		node = name_map[name]
		for n in map(name_map.get, conn):
			graph[node].append(n)
			graph[n].append(node)

make_graph()

def get_flow(source, sink):
	num_nodes = len(graph)
	first_edge = [-1] * num_nodes
	# Each edge is a list of (to, next, capacity)
	edges = []
	edge_idx = 0

	# Create the flow network and residual graph
	for n in range(num_nodes):
		for to in graph[n]:
			# Add edge n->to with capacity 1
			edges.append([to, first_edge[n], 1])
			first_edge[n] = edge_idx
			edge_idx += 1
			# Add residual edge to->n with capacity 0
			edges.append([n, first_edge[to], 0])
			first_edge[to] = edge_idx
			edge_idx += 1

	dead_end = None
	levels = None

	def flow(node):
		edge_idx = first_edge[node]
		while edge_idx != -1:
			to, next, cap = edges[edge_idx]
			if cap > 0 and levels[node]<levels[to] and not dead_end[to]:
				if (to == sink) or (levels[to] < levels[sink] and flow(to)):
					edges[edge_idx][2] -= 1
					edges[edge_idx^1][2] += 1
					return True
				else:
					dead_end[to] = True
			edge_idx = next
		return False

	max_flow = 0 # The maximum flow reached
	# How many nodes are reached from the source. This will give us the result.
	source_nodes = 0
	while True:
		# Make levels for Dinitz's algorithm
		levels = [-1] * num_nodes
		levels[source] = 0
		curr_nodes = [source]
		curr_level = 0
		source_nodes = 1
		while len(curr_nodes) != 0:
			next_nodes = []
			curr_level += 1
			for n in curr_nodes:
				edge_idx = first_edge[n]
				while edge_idx != -1:
					to, next, cap = edges[edge_idx]
					if cap > 0 and levels[to] == -1:
						levels[to] = curr_level
						next_nodes.append(to)
					edge_idx = next
			curr_nodes = next_nodes
			source_nodes += len(next_nodes)

		if levels[sink] == -1:
			# No more augmenting paths
			break

		dead_end = [False] * num_nodes
		while True:
			if not flow(source):
				break
			max_flow += 1

	return max_flow, source_nodes * (num_nodes - source_nodes)

def solve_part1():
	for source in range(len(graph)):
		for sink in range(len(graph)-1, -1, -1):
			flow, ans = get_flow(source, sink)
			if flow == 3:
				return ans
	return None

print(f'Part 1:', solve_part1()) # 583632
print(f'Part 2:', "Just press the button!")
