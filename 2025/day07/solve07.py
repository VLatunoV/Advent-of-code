import os

input_file = os.path.join(os.path.dirname(__file__), 'input07.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

def solve():
	start_idx = lines[0].index('S')
	current_layer = {start_idx: 1}
	splits = 0
	for i in range(2, len(lines), 2):
		next_layer = {}
		for beam, ways in current_layer.items():
			if lines[i][beam] == '^':
				next_layer[beam-1] = next_layer.get(beam-1, 0) + ways
				next_layer[beam+1] = next_layer.get(beam+1, 0) + ways
				splits += 1
			else:
				next_layer[beam] = next_layer.get(beam, 0) + ways
		current_layer = next_layer
	unique_paths = sum(current_layer.values())
	return splits, unique_paths

p1, p2 = solve()
print('Part 1:', p1) # 1537
print('Part 2:', p2) # 18818811755665
