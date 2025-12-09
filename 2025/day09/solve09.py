import os

input_file = os.path.join(os.path.dirname(__file__), 'input09.txt')
with open(input_file) as f:
	lines = f.read().splitlines()
	points = [tuple(map(int, x.split(','))) for x in lines]

def solve_part1():
	n = len(points)
	ans = 0
	for i in range(n):
		for j in range(i+1, n):
			width = max(points[i][0], points[j][0]) - min(points[i][0], points[j][0])
			height = max(points[i][1], points[j][1]) - min(points[i][1], points[j][1])
			area = (width+1)*(height+1)
			ans = max(ans, area)
	return ans

def solve_part2():
	# First create a reduction of the coordinates. There are <500 points, so that many unique coordinates
	# in each dimension
	# Important observation: Because each point connects to a next, they share one coordinate. So the number
	# of unique coordinates is even. I need at least one empty space between coordinates to be able to flood
	# fill the inside. So, I don't have to expand the coordinates after the reduction.
	n = len(points)
	x_coordinates = sorted([p[0] for p in points])
	y_coordinates = sorted([p[1] for p in points])
	x_map = {p[0]: x_coordinates.index(p[0]) for p in points}
	y_map = {p[1]: y_coordinates.index(p[1]) for p in points}
	reduced_points = [(x_map[p[0]], y_map[p[1]]) for p in points]

	# Place all tiles
	grid_width  = max(x_map.values()) - min(x_map.values()) + 1
	grid_height = max(y_map.values()) - min(y_map.values()) + 1
	grid = [['.'] * grid_width for _ in range(grid_height)]

	for i in range(n):
		next_i = (i+1) % n
		p1 = reduced_points[i]
		p2 = reduced_points[next_i]
		if p1[0] == p2[0]:
			for row in range(min(p1[1], p2[1]), max(p1[1], p2[1])+1):
				grid[row][p1[0]] = '#'
		else:
			for col in range(min(p1[0], p2[0]), max(p1[0], p2[0])+1):
				grid[p1[1]][col] = '#'

	# Flood fill inside
	idx1 = 0
	while reduced_points[idx1][0] != 0:
		idx1 += 1
	idx2 = (idx1+1) % n
	if reduced_points[idx2][0] != 0:
		idx2 = (idx1-1) % n

	neighbours = [(-1, 0), (0, 1), (1, 0), (0, -1)]
	flood_start = (
		reduced_points[idx1][0] + 1,
		reduced_points[idx2][1] + (reduced_points[idx1][1] - reduced_points[idx2][1])//2
	)
	curr_layer = [flood_start]
	grid[flood_start[1]][flood_start[0]] = '#'
	while len(curr_layer) != 0:
		next_layer = []
		for p in curr_layer:
			for off in neighbours:
				np = (p[0] + off[0], p[1] + off[1])
				if grid[np[1]][np[0]] == '.':
					grid[np[1]][np[0]] = '#'
					next_layer.append(np)
		curr_layer = next_layer

	# Check all pairs of corners (same as part1)
	def is_valid(i, j):
		lx = min(reduced_points[i][0], reduced_points[j][0])
		ly = min(reduced_points[i][1], reduced_points[j][1])
		rx = max(reduced_points[i][0], reduced_points[j][0])
		ry = max(reduced_points[i][1], reduced_points[j][1])
		for row in range(ly, ry+1):
			for col in range(lx, rx+1):
				if grid[row][col] != '#':
					return False
		return True

	ans = 0
	for i in range(n):
		for j in range(i+1, n):
			width  = abs(x_coordinates[reduced_points[i][0]] - x_coordinates[reduced_points[j][0]])
			height = abs(y_coordinates[reduced_points[i][1]] - y_coordinates[reduced_points[j][1]])
			area = (width+1)*(height+1)
			# First check if the area is actually larger. If not, no point in doing the n^2 check
			# to see if its valid
			if ans < area and is_valid(i, j):
				ans = area
	return ans

print('Part 1:', solve_part1()) # 4758598740
print('Part 2:', solve_part2()) # 1474699155
