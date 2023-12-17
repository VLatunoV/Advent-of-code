import os

input_file = os.path.join(os.path.dirname(__file__), 'input16.txt')

UP_IDX = 0
RIGHT_IDX = 1
DOWN_IDX = 2
LEFT_IDX = 3

UP = (1<<UP_IDX)
RIGHT = (1<<RIGHT_IDX)
DOWN = (1<<DOWN_IDX)
LEFT = (1<<LEFT_IDX)

next_cell = [(-1, 0), (0, 1), (1, 0), (0, -1)]

next_dir = {
	'.': list(range(4)),
	'|': list(range(4)),
	'-': list(range(4)),
	'\\': [LEFT_IDX, DOWN_IDX, RIGHT_IDX, UP_IDX],
	'/': [RIGHT_IDX, UP_IDX, LEFT_IDX, DOWN_IDX],
}

dir_idx = {
	UP: UP_IDX,
	RIGHT: RIGHT_IDX,
	DOWN: DOWN_IDX,
	LEFT: LEFT_IDX,
}

with open(input_file) as f:
	board = f.read().splitlines()

w, h = len(board[0]), len(board)

def valid_pos(row, col):
	return row >= 0 and row < h and col >= 0 and col < w

def should_split(row, col, direction):
	c = board[row][col]
	match c:
		case '-': return bool(direction & (UP | DOWN))
		case '|': return bool(direction & (LEFT | RIGHT))
	return False

def send_light(light, row, col, d):
	while valid_pos(row, col) and bool(light[row][col] & (1<<d)) == 0:
		light[row][col] |= 1<<d
		cell = board[row][col]
		if should_split(row, col, 1<<d):
			# Send light to on of the split ends
			d = d ^ 1
			nc = next_cell[d]
			new_row = row + nc[0]
			new_col = col + nc[1]
			send_light(light, new_row, new_col, d)

			# Continue without recursion on the other end
			# This is called Tail call optimization
			d = d ^ 2
		else:
			d = next_dir[cell][d]

		nc = next_cell[d]
		row += nc[0]
		col += nc[1]

def solve(row, col, d):
	light = [[0] * w for _ in range(h)]
	send_light(light, row, col, d)
	return sum([bool(x) for r in light for x in r])

def solve_part1():
	return solve(0, 0, RIGHT_IDX)

def solve_part2():
	result = 0
	for row in range(h):
		result = max(result, solve(row, 0, RIGHT_IDX), solve(row, w-1, LEFT_IDX))
	for col in range(w):
		result = max(result, solve(0, col, DOWN_IDX), solve(h-1, col, UP_IDX))
	return result

print(f'Part 1:', solve_part1()) # 7060
print(f'Part 2:', solve_part2()) # 7493
