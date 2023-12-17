import os

input_file = os.path.join(os.path.dirname(__file__), 'input12.txt')
with open(input_file) as f:
	lines = f.read().splitlines()
	lines = [x.split() for x in lines]

records = [x[0] for x in lines]
counts = [[int(x) for x in y[1].split(',')] for y in lines]

# This tells me how many # can i have starting from each index
consecutive = None

def make_consecutive_cache():
	global consecutive
	consecutive = [[0] * len(x) for x in records]
	for x, y in zip(records, consecutive):
		y[-1] = 0 if x[-1] == '.' else 1
		for i in range(len(x)-2, -1, -1):
			y[i] = 0 if x[i] == '.' else y[i+1] + 1

def find_ways(i, record_idx, count_idx, dyn):
	r = records[i]
	c = counts[i]
	# We reached the end of the record or the counts
	if count_idx == len(c):
		return 1 if r[record_idx:].count('#') == 0 else 0
	if record_idx >= len(r):
		return 0

	# If we have seen this result already, return it
	if dyn[record_idx][count_idx] != -1:
		return dyn[record_idx][count_idx]

	# Minimum space needed if we pack the remaining records as close as possible
	result = 0
	needed_space = sum(c[count_idx:]) + (len(c) - count_idx - 1)
	r_idx = record_idx
	while r_idx+needed_space <= len(r):
		# If possible to place the next count of springs
		if consecutive[i][r_idx] >= c[count_idx]:
			end_idx = r_idx + c[count_idx]
			# Check that if I place the next count of springs, the sequence can definitely be surrounded with '.'
			if (r_idx-1 == -1 or r[r_idx-1] != '#') and (end_idx == len(r) or r[end_idx] != '#'):
				result += find_ways(i, end_idx + 1, count_idx + 1, dyn)

		# If we see this, it is the first one we see for the current count. Then we know we have tried all
		# possibilities for it and we can exit
		if r[r_idx]=='#':
			break
		r_idx += 1

	dyn[record_idx][count_idx] = result
	return result

def solve_part1():
	make_consecutive_cache()
	result = 0
	for i in range(len(records)):
		state = [[-1] * len(counts[i]) for _ in range(len(records[i]))]
		result += find_ways(i, 0, 0, state)
	return result

def solve_part2():
	global records
	global counts

	records = ['?'.join([x]*5) for x in records]
	counts = [x*5 for x in counts]
	return solve_part1()

print(f'Part 1:', solve_part1()) # 7857
print(f'Part 2:', solve_part2()) # 28606137449920
