import os

input_file = os.path.join(os.path.dirname(__file__), 'input17.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

next_cell = [(-1, 0), (0, 1), (1, 0), (0, -1)]

grid = [[int(x) for x in l] for l in lines]
w, h = len(grid[0]), len(grid)

# Operations for a min heap. It has a dummy element at the start for more practical indexing.
# The dummy element is chosen to be guaranteed the smallest possible, which removes a check in
# the push_heap loop for index validity
def push_heap(elem, heap):
	heap.append(elem)
	pos = len(heap) - 1
	up_pos = pos >> 1
	while heap[pos][0] < heap[up_pos][0]:
		heap[pos], heap[up_pos] = heap[up_pos], heap[pos]
		pos, up_pos = up_pos, (up_pos >> 1)

def pop_heap(heap):
	if len(heap) == 2:
		return heap.pop()
	elem = heap[1]
	heap[1] = heap.pop()
	pos = 1
	while True:
		min_idx = pos
		if pos*2 < len(heap) and heap[pos*2][0] < heap[min_idx][0]:
			min_idx = pos*2
		if pos*2+1 < len(heap) and heap[pos*2+1][0] < heap[min_idx][0]:
			min_idx = pos*2+1

		if min_idx != pos:
			heap[min_idx], heap[pos] = heap[pos], heap[min_idx]
			pos = min_idx
		else:
			break
	return elem

def valid_pos(row, col):
	return row >= 0 and row < h and col >= 0 and col < w

def get_neighbours_part1(d, row, col, dir, cnt):
	res = []
	for i in range(4):
		# Can't reverse direction and can't continue more than 3 steps in one direction
		if i^2 == dir or (i == dir and cnt == 2):
			continue
		new_row = row + next_cell[i][0]
		new_col = col + next_cell[i][1]
		if not valid_pos(new_row, new_col):
			continue

		new_cnt = cnt + 1 if i == dir else 0
		new_dist = d + grid[new_row][new_col]
		res.append((new_dist, new_row, new_col, i, new_cnt))
	return res

def get_neighbours_part2(d, row, col, dir, cnt):
	res = []
	for i in range(4):
		# Can't reverse direction and can't continue more than 10 steps in one direction, but a minimum
		# of 4. Counting from 0 that is 0-6 (7 states)
		if i^2 == dir or (i == dir and cnt == 6):
			continue
		# Add 1 step in the same direction
		if i == dir:
			new_row = row + next_cell[i][0]
			new_col = col + next_cell[i][1]
			if not valid_pos(new_row, new_col):
				continue

			new_cnt = cnt + 1
			new_dist = d + grid[new_row][new_col]
		# Otherwise start from 4 steps
		else:
			new_row = row + next_cell[i][0]*4
			new_col = col + next_cell[i][1]*4
			if not valid_pos(new_row, new_col):
				continue

			new_cnt = 0
			new_dist = d
			for j in range(1, 5):
				new_dist += grid[row + next_cell[i][0]*j][col + next_cell[i][1]*j]
		res.append((new_dist, new_row, new_col, i, new_cnt))
	return res

def solve(part):
	inf = 2**31-1
	total_steps = 3 if part == 1 else 7
	# The distance is a 4d array with dimensions [row][col][last_direction][num_steps]
	dist = [[[[inf] * total_steps for _ in range(4)] for _ in range(w)] for _ in range(h)]
	# Any element set to true means that the shortest path to that node has been found
	visited = [[[[False] * total_steps for _ in range(4)] for _ in range(w)] for _ in range(h)]
	# The heap holds a tuple of (dist, (row, col), last_direction, number steps in that direction)
	heap = [(-1,)]

	result = -1
	# Put the initial position from (0, 0) and last direction such that it cannot be continued
	# Since we can't reverse, put the other edge too
	push_heap((0, 0, 0, LEFT, 0), heap)
	push_heap((0, 0, 0, UP, 0), heap)
	while True:
		d, row, col, dir, cnt = pop_heap(heap)

		if visited[row][col][dir][cnt] == False:
			visited[row][col][dir][cnt] = True
			if row == h-1 and col == w-1:
				result = d
				break

			if part == 1:
				next_nodes = get_neighbours_part1(d, row, col, dir, cnt)
			else:
				next_nodes = get_neighbours_part2(d, row, col, dir, cnt)

			for n in next_nodes:
				new_dist, new_row, new_col, new_dir, new_cnt = n
				if new_dist < dist[new_row][new_col][new_dir][new_cnt]:
					dist[new_row][new_col][new_dir][new_cnt] = new_dist
					push_heap(n, heap)

	return result

print(f'Part 1:', solve(part=1)) # 767
print(f'Part 2:', solve(part=2)) # 904
