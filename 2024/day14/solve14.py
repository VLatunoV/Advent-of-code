import os

input_file = os.path.join(os.path.dirname(__file__), 'input14.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

def parse_robot(l):
	pos, vel = l.split()
	pos = tuple([int(x) for x in pos.split('=')[1].split(',')])
	vel = tuple([int(x) for x in vel.split('=')[1].split(',')])
	return pos, vel

robots = [parse_robot(l) for l in lines]
width = 101
height = 103
time_steps = 100

def mul(a, x):
	return (a*x[0], a*x[1])
def add(x, y):
	return (x[0]+y[0], x[1]+y[1])
def make_valid(x):
	return (x[0]%width, x[1]%height)

def solve_part1():
	res = [0]*4
	for pos, vel in robots:
		end_pos = make_valid(add(pos, mul(time_steps, vel)))
		idx = (int(end_pos[0] < width//2) << 0) | (int(end_pos[1] < height//2) << 1)
		if end_pos[0] != width//2 and end_pos[1] != height//2:
			res[idx] += 1
	for i in range(1, len(res)):
		res[i] *= res[i-1]
	return res[-1]

def print_robots(t, file):
	img = [['.']*width for _ in range(height)]
	histograms = [0] * width
	for pos, vel in robots:
		end_pos = make_valid(add(pos, mul(t, vel)))
		img[end_pos[1]][end_pos[0]] = '*'
		histograms[end_pos[0]] += 1

	histograms.sort()
	for i in range(len(histograms)):
		if histograms[i] != 0:
			histograms = histograms[i:]
			break
	avg = sum(histograms) / len(histograms)
	stdv = sum([(x-avg)**2 for x in histograms]) ** 0.5
	if stdv > 50:
		print(f"Interesting time {t}: {stdv}")
		for r in img:
			file.write(''.join(r))
			file.write('\n')
		file.write(f'^-- For time {t}\n\n')

def solve_part2():
	with open('result.txt', 'w') as f:
		for t in range(10000):
			print_robots(t, f)

print('Part 1:', solve_part1())
print('Part 2:', solve_part2())
