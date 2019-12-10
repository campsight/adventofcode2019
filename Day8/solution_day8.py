import csv
with open('input_d8.txt', 'r') as input_file:
    reader = csv.reader(input_file)
    input_string = list(reader)[0][0]

width = 25
size = 6
layer_size = width*size
layer_split = [input_string[i:i+layer_size] for i in range(0, len(input_string), layer_size)]

nb_zeros = [layer.count('0') for layer in layer_split]

min_zeros = min(nb_zeros)
min_zeros_index = nb_zeros.index(min_zeros)
solution = layer_split[min_zeros_index].count('1') * layer_split[min_zeros_index].count('2')
print("Solution part 1: ", solution)

import numpy as np
final_image = np.full(layer_size, 9)

for i in range(width*size):
    rep_found = False
    layer_nb = 0
    while (not rep_found):
        current_layer = layer_split[layer_nb]
        if (int(current_layer[i]) < 2):
            final_image[i] = current_layer[i]
            rep_found = True
        else:
            layer_nb += 1

#solution2 = final_image.reshape((size, width))
#print(solution2)

picture = []
for i in range(len(final_image)):
    if (final_image[i] == 1):
        picture.append("*")
    else:
        picture.append(" ")
picture_string = ''.join(picture)
picture_split = [picture_string[i:i+width] for i in range(0, len(picture_string), width)]

print("Solution part 2:")
for i in range(len(picture_split)):
    print(picture_split[i])

