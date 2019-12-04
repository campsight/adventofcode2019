import math

input_file = open("input.txt", "r")


def calculate_fuel(mass):
    fuel_required = int(math.floor(mass / 3)) - 2
    if fuel_required <= 0:
        return 0
    else:
        return fuel_required + calculate_fuel(fuel_required)


amount_of_fuel = 0
for line in input_file:
    mass = int(line)
    amount_of_fuel = amount_of_fuel + calculate_fuel(mass)
print(amount_of_fuel)