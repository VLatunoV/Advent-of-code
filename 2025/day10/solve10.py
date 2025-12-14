import os
from math import gcd

input_file = os.path.join(os.path.dirname(__file__), 'input10.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

inf = 999999
num_lights = [None] * len(lines)
lights = [None] * len(lines)
switch_values = [None] * len(lines)
switches = [None] * len(lines)
jolts = [None] * len(lines)

def parse_light(light):
	light = light[1:-1]
	result = 0
	n = len(light)
	for i in range(n):
		if light[i] == '#':
			result |= 1 << i
	return result, n

def parse_switch(switch):
	result = list(map(int, switch[1:-1].split(',')))
	return result

def parse_jolts(jolt):
	result = tuple(map(int, jolt[1:-1].split(',')))
	return result

for idx in range(len(lines)):
	elems = lines[idx].split()
	lights[idx], num_lights[idx] = parse_light(elems[0])
	switches[idx] = [parse_switch(x) for x in elems[1:-1]]
	switch_values[idx] = [sum([1 << x for x in s]) for s in switches[idx]]
	jolts[idx] = parse_jolts(elems[-1])

######################################################################
# Part 1

def solve_lights(initial_light, num_lights, switches):
	num_switches = len(switches)
	max_light = 1 << num_lights
	dp = [[inf] * max_light for _ in range(num_switches+1)]
	dp[0][initial_light] = 0
	for s in range(num_switches):
		for l in range(max_light):
			new_light = l ^ switches[s]
			dp[s+1][l] = min(dp[s][l], dp[s][new_light] + 1)
	return dp[num_switches][0]

def solve_part1():
	ans = 0
	for idx in range(len(lines)):
		ans += solve_lights(lights[idx], num_lights[idx], switch_values[idx])
	return ans

######################################################################
# Part 2

def swap_rows(mat, r1, r2):
	if r1 == r2:
		return
	mat[r1], mat[r2] = mat[r2], mat[r1]

def swap_cols(mat, max_values, c1, c2):
	if c1 == c2:
		return
	for r in range(len(mat)):
		mat[r][c1], mat[r][c2] = mat[r][c2], mat[r][c1]
	max_values[c1], max_values[c2] = max_values[c2], max_values[c1]

def normalize_row(mat, r):
	mult = gcd(*mat[r]) * (-1 if mat[r][r] < 0 else 1)
	if mult == 1 or mult == 0:
		return
	for c in range(len(mat[r])):
		mat[r][c] //= mult

def add_row(mat, r_src, r_dst, mult):
	if mult == 0:
		return
	for c in range(len(mat[r_dst])):
		mat[r_dst][c] += mat[r_src][c]*mult

def ensure_diag_elem(mat, diag, max_values):
	if mat[diag][diag] != 1:
		new_diag = diag
		for r in range(diag+1, len(mat)):
			if mat[r][diag] != 0:
				if mat[new_diag][diag] == 0 or (abs(mat[r][diag]) < abs(mat[new_diag][diag])):
					new_diag = r
			if abs(mat[new_diag][diag]) == 1:
				break
		swap_rows(mat, diag, new_diag)
		if mat[diag][diag] == 0:
			for c in range(diag+1, len(mat[diag])-1):
				if mat[diag][c] != 0:
					swap_cols(mat, max_values, diag, c)
					break

def solve_jolts(jolts, switches):
	# Create matrix
	rows = len(jolts)
	cols = len(switches)
	mat = [[0] * (cols+1) for _ in range(rows)]
	for r in range(rows):
		for diag in range(cols):
			mat[r][diag] = 1 if r in switches[diag] else 0
		mat[r][-1] = jolts[r]

	# Max values for each variable. These are the limits to which we have to search for a solution
	max_values = [inf] * cols
	for r in range(rows):
		for c in range(cols):
			if mat[r][c] == 1:
				max_values[c] = min(max_values[c], jolts[r])

	# Transform matrix to upper triangle form
	free_vars = []
	for diag in range(min(rows, cols)):
		ensure_diag_elem(mat, diag, max_values)
		if mat[diag][diag] == 0:
			free_vars.append(diag)
		else:
			for r in range(diag+1, rows):
				while mat[r][diag] != 0:
					add_row(mat, diag, r, -mat[r][diag]//mat[diag][diag])
					if mat[r][diag] != 0:
						swap_rows(mat, r, diag)

	# Clear above diagonal for elements that can be cleared
	for diag in range(min(rows, cols)-1, -1, -1):
		normalize_row(mat, diag)
		if mat[diag][diag] != 1:
			continue
		for r in range(diag-1, -1, -1):
			if mat[r][diag] != 0:
				add_row(mat, diag, r, -mat[r][diag]//mat[diag][diag])

	# Add missing free variables if cols > rows
	for col in range(min(rows, cols), cols):
		free_vars.append(col)

	# If no free variables, matrix is solved
	if len(free_vars) == 0:
		return sum([mat[r][-1] for r in range(rows)])

	# Divide the variables into fixed (solved), unsolved and free
	# For given values for the free variables, the unsolved can be solved and the fixed don't change
	unsolved = []
	fixed_total = 0
	for diag in range(min(rows, cols)):
		if mat[diag][diag] != 0:
			solved = True
			for c in range(diag+1, cols):
				if mat[diag][c] != 0:
					solved = False
					break
			if not solved:
				unsolved.append(diag)
			else:
				fixed_total += mat[diag][-1]

	unsolved = list(reversed(unsolved))
	return fixed_total + search_solution(mat, free_vars, unsolved, max_values)

def search_solution(mat, free_vars, unsolved, max_values):
	cols = len(mat[0])-1
	vars = [0] * cols
	def is_feasable(idx):
		if idx == len(free_vars):
			for v in unsolved:
				x = mat[v][-1]
				for col in range(v+1, cols):
					x -= mat[v][col]*vars[col]
				if x < 0 or x % mat[v][v] != 0:
					return None
				vars[v] = x // mat[v][v]
			return sum(vars)

		best_ans = None
		for value in range(max_values[free_vars[idx]]+1):
			vars[free_vars[idx]] = value
			inner = is_feasable(idx+1)
			if inner is not None and (best_ans is None or inner < best_ans):
				best_ans = inner
		return best_ans

	return is_feasable(0)

def solve_part2():
	ans = 0
	for idx in range(len(jolts)):
		inner = solve_jolts(jolts[idx], switches[idx])
		ans += inner
		# print(f'Solved {idx+1}/{len(jolts)} -> {inner}')
	return ans

print('Part 1:', solve_part1()) # 425
print('Part 2:', solve_part2()) # 15883
