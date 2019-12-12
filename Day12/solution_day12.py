import operator as op
import copy

''''<x=-19, y=-4, z=2>
<x=-9, y=8, z=-16>
<x=-4, y=5, z=-11>
<x=1, y=9, z=-13>'''

moons = [[[-19, -4, 2], [0, 0, 0]],
         [[-9, 8, -16], [0, 0, 0]],
         [[-4, 5, -11], [0, 0, 0]],
         [[1, 9, -13], [0, 0, 0]]]

'''moons = [[[-8, -10, 0], [0, 0, 0]],
         [[5, 5, 10], [0, 0, 0]],
         [[2, -7, 3], [0, 0, 0]],
         [[9, -8, -3], [0, 0, 0]]]'''

'''moons = [[[-1, 0, 2], [0, 0, 0]],
         [[2, -10, -7], [0, 0, 0]],
         [[4, -8, 8], [0, 0, 0]],
         [[3, 5, -1], [0, 0, 0]]]'''

def run_moon_cycles(moons, nb_cycles):
    initial_positions = copy.deepcopy(moons)
    return_cycle = [] + ([-1] * 3)
    for i in range(nb_cycles):
        # for each pair of moons
        moons = run_moon_step(moons)
        for c in range(3):
            if (moons[0][0][c] == initial_positions[0][0][c]) and (moons[1][0][c] == initial_positions[1][0][c]) and (
                    moons[2][0][c] == initial_positions[2][0][c]) and (moons[3][0][c] == initial_positions[3][0][c] and (
                    moons[0][1][c] == 0) and (moons[1][1][c] == 0) and (
                    moons[2][1][c] == 0) and (moons[3][1][c] == 0)):
                if return_cycle[c] < 0:
                    return_cycle[c] = i
                    print(i, moons, initial_positions)
        if (return_cycle[0] > 0) and (return_cycle[1] > 0) and (return_cycle[2]>0): break
    print(return_cycle)
    return [moons, return_cycle]



def run_moon_step(moons):
    for i in range(len(moons)):
        for j in range(i, len(moons)):
            moon1 = moons[i]
            moon2 = moons[j]
            # apply gravity
            for c in range(3):
                if moon1[0][c] > moon2[0][c]:
                    moon1[1][c] -= 1
                    moon2[1][c] += 1
                elif moon1[0][c] < moon2[0][c]:
                    moon1[1][c] += 1
                    moon2[1][c] -= 1
    # apply velocity
    for moon in moons:
        moon[0] = list(map(op.add, moon[0], moon[1]))
    return moons


result = run_moon_cycles(moons, 1000000)
moons = result[0]
solution = result[1]

total_energy = 0
for moon in moons:
    potentials = [abs(x) for x in moon[0]]
    kinetics = [abs(x) for x in moon[1]]
    total_energy += sum(potentials) * sum(kinetics)

#print(total_energy)

def gcd(a, b):
    if a < b:
        a, b = b, a
    while b:
        a, b = b, a % b
    return a

def compute_lcm(x, y):
   lcm = (x*y)//gcd(x,y)
   return lcm


#solution = [161426, 113026, 231612]

print(compute_lcm(solution[0]+1,compute_lcm(solution[1]+1,solution[2]+1)))
