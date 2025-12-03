import os

input_file = os.path.join(os.path.dirname(__file__), 'input03.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

max_n = 12
factors = [10 ** i for i in range(max_n + 1)]

def find_joltage_dp(line, state, start_idx, taken, digits):
	if taken == digits:
		return 0
	if state[start_idx][taken] != -1:
		return state[start_idx][taken]
	
	remaining = digits - taken
	assert remaining > 0

	ans = 0
	for i in range(start_idx, len(line) - (remaining-1)):
		ans = max(ans, int(line[i]) * factors[remaining-1] + find_joltage_dp(line, state, i+1, taken+1, digits))

	state[start_idx][taken] = ans
	return ans

def find_joltage(line, digits):
	mem = [[-1] * digits for _ in range(len(line))]
	return find_joltage_dp(line, mem, 0, 0, digits)

def solve(part):
	ans = 0
	for l in lines:
		ans += find_joltage(l, 2 if part==1 else 12)
	return ans

print('Part 1:', solve(part=1)) # 17311
print('Part 2:', solve(part=2)) # 171419245422055
