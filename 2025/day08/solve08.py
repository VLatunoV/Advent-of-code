import os

input_file = os.path.join(os.path.dirname(__file__), 'input08.txt')
with open(input_file) as f:
	lines = f.read().splitlines()
	points = [list(map(int, x.split(','))) for x in lines]

def dist2(x, y):
	return (x[0]-y[0])**2 + (x[1]-y[1])**2 + (x[2]-y[2])**2

def make_parents(size):
	'''
	If a node is the root, its value is -<number of nodes> in the tree
	Otherwise, its parent is the index of the parent
	'''
	return [-1] * size

def get_parent(node, parents):
	'''
	This traverses only nodes with parents (parents value is non-negative).
	So there is no need to handle tree size arithmetics
	'''
	if parents[node] < 0:
		return node

	result = node
	while parents[result] >= 0:
		result = parents[result]
	while parents[node] != result:
		next_node = parents[node]
		parents[node] = result
		node = next_node
	return result

def connect(x, y, parents):
	px = get_parent(x, parents)
	py = get_parent(y, parents)
	if px != py:
		parents[py] += parents[px]
		parents[px] = py

def solve():
	# Create all pairs
	n = len(points)
	pairs = [(i, j)
		for i in range(n - 1)
			for j in range(i+1, n)
	]
	pairs.sort(key=lambda x: dist2(points[x[0]], points[x[1]]))
	
	# Connect closest 1000 pairs
	parents = make_parents(n)
	for i in range(1000):
		connect(*pairs[i], parents)

	# Part 1 is the size of the 3 largest trees
	tmp_parents = sorted(parents)
	part1 = abs(tmp_parents[0] * tmp_parents[1] * tmp_parents[2])

	# Continue until some parent has all nodes. Then everything is connected
	while parents[pairs[i][0]] != -n and parents[pairs[i][1]] != -n:
		i += 1
		connect(*pairs[i], parents)
	part2 = points[pairs[i][0]][0] * points[pairs[i][1]][0]
	return part1, part2

p1, p2 = solve()
print('Part 1:', p1) # 133574
print('Part 2:', p2) # 2435100380
