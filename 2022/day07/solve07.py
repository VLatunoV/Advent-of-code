import os

input_file = os.path.join(os.path.dirname(__file__), 'input07.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

def build_filesystem():
	result = {}
	current_dir_name = [None]
	current_dir_obj = [result]
	def mkdir(name):
		if name not in current_dir_obj[-1].keys():
			current_dir_obj[-1][name] = {}
	def cd(name):
		if name == '..':
			current_dir_name.pop()
			current_dir_obj.pop()
		else:
			current_dir_name.append(name)
			mkdir(name)
			current_dir_obj.append(current_dir_obj[-1][name])
	def touch(name, size):
		current_dir_obj[-1][name] = size

	for l in lines:
		cmd = l.split()
		if cmd[0] == '$':
			if cmd[1] == 'cd':
				cd(cmd[2])
		else:
			if cmd[0] == 'dir':
				mkdir(cmd[1])
			else:
				touch(cmd[1], int(cmd[0]))
	return result

def get_size(directory):
	result = 0
	for d in directory.values():
		if isinstance(d, int):
			result += d
		else:
			result += get_size(d)
	return result

def walk(fs, func):
	for f in fs.values():
		func(f)
		if isinstance(f, dict):
			walk(f, func)

fs = build_filesystem()

def solve_part1():
	global fs
	result = [0]
	def func(f, res):
		if isinstance(f, dict):
			size = get_size(f)
			if size < 100000:
				res[0] += size
	walk(fs['/'], lambda f: func(f, result))
	return result[0]

def solve_part2():
	global fs
	total_space = 70000000
	needed_space = 30000000
	result = [get_size(fs)]
	free_space = total_space - result[0]
	needed_space -= free_space
	def func(f, res, target):
		if isinstance(f, dict):
			size = get_size(f)
			if size > target:
				res[0] = min(res[0], size)
	walk(fs['/'], lambda f: func(f, result, needed_space))
	return result[0]

print('Part 1:', solve_part1()) # 1642503
print('Part 2:', solve_part2()) # 6999588
