# Finally got to the point of writing a separate class for the int computer :-)


# static method to extract the opcode from an instruction
def extract_modes(instruction):
    instruction_set = [int(x[0]) for x in instruction]
    n = len(instruction_set)
    if n == 1:
        opcode = instruction_set.pop()
        return [opcode]
    else:
        opcode = instruction_set.pop() + instruction_set.pop() * 10
        instruction_set.reverse()
        return [opcode] + instruction_set


class IntComputer:

    def __init__(self, instruction_set, ic_input=[], ic_rel_base=0):
        self.instructions = instruction_set
        self.instruction_pointer = 0
        self.input = ic_input
        self.output = []
        self.halt_code = 99
        self.relative_base = ic_rel_base

    def set_input(self, new_input):
        self.input = new_input

    def set_halt_code(self, new_halt_code):
        self.halt_code = new_halt_code

    def get_halt_code(self):
        return self.halt_code

    def clear_output(self):
        self.output = []

    def popleft_output(self, nb_elements=1):
        my_output = []
        for i in range(nb_elements):
            my_output.append(self.output.pop(0))
        return my_output

    def pop_output(self):
        return self.output.pop()

    def get_output(self):
        return self.output

    def extend_memory(self, mem_size=1000):
        self.instructions += [0]*mem_size

    # helper function to make process_step more readable
    # 'solves' the instruction mode (value vs address) topic
    def get_instruction_values(self, instruction_mode, nb_of_params=1):
        while len(instruction_mode) < (nb_of_params + 1):
            instruction_mode.append(0)
        values = []
        for i in range(nb_of_params):
            param = self.instructions[self.instruction_pointer + i + 1]
            # 2 = relative mode: offset to relative position
            if instruction_mode[i + 1] == 0:  # position mode: param is value at the address
                values.append(self.instructions[param])
            elif instruction_mode[i + 1] == 2:  # relative mode: offset to relative position
                values.append(self.instructions[param + self.relative_base])
            else:  # immediate mode: param is value itself
                values.append(param)
        return values

    def get_store_pos(self, instruction_mode, nb_of_params, normal_store_pos):
        while len(instruction_mode) < (nb_of_params + 1):
            instruction_mode.append(0)
        mode = instruction_mode.pop()
        if mode == 2: normal_store_pos += self.relative_base
        return normal_store_pos

    # AoC 2019 Intcode processor.
    # haltcode = 1 to continue, 0 to wait for self.input and 99 if the program halts
    def process_step(self):
        if (self.halt_code == 0) or (self.halt_code == 99): return self.halt_code
        instruction = self.instructions[self.instruction_pointer]
        instruction_mode = extract_modes(str(instruction))
        opcode = instruction_mode[0]
        if opcode == 1:
            values = self.get_instruction_values(instruction_mode, 2)
            store_pos = self.get_store_pos(instruction_mode, 3, self.instructions[self.instruction_pointer + 3])
            self.instructions[store_pos] = values[0] + values[1]
            self.halt_code = 1
            self.instruction_pointer += 4
            return self.halt_code
        elif opcode == 2:
            values = self.get_instruction_values(instruction_mode, 2)
            store_pos = self.get_store_pos(instruction_mode, 3, self.instructions[self.instruction_pointer + 3])
            self.instructions[store_pos] = values[0] * values[1]
            self.instruction_pointer += 4
            self.halt_code = 1
            return self.halt_code
        elif opcode == 3:  # read self.input - but could be that it needs to wait if there is non
            store_pos = self.get_store_pos(instruction_mode, 1, self.instructions[self.instruction_pointer + 1])
            if (len(self.input) > 0):
                self.instructions[store_pos] = self.input.pop(0)
                self.instruction_pointer += 2
                self.halt_code = 1
                return self.halt_code
            else:  # no self.input anymore => halt and don't move the instruction pointer
                self.halt_code = 0
                return self.halt_code
        elif opcode == 4:  # self.output
            values = self.get_instruction_values(instruction_mode, 1)
            self.output.append(values[0])
            self.instruction_pointer += 2
            self.halt_code = 1
            return self.halt_code
        elif (opcode == 5) or (opcode == 6):  # jump-if true(5) or false(6)
            values = self.get_instruction_values(instruction_mode, 2)
            cond = values[0]
            if ((opcode == 5) and (cond != 0)) or ((opcode == 6) and (cond == 0)):
                self.instruction_pointer = values[1]
                self.halt_code = 1
                return self.halt_code
            else:
                self.instruction_pointer += 3
                self.halt_code = 1
                return self.halt_code
        elif (opcode == 7) or (opcode == 8):
            values = self.get_instruction_values(instruction_mode, 2)
            store_pos = self.get_store_pos(instruction_mode, 3, self.instructions[self.instruction_pointer + 3])
            if ((opcode == 7) and (values[0] < values[1])) or ((opcode == 8) and (values[0] == values[1])):
                self.instructions[store_pos] = 1
            else:
                self.instructions[store_pos] = 0
            self.instruction_pointer += 4
            self.halt_code = 1
            return self.halt_code
        elif opcode == 9:  # change relative base
            values = self.get_instruction_values(instruction_mode, 1)
            self.relative_base += values[0]
            self.instruction_pointer += 2
            self.halt_code = 1
            return self.halt_code
        elif opcode == 99:  # end of the program
            self.halt_code = 99
            return self.halt_code
        else:  # something went wrong
            print("Error, command unkonwn: ")
            self.halt_code = -1
            return self.halt_code

    def run_cycle(self, new_input):
        finished = False
        self.input = new_input
        self.halt_code = 1
        while not finished:
            step_halt_code = self.process_step()
            if step_halt_code == 0:  # set the input
                # print("halting because input is required")
                finished = True
            elif step_halt_code != 1:
                print("halting because of haltcode ", step_halt_code)
                finished = True
        return self.output

