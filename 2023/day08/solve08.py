import os

input_file = os.path.join(os.path.dirname(__file__), 'input08.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

def parse_node(string):
	# Get only the name of the nodes
	return (string[0:3], (string[7:10], string[12:15]))

# Turn instruction letter L, R to 0, 1
instructions = [0 if x=='L' else 1 for x in lines[0]]

# Extract node names (the three letters) and their next nodes
nodes = [parse_node(x) for x in lines[2:]]

# Only the node names
node_names = [x[0] for x in nodes]

num_nodes = len(nodes)
num_instructions = len(instructions)

# Turn node names into numbers
name_to_id_map = {y: x for x, y in enumerate(node_names)}

# Same as 'nodes', but with numbers instead names
graph = [(name_to_id_map[y[0]], name_to_id_map[y[1]]) for _, y in nodes]


def solve_part1():
	current = name_to_id_map['AAA']
	target = name_to_id_map['ZZZ']
	steps = 0
	while current != target:
		current = graph[current][instructions[steps % len(instructions)]]
		steps += 1
	return steps

# Greatest common denominator of two numbers
# Example gcd(56 [2*2*2*7], 42 [2*3*7]) = 14 [2*7]
def gcd(x, y):
	while y != 0:
		x, y = y, x % y
	return x

# Least common multiplier of all numbers in the list
def lcm(numbers):
	result = 1
	for n in numbers:
		result = result * n // gcd(result, n)
	return result

def solve_part2():
	# This will tell use when we enter a cycle of nodes that repeats. A node is considered a specific name
	# on a specific step. So we cycle only if we are at the same on on the same step. That guarantees that
	# all next steps will be the same.
	seen_from = [[None] * num_instructions for _ in range(num_nodes)]
	cycle_lengths = []
	start_nodes = [name_to_id_map[x] for x in node_names if x[-1] == 'A']
	# Hopefully the solution is valid. In general it won't be, but the input is designed so that this should work. :D
	all_valid = True

	# From each starting node, find the cycle length
	for s in start_nodes:
		n = s # node
		i = 0 # instruction index
		step = 0 # total number of steps
		# list of nodes that end in 'Z' and how many steps have been taken to reach it from the start
		# Should be only 1, since the input is designed that way...
		end_nodes = []
		while True:
			if node_names[n][-1] == 'Z':
				# print(f"Found end node {node_names[n]}:{n}")
				end_nodes.append((step, n))

			if seen_from[n][i] is None:
				seen_from[n][i] = (s, step)
			else:
				# We see that we enter a cycle at 'step' (seen_from[n][i] was not None). The cycle length is that many steps, minus
				# the number of steps needed to reach it for the first time.
				cycle_length = step - seen_from[n][i][1]
				if seen_from[n][i][0] == s:
					# print(f"Node {n} seen again from starting node {s}")
					pass
				else:
					# This should never happen for our input
					# print(f"Node seen from a different start: Initially - {seen_from[n][i][0]}, Now - {s}")
					all_valid = False
				# print(f"Total steps: {step}, First seen steps: {seen_from[n][i][1]}")
				# print(f'Cycle: {cycle_length}')
				# print(f"All ends founds: {end_nodes}")
				# print('---------------------------------------------------------------------------------')

				# Should never happen
				if len(end_nodes) != 1 or end_nodes[0][0] != cycle_length:
					all_valid = False

				cycle_lengths.append(cycle_length)
				break

			# Take a step
			n = graph[n][instructions[i]]
			step += 1
			i += 1
			if i == num_instructions:
				i = 0

	return lcm(cycle_lengths)

print(f'Part 1: {solve_part1()}') # 12169
print(f'Part 2: {solve_part2()}') # 12030780859469
