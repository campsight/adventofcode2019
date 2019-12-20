import copy as cp
import numpy as np

PRINTCHAR = [".", "#"]

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


def run_program_part1(instructions):
    dim = 50
    scan = np.zeros((dim, dim))
    shift_points_r = {}
    shift_points_c = {}
    shift_c = 0
    print(scan)
    for i in range(dim):
        shift_r = 0
        for j in range(dim):
            print(i,j)
            init_program = cp.deepcopy(instructions)
            scan[i][j] = run_cycle(init_program, 0, [i,j], [], 1, 0)[3][0]
            if scan[i][j] and (j > 0) and (i > 0):
                if not scan[i][j-1]:
                    shift_points_r[i] = j
                    shift_r = j
                if not scan[i-1][j]:
                    shift_points_c[j] = i
                    shift_c = i
            if not scan[i][j] and (i in shift_points_r.keys()) and (j > shift_r):
                if (j > 0) and scan[i][j-1]:
                    shift_points_r[i] = j - shift_points_r[i]
            if not scan[i][j] and (j in shift_points_c.keys()) and (i > shift_c):
                if (i > 0) and scan[i-1][j]:
                    shift_points_c[j] = i - shift_points_c[j]

    print(shift_points_r)
    print(shift_points_c)
    print(shift_points_r.values())
    print(shift_points_c.values())
    for i in range(1, max(shift_points_r.values())+1):
        print(list(shift_points_r.keys())[list(shift_points_r.values()).index(i)])

    for i in range(len(scan)):
        line = [PRINTCHAR[int(x)] for x in scan[i]]
        print(''.join(line))
    print("Solution part 1:", np.sum(scan))


drone_program = [109,424,203,1,21102,11,1,0,1106,0,282,21102,18,1,0,1105,1,259,1202,1,1,221,203,1,21102,31,1,0,1106,0,282,21101,38,0,0,1106,0,259,21002,23,1,2,22102,1,1,3,21102,1,1,1,21102,1,57,0,1105,1,303,2101,0,1,222,21002,221,1,3,20101,0,221,2,21101,0,259,1,21102,1,80,0,1105,1,225,21102,1,8,2,21101,91,0,0,1106,0,303,1202,1,1,223,21002,222,1,4,21102,1,259,3,21101,225,0,2,21101,225,0,1,21101,0,118,0,1105,1,225,21001,222,0,3,21101,0,48,2,21102,133,1,0,1106,0,303,21202,1,-1,1,22001,223,1,1,21102,1,148,0,1105,1,259,1201,1,0,223,20101,0,221,4,21001,222,0,3,21101,0,6,2,1001,132,-2,224,1002,224,2,224,1001,224,3,224,1002,132,-1,132,1,224,132,224,21001,224,1,1,21102,1,195,0,105,1,108,20207,1,223,2,21001,23,0,1,21101,-1,0,3,21101,0,214,0,1105,1,303,22101,1,1,1,204,1,99,0,0,0,0,109,5,2101,0,-4,249,21201,-3,0,1,22102,1,-2,2,21202,-1,1,3,21102,1,250,0,1106,0,225,21201,1,0,-4,109,-5,2106,0,0,109,3,22107,0,-2,-1,21202,-1,2,-1,21201,-1,-1,-1,22202,-1,-2,-2,109,-3,2106,0,0,109,3,21207,-2,0,-1,1206,-1,294,104,0,99,22101,0,-2,-2,109,-3,2106,0,0,109,5,22207,-3,-4,-1,1206,-1,346,22201,-4,-3,-4,21202,-3,-1,-1,22201,-4,-1,2,21202,2,-1,-1,22201,-4,-1,1,22102,1,-2,3,21101,0,343,0,1105,1,303,1105,1,415,22207,-2,-3,-1,1206,-1,387,22201,-3,-2,-3,21202,-2,-1,-1,22201,-3,-1,3,21202,3,-1,-1,22201,-3,-1,2,22101,0,-4,1,21101,384,0,0,1106,0,303,1106,0,415,21202,-4,-1,-4,22201,-4,-3,-4,22202,-3,-2,-2,22202,-2,-4,-4,22202,-3,-2,-3,21202,-4,-1,-2,22201,-3,-2,1,21201,1,0,-4,109,-5,2106,0,0]
drone_program = drone_program + ([0] * 1000)

#run_program_part1(drone_program)

#check_field = np.array((110, 110))
#for i in range(1074, 1074+101, 10):
#    for j in range(412,412+101, 10):
#        init_program = cp.deepcopy(drone_program)
#        scan = run_cycle(init_program, 0, [i, j], [], 1, 0)[3][0]
#        print(i,j,scan)


def run_program_check(instructions):
    offset_r = 1082 - 2
    offset_c = 415 - 2
    dim = 120
    scan = np.zeros((dim, dim))
    for i in range(dim):
        for j in range(dim):
            print(i, j)
            init_program = cp.deepcopy(instructions)
            scan[i][j] = run_cycle(init_program, 0, [offset_r+i, offset_c+j], [], 1, 0)[3][0]

    hitpoints_r = np.zeros((dim,dim))
    hitpoints_c = np.zeros((dim,dim))
    #for i in range(len(scan)):
    for i in range(dim):
        line = [PRINTCHAR[int(x)] for x in scan[i]]
        itemindex = np.where(scan[i] == 1)
        print(''.join(line), np.sum(scan[i]), itemindex[0][0], itemindex[0][-1])
    sol = (0,0)
    for i in range(dim-100):
        for j in range(dim-100):
            hitpoints_r[i][j] = np.sum(scan[i][j:])
            col = [x[j] for x in scan]
            hitpoints_c[i][j] = np.sum(col[i:])
            if (sol == (0,0)) and (hitpoints_c[i][j] == 101) and (hitpoints_r[i][j] == 101):
                sol = (i, j)
    print("Solution part 2:", sol)


def run_program_part2_alt(instructions):
    curr_x = 950
    curr_y = 330
    continue_search = True
    while continue_search:
        scan = run_cycle(cp.deepcopy(instructions), 0, [curr_x, curr_y], [], 1, 0)[3][0]
        if not scan:
            curr_y += 1
            continue
        scan_up = run_cycle(cp.deepcopy(instructions), 0, [curr_x-99, curr_y+99], [], 1, 0)[3][0]
        if scan_up:
            scan_down = run_cycle(cp.deepcopy(instructions), 0, [curr_x, curr_y+99], [], 1, 0)[3][0]
            if scan_down:
                print("Solution part 2 found: ", curr_x, curr_y, ((curr_x-100) * 10000) + curr_y)
                continue_search = False
                continue
        curr_x += 1


def run_program_part2(instructions):
    offset_r = 950 #try 1000
    offset_c = 330 #try 440-120
    dim = 200
    scan = np.zeros((10, dim))
    for i in range(10):
        for j in range(dim):
            print(i,j)
            init_program = cp.deepcopy(instructions)
            scan[i][j] = run_cycle(init_program, 0, [offset_r+i, offset_c+j], [], 1, 0)[3][0]

    hitpoints_r = np.zeros((dim,dim))
    hitpoints_c = np.zeros((dim,dim))
    #for i in range(len(scan)):
    for i in range(dim):
        line = [PRINTCHAR[int(x)] for x in scan[i]]
        itemindex = np.where(scan[i] == 1)
        reversline = cp.copy(line)
        print(''.join(line), np.sum(scan[i]), itemindex[0][0], itemindex[0][-1])
    sol = (0,0)
    for i in range(dim-100):
        for j in range(dim-100):
            hitpoints_r[i][j] = np.sum(scan[i][j:])
            col = [x[j] for x in scan]
            hitpoints_c[i][j] = np.sum(col[i:])
            if (sol == (0,0)) and (hitpoints_c[i][j] == 101) and (hitpoints_r[i][j] == 101):
                sol = (i,j)
    print("Solution part 2:", sol)


run_program_part2_alt(drone_program)
#run_program_check(drone_program)
curr_x = 950
curr_y = 333
scan = run_cycle(cp.deepcopy(drone_program), 0, [curr_x, curr_y], [], 1, 0)[3][0]
scan_up = run_cycle(cp.deepcopy(drone_program), 0, [curr_x-99, curr_y], [], 1, 0)[3][0]
scan_down = run_cycle(cp.deepcopy(drone_program), 0, [curr_x, curr_y+99], [], 1, 0)[3][0]

print(scan, scan_up, scan_down)