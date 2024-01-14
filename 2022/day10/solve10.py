import os
import pprint

input_file = os.path.join(os.path.dirname(__file__), 'input10.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

def solve_part1():
	result = 0
	x = 1
	cycle = 0
	to_add = 0
	for l in lines:
		l = l.split()
		x += to_add
		to_add = 0
		if len(l) == 1:
			cycle += 1
			if cycle in [20, 60, 100, 140, 180, 220]:
				result += x * cycle
		else:
			to_add = int(l[1])
			cycle += 1
			if cycle in [20, 60, 100, 140, 180, 220]:
				result += x * cycle
			cycle += 1
			if cycle in [20, 60, 100, 140, 180, 220]:
				result += x * cycle
	return result

def solve_part2():
	screen = [['.' for _ in range(40)] for _ in range(6)]
	def draw(p, cycle, screen):
		x = cycle % 40
		y = cycle // 40
		if abs(x - p) < 2:
			screen[y][x] = '#'
	x = 1
	cycle = 0
	to_add = 0
	for l in lines:
		l = l.split()
		x += to_add
		to_add = 0
		if len(l) == 1:
			draw(x, cycle, screen)
			cycle += 1
		else:
			to_add = int(l[1])
			draw(x, cycle, screen)
			cycle += 1
			draw(x, cycle, screen)
			cycle += 1
	screen = [''.join(q) for q in screen]
	return screen

print('Part 1:', solve_part1()) # 15260
print('Part 2:')
pprint.pprint(solve_part2()) # PGHFGLUG
