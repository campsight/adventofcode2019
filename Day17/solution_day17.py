import numpy as np

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

CHANGE_DIRS = [['?', 'R', '?', 'L'], ['L', '?', 'R', '?'], ['?', 'L', '?', 'R'], ['R', '?', 'L', '?']]

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
        if halt_code == 0:  # set the input
            # print("halting because input is required")
            finished = True
        elif halt_code != 1:
            print("halting because of haltcode ", halt_code)
            finished = True
    return [instructions, instruction_pointer, input, output, halt_code, relative_base]


def get_cleaning_instructions(raw_input):

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

    def get_adjacents(dpos, dgrid, exclude_dir):
        drow = dpos[0]
        dcol = dpos[1]
        adjacents = []
        if (drow > 0) and (exclude_dir != NORTH):
            adjacents.append((NORTH, grid[drow-1, dcol]))
        if (dcol < (len(dgrid[0])-1)) and (exclude_dir != EAST):
            adjacents.append((EAST, grid[drow, dcol+1]))
        if (drow < (len(dgrid)-1)) and (exclude_dir != SOUTH):
            adjacents.append((SOUTH, grid[drow+1,dcol]))
        if (dcol > 0) and (exclude_dir != WEST):
            adjacents.append((WEST, grid[drow, dcol-1]))
        return adjacents

    def determine_direction(dgrid, dpos, fromdir):
        d_adjacents = get_adjacents(dpos, dgrid, get_inverse_dir(fromdir))
        new_direction = -1
        try:
            helper = [x[1] for x in d_adjacents]
            new_direction = d_adjacents[helper.index('#')][0]
        except ValueError:
            print("Error, no now direction found - or final step taken", d_adjacents)
        return new_direction

    def determine_endpos(c_robot_pos, c_direction, c_grid):
        c_row = c_robot_pos[0]
        c_col = c_robot_pos[1]
        n_row = 0
        n_col = 0
        steps = 0
        search_array = []
        if c_direction == NORTH:
            n_col = c_col
            search_array = [r[c_col] for r in c_grid][0:c_row]
            search_array = search_array[::-1]
            try:
                n_row = (c_row - search_array.index('.'))
            except ValueError:
                n_row = 0
            steps = c_row - n_row
        elif c_direction == SOUTH:
            n_col = c_col
            search_array = [r[c_col] for r in c_grid][(c_row + 1):len(grid)]
            try:
                n_row = (c_row + search_array.index('.'))
            except ValueError:
                n_row = len(grid) - 1
            steps = n_row - c_row
        elif c_direction == EAST:
            n_row = c_row
            search_array = grid[c_row][(c_col + 1):len(grid[0])]
            try:
                n_col = (c_col + search_array.tostring().index('.'))
            except ValueError:
                n_col = len(grid[0]) - 1
            steps = n_col - c_col
        elif c_direction == WEST:
            n_row = c_row
            search_array = grid[c_row][0:c_col]
            search_array = search_array[::-1]
            try:
                n_col = (c_col - search_array.tostring().index('.'))
            except ValueError:
                n_col = 0
            steps = c_col - n_col
        return [steps,(n_row, n_col)]


    line = len(raw_input)
    cols = raw_input.index(10)
    rows = line // (cols + 1)
    raw_input.pop()
    raw_input = [chr(x) for x in raw_input]
    grid = np.chararray(line - 1)
    for i in range(line - 1): grid[i] = raw_input[i]
    grid = grid.reshape((rows, (cols + 1)))
    print(grid)
    for line in grid:
        print(''.join(line))
    sum = 0
    robot_pos = (-1,-1)
    for r in range(1, len(grid) - 1):
        for c in range(1, len(grid[0]) - 1):
            if (grid[r, c] == '#') and (grid[r - 1, c] == '#') and (grid[r, c - 1] == '#') and (
                    grid[r + 1, c] == '#') and (grid[r, c + 1] == '#'):
                #print("found intersection at", r, c)
                sum += r * c
            if grid[r, c] == '^':
                #print("robot at", r, c)
                robot_pos = (r, c)
    print("Solution part 1:", sum)
    print("Solution starting from ^", robot_pos)
    continue_movement = True
    prv_direction = NORTH  # type: int
    ascii_instructions = []
    while continue_movement:
        nxt_direction = determine_direction(grid, robot_pos, prv_direction)
        if nxt_direction == -1:
            continue_movement = False
        else:
            nxt_step = determine_endpos(robot_pos, nxt_direction, grid)
            ascii_instructions.append((CHANGE_DIRS[prv_direction][nxt_direction], nxt_step[0]))
            robot_pos, prv_direction = nxt_step[1], nxt_direction
    # print("Instruction set:")
    # print(ascii_instructions)
    # print(len(ascii_instructions))
    ascii_string_array = [x[0] + ',' + str(x[1]) for x in ascii_instructions]
    print("Instruction set full:", ','.join(ascii_string_array))
    substring_a = "L,10,R,10,L,10,L,10" + chr(10)
    substring_b = "R,10,R,12,L,12" + chr(10)
    substring_c = "R,12,L,12,R,6" + chr(10)
    program_string = "A,B,A,B,C,C,B,A,B,C" + chr(10)
    # print(program_string, substring_a, substring_b, substring_c)
    program_input = [ord(c) for c in program_string]
    substring_a_input = [ord(c) for c in substring_a]
    substring_b_input = [ord(c) for c in substring_b]
    substring_c_input = [ord(c) for c in substring_c]
    enable_livefeed_input = [ord('n'), 10]
    instruction_set = program_input + substring_a_input + substring_b_input + substring_c_input + enable_livefeed_input
    return instruction_set


def run_program(instructions, cleaning_program):
    instruction_pointer = 0
    input = []
    output = []
    relative_base = 0
    halt_code = 1
    result = run_cycle(instructions, instruction_pointer, input, output, halt_code, relative_base)
    #print(result[3])
    cleaning_instructions = get_cleaning_instructions(result[3])
    result = run_cycle(cleaning_program, 0, cleaning_instructions, [], 1, 0)
    print("Solution part 2:", result[3][-1])


ascii_program = [1, 330, 331, 332, 109, 6690, 1102, 1, 1182, 16, 1102, 1, 1505, 24, 102, 1, 0, 570, 1006, 570, 36, 1002,
                 571, 1, 0, 1001, 570, -1, 570, 1001, 24, 1, 24, 1106, 0, 18, 1008, 571, 0, 571, 1001, 16, 1, 16, 1008,
                 16, 1505, 570, 1006, 570, 14, 21102, 58, 1, 0, 1105, 1, 786, 1006, 332, 62, 99, 21101, 333, 0, 1,
                 21102, 73, 1, 0, 1105, 1, 579, 1102, 0, 1, 572, 1101, 0, 0, 573, 3, 574, 101, 1, 573, 573, 1007, 574,
                 65, 570, 1005, 570, 151, 107, 67, 574, 570, 1005, 570, 151, 1001, 574, -64, 574, 1002, 574, -1, 574,
                 1001, 572, 1, 572, 1007, 572, 11, 570, 1006, 570, 165, 101, 1182, 572, 127, 1002, 574, 1, 0, 3, 574,
                 101, 1, 573, 573, 1008, 574, 10, 570, 1005, 570, 189, 1008, 574, 44, 570, 1006, 570, 158, 1106, 0, 81,
                 21101, 340, 0, 1, 1106, 0, 177, 21102, 1, 477, 1, 1106, 0, 177, 21101, 0, 514, 1, 21102, 1, 176, 0,
                 1106, 0, 579, 99, 21101, 0, 184, 0, 1105, 1, 579, 4, 574, 104, 10, 99, 1007, 573, 22, 570, 1006, 570,
                 165, 1001, 572, 0, 1182, 21101, 375, 0, 1, 21102, 211, 1, 0, 1106, 0, 579, 21101, 1182, 11, 1, 21101,
                 222, 0, 0, 1105, 1, 979, 21101, 388, 0, 1, 21101, 0, 233, 0, 1105, 1, 579, 21101, 1182, 22, 1, 21102,
                 1, 244, 0, 1105, 1, 979, 21101, 401, 0, 1, 21101, 255, 0, 0, 1105, 1, 579, 21101, 1182, 33, 1, 21101,
                 0, 266, 0, 1105, 1, 979, 21101, 0, 414, 1, 21101, 277, 0, 0, 1106, 0, 579, 3, 575, 1008, 575, 89, 570,
                 1008, 575, 121, 575, 1, 575, 570, 575, 3, 574, 1008, 574, 10, 570, 1006, 570, 291, 104, 10, 21101,
                 1182, 0, 1, 21102, 1, 313, 0, 1106, 0, 622, 1005, 575, 327, 1101, 0, 1, 575, 21101, 327, 0, 0, 1106, 0,
                 786, 4, 438, 99, 0, 1, 1, 6, 77, 97, 105, 110, 58, 10, 33, 10, 69, 120, 112, 101, 99, 116, 101, 100,
                 32, 102, 117, 110, 99, 116, 105, 111, 110, 32, 110, 97, 109, 101, 32, 98, 117, 116, 32, 103, 111, 116,
                 58, 32, 0, 12, 70, 117, 110, 99, 116, 105, 111, 110, 32, 65, 58, 10, 12, 70, 117, 110, 99, 116, 105,
                 111, 110, 32, 66, 58, 10, 12, 70, 117, 110, 99, 116, 105, 111, 110, 32, 67, 58, 10, 23, 67, 111, 110,
                 116, 105, 110, 117, 111, 117, 115, 32, 118, 105, 100, 101, 111, 32, 102, 101, 101, 100, 63, 10, 0, 37,
                 10, 69, 120, 112, 101, 99, 116, 101, 100, 32, 82, 44, 32, 76, 44, 32, 111, 114, 32, 100, 105, 115, 116,
                 97, 110, 99, 101, 32, 98, 117, 116, 32, 103, 111, 116, 58, 32, 36, 10, 69, 120, 112, 101, 99, 116, 101,
                 100, 32, 99, 111, 109, 109, 97, 32, 111, 114, 32, 110, 101, 119, 108, 105, 110, 101, 32, 98, 117, 116,
                 32, 103, 111, 116, 58, 32, 43, 10, 68, 101, 102, 105, 110, 105, 116, 105, 111, 110, 115, 32, 109, 97,
                 121, 32, 98, 101, 32, 97, 116, 32, 109, 111, 115, 116, 32, 50, 48, 32, 99, 104, 97, 114, 97, 99, 116,
                 101, 114, 115, 33, 10, 94, 62, 118, 60, 0, 1, 0, -1, -1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 84, 18, 0, 109, 4,
                 2101, 0, -3, 587, 20102, 1, 0, -1, 22101, 1, -3, -3, 21102, 1, 0, -2, 2208, -2, -1, 570, 1005, 570,
                 617, 2201, -3, -2, 609, 4, 0, 21201, -2, 1, -2, 1106, 0, 597, 109, -4, 2106, 0, 0, 109, 5, 2102, 1, -4,
                 629, 21001, 0, 0, -2, 22101, 1, -4, -4, 21102, 1, 0, -3, 2208, -3, -2, 570, 1005, 570, 781, 2201, -4,
                 -3, 652, 21001, 0, 0, -1, 1208, -1, -4, 570, 1005, 570, 709, 1208, -1, -5, 570, 1005, 570, 734, 1207,
                 -1, 0, 570, 1005, 570, 759, 1206, -1, 774, 1001, 578, 562, 684, 1, 0, 576, 576, 1001, 578, 566, 692, 1,
                 0, 577, 577, 21101, 702, 0, 0, 1106, 0, 786, 21201, -1, -1, -1, 1106, 0, 676, 1001, 578, 1, 578, 1008,
                 578, 4, 570, 1006, 570, 724, 1001, 578, -4, 578, 21101, 0, 731, 0, 1106, 0, 786, 1105, 1, 774, 1001,
                 578, -1, 578, 1008, 578, -1, 570, 1006, 570, 749, 1001, 578, 4, 578, 21102, 756, 1, 0, 1106, 0, 786,
                 1106, 0, 774, 21202, -1, -11, 1, 22101, 1182, 1, 1, 21102, 1, 774, 0, 1106, 0, 622, 21201, -3, 1, -3,
                 1105, 1, 640, 109, -5, 2105, 1, 0, 109, 7, 1005, 575, 802, 20101, 0, 576, -6, 21002, 577, 1, -5, 1106,
                 0, 814, 21102, 0, 1, -1, 21102, 0, 1, -5, 21102, 1, 0, -6, 20208, -6, 576, -2, 208, -5, 577, 570,
                 22002, 570, -2, -2, 21202, -5, 85, -3, 22201, -6, -3, -3, 22101, 1505, -3, -3, 1201, -3, 0, 843, 1005,
                 0, 863, 21202, -2, 42, -4, 22101, 46, -4, -4, 1206, -2, 924, 21101, 0, 1, -1, 1105, 1, 924, 1205, -2,
                 873, 21101, 0, 35, -4, 1105, 1, 924, 2101, 0, -3, 878, 1008, 0, 1, 570, 1006, 570, 916, 1001, 374, 1,
                 374, 2102, 1, -3, 895, 1102, 1, 2, 0, 2101, 0, -3, 902, 1001, 438, 0, 438, 2202, -6, -5, 570, 1, 570,
                 374, 570, 1, 570, 438, 438, 1001, 578, 558, 922, 20101, 0, 0, -4, 1006, 575, 959, 204, -4, 22101, 1,
                 -6, -6, 1208, -6, 85, 570, 1006, 570, 814, 104, 10, 22101, 1, -5, -5, 1208, -5, 61, 570, 1006, 570,
                 810, 104, 10, 1206, -1, 974, 99, 1206, -1, 974, 1101, 0, 1, 575, 21102, 973, 1, 0, 1105, 1, 786, 99,
                 109, -7, 2106, 0, 0, 109, 6, 21101, 0, 0, -4, 21102, 0, 1, -3, 203, -2, 22101, 1, -3, -3, 21208, -2,
                 82, -1, 1205, -1, 1030, 21208, -2, 76, -1, 1205, -1, 1037, 21207, -2, 48, -1, 1205, -1, 1124, 22107,
                 57, -2, -1, 1205, -1, 1124, 21201, -2, -48, -2, 1106, 0, 1041, 21101, 0, -4, -2, 1105, 1, 1041, 21101,
                 0, -5, -2, 21201, -4, 1, -4, 21207, -4, 11, -1, 1206, -1, 1138, 2201, -5, -4, 1059, 2101, 0, -2, 0,
                 203, -2, 22101, 1, -3, -3, 21207, -2, 48, -1, 1205, -1, 1107, 22107, 57, -2, -1, 1205, -1, 1107, 21201,
                 -2, -48, -2, 2201, -5, -4, 1090, 20102, 10, 0, -1, 22201, -2, -1, -2, 2201, -5, -4, 1103, 1202, -2, 1,
                 0, 1105, 1, 1060, 21208, -2, 10, -1, 1205, -1, 1162, 21208, -2, 44, -1, 1206, -1, 1131, 1106, 0, 989,
                 21101, 0, 439, 1, 1106, 0, 1150, 21102, 477, 1, 1, 1106, 0, 1150, 21101, 0, 514, 1, 21101, 1149, 0, 0,
                 1106, 0, 579, 99, 21101, 0, 1157, 0, 1105, 1, 579, 204, -2, 104, 10, 99, 21207, -3, 22, -1, 1206, -1,
                 1138, 1202, -5, 1, 1176, 1202, -4, 1, 0, 109, -6, 2106, 0, 0, 46, 7, 78, 1, 84, 1, 84, 1, 84, 1, 84, 1,
                 80, 13, 72, 1, 3, 1, 7, 1, 72, 1, 3, 1, 7, 1, 9, 11, 52, 1, 3, 1, 7, 1, 9, 1, 9, 1, 52, 1, 3, 1, 7, 1,
                 9, 1, 9, 1, 52, 1, 3, 1, 7, 1, 9, 1, 9, 1, 44, 13, 7, 1, 9, 1, 9, 1, 44, 1, 7, 1, 11, 1, 9, 1, 9, 1,
                 44, 1, 7, 1, 11, 1, 9, 1, 9, 1, 44, 1, 7, 1, 11, 1, 9, 1, 9, 1, 42, 11, 11, 1, 9, 1, 9, 1, 42, 1, 1, 1,
                 19, 1, 9, 1, 9, 1, 42, 1, 1, 1, 19, 11, 9, 11, 32, 1, 1, 1, 82, 1, 1, 1, 82, 1, 1, 1, 82, 1, 1, 1, 82,
                 1, 1, 1, 72, 13, 72, 1, 9, 1, 74, 1, 9, 11, 64, 1, 19, 1, 64, 1, 19, 1, 64, 1, 19, 1, 64, 1, 19, 1, 64,
                 1, 19, 1, 64, 1, 19, 1, 64, 1, 19, 1, 64, 11, 9, 1, 74, 1, 9, 1, 72, 13, 72, 1, 1, 1, 82, 1, 1, 1, 82,
                 1, 1, 1, 82, 1, 1, 1, 82, 1, 1, 1, 52, 11, 19, 1, 1, 1, 52, 1, 9, 1, 19, 1, 1, 1, 52, 1, 9, 1, 11, 11,
                 52, 1, 9, 1, 11, 1, 7, 1, 54, 1, 9, 1, 11, 1, 7, 1, 54, 1, 9, 1, 11, 1, 7, 1, 54, 13, 5, 13, 64, 1, 1,
                 1, 5, 1, 3, 1, 72, 1, 1, 1, 5, 1, 3, 1, 72, 1, 1, 1, 5, 1, 3, 1, 72, 1, 1, 1, 5, 1, 3, 1, 72, 1, 1, 1,
                 5, 1, 3, 1, 72, 13, 74, 1, 5, 1, 78, 1, 5, 1, 78, 1, 5, 1, 78, 1, 5, 1, 78, 1, 5, 1, 78, 7, 66]
ascii_program = ascii_program + ([0] * 100000)

ascii_program2 = [2, 330, 331, 332, 109, 6690, 1102, 1, 1182, 16, 1102, 1, 1505, 24, 102, 1, 0, 570, 1006, 570, 36, 1002,
                 571, 1, 0, 1001, 570, -1, 570, 1001, 24, 1, 24, 1106, 0, 18, 1008, 571, 0, 571, 1001, 16, 1, 16, 1008,
                 16, 1505, 570, 1006, 570, 14, 21102, 58, 1, 0, 1105, 1, 786, 1006, 332, 62, 99, 21101, 333, 0, 1,
                 21102, 73, 1, 0, 1105, 1, 579, 1102, 0, 1, 572, 1101, 0, 0, 573, 3, 574, 101, 1, 573, 573, 1007, 574,
                 65, 570, 1005, 570, 151, 107, 67, 574, 570, 1005, 570, 151, 1001, 574, -64, 574, 1002, 574, -1, 574,
                 1001, 572, 1, 572, 1007, 572, 11, 570, 1006, 570, 165, 101, 1182, 572, 127, 1002, 574, 1, 0, 3, 574,
                 101, 1, 573, 573, 1008, 574, 10, 570, 1005, 570, 189, 1008, 574, 44, 570, 1006, 570, 158, 1106, 0, 81,
                 21101, 340, 0, 1, 1106, 0, 177, 21102, 1, 477, 1, 1106, 0, 177, 21101, 0, 514, 1, 21102, 1, 176, 0,
                 1106, 0, 579, 99, 21101, 0, 184, 0, 1105, 1, 579, 4, 574, 104, 10, 99, 1007, 573, 22, 570, 1006, 570,
                 165, 1001, 572, 0, 1182, 21101, 375, 0, 1, 21102, 211, 1, 0, 1106, 0, 579, 21101, 1182, 11, 1, 21101,
                 222, 0, 0, 1105, 1, 979, 21101, 388, 0, 1, 21101, 0, 233, 0, 1105, 1, 579, 21101, 1182, 22, 1, 21102,
                 1, 244, 0, 1105, 1, 979, 21101, 401, 0, 1, 21101, 255, 0, 0, 1105, 1, 579, 21101, 1182, 33, 1, 21101,
                 0, 266, 0, 1105, 1, 979, 21101, 0, 414, 1, 21101, 277, 0, 0, 1106, 0, 579, 3, 575, 1008, 575, 89, 570,
                 1008, 575, 121, 575, 1, 575, 570, 575, 3, 574, 1008, 574, 10, 570, 1006, 570, 291, 104, 10, 21101,
                 1182, 0, 1, 21102, 1, 313, 0, 1106, 0, 622, 1005, 575, 327, 1101, 0, 1, 575, 21101, 327, 0, 0, 1106, 0,
                 786, 4, 438, 99, 0, 1, 1, 6, 77, 97, 105, 110, 58, 10, 33, 10, 69, 120, 112, 101, 99, 116, 101, 100,
                 32, 102, 117, 110, 99, 116, 105, 111, 110, 32, 110, 97, 109, 101, 32, 98, 117, 116, 32, 103, 111, 116,
                 58, 32, 0, 12, 70, 117, 110, 99, 116, 105, 111, 110, 32, 65, 58, 10, 12, 70, 117, 110, 99, 116, 105,
                 111, 110, 32, 66, 58, 10, 12, 70, 117, 110, 99, 116, 105, 111, 110, 32, 67, 58, 10, 23, 67, 111, 110,
                 116, 105, 110, 117, 111, 117, 115, 32, 118, 105, 100, 101, 111, 32, 102, 101, 101, 100, 63, 10, 0, 37,
                 10, 69, 120, 112, 101, 99, 116, 101, 100, 32, 82, 44, 32, 76, 44, 32, 111, 114, 32, 100, 105, 115, 116,
                 97, 110, 99, 101, 32, 98, 117, 116, 32, 103, 111, 116, 58, 32, 36, 10, 69, 120, 112, 101, 99, 116, 101,
                 100, 32, 99, 111, 109, 109, 97, 32, 111, 114, 32, 110, 101, 119, 108, 105, 110, 101, 32, 98, 117, 116,
                 32, 103, 111, 116, 58, 32, 43, 10, 68, 101, 102, 105, 110, 105, 116, 105, 111, 110, 115, 32, 109, 97,
                 121, 32, 98, 101, 32, 97, 116, 32, 109, 111, 115, 116, 32, 50, 48, 32, 99, 104, 97, 114, 97, 99, 116,
                 101, 114, 115, 33, 10, 94, 62, 118, 60, 0, 1, 0, -1, -1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 84, 18, 0, 109, 4,
                 2101, 0, -3, 587, 20102, 1, 0, -1, 22101, 1, -3, -3, 21102, 1, 0, -2, 2208, -2, -1, 570, 1005, 570,
                 617, 2201, -3, -2, 609, 4, 0, 21201, -2, 1, -2, 1106, 0, 597, 109, -4, 2106, 0, 0, 109, 5, 2102, 1, -4,
                 629, 21001, 0, 0, -2, 22101, 1, -4, -4, 21102, 1, 0, -3, 2208, -3, -2, 570, 1005, 570, 781, 2201, -4,
                 -3, 652, 21001, 0, 0, -1, 1208, -1, -4, 570, 1005, 570, 709, 1208, -1, -5, 570, 1005, 570, 734, 1207,
                 -1, 0, 570, 1005, 570, 759, 1206, -1, 774, 1001, 578, 562, 684, 1, 0, 576, 576, 1001, 578, 566, 692, 1,
                 0, 577, 577, 21101, 702, 0, 0, 1106, 0, 786, 21201, -1, -1, -1, 1106, 0, 676, 1001, 578, 1, 578, 1008,
                 578, 4, 570, 1006, 570, 724, 1001, 578, -4, 578, 21101, 0, 731, 0, 1106, 0, 786, 1105, 1, 774, 1001,
                 578, -1, 578, 1008, 578, -1, 570, 1006, 570, 749, 1001, 578, 4, 578, 21102, 756, 1, 0, 1106, 0, 786,
                 1106, 0, 774, 21202, -1, -11, 1, 22101, 1182, 1, 1, 21102, 1, 774, 0, 1106, 0, 622, 21201, -3, 1, -3,
                 1105, 1, 640, 109, -5, 2105, 1, 0, 109, 7, 1005, 575, 802, 20101, 0, 576, -6, 21002, 577, 1, -5, 1106,
                 0, 814, 21102, 0, 1, -1, 21102, 0, 1, -5, 21102, 1, 0, -6, 20208, -6, 576, -2, 208, -5, 577, 570,
                 22002, 570, -2, -2, 21202, -5, 85, -3, 22201, -6, -3, -3, 22101, 1505, -3, -3, 1201, -3, 0, 843, 1005,
                 0, 863, 21202, -2, 42, -4, 22101, 46, -4, -4, 1206, -2, 924, 21101, 0, 1, -1, 1105, 1, 924, 1205, -2,
                 873, 21101, 0, 35, -4, 1105, 1, 924, 2101, 0, -3, 878, 1008, 0, 1, 570, 1006, 570, 916, 1001, 374, 1,
                 374, 2102, 1, -3, 895, 1102, 1, 2, 0, 2101, 0, -3, 902, 1001, 438, 0, 438, 2202, -6, -5, 570, 1, 570,
                 374, 570, 1, 570, 438, 438, 1001, 578, 558, 922, 20101, 0, 0, -4, 1006, 575, 959, 204, -4, 22101, 1,
                 -6, -6, 1208, -6, 85, 570, 1006, 570, 814, 104, 10, 22101, 1, -5, -5, 1208, -5, 61, 570, 1006, 570,
                 810, 104, 10, 1206, -1, 974, 99, 1206, -1, 974, 1101, 0, 1, 575, 21102, 973, 1, 0, 1105, 1, 786, 99,
                 109, -7, 2106, 0, 0, 109, 6, 21101, 0, 0, -4, 21102, 0, 1, -3, 203, -2, 22101, 1, -3, -3, 21208, -2,
                 82, -1, 1205, -1, 1030, 21208, -2, 76, -1, 1205, -1, 1037, 21207, -2, 48, -1, 1205, -1, 1124, 22107,
                 57, -2, -1, 1205, -1, 1124, 21201, -2, -48, -2, 1106, 0, 1041, 21101, 0, -4, -2, 1105, 1, 1041, 21101,
                 0, -5, -2, 21201, -4, 1, -4, 21207, -4, 11, -1, 1206, -1, 1138, 2201, -5, -4, 1059, 2101, 0, -2, 0,
                 203, -2, 22101, 1, -3, -3, 21207, -2, 48, -1, 1205, -1, 1107, 22107, 57, -2, -1, 1205, -1, 1107, 21201,
                 -2, -48, -2, 2201, -5, -4, 1090, 20102, 10, 0, -1, 22201, -2, -1, -2, 2201, -5, -4, 1103, 1202, -2, 1,
                 0, 1105, 1, 1060, 21208, -2, 10, -1, 1205, -1, 1162, 21208, -2, 44, -1, 1206, -1, 1131, 1106, 0, 989,
                 21101, 0, 439, 1, 1106, 0, 1150, 21102, 477, 1, 1, 1106, 0, 1150, 21101, 0, 514, 1, 21101, 1149, 0, 0,
                 1106, 0, 579, 99, 21101, 0, 1157, 0, 1105, 1, 579, 204, -2, 104, 10, 99, 21207, -3, 22, -1, 1206, -1,
                 1138, 1202, -5, 1, 1176, 1202, -4, 1, 0, 109, -6, 2106, 0, 0, 46, 7, 78, 1, 84, 1, 84, 1, 84, 1, 84, 1,
                 80, 13, 72, 1, 3, 1, 7, 1, 72, 1, 3, 1, 7, 1, 9, 11, 52, 1, 3, 1, 7, 1, 9, 1, 9, 1, 52, 1, 3, 1, 7, 1,
                 9, 1, 9, 1, 52, 1, 3, 1, 7, 1, 9, 1, 9, 1, 44, 13, 7, 1, 9, 1, 9, 1, 44, 1, 7, 1, 11, 1, 9, 1, 9, 1,
                 44, 1, 7, 1, 11, 1, 9, 1, 9, 1, 44, 1, 7, 1, 11, 1, 9, 1, 9, 1, 42, 11, 11, 1, 9, 1, 9, 1, 42, 1, 1, 1,
                 19, 1, 9, 1, 9, 1, 42, 1, 1, 1, 19, 11, 9, 11, 32, 1, 1, 1, 82, 1, 1, 1, 82, 1, 1, 1, 82, 1, 1, 1, 82,
                 1, 1, 1, 72, 13, 72, 1, 9, 1, 74, 1, 9, 11, 64, 1, 19, 1, 64, 1, 19, 1, 64, 1, 19, 1, 64, 1, 19, 1, 64,
                 1, 19, 1, 64, 1, 19, 1, 64, 1, 19, 1, 64, 11, 9, 1, 74, 1, 9, 1, 72, 13, 72, 1, 1, 1, 82, 1, 1, 1, 82,
                 1, 1, 1, 82, 1, 1, 1, 82, 1, 1, 1, 52, 11, 19, 1, 1, 1, 52, 1, 9, 1, 19, 1, 1, 1, 52, 1, 9, 1, 11, 11,
                 52, 1, 9, 1, 11, 1, 7, 1, 54, 1, 9, 1, 11, 1, 7, 1, 54, 1, 9, 1, 11, 1, 7, 1, 54, 13, 5, 13, 64, 1, 1,
                 1, 5, 1, 3, 1, 72, 1, 1, 1, 5, 1, 3, 1, 72, 1, 1, 1, 5, 1, 3, 1, 72, 1, 1, 1, 5, 1, 3, 1, 72, 1, 1, 1,
                 5, 1, 3, 1, 72, 13, 74, 1, 5, 1, 78, 1, 5, 1, 78, 1, 5, 1, 78, 1, 5, 1, 78, 1, 5, 1, 78, 7, 66]
ascii_program2 = ascii_program2 + ([0] * 100000)

run_program(ascii_program, ascii_program2)
