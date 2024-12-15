import os

input_file = os.path.join(os.path.dirname(__file__), 'input10.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

grid = [[int(x) for x in y] for y in lines]

def count_ends(r, c):
	visited = [[False] * len(grid[0]) for _ in grid]
	visited[r][c] = True

	front = [(r, c)]
	neighbour = [(1, 0), (-1, 0), (0, 1), (0, -1)]
	level = 0
	while level < 9:
		new_front = []
		level += 1
		for r, c in front:
			for rr, cc in neighbour:
				nr = r + rr
				nc = c + cc
				if nr >= 0 and nr < len(grid) and nc >= 0 and nc < len(grid[0]):
					if not visited[nr][nc] and grid[nr][nc] == level:
						visited[nr][nc] = True
						new_front.append((nr, nc))
		front = new_front
	return len(front)

def solve_part1():
	ans = 0
	for r in range(len(grid)):
		for c in range(len(grid[0])):
			if grid[r][c] == 0:
				ans += count_ends(r, c)
	return ans

def solve_part2():
	paths = [[0] * len(grid[0]) for _ in range(len(grid))]
	front = []
	for r in range(len(grid)):
		for c in range(len(grid[0])):
			if grid[r][c] == 9:
				paths[r][c] = 1
				front.append((r, c))
	
	neighbour = [(1, 0), (-1, 0), (0, 1), (0, -1)]
	for level in range(8, -1, -1):
		new_front = []
		for r, c in front:
			for rr, cc in neighbour:
				nr = r + rr
				nc = c + cc
				if nr >= 0 and nr < len(grid) and nc >= 0 and nc < len(grid[0]):
					if grid[nr][nc] == level:
						if paths[nr][nc] == 0:
							new_front.append((nr, nc))
						paths[nr][nc] += paths[r][c]
		front = new_front
	
	ans = 0
	for r, c in front:
		ans += paths[r][c]
	return ans

print('Part 1:', solve_part1())
print('Part 2:', solve_part2())
