import os
import re

input_file = os.path.join(os.path.dirname(__file__), 'input13.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

def parse_bs(string):
	print(string)
	def parse_vector(single_line):
		single_line = single_line.split(':')[1]
		x, y = single_line.split(',')
		prog = re.compile('[0-9]+$')
		m1 = prog.search(x)
		m2 = prog.search(y)
		res1 = x[m1.start():m1.end()]
		res2 = y[m2.start():m2.end()]
		return int(res1), int(res2)

	a = parse_vector(string[0])
	b = parse_vector(string[1])
	prize = parse_vector(string[2])
	print(a, b, prize)

claws = [parse_bs(lines[i:i+4]) for i in range(0, len(lines), 4)]

def solve_part1():
	pass

def solve_part2():
	pass

print('Part 1:', solve_part1())
print('Part 2:', solve_part2())
