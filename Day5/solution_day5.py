def extract_modes(instruction):
    instruction_set = [int(x[0]) for x in instruction]
    print(instruction_set)
    n = len(instruction_set)
    if (n==1):
        opcode = instruction_set.pop()
        return [opcode]
    else:
        opcode = instruction_set.pop() + instruction_set.pop()*10
        instruction_set.reverse()
        return ([opcode] + instruction_set)

def process_step(my_list, instruction_pointer, input=[], output=[]):
    print(instruction_pointer, output, my_list)
    instruction = my_list[instruction_pointer]
    instruction_mode = extract_modes(str(instruction))
    opcode = instruction_mode[0]
    if (opcode == 1):
        params = 3
        while (len(instruction_mode) < (params+1)): instruction_mode.append(0)
        # add those things
        param1 = my_list[instruction_pointer + 1]
        param2 = my_list[instruction_pointer + 2]
        param3 = my_list[instruction_pointer + 3]
        if (instruction_mode[1] == 0):
            value1 = my_list[param1]
        else:
            value1 = param1
        if (instruction_mode[2] == 0):
            value2 = my_list[param2]
        else:
            value2 = param2
        if (instruction_mode[3] == 1): print("strange stuff in add third param")
        my_list[param3] = value1 + value2
        # print("recursive call: ", instruction_pointer+4, my_list)
        return process_step(my_list, instruction_pointer + 4, input, output)
    elif (opcode == 2):
        params = 3
        while (len(instruction_mode) < (params+1)): instruction_mode.append(0)
        # multiply those things
        param1 = my_list[instruction_pointer + 1]
        param2 = my_list[instruction_pointer + 2]
        param3 = my_list[instruction_pointer + 3]
        if (instruction_mode[1] == 0):
            value1 = my_list[param1]
        else:
            value1 = param1
        if (instruction_mode[2] == 0):
            value2 = my_list[param2]
        else:
            value2 = param2
        if (instruction_mode[3] == 1): print("strange stuff in add third param")
        my_list[param3] = value1 * value2
        # print("recursive call: ", instruction_pointer+4, my_list)
        return process_step(my_list, instruction_pointer + 4, input, output)
    elif (opcode == 3):
        params = 1
        while (len(instruction_mode) < (params+1)): instruction_mode.append(0)
        #put value at its own address
        store_pos = my_list[instruction_pointer + 1]
        my_list[store_pos] = input.pop(0)
        return process_step(my_list, instruction_pointer + 2, input, output)
    elif (opcode == 4):
        params = 1
        while (len(instruction_mode) < (params+1)): instruction_mode.append(0)
        if (instruction_mode[1]==0):
            output.append(my_list[my_list[instruction_pointer+1]])
        else:
            output.append(my_list[instruction_pointer+1])
        return process_step(my_list, instruction_pointer + 2, input, output)
    elif ((opcode == 5) or (opcode == 6)): #jump-if true(5) or false(6)
        params = 2
        while (len(instruction_mode) < (params+1)): instruction_mode.append(0)
        #jump if parameter is non-zero
        param1 = my_list[instruction_pointer + 1]
        if (instruction_mode[1] == 0):
            cond = my_list[param1]
        else:
            cond = param1
        if (((opcode == 5) and (cond != 0)) or ((opcode == 6) and (cond ==0))):
            param2 = my_list[instruction_pointer + 2]
            if (instruction_mode[2] == 0):
                address = my_list[param2]
            else:
                address = param2
            return process_step(my_list, address, input, output)
        else:
            return process_step(my_list, instruction_pointer + params + 1, input, output)
    elif ((opcode == 7) or (opcode == 8)):
        params = 3
        while (len(instruction_mode) < (params+1)): instruction_mode.append(0)
        param1 = my_list[instruction_pointer + 1]
        param2 = my_list[instruction_pointer + 2]
        param3 = my_list[instruction_pointer + 3]
        if (instruction_mode[1] == 0):
            value1 = my_list[param1]
        else:
            value1 = param1
        if (instruction_mode[2] == 0):
            value2 = my_list[param2]
        else:
            value2 = param2
        if (instruction_mode[3] == 1): print("strange stuff in add third param")
        if (((opcode == 7) and (value1 < value2)) or ((opcode==8) and (value1==value2))):
            my_list[param3] = 1
        else:
            my_list[param3] = 0
        return process_step(my_list, instruction_pointer + params + 1, input, output)
    elif (opcode == 99):
        # print("finished", my_list)
        return (my_list, output)
    else:  # something went wrong
        print("Error, command unkonwn: ")
        # print(instruction_pointer)
        # print(my_list)
        return process_step(my_list, instruction_pointer + 2, input, output)

instructionset = [3,225,1,225,6,6,1100,1,238,225,104,0,1002,188,27,224,1001,224,-2241,224,4,224,102,8,223,223,1001,224,6,224,1,223,224,223,101,65,153,224,101,-108,224,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,1,158,191,224,101,-113,224,224,4,224,102,8,223,223,1001,224,7,224,1,223,224,223,1001,195,14,224,1001,224,-81,224,4,224,1002,223,8,223,101,3,224,224,1,224,223,223,1102,47,76,225,1102,35,69,224,101,-2415,224,224,4,224,102,8,223,223,101,2,224,224,1,224,223,223,1101,32,38,224,101,-70,224,224,4,224,102,8,223,223,101,3,224,224,1,224,223,223,1102,66,13,225,1102,43,84,225,1101,12,62,225,1102,30,35,225,2,149,101,224,101,-3102,224,224,4,224,102,8,223,223,101,4,224,224,1,223,224,223,1101,76,83,225,1102,51,51,225,1102,67,75,225,102,42,162,224,101,-1470,224,224,4,224,102,8,223,223,101,1,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1108,226,677,224,1002,223,2,223,1005,224,329,101,1,223,223,108,226,226,224,1002,223,2,223,1005,224,344,1001,223,1,223,1107,677,226,224,1002,223,2,223,1006,224,359,101,1,223,223,1008,226,226,224,1002,223,2,223,1005,224,374,101,1,223,223,8,226,677,224,102,2,223,223,1006,224,389,101,1,223,223,7,226,677,224,1002,223,2,223,1005,224,404,1001,223,1,223,7,226,226,224,1002,223,2,223,1005,224,419,101,1,223,223,107,226,677,224,1002,223,2,223,1005,224,434,101,1,223,223,107,226,226,224,1002,223,2,223,1005,224,449,1001,223,1,223,1107,226,677,224,102,2,223,223,1006,224,464,1001,223,1,223,1007,677,226,224,1002,223,2,223,1006,224,479,1001,223,1,223,1107,677,677,224,1002,223,2,223,1005,224,494,101,1,223,223,1108,677,226,224,102,2,223,223,1006,224,509,101,1,223,223,7,677,226,224,1002,223,2,223,1005,224,524,1001,223,1,223,1008,677,226,224,102,2,223,223,1005,224,539,1001,223,1,223,1108,226,226,224,102,2,223,223,1005,224,554,101,1,223,223,107,677,677,224,102,2,223,223,1006,224,569,1001,223,1,223,1007,226,226,224,102,2,223,223,1006,224,584,101,1,223,223,8,677,677,224,102,2,223,223,1005,224,599,1001,223,1,223,108,677,677,224,1002,223,2,223,1005,224,614,101,1,223,223,108,226,677,224,102,2,223,223,1005,224,629,101,1,223,223,8,677,226,224,102,2,223,223,1006,224,644,1001,223,1,223,1007,677,677,224,1002,223,2,223,1006,224,659,1001,223,1,223,1008,677,677,224,1002,223,2,223,1005,224,674,101,1,223,223,4,223,99,226]

print(len(instructionset))

result = process_step(instructionset, 0, [5], [])
print(result[1])