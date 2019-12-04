def non_decreasing(digits):
    for i in range(len(digits) - 1):
        if (digits[i + 1] < digits[i]): return False
    return True


def has_double(digits):
    solution = False
    for i in range(len(digits) - 1):
        if (digits[i + 1] == digits[i]): solution = True
    return solution

def nb_repeats(digits, pos):
    n = 1
    for i in range(pos, len(digits) - 1):
        if (digits[i + 1] == digits[i]):
            n += 1
        else:
            return n
    return n

def locate_double_digits(digits):
    repeats = []
    pos = 0
    while (pos < len(digits)):
        n = nb_repeats(digits, pos)
        repeats.append(n)
        pos += n
    return repeats

counter_part1 = 0
counter_part2 = 0
for i in range(246515, 739105):
    digits = [int(d) for d in str(i)]
    if (non_decreasing(digits)):
        digitrepeats = locate_double_digits(digits)
        if (len(digitrepeats) < 6): counter_part1 += 1
        if (2 in digitrepeats): counter_part2 += 1

print("part 1", counter_part1, "part 2", counter_part2)