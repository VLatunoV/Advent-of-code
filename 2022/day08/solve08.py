import os

input_file = os.path.join(os.path.dirname(__file__), 'input08.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

w, h = len(lines[0]), len(lines)

def solve_part1():
	visible = [[False] * w for _ in range(h)]
	for row in range(h):
		# Left to right
		l = lines[row]
		min_h = -1
		for col in range(w):
			height = int(l[col])
			if height > min_h:
				visible[row][col] = True
				min_h = height
		# Right to left
		min_h = -1
		for col in range(w-1, -1, -1):
			height = int(l[col])
			if height > min_h:
				visible[row][col] = True
				min_h = height
	for col in range(w):
		# Top to bottom
		min_h = -1
		for row in range(h):
			height = int(lines[row][col])
			if height > min_h:
				visible[row][col] = True
				min_h = height
		# Bottom to top
		min_h = -1
		for row in range(h-1, -1, -1):
			height = int(lines[row][col])
			if height > min_h:
				visible[row][col] = True
				min_h = height
	result = 0
	for row in range(h):
		for col in range(w):
			if visible[row][col]:
				result += 1
	return result

def scene_score(row, col):
	left, right, up, down = (0, 0, 0, 0)
	height = int(lines[row][col])
	# Left
	for c in range(col-1, -1, -1):
		left += 1
		if int(lines[row][c]) >= height:
			break
	# Right
	for c in range(col+1, w, 1):
		right += 1
		if int(lines[row][c]) >= height:
			break
	# Up
	for r in range(row-1, -1, -1):
		up += 1
		if int(lines[r][col]) >= height:
			break
	# Down
	for r in range(row+1, h, 1):
		down += 1
		if int(lines[r][col]) >= height:
			break
	return left * right * up * down

def solve_part2():
	result = 0
	for row in range(1, h-1):
		for col in range(1, w-1):
			result = max(result, scene_score(row, col))
	return result

print('Part 1:', solve_part1()) # 1812
print('Part 2:', solve_part2()) # 315495
