import os

input_file = os.path.join(os.path.dirname(__file__), 'input24.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

lines = [(x[0].split(','), x[1].split(',')) for x in [l.split('@') for l in lines]]

pos = [tuple(map(int, l[0])) for l in lines]
vel = [tuple(map(int, l[1])) for l in lines]

def intersect(i, j):
	p1, p2 = pos[i], pos[j]
	v1, v2 = vel[i], vel[j]
	det = -v1[0]*v2[1] + v1[1]*v2[0]
	if det == 0:
		return (None, None)

	inv_a = (
		(v2[1] / det, -v2[0] / det),
		(v1[1] / det, -v1[0] / det)
	)
	px = p1[0] - p2[0]
	py = p1[1] - p2[1]
	return (inv_a[0][0]*px + inv_a[0][1]*py, inv_a[1][0]*px + inv_a[1][1]*py)

def solve_part1():
	result = 0
	boundary = (200000000000000, 400000000000000)
	for i in range(len(pos)):
		for j in range(i+1, len(pos)):
			t1, t2 = intersect(i, j)
			if t1 and t2:
				i_pos_x = pos[i][0] + t1*vel[i][0]
				i_pos_y = pos[i][1] + t1*vel[i][1]
				if t1>0.0 and t2>0.0 and boundary[0] <= i_pos_x <= boundary[1] and boundary[0] <= i_pos_y <= boundary[1]:
					result += 1
	return result

def vec_prod(a, b):
	return (
		a[1]*b[2] - a[2]*b[1],
		a[2]*b[0] - a[0]*b[2],
		a[0]*b[1] - a[1]*b[0]
	)
def dot_prod(a, b):
	return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
def vec_add(a, b):
	return (a[0]+b[0], a[1]+b[1], a[2]+b[2])
def vec_sub(a, b):
	return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def vec_mul(a, b):
	return (a[0]*b, a[1]*b, a[2]*b)

# The idea is to pick a direction of the stone and then pick any hail, which does not go in the same
# direction. These two vectors form a plane, which can be parameratrized by pos[hail] + lambda*dir[hail] + mu*dir[chosen].
# Then pick a second hail, which intersects this plane and find the intersection time tau. If tau = lambda+mu,
# then the stone hits both hails. The stone position can be found from pos[stone] + dir[chosen]*tau == intersection.
# Lastly, check if every hail is hit and stop if they are.
def check_direction(dir):
	if not (dir[0]!=0 or dir[1]!=0 or dir[2]!=0):
		return None
	epsilon = 1e-3
	for i in range(len(pos)):
		normal = vec_prod(vel[i], dir)
		if normal[0] != 0 or normal[1] != 0 or normal[2] != 0:
			break

	p = None
	tau = None
	for j in range(i+1, len(pos)):
		denom = dot_prod(normal, vel[j])
		if denom == 0:
			continue
		dp = vec_sub(pos[i], pos[j])
		tau = dot_prod(normal, dp) / denom
		p = vec_add(pos[j], vec_mul(vel[j], tau))
		k = vec_sub(p, pos[i])
		e1 = vel[i]
		e2 = dir
		e11 = dot_prod(e1, e1)
		e12 = dot_prod(e1, e2)
		e22 = dot_prod(e2, e2)
		det = (e11*e22) - e12**2
		if det == 0:
			continue
		lam = (e22 * dot_prod(k, e1) - e12*dot_prod(k, e2)) / det
		mu =  (e11 * dot_prod(k, e2) - e12*dot_prod(k, e1)) / det
		if abs(lam + mu - tau) > epsilon:
			return None
		else:
			break

	start_pos = vec_add(p, vec_mul(dir, -tau))
	start_pos = tuple(map(round, start_pos))
	for i in range(len(pos)):
		for dim in range(3):
			if vel[i][dim] != dir[dim]:
				break
		if vel[i][dim] == dir[dim]:
			if start_pos != pos[i]:
				return None
		else:
			time = (start_pos[dim] - pos[i][dim]) / (vel[i][dim] - dir[dim])
			p1 = vec_add(start_pos, vec_mul(dir, time))
			p2 = vec_add(pos[i], vec_mul(vel[i], time))
			if abs(p1[0]-p2[0]) > epsilon or abs(p1[1]-p2[1]) > epsilon or abs(p1[2]-p2[2]) > epsilon:
				return None
	return start_pos

def solve_part2():
	for r in range(1, 1000):
		z = r
		print('Checking radius:', r)
		for x in range(-r, r+1):
			for y in range(-r, r+1):
				start_pos = check_direction((x,y,z))
				if start_pos is not None:
					print(f"Start pos is: {start_pos}")
					return sum(start_pos)
				start_pos = check_direction((x,y,-z))
				if start_pos is not None:
					print(f"Start pos is: {start_pos}")
					return sum(start_pos)
		y = r
		for x in range(-r, r+1):
			for z in range(-(r-1), r):
				start_pos = check_direction((x,y,z))
				if start_pos is not None:
					print(f"Start pos is: {start_pos}")
					return sum(start_pos)
				start_pos = check_direction((x,-y,z))
				if start_pos is not None:
					print(f"Start pos is: {start_pos}")
					return sum(start_pos)
		x = r
		for y in range(-(r-1), r):
			for z in range(-(r-1), r):
				start_pos = check_direction((x,y,z))
				if start_pos is not None:
					print(f"Start pos is: {start_pos}")
					return sum(start_pos)
				start_pos = check_direction((-x,y,z))
				if start_pos is not None:
					print(f"Start pos is: {start_pos}")
					return sum(start_pos)

	return "Couldn't find :("

print(f'Part 1:', solve_part1()) # 15262
print(f'Part 2:', solve_part2()) # 695832176624149
