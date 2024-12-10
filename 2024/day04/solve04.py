import os

input_file = os.path.join(os.path.dirname(__file__), 'input04.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

xmas = 'XMAS'
def count_xmas_one_direction(row, col, r_off, c_off):
	for i in range(len(xmas)):
		if row < 0 or row >= len(lines):
			return 0
		if col < 0 or col >= len(lines[0]):
			return 0
		if lines[row][col] != xmas[i]:
			return 0
		row += r_off
		col += c_off
	return 1

def solve_part1():
	ans = 0
	for r in range(len(lines)):
		for c in range(len(lines[0])):
			for rr in range(-1, 2):
				for cc in range(-1, 2):
					if rr != 0 or cc != 0:
						ans += count_xmas_one_direction(r, c, rr, cc)
	return ans

def is_x_mas(row, col):
	if row < 1 or row >= len(lines)-1:
		return False
	if col < 1 or col >= len(lines[0])-1:
		return False
	if lines[row][col] != 'A':
		return False
	is_m = [lines[row+r][col+c]=='M' for r in [-1, 1] for c in [-1, 1]]
	is_s = [lines[row+r][col+c]=='S' for r in [-1, 1] for c in [-1, 1]]
	# 0 and 3 are on one diag, 1 and 2 on the other
	return (is_m[0]^is_m[3]) and (is_m[1]^is_m[2]) and (is_s[0]^is_s[3]) and (is_s[1]^is_s[2])

def solve_part2():
	ans = 0
	for r in range(len(lines)):
		for c in range(len(lines[0])):
			if is_x_mas(r, c):
				ans += 1
	return ans

print('Part 1:', solve_part1())
print('Part 2:', solve_part2())
