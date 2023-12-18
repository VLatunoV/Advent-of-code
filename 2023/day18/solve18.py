import os

input_file = os.path.join(os.path.dirname(__file__), 'input18.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

lines = [x.split() for x in lines]

# Choosen so that posivite angles show an increase of the index
# The direction is equal to 90* times its index
RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3
dir_map = {'U': UP, 'R': RIGHT, 'D': DOWN, 'L': LEFT}
next_cell = [(0, 1), (-1, 0), (0, -1), (1, 0)]

num_lines = len(lines)
directions = [dir_map[x[0]] for x in lines]
distances = [int(x[1]) for x in lines]
colors = [x[2] for x in lines]

def decode_color(col):
	dir = -1
	match col[5]:
		case '0': dir = RIGHT
		case '1': dir = DOWN
		case '2': dir = LEFT
		case '3': dir = UP
		case _: raise ValueError()
	dist = 0
	for c in col[:5]:
		if c.isdigit():
			dist = (dist << 4) + (ord(c) - ord('0'))
		else:
			dist = (dist << 4) + (ord(c) - ord('a') + 10)
	return dir, dist

# Get the turn that is made on the 'idx' move. (1 = CCW, -1 = CW)
def get_turn_value(idx):
	turn = directions[idx] - directions[idx-1]
	if turn > 1: turn -= 4
	if turn < -1: turn += 4
	return turn

def get_area(p1, p2):
	return p1[0]*p2[1] - p1[1]*p2[0]

def solve_part1():
	# First orient the line. Since the lines make a closed loop by the end there should
	# be 1 full rotation (either 4 or -4)
	orientation = sum([get_turn_value(i) for i in range(num_lines)]) // 4

	# Now create the outline of the region and at the same time compute the area. The given lengths
	# are the distances from the center of the cell to the center of the next corner. Expand each line
	# by 2, 0 or -2 *(1/2) for each of its corners, depending on which side is the inside and which
	# direction the corner turns
	for i in range(num_lines):
		# If the inside is on the right side (orientation == -1) and the line makes two right turns going in and out
		# of that line, then the result is (-1 + -1) / 2 * (-1) = 1. It increases by one.
		distances[i] += ((get_turn_value(i) + get_turn_value((i+1)%num_lines)) // 2) * orientation

	# Finally, we can compute the area of the outline, which is the area of the dig.
	area = 0
	p2 = (next_cell[directions[0]][0] * distances[0], next_cell[directions[0]][1] * distances[0])
	for i in range(1, num_lines):
		p1 = p2
		p2 = (p1[0] + next_cell[directions[i]][0] * distances[i], p1[1] + next_cell[directions[i]][1] * distances[i])
		area += get_area(p1, p2) * orientation
	return area // 2

def solve_part2():
	new_input = [decode_color(c[2:2+6]) for c in colors]

	global directions
	global distances
	directions = [x[0] for x in new_input]
	distances = [x[1] for x in new_input]
	return solve_part1()

print(f'Part 1:', solve_part1()) # 53300
print(f'Part 2:', solve_part2()) # 64294334780659
