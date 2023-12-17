import os

input_file = os.path.join(os.path.dirname(__file__), 'input14.txt')
def get_result(lines):
	return sum([x * y for x, y in zip(range(len(lines), 0, -1), [''.join(l).count('O') for l in lines])])

def solve_part1():
	with open(input_file) as f:
		lines = f.read().splitlines()

	lines = [list(x) for x in lines]
	w, h = len(lines[0]), len(lines)

	for col in range(w):
		for row in range(h):
			if lines[row][col] == 'O':
				while row >= 1 and lines[row-1][col] == '.':
					lines[row][col], lines[row-1][col] = lines[row-1][col], lines[row][col]
					row -= 1

	return get_result(lines)

def solve_part2():
	with open(input_file) as f:
		lines = f.read().splitlines()

	lines = [list(x) for x in lines]
	w, h = len(lines[0]), len(lines)

	patterns = {}

	iter = 0
	while iter < 1000000000:
		# North
		for col in range(w):
			next_empty = 0
			for row in range(h):
				if lines[row][col] == 'O':
					while next_empty+1 < h and lines[next_empty][col] != '.':
						next_empty += 1
					if next_empty < row:
						lines[row][col], lines[next_empty][col] = lines[next_empty][col], lines[row][col]
				elif lines[row][col] == '#':
					next_empty = row
		# West
		for row in range(h):
			next_empty = 0
			for col in range(w):
				if lines[row][col] == 'O':
					while next_empty+1 < w and lines[row][next_empty] != '.':
						next_empty += 1
					if next_empty < col:
						lines[row][col], lines[row][next_empty] = lines[row][next_empty], lines[row][col]
				elif lines[row][col] == '#':
					next_empty = col
		# South
		for col in range(w):
			next_empty = h-1
			for row in range(h-1, -1, -1):
				if lines[row][col] == 'O':
					while next_empty-1 >= 0 and lines[next_empty][col] != '.':
						next_empty -= 1
					if next_empty > row:
						lines[row][col], lines[next_empty][col] = lines[next_empty][col], lines[row][col]
				elif lines[row][col] == '#':
					next_empty = row
		# East
		for row in range(h):
			next_empty = w-1
			for col in range(w-1, -1, -1):
				if lines[row][col] == 'O':
					while next_empty-1 >= 0 and lines[row][next_empty] != '.':
						next_empty -= 1
					if next_empty > col:
						lines[row][col], lines[row][next_empty] = lines[row][next_empty], lines[row][col]
				elif lines[row][col] == '#':
					next_empty = col

		iter += 1
		new_pattern = ''.join([x for l in lines for x in l])
		if new_pattern in patterns.keys():
			cycle_len = iter - patterns[new_pattern]
			iter += cycle_len * ((1000000000 - iter)//cycle_len)
		else:
			patterns[new_pattern] = iter

	return get_result(lines)

print(f'Part 1: {solve_part1()}') # 109385
print(f'Part 2: {solve_part2()}') # 93102
