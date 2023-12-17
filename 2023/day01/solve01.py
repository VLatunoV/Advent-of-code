import os

input_file = os.path.join(os.path.dirname(__file__), 'input01.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

mappings = {str(x): x for x in range(1, 10)}

def make_number(l):
	result = ''
	for i in range(len(l)):
		found = False
		for j in mappings.keys():
			if l[i:].startswith(j):
				result = str(mappings[j])
				found = True
				break
		if found:
			break
	for i in range(len(l)-1, -1, -1):
		found = False
		for j in mappings.keys():
			if l[i:].startswith(j):
				result += str(mappings[j])
				found = True
				break
		if found:
			break
	return int(result)

def solve_part1():
	return sum([make_number(l) for l in lines])

def solve_part2():
	mappings.update({
		'one': 1,
		'two': 2,
		'three': 3,
		'four': 4,
		'five': 5,
		'six': 6,
		'seven': 7,
		'eight': 8,
		'nine': 9,
	})
	return solve_part1()

print(f'Part 1:', solve_part1()) # 54990
print(f'Part 2:', solve_part2()) # 54473
