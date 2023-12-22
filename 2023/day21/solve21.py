import os

input_file = os.path.join(os.path.dirname(__file__), 'input21.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

grid = [[c for c in l] for l in lines]
w, h = len(grid[0]), len(grid)
next_cell = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def valid_pos(row, col):
	return row >= 0 and row < h and col >= 0 and col < w

# Input is rigged, so this is true
start_row, start_col = 65, 65
# for row in range(h):
# 	for col in range(w):
# 		if grid[row][col] == 'S':
# 			start_row = row
# 			start_col = col
# 			grid[row][col] = '.'
# 			break
# 	if start_row != -1:
# 		break

# Calculate what the answer is for the grid for each step size, until all cells are visited.
# The result has some unknown length.
def calc_counts(row, col):
	visited = [[False] * w for _ in range(h)]
	visited[row][col] = True
	current_nodes = [(row, col)]
	counts = []
	while len(current_nodes) != 0:
		next_nodes = []
		counts.append(len(current_nodes))
		for r, c in current_nodes:
			for d in range(4):
				new_row = r + next_cell[d][0]
				new_col	= c + next_cell[d][1]
				if valid_pos(new_row, new_col) and not visited[new_row][new_col] and grid[new_row][new_col] == '.':
					visited[new_row][new_col] = True
					next_nodes.append((new_row, new_col))
		current_nodes = next_nodes

	for i in range(2, len(counts)):
		counts[i] += counts[i-2]
	return counts

# Get the how many cells are visited for the given number of steps. If there are more steps
# than 'counts', just go back and forth to decrease the steps. That means we should get the
# largest answer with the same oddness as the number of steps.
def get_result_for_steps(steps, counts):
	if steps < 0:
		return 0
	if steps < len(counts):
		return counts[steps]
	if (steps&1) == (len(counts)&1):
		return counts[-2]
	else:
		return counts[-1]

def solve(max_steps):
	# Precompute the answer starting from specific positions
	# 0 = lower boundary of the grid
	# 1 = upper boundary of the grid
	# 2 = start position
	# The name prc encodes p = point, r = row and c = col
	p00 = calc_counts(0, 0)
	p01 = calc_counts(0, w-1)
	p10 = calc_counts(h-1, 0)
	p11 = calc_counts(h-1, w-1)
	p02 = calc_counts(0, start_col)
	p12 = calc_counts(h-1, start_col)
	p20 = calc_counts(start_row, 0)
	p21 = calc_counts(start_row, w-1)
	p22 = calc_counts(start_row, start_col)

	# Start by adding the cells from the initial grid
	result = get_result_for_steps(max_steps, p22)
	# Move to the edge. Because the input is rigged and we are the center, each edge is the same distance away.
	max_steps -= w - start_col

	# Now we take steps, which expand the reachable cells in a diamond.
	# This variable keeps track of how many grids are between each north, east, south and west leading grids
	side_grids = 1
	while max_steps >= 0:
		result += (
			get_result_for_steps(max_steps, p20) +
			get_result_for_steps(max_steps, p21) +
			get_result_for_steps(max_steps, p02) +
			get_result_for_steps(max_steps, p12)
		)
		result += side_grids * (
			get_result_for_steps(max_steps - (w - start_col), p00) +
			get_result_for_steps(max_steps - (w - start_col), p01) +
			get_result_for_steps(max_steps - (w - start_col), p10) +
			get_result_for_steps(max_steps - (w - start_col), p11)
		)
		max_steps -= w
		side_grids += 1

	return result

print(f'Part 1:', solve(64)) # 3532
print(f'Part 2:', solve(26501365)) # 590104708070703
