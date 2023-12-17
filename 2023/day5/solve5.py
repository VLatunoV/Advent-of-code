import os

input_file = os.path.join(os.path.dirname(__file__), 'input5.txt')
with open(input_file) as f:
	l = f.readline()
	seeds = [int(x) for x in l.split(':')[1].strip().split()]
	
	forward_maps = []
	for line in f.read().splitlines():
		if line == '':
			continue
		if line.endswith(':'):
			forward_maps.append([])
		else:
			interval = tuple([int(x) for x in line.split()])
			forward_maps[-1].append(interval)

def use_map(map_index, input):
	for dest, src, dist in forward_maps[map_index]:
		if input >= src and input < src + dist:
			return dest + (input - src)
	return input

def solve_part1():
	initial_seeds = seeds
	for map_index in range(len(forward_maps)):
		initial_seeds = [use_map(map_index, x) for x in initial_seeds]
	return min(initial_seeds)

##################################################################################

def get_end(interval):
	return interval[1] + interval[2]

def fix_ranges(mapping):
	additional_mappings = []
	for index in range(len(mapping)):
		new_start = get_end(mapping[index - 1]) if index > 0 else 0
		new_end = mapping[index][1]
		additional_mappings.append((new_start, new_start, new_end - new_start))
	last_start = get_end(mapping[-1])
	last_end = 2**64 - 1
	additional_mappings.append((last_start, last_start, last_end - last_start))
	result = list(filter(lambda x: x[2]!=0, sorted(mapping + additional_mappings, key=lambda x: x[1])))

	return result

def interval_intersection(interval1, interval2):
	start1, end1 = interval1
	start2, end2 = interval2

	# Calculate intersection
	intersection_start = max(start1, start2)
	intersection_end = min(end1, end2)

	if intersection_start >= intersection_end:
		return None

	return (intersection_start, intersection_end)

def use_maps_range(seed_range, mappings):
	result = [seed_range]
	for mapping in mappings:
		new_result = []
		for seed in result:
			for dest, src, dist in mapping:
				new_seed = interval_intersection(seed, (src, get_end((dest, src, dist))))
				if new_seed:
					offset = dest - src
					new_result.append((new_seed[0] + offset, new_seed[1] + offset))
		result = new_result

	return result

def solve_part2():
	sorted_map = [fix_ranges(sorted(x, key=lambda y: y[1])) for x in forward_maps]
	seed_ranges = list(zip(seeds[::2], seeds[1::2]))
	seed_ranges = [(x, x+y) for x, y in seed_ranges]
	result = [use_maps_range(x, sorted_map) for x in seed_ranges]
	result = [element for sublist in result for element in sublist]
	return min(result)[0]

print(f'Part 1: {solve_part1()}') # 993500720
print(f'Part 2: {solve_part2()}') # 4917124
