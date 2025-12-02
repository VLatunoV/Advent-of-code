import os

input_file = os.path.join(os.path.dirname(__file__), 'input01.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

offsets = [int(x[1:]) * (-1 if x[0] == 'L' else 1) for x in lines]

def solve_part1():
	ans = 0
	value = 50
	for off in offsets:
		value += off
		if value % 100 == 0:
			ans += 1
	return ans

def solve_part2():
	ans = 0
	value = 50
	for off in offsets:
		old_value = value
		value += off
		# Count number of 100s in the interval [l, r]
		l = min(old_value, value)
		r = max(old_value, value)
		l += (100 - l % 100) % 100
		r -= r % 100
		ans += 1 + (r-l)//100
		if value % 100 == 0:
			ans -= 1 # Over counting if l or r was a 100
	return ans

print('Part 1:', solve_part1()) # 1055
print('Part 2:', solve_part2()) # 6386
