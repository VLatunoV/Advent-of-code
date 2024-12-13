import os

input_file = os.path.join(os.path.dirname(__file__), 'input08.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

antennas = {}
for r in range(len(lines)):
	for c in range(len(lines[0])):
		if lines[r][c] != '.':
			ant = antennas.setdefault(lines[r][c], [])
			ant.append((r, c))

def check_in_bounds(p):
	return p[0] >= 0 and p[0] < len(lines) and p[1] >= 0 and p[1] < len(lines[0])

def solve_part1():
	antipodes = [[False]*len(lines[0]) for _ in range(len(lines))]
	for antenna in antennas.values():
		for i in range(len(antenna)):
			for j in range(i+1, len(antenna)):
				x = antenna[i]
				y = antenna[j]
				row_diff = x[0]-y[0]
				col_diff = x[1]-y[1]
				anti1 = (x[0] + row_diff, x[1] + col_diff)
				anti2 = (y[0] - row_diff, y[1] - col_diff)
				if check_in_bounds(anti1):
					antipodes[anti1[0]][anti1[1]] = True
				if check_in_bounds(anti2):
					antipodes[anti2[0]][anti2[1]] = True
	
	return sum(map(sum, antipodes))

def gcd(x, y):
	while y != 0:
		x, y = y, x%y
	return x

def solve_part2():
	antipodes = [[False]*len(lines[0]) for _ in range(len(lines))]
	for antenna in antennas.values():
		for i in range(len(antenna)):
			for j in range(i+1, len(antenna)):
				x = antenna[i]
				y = antenna[j]
				row_diff = x[0]-y[0]
				col_diff = x[1]-y[1]
				div = gcd(row_diff, col_diff)
				row_diff //= div
				col_diff //= div
				for dist in range(0, max(len(antipodes), len(antipodes[0]))):
					anti = (x[0] + row_diff*dist, x[1] + col_diff*dist)
					if check_in_bounds(anti):
						antipodes[anti[0]][anti[1]] = True
					else:
						break
				for dist in range(0, max(len(antipodes), len(antipodes[0]))):
					anti = (x[0] - row_diff*dist, x[1] - col_diff*dist)
					if check_in_bounds(anti):
						antipodes[anti[0]][anti[1]] = True
					else:
						break
	
	return sum(map(sum, antipodes))

print('Part 1:', solve_part1())
print('Part 2:', solve_part2())
