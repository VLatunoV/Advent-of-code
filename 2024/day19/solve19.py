import os

input_file = os.path.join(os.path.dirname(__file__), 'input19.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

towels = {}
for p in  [x.strip() for x in lines[0].split(',')]:
	l = towels.setdefault(p[0], [])
	l.append(p)

patterns = lines[2:]

def can_make(p, dyn):
	if dyn[len(p)] != -1:
		return dyn[len(p)]
	res = 0
	for t in towels[p[0]]:
		if t == p[:len(t)]:
			res += can_make(p[len(t):], dyn)
	dyn[len(p)] = res
	return res

def solve():
	p1, p2 = (0, 0)
	for p in patterns:
		dyn = [-1] * (len(p)+1)
		dyn[0] = 1
		ways = can_make(p, dyn)
		if ways > 0:
			p1 += 1
			p2 += ways
	return p1, p2

p1, p2 = solve()
print('Part 1:', p1)
print('Part 2:', p2)
