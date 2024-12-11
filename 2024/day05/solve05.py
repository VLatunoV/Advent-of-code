import os

input_file = os.path.join(os.path.dirname(__file__), 'input05.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

# Input string parsing
rules_end = lines.index("")
rules = lines[:rules_end]
updates = lines[rules_end+1:]

# Input to numbers parsing
rules = set([tuple(map(int, x.split('|'))) for x in rules])
updates = [list(map(int, x.split(','))) for x in updates]

def check_correct(u):
	for i in range(len(u)):
		for j in range(i+1, len(u)):
			if (u[j], u[i]) in rules:
				return False
	return True

def fix_incorrect(u):
	for i in range(len(u)):
		for j in range(i+1, len(u)):
			if (u[j], u[i]) in rules:
				u[i], u[j] = u[j], u[i]

def solve():
	correct = 0
	incorrect = 0
	for u in updates:
		if check_correct(u):
			correct += u[len(u)//2]
		else:
			fix_incorrect(u)
			incorrect += u[len(u)//2]
	return correct, incorrect

p1, p2 = solve()

print('Part 1:', p1)
print('Part 2:', p2)
