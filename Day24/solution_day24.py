import itertools
import copy as cp

PRINT_CHARS = ['.', '#']

with open('input_d24.txt', 'r') as input_file:
    input_values = [s.rstrip() for s in input_file.readlines()]

grid = []
for line in input_values:
     grid.append([x == '#' for x in line])
print(grid)
initial_gird = cp.copy(grid)

def get_nb_adjacent_bugs(input_grid, i_row, i_col):
    sum = 0
    if i_row > 0: sum += input_grid[i_row-1][i_col]
    if i_row < len(input_grid)-1: sum += input_grid[i_row+1][i_col]
    if i_col > 0: sum += input_grid[i_row][i_col-1]
    if i_col < len(input_grid[0])-1: sum += input_grid[i_row][i_col+1]
    return sum


def print_grid(pgrid):
    for line in pgrid:
        pline = [PRINT_CHARS[x] for x in line]
        print(''.join(pline))


def run_bug_life_cycle(input_grid):
    new_grid = []
    for r in range(len(grid)):
        new_grid_line = []
        for c in range(len(grid[0])):
            # print(r, c, get_nb_adjacent_bugs(grid, r, c))
            if grid[r][c]:  # bug dies if exactly one bug adjacent
                new_grid_line.append(get_nb_adjacent_bugs(grid, r, c) == 1)
            else:  # infexted if exactly 1 or 2 bugs
                nb_bugs = get_nb_adjacent_bugs(grid, r, c)
                new_grid_line.append((nb_bugs == 1) or (nb_bugs == 2))
        new_grid.append(new_grid_line)
    return new_grid


print_grid(grid)
print()
all_solutions = []
nb_minutes = 1000
for cycle in range(nb_minutes):
    linear_grid = list(itertools.chain.from_iterable(grid))
    if linear_grid in all_solutions:
        print("Solution found")
        break
    all_solutions.append(cp.copy(linear_grid))
    next_step = run_bug_life_cycle(grid)
    grid = next_step

solution = 0
for i in range(len(linear_grid)):
    solution += linear_grid[i] * pow(2,i)
print(solution)

# PART 2


def get_nb_adjacent_bugs_in_dim(all_dims, current_dim, r, c):
    if (r == 2) and (c == 2): return 0
    rsum = 0
    if not current_dim in all_dims.keys():
        all_dims[current_dim] = [[False]*5]*5
    if not (current_dim+1) in all_dims.keys():
        all_dims[(current_dim+1)] = [[False]*5]*5
    if not (current_dim-1) in all_dims.keys():
        all_dims[(current_dim-1)] = [[False]*5]*5
    ud_grid, main_grid, ld_grid = all_dims[current_dim+1], all_dims[current_dim], all_dims[current_dim-1]

    # tile(s) above
    if r in (1, 2, 3, 4):
        if (r == 3) and (c == 2):  # sum of tiles in lower dimension
            for ic in range(5): rsum += ld_grid[4][ic]
        else:
            rsum += main_grid[r - 1][c]
    elif r == 0:  # one tile in upper dimension: row 1 column 2
        rsum += ud_grid[1][2]

    # tile(s) below
    if r in (0, 1, 2, 3):
        if (r == 1) and (c == 2): # sum of tiles in lower dimension
            for ic in range(5): rsum += ld_grid[0][ic]
        else:
            rsum += main_grid[r + 1][c]
    elif r == 4:  # one tile in upper dimension: row 3 column 2
        rsum += ud_grid[3][2]

    # tile(s) to the left
    if c in (1, 2, 3, 4):
        if (c == 3) and (r == 2):  # sum of tiles in lower dimension
            for ic in range(5): rsum += ld_grid[ic][4]
        else:
            rsum += main_grid[r][c - 1]
    elif c == 0:  # one tile in upper dimension: row 2, column 1
        rsum += ud_grid[2][1]

    # tile(s) to the right
    if c in (0, 1, 2, 3):
        if (c == 1) and (r == 2):  # sum of tile in lower dimension
            for ic in range(5): rsum += ld_grid[ic][0]
        else:
            rsum += main_grid[r][c + 1]
    elif c == 4:  # one tile in upper dimension: row 2, column 3
        rsum += ud_grid[2][3]

    return rsum


def run_bug_life_cycle_all_dims(all_dims, cmin):
    # print("running minute", cmin, "with dims", all_dims.keys())
    # initialize empty result
    result_all_dims = {}
    for k in all_dims.keys():
        result_all_dims[k] = [[False]*5]*5

    # run through dimensions from top to bottom
    # nb dims = 1 for 2 minutes, 2 after 4 mintues, ... => nb_dims_to_scan = (# minutes + 1) // 2
    nb_dims_to_scan = (cmin + 1) // 2
    for k in range(nb_dims_to_scan, -nb_dims_to_scan-1, -1):
        # print("scanning dimension", k)
        try:
            scan_grid = all_dims[k]
        except KeyError:
            scan_grid = [[False]*5]*5
        new_grid = []
        for r in range(len(scan_grid)):
            new_grid_line = []
            for c in range(len(scan_grid[0])):
                # print(r, c, get_nb_adjacent_bugs(grid, r, c))
                if scan_grid[r][c]:  # bug dies if exactly one bug adjacent
                    new_grid_line.append(get_nb_adjacent_bugs_in_dim(all_dims, k, r, c) == 1)
                else:  # infected if exactly 1 or 2 bugs
                    nb_bugs = get_nb_adjacent_bugs_in_dim(all_dims, k, r, c)
                    if nb_bugs == -1: print("oeps", cmin, k)
                    new_grid_line.append((nb_bugs == 1) or (nb_bugs == 2))
            new_grid.append(new_grid_line)
        result_all_dims[k] = cp.deepcopy(new_grid)
    return result_all_dims


empty_grid = [[False]*5]*5

all_dim_grid = {0: cp.copy(initial_gird)}
nb_minutes = 200
for i in range(nb_minutes):
    all_dim_grid = run_bug_life_cycle_all_dims(cp.copy(all_dim_grid), i+1)

adsum = 0
for g in all_dim_grid.keys():
    adsum += sum(sum(all_dim_grid[g],[]))
print("Solution part 2:", adsum)
