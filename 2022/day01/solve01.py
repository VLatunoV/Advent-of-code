import os

input_file = os.path.join(os.path.dirname(__file__), 'input01.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

def get_calories():
	calories = [0]
	for l in lines:
		if l == '':
			calories.append(0)
		else:
			calories[-1] += int(l)
	return calories

def solve_part1():
	return max(get_calories())

def solve_part2():
	return sum(sorted(get_calories())[-3:])

print('Part 1:', solve_part1()) # 69501
print('Part 2:', solve_part2()) # 202346
