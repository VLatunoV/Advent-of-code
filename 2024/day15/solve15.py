import os

input_file = os.path.join(os.path.dirname(__file__), 'input15.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

map_end = lines.index('')
warehouse = lines[:map_end]
moves = ''.join(lines[map_end+1:])
for r in range(len(warehouse)):
	robot = warehouse[r].find('@')
	if robot != -1:
		robot_r, robot_c = r, robot
		break

direction = {
	'>': (0, 1),
	'<': (0, -1),
	'v': (1, 0),
	'^': (-1, 0)
}

def move_robot(grid, r, c, d):
	dir = direction[d]
	last_r = r + dir[0]
	last_c = c + dir[1]
	while grid[last_r][last_c] == 'O':
		last_r += dir[0]
		last_c += dir[1]
	
	if grid[last_r][last_c] == '.':
		while (last_r, last_c) != (r, c):
			nr, nc = (last_r - dir[0], last_c - dir[1])
			grid[last_r][last_c] = grid[nr][nc]
			last_r, last_c = nr, nc
		grid[r][c] = '.'
		return r + dir[0], c + dir[1]
	return r, c

def solve_part1():
	grid = [[y for y in x] for x in warehouse]
	r = robot_r
	c = robot_c
	for d in moves:
		r, c = move_robot(grid, r, c, d)

	ans = 0
	for r in range(len(grid)):
		for c in range(len(grid[0])):
			if grid[r][c] == 'O':
				ans += r*100 + c
	return ans

def move_robot_wide(grid, r, c, d):
	dir = direction[d]
	if dir[0] == 0:
		# Horizontal move
		nc = c + dir[1]
		while grid[r][nc] in ['[', ']']:
			nc += dir[1]
		if grid[r][nc] == '.':
			while nc != c:
				grid[r][nc] = grid[r][nc - dir[1]]
				nc -= dir[1]
			grid[r][c] = '.'
			return True
		else:
			return False
	else:
		# Vertical move
		to_be_moved = []
		last_moved = [(r, c)]
		can_move = True
		while can_move and len(last_moved) > 0:
			new_moved = []
			to_be_moved.extend(last_moved)
			for r, c in last_moved:
				nr = r + dir[0]
				if (nr, c) in new_moved:
					continue
				match grid[nr][c]:
					case '#':
						can_move = False
						break
					case '.':
						continue
					case '[':
						new_moved.append((nr, c))
						new_moved.append((nr, c+1))
					case ']':
						new_moved.append((nr, c))
						new_moved.append((nr, c-1))
			last_moved = new_moved

		if not can_move:
			return False
		
		for r, c in reversed(to_be_moved):
			grid[r + dir[0]][c] = grid[r][c]
			grid[r][c] = '.'
		
		return True

new_tiles = {
	'#': '##',
	'.': '..',
	'O': '[]',
	'@': '@.'
}

def solve_part2():
	grid = [[z for y in x for z in list(new_tiles[y])] for x in warehouse]
	r = robot_r
	c = robot_c*2
	for d in moves:
		if move_robot_wide(grid, r, c, d):
			r += direction[d][0]
			c += direction[d][1]

	ans = 0
	for r in range(len(grid)):
		for c in range(len(grid[0])):
			if grid[r][c] == '[':
				ans += r*100 + c
	return ans

print('Part 1:', solve_part1())
print('Part 2:', solve_part2())
