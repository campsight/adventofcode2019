import numpy as np
import copy as cp

#sys.setrecursionlimit(10000)

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

WALL = 0
STEP = 1
TARGET = 2
UNKNOWN = 3

FIELD_CHARS = ['#', '.', '0', '?']

FIELD_SIZE = 1000

center = FIELD_SIZE / 2
environment = np.zeros([FIELD_SIZE, FIELD_SIZE])
environment.fill(int(UNKNOWN))

def extract_modes(instruction):
    instruction_set = [int(x[0]) for x in instruction]
    # print(instruction_set)
    n = len(instruction_set)
    if (n == 1):
        opcode = instruction_set.pop()
        return [opcode]
    else:
        opcode = instruction_set.pop() + instruction_set.pop() * 10
        instruction_set.reverse()
        return ([opcode] + instruction_set)


# helper function to make process_step more readable
# 'solves' the instruction mode (value vs address) topic
def get_instruction_values(my_list, instruction_pointer, instruction_mode, nb_of_params=1, relative_base=0):
    while (len(instruction_mode) < (nb_of_params + 1)): instruction_mode.append(0)
    values = []
    for i in range(nb_of_params):
        param = my_list[instruction_pointer + i + 1]
        # 2 = relative mode: offset to relative position
        if instruction_mode[i + 1] == 0:  # position mode: param is value at the address
            values.append(my_list[param])
        elif instruction_mode[i + 1] == 2:  # relative mode: offset to relative position
            # print("relative mode: ", param, relative_base)
            values.append(my_list[param + relative_base])
        else:  # immediate mode: param is value itself
            values.append(param)
    return values


def get_store_pos(instruction_mode, nb_of_params, relative_base, normal_store_pos):
    while (len(instruction_mode) < (nb_of_params + 1)): instruction_mode.append(0)
    mode = instruction_mode.pop()
    if mode == 2: normal_store_pos += relative_base
    return normal_store_pos


# AoC 2019 processor. Input: a program (my_list), an instruction_pointer (pointing to next instruction), the inputs, outputs and haltcode
# haltcode = 1 to continue, 0 to wait for input and 99 if the program halts
def process_step(my_list, instruction_pointer, input=[], output=[], haltcode=1, relative_base=0):
    if (haltcode == 0): return (my_list, instruction_pointer, input, output, haltcode, relative_base)
    if (haltcode == 99): return (my_list, instruction_pointer, input, output, haltcode, relative_base)
    # print(instruction_pointer, output, my_list)
    instruction = my_list[instruction_pointer]
    instruction_mode = extract_modes(str(instruction))
    opcode = instruction_mode[0]
    if (opcode == 1):
        values = get_instruction_values(my_list, instruction_pointer, instruction_mode, 2, relative_base)
        store_pos = get_store_pos(instruction_mode, 3, relative_base, my_list[instruction_pointer + 3])
        my_list[store_pos] = values[0] + values[1]
        # return process_step(my_list, instruction_pointer + 4, input, output, 1, relative_base)
        return (my_list, instruction_pointer + 4, input, output, 1, relative_base)
    elif (opcode == 2):
        values = get_instruction_values(my_list, instruction_pointer, instruction_mode, 2, relative_base)
        store_pos = get_store_pos(instruction_mode, 3, relative_base, my_list[instruction_pointer + 3])
        my_list[store_pos] = values[0] * values[1]
        # return process_step(my_list, instruction_pointer + 4, input, output, 1, relative_base)
        return (my_list, instruction_pointer + 4, input, output, 1, relative_base)
    elif (opcode == 3):  # read input - but could be that it needs to wait if there is non
        store_pos = get_store_pos(instruction_mode, 1, relative_base, my_list[instruction_pointer + 1])
        if (len(input) > 0):
            my_list[store_pos] = input.pop(0)
            # return process_step(my_list, instruction_pointer + 2, input, output, 1, relative_base)
            return (my_list, instruction_pointer + 2, input, output, 1, relative_base)
        else:  # no input anymore => halt and don't move the instruction pointer
            # return process_step(my_list, instruction_pointer, input, output, 0, relative_base)
            return (my_list, instruction_pointer, input, output, 0, relative_base)
    elif (opcode == 4):  # output
        values = get_instruction_values(my_list, instruction_pointer, instruction_mode, 1, relative_base)
        output.append(values[0])
        # return process_step(my_list, instruction_pointer + 2, input, output, 1, relative_base)
        return (my_list, instruction_pointer + 2, input, output, 1, relative_base)
    elif ((opcode == 5) or (opcode == 6)):  # jump-if true(5) or false(6)
        values = get_instruction_values(my_list, instruction_pointer, instruction_mode, 2, relative_base)
        cond = values[0]
        if (((opcode == 5) and (cond != 0)) or ((opcode == 6) and (cond == 0))):
            # return process_step(my_list, values[1], input, output, 1, relative_base)
            return (my_list, values[1], input, output, 1, relative_base)
        else:
            # return process_step(my_list, instruction_pointer + 3, input, output, 1, relative_base)
            return (my_list, instruction_pointer + 3, input, output, 1, relative_base)
    elif ((opcode == 7) or (opcode == 8)):
        values = get_instruction_values(my_list, instruction_pointer, instruction_mode, 2, relative_base)
        store_pos = get_store_pos(instruction_mode, 3, relative_base, my_list[instruction_pointer + 3])
        if (((opcode == 7) and (values[0] < values[1])) or ((opcode == 8) and (values[0] == values[1]))):
            my_list[store_pos] = 1
        else:
            my_list[store_pos] = 0
        # return process_step(my_list, instruction_pointer + 4, input, output, 1, relative_base)
        return (my_list, instruction_pointer + 4, input, output, 1, relative_base)
    elif (opcode == 9):
        values = get_instruction_values(my_list, instruction_pointer, instruction_mode, 1, relative_base)
        relative_base += values[0]
        # return process_step(my_list, instruction_pointer + 2, input, output, 1, relative_base)
        return (my_list, instruction_pointer + 2, input, output, 1, relative_base)
    elif (opcode == 99):
        # print("finished", my_list)
        # return (my_list, output, instruction_pointer, input, 99)
        return (my_list, instruction_pointer, input, output, 99, relative_base)
    else:  # something went wrong
        print("Error, command unkonwn: ")
        # print(instruction_pointer)
        # print(my_list)
        # return process_step(my_list, instruction_pointer + 2, input, output, -1, relative_base)
        return my_list, instruction_pointer, input, output, -1, relative_base


def run_cycle(instructions, instruction_pointer, input, output, halt_code, relative_base):
    finished = False
    while not finished:
        result = process_step(instructions, instruction_pointer, input, output, halt_code, relative_base)
        instructions = result[0]
        instruction_pointer = result[1]
        input = result[2]
        output = result[3]
        halt_code = result[4]
        relative_base = result[5]
        # print(input, output, halt_code)
        if halt_code == 0: # set the input
            # print("halting because input is required")
            finished = True
        elif halt_code != 1:
            print("halting because of haltcode ", halt_code)
            finished = True
    return [instructions, instruction_pointer, input, output, halt_code, relative_base]


def get_adjacent_squares_with_directions(x, y):
    return [NORTH, x-1, y], [EAST, x, y+1], [SOUTH, x+1, y], [WEST, x, y-1]


def get_inverse_dir(gid_dir):
    if gid_dir == NORTH:
        return SOUTH
    elif gid_dir == EAST:
        return WEST
    elif gid_dir == SOUTH:
        return NORTH
    elif gid_dir == WEST:
        return EAST
    return -1


def print_environment(sizex, sizey):
    map = environment[(center-sizex):(center+sizex+1), (center-sizey):(center+sizey+1)]
    for line in map:
        print(''.join([FIELD_CHARS[int(x)] for x in line]))


def run_BFS_cycle(path, visited, walls, directions, depth_level, init_instructions, finished):
    depth_level += 1
    current_coord = path.pop(0)
    visited.append(current_coord)
    current_x = current_coord[0]
    current_y = current_coord[1]
    initial_set = cp.deepcopy(init_instructions)

    if (current_x != 0) or (current_y != 0):
        # print("sending robot from initial location with directions ", directions)
        # print("recursive call", [current_coord] + path, depth_level, len(directions[0]), directions)
        print("recursive call nb", depth_level, "with shortest path", len(directions[0]))
        directions_to_get_here = directions.pop(0)
        instruction_set = run_cycle(initial_set[0], initial_set[1], cp.copy(directions_to_get_here), [], 1, initial_set[5])
        # print("resulting in output", instruction_set[3])
    else:
        # print("recursive call", [current_coord], directions, depth_level)
        print("first recursive call")
        directions_to_get_here = []
        instruction_set = initial_set

    for square in get_adjacent_squares_with_directions(current_x, current_y):
        sdir, sx, sy = square[0], square[1], square[2]
        if ((sx, sy) in visited) or ((sx, sy) in walls):
            # print(sx, sy, "in visited or wall")
            continue
        else:
            instruction_set = run_cycle(instruction_set[0], instruction_set[1], [sdir], [], 1, instruction_set[5])
            el = instruction_set[3][0]
            # print("unknown element at", sx, sy, "is", el)
            # move back to current squarea - not required if its a wall
            if el != WALL:
                instruction_set = run_cycle(instruction_set[0], instruction_set[1], [get_inverse_dir(sdir)], [], 1, instruction_set[5])
                # print("back to", current_x, current_y)
        if el == WALL:
            visited.append((sx, sy))
            walls.append((sx, sy))
            continue
        elif el == TARGET:
            # print("********* Target found at: ", sx, sy, "after", depth_level, "iterations and going ", sdir)
            path.append((sx, sy))
            directions.append(directions_to_get_here + [sdir])
            print("********* Target found at: ", sx, sy, "at directions", len(directions_to_get_here)+1)
            # instruction_set[5] = 99 #nasty
            finished = True
            break
        elif (sx, sy) not in visited:
            # print("not in visited", sdir, sx, sy)
            # add to the path, but also add the directions to get there!
            path.append((sx, sy))
            directions.append(directions_to_get_here + [sdir])
    return [path, visited, walls, directions, depth_level, init_instructions, finished]


def run_BFS(path, visited, walls, directions, depth_level, init_instructions):
    result = [path, visited, walls, directions, depth_level, init_instructions, False]
    while not result[6]:
        result = run_BFS_cycle(result[0], result[1], result[2], result[3], result[4], result[5], result[6])
    print("finished...", len(result[3][0])+1)
    return result


def run_oxygen_cycle(path, oxygen_squares, visited, walls, directions, instructions_after_goto):
    current_coord = path.pop(0)
    oxygen_squares.append(current_coord)
    current_x = current_coord[0]
    current_y = current_coord[1]
    initial_set = cp.deepcopy(instructions_after_goto)

    # print("run oxygen cycle", [current_coord] + path, len(oxygen_squares), directions)

    if (current_x != 18) or (current_y != 16): # hard coded the robot initial coordinates here; might better be param
        # print("sending robot from goto location with directions ", directions)
        directions_to_get_here = directions.pop(0)
        instruction_set = run_cycle(initial_set[0], initial_set[1], cp.copy(directions_to_get_here), [], 1, initial_set[5])
    else:
        directions_to_get_here = []
        instruction_set = initial_set

    for square in get_adjacent_squares_with_directions(current_x, current_y):
        sdir, sx, sy = square[0], square[1], square[2]
        if ((sx, sy) in oxygen_squares) or ((sx, sy) in walls):
            # print(sx, sy, "in oxygen squares or walls")
            continue
        elif (sx, sy) in visited: #already visited in first part => sure that this is a normal square where oxygen can go
            # print("not in oxygen_squares [SHORTCUT]", sdir, sx, sy)
            path.append((sx, sy))
            directions.append(directions_to_get_here + [sdir])
            continue
        else:
            instruction_set = run_cycle(instruction_set[0], instruction_set[1], [sdir], [], 1, instruction_set[5])
            el = instruction_set[3][0]
            # print("unknown element at", sx, sy, "is", el)
            # move back to current squarea - not required if its a wall
            if el != WALL:
                instruction_set = run_cycle(instruction_set[0], instruction_set[1], [get_inverse_dir(sdir)], [], 1, instruction_set[5])
                # print("back to", current_x, current_y)
        if el == WALL:
            walls.append((sx, sy))
            continue
        else:
            # print("not in oxygen_squares", sdir, sx, sy)
            # add to the path, but also add the directions to get there!
            path.append((sx, sy))
            directions.append(directions_to_get_here + [sdir])

    return [path, oxygen_squares, visited, walls, directions, instructions_after_goto]


def run_oxygen(path, visited, walls, init_instructions):
    minutes_for_oxygen = 0
    new_path = path
    n_path_len = len(new_path)
    result = [path, [], visited, walls, [], init_instructions]
    while n_path_len > 0:
        minutes_for_oxygen += 1
        print("running minute", minutes_for_oxygen, "to spread oxygen to", new_path)
        for i in range(n_path_len):
            result = run_oxygen_cycle(result[0], result[1], result[2], result[3], result[4], result[5])
        new_path = result[0]
        n_path_len = len(new_path)

    # print("finished...", minutes_for_oxygen-1)
    return minutes_for_oxygen - 1


def run_program(instructions):
    init_instructions = [instructions, 0, [], [], 1, 0]  # instructions, pointer, input, output, haltcode, relative base
    init_path = [(0,0)]
    result_part1 = run_BFS(init_path, [], [], [], 0, init_instructions)
    goto_position = result_part1[0].pop()
    visited = result_part1[1]
    walls = result_part1[2]
    goto_directions = result_part1[3].pop()
    print(goto_position)
    print(goto_directions)
    print(visited)
    print(walls)
    # goto_position = [(18, 16)]
    # goto_directions = [1, 1, 1, 1, 4, 4, 1, 1, 4, 4, 2, 2, 2, 2, 4, 4, 4, 4, 2, 2, 3, 3, 3, 3, 3, 3, 2, 2, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2, 4, 4, 2, 2, 3, 3, 2, 2, 4, 4, 2, 2, 3, 3, 2, 2, 2, 2, 3, 3, 1, 1, 3, 3, 1, 1, 4, 4, 1, 1, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 4, 4, 1, 1, 1, 1, 3, 3, 2, 2, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 2, 2, 4, 4, 1, 1, 4, 4, 2, 2, 4, 4, 4, 4, 1, 1, 3, 3, 1, 1, 4, 4, 4, 4, 1, 1, 4, 4, 2, 2, 4, 4, 1, 1, 4, 4, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 3, 3, 1, 1, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 4, 4, 4, 4, 4, 4, 2, 2, 3, 3, 3, 3, 3, 3, 2, 2, 3, 3, 2, 2, 4, 4, 2, 2, 2, 2, 3, 3, 3, 3, 2, 2, 4, 4, 4, 4, 4, 4, 1, 1, 4, 4, 2, 2, 4, 4, 2, 2, 3, 3, 2, 2, 4, 4, 2, 2, 3, 3, 3, 3, 3, 3, 1, 1, 3, 3, 2, 2, 2, 2, 2, 2, 4, 4, 2, 2, 2, 2, 4, 4, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 2, 2, 3, 3, 2, 2, 4, 4, 2, 2, 3, 3]
    goto_instructions = run_cycle(instructions, 0, goto_directions, [], 1, 0)
    print("Solution part 1:", sum(goto_instructions[3])-1, goto_instructions[3][-1] == 2)
    minutes = run_oxygen([goto_position], visited, walls, goto_instructions)
    print("Solution part 2:", minutes)


repairdroid_program = [3, 1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,102,1,1034,1039,101,0,1036,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1105,1,124,1001,1034,0,1039,102,1,1036,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1106,0,124,1001,1034,-1,1039,1008,1036,0,1041,102,1,1035,1040,1002,1038,1,1043,101,0,1037,1042,1106,0,124,1001,1034,1,1039,1008,1036,0,1041,1002,1035,1,1040,102,1,1038,1043,101,0,1037,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,37,1032,1006,1032,165,1008,1040,39,1032,1006,1032,165,1102,2,1,1044,1106,0,224,2,1041,1043,1032,1006,1032,179,1101,0,1,1044,1105,1,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,74,1044,1106,0,224,1102,0,1,1044,1106,0,224,1006,1044,247,1002,1039,1,1034,102,1,1040,1035,1002,1041,1,1036,102,1,1043,1038,1001,1042,0,1037,4,1044,1106,0,0,4,35,96,8,87,44,67,40,80,25,91,53,86,23,96,7,76,76,10,30,90,46,47,40,93,75,3,17,1,19,89,7,92,47,95,3,92,39,72,69,6,18,86,94,19,82,98,9,7,91,42,86,29,83,65,43,91,71,92,16,96,82,5,81,6,92,93,76,71,17,91,91,73,64,33,27,89,4,99,81,80,6,57,87,9,42,99,97,13,42,81,82,72,68,35,93,2,99,6,6,94,2,39,39,86,43,97,77,86,21,56,75,61,91,82,56,94,32,47,90,33,72,93,13,87,12,42,68,99,71,34,97,79,87,99,79,25,42,95,97,51,93,80,33,71,68,89,50,49,78,77,24,93,70,13,11,56,29,18,77,77,94,60,80,75,84,42,87,90,58,84,27,78,3,80,70,85,79,4,36,94,65,79,93,94,13,97,75,49,92,15,84,5,85,35,67,96,87,64,32,83,97,20,89,64,18,93,32,46,91,57,53,75,56,7,56,92,99,36,22,93,19,25,29,48,86,94,68,18,95,79,87,97,55,75,44,65,82,99,31,94,42,53,81,72,85,70,93,47,40,77,60,85,87,11,60,98,25,90,88,93,93,85,64,43,88,96,36,83,14,98,40,48,11,18,80,97,49,23,2,91,85,50,88,94,41,75,99,84,15,45,9,81,83,96,51,56,58,76,72,50,94,59,76,87,10,25,88,73,99,20,95,46,93,88,2,50,89,86,26,18,85,72,85,75,66,83,25,97,96,25,94,14,34,94,89,57,88,78,17,92,59,40,29,84,87,55,61,81,9,82,93,17,33,81,81,58,43,91,68,86,80,61,83,23,46,78,60,14,94,79,28,91,57,79,83,48,92,5,49,97,81,56,53,84,42,58,93,20,71,29,29,89,88,34,31,87,92,78,62,78,72,93,3,54,97,82,38,32,89,86,88,38,19,84,51,99,60,90,95,14,78,11,82,89,12,87,98,70,79,33,76,44,97,79,33,19,34,83,58,4,89,21,88,78,46,78,76,66,61,92,91,38,86,27,61,86,46,52,97,44,80,89,53,55,47,83,34,44,97,37,41,92,28,70,95,82,91,76,8,99,2,80,1,66,96,71,94,1,44,89,29,13,99,35,80,89,31,91,19,77,46,85,77,93,61,31,62,14,92,82,73,94,86,20,31,94,72,73,44,61,91,79,40,88,69,85,6,83,96,49,12,77,39,83,91,24,70,13,81,57,39,88,38,23,80,43,92,67,46,87,25,80,93,82,68,98,93,63,85,29,18,78,94,27,89,85,20,63,89,93,96,99,50,71,97,15,28,53,78,85,78,82,64,67,14,94,47,96,65,58,81,20,91,36,82,55,11,85,87,59,84,6,67,87,69,88,81,68,38,84,52,33,79,97,69,89,89,34,96,18,78,67,87,36,93,57,77,77,21,47,99,27,26,79,7,88,37,90,33,25,96,66,83,24,30,82,84,16,82,85,15,55,92,20,80,92,38,20,34,87,67,11,84,28,42,93,26,54,89,85,78,82,60,14,9,76,85,10,80,80,50,85,29,86,20,61,81,80,51,32,88,91,92,34,56,79,58,76,41,47,89,24,40,90,85,88,30,48,91,42,2,91,95,98,60,79,40,86,61,79,81,23,91,91,12,21,78,54,75,61,11,79,89,73,84,13,95,81,6,52,92,37,76,65,82,84,87,40,94,70,78,71,83,46,94,2,79,57,80,35,99,21,83,81,93,64,81,78,99,57,87,49,87,41,92,83,82,58,92,0,0,21,21,1,10,1,0,0,0,0,0,0]
repairdroid_program = repairdroid_program + ([0]*100000)
run_program(repairdroid_program)

#nele_program = [3,1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,1002,1034,1,1039,102,1,1036,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1105,1,124,1002,1034,1,1039,101,0,1036,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1106,0,124,1001,1034,-1,1039,1008,1036,0,1041,101,0,1035,1040,1001,1038,0,1043,1001,1037,0,1042,1105,1,124,1001,1034,1,1039,1008,1036,0,1041,1002,1035,1,1040,102,1,1038,1043,101,0,1037,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,37,1032,1006,1032,165,1008,1040,37,1032,1006,1032,165,1102,1,2,1044,1106,0,224,2,1041,1043,1032,1006,1032,179,1101,1,0,1044,1105,1,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,73,1044,1105,1,224,1102,1,0,1044,1105,1,224,1006,1044,247,1002,1039,1,1034,1001,1040,0,1035,101,0,1041,1036,101,0,1043,1038,101,0,1042,1037,4,1044,1105,1,0,58,87,52,69,28,16,88,43,75,16,91,2,94,51,62,80,96,46,64,98,72,8,54,71,47,84,88,44,81,7,90,13,80,42,62,68,85,27,34,2,13,89,87,79,63,76,9,82,58,60,93,63,78,79,43,32,84,25,34,80,87,15,89,96,1,50,75,25,67,82,27,3,89,48,99,33,36,77,86,62,99,19,86,92,6,56,24,96,2,79,9,3,84,41,94,79,76,91,66,50,82,88,85,13,88,18,93,79,12,98,46,75,52,99,95,11,16,25,17,77,55,87,17,74,76,81,41,77,80,92,46,20,99,22,16,41,90,64,89,53,3,61,88,97,14,2,33,79,62,79,90,80,77,71,45,40,51,62,67,82,42,27,97,17,72,77,12,38,97,85,85,35,92,82,3,84,96,40,27,93,96,18,45,98,16,49,82,52,90,43,81,10,88,94,15,42,77,67,84,88,51,35,84,20,99,7,9,79,65,86,39,93,52,98,11,19,83,75,92,27,72,77,77,78,99,18,53,35,75,14,23,90,15,83,15,98,74,14,75,67,98,93,64,97,97,58,77,88,28,19,1,82,96,69,92,34,1,90,45,79,27,25,85,59,89,88,13,91,93,38,95,55,24,61,79,56,63,61,80,10,76,84,24,80,41,83,37,86,81,93,53,33,75,78,6,81,66,84,98,3,37,84,48,89,88,70,93,96,17,94,38,82,39,74,65,90,9,77,55,53,78,10,98,27,96,11,18,86,54,98,53,86,66,19,93,52,99,44,85,79,19,7,53,86,13,90,46,33,86,19,52,79,60,92,94,97,4,99,83,67,84,58,10,96,5,91,75,47,74,93,68,76,74,50,45,99,15,85,13,99,96,30,99,84,59,81,51,64,74,9,27,2,99,34,49,76,61,28,87,56,84,81,32,6,88,48,57,89,43,76,77,15,80,91,45,9,6,52,93,84,77,17,82,32,67,97,92,74,54,46,99,80,5,83,74,85,64,89,36,41,77,47,94,24,86,45,23,99,59,90,43,61,95,98,91,90,33,91,15,19,88,49,54,86,75,42,67,43,54,97,10,10,42,85,10,11,60,76,17,90,43,80,80,34,90,85,71,70,40,80,97,31,55,80,3,58,99,31,31,99,31,90,90,57,29,85,76,22,14,77,76,87,21,88,77,85,33,81,77,94,57,56,18,83,54,90,90,2,89,87,36,13,85,36,85,70,96,20,85,82,43,34,97,93,27,40,44,80,97,2,81,16,44,12,91,35,90,24,49,75,71,96,5,29,65,80,87,35,51,92,43,94,30,84,88,10,99,4,71,76,65,77,71,1,89,90,58,28,77,42,57,81,87,13,16,72,74,32,98,83,8,75,79,10,96,11,92,34,84,13,1,77,78,71,21,63,78,37,98,86,53,84,75,1,60,75,66,86,22,78,32,31,78,97,97,89,23,88,78,4,75,59,99,65,13,85,70,74,77,83,39,62,76,81,33,98,87,25,41,90,48,42,33,24,94,86,15,94,89,21,23,81,29,36,99,93,60,20,90,19,66,52,90,80,97,95,21,86,45,80,78,7,37,80,84,22,6,97,79,34,87,27,43,52,97,84,72,9,89,93,2,75,82,60,92,12,87,89,59,74,64,90,38,71,89,12,26,81,6,53,78,96,8,81,91,69,68,89,76,79,50,77,19,83,14,75,26,76,34,78,1,83,70,80,39,99,62,95,89,99,6,79,93,80,10,83,50,79,80,92,41,78,20,86,9,84,53,87,13,74,0,0,21,21,1,10,1,0,0,0,0,0,0]
#nele_program = nele_program + ([0]*100000)
#run_program(nele_program)
