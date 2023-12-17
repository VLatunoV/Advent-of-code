import os
from functools import reduce

input_file = os.path.join(os.path.dirname(__file__), 'input02.txt')
with open(input_file) as f:
	lines = f.readlines()

cubes = (12, 13, 14)
colors = ['red', 'green', 'blue']

# Check if all elements of one tuple are <= than the corresponding elements from another tuple
def tuple_leq(x, y):
	return all([xx <= yy for xx, yy in zip(x, y)])

# Return a tuple with each element being the maximal of the corresponding elements from the given tuples
def tuple_max(x, y):
	return tuple([max(xx, yy) for xx, yy in zip(x, y)])

def parse_handful(string):
	pairs = string.split(',')
	pairs = {col: int(num) for num, col in [x.strip().split() for x in pairs]}
	return tuple((pairs.get(key, 0) for key in colors))

def parse_line(l):
	game_id, game = l.split(":")
	game_id = int(game_id.split()[1])
	games = game.split(';')
	games = [parse_handful(x) for x in games]
	return game_id, games

def solve_part1():
	result = 0
	for l in lines:
		game_id, games = parse_line(l)
		if all([tuple_leq(x, cubes) for x in games]):
			result += game_id
	return result

def solve_line(l):
	_, games = parse_line(l)
	max_t = games[0]
	for g in games:
		max_t = tuple_max(max_t, g)
	return reduce(lambda x, y: x*y, max_t)

def solve_part2():
	return sum([solve_line(l) for l in lines])

print(f'Part 1: {solve_part1()}') # 2176
print(f'Part 2: {solve_part2()}') # 63700
