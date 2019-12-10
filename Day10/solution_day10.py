import copy

def isBetween(a, b, c):
    crossproduct = (c[1] - a[1]) * (b[0] - a[0]) - (c[0] - a[0]) * (b[1] - a[1])
    # compare versus epsilon for floating point values, or != 0 if using integers
    # if abs(crossproduct) > epsilon:
    if abs(crossproduct) > 0:
        return False
    return True


import csv
with open('input_d10.txt', 'r') as input_file:
    reader = csv.reader(input_file)
    input_values = list(reader)

astroid_locations = [''.join(x) for x in input_values]

for i in range(len(astroid_locations)):
    astroid_locations[i] = [pos for pos, char in enumerate(astroid_locations[i]) if char == '#']


def get_subset(a, b, astroids):
    lowest_x = min(a[0], b[0])
    lowest_y = min(a[1], b[1])
    highest_x = max(a[0], b[0])
    highest_y = max(a[1], b[1])
    subset = copy.deepcopy(astroids[lowest_y:(highest_y + 1)])
    for sy in range(len(subset)):
        remove_list = []
        for sx in subset[sy]:
            if (sx < lowest_x) or (sx > highest_x):
                remove_list.append(sx)
        for element in remove_list:
            subset[sy].remove(element)
    subset[a[1]-lowest_y].remove(a[0])
    subset[b[1]-lowest_y].remove(b[0])
    return subset


def check_in_between(a, b, subset, y_offset):
    for cib_y in range(len(subset)):
        for cib_x in subset[cib_y]:
            real_y = cib_y + y_offset
            if ((cib_x != a[0]) or (real_y != a[1])) and ((cib_x != b[0]) or (real_y != b[1])):
                if isBetween(a, b, [cib_x, real_y]):
                    return True
    return False


def search_visible_astroids(x_coord, y_coord, asteroids):
    result = [[x_coord], [y_coord]]
    for vy in range(len(asteroids)):
        for vx in asteroids[vy]:
            if (vx != x_coord) or (vy != y_coord):
                subset = get_subset([x_coord, y_coord], [vx, vy], asteroids)
                in_between = check_in_between([x_coord, y_coord], [vx, vy], subset, min(y_coord, vy))
                if not in_between:
                    result[0].append(vx)
                    result[1].append(vy)
    result[0].pop(0)
    result[1].pop()
    return result


max_nb_astroids = 0
visible_astroids = []
solution_x = -1
solution_y = -1
for y in range(len(astroid_locations)):
    for x in astroid_locations[y]:
        xy_astroids = search_visible_astroids(x, y, astroid_locations)
        if (len(xy_astroids[0]) > max_nb_astroids):
                max_nb_astroids = len(xy_astroids[0])
                solution_x = x
                solution_y = y
                visible_astroids = xy_astroids
                print("nb", max_nb_astroids, "x", solution_x, "y", solution_y, "visible", visible_astroids)

print("solution has ", max_nb_astroids, " visibles from (x,y)", solution_x, solution_y, "with visibles: ", visible_astroids)

# PART 2
# let's have some fun with quadrants :-)
# 1st quadrant = uppper right one: lower y, higher x
max_x = max(visible_astroids[0])
max_y = max(visible_astroids[1])
visible_asteroids_merged = [(visible_astroids[0][i], visible_astroids[1][i]) for i in range(0, len(visible_astroids[0]))]
'''quadrant_1 = []
for i in range(visible_astroids[0]):
    asteroid_x = visible_astroids[0][i]
    asteroid_y = visible_astroids[1][i]
for qy in range(solution_y): #this doesn't add the solution_y itself to the quadrant
    for qx in range(solution_x, max_x+1): # the initial x and max x should be included'''

