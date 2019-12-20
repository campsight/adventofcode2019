import copy as cp
import string
import itertools
from collections import deque
import csv
# with open('input_d20-t2.txt', 'r') as input_file:
with open('input_d20.txt', 'r') as input_file:
    reader = csv.reader(input_file)
    input_values = list(reader)

grid = [list(x[0]) for x in input_values]
print(grid)

# '''
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

max_depth = len(teleport_rcs) // 2

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


def get_neighbours(node, curr_depth):
    curr_r = node[0]
    curr_c = node[1]
    neighbours = []
    # south
    if (curr_r < (len(grid) - 1)) and ((curr_r + 1, curr_c) not in walls):
        if (curr_r + 1, curr_c) != start:
            neighbours.append(("S", curr_depth, (curr_r+1, curr_c)))
    elif curr_r == IWSR:  # we are at row where inner wall starts
        neighbours.append(("S", curr_depth + 1, get_teleport_coord(node)))
    elif curr_r == (len(grid) - 1):  # we are at row outer wall
        if (curr_depth > 0) and (node != start):  # outer teleports are only available at higher levels
            neighbours.append(("S", curr_depth - 1, get_teleport_coord(node)))
    # north
    if (curr_r > 0) and ((curr_r - 1, curr_c) not in walls):
        if (curr_r - 1, curr_c) == exit:
            if curr_depth == 0:
                neighbours.append(("N", curr_depth, (curr_r-1, curr_c)))
        else:
            neighbours.append(("N", curr_depth, (curr_r-1, curr_c)))
    elif curr_r == IWER:  # we are at row where inner wall ends
        neighbours.append(("N", curr_depth + 1, get_teleport_coord(node)))
    elif curr_r == 0: # we are at row outer wall
        if curr_depth > 0: # outer teleports are only available at higher depth levels
            neighbours.append(("N", curr_depth - 1, get_teleport_coord(node)))
    # east
    if (curr_c < (len(grid[0])-1)) and ((curr_r, curr_c+1) not in walls):
        neighbours.append(("E", curr_depth, (curr_r, curr_c+1)))
    elif curr_c == IWSC:  # we are at inner wall start
        neighbours.append(("E", curr_depth + 1, get_teleport_coord(node)))
    elif curr_c == (len(grid[0])-1): # we are at column outer wall
        if curr_depth > 0:  # outer teleports are only available at higher depth levels
            neighbours.append(("E", curr_depth - 1, get_teleport_coord(node)))
    # west
    if (curr_c > 0) and ((curr_r, curr_c-1) not in walls):
        if (curr_r, curr_c - 1) == exit:
            if curr_depth == 0:
                neighbours.append(("W", curr_depth, (curr_r, curr_c - 1)))
        else:
            neighbours.append(("W", curr_depth, (curr_r, curr_c - 1)))
    elif curr_c == IWEC: # we are at row where inner wall ends
        neighbours.append(("W", curr_depth + 1, get_teleport_coord(node)))
    elif curr_c == 0: # we are at column outer wall
        if curr_depth > 0:  # outer teleports are only available at higher depth levels
            neighbours.append(("W", curr_depth - 1, get_teleport_coord(node)))
    return neighbours


def find_path_bfs(bfs_start, bfs_goal, bfs_max_depth):
    queue = deque([("", 0, bfs_start)])
    visited = set()
    while queue:
        path, depth, current = queue.popleft()
        if current == bfs_goal:
            return path
        if (current, depth) in visited:
            continue
        visited.add((current, depth))
        next_ones = get_neighbours(current, depth)
        for direction, new_depth, neighbour in next_ones:
            if ((neighbour, new_depth) not in visited) and (new_depth <= bfs_max_depth):
                queue.append((path + direction, new_depth, neighbour))
    return "NO WAY"


sol_path = find_path_bfs(start, exit, max_depth)
print(sol_path)
print(len(sol_path))
