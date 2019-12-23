import collections
import itertools

with open('input_d18-nele.txt', 'r') as input_file:
    grid = [s.rstrip() for s in input_file.readlines()]

linear_grid = list(itertools.chain.from_iterable(grid))
gr_width, gr_height = len(grid[0]), len(grid)
start = linear_grid.index('@')
start_col, start_row = start % gr_width, start // gr_width
all_keys = set(c for c in linear_grid if c.islower())

grid[start_row-1] = grid[start_row-1][:start_col]   +  '#'  + grid[start_row-1][start_col+1:]
grid[  start_row] = grid[start_row  ][:start_col-1] + '###' + grid[start_row  ][start_col+2:]
grid[start_row+1] = grid[start_row+1][:start_col]   +  '#'  + grid[start_row+1][start_col+1:]


def get_reachable_keys(grk_row, grk_col, grk_keys):
    queue = collections.deque([(grk_row, grk_col, 0)])
    visited = set()
    adjacents = ( (-1, 0), (1, 0), (0, -1), (0, 1) )
    while queue:
        c_row, c_col, length = queue.popleft()
        if grid[c_row][c_col].islower() and grid[c_row][c_col] not in grk_keys:
            yield length, c_row, c_col, grid[c_row][c_col]
            continue
        for delta_row, delta_col in adjacents:
            nxt_col, nxt_row = c_col + delta_col, c_row + delta_row
            if ((nxt_row, nxt_col)) in visited:
                continue
            visited.add((nxt_row, nxt_col))

            c = grid[nxt_row][nxt_col]
            if c != '#' and (not c.isupper() or c.lower() in grk_keys):
                queue.append((nxt_row, nxt_col, length + 1))


start_pos = (
   (start_row-1, start_col-1),
   (start_row+1, start_col-1),
   (start_row-1, start_col+1),
   (start_row+1, start_col+1),)

queue = [(0, start_pos, frozenset())]
visited = [set(), set(), set(), set()]

while queue:
    distance, cpos, current_keys = queue.pop(0)  # queue.pop()  # heapq.heappop(queue)
    if current_keys == all_keys:
        print(distance)
        break

    for i, (c_row, c_col) in enumerate(cpos):
        if (c_row, c_col, current_keys) in visited[i]:
            continue
        visited[i].add((c_row, c_col, current_keys))
        for length, nxt_row, nxt_col, key in get_reachable_keys(c_row, c_col, current_keys):
            nxt_pos = cpos[0:i] + ((nxt_row, nxt_col),) + cpos[i+1:]
            queue.append((distance + length, nxt_pos, current_keys | frozenset([key])))
    queue = sorted(queue, key=lambda x: x[0])
