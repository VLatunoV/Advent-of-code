import os

input_file = os.path.join(os.path.dirname(__file__), 'input9.txt')
with open(input_file) as f:
	lines = [[int(x) for x in l.split()] for l in f.read().splitlines()]

def make_difference(line):
	return [line[i+1] - line[i] for i in range(len(line)-1)]

def solve_line(line):
	diffs = [line]
	for _ in range(len(line)-1):
		diffs.append(make_difference(diffs[-1]))
	result = 0
	for d in diffs:
		result += d[-1]
	return result

def solve_part1():
	result = [solve_line(l) for l in lines]
	return sum(result)

def solve_line_2(line):
	diffs = [line]
	for _ in range(len(line)-1):
		diffs.append(make_difference(diffs[-1]))
	diffs = [list(reversed(d)) for d in diffs]
	result = 0
	for d in diffs:
		result = d[-1] - result
	return result

def solve_part2():
	result = [solve_line_2(l) for l in lines]
	return sum(result)

print(f'Part 1: {solve_part1()}') # 1980437560
print(f'Part 2: {solve_part2()}') # 977
