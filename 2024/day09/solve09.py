import os

input_file = os.path.join(os.path.dirname(__file__), 'input09.txt')
with open(input_file) as f:
	line = f.read()

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
	while left < right:
		if mem[left] != -1:
			print(f"adding {mem[left]}x{idx} = {mem[left]*idx}")
			ans += mem[left]*idx
		else:
			print(f'adding {mem[right]}x{idx} = {mem[right]*idx}')
			ans += mem[right]*idx
			right -=  1
			while mem[right] == -1:
				right -= 1
		left += 1
		idx += 1

	return ans

def solve_part2():
	pass

print('Part 1:', solve_part1())
print('Part 2:', solve_part2())
