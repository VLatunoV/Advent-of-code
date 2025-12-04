import os

input_file = os.path.join(os.path.dirname(__file__), 'input04.txt')
with open(input_file) as f:
	lines = f.read().splitlines()
	lines = [[x for x in l] for l in lines]

def remove_layer():
	ans = 0
	active = [[False] * len(lines[r]) for r in range(len(lines))]
	for r in range(len(lines)):
		for c in range(len(lines[r])):
			if lines[r][c] != '@':
				continue
			active[r][c] = True
			neighbors = 0
			for rr in range(-1, 2):
				nr = r + rr
				if nr < 0 or nr >= len(lines):
					continue
				for cc in range(-1, 2):
					nc = c + cc
					if nc < 0 or nc >= len(lines[nr]):
						continue
					if rr == 0 and cc == 0:
						continue
					if lines[nr][nc] == '@' or active[nr][nc]:
						neighbors += 1
			if neighbors < 4:
				ans += 1
				lines[r][c] = '.'
	return ans

def solve():
	v = remove_layer()
	part1, part2 = v, 0
	while v > 0:
		part2 += v
		v = remove_layer()
	return part1, part2

p1, p2 = solve()
print('Part 1:', p1) # 1626
print('Part 2:', p2) # 9173
