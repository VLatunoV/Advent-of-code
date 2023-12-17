import os

input_file = os.path.join(os.path.dirname(__file__), 'input15.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

input = lines[0].split(',')

def hash(string):
	result = 0
	for c in string:
		result = ((result + ord(c))*17) & 255
	return result

def solve_part1():
	return sum([hash(x) for x in input])

def solve_part2():
	boxes = [[] for _ in range(256)]
	lens_map = {}
	for x in input:
		label = None
		focus = None
		if x[-1] == '-':
			label = x[:-1]
			box = lens_map.pop(label, None)
			if box:
				for i in range(len(box)):
					if box[i][0] == label:
						box.pop(i)
						break
		else:
			label = x[:-2]
			focus = int(x[-1])
			box = boxes[hash(label)]
			has_lens = label in lens_map.keys()
			if has_lens:
				for i in range(len(box)):
					if box[i][0] == label:
						box[i] = (label, focus)
						break
			else:
				box.append((label, focus))
				lens_map[label] = box

	result = 0
	for i in range(len(boxes)):
		for j in range(len(boxes[i])):
			result += (i+1) * (j+1) * boxes[i][j][1]
	return result

print(f'Part 1:', solve_part1()) # 511343
print(f'Part 2:', solve_part2()) # 294474
