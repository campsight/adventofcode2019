import copy as cp
import numpy as np

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
    springbot_instr = []
    springbot_instr.append("NOT A J")
    springbot_instr.append("NOT B T")
    springbot_instr.append("OR T J")
    springbot_instr.append("NOT C T")
    springbot_instr.append("OR T J")
    springbot_instr.append("AND D J")
    springbot_instr.append("WALK")
    input = []
    for spi in springbot_instr:
        input += [ord(c) for c in spi]
        input += [10]
    # print(springbot_instr)
    # print(input)
    result = run_cycle(instructions, 0, input, [], 1, 0)
    print("Solution part 1:", result[3][-1])


def run_program_part2(instructions):
    springbot_instr = []
    springbot_instr.append("NOT A J")
    springbot_instr.append("NOT B T")
    springbot_instr.append("OR T J")
    springbot_instr.append("NOT C T")
    springbot_instr.append("OR T J")
    springbot_instr.append("AND D J")
    #part two begins here
    springbot_instr.append("OR J T")
    springbot_instr.append("AND E T")
    springbot_instr.append("OR H T")
    springbot_instr.append("AND T J")
    springbot_instr.append("RUN")
    input = []
    for spi in springbot_instr:
        input += [ord(c) for c in spi]
        input += [10]
    # print(springbot_instr)
    # print(input)
    result = run_cycle(instructions, 0, input, [], 1, 0)
    print("Solution part 2:", result[3][-1])


springbot_program = [109,2050,21101,966,0,1,21101,0,13,0,1105,1,1378,21101,0,20,0,1105,1,1337,21101,0,27,0,1105,1,1279,1208,1,65,748,1005,748,73,1208,1,79,748,1005,748,110,1208,1,78,748,1005,748,132,1208,1,87,748,1005,748,169,1208,1,82,748,1005,748,239,21101,1041,0,1,21101,73,0,0,1106,0,1421,21101,78,0,1,21101,0,1041,2,21101,0,88,0,1105,1,1301,21102,68,1,1,21102,1,1041,2,21102,103,1,0,1105,1,1301,1101,0,1,750,1105,1,298,21102,1,82,1,21101,0,1041,2,21102,1,125,0,1106,0,1301,1101,0,2,750,1105,1,298,21101,0,79,1,21102,1041,1,2,21102,1,147,0,1105,1,1301,21101,0,84,1,21102,1041,1,2,21102,1,162,0,1105,1,1301,1102,3,1,750,1106,0,298,21101,0,65,1,21101,1041,0,2,21102,1,184,0,1105,1,1301,21101,0,76,1,21102,1,1041,2,21102,199,1,0,1105,1,1301,21101,0,75,1,21101,1041,0,2,21101,0,214,0,1106,0,1301,21102,221,1,0,1106,0,1337,21101,10,0,1,21102,1041,1,2,21101,0,236,0,1105,1,1301,1106,0,553,21102,1,85,1,21102,1041,1,2,21101,254,0,0,1105,1,1301,21101,78,0,1,21102,1,1041,2,21101,0,269,0,1106,0,1301,21102,1,276,0,1105,1,1337,21101,0,10,1,21101,0,1041,2,21102,1,291,0,1106,0,1301,1102,1,1,755,1106,0,553,21102,32,1,1,21101,1041,0,2,21101,313,0,0,1105,1,1301,21101,0,320,0,1105,1,1337,21101,0,327,0,1105,1,1279,2102,1,1,749,21102,1,65,2,21102,73,1,3,21101,0,346,0,1105,1,1889,1206,1,367,1007,749,69,748,1005,748,360,1101,1,0,756,1001,749,-64,751,1106,0,406,1008,749,74,748,1006,748,381,1102,-1,1,751,1105,1,406,1008,749,84,748,1006,748,395,1101,-2,0,751,1105,1,406,21101,1100,0,1,21101,406,0,0,1106,0,1421,21101,0,32,1,21101,0,1100,2,21101,0,421,0,1105,1,1301,21102,1,428,0,1106,0,1337,21101,435,0,0,1106,0,1279,2102,1,1,749,1008,749,74,748,1006,748,453,1102,1,-1,752,1105,1,478,1008,749,84,748,1006,748,467,1102,1,-2,752,1105,1,478,21101,0,1168,1,21101,478,0,0,1106,0,1421,21102,1,485,0,1106,0,1337,21102,1,10,1,21101,0,1168,2,21102,500,1,0,1105,1,1301,1007,920,15,748,1005,748,518,21102,1,1209,1,21102,1,518,0,1105,1,1421,1002,920,3,529,1001,529,921,529,1001,750,0,0,1001,529,1,537,101,0,751,0,1001,537,1,545,1001,752,0,0,1001,920,1,920,1106,0,13,1005,755,577,1006,756,570,21101,1100,0,1,21102,570,1,0,1105,1,1421,21102,1,987,1,1105,1,581,21102,1001,1,1,21102,1,588,0,1106,0,1378,1101,0,758,594,101,0,0,753,1006,753,654,20101,0,753,1,21101,0,610,0,1105,1,667,21102,0,1,1,21101,621,0,0,1106,0,1463,1205,1,647,21102,1,1015,1,21102,635,1,0,1106,0,1378,21102,1,1,1,21101,0,646,0,1106,0,1463,99,1001,594,1,594,1106,0,592,1006,755,664,1101,0,0,755,1105,1,647,4,754,99,109,2,1101,0,726,757,22101,0,-1,1,21102,9,1,2,21101,697,0,3,21102,1,692,0,1105,1,1913,109,-2,2106,0,0,109,2,102,1,757,706,1202,-1,1,0,1001,757,1,757,109,-2,2106,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,255,63,95,223,191,127,159,0,121,84,226,241,79,188,138,166,93,50,254,115,244,239,190,246,61,109,106,212,153,167,85,219,110,214,179,228,124,243,230,38,174,232,125,158,78,99,245,168,222,119,216,169,117,252,155,77,51,213,114,39,204,57,207,171,185,238,250,197,248,152,103,202,175,69,76,101,253,62,107,108,140,59,247,229,68,201,196,242,231,42,206,173,170,47,122,55,184,139,141,118,186,220,163,123,183,217,215,111,46,157,205,162,92,189,71,53,198,142,221,54,60,233,172,116,237,227,200,120,181,236,137,154,100,234,143,49,182,218,199,70,235,187,102,156,113,177,34,178,58,203,86,98,249,56,94,126,251,43,87,136,35,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,20,73,110,112,117,116,32,105,110,115,116,114,117,99,116,105,111,110,115,58,10,13,10,87,97,108,107,105,110,103,46,46,46,10,10,13,10,82,117,110,110,105,110,103,46,46,46,10,10,25,10,68,105,100,110,39,116,32,109,97,107,101,32,105,116,32,97,99,114,111,115,115,58,10,10,58,73,110,118,97,108,105,100,32,111,112,101,114,97,116,105,111,110,59,32,101,120,112,101,99,116,101,100,32,115,111,109,101,116,104,105,110,103,32,108,105,107,101,32,65,78,68,44,32,79,82,44,32,111,114,32,78,79,84,67,73,110,118,97,108,105,100,32,102,105,114,115,116,32,97,114,103,117,109,101,110,116,59,32,101,120,112,101,99,116,101,100,32,115,111,109,101,116,104,105,110,103,32,108,105,107,101,32,65,44,32,66,44,32,67,44,32,68,44,32,74,44,32,111,114,32,84,40,73,110,118,97,108,105,100,32,115,101,99,111,110,100,32,97,114,103,117,109,101,110,116,59,32,101,120,112,101,99,116,101,100,32,74,32,111,114,32,84,52,79,117,116,32,111,102,32,109,101,109,111,114,121,59,32,97,116,32,109,111,115,116,32,49,53,32,105,110,115,116,114,117,99,116,105,111,110,115,32,99,97,110,32,98,101,32,115,116,111,114,101,100,0,109,1,1005,1262,1270,3,1262,20101,0,1262,0,109,-1,2105,1,0,109,1,21101,0,1288,0,1106,0,1263,21002,1262,1,0,1101,0,0,1262,109,-1,2105,1,0,109,5,21101,1310,0,0,1105,1,1279,22102,1,1,-2,22208,-2,-4,-1,1205,-1,1332,21202,-3,1,1,21102,1,1332,0,1105,1,1421,109,-5,2105,1,0,109,2,21101,0,1346,0,1106,0,1263,21208,1,32,-1,1205,-1,1363,21208,1,9,-1,1205,-1,1363,1106,0,1373,21101,0,1370,0,1105,1,1279,1105,1,1339,109,-2,2106,0,0,109,5,1202,-4,1,1386,20102,1,0,-2,22101,1,-4,-4,21101,0,0,-3,22208,-3,-2,-1,1205,-1,1416,2201,-4,-3,1408,4,0,21201,-3,1,-3,1105,1,1396,109,-5,2106,0,0,109,2,104,10,22101,0,-1,1,21101,0,1436,0,1105,1,1378,104,10,99,109,-2,2105,1,0,109,3,20002,594,753,-1,22202,-1,-2,-1,201,-1,754,754,109,-3,2105,1,0,109,10,21102,5,1,-5,21101,0,1,-4,21102,1,0,-3,1206,-9,1555,21102,3,1,-6,21101,0,5,-7,22208,-7,-5,-8,1206,-8,1507,22208,-6,-4,-8,1206,-8,1507,104,64,1106,0,1529,1205,-6,1527,1201,-7,716,1515,21002,0,-11,-8,21201,-8,46,-8,204,-8,1106,0,1529,104,46,21201,-7,1,-7,21207,-7,22,-8,1205,-8,1488,104,10,21201,-6,-1,-6,21207,-6,0,-8,1206,-8,1484,104,10,21207,-4,1,-8,1206,-8,1569,21102,1,0,-9,1105,1,1689,21208,-5,21,-8,1206,-8,1583,21101,1,0,-9,1105,1,1689,1201,-5,716,1589,20101,0,0,-2,21208,-4,1,-1,22202,-2,-1,-1,1205,-2,1613,22101,0,-5,1,21101,0,1613,0,1105,1,1444,1206,-1,1634,21201,-5,0,1,21101,1627,0,0,1106,0,1694,1206,1,1634,21102,1,2,-3,22107,1,-4,-8,22201,-1,-8,-8,1206,-8,1649,21201,-5,1,-5,1206,-3,1663,21201,-3,-1,-3,21201,-4,1,-4,1106,0,1667,21201,-4,-1,-4,21208,-4,0,-1,1201,-5,716,1676,22002,0,-1,-1,1206,-1,1686,21102,1,1,-4,1106,0,1477,109,-10,2105,1,0,109,11,21102,0,1,-6,21102,0,1,-8,21101,0,0,-7,20208,-6,920,-9,1205,-9,1880,21202,-6,3,-9,1201,-9,921,1724,21002,0,1,-5,1001,1724,1,1733,20101,0,0,-4,22102,1,-4,1,21102,1,1,2,21102,9,1,3,21102,1754,1,0,1105,1,1889,1206,1,1772,2201,-10,-4,1767,1001,1767,716,1767,20101,0,0,-3,1106,0,1790,21208,-4,-1,-9,1206,-9,1786,21202,-8,1,-3,1105,1,1790,22102,1,-7,-3,1001,1733,1,1795,21002,0,1,-2,21208,-2,-1,-9,1206,-9,1812,22101,0,-8,-1,1105,1,1816,21202,-7,1,-1,21208,-5,1,-9,1205,-9,1837,21208,-5,2,-9,1205,-9,1844,21208,-3,0,-1,1106,0,1855,22202,-3,-1,-1,1106,0,1855,22201,-3,-1,-1,22107,0,-1,-1,1106,0,1855,21208,-2,-1,-9,1206,-9,1869,22101,0,-1,-8,1106,0,1873,21201,-1,0,-7,21201,-6,1,-6,1106,0,1708,22101,0,-8,-10,109,-11,2106,0,0,109,7,22207,-6,-5,-3,22207,-4,-6,-2,22201,-3,-2,-1,21208,-1,0,-6,109,-7,2106,0,0,0,109,5,2102,1,-2,1912,21207,-4,0,-1,1206,-1,1930,21102,1,0,-4,21201,-4,0,1,22102,1,-3,2,21101,1,0,3,21101,0,1949,0,1106,0,1954,109,-5,2106,0,0,109,6,21207,-4,1,-1,1206,-1,1977,22207,-5,-3,-1,1206,-1,1977,21202,-5,1,-5,1106,0,2045,21202,-5,1,1,21201,-4,-1,2,21202,-3,2,3,21102,1,1996,0,1105,1,1954,21202,1,1,-5,21101,0,1,-2,22207,-5,-3,-1,1206,-1,2015,21101,0,0,-2,22202,-3,-2,-3,22107,0,-4,-1,1206,-1,2037,21202,-2,1,1,21101,0,2037,0,106,0,1912,21202,-3,-1,-3,22201,-5,-3,-5,109,-6,2105,1,0]
springbot_program += [0] * 1000

run_program_part1(cp.deepcopy(springbot_program))
run_program_part2(cp.deepcopy(springbot_program))

