# Exercise 11
# Author: Kristin Avans

def find_empty(lines):
	col_ind_double = []
	row_ind_double = []
	# Find columns with only "."
	for j in range(len(lines)):
			current_col = "".join([lines[i][j] for i in range(len(lines))])
			if current_col.count(".") == len(lines):
				col_ind_double.append(j)
	# Find rows with only "."
	for l in range(len(lines)):
		if lines[l].count(".") == len(lines):
			row_ind_double.append(l)

	return row_ind_double, col_ind_double


def find_min_distances(lines, row_add, col_add):

	coord_empty = find_empty(lines)
	row_ind_double = coord_empty[0]
	col_ind_double = coord_empty[1]

	nr_rows = len(lines)
	nr_cols = len(lines[0])

	coord = []

	# Find coordinates for #
	for r in range(nr_rows):
		for c in range(nr_cols):
			if lines[r][c] == "#": coord.append((r, c))
	#print(coord)

	distances = 0
	for i in range(len(coord)):
		for j in range(i+1, len(coord)):
			c_curr = coord[i]
			c_next = coord[j]
			# New coordinates will be shifted row_add/col_add times
			row_current = c_curr[0] + (row_add-1)*(sum([c_curr[0] > x for x in row_ind_double]))
			col_current = c_curr[1] + (col_add-1)*(sum([c_curr[1] > x for x in col_ind_double]))
			row_next = c_next[0] + (row_add-1)*(sum([c_next[0] > x for x in row_ind_double]))
			col_next = c_next[1] + (col_add-1)*(sum([c_next[1] > x for x in col_ind_double]))

			# Since we can only step up, down, left, right, then shortest is just as going straight
			distances += row_next-row_current + abs(col_next-col_current)

	return distances

import os

input_file = os.path.join(os.path.dirname(__file__), 'input11.txt')
with open(input_file) as f:
	lines = f.readlines()
	lines = [x.strip() for x in lines]

	distances = find_min_distances(lines, 2, 2)
	print("Part 1:", distances) # 9312968
	distances2 = find_min_distances(lines, 1000000, 1000000)
	print("Part 2:", distances2) # 597714117556
