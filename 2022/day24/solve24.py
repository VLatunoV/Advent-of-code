import os

input_file = os.path.join(os.path.dirname(__file__), 'input24.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

w, h = len(lines[0]), len(lines)
lines.insert(0, '#' * w)
lines.append('#' * w)
h += 2
start_row = 1
start_col = lines[start_row].index('.')
end_row = h-2
end_col = lines[end_row].index('.')

next_cell = [(0,0), (1,0), (-1,0), (0,1), (0,-1)]
left_grid = [[0]*w for _ in range(h)]
right_grid = [[0]*w for _ in range(h)]
up_grid = [[0]*w for _ in range(h)]
down_grid = [[0]*w for _ in range(h)]
for r in range(h):
	for c in range(w):
		match lines[r][c]:
			case '<':
				left_grid[r][c] = 1
			case '>':
				right_grid[r][c] = 1
			case '^':
				up_grid[r][c] = 1
			case 'v':
				down_grid[r][c] = 1

def cell_free(row, col, step):
	col -= 1
	# Subtract 1 more because of the added border
	row -= 2
	if left_grid[2 + row][1 + (col+step)%(w-2)]:
		return False
	if right_grid[2 + row][1 + (col-step)%(w-2)]:
		return False
	if up_grid[2 + (row + step)%(h-4)][1 + col]:
		return False
	if down_grid[2 + (row - step)%(h-4)][1 + col]:
		return False
	return True

def solve(level):
	result = 0
	nodes = set([(start_row, start_col, 0)])
	while len(nodes) != 0:
		next_nodes = set()
		result += 1
		for r, c, l in nodes:
			for n in next_cell:
				nr = r + n[0]
				nc = c + n[1]
				nl = l
				if nr == start_row and nc == start_col and (l&1) == 1:
					nl += 1
				if nr == end_row and nc == end_col and (l&1) == 0:
					nl += 1
					if nl == level:
						return result
				if lines[nr][nc] != '#' and cell_free(nr, nc, result):
					next_nodes.add((nr, nc, nl))
		nodes = next_nodes

def solve_part1():
	return solve(1)

def solve_part2():
	return solve(3)

print('Part 1:', solve_part1())
print('Part 2:', solve_part2())
