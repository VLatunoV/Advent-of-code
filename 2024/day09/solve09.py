import os

input_file = os.path.join(os.path.dirname(__file__), 'input09.txt')
with open(input_file) as f:
	line = f.readline().split()[0]

def solve_part1():
	total_len = 0
	for c in line:
		total_len += int(c)
	mem = [-1] * total_len
	write_head = 0
	id = 0
	for i in range(len(line)):
		digit = int(line[i])
		if i%2 == 0:
			for _ in range(digit):
				mem[write_head] = id
				write_head += 1
			id += 1
		else:
			write_head += digit

	ans = 0
	left = 0
	right = total_len-1
	idx = 0
	while left <= right:
		if mem[left] != -1:
			ans += mem[left]*idx
		else:
			ans += mem[right]*idx
			right -=  1
			while mem[right] == -1:
				right -= 1
		left += 1
		idx += 1

	return ans

def solve_part2():
	files = []
	empty = []
	idx = 0
	for i, c in enumerate(line):
		l = int(c)
		if i % 2 == 0:
			files.append((idx, l, i//2))
		else:
			empty.append((idx, l))
		idx += l
	for fIdx in range(len(files)-1, -1, -1):
		f = files[fIdx]
		for eIdx, e in enumerate(empty):
			if f[0] < e[0]:
				break
			if e[1] >= f[1]:
				empty[eIdx] = (e[0]+f[1], e[1]-f[1])
				files[fIdx] = (e[0], f[1], f[2])
				if empty[eIdx][1] == 0:
					empty.pop(eIdx)
				break
	ans = 0
	for f in files:
		ans += f[2]*(f[0]*f[1] + f[1]*(f[1]-1)//2)
	return ans

print('Part 1:', solve_part1())
print('Part 2:', solve_part2())
