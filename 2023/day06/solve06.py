import os

input_file = os.path.join(os.path.dirname(__file__), 'input06.txt')
with open(input_file) as f:
	times = [int(x) for x in f.readline().split(':')[1].split()]
	distances = [int(x) for x in f.readline().split(':')[1].split()]

def calc_distance(hold_time, total_time):
	return hold_time*(total_time - hold_time)

def solve_part1():
	result = 1
	for index, time in enumerate(times):
		ways = 0
		for hold_time in range(1, time):
			if calc_distance(hold_time, time) > distances[index]:
				ways += 1
		result *= ways
	return result

print(f'Part 1:', solve_part1()) # 1108800

with open(input_file) as f:
	time = int(''.join(f.readline().split(':')[1].strip().split()))
	distance = int(''.join(f.readline().split(':')[1].strip().split()))

def solve_part2():
	# The maximum distance we can do is when we spend exactly half the time holding the button
	# After that, any amount more or less will give the same result, so we can only search for
	# hold long can we hold it after that (with binary search)
	left = time // 2
	right = time
	mid = 0
	best = 0
	while left <= right:
		mid = (left + right) // 2
		if calc_distance(mid, time) > distance:
			best = mid
			left = mid + 1
		else:
			right = mid - 1

	best_range = best - time//2
	# Add one for the center time (time//2)
	result = 1 + 2*best_range
	# Check the other side in case the time is odd
	if calc_distance(time // 2 - best_range - 1, time) > distance:
		result += 1
	if calc_distance(time // 2 - best_range + 1, time) <= distance:
		result -= 1
	return result

print(f'Part 2:', solve_part2()) # 36919753
