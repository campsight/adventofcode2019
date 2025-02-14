import numpy as np

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4
SCREEN_CHARS = ['_', 'W', '#', 'P', 'o']
GO_LEFT = -1
STAY_PUT = 0
GO_RIGHT = +1

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

def get_nb_blocks(my_screen):
    my_blocks = [x[2]==BLOCK for x in my_screen]
    return sum(my_blocks)

def get_nb_blocks2(my_screen2):
    my_blocks = 0
    for row in my_screen2:
        my_blocks += sum([x == BLOCK for x in row])
    return my_blocks

def convert_game_screen(my_screen):
    screen_width = max([x[0] for x in my_screen])
    screen_height = max([x[1] for x in my_screen])
    result = np.empty([screen_width+1,screen_height+1])
    for point in my_screen:
        result[point[0],point[1]] = int(point[2])
    return result

def print_game_screen(my_screen):
    screen_width = max([x[0] for x in my_screen])
    screen_height = max([x[1] for x in my_screen])
    visuals = np.chararray((screen_width+1, screen_height+1))
    for point in my_screen:
        visuals[point[0],point[1]] = SCREEN_CHARS[point[2]]
    visuals_t = np.transpose(visuals)
    for i in range(len(visuals_t)):
        print(''.join(visuals_t[i]))

def print_game_screen2(my_screen2):
    screen_width = len(my_screen2)
    screen_height = len(my_screen2[0])
    visuals = np.chararray((screen_width, screen_height))
    for i in range(screen_width):
        visuals[i] = [SCREEN_CHARS[int(x)] for x in my_screen2[i]]
    visuals_t = np.transpose(visuals)
    for i in range(len(visuals_t)):
        print(''.join(visuals_t[i]))

def get_single_item_pos(game_screen, item):
    for pos in game_screen:
        if pos[2] == item:
            return (pos[0],pos[1])
    return (-1,-1)

def get_single_item_pos2(game_screen2, item):
    pos = np.where(game_screen2 == item)
    if (len(pos[0]) > 0):
        return (pos[0][0], pos[1][0])
    else:
        return (-1, -1)

def run_program(instructions):
    instruction_pointer = 0
    input = []
    output = []
    relative_base = 0
    halt_code = 1
    finished = False
    game_screen = []
    game_screen_content = []
    build_game_screen = True
    score = 0
    while not finished:
        result = process_step(instructions, instruction_pointer, input, output, halt_code, relative_base)
        instructions = result[0]
        instruction_pointer = result[1]
        input = result[2]
        output = result[3]
        halt_code = result[4]
        relative_base = result[5]
        #print(input, output, halt_code)
        if (len(output) == 3): # set of instructions for the robot is complete
            if output[0] >= 0:
                if build_game_screen:
                    game_screen.append(output)
                else:
                    game_screen2[output[0],output[1]] = output[2]
            else:
                nb_blocks = 0
                if (score == 0) and build_game_screen:
                    build_game_screen = False
                    game_screen2 = convert_game_screen(game_screen)
                    print_game_screen(game_screen)
                    nb_blocks = get_nb_blocks(game_screen)
                    print(nb_blocks)
                else:
                    print_game_screen2(game_screen2)
                    nb_blocks = get_nb_blocks2(game_screen2)
                    print(nb_blocks)
                score = output[2]
                print("New score: ", score)
                if nb_blocks == 0:
                    print("Final score: ", score)
                    finished = True
            output = []
        if halt_code == 0:
            balpos = get_single_item_pos2(game_screen2, BALL)
            paddlepos = get_single_item_pos2(game_screen2, PADDLE)
            #print("expecting input with balpos and paddlepos ", balpos, paddlepos)
            if (balpos[0] > paddlepos[0]): # bal is more to the right than the paddle
                #print("providing input Go Right: ", GO_RIGHT)
                input = [GO_RIGHT]
            elif (balpos[0] < paddlepos[0]): # bal is more to the left than the paddle
                #print("providing input Go Left: ", GO_LEFT)
                input = [GO_LEFT]
            else: #the same x positions
                #print("providing input Stay Put: ", STAY_PUT)
                input = [STAY_PUT]
            halt_code = 1
        elif halt_code != 1:
            print("halting because of haltcode ", halt_code)
            print_game_screen(game_screen)
            print(get_nb_blocks(game_screen))
            finished = True



painting_program =[1,380,379,385,1008,2563,464403,381,1005,381,12,99,109,2564,1102,1,0,383,1101,0,0,382,20101,0,382,1,20102,1,383,2,21102,37,1,0,1106,0,578,4,382,4,383,204,1,1001,382,1,382,1007,382,37,381,1005,381,22,1001,383,1,383,1007,383,26,381,1005,381,18,1006,385,69,99,104,-1,104,0,4,386,3,384,1007,384,0,381,1005,381,94,107,0,384,381,1005,381,108,1105,1,161,107,1,392,381,1006,381,161,1101,0,-1,384,1106,0,119,1007,392,35,381,1006,381,161,1102,1,1,384,20101,0,392,1,21102,1,24,2,21102,0,1,3,21102,138,1,0,1105,1,549,1,392,384,392,20102,1,392,1,21101,0,24,2,21102,3,1,3,21102,1,161,0,1106,0,549,1101,0,0,384,20001,388,390,1,21001,389,0,2,21102,180,1,0,1105,1,578,1206,1,213,1208,1,2,381,1006,381,205,20001,388,390,1,20101,0,389,2,21102,205,1,0,1105,1,393,1002,390,-1,390,1101,1,0,384,20101,0,388,1,20001,389,391,2,21102,228,1,0,1106,0,578,1206,1,261,1208,1,2,381,1006,381,253,21001,388,0,1,20001,389,391,2,21102,1,253,0,1106,0,393,1002,391,-1,391,1101,0,1,384,1005,384,161,20001,388,390,1,20001,389,391,2,21101,0,279,0,1106,0,578,1206,1,316,1208,1,2,381,1006,381,304,20001,388,390,1,20001,389,391,2,21101,0,304,0,1106,0,393,1002,390,-1,390,1002,391,-1,391,1102,1,1,384,1005,384,161,21001,388,0,1,21002,389,1,2,21102,1,0,3,21102,1,338,0,1106,0,549,1,388,390,388,1,389,391,389,21001,388,0,1,20102,1,389,2,21101,0,4,3,21101,365,0,0,1105,1,549,1007,389,25,381,1005,381,75,104,-1,104,0,104,0,99,0,1,0,0,0,0,0,0,372,16,21,1,1,18,109,3,22102,1,-2,1,22102,1,-1,2,21102,0,1,3,21101,0,414,0,1105,1,549,22101,0,-2,1,21201,-1,0,2,21101,0,429,0,1105,1,601,1202,1,1,435,1,386,0,386,104,-1,104,0,4,386,1001,387,-1,387,1005,387,451,99,109,-3,2105,1,0,109,8,22202,-7,-6,-3,22201,-3,-5,-3,21202,-4,64,-2,2207,-3,-2,381,1005,381,492,21202,-2,-1,-1,22201,-3,-1,-3,2207,-3,-2,381,1006,381,481,21202,-4,8,-2,2207,-3,-2,381,1005,381,518,21202,-2,-1,-1,22201,-3,-1,-3,2207,-3,-2,381,1006,381,507,2207,-3,-4,381,1005,381,540,21202,-4,-1,-1,22201,-3,-1,-3,2207,-3,-4,381,1006,381,529,21202,-3,1,-7,109,-8,2105,1,0,109,4,1202,-2,37,566,201,-3,566,566,101,639,566,566,1201,-1,0,0,204,-3,204,-2,204,-1,109,-4,2105,1,0,109,3,1202,-1,37,594,201,-2,594,594,101,639,594,594,20101,0,0,-2,109,-3,2106,0,0,109,3,22102,26,-2,1,22201,1,-1,1,21102,487,1,2,21101,0,823,3,21102,1,962,4,21102,630,1,0,1105,1,456,21201,1,1601,-2,109,-3,2106,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,2,2,2,0,2,2,2,0,2,0,2,2,0,2,0,0,0,0,0,2,0,0,2,0,0,2,0,0,0,0,2,0,0,1,1,0,2,2,2,2,2,0,0,2,2,2,2,2,2,2,0,0,0,2,2,2,2,0,0,0,2,2,2,2,2,2,2,2,0,0,1,1,0,0,2,2,2,2,2,2,2,0,2,2,2,2,0,2,2,2,0,0,2,2,2,2,2,0,0,0,2,2,0,2,2,2,0,1,1,0,0,2,0,0,2,2,0,2,2,2,2,0,2,2,2,2,0,2,2,2,0,2,0,0,2,2,2,2,2,2,0,2,2,0,1,1,0,0,2,2,2,2,2,0,2,2,0,2,0,0,0,0,2,0,0,2,2,2,2,2,2,0,0,2,0,2,2,0,2,2,0,1,1,0,0,0,2,2,2,2,2,0,2,0,0,0,2,2,2,2,2,0,0,2,2,2,0,0,2,2,2,0,2,2,2,2,0,0,1,1,0,0,0,2,2,2,2,0,2,0,2,0,0,2,2,0,0,0,2,0,0,2,2,2,2,2,2,2,2,0,0,2,0,0,0,1,1,0,2,2,0,2,2,2,2,0,2,2,2,2,2,0,2,2,2,2,2,0,0,2,2,2,0,0,2,0,2,2,2,0,2,0,1,1,0,2,2,2,0,0,2,2,2,2,2,0,2,2,2,2,0,0,2,2,2,0,0,0,2,2,0,2,2,2,2,2,0,0,0,1,1,0,0,2,2,2,0,0,0,0,0,2,0,2,0,2,0,0,0,2,0,2,2,2,2,0,0,0,2,2,2,2,0,0,2,0,1,1,0,2,2,0,2,2,2,2,2,2,2,0,2,2,0,0,0,2,2,2,2,0,2,2,2,0,0,2,2,0,2,0,2,2,0,1,1,0,0,2,2,2,0,2,0,0,2,0,2,0,2,2,2,0,2,2,2,2,2,0,2,2,2,2,0,0,0,2,2,0,2,0,1,1,0,2,2,2,2,0,0,0,2,0,0,0,2,2,0,0,2,2,2,0,0,2,2,2,0,2,2,0,2,2,0,2,0,2,0,1,1,0,2,2,2,2,2,2,2,0,2,2,0,2,0,2,2,0,0,2,2,2,2,2,2,0,2,2,2,0,2,2,2,0,2,0,1,1,0,2,0,2,0,2,2,2,0,0,2,0,2,0,0,2,2,2,2,2,0,0,2,0,0,0,0,0,2,2,0,0,2,2,0,1,1,0,0,0,2,2,0,2,2,0,0,0,0,2,0,2,0,0,2,2,0,2,2,0,0,0,2,0,2,2,2,0,0,2,2,0,1,1,0,0,2,2,2,2,0,2,0,2,2,0,0,0,2,0,2,2,0,2,0,0,2,2,2,2,2,0,0,0,2,2,2,2,0,1,1,0,0,2,2,2,2,0,2,2,0,2,2,2,0,2,2,0,2,2,2,2,2,2,2,2,2,0,2,2,2,2,2,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,11,37,14,23,15,37,71,61,7,18,91,52,5,7,98,91,47,52,13,61,2,90,13,47,30,62,79,74,31,54,19,25,3,29,7,71,96,58,15,86,38,47,73,81,23,69,85,18,49,89,89,89,25,72,58,78,13,44,68,52,60,73,12,33,98,86,36,13,70,31,28,68,10,63,14,93,8,78,28,59,20,87,33,80,36,76,72,51,96,91,8,52,25,29,75,90,93,6,29,80,56,37,38,18,36,54,80,30,96,72,10,65,70,22,49,97,62,84,54,96,32,3,98,93,78,14,69,38,98,48,89,4,45,12,38,77,72,71,91,17,17,6,88,37,18,94,60,38,21,18,79,18,57,57,53,90,8,14,61,71,22,4,68,86,35,41,39,80,14,60,34,81,81,85,95,35,40,77,40,27,88,44,61,14,76,14,6,14,35,98,70,3,61,37,48,90,90,11,2,8,61,13,5,63,74,22,22,1,80,37,47,77,16,5,19,41,66,43,14,84,27,55,70,49,57,59,65,62,51,31,39,5,63,98,54,53,82,79,86,24,2,27,66,58,8,44,39,46,45,25,55,12,23,84,46,9,21,98,21,42,24,34,90,96,21,72,10,68,82,15,15,29,59,91,61,94,98,1,81,97,46,70,71,81,94,17,41,63,5,64,40,85,61,95,56,9,36,70,73,18,29,60,70,95,48,74,54,18,77,74,48,84,53,32,69,57,31,26,25,63,69,73,26,1,34,97,31,40,78,64,18,87,78,88,26,52,78,42,82,20,71,50,21,81,64,75,57,92,68,78,18,44,58,68,33,79,67,83,53,6,48,12,54,41,67,26,79,9,84,93,22,86,95,3,39,38,68,24,36,80,28,27,72,64,30,37,38,61,97,86,2,89,66,70,69,31,27,53,26,26,11,67,57,20,34,59,35,58,39,74,90,92,35,44,39,88,47,53,74,92,52,3,62,68,48,34,89,27,24,82,8,10,92,73,18,84,49,87,42,17,34,12,12,36,41,40,54,9,81,87,96,33,17,50,95,24,71,79,42,90,9,48,56,89,27,63,47,89,27,49,50,53,57,49,45,18,38,44,48,96,1,63,73,29,26,7,5,92,17,97,51,28,28,28,14,63,11,13,74,35,5,97,14,82,96,93,68,43,97,10,96,67,28,96,68,48,51,55,67,66,14,18,52,7,55,90,52,28,10,33,50,82,85,80,75,76,6,42,47,53,77,15,19,54,15,62,52,57,34,38,75,50,25,21,70,52,59,31,93,80,15,16,34,77,41,98,53,97,80,41,76,19,51,1,29,56,57,93,85,5,84,49,9,92,61,66,58,80,58,41,7,23,53,14,20,83,72,98,86,90,50,35,20,81,58,55,18,29,37,69,87,79,38,72,38,74,31,1,44,56,73,95,50,33,64,29,11,80,49,29,14,90,2,17,18,71,95,17,12,82,75,94,70,10,35,43,11,66,64,86,40,51,70,73,32,69,45,51,91,59,56,18,15,40,42,35,23,5,2,94,60,92,48,14,31,80,29,61,85,58,93,80,26,21,1,93,86,2,75,14,20,54,78,58,28,30,33,6,10,43,62,37,6,93,62,51,29,74,4,26,30,97,47,68,82,21,56,89,47,28,12,58,47,48,73,46,11,25,3,86,43,14,53,30,87,56,64,16,85,25,59,91,88,64,52,62,38,30,8,59,97,76,16,22,59,59,55,6,2,53,74,94,7,58,92,53,89,97,9,79,65,48,15,76,29,39,73,63,72,45,45,62,97,92,67,22,37,17,89,95,44,71,44,23,39,58,37,27,6,28,87,43,23,21,79,75,38,14,68,53,82,49,95,91,65,13,30,13,42,49,57,7,3,47,92,53,29,73,44,98,12,12,24,98,70,93,35,60,10,19,65,2,74,55,45,48,32,68,15,57,20,73,70,8,26,88,77,59,31,98,69,31,80,81,32,20,83,43,31,47,35,43,55,58,58,83,52,72,64,7,78,33,13,1,13,38,96,21,11,10,54,96,95,47,4,15,91,65,35,13,41,42,79,79,81,53,84,30,5,25,39,13,73,33,89,4,80,92,76,13,26,64,28,98,16,95,63,92,60,79,48,7,77,14,58,20,37,50,1,45,58,10,71,9,74,2,68,69,25,78,71,49,74,46,75,34,79,19,43,83,85,64,464403]
painting_program = painting_program + ([0]*100000)

run_program(painting_program)

painting_program[0] = 2

run_program(painting_program)
