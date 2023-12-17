import os

input_file = os.path.join(os.path.dirname(__file__), 'input3.txt')
with open(input_file) as f:
	input_lines = f.readlines()

board = [x[:-1] for x in input_lines]

width = len(board[0])
height = len(board)

symbol_map = [[False]*width for _ in range(height)]

def get_number(row, col):
	number = 0
	i = 0
	should_add = False
	while col + i < width and board[row][col + i].isdigit():
		number = number*10 + int(board[row][col + i])
		should_add = should_add or symbol_map[row][col + i]
		i += 1
	return number, i, should_add

# Solve part 1
def solve_part1():
	for row in range(height):
		for col in range(width):
			cell = board[row][col]
			if not cell.isdigit() and cell != '.':
				for offset_row in range(-1, 2):
					new_row = row + offset_row
					if new_row >= 0 and new_row < height:
						for offset_col in range(-1, 2):
							new_col = col + offset_col
							if new_col >= 0 and new_col < width:
								symbol_map[new_row][new_col] = True
	
	result = 0
	for row in range(height):
		col = 0
		while col < width:
			cell = board[row][col]
			if cell.isdigit():
				number, num_digits, should_add = get_number(row, col)
				col += num_digits
				if should_add:
					result += number
			else:
				col += 1
	
	return result

def get_gear_power(row, col):
	# Keeps track of which neighbours have been processed around the gear.
	# The idea is to mark them and skip them if we see them again.
	processed_cells = [[False]*3 for _ in range(3)]
	numbers = []
	for row_offset in range(-1, 2):
		new_row = row + row_offset
		if new_row < 0 or new_row > height-1:
			continue
		# This time we will go right-to-left. It doesn't matter if we go from the top or bottom first.
		# Start from 1. Continue until -2. Add -1 at each step.
		# Since in any case we could start from the middle of a number, we would have to go in both direction
		# to find all of it. But as you will see later, we will go back to find the start of the number.
		# While we do this 'going back', we will mark the digits as processed as well. And because we are going
		# right-to-left, we know that any digits before it are either already marked, or too far (so we don't mark them,
		# we only mark 3 cells around the gear)
		for col_offset in range(1, -2, -1):
			new_col = col + col_offset
			if new_col < 0 or new_col > width - 1:
				continue
			# For each neighbouring cell, check first if it has been processed.
			# The +1 makes the offset [-1, 0, 1] into an index [0, 1, 2]
			if processed_cells[row_offset+1][col_offset+1] == False:
				processed_cells[row_offset+1][col_offset+1] = True
				if board[new_row][new_col].isdigit():
					# Find the start of the number by going backward as much as we can
					number_start_position = new_col
					# While we can still go backward, subtract 1 from the position
					while number_start_position-1 >= 0 and board[new_row][number_start_position-1].isdigit():
						number_start_position -= 1
						# Mark any other neighbour cells along the way
						# number_start_position = new_col = col + col_offset, so the col_offset = number_start_position - col.
						# Add +1 to turn into an index
						index = number_start_position - col + 1
						if index >= 0:
							processed_cells[row_offset+1][index] = True
					# Now we can reuse the last function to get the number
					number, _, _ = get_number(new_row, number_start_position)
					# Add the number to our final list of neighbour numbers
					numbers.append(number)
	
	return numbers[0]*numbers[1] if len(numbers) == 2 else 0

def solve_part2():
	result = 0
	for row in range(height):
		for col in range(width):
			cell = board[row][col]
			if cell == '*':
				result += get_gear_power(row, col)
	return result

print(f"Part 1: {solve_part1()}") # 527446
print(f"Part 2: {solve_part2()}") # 73201705
