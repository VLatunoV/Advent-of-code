import os

input_file = os.path.join(os.path.dirname(__file__), 'input09.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

moves = {
	'L': (0, -1),
	'R': (0, 1),
	'U': (1, 0),
	'D': (-1, 0)
}

def clamp(x, a = -1, b = 1):
	return max(a, min(b, x))

def solve(rope_len):
	rope = [(0,0)] * rope_len
	tail_positions = set([rope[-1]])
	for l in lines:
		direction, dist = l.split()
		dist = int(dist)
		m = moves[direction]
		for _ in range(dist):
			rope[0] = (rope[0][0] + m[0], rope[0][1] + m[1])
			for i in range(1, len(rope)):
				delta_row = rope[i-1][0] - rope[i][0]
				delta_col = rope[i-1][1] - rope[i][1]
				if abs(delta_row) > 1 or abs(delta_col) > 1:
					rope[i] = (rope[i][0] + clamp(delta_row), rope[i][1] + clamp(delta_col))
			tail_positions.add(rope[-1])
	return len(tail_positions)

print('Part 1:', solve(2)) # 5710
print('Part 2:', solve(10)) # 2259
