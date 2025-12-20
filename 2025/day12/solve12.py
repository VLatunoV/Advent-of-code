import os

input_file = os.path.join(os.path.dirname(__file__), 'input12.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

class Region:
	def __init__(self, width, height, presents):
		self.width = width
		self.height = height
		self.presents = presents

def parse_region(l):
	dim, pres = l.split(":")
	w, h = list(map(int, dim.strip().split('x')))
	pres = list(map(int, pres.strip().split()))
	return Region(w, h, pres)

regions = []
presents = []
curr_present = []
for l in lines:
	if 'x' in l:
		regions.append(parse_region(l))
	elif l == '':
		presents.append(curr_present)
		curr_present = []
	elif ':' not in l:
		curr_present.append([x for x in l])

def generate_variations(p):
	def flip(p):
		return [list(reversed(x)) for x in p]
	def generate_rotations(p):
		def rotate(p):
			idx_map = [[(2,0), (1,0), (0,0)], [(2,1), (1,1), (0,1)], [(2,2), (1,2), (0,2)]]
			return [[p[y][x] for y,x in row] for row in idx_map]
		result = [p]
		for _ in range(3):
			result.append(rotate(result[-1]))
		return result

	result = [*generate_rotations(p), *generate_rotations(flip(p))]
	result = [
		tuple([sum(1<<idx for idx, val in enumerate(row) if val == '#')
			for row in var])
				for var in result
	]
	result = list(set(result))

	return result

presents = [generate_variations(p) for p in presents]

def calc_area(pres):
	return sum(map(int.bit_count, pres))

def solve_region(region: Region):
	total_fit = (region.width // 3) * (region.height // 3)
	if total_fit >= sum(region.presents):
		# print("Trivially fit all")
		return True

	required_area = sum([calc_area(presents[idx][0]) * amount for idx, amount in enumerate(region.presents)])
	if required_area > region.width * region.height:
		# print("Trivially can't fit")
		return False

	# The input is trolling me. All individual problems are trivially solved.
	print("Non-trivial input")
	# state = [bin(0) for _ in range(region.height)]
	# def search(row, remaining):
	# 	def fit_shape(shape, row):
	# 		for col in range(region.width - 2):
	# 			fit = True
	# 			for r in range(3):
	# 				if (shape[r] << col) & state[row+r] != 0:
	# 					fit = False
	# 					break
	# 			if fit:
	# 				return col
	# 		return -1

	# 	if sum(remaining) == 0:
	# 		return True

	# 	fit = False
	# 	for r in range(row, min(row+3, region.height)):
	# 		for idx, p in enumerate(remaining):
	# 			if p > 0:
	# 				for shape in presents[idx]:
	# 					col = fit_shape(shape, r)
	# 					if col != -1:
	# 						fit = True
	# 						# Modify state
	# 						for rr in range(3):
	# 							state[r+rr] |= (shape[r] << col)
	# 						remaining[idx] -= 1
	# 						if search(row, remaining):
	# 							return True
	# 						# Backtrack state
	# 						remaining[idx] += 1
	# 						for rr in range(3):
	# 							state[r+rr] ^= (shape[r] << col)
	# 	if fit == False:
	# 		return search(row+1, remaining)
	# 	else:
	# 		return False

	# return search(0, region.presents)

def solve_part1():
	ans = 0
	for r in regions:
		if solve_region(r):
			ans += 1
	return ans

print('Part 1:', solve_part1()) # 546
