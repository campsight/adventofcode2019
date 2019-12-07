import csv

with open('inputd6.txt', 'r') as input_file:
    reader = csv.reader(input_file)
    input_values = list(reader)

print(input_values)

#orbits = [x[0].split[')'] for x in input_values]

orbits = []

for i in range(len(input_values)):
    orbit = input_values[i][0].split(')')
    orbits.append(orbit)

print(orbits)

from_orbits = [x[1] for x in orbits]
to_orbits = [x[0] for x in orbits]

print(from_orbits)
print(to_orbits)

def calculate_orbit_length(i, from_orbits, to_orbits):
    at_com = False
    steps = 1
    while (not at_com):
        next_orbit = to_orbits[i]
        if (next_orbit == 'COM'):
            return steps
        else:
            steps += 1
            i = from_orbits.index(next_orbit)

length = 0

for i in range(len(orbits)):
    length += calculate_orbit_length(i, from_orbits, to_orbits)

print(length)

#part 2

