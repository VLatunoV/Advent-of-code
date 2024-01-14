import os

input_file = os.path.join(os.path.dirname(__file__), 'input11.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

class Monkey:
	def __init__(self, items, operation, operand, test, if_true, if_false):
		self.items = items
		self.operation = operation
		self.operand = operand
		self.test = test
		self.if_true = if_true
		self.if_false = if_false

	def get_items(self):
		transform = None
		if self.operand == 'old':
			if self.operation == '*':
				transform = lambda x: x * x
			else:
				transform = lambda x: x + x
		else:
			if self.operation == '*':
				transform = lambda x: x * int(self.operand)
			else:
				transform = lambda x: x + int(self.operand)
		return list(map(lambda x: transform(x), self.items))

def parse_input():
	result = []
	i = 0
	while i + 1 < len(lines):
		i += 1
		_, items = lines[i].split(':')
		items = items.split(",")
		items = list(map(lambda x: int(x.strip()), items))
		i += 1
		_, operation = lines[i].split("=")
		parts = operation.split()
		operation = parts[1]
		operand = parts[2]
		i += 1
		test = int(lines[i].split()[-1])
		i += 1
		if_true = int(lines[i].split()[-1])
		i += 1
		if_false = int(lines[i].split()[-1])
		result.append(Monkey(items, operation, operand, test, if_true, if_false))
		i += 2
	return result

def solve(part):
	monkeys = parse_input()
	monkey_inspect = [0] * len(monkeys)
	if part == 2:
		divisor = 1
		for m in monkeys:
			divisor *= m.test
	for _ in range(20 if part == 1 else 10000):
		for i in range(len(monkeys)):
			m = monkeys[i]
			items = m.get_items()
			for item in items:
				if part == 1:
					item = item // 3
				else:
					item = item % divisor
				if item % m.test == 0:
					monkeys[m.if_true].items.append(item)
				else:
					monkeys[m.if_false].items.append(item)
			monkey_inspect[i] += len(items)
			m.items = []

	monkey_inspect = sorted(monkey_inspect)
	return monkey_inspect[-1] * monkey_inspect[-2]

print('Part 1:', solve(part=1)) # 182293
print('Part 2:', solve(part=2)) # 54832778815
