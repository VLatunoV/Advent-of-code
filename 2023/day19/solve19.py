import os

input_file = os.path.join(os.path.dirname(__file__), 'input19.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

def parse_workflow(line):
	name, rest = line.split('{')
	rules = rest[:-1].split(',')
	result = []
	for r in rules:
		parts = r.split(':')
		if len(parts) == 1:
			result.append((None, None, None, parts[0]))
		else:
			condition, destination = parts
			prop = condition[0]
			operation = condition[1]
			value = int(condition[2:])
			result.append((prop, operation, value, destination))
	return (name, result)

def parse_part(line):
	return {x: int(y) for x, y in [x.split('=') for x in line[1:-1].split(',')]}

blank_line = lines.index('')
workflows = dict([parse_workflow(l) for l in lines[:blank_line]])
parts = [parse_part(l) for l in lines[blank_line+1:]]
workflows['A'] = True
workflows['R'] = False

def accepted_part1(part, workflow):
	while type(workflow) is not bool:
		for r in workflow:
			if r[1] is None:
				workflow = workflows[r[3]]
				break
			else:
				if (r[1] == '>' and part[r[0]] > r[2]) or (r[1] == '<' and part[r[0]] < r[2]):
					workflow = workflows[r[3]]
					break
	return workflow

def solve_part1():
	return sum([sum(p.values()) for p in parts if accepted_part1(p, workflows['in'])])

def part_value(part):
	result = 1
	for p in part.values():
		result *= (p[1] - p[0] + 1)
	return result

def accepted_part2(part, workflow):
	if type(workflow) == bool:
		return workflow * part_value(part)

	result = 0
	for r in workflow:
		if r[1] is None:
			result += accepted_part2(part, workflows[r[3]])
		else:
			if r[1] == '>' and part[r[0]][1] > r[2]:
				old_range = part[r[0]]
				new_part = {**part}
				new_part[r[0]] = [max(old_range[0], r[2]+1), old_range[1]]
				result += accepted_part2(new_part, workflows[r[3]])
				part[r[0]] = [old_range[0], min(old_range[1], r[2])]
			if r[1] == '<' and part[r[0]][0] < r[2]:
				old_range = part[r[0]]
				new_part = {**part}
				new_part[r[0]] = [old_range[0], min(old_range[1], r[2]-1)]
				result += accepted_part2(new_part, workflows[r[3]])
				part[r[0]] = [max(old_range[0], r[2]), old_range[1]]
			if part[r[0]][1] < part[r[0]][0]:
				break
	return result

def solve_part2():
	all_parts = {x: [1, 4000] for x in ['x', 'm', 'a', 's']}
	return accepted_part2(all_parts, workflows['in'])

print(f'Part 1:', solve_part1()) # 263678
print(f'Part 2:', solve_part2()) # 125455345557345
