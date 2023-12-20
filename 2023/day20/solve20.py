import os

input_file = os.path.join(os.path.dirname(__file__), 'input20.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

lines = list(sorted([l.replace('->', '=').replace(' ', '') for l in lines]))

def parse_module(line):
	name, connections = line.split('=')
	module_type = None
	broadcast = (name[0] == 'b')
	if broadcast == False:
		module_type = name[0]
		name = name[1:]
	connections = connections.split(',')
	return (name, module_type, connections)

all_modules = [parse_module(l) for l in lines]
# Map str -> [idx, visited:bool]
# A mapping from a module name to its new index. Initially this maps to the old index, but when
# we visit it, we change it, setting the flag to true
idx_map = {y[0]: [x, False] for x, y in enumerate(all_modules)}

# Rename modules to numbers, starting from the broadcaster
def rename_modules():
	# Next available index for modules
	next_idx = 0
	# Next index for modules that don't have any connections (there are such :( )
	next_last_idx = len(all_modules)
	# Start from the broadcaster module
	curr_modules = [all_modules[-1][0]]
	while len(curr_modules) != 0:
		next_modules = []
		for m in curr_modules:
			if m not in idx_map.keys():
				idx_map[m] = [next_last_idx, True]
				all_modules.append((m, '%', []))
				next_last_idx += 1
			if idx_map[m][1] == False:
				next_connections = idx_map[m][0]
				idx_map[m] = [next_idx, True]
				next_idx += 1
				next_modules += all_modules[next_connections][2]
		curr_modules = next_modules

rename_modules()

# Update the idx_map to store only the index. No need for the flag anymore
idx_map = {k: v[0] for k, v in idx_map.items()}
name_map = [x[1] for x in sorted([(v, k) for k, v in idx_map.items()])]
all_modules = sorted([(idx_map[x[0]], x[1], [idx_map[y] for y in x[2]]) for x in all_modules])
# Create the lists of module inputs. This is needed for the conjunction modules
module_inputs = [[] for _ in range(len(idx_map))]
for m in all_modules:
	for c in m[2]:
		module_inputs[c].append(m[0])

def solve(signal_state, conj_state):
	sig_cnt = [1, 0]
	curr_modules = [0]

	# Helper to change the module states after a signal was sent
	def send_signal(dest, src):
		emits = True
		if all_modules[dest][1] == '%':
			if signal_state[src] == 0:
				signal_state[dest] ^= 1
			else:
				emits = False
		else: # '&'
			old_signal = conj_state[dest][1][src]
			conj_state[dest][1][src] = signal_state[src]
			conj_state[dest][0] += signal_state[src] - old_signal
			signal_state[dest] = int(conj_state[dest][0] != len(conj_state[dest][1]))

		return emits

	while len(curr_modules) !=0:
		next_modules = []
		for m in curr_modules:
			for dest in all_modules[m][2]:
				if send_signal(dest, m):
					next_modules.append(dest)
			sig_cnt[signal_state[m]] += len(all_modules[m][2])
		curr_modules = next_modules

	return tuple(sig_cnt)

def solve_part1():
	l, h = 0, 0
	signal_state = [0] * len(all_modules)
	conj_state = [None] * len(all_modules)
	for m in all_modules:
		if m[1] == '&':
			conj_state[m[0]] = [0, {x: 0 for x in module_inputs[m[0]]}]
	for _ in range(1000):
		ll, hh = solve(signal_state, conj_state)
		l += ll
		h += hh
	return l * h

# Greatest common denominator of two numbers
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
	curr_module = [0]
	cycle_len = [0] * len(all_modules)
	while len(curr_module) != 0:
		next_modules = []
		for m in curr_module:
			for dest in all_modules[m][2]:
				if all_modules[dest][1] == '%':
					cycle_len[dest] = max(1, cycle_len[m]*2)
					next_modules.append(dest)
				else:
					cycle_len[dest] |= cycle_len[m]
		curr_module = next_modules

	def get_cycle(m):
		if cycle_len[m] != 0:
			return cycle_len[m]
		if len(module_inputs[m]) == 1:
			return get_cycle(module_inputs[m][0])
		return [get_cycle(x) for x in module_inputs[m]]

	return lcm(get_cycle(idx_map['rx']))

print(f'Part 1:', solve_part1()) # 680278040
print(f'Part 2:', solve_part2()) # 243548140870057
