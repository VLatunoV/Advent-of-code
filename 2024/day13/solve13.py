import os
import re

input_file = os.path.join(os.path.dirname(__file__), 'input13.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

def parse_bs(string):
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
	return a, b, prize

claws = [parse_bs(lines[i:i+4]) for i in range(0, len(lines), 4)]

def dot(x, y):
	return sum([x_i*y_i for x_i, y_i in zip(x, y)])
def mul(a, x):
	return tuple([x_i*a for x_i in x])
def add(x, y):
	return tuple([x_i+y_i for x_i, y_i in zip(x, y)])

def solve_part1():
	ans = 0
	for a, b, p in claws:
		a_orth = (-a[1], a[0])
		b_orth = (-b[1], b[0])
		a_div = dot(b_orth, a)
		b_div = dot(a_orth, b)
		a_weight = dot(b_orth, p) / a_div if a_div != 0 else 0
		b_weight = dot(a_orth, p) / b_div if b_div != 0 else 0
		a_weight_int = round(a_weight)
		b_weight_int = round(b_weight)
		if p == add(mul(a_weight_int, a), mul(b_weight_int, b)):
			ans += 3*a_weight_int + 1*b_weight_int
	return ans

def solve_part2():
	global claws
	claws = [(a, b, add((10000000000000, 10000000000000), p)) for a,b,p in claws]
	return solve_part1()

print('Part 1:', solve_part1())
print('Part 2:', solve_part2())
