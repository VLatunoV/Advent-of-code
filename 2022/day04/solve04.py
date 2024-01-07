import os

input_file = os.path.join(os.path.dirname(__file__), 'input04.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

ranges = [None] * len(lines)
for i in range(len(lines)):
	l = lines[i]
	x, y = l.split(',')
	x1, x2 = map(int, x.split('-'))
	y1, y2 = map(int, y.split('-'))
	ranges[i] = ((x1, x2), (y1, y2))

def intersect(x, y):
	return (max(x[0], y[0]), min(x[1], y[1]))

def is_fully_contained(x, y):
	i = intersect(x, y)
	return x == i or y == i

def has_overlap(x, y):
	i = intersect(x, y)
	return i[0] <= i[1]

def solve_part1():
	return sum([1 for r in ranges if is_fully_contained(r[0], r[1])])

def solve_part2():
	return sum([1 for r in ranges if has_overlap(r[0], r[1])])

print('Part 1:', solve_part1()) # 503
print('Part 2:', solve_part2()) # 827
