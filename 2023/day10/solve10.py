import os

LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

def direction(x):
	return 1<<x

def opposite(x):
	return 1<<(x^1)

DIR_TO_IDX = {direction(x): x for x in range(4)}

def makePipe(directions):
	return sum([direction(x) for x in directions])

PIPES = {
	'|': makePipe([UP, DOWN]),
	'-': makePipe([LEFT, RIGHT]),
	'J': makePipe([UP, LEFT]),
	'L': makePipe([UP, RIGHT]),
	'7': makePipe([LEFT, DOWN]),
	'F': makePipe([RIGHT, DOWN]),
	'.': 0,
}

# Left, right, up, down in that order
NEIGHBOURS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

input_file = os.path.join(os.path.dirname(__file__), 'input10.txt')
with open(input_file) as f:
	graph = f.read().splitlines()

w = len(graph[0])
h = len(graph)

def pos_valid(row, col):
	return row >= 0 and col >= 0 and row < h and col < w

def solve():
	dist = [[-1] * w for _ in range(h)]
	next_nodes = []
	for row in range(h):
		for col in range(w):
			if graph[row][col] == 'S':
				next_nodes.append((row, col))
				dist[row][col] = 0
				break

	start_row, start_col = next_nodes.pop()
	start_pipe = 0
	for dir, neigh in enumerate(NEIGHBOURS):
		new_row = start_row + neigh[0]
		new_col = start_col + neigh[1]
		if pos_valid(new_row, new_col) and PIPES[graph[new_row][new_col]] & opposite(dir):
			next_nodes.append((new_row, new_col, DIR_TO_IDX[PIPES[graph[new_row][new_col]] & ~(opposite(dir))]))
			start_pipe += direction(dir)

	# In python, I can't change the string, so I can't change the 'S' to whatever pipe it actually is.
	# Instead, just add it as another type
	PIPES['S'] = start_pipe

	if len(next_nodes) != 2:
		print("Solutions is not valid")

	current_dist = 0
	while len(next_nodes) > 0:
		current_nodes = next_nodes
		next_nodes = []
		current_dist += 1
		for row, col, dir in current_nodes:
			if dist[row][col] == -1:
				dist[row][col] = current_dist
				new_row = row + NEIGHBOURS[dir][0]
				new_col = col + NEIGHBOURS[dir][1]
				if pos_valid(new_row, new_col):
					pipe = PIPES[graph[new_row][new_col]]
					next_nodes.append((new_row, new_col, DIR_TO_IDX[pipe & ~(opposite(dir))]))

	# Remove 1 since the loop goes one more time after reaching the end before it exits
	current_dist -= 1
	print(f'Part 1: {current_dist}') # 6842
	# =========================================================================================

	num_inside = 0

	# For part 2 I use a horizontal line intersection with the border of the loop. But offset with a infinitely small amount up.
	# This is just enough, so that we don't align exactly on the horizontal segments, but small enough so that we cross
	# exactly the same cells. For horizontal cells, even if we are on the inside, we won't count those anyway.
	# The every time we intersect the border, we change on which side we are (starting from the outside).

	# Interestingly, the only pipes we will intersect are the ones that have a vertical line going up. We could change to a small
	# offset down, and then only pipes with ends going down will be intersected.
	for row in range(h):
		# For each row, start from the outside
		is_outside = True
		for col in range(w):
			# If this cell is part of the loop, check the pipe direction
			if dist[row][col] != -1:
				pipe = PIPES[graph[row][col]]
				if bool(pipe & direction(UP)):
					is_outside = not is_outside
			# Otherwise, it is just a random cell. Count it if we are on the inside
			elif not is_outside:
				num_inside += 1

	print(f'Part 2: {num_inside}') # 393

solve()
