import copy as cp
import string
import itertools
from collections import deque
import csv
#with open('input_d20-t2.txt', 'r') as input_file:
with open('input_d20.txt', 'r') as input_file:
    reader = csv.reader(input_file)
    input_values = list(reader)

grid = [list(x[0]) for x in input_values]
print(grid)


IWSR = 34  # Inner Wall Start Row
IWER = 96  # Inner Wall End Row
IWSC = 34  # Inner Wall Start Column
IWEC = 90  # Inner Wall End Column
'''

IWSR = 6  # Inner Wall Start Row
IWER = 26  # Inner Wall End Row
IWSC = 6  # Inner Wall Start Column
IWEC = 34  # Inner Wall End Column
'''

teleports = {}
wall_locations = []
teleport_pos_c = []
teleport_pos_r = []
teleport_pos_char = []
start = []
exit = []


# teleports defined in columns
r_offsets = [0, -3, 0, -3]
r_tps = [0, IWSR + 3, IWER, len(grid)-2]
p_len = 0
for k in (range(4)):
    i = r_tps[k]
    teleport_pos_c += [(pos - 2) for pos, char in enumerate(grid[i]) if char in string.ascii_uppercase]
    c_len = len(teleport_pos_c)
    teleport_pos_r += [int(i + r_offsets[k])]*(c_len - p_len)
    teleport_pos_char += [str(ltr[0]) + str(ltr[1]) for ltr in list(zip(grid[i], grid[i+1])) if
                          ltr[0] in string.ascii_uppercase]
    p_len = c_len

print(teleport_pos_r)
print(teleport_pos_c)
print(teleport_pos_char)

# add teleports defined in rows
r_offsets = [0, -3, 0, -3]
r_tps = [0, IWSC + 3, IWEC, len(grid[0])-2]
for k in (range(4)):
    i = r_tps[k]
    col = [x[i] for x in grid]
    nxt_col = [x[i+1] for x in grid]
    teleport_pos_r += [(pos - 2) for pos, char in enumerate(col) if char in string.ascii_uppercase]
    c_len = len(teleport_pos_r)
    teleport_pos_c += [int(i + r_offsets[k])]*(c_len - p_len)
    teleport_pos_char += [str(ltr[0]) + str(ltr[1]) for ltr in list(zip(col, nxt_col)) if
                          ltr[0] in string.ascii_uppercase]
    p_len = c_len

print(teleport_pos_r)
print(teleport_pos_c)
print(teleport_pos_char)

# subset grid to exclude teleport indications
grid = grid[2:(-2)]
grid = [x[2:(-2)] for x in grid]
# print(grid[0], chr(10), grid[-1])

start_i = teleport_pos_char.index('AA')
exit_i = teleport_pos_char.index('ZZ')
start = (teleport_pos_r[start_i], teleport_pos_c[start_i])
exit = (teleport_pos_r[exit_i], teleport_pos_c[exit_i])

for array in (teleport_pos_c, teleport_pos_r, teleport_pos_char):
    if start_i < exit_i:
        array.pop(exit_i)
        array.pop(start_i)
    else:
        array.pop(start_i)
        array.pop(exit_i)

print(start, exit)

# fill middle rectangle with walls
for r in range(IWSR+1, IWER):
    for c in range(IWSC+1, IWEC):
        grid[r][c] = '#'

for i in range(len(grid)):
    wall_locations.append([pos for pos, char in enumerate(grid[i]) if char == '#'])

walls = [(i, j) for i in range(len(wall_locations)) for j in wall_locations[i]]
teleport_rcs = list(zip(teleport_pos_r, teleport_pos_c))

print(teleport_rcs)


def get_teleport_coord(origin_coords):
    if (origin_coords == start) or (origin_coords == exit): return origin_coords
    loc = teleport_rcs.index(origin_coords)
    name = teleport_pos_char[loc]
    tc_loc = teleport_pos_char.index(name)
    if tc_loc == loc:
        tc_loc = teleport_pos_char[(loc+1):].index(name) + loc + 1
    return teleport_rcs[tc_loc]


def get_direction(from_coords):
    if (from_coords[0] == 0) or (from_coords[0] == IWER):
        return "N"
    elif (from_coords[0] == IWSR) or (from_coords[0] == (len(grid)-1)):
        return "S"
    elif (from_coords[1] == 0) or (from_coords[1] == IWEC):
        return "W"
    elif (from_coords[1] == IWSC) or (from_coords[1] == (len(grid[0])-1)):
        return "E"


def grid2graph(g2grid, g2walls):
    teleport_coords_handled = [start, exit]
    height = len(g2grid)
    width = len(g2grid[0]) if height else 0
    graph = {(i, j): [] for j in range(width) for i in range(height) if not ((i,j) in g2walls)}
    for row, col in graph.keys():
        # if row < height - 1 and not ((row + 1, col) in g2walls):
        if row < height and not ((row + 1, col) in g2walls):
            if (row == 0) or ((row == IWER) and (col >= IWSC) and (col <= IWEC)): # teleport row
                # top rows => also add normal items
                graph[(row, col)].append(("S", (row + 1, col)))
                graph[(row + 1, col)].append(("N", (row, col)))
                teleport_coords = get_teleport_coord((row, col))
                if teleport_coords not in teleport_coords_handled:
                    graph[(row, col)].append(("N", teleport_coords))
                    teleport_dir = get_direction(teleport_coords)
                    graph[teleport_coords].append((teleport_dir, (row, col)))
                    teleport_coords_handled.append((row, col))
                    teleport_coords_handled.append(teleport_coords)
            elif (row == (len(grid)-1)) or ((row == IWSR) and (col >= IWSC) and (col <= IWEC)):
                if (row, col) == start: continue
                teleport_coords = get_teleport_coord((row, col))
                if teleport_coords not in teleport_coords_handled:
                    graph[(row, col)].append(("S", teleport_coords))
                    teleport_dir = get_direction(teleport_coords)
                    graph[teleport_coords].append((teleport_dir, (row, col)))
                    teleport_coords_handled.append((row, col))
                    teleport_coords_handled.append(teleport_coords)
            else:
                graph[(row, col)].append(("S", (row + 1, col)))
                graph[(row + 1, col)].append(("N", (row, col)))
        # if col < width - 1 and not ((row, col + 1) in g2walls):
        if col < width and not ((row, col + 1) in g2walls):
            if (col == 0) or ((col == IWEC) and (row >= IWSR) and (row <= IWER)):
                graph[(row, col)].append(("E", (row, col + 1)))
                graph[(row, col + 1)].append(("W", (row, col)))
                teleport_coords = get_teleport_coord((row, col))
                if teleport_coords not in teleport_coords_handled:
                    graph[(row, col)].append(("W", teleport_coords))
                    teleport_dir = get_direction(teleport_coords)
                    graph[teleport_coords].append((teleport_dir, (row, col)))
                    teleport_coords_handled.append((row, col))
                    teleport_coords_handled.append(teleport_coords)
            elif (col == (len(grid[0])-1)) or ((col == IWSC) and (row >= IWSR) and (row <= IWER)):
                teleport_coords = get_teleport_coord((row, col))
                if teleport_coords not in teleport_coords_handled:
                    graph[(row, col)].append(("E", teleport_coords))
                    teleport_dir = get_direction(teleport_coords)
                    graph[teleport_coords].append((teleport_dir, (row, col)))
                    teleport_coords_handled.append((row, col))
                    teleport_coords_handled.append(teleport_coords)
            else:
                graph[(row, col)].append(("E", (row, col + 1)))
                graph[(row, col + 1)].append(("W", (row, col)))
    return graph


def find_path_bfs(bfs_graph, bfs_start, bfs_goal):
    queue = deque([("", bfs_start)])
    visited = set()
    while queue:
        path, current = queue.popleft()
        if current == bfs_goal:
            return path
        if current in visited:
            continue
        visited.add(current)
        for direction, neighbour in bfs_graph[current]:
            queue.append((path + direction, neighbour))
    return "NO WAY"


graph = grid2graph(grid, walls)
path = find_path_bfs(graph, start, exit)
print(path)
print(len(path))
