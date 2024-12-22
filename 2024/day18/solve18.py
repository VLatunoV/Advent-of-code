import os

input_file = os.path.join(os.path.dirname(__file__), 'input18.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

width = height = 71
obstacles = [(int(x), int(y)) for x,y in [z.split(',') for z in lines]]
neighbour = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def check_bounds(r, c):
	return r>=0 and r<height and c>=0 and c<width

def solve_part1():
	visited = [[False] * width for _ in range(height)]
	for r, c in obstacles[:1024]:
		visited[r][c] = True
	
	dist = 0
	visited[0][0] = True
	front = [(0, 0)]
	while len(front) > 0:
		new_front = []
		for r, c in front:
			if (r, c) == (height-1, width-1):
				return dist
			for rr, cc in neighbour:
				nr = r+rr
				nc = c+cc
				if check_bounds(nr, nc) and not visited[nr][nc]:
					visited[nr][nc] = True
					new_front.append((nr, nc))
		front = new_front
		dist += 1
	return -1

def find_root(parent, x):
	r, c = x
	orig_x = x
	while parent[r][c] != (r, c):
		r, c = parent[r][c]
	while parent[orig_x[0]][orig_x[1]] != (r, c):
		next = parent[orig_x[0]][orig_x[1]]
		parent[orig_x[0]][orig_x[1]] = (r, c)
		orig_x = next
	return r, c

def parent_merge(parent, x, y):
	root_x = find_root(parent, x)
	root_y = find_root(parent, y)
	if root_x != root_y:
		parent[root_x[0]][root_x[1]] = root_y

def solve_part2():
	grid = [[0] * width for _ in range(height)]
	for r, c in obstacles:
		grid[r][c] += 1
	parent = [[-1]*width for _ in range(height)]
	for r in range(height):
		for c in range(width):
			if grid[r][c] != 0:
				continue

			parent[r][c] = (r, c)
			if c > 0 and grid[r][c-1] == 0:
				parent[r][c] = parent[r][c-1]
			if r > 0 and grid[r-1][c] == 0:
				parent_merge(parent, (r,c), (r-1, c))

	ans = -1
	for idx in range(len(obstacles)-1, -1, -1):
		r, c = obstacles[idx]
		grid[r][c] -= 1
		if grid[r][c] != 0:
			continue
		parent[r][c] = (r, c)
		for rr, cc in neighbour:
			nr = r + rr
			nc = c + cc
			if check_bounds(nr, nc) and grid[nr][nc] == 0:
				parent_merge(parent, (r, c), (nr, nc))
		if find_root(parent, (0, 0)) == find_root(parent, (height-1, width-1)):
			ans = f'{r},{c}'
			break
	return ans

print('Part 1:', solve_part1())
print('Part 2:', solve_part2())
