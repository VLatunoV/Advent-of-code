import os

input_file = os.path.join(os.path.dirname(__file__), 'input11.txt')
with open(input_file) as f:
	board = [list(x) for x in f.read().splitlines()]

w = len(board[0])
h = len(board)

def solve(part):
	if part == 1:
		empty_dist = 2-1
	else:
		empty_dist = int(10**6)-1

	row_tree = [0] * (2*h)
	col_tree = [0] * (2*w)

	for row in range(h):
		empty = True
		for col in range(w):
			if board[row][col] == '#':
				empty = False
				break
		if empty:
			row_tree[h + row] += empty_dist

	for col in range(w):
		empty = True
		for row in range(h):
			if board[row][col] == '#':
				empty = False
				break
		if empty:
			col_tree[w + col] += empty_dist

	# Make the trees
	for i in range(h-1, -1, -1):
		row_tree[i] = row_tree[i*2] + row_tree[i*2 + 1]
	for i in range(w-1, -1, -1):
		col_tree[i] = col_tree[i*2] + col_tree[i*2 + 1]

	def get_interval(tree, left, right):
		left += len(tree)//2
		right += len(tree)//2
		result = 0
		while left != right:
			if (left&1):
				result += tree[left]
				left += 1
			if (right&1):
				right -= 1
				result += tree[right]
			left = left//2
			right = right//2
		return result

	star_positions = []
	for row in range(h):
		for col in range(w):
			if board[row][col] == '#':
				star_positions.append((row, col))

	def get_dist(star1, star2):
		r1, c1 = star1
		r2, c2 = star2
		if r1 > r2:
			r1, r2 = r2, r1
		if c1 > c2:
			c1, c2 = c2, c1
		return \
			abs(star1[0] - star2[0]) + abs(star1[1] - star2[1]) \
			+ get_interval(row_tree, r1, r2) + get_interval(col_tree, c1, c2)

	result = 0
	for star1_idx in range(len(star_positions)):
		star1 = star_positions[star1_idx]
		for star2_idx in range(star1_idx + 1, len(star_positions)):
			star2 = star_positions[star2_idx]
			result += get_dist(star1, star2)
	return result

print(f'Part 1: {solve(part=1)}') # 9521550
print(f'Part 2: {solve(part=2)}') # 298932923702
