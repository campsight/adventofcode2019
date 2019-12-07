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

def orbit_path(i, from_orbits, to_orbits):
    at_com = False
    path=[]
    while (not at_com):
        next_orbit = to_orbits[i]
        if (next_orbit == 'COM'):
            return path
        else:
            path.append(next_orbit)
            i = from_orbits.index(next_orbit)


#for i in range(len(orbits)):
#    length += calculate_orbit_length(i, from_orbits, to_orbits)

you_path =  orbit_path(from_orbits.index('YOU'), from_orbits, to_orbits)
print(you_path)

san_path =  orbit_path(from_orbits.index('SAN'), from_orbits, to_orbits)
print(san_path)

non_common = []

for orbit in san_path:
    try:
        i = you_path.index(orbit)
    except ValueError:
        non_common.append(orbit)
    else:
        print("solution: ", orbit, san_path.index(orbit), i)
        break