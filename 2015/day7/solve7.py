import os

input_file = os.path.join(os.path.dirname(__file__), 'input7.txt')
with open(input_file) as f:
	lines = [l.replace(' -> ', '-') for l in f.read().splitlines()]

operations = [(x.split(), y) for x, y in [x.split('-') for x in lines]]
label_map = {op[1]: idx for idx, op in enumerate(operations)}

dyn = {}

def get_input(label):
	if label[0].isdigit():
		return int(label)
	if label in dyn.keys():
		return dyn[label]

	result = -1
	op_idx = label_map[label]
	op = operations[op_idx][0]
	match len(op):
		case 1:
			if op[0].isdigit():
				result = int(op[0])
			else:
				result = get_input(op[0])
		case 2:
			if op[0].lower() == 'not':
				result = (~get_input(op[1])) & 0xFFFF
			else:
				raise ValueError()
		case 3:
			lhs = get_input(op[0])
			rhs = get_input(op[2])
			match op[1].lower():
				case 'or':
					result = lhs | rhs
				case 'and':
					result = lhs & rhs
				case 'rshift':
					result = lhs >> rhs
				case 'lshift':
					result = (lhs << rhs) & 0xFFFF
				case _:
					raise ValueError()

	assert result != -1
	dyn[label] = result
	return result

def solve_part1():
	return get_input('a')

def solve_part2():
	new_signal = get_input('a')
	global dyn
	dyn = {'b': new_signal}
	return get_input('a')

print(f'Part 1: {solve_part1()}') # 3176
print(f'Part 2: {solve_part2()}') # 14710
