import os

input_file = os.path.join(os.path.dirname(__file__), 'input06.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

def stupid_solve(size):
	for i in range(size, len(lines[0])):
		if len(list(set(lines[0][i-size:i]))) == size:
			return i
	return None

def solve_part1():
	return stupid_solve(4)

def solve_part2():
	return stupid_solve(14)

print('Part 1:', solve_part1()) # 1343
print('Part 2:', solve_part2()) # 2193
