import os

input_file = os.path.join(os.path.dirname(__file__), 'input20.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

for r in range(len(lines)):
	s_idx = lines[r].find('S')
	if s_idx != -1:
		rs = r
		cs = s_idx
	e_idx = lines[r].find('E')
	if e_idx != -1:
		re = r
		ce = e_idx

def solve(search_range):
	dist = [[-1]*len(lines[0]) for _ in range(len(lines))]
	dist[rs][cs] = 0
	front = [(rs, cs)]
	d = 0
	neighbour = [(1, 0), (-1, 0), (0, 1), (0, -1)]
	path = [(rs, cs)]
	while len(front) > 0:
		new_front = []
		d += 1
		for r, c in front:
			for rr, cc in neighbour:
				nr = r + rr
				nc = c + cc
				if lines[nr][nc] != '#' and dist[nr][nc] == -1:
					dist[nr][nc] = d
					new_front.append((nr, nc))
					path.append((nr, nc))

		front = new_front
	
	ans = 0
	for r, c in path:
		for rr in range(-search_range, search_range+1):
			remaining = search_range - abs(rr)
			for cc in range(-remaining, remaining+1):
				nr = r + rr
				nc = c + cc
				if nr>=0 and nr<len(lines) and nc>=0 and nc<len(lines[0]):
					if dist[nr][nc] != -1:
						saved = dist[nr][nc] - dist[r][c] - (abs(rr)+abs(cc))
						if saved >= 100:
							ans += 1

	return ans

print('Part 1:', solve(2))
print('Part 2:', solve(20))
