import os
from functools import reduce

input_file = os.path.join(os.path.dirname(__file__), 'input06.txt')
with open(input_file) as f:
	lines = f.read().splitlines()
	numbers = [list(map(int, x.split())) for x in lines[:-1]]
	ops = lines[-1].split()
	number_starts = [idx for idx in range(len(lines[-1])) if lines[-1][idx] != ' ']
	number_starts.append(len(lines[-1]) + 1)

def solve(get_numbers):
	ans = 0
	for col in range(len(numbers[0])):
		nums = get_numbers(col)
		match ops[col]:
			case '+':
				ans += reduce(lambda x,y: x+y, nums, 0)
			case '*':
				ans += reduce(lambda x,y: x*y, nums, 1)
	return ans

def solve_part1():
	def generate_numbers(col):
		return [numbers[i][col] for i in range(len(numbers))]

	return solve(generate_numbers)

def solve_part2():
	def generate_numbers(col):
		start_idx = number_starts[col]
		end_idx = number_starts[col+1] - 1
		result = []
		for c in range(start_idx, end_idx):
			current_number = 0
			for r in range(len(numbers)):
				digit = lines[r][c]
				if digit != ' ':
					current_number = current_number*10 + int(digit)
			result.append(current_number)
		return result

	return solve(generate_numbers)

print('Part 1:', solve_part1()) # 4364617236318
print('Part 2:', solve_part2()) # 9077004354241
