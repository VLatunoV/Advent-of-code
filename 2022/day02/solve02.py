import os

input_file = os.path.join(os.path.dirname(__file__), 'input02.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

games = [(ord(x) - ord('A'), ord(y) - ord('X')) for x, y in [l.split() for l in lines]]

def solve_part1():
	result = 0
	for x, y in games:
		result += 1 + y
		result += ((y-x+1) % 3) * 3
	return result

def solve_part2():
	result = 0
	for x, y in games:
		result += 1 + ((x - (1-y)) % 3)
		result += y * 3
	return result

print('Part 1:', solve_part1()) # 14297
print('Part 2:', solve_part2()) # 10498
