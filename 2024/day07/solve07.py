import os

input_file = os.path.join(os.path.dirname(__file__), 'input07.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

def make_equation(line):
	res, operands = line.split(":")
	res = int(res)
	operands = list(map(int, operands.split()))
	return res, operands

equations = list(map(make_equation, lines))

def can_fix(equation):
	res, ops = equation
	for idx in range(2**len(ops)-1):
		total = ops[0]
		for i in range(1, len(ops)):
			if idx & (1 << (i-1)):
				total += ops[i]
			else:
				total *= ops[i]
		if total == res:
			return True
	return False

def solve_part1():
	ans = 0
	for e in equations:
		if can_fix(e):
			ans += e[0]
	return ans

def get_pow_10(x):
	res = 10
	while res <= x:
		res *= 10
	return res

def can_fix_2(result, operands, op_idx):
	op = operands[op_idx]
	if op_idx == 0:
		return result == op
	
	if result % op == 0 and can_fix_2(result // op, operands, op_idx-1):
		return True
	tens = get_pow_10(op)
	if (result-op)%tens == 0 and can_fix_2((result-op) // tens, operands, op_idx-1):
		return True
	if result - op > 0 and can_fix_2(result - op, operands, op_idx-1):
		return True
	
	return False

def solve_part2():
	ans = 0
	for res, ops in equations:
		if can_fix_2(res, ops, len(ops)-1):
			ans += res
	return ans

print('Part 1:', solve_part1())
print('Part 2:', solve_part2())
