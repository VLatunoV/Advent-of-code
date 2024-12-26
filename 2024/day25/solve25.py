import os

input_file = os.path.join(os.path.dirname(__file__), 'input25.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

schematics = [lines[i*8:(i+1)*8-1] for i in range((len(lines)+7)//8)]
keys = []
locks = []

for s in schematics:
	if s[0] == '#'*5:
		pins = []
		for c in range(5):
			for r in range(5, -1, -1):
				if s[r][c] == '#':
					pins.append(r)
					break

		locks.append(tuple(pins))
	else:
		pins = []
		for c in range(5):
			for r in range(1, len(s)):
				if s[r][c] == '#':
					pins.append(6-r)
					break
		keys.append(pins)

def solve_part1():
	ans = 0
	for l in locks:
		for k in keys:
			if all([l[i]+k[i] <= 5 for i in range(5)]):
				ans += 1
	return ans

print('Part 1:', solve_part1())
