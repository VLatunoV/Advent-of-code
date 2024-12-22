import os

input_file = os.path.join(os.path.dirname(__file__), 'input16.txt')
with open(input_file) as f:
	lines = f.read().splitlines()

for r in range(len(lines)):
	for c in range(len(lines[0])):
		if lines[r][c] == 'S':
			rs = r
			cs = c
		if lines[r][c] == 'E':
			re = r
			ce = c

lines[rs] = lines[rs][0:cs] + '.' + lines[rs][cs+1:]
lines[re] = lines[re][0:ce] + '.' + lines[re][ce+1:]

def heap_push(heap, x):
	heap.append(x)
	idx = len(heap)-1
	while idx > 1:
		nIdx = idx>>1
		if heap[nIdx] > heap[idx]:
			heap[nIdx], heap[idx] = heap[idx], heap[nIdx]
		else:
			break
		idx = nIdx

def heap_pop(heap):
	if len(heap) <= 2:
		return heap.pop()
	result = heap[1]
	heap[1] = heap.pop()
	idx = 1
	min_idx = idx
	while True:
		nIdx = idx<<1
		if nIdx < len(heap) and heap[min_idx] > heap[nIdx]:
			min_idx = nIdx
		nIdx += 1
		if nIdx < len(heap) and heap[min_idx] > heap[nIdx]:
			min_idx = nIdx
		if min_idx == idx:
			break
		else:
			heap[min_idx], heap[idx] = heap[idx], heap[min_idx]
		idx = min_idx
	return result

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def solve():
	inf = -1
	dist = [[[inf] * len(lines[0]) for _ in range(len(lines))] for _ in range(4)]
	parent = [[[None] * len(lines[0]) for _ in range(len(lines))] for _ in range(4)]
	heap = [None]
	dist[0][rs][cs] = 0
	heap_push(heap, (0, 0, rs, cs))

	while len(heap) > 1:
		dst, dir, r, c = heap_pop(heap)

		nr = r + directions[dir][0]
		nc = c + directions[dir][1]
		if lines[nr][nc] != '#' and (dist[dir][nr][nc] == inf or dist[dir][nr][nc] > dst + 1):
			dist[dir][nr][nc] = dst + 1
			parent[dir][nr][nc] = (dir, r, c)
			heap_push(heap, (dst+1, dir, nr, nc))
		
		nd = (dir+1)%4
		if (dist[nd][r][c] == inf or dist[nd][r][c] > dst + 1000):
			dist[nd][r][c] = dst + 1000
			parent[nd][r][c] = (dir, r, c)
			heap_push(heap, (dst+1000, nd, r, c))
		nd = (dir-1)%4
		if (dist[nd][r][c] == inf or dist[nd][r][c] > dst + 1000):
			dist[nd][r][c] = dst + 1000
			parent[nd][r][c] = (dir, r, c)
			heap_push(heap, (dst+1000, nd, r, c))
	
	p1 = min([dist[i][re][ce] for i in range(4)])

	# Part 2
	visited = [[[False] * len(lines[0]) for _ in range(len(lines))] for _ in range(4)]
	for d in range(4):
		if dist[d][re][ce] > p1:
			continue

		other_paths = [(d, re, ce)]
		while len(other_paths) > 0:
			d, r, c = other_paths.pop()
			visited[d][r][c] = True

			while (d, r, c) != (0, rs, cs):
				# Check neighbours
				nr = r - directions[d][0]
				nc = c - directions[d][1]
				if parent[d][r][c] != (d, nr, nc) and not visited[d][nr][nc] and dist[d][nr][nc] + 1 == dist[d][r][c]:
					other_paths.append((d, nr, nc))
				nd = (d+1)%4
				if parent[d][r][c] != (nd, r, c) and not visited[nd][r][c] and dist[nd][r][c]+1000 == dist[d][r][c]:
					other_paths.append((nd, r, c))
				nd = (d-1)%4
				if parent[d][r][c] != (nd, r, c) and not visited[nd][r][c] and dist[nd][r][c]+1000 == dist[d][r][c]:
					other_paths.append((nd, r, c))

				d, r, c = parent[d][r][c]
				if visited[d][r][c] == True:
					break
				visited[d][r][c] = True

	p2 = 0
	for r in range(len(lines)):
		for c in range(len(lines[0])):
			for d in range(4):
				if visited[d][r][c]:
					p2 += 1
					break
	return p1, p2

p1, p2 = solve()

print('Part 1:', p1)
print('Part 2:', p2)
