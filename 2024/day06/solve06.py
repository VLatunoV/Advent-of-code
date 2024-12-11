import os

input_file = os.path.join(os.path.dirname(__file__), 'input06.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

start_row = 0
start_col = 0
for r in range(len(lines)):
	start_col = lines[r].find('^')
	if start_col != -1:
		start_row = r
		break

dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def do_walk(r, c, d, visited):
	if visited is None:
		visited = [[[False] * len(lines[0]) for _ in range(len(lines))] for _ in range(len(dir))]
	visited[d][r][c] = True
	while True:
		nr = r + dir[d][0]
		nc = c + dir[d][1]
		if nr < 0 or nr >= len(lines):
			return False
		if nc < 0 or nc >= len(lines[0]):
			return False
		if visited[d][nr][nc]:
			return True

		if lines[nr][nc] == '#':
			d = (d+1)%len(dir)
		else:
			r = nr
			c = nc
			visited[d][r][c] = True

def solve_part1():
	visited = [[[False] * len(lines[0]) for _ in range(len(lines))] for _ in range(len(dir))]
	do_walk(start_row, start_col, 0, visited)
	
	ans = 0
	for r in range(len(lines)):
		for c in range(len(lines[0])):
			for d in range(len(dir)):
				if visited[d][r][c]:
					ans += 1
					break
	return ans

def solve_part2():
	visited = [[[False] * len(lines[0]) for _ in range(len(lines))] for _ in range(len(dir))]
	do_walk(start_row, start_col, 0, visited)

	# Lazy (and slow) solution: each time we check, we walk one
	# cell at a time. The better way would be to cache all distances
	# that we can walk in each direction for every empty cell.
	# But this runs in a minutes, so whatever.
	ans = 0
	for r in range(len(lines)):
		for c in range(len(lines[0])):
			if lines[r][c] == '.':
				is_visited = any([visited[x][r][c] for x in range(len(dir))])
				if is_visited:
					old = lines[r]
					lines[r] = old[:c] + '#' + old[c+1:]
					if do_walk(start_row, start_col, 0, None):
						ans += 1
					lines[r] = old
	return ans

print('Part 1:', solve_part1())
print('Part 2:', solve_part2())
