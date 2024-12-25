import os

input_file = os.path.join(os.path.dirname(__file__), 'input22.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

mod = 16777216 - 1
numbers = [int(x) for x in lines]

def next_num(x):
	x ^= (x << 6)
	x &= mod
	x ^= (x >> 5)
	x ^= (x << 11)
	return x & mod

def solve_part1():
	ans = 0
	for n in numbers:
		for _ in range(2000):
			n = next_num(n)
		ans += n
	return ans

def solve_part2():
	changes = [[None]*2000 for _ in numbers]
	price = [[None]*2000 for _ in numbers]
	profit = [{} for _ in numbers]
	possible_seq = set()
	for i, n in enumerate(numbers):
		for j in range(2000):
			nn = next_num(n)
			p = nn%10
			changes[i][j] = p - (n%10)
			price[i][j] = p
			n = nn
			if j-3 >= 0:
				seq = tuple(changes[i][j-3:j+1])
				if seq not in profit[i]:
					profit[i][seq] = p
					possible_seq.add(seq)
	best = 0
	for seq in possible_seq:
		curr = 0
		for p in profit:
			curr += p.get(seq, 0)
		best = max(best, curr)
	return best

print('Part 1:', solve_part1())
print('Part 2:', solve_part2())
