import os

input_file = os.path.join(os.path.dirname(__file__), 'input11.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

graph = {}
for l in lines:
	x, y = l.split(':')
	graph[x] = y.strip().split()

def solve_part1():
	start_node = 'you'
	end_node = 'out'
	dyn = {end_node: 1}
	def solve_node(node):
		nonlocal dyn
		if node in dyn:
			return dyn[node]

		ans = 0
		for next_node in graph[node]:
			ans += solve_node(next_node)
		dyn[node] = ans
		return ans

	return solve_node(start_node)

def solve_part2():
	start_node = 'svr'
	end_node = 'out'
	intermediate = ['fft', 'dac']
	dyn = {end_node: [1 if x==0 else 0 for x in range(1<<len(intermediate))]}
	def solve_node(node):
		nonlocal dyn
		if node in dyn:
			return dyn[node]

		ans = [0] * (1<<len(intermediate))
		for next_node in graph[node]:
			add = solve_node(next_node)
			for idx, val in enumerate(add):
				ans[idx] += val
		for bit, n in enumerate(intermediate):
			if node == n:
				for idx in range(len(ans)-1, -1, -1):
					if idx&(1<<bit) != 0:
						ans[idx] += ans[idx^(1<<bit)]
					else:
						ans[idx] = 0
				break
		dyn[node] = ans
		return ans

	return solve_node(start_node)[3]

print('Part 1:', solve_part1()) # 506
print('Part 2:', solve_part2()) # 385912350172800
