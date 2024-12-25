import os

input_file = os.path.join(os.path.dirname(__file__), 'input21.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

# Right=0, up=1, left=2, down=3
directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]
num_pad = [
	[7, 8, 9],
	[4, 5, 6],
	[1, 2, 3],
	[None, 0, 10]
]
np_neighbour = {
	7: [0, 3],
	8: [0, 2, 3],
	9: [2, 3],
	4: [0, 1, 3],
	5: [0, 1, 2, 3],
	6: [1, 2, 3],
	1: [0, 1],
	2: [0, 1, 2, 3],
	3: [1, 2, 3],
	0: [0, 1],
	10: [1, 2]
}

dir_pad = [
	[None, 1, 2],
	[3, 4, 5]
]
directions_on_pad = [5, 1, 3, 4]
dir_action_button = 2
dp_neighbour = {
	1: [0, 3],
	2: [2, 3],
	3: [0],
	4: [0, 1, 2],
	5: [1, 2]
}

# Holds the number of moves to click button j from initial position i, while all previous
# positions are on 'A'
inf = 2**62
max_keypads = 25 + 1
directional_dist = [[[inf] * 6 for _ in range(6)] for _ in range(max_keypads)]
for i in range(6):
	for j in range(6):
		directional_dist[0][i][j] = 1

# Precompute the cost to press any num key from any other
# Uses Dijkstra's algorithm with weights fron the cost_table. The graph nodes are the state of the current position
# with the position of the previous arm. The precomputed tables are the cost to press the button, while dijkstra
# computes the cost only to move over a button (without pressing it). The separation is because we want to move
# many times to reach the target button, but ultimately we care only about the cost to press it in the end.
def precompute_table(table, cost_table, pad, neighbour):
	for sr in range(len(pad)):
		for sc in range(len(pad[sr])):
			start = pad[sr][sc]
			if start is None:
				continue
			# Holds the current distance, the number of the current pad, the number of the previous pad
			queue = [(0, sr, sc, dir_action_button)]
			move_cost = [[[inf] * 6 for _ in range(12)] for _ in range(12)]
			move_cost[start][start][dir_action_button] = 0
			table[start][start] = 1
			while len(queue) > 0:
				# Find min from queue
				min_idx = 0
				for idx in range(1, len(queue)):
					if queue[idx] < queue[min_idx]:
						min_idx = idx
				dd, r, c, prev = queue[min_idx]
				queue[min_idx] = queue[-1]
				queue.pop()
				node_val = pad[r][c]
				# Walk its neighbours
				for di in neighbour[node_val]:
					dir_to_press = directions_on_pad[di]
					nr = r + directions[di][0]
					nc = c + directions[di][1]
					next_node_val = pad[nr][nc]
					cost = dd + cost_table[prev][dir_to_press]
					if move_cost[node_val][next_node_val][dir_to_press] > cost:
						move_cost[node_val][next_node_val][dir_to_press] = cost
						queue.append((move_cost[node_val][next_node_val][dir_to_press], nr, nc, dir_to_press))
					cost_to_press = cost + cost_table[dir_to_press][dir_action_button]
					if table[start][next_node_val] > cost_to_press:
						table[start][next_node_val] = cost_to_press

for level in range(1, max_keypads):
	precompute_table(directional_dist[level], directional_dist[level-1], dir_pad, dp_neighbour)

def path_len(code, table):
	res = 0
	last = 10
	for c in code:
		target = 10 if c=='A' else int(c)
		res += table[last][target]
		last = target
	return res

def solve(table):
	ans = 0
	for code in lines:
		numeric = int(code[:-1])
		ans += path_len(code, table) * numeric
	return ans

def solve_part1():
	t = [[inf]*12 for _ in range(12)]
	precompute_table(t, directional_dist[2], num_pad, np_neighbour)
	return solve(t)

def solve_part2():
	t = [[inf]*12 for _ in range(12)]
	precompute_table(t, directional_dist[25], num_pad, np_neighbour)
	return solve(t)

print('Part 1:', solve_part1())
print('Part 2:', solve_part2())
