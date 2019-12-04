test_list = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
input_list = [1, 12, 2, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 9, 1, 19, 1, 19, 6, 23, 2, 6, 23, 27, 2, 27, 9, 31, 1,
              5, 31, 35, 1, 35, 10, 39, 2, 39, 9, 43, 1, 5, 43, 47, 2, 47, 10, 51, 1, 51, 6, 55, 1, 5, 55, 59, 2, 6, 59,
              63, 2, 63, 6, 67, 1, 5, 67, 71, 1, 71, 9, 75, 2, 75, 10, 79, 1, 79, 5, 83, 1, 10, 83, 87, 1, 5, 87, 91, 2,
              13, 91, 95, 1, 95, 10, 99, 2, 99, 13, 103, 1, 103, 5, 107, 1, 107, 13, 111, 2, 111, 9, 115, 1, 6, 115,
              119, 2, 119, 6, 123, 1, 123, 6, 127, 1, 127, 9, 131, 1, 6, 131, 135, 1, 135, 2, 139, 1, 139, 10, 0, 99, 2,
              0, 14, 0]


def process_step(my_list, instruction_pointer):
    instruction = my_list[instruction_pointer]
    if (instruction == 1):
        # add those things
        add_pos1 = my_list[instruction_pointer + 1]
        add_pos2 = my_list[instruction_pointer + 2]
        store_pos = my_list[instruction_pointer + 3]
        my_list[store_pos] = my_list[add_pos1] + my_list[add_pos2]
        # print("recursive call: ", instruction_pointer+4, my_list)
        return process_step(my_list, instruction_pointer + 4)
    elif (instruction == 2):
        # multiply those things
        mul_pos1 = my_list[instruction_pointer + 1]
        mul_pos2 = my_list[instruction_pointer + 2]
        store_pos = my_list[instruction_pointer + 3]
        my_list[store_pos] = my_list[mul_pos1] * my_list[mul_pos2]
        # print("recursive call: ", instruction_pointer+4, my_list)
        return process_step(my_list, instruction_pointer + 4)
    elif (instruction == 99):
        # print("finished", my_list)
        return my_list
    else:  # something went wrong
        print("Error, command unkonwn: ")
        # print(instruction_pointer)
        # print(my_list)


process_step(test_list, 0)
process_step(input_list, 0)
print("solution: ", input_list[0])  # should give 6730673

# part two
solution_value = 19690720
for i in range(100):
    for j in range(100):
        my_list = [1, 12, 2, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 9, 1, 19, 1, 19, 6, 23, 2, 6, 23, 27, 2, 27, 9,
                   31, 1, 5, 31, 35, 1, 35, 10, 39, 2, 39, 9, 43, 1, 5, 43, 47, 2, 47, 10, 51, 1, 51, 6, 55, 1, 5, 55,
                   59, 2, 6, 59, 63, 2, 63, 6, 67, 1, 5, 67, 71, 1, 71, 9, 75, 2, 75, 10, 79, 1, 79, 5, 83, 1, 10, 83,
                   87, 1, 5, 87, 91, 2, 13, 91, 95, 1, 95, 10, 99, 2, 99, 13, 103, 1, 103, 5, 107, 1, 107, 13, 111, 2,
                   111, 9, 115, 1, 6, 115, 119, 2, 119, 6, 123, 1, 123, 6, 127, 1, 127, 9, 131, 1, 6, 131, 135, 1, 135,
                   2, 139, 1, 139, 10, 0, 99, 2, 0, 14, 0]
        my_list[1] = i
        my_list[2] = j
        tested_solution = process_step(my_list, 0)[0]
        # print("(", i, ", ", j, "): ", tested_solution)
        if (tested_solution == solution_value):
            print("Solution found: (", i, ", ", j, "): ", 100 * i + j)
            break

