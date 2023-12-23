import os

input_file = os.path.join(os.path.dirname(__file__), 'input23.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

w, h = len(lines[0]), len(lines)

start_row = 0
start_col = lines[0].index('.')
end_row = h-1
end_col = lines[-1].index('.')

# Helps avoid bound checks, since the whole grid is already surrounded with '#'s
lines[0] = lines[0].replace('.', 'v')
lines[-1] = lines[-1].replace('.', '^')

next_cell = [(1, 0), (-1, 0), (0, 1), (0, -1)]

# Map from nodes to a list of neighbours
graph = {}

# Reduce the grid to only single step edges. To do this traverce the grid with DFS and check if
# each cell is an intersection (has 3 or 4 open cells). Those cells are the new vertices of the
# graph. The edges are added by keeping from which previous node any node was discovered, and the
# distance to it.
def make_graph(part):
	global graph
	graph[(start_row, start_col)] = []
	graph[(end_row, end_col)] = []
	for row in range(1, h-1):
		for col in range(1, w-1):
			if lines[row][col] != '#':
				empty_count = 0
				for i in range(4):
					nr = row + next_cell[i][0]
					nc = col + next_cell[i][1]
					if lines[nr][nc] != '#':
						empty_count += 1
				if empty_count > 2:
					# This is an intersection. Add it as a new node
					graph[(row, col)] = []

	visited = [[0] * w for _ in range(h)]
	visited[start_row][start_col] = 1
	stack = [[start_row, start_col, 0, 0]]
	nodes = [(start_row, start_col)]
	while len(stack) != 0:
		# Check if all neighbours were visited
		if stack[-1][3] == 4:
			_, _, d, _ = stack.pop()
			if d == 0:
				nodes.pop()
			continue
		r, c, d, i = stack[-1]

		# Get the next neighbour cell
		if lines[r][c] == '.':
			nr = r + next_cell[i][0]
			nc = c + next_cell[i][1]
			stack[-1][3] += 1
		else:
			nr, nc = r, c
			match lines[r][c]:
				case '>': nc += 1
				case '<': nc -= 1
				case '^': nr -= 1
				case 'v': nr += 1
			stack[-1][3] = 4

		# Handle the cell if it's open
		if lines[nr][nc] != '#':
			# For part 1 we don't want to move against a slope. (Except on the end, because it was added)
			if part == 1 and nr != h-1:
				if lines[nr][nc] == 'v' and nr == r-1: continue
				if lines[nr][nc] == '^' and nr == r+1: continue
				if lines[nr][nc] == '>' and nc == c-1: continue
				if lines[nr][nc] == '<' and nc == c+1: continue
			# If the next cell is a node, add an edge to the graph
			if (nr, nc) in graph.keys() and (nr, nc) != nodes[-1]:
				# For part 1 all edges are oriented. For part 2 they are not, so add the opposite too.
				graph[nodes[-1]].append((nr, nc, d+1))
				if part == 2:
					graph[(nr, nc)].append((nodes[-1][0], nodes[-1][1], d+1))
				# Book keeping
				if not visited[nr][nc]:
					nodes.append((nr, nc))
				d = -1
			if not visited[nr][nc]:
				visited[nr][nc] = 1
				stack.append([nr, nc, d + 1, 0])

def visit(row, col, visited):
	result = 0
	if row == h-1:
		# Return as second argument whether we found the end
		return result, True

	for nr, nc, d in graph[(row, col)]:
		if not visited[nr][nc]:
			visited[nr][nc] = True
			r, found = visit(nr, nc, visited)
			if found and result < r + d:
				result = r + d
			visited[nr][nc] = False
	return result, result != 0

def solve_part1():
	make_graph(part=1)
	visited = [[False] * w for _ in range(h)]
	visited[start_row][start_col] = True
	return visit(start_row, start_col, visited)[0]

def solve_part2():
	lines[1:-1] = [l.replace('v', '.').replace('^', '.').replace('<', '.').replace('>', '.') for l in lines[1:-1]]
	make_graph(part=2)
	visited = [[False] * w for _ in range(h)]
	visited[start_row][start_col] = True
	return visit(start_row, start_col, visited)[0]

print(f'Part 1:', solve_part1()) # 2202
print(f'Part 2:', solve_part2()) # 6226
