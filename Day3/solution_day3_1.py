import csv

with open('input.csv', 'r') as input_file:
    reader = csv.reader(input_file)
    input_values = list(reader)

# wire1=["R8","U5","L5","D3"]
# wire2=["U7","R6","D4","L4"]
# wire1= ["R75","D30","R83","U83","L12","D49","R71","U7","L72"]
# wire2= ["U62","R66","U55","R34","D71","R55","D58","R83"]
# wire1=["R98","U47","R26","D63","R33","U87","L62","D20","R33","U53","R51"]
# wire2=["U98","R91","D20","R16","D67","R40","U7","R15","U6","R7"]
wire1 = input_values[0]
wire2 = input_values[1]

wire1Directions = [x[0] for x in wire1]
wire1Distances = [int(x[1:len(x)]) for x in wire1]

wire2Directions = [x[0] for x in wire2]
wire2Distances = [int(x[1:len(x)]) for x in wire2]

print(wire1Directions)
print(wire1Distances)
print(wire2Directions)
print(wire2Distances)


def line_points(wireDirections, wireDistances, xPoints=[0], yPoints=[0]):
    currentX = xPoints[len(xPoints) - 1]
    currentY = yPoints[len(yPoints) - 1]
    direction = wireDirections[0]
    distance = wireDistances[0]
    if (direction == "R"):
        xPoints.append(currentX + distance)
        yPoints.append(currentY)
    elif (direction == "D"):
        xPoints.append(currentX)
        yPoints.append(currentY - distance)
    elif (direction == "L"):
        xPoints.append(currentX - distance)
        yPoints.append(currentY)
    elif (direction == "U"):
        xPoints.append(currentX)
        yPoints.append(currentY + distance)
    if (len(wireDirections) > 1):
        return line_points(wireDirections[1:], wireDistances[1:], xPoints, yPoints)
    else:
        return [xPoints, yPoints]


wire1_coord = line_points(wire1Directions, wire1Distances, [0], [0])
print(wire1_coord)

wire2_coord = line_points(wire2Directions, wire2Distances, [0], [0])
print(wire2_coord)


def line_intersection(line1, line2):
    x11 = line1[0][0]
    x12 = line1[1][0]
    y11 = line1[0][1]
    y12 = line1[1][1]
    if (x11 == x12):  # vertical line
        if (y11 > y12):  # from top to bottom => swap to get the inverse
            x11, x12 = x12, x11
            y11, y12 = y12, y11
    else:  # horizontal line
        if (x11 > x12):  # from right to left => swap to get the inverse
            x11, x12 = x12, x11
            y11, y12 = y12, y11
    x21 = line2[0][0]
    y21 = line2[0][1]
    x22 = line2[1][0]
    y22 = line2[1][1]
    if (x21 == x22):  # vertical line
        if (y21 > y22):  # from top to bottom => swap to get the inverse
            x21, x22 = x22, x21
            y21, y22 = y22, y21
    else:  # horizontal line
        if (x21 > x22):  # from right to left => swap to get the inverse
            x21, x22 = x22, x21
            y21, y22 = y22, y21

    if (x11 == x12):  # vertical line
        if (x21 == x22):
            return (0, 0)  # two vertical lines don't intersect
        else:  # vertical and horizontal lines could intersect
            if (((x11 >= x21) and (x11 <= x22)) and ((y21 >= y11) and (y21 <= y12))):
                return (x11, y21)
            else:
                return (0, 0)
    elif (y21 == y22):
        return (0, 0)  # two horizontal lines don't intersect
    elif (((x21 >= x11) and (x21 <= x12)) and ((y11 >= y21) and (y11 <= y22))):
        return (x21, y11)
    else:
        return (0, 0)
    return (0, 0)


closest = (0, 0)

# print(wire2_coord[1][2])
# print(closest != (0,0))
for i in range(len(wire1_coord[0]) - 1):
    for j in range(len(wire2_coord[0]) - 1):
        # print(i,j)
        p1 = [wire1_coord[0][i], wire1_coord[1][i]]
        p2 = [wire1_coord[0][i + 1], wire1_coord[1][i + 1]]
        q1 = [wire2_coord[0][j], wire2_coord[1][j]]
        q2 = [wire2_coord[0][j + 1], wire2_coord[1][j + 1]]
        intersection = line_intersection([p1, p2], [q1, q2])
        # print("closest", closest, "intersection", intersection)
        if (intersection != (0, 0)):  # if they intersect
            if (closest == (0, 0)):
                closest = intersection
            elif ((abs(intersection[0]) + abs(intersection[1])) < (abs(closest[0]) + abs(closest[1]))):
                closest = intersection

# print(line_intersection([[0,0],[8,0]],[[5,7],[5,3]]))
print(closest, " => ", abs(closest[0]) + abs(closest[1]))