import os

input_file = os.path.join(os.path.dirname(__file__), 'input01.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

list1 = []
list2 = []
for l in lines:
	x1, x2 = (int(x) for x in l.split())
	list1.append(x1)
	list2.append(x2)

list1.sort()
list2.sort()

def solve_part1():
	ans = 0
	for x1, x2 in zip(list1, list2):
		ans += abs(x1 - x2)
	return ans

def solve_part2():
	ans = 0
	right_numbers = {}
	for x in list2:
		if x not in right_numbers:
			right_numbers[x] = 0
		right_numbers[x] += 1
	for x in list1:
		ans += x * right_numbers.get(x, 0)
	return ans

print('Part 1:', solve_part1())
print('Part 2:', solve_part2())
