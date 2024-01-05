import os

input_file = os.path.join(os.path.dirname(__file__), 'input03.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

def prio(letter):
	if ord('A') <= ord(letter) <= ord('Z'):
		return 27 + ord(letter) - ord('A')
	else:
		return 1 + ord(letter) - ord('a')

def solve_part1():
	result = 0
	for pack in lines:
		l = len(pack) // 2
		left = set(pack[:l])
		right = set(pack[l:])
		result += prio(list(left.intersection(right))[0])
	return result

def solve_part2():
	result = 0
	for i in range(len(lines) // 3):
		s1 = set(lines[i*3 + 0])
		s2 = set(lines[i*3 + 1])
		s3 = set(lines[i*3 + 2])
		badge = s1.intersection(s2)
		badge = list(badge.intersection(s3))[0]
		result += prio(badge)
	return result

print('Part 1:', solve_part1()) # 8202
print('Part 2:', solve_part2()) # 2864
