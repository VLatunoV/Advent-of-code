import os
import re

input_file = os.path.join(os.path.dirname(__file__), 'input03.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

def solve():
	pattern = "mul\([0-9]+,[0-9]+\)|do\(\)|don't\(\)"
	prog = re.compile(pattern)
	enabled_sum = 0
	disabled_sum = 0
	is_enabled = True
	for l in lines:
		string = l
		while True:
			result = prog.search(string)
			if result:
				substr = string[result.start() : result.end()]
				string = string[result.end():]
				if substr[0] == 'm':
					x, y = [int(x) for x in substr[4:-1].split(',')]
					if is_enabled:
						enabled_sum += x*y
					else:
						disabled_sum += x*y
				elif substr == 'do()':
					is_enabled = True
				else:
					is_enabled = False
			else:
				break
	disabled_sum += enabled_sum
	return disabled_sum, enabled_sum

p1, p2 = solve()

print('Part 1:', p1)
print('Part 2:', p2)
