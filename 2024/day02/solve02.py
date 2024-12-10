import os

input_file = os.path.join(os.path.dirname(__file__), 'input02.txt')
with open(input_file) as f:
	lines = [[int(x) for x in y.split()] for y in f.read().splitlines()]

def is_report_safe(line):
	if len(line) < 2:
		return True

	if line[0] > line[1]:
		for i in range(1, len(line)):
			diff = line[i] - line[i-1]
			if diff > -1 or diff < -3:
				return False
		return True
	elif line[0] < line[1]:
		for i in range(1, len(line)):
			diff = line[i] - line[i-1]
			if diff > 3 or diff < 1:
				return False
		return True
	else:
		return False

def solve_part1():
	res = 0
	for l in lines:
		if is_report_safe(l):
			res += 1
	return res

def solve_part2():
	res = 0
	for l in lines:
		if is_report_safe(l):
			res += 1
		else:
			for i in range(len(l)):
				new_l = l[0:i] + l[i+1:]
				if (is_report_safe(new_l)):
					res += 1
					break
	return res

print('Part 1:', solve_part1())
print('Part 2:', solve_part2())
