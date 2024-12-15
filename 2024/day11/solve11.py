import os
import math

input_file = os.path.join(os.path.dirname(__file__), 'input11.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

stones = [int(x) for x in lines[0].split()]

def solve_part1():
	old_stones = [x for x in stones]
	for _ in range(25):
		new_stones = []
		for s in old_stones:
			if s == 0:
				new_stones.append(1)
			else:
				digits = math.floor(math.log10(s))+1
				if digits % 2 == 0:
					half = 10 ** (digits//2)
					s1 = s // half
					s2 = s - s1*half
					new_stones.append(s1)
					new_stones.append(s2)
				else:
					new_stones.append(s * 2024)
		old_stones = new_stones
	return len(old_stones)

def count_stones(stone, level, dyn):
	if level == 1:
		digits = 1 if stone==0 else math.floor(math.log10(stone))+1
		return 1 if digits%2 == 1 else 2
	table = dyn[level - 1]
	if stone in table:
		return table[stone]

	res = 0
	if stone == 0:
		res = count_stones(1, level-1, dyn)
	else:
		digits = math.floor(math.log10(stone))+1
		if digits % 2 == 0:
			half = 10 ** (digits//2)
			s1 = stone // half
			s2 = stone - s1*half
			res = count_stones(s1, level-1, dyn) + count_stones(s2, level-1, dyn)
		else:
			res = count_stones(stone*2024, level-1, dyn)
	table[stone] = res
	return res

def solve_part2():
	dyn = [{} for _ in range(75)]
	ans = 0
	for s in stones:
		ans += count_stones(s, 75, dyn)
	return ans

print('Part 1:', solve_part1())
print('Part 2:', solve_part2())
