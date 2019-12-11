import numpy as np
BLACK = 0
WHITE = 1
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
DIRECTIONS = [UP, RIGHT, DOWN, LEFT]
LEFT_90 = 0
RIGHT_90 = 1

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
        return (my_list, instruction_pointer, input, output, -1, relative_base)

def get_new_robot_pos(current_pos, direction):
    if (direction == UP):
        return (current_pos[0], current_pos[1]+1)
    elif (direction == RIGHT):
        return (current_pos[0]+1, current_pos[1])
    elif (direction == DOWN):
        return (current_pos[0], current_pos[1]-1)
    elif (direction == LEFT):
        return (current_pos[0]-1, current_pos[1])

def run_program(instructions):
    instruction_pointer = 0
    output = []
    relative_base = 0
    halt_code = 1
    finished = False
    robot_pos = (0, 0)
    robot_direction = UP
    white_squares = []
    squares_visited = [robot_pos]
    robot_instructions = []
    input = [WHITE] #initially, everything is black for part 1, but white for part 2
    while not finished:
        result = process_step(instructions, instruction_pointer, input, output, halt_code, relative_base)
        instructions = result[0]
        instruction_pointer = result[1]
        input = result[2]
        output = result[3]
        halt_code = result[4]
        relative_base = result[5]
        print(input, output, halt_code)
        if (len(output) == 2): # set of instructions for the robot is complete
            robot_instructions.append(output)
            color = output[0] # first instruction is the color
            direction_change = output[1] # second instruction is the direction
            if (color == WHITE): # if the color is white, add the current position to the white squares
                white_squares.append(robot_pos)
            elif(color == BLACK): # if not, it should be black of course
                if robot_pos in white_squares:
                    white_squares.remove(robot_pos)
            else:
                print("error in output. Color: ", color, "doesn't exist.")
            if (direction_change == LEFT_90): # if the direction is rotate left => get direction to the left
                robot_direction = DIRECTIONS[robot_direction - 1]
            elif (direction_change == RIGHT_90):
                #robot_direction = DIRECTIONS[robot_direction + 1]
                robot_direction = DIRECTIONS[robot_direction - 3]
            else:
                print("error in output. Direction change: ", direction_change)
            output = []
            robot_pos = get_new_robot_pos(robot_pos, robot_direction)
            if robot_pos not in squares_visited:
                squares_visited.append(robot_pos)
            if robot_pos in white_squares:
                input = [WHITE]
            else:
                input = [BLACK]
        if halt_code != 1:
            print("halting because of haltcode ", halt_code)
            print(white_squares)
            print(len(white_squares))
            print(robot_instructions)
            print(len(robot_instructions))
            print(squares_visited)
            print(len(squares_visited))
            finished = True

    max_x = max(white_squares,key=lambda item:item[0])[0]
    max_y = max(white_squares,key=lambda item:item[1])[1]
    min_x = min(white_squares,key=lambda item:item[0])[0]
    min_y = min(white_squares,key=lambda item:item[1])[1]
    print(min_x, min_y, max_x, max_y)
    picture = np.chararray((max_x - min_x+1, max_y - min_y+1))
    picture[:] = '-'
    print(picture)
    for square in white_squares:
        picture[square[0]-min_x,square[1]-min_y] = '*'
    print(picture)
    picture = np.transpose(picture)
    print("Solution part 2:")
    for i in range(len(picture)-1,-1,-1):
        print(''.join(picture[i]))


painting_program = [3, 8, 1005, 8, 290, 1106, 0, 11, 0, 0, 0, 104, 1, 104, 0, 3, 8, 1002, 8, -1, 10, 1001, 10, 1, 10, 4,
                    10, 108, 1, 8, 10, 4, 10, 1002, 8, 1, 28, 1006, 0, 59, 3, 8, 1002, 8, -1, 10, 101, 1, 10, 10, 4, 10,
                    108, 0, 8, 10, 4, 10, 101, 0, 8, 53, 3, 8, 1002, 8, -1, 10, 101, 1, 10, 10, 4, 10, 1008, 8, 0, 10,
                    4, 10, 101, 0, 8, 76, 1006, 0, 81, 1, 1005, 2, 10, 3, 8, 102, -1, 8, 10, 1001, 10, 1, 10, 4, 10,
                    1008, 8, 1, 10, 4, 10, 1002, 8, 1, 105, 3, 8, 102, -1, 8, 10, 1001, 10, 1, 10, 4, 10, 108, 1, 8, 10,
                    4, 10, 1001, 8, 0, 126, 3, 8, 1002, 8, -1, 10, 1001, 10, 1, 10, 4, 10, 108, 1, 8, 10, 4, 10, 1002,
                    8, 1, 148, 3, 8, 102, -1, 8, 10, 101, 1, 10, 10, 4, 10, 1008, 8, 1, 10, 4, 10, 1001, 8, 0, 171, 3,
                    8, 1002, 8, -1, 10, 1001, 10, 1, 10, 4, 10, 1008, 8, 0, 10, 4, 10, 101, 0, 8, 193, 1, 1008, 8, 10,
                    1, 106, 3, 10, 1006, 0, 18, 3, 8, 1002, 8, -1, 10, 1001, 10, 1, 10, 4, 10, 108, 0, 8, 10, 4, 10,
                    1001, 8, 0, 225, 1, 1009, 9, 10, 1006, 0, 92, 3, 8, 1002, 8, -1, 10, 1001, 10, 1, 10, 4, 10, 108, 0,
                    8, 10, 4, 10, 1001, 8, 0, 254, 2, 1001, 8, 10, 1, 106, 11, 10, 2, 102, 13, 10, 1006, 0, 78, 101, 1,
                    9, 9, 1007, 9, 987, 10, 1005, 10, 15, 99, 109, 612, 104, 0, 104, 1, 21102, 1, 825594852136, 1,
                    21101, 0, 307, 0, 1106, 0, 411, 21101, 0, 825326580628, 1, 21101, 0, 318, 0, 1105, 1, 411, 3, 10,
                    104, 0, 104, 1, 3, 10, 104, 0, 104, 0, 3, 10, 104, 0, 104, 1, 3, 10, 104, 0, 104, 1, 3, 10, 104, 0,
                    104, 0, 3, 10, 104, 0, 104, 1, 21102, 179557207043, 1, 1, 21101, 0, 365, 0, 1106, 0, 411, 21101, 0,
                    46213012483, 1, 21102, 376, 1, 0, 1106, 0, 411, 3, 10, 104, 0, 104, 0, 3, 10, 104, 0, 104, 0, 21101,
                    988648727316, 0, 1, 21102, 399, 1, 0, 1105, 1, 411, 21102, 988224959252, 1, 1, 21101, 0, 410, 0,
                    1106, 0, 411, 99, 109, 2, 21201, -1, 0, 1, 21101, 0, 40, 2, 21102, 1, 442, 3, 21101, 432, 0, 0,
                    1105, 1, 475, 109, -2, 2105, 1, 0, 0, 1, 0, 0, 1, 109, 2, 3, 10, 204, -1, 1001, 437, 438, 453, 4, 0,
                    1001, 437, 1, 437, 108, 4, 437, 10, 1006, 10, 469, 1102, 0, 1, 437, 109, -2, 2105, 1, 0, 0, 109, 4,
                    2102, 1, -1, 474, 1207, -3, 0, 10, 1006, 10, 492, 21101, 0, 0, -3, 21202, -3, 1, 1, 22102, 1, -2, 2,
                    21101, 0, 1, 3, 21102, 511, 1, 0, 1105, 1, 516, 109, -4, 2105, 1, 0, 109, 5, 1207, -3, 1, 10, 1006,
                    10, 539, 2207, -4, -2, 10, 1006, 10, 539, 21201, -4, 0, -4, 1106, 0, 607, 21202, -4, 1, 1, 21201,
                    -3, -1, 2, 21202, -2, 2, 3, 21101, 558, 0, 0, 1106, 0, 516, 22101, 0, 1, -4, 21101, 1, 0, -1, 2207,
                    -4, -2, 10, 1006, 10, 577, 21102, 1, 0, -1, 22202, -2, -1, -2, 2107, 0, -3, 10, 1006, 10, 599,
                    21201, -1, 0, 1, 21101, 0, 599, 0, 105, 1, 474, 21202, -2, -1, -2, 22201, -4, -2, -4, 109, -5, 2106,
                    0, 0]
painting_program = painting_program + ([0]*100000)
print(painting_program[87:90])

run_program(painting_program)
