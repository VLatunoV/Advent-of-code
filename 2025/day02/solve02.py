import os

input_file = os.path.join(os.path.dirname(__file__), 'input02.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

ranges = sorted([tuple(map(int, r.split('-'))) for r in ''.join(lines).split(',')])

def count_digits(x):
	ans = 0
	while x > 0:
		ans += 1
		x //= 10
	return ans

def is_invalid(x, part):
	num_digits = count_digits(x)
	for num_copies in range(2, 3 if part == 1 else num_digits+1):
		if num_digits % num_copies != 0:
			continue
		num_digits_in_group = num_digits // num_copies
		factor = 10 ** num_digits_in_group
		repeated = x % factor

		invalid = True
		for offset in range(1, num_copies):
			if (x // (factor**offset)) % factor != repeated:
				invalid = False
				break
		if invalid:
			return True
	return False

def solve(part):
	ans = 0
	for r in ranges:
		for num in range(r[0], r[1]+1):
			if is_invalid(num, part):
				ans += num
	return ans

print('Part 1:', solve(part=1)) # 15873079081
print('Part 2:', solve(part=2)) # 22617871034
