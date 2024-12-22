import os

input_file = os.path.join(os.path.dirname(__file__), 'input17.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

reg_a = int(lines[0].split()[-1])
reg_b = int(lines[1].split()[-1])
reg_c = int(lines[2].split()[-1])
program = [int(x) for x in lines[4].split()[-1].split(',')]

goal_val = sum([x << (3*i) for i,x in enumerate(program)])
total_bits = 3*len(program)
all_set = (1<<total_bits) - 1

def combo_op(x):
	if x < 4: return x
	if x == 4: return reg_a
	if x == 5: return reg_b
	if x == 6: return reg_c
	return None

def solve_part1():
	global reg_a, reg_b, reg_c
	ip = 0
	output = ''
	while ip < len(program):
		instr = program[ip]
		match instr:
			case 0:
				reg_a = reg_a >> combo_op(program[ip+1])
			case 1:
				reg_b = reg_b ^ program[ip+1]
			case 2:
				reg_b = combo_op(program[ip+1]) & 7
			case 3:
				if reg_a == 0:
					ip += 2
				else:
					ip = program[ip+1]
			case 4:
				reg_b = reg_b ^ reg_c
			case 5:
				result = combo_op(program[ip+1]) & 7
				output = str(result) if output=='' else output+','+str(result)
			case 6:
				reg_b = reg_a >> combo_op(program[ip+1])
			case 7:
				reg_c = reg_a >> combo_op(program[ip+1])
		if instr != 3:
			ip += 2
	return output

def search_bits(curr_value, fixed_bits, idx):
	if idx >= len(program):
		return curr_value
	
	shft = idx*3
	target = (goal_val >> shft) & 7
	for candidate in range(8):
		x1 = candidate ^ 4
		x2 = target ^ x1 # x2 = target >> (t2t1!(t0))
		reverse_shift = candidate ^ 1
		active_bits = 7 & (7 << reverse_shift)
		# Check if the current bits we want to fix overlap, and if so, if they are the
		# same in the overlap area
		if (candidate & active_bits) != ((x2 << reverse_shift) & active_bits):
			continue

		candidate_fit = (candidate | (x2 << reverse_shift)) << shft
		candidate_mask = (7 | (7 << reverse_shift)) << shft
		active_bits = fixed_bits & candidate_mask
		# Check if the bits we want to fix are already fixed, and if so, if they are the same
		if (candidate_fit & active_bits) != (curr_value & active_bits):
			continue

		res = search_bits(curr_value | candidate_fit, fixed_bits | candidate_mask, idx+1)
		if res:
			return res

	return None

def solve_part2():
	return search_bits(0, 0, 0)

print('Part 1:', solve_part1())
print('Part 2:', solve_part2())
