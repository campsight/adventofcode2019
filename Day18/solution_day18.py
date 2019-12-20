import copy as cp
import string
import itertools
from collections import deque
import csv
with open('input_d18.txt', 'r') as input_file:
    reader = csv.reader(input_file)
    input_values = list(reader)

grid = [list(x[0]) for x in input_values]
print(grid)

wall_locations = []
key_locations = []
key_values = []
door_locations = []
start = []

for i in range(len(grid)):
    start_pos = [pos for pos, char in enumerate(grid[i]) if char == '@']
    if len(start_pos) > 0: start = (i, start_pos[0])
    wall_locations.append([pos for pos, char in enumerate(grid[i]) if char == '#'])
    key_locations.append([pos for pos, char in enumerate(grid[i]) if char in string.ascii_lowercase])
    key_values += [char for pos, char in enumerate(grid[i]) if char in string.ascii_lowercase]
    door_locations.append([pos for pos, char in enumerate(grid[i]) if char in string.ascii_uppercase])

print(wall_locations, chr(10), key_locations, chr(10), key_values, chr(10), door_locations)

walls = [(i, j) for i in range(len(wall_locations)) for j in wall_locations[i]]
keys = [(i, j) for i in range(len(key_locations)) for j in key_locations[i]]
doors = [(i, j) for i in range(len(door_locations)) for j in door_locations[i]]

print(walls, chr(10), keys, chr(10), doors)


def grid2graph(g2grid, g2walls):
    height = len(g2grid)
    width = len(g2grid[0]) if height else 0
    graph = {(i, j): [] for j in range(width) for i in range(height) if not ((i,j) in g2walls)}
    for row, col in graph.keys():
        if row < height - 1 and not ((row + 1, col) in g2walls):
            graph[(row, col)].append(("S", (row + 1, col)))
            graph[(row + 1, col)].append(("N", (row, col)))
        if col < width - 1 and not ((row, col + 1) in g2walls):
            graph[(row, col)].append(("E", (row, col + 1)))
            graph[(row, col + 1)].append(("W", (row, col)))
    return graph


def find_path_bfs(bfs_graph, bfs_grid, bfs_start, bfs_keys, bfs_doors):
    objects = [bfs_start] + bfs_keys + bfs_doors
    routes = {}
    keys_to_get_here = {}
    for obj in objects: routes[bfs_grid[obj[0]][obj[1]]] = {}
    # print(routes)
    queue = deque([("", objects.pop(0), "@", 0, [])])
    visited = set()
    while queue:
        path, current, prev, prev_path_len, keys_req = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        if current in objects:
            current_char = bfs_grid[current[0]][current[1]]
            routes[prev][current_char] = len(path) - prev_path_len
            objects.remove(current)
            prev = current_char
            prev_path_len = len(path)
            if current in bfs_doors: keys_req += [current_char.lower()]
            if current in bfs_keys: keys_to_get_here[current_char] = cp.copy(keys_req)
            if len(objects) == 0: return routes, keys_to_get_here
        for direction, neighbour in bfs_graph[current]:
            queue.append((path + direction, neighbour, prev, prev_path_len, keys_req))
    return routes, keys_to_get_here


graph = grid2graph(grid, walls)
routes, keys_to_get_here = find_path_bfs(graph, grid, start,  keys, doors)
print(routes)
print(keys_to_get_here)
print(max(key_values))
my_key_list = list(map(chr, range(ord('a'), ord(max(key_values))+1)))
print(list(itertools.permutations(my_key_list)))