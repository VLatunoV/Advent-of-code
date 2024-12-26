import os

input_file = os.path.join(os.path.dirname(__file__), 'input24.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

num_bits_input = 45
sep = lines.index('')
initial = lines[:sep]
rules = lines[sep+1:]
ops = {
	'AND': int.__and__,
	'OR': int.__or__,
	'XOR': int.__xor__
}

def parse_wire(x):
	wire, val = x.split(':')
	return (wire, int(val))

def parse_rule(x):
	w = x.split()
	if w[0] > w[2]:
		w[0], w[2] = w[2], w[0]
	return (w[0], w[2], w[4], ops[w[1]])

rules = sorted([parse_rule(x) for x in rules], key=lambda x: x[0])
initial = {k: v for k, v in [parse_wire(x) for x in initial]}

graph = {}
for idx, r in enumerate(rules):
	x, y, z, *_ = r
	graph.setdefault(x, []).append(idx)
	graph.setdefault(y, []).append(idx)

def simulate_wires(x_init = None, y_init = None, wires = None, swaps = None):
	rules_to_process = [idx for idx, v in enumerate(rules) if v[0][0] in ['x', 'y']]
	if wires is None:
		wires = {**initial}
	if x_init is not None:
		for i in range(num_bits_input):
			wires[f'x{i:02}'] = (x_init >> i) & 1
	if y_init is not None:
		for i in range(num_bits_input):
			wires[f'y{i:02}'] = (y_init >> i) & 1
	
	rules_visit_count = [0] * len(rules)
	while len(rules_to_process) > 0:
		new_rules = []
		for idx in rules_to_process:
			x, y, r, op = rules[idx]
			if swaps and r in swaps:
				r = swaps[r]
			wires[r] = op(wires[x], wires[y])
			for dep_rule in graph.get(r, []):
				rules_visit_count[dep_rule] += 1
				if rules_visit_count[dep_rule] == 2:
					new_rules.append(dep_rule)
		rules_to_process = new_rules
	
	return sum([(wires[f'z{i:02}'] << i) for i in range(num_bits_input+1)])

def solve_part1():
	return simulate_wires()

def solve_part2():
	potential_fixes = {}
	for idx in range(num_bits_input):
		for x in range(4):
			x_val = (x&1) << idx
			y_val = ((x>>1)&1) << idx
			wires = {**initial}
			res = simulate_wires(x_val, y_val, wires)
			exp = x_val + y_val
			if res != exp:
				for i in range(num_bits_input+1):
					if ((exp>>i) & 1) == 1 and ((res>>i)&1) == 0:
						potential_fixes.setdefault(f'z{i:02}', set()).update([k for k,v in wires.items() if v==1 and k[0] not in ['x','y']])
	
	# Merge potential fixes that have another potential fix in their list
	do_merge = True
	while do_merge:
		do_merge = False
		for k, v in potential_fixes.items():
			v.add(k)
			for p in v:
				if p == k:
					continue
				if p in potential_fixes:
					v.update(potential_fixes[p])
					del potential_fixes[p]
					do_merge = True
					break
			if do_merge:
				break

	assert len(potential_fixes) == 4
	potential_fixes = {k: list(v) for k,v in potential_fixes.items()}

	# Find swaps
	swaps = []
	for k, v in potential_fixes.items():
		test_idx = max(int(k[1:])-1, 0)
		all_good = True
		for i in range(len(v)):
			for j in range(i+1, len(v)):
				swap = {v[i]: v[j], v[j]: v[i]}
				all_good = True
				for x in range(1 << 6):
					x_val = ((x) & 7) << test_idx
					y_val = ((x>>3) & 7) << test_idx
					try:
						res = simulate_wires(x_val, y_val, swaps=swap)
					except KeyError:
						all_good = False
						break
					exp = x_val + y_val
					if res != exp:
						all_good = False
						break
				if all_good:
					break
			if all_good:
				swaps.extend((v[i], v[j]))
				break
	return ','.join(sorted(swaps))

print('Part 1:', solve_part1())
print('Part 2:', solve_part2())
