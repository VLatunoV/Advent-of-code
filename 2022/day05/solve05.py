import os

input_file = os.path.join(os.path.dirname(__file__), 'input05.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

empty_line = lines.index('')

def parse_crates():
	numbers = len(lines[empty_line-1].split())
	stacks = [[] for _ in range(numbers)]
	for i in range(empty_line-2, -1, -1):
		for j in range(numbers):
			if 1 + 4*j < len(lines[i]):
				crate = lines[i][1 + 4*j]
				if crate != ' ':
					stacks[j].append(crate)
	return stacks

def parse_moves():
	result = []
	for i in range(empty_line+1, len(lines), 1):
		l = lines[i].split()
		result.append((int(l[1]), int(l[3]), int(l[5])))
	return result

def solve_part1():
	stacks = parse_crates()
	moves = parse_moves()
	for cnt, src, dest in moves:
		src -= 1
		dest -= 1
		for _ in range(cnt):
			stacks[dest].append(stacks[src].pop())
	return ''.join([s[-1] for s in stacks if len(s) != 0])

def solve_part2():
	stacks = parse_crates()
	moves = parse_moves()
	for cnt, src, dest in moves:
		src -= 1
		dest -= 1
		stacks[dest].extend(stacks[src][-cnt:])
		stacks[src] = stacks[src][:-cnt]
	return ''.join([s[-1] for s in stacks if len(s) != 0])

print('Part 1:', solve_part1()) # QNNTGTPFN
print('Part 2:', solve_part2()) # GGNPJBTTR
