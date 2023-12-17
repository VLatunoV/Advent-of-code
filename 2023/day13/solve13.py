import os

input_file = os.path.join(os.path.dirname(__file__), 'input13.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

patterns = [[]]
for l in lines:
	if l == '':
		patterns.append([])
	else:
		patterns[-1].append(l)

def get_row(pattern, i):
	return pattern[i]
def get_col(pattern, i):
	return ''.join([pattern[j][i] for j in range(len(pattern))])
def find_num_difference(p1, p2):
	return sum([int(x != y) for x, y in zip(p1, p2)])

def solve(part):
	result = 0
	for p in patterns:
		w, h = len(p[0]), len(p)
		for i in range(1, w):
			differences = 0
			for j in range(i):
				if i+j >= w or i-1-j < 0:
					break
				differences += find_num_difference(get_col(p, i+j), get_col(p, i-1-j))
			if differences == (part-1):
				result += i
				break

		for i in range(1, h):
			differences = 0
			for j in range(i):
				if i+j >= h or i-1-j < 0:
					break
				differences += find_num_difference(get_row(p, i+j), get_row(p, i-1-j))
			if differences == (part-1):
				result += i*100
				break
	return result

print(f'Part 1: {solve(part=1)}') # 31739
print(f'Part 2: {solve(part=2)}') # 31539
