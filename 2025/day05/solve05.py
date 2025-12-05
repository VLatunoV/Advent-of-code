import os

input_file = os.path.join(os.path.dirname(__file__), 'input05.txt')
with open(input_file) as f:
	lines = f.read().splitlines()
	ranges_index = lines.index('')
	mapper = lambda l, r: tuple([int(l), int(r)+1])
	intervals = [mapper(*x.split('-')) for x in lines[:ranges_index]]
	ids = list(map(int, lines[ranges_index+1:]))

def solve_part1():
	ans = 0
	for id in ids:
		for r in intervals:
			if id >= r[0] and id < r[1]:
				ans += 1
				break
	return ans

def solve_part2():
	ans = 0
	intervals.sort()

	l, r = intervals[0]
	for idx in range(1, len(intervals)):
		nl, nr = intervals[idx]
		if nl <= r:
			r = max(r, nr)
		else:
			ans += r - l
			l, r = intervals[idx]

	ans += r - l
	return ans

print('Part 1:', solve_part1()) # 868
print('Part 2:', solve_part2()) # 354143734113772
