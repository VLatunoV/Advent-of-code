import os

input_file = os.path.join(os.path.dirname(__file__), 'input22.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

min_coord = [int(2**31 - 1)] * 3
max_coord = [-int(2**31)] * 3

def parse_brick(line):
	global min_coord
	global max_coord

	start, end = line.split('~')
	a,b,c = tuple(map(int, start.split(',')))
	x,y,z = tuple(map(int, end.split(',')))
	if a > x: a, x = x, a
	if b > y: b, y = y, b
	if c > z: c, z = z, c
	min_coord = list(map(min, zip(min_coord, (a,b,c))))
	max_coord = list(map(max, zip(max_coord, (x,y,z))))
	orientation = (1, 0, 0)
	length = x - a
	if b != y:
		orientation = (0, 1, 0)
		length = y - b
	if c != z:
		orientation = (0, 0, 1)
		length = z - c
	return [[a,b,c], [x,y,z], orientation, length + 1]

bricks = sorted([parse_brick(x) for x in lines], key=lambda x: x[0][2])

def solve():
	# Keeps track of which voxel holds which brick index
	volume = [[[-1] * (max_coord[2]+1) for _ in range(max_coord[1]+1)] for _ in range(max_coord[0]+1)]
	for i, b in enumerate(bricks):
		for j in range(b[3]):
			x = b[0][0] + j*b[2][0]
			y = b[0][1] + j*b[2][1]
			z = b[0][2] + j*b[2][2]
			volume[x][y][z] = i

	can_move = [True] * len(bricks)
	moveable = len(bricks)
	while moveable != 0:
		# Check which bricks are moveable down
		for i, b in enumerate(bricks):
			if can_move[i] == False:
				continue
			for j in range(b[3]):
				x = b[0][0] + j*b[2][0]
				y = b[0][1] + j*b[2][1]
				z = b[0][2] + j*b[2][2]
				if z == 1 or (volume[x][y][z-1] != -1 and can_move[volume[x][y][z-1]] == False):
					can_move[i] = False
					moveable -= 1
					break
		# For each moveable brick, move it down by 1
		for i, b in enumerate(bricks):
			if can_move[i]:
				for j in range(b[3]):
					x = b[0][0] + j*b[2][0]
					y = b[0][1] + j*b[2][1]
					z = b[0][2] + j*b[2][2]
					volume[x][y][z-1] = volume[x][y][z]
					volume[x][y][z] = -1
				b[0][2] -= 1
				b[1][2] -= 1
	# Build a graph of supports
	supports = [set() for _ in range(len(bricks))]
	supported_by = [set() for _ in range(len(bricks))]
	for i, b in enumerate(bricks):
		for j in range(b[3]):
			x = b[0][0] + j*b[2][0]
			y = b[0][1] + j*b[2][1]
			z = b[0][2] + j*b[2][2]
			above = volume[x][y][z+1]
			if above != -1 and above != i:
				supports[i].add(above)
				supported_by[above].add(i)
	# Solve :)
	del volume
	part1 = 0
	part2 = 0
	for i, b in enumerate(bricks):
		if len(supports[i]) == 0:
			# No bricks above it. Can be destroyed.
			part1 += 1
		else:
			can_remove = True
			for other in supports[i]:
				if len(supported_by[other]) == 1:
					# If 'i' is the only supporting brick, it can't be destroyed.
					can_remove = False

			if can_remove:
				part1 += 1
			else:
				# See how many bricks will fall if we destroy 'i'.
				removed = set([i])
				current_nodes = set([i])
				while len(current_nodes) != 0:
					next_nodes = set()
					for n in current_nodes:
						for s in supports[n]:
							if len(supported_by[s] - removed) == 0:
								removed.add(s)
								next_nodes.add(s)
					current_nodes = next_nodes
				# -1 since we don't count 'i' itself.
				part2 += len(removed) - 1

	return part1, part2

p1, p2 = solve()
print(f'Part 1:', p1) # 428
print(f'Part 2:', p2) # 35654
