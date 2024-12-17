import os

input_file = os.path.join(os.path.dirname(__file__), 'input12.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

def check_bounds(r, c):
	return r >= 0 and r < len(lines) and c >= 0 and c < len(lines[0])

def calc_price(r, c, visited):
	area = 0
	perimeter = 0
	garden_type = lines[r][c]

	visited[r][c] = True
	front = [(r, c)]
	neighbour = [(1,0), (-1,0), (0,1), (0,-1)]
	while len(front) > 0:
		new_front = []
		area += len(front)
		for r, c in front:
			for rr, cc in neighbour:
				nr = r + rr
				nc = c + cc
				if check_bounds(nr, nc) and lines[nr][nc] == garden_type:
					if not visited[nr][nc]:
						visited[nr][nc] = True
						new_front.append((nr, nc))
					perimeter -= 1
		front = new_front
	perimeter += 4*area
	return area * perimeter

def solve_part1():
	ans = 0
	visited = [[False] * len(lines[0]) for _ in range(len(lines))]

	for r in range(len(lines)):
		for c in range(len(lines[0])):
			if not visited[r][c]:
				ans += calc_price(r, c, visited)
	return ans

def solve_part2():
	ver_edge = [[0] * (len(lines[0])+1) for _ in range(len(lines))]
	hor_edge = [[0] * (len(lines[0])) for _ in range(len(lines)+1)]
	init_val = 7
	for r in range(len(lines)):
		ver_edge[r][0] = init_val
		ver_edge[r][-1] = init_val
	for c in range(len(lines)):
		hor_edge[0][c] = init_val
		hor_edge[-1][c] = init_val

	for r in range(len(lines)-1):
		for c in range(len(lines[0])-1):
			if lines[r][c] != lines[r+1][c]:
				hor_edge[r+1][c] = init_val
			if lines[r][c] != lines[r][c+1]:
				ver_edge[r][c+1] = init_val
		if lines[r][-1] != lines[r+1][-1]:
			hor_edge[r+1][-1] = init_val
	for c in range(len(lines[0])-1):
		if lines[-1][c] != lines[-1][c+1]:
			ver_edge[-1][c+1] = init_val

	edges = [hor_edge, ver_edge]

	# 0 = top edge, going left
	# 1 = left edge, going down
	# 2 = down edge, going right
	# 3 = right edge, going up
	neighbour = [(0, -1), (1, 0), (0, 1), (-1, 0)]
	def edge_idx(r, c, d):
		if d&1:
			return (r, c + d//2, 1)
		else:
			return (r + d//2, c, 0)
	def has_edge(r, c, d):
		r, c, i = edge_idx(r, c, d)
		return edges[i][r][c] & (1 << (d//2))
	def get_edge(r, c, d):
		r, c, i = edge_idx(r, c, d)
		return edges[i][r][c] & (1 << 2)
	def clear_edge(r, c, d):
		r, c, i = edge_idx(r, c, d)
		edges[i][r][c] &= ~(1 << (d//2))
	def follow_edge(r, c, d):
		if get_edge(r, c, (d+1)%4):
			return (r, c, (d+1)%4)
		r += neighbour[d][0]
		c += neighbour[d][1]
		if get_edge(r, c, d):
			return (r, c, d)
		d = (d-1)%4
		r += neighbour[d][0]
		c += neighbour[d][1]
		return (r, c, d)

	def walk(r, c, visited):
		area = 0
		perimeter = 0
		visited[r][c] = True
		garden_type = lines[r][c]
		front = [(r, c)]
		while len(front) > 0:
			area += len(front)
			new_front = []
			for r, c in front:
				for rr, cc in neighbour:
					nr = r + rr
					nc = c + cc
					if check_bounds(nr, nc) and lines[nr][nc] == garden_type and not visited[nr][nc]:
						visited[nr][nc] = True
						new_front.append((nr, nc))
				for d in range(4):
					if has_edge(r, c, d):
						current = last = r, c, d
						clear_edge(*current)
						next = follow_edge(r, c, d)
						while True:
							if next[2] != current[2]:
								perimeter += 1
							if next == last:
								break
							current, next = next, follow_edge(*next)
							clear_edge(*current)
			front = new_front
		return area, perimeter

	ans = 0
	visited = [[False] * len(lines[0]) for _ in range(len(lines))]
	for r in range(len(lines)):
		for c in range(len(lines[0])):
			if not visited[r][c]:
				area, per = walk(r, c, visited)
				ans += area*per

	return ans

print('Part 1:', solve_part1())
print('Part 2:', solve_part2())
