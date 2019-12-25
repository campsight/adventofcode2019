import copy
input_values = []
import csv
with open('input_d14test.txt', 'r') as input_file:
    reader = csv.reader(input_file, delimiter='*')
    for row in reader:
        input_values.append(', '.join(row))

formulas = []
f_inputs = []
f_outputs = []

print(input_values)
for line in input_values:
    splitline = line.split("=> ")
    inputs = splitline[0].split(',')
    inputs = [x.strip().split(' ') for x in inputs]
    inputs = [[int(x[0]), x[1]] for x in inputs]
    f_inputs.append(inputs)
    output = splitline[1].split(' ')
    output[0] = int(output[0])
    f_outputs.append(output)
    formulas.append(output[1])

print(f_outputs)
print(f_inputs)
print(formulas)

ingredients = {}

for line in f_inputs:
    for prescr in line:
        if prescr[1] not in ingredients.keys():
            ingredients[prescr[1]] = 0

print(ingredients)


def get_ingredients_for(i_element, i_quantity):
    location = formulas.index(i_element)
    mix_quantity = f_outputs[location][0]
    production_multiple = i_quantity // mix_quantity
    if (i_quantity % mix_quantity) > 0:
        production_multiple += 1
    leftover_quantity = (production_multiple * mix_quantity) - i_quantity
    ingredients = f_inputs[location]
    result = [[x[0] * production_multiple, x[1]] for x in ingredients]
    return [result, leftover_quantity]



def calculate_recipe(level_of_fuel):
    recipe = {}
    final_step = False
    leftovers = copy.deepcopy(ingredients)
    #next_step = get_ingredients_for('FUEL', level_of_fuel)
    next_step = get_ingredients_for('FUEL', level_of_fuel)[0]

    while not final_step:
        prepare_next_step = []
        for prescription in next_step:
            element = prescription[1]
            quantity = prescription[0]
            print("making", quantity, "of", element)
            if element in leftovers.keys():
                lo_quantity = leftovers[element]
                print(lo_quantity, " in leftovers")
                if (lo_quantity >= quantity):
                    leftovers[element] -= quantity
                    quantity = 0
                else:
                    quantity -= lo_quantity
                    leftovers[element] = 0
            if (quantity > 0):
                rresult = get_ingredients_for(element, quantity)
                extra_quantity = rresult[1]
                next_ingredients = rresult[0]
                print("Recipe requires", next_ingredients, "and gives leftover of", extra_quantity)
                if next_ingredients[0][1] == 'ORE':
                    #print("coming to the source")
                    if element in recipe.keys():
                        recipe[element] += quantity
                    else:
                        recipe[element] = quantity
                else:
                    if extra_quantity > 0:
                        leftovers[element] = extra_quantity
                    prepare_next_step += next_ingredients
        if len(prepare_next_step) == 0:
            print("final one", recipe)
            final_step = True
        else:
            print("current recipe", recipe)
            print("prepare next", prepare_next_step)
            next_step = copy.deepcopy(prepare_next_step)

    ore_required = 0
    recipe_extra = {}
    recipe_in_ore = {}
    element_leftovers = {}
    for el in recipe:
        rresult = get_ingredients_for(el, recipe[el])
        ore_required += rresult[0][0][0]
        recipe_in_ore[el] = rresult[0][0][0]
        recipe_extra[el] = rresult[1]
        element_leftovers[el] = 0
        quantity = recipe[el]
        #print(rresult[1])
    print("ore required: ", ore_required)
    #print(recipe_extra)
    return [recipe, recipe_in_ore, recipe_extra]

result = calculate_recipe(1)
print(result[0])
print(result[1])
print(result[2])

'''
#part 2
print("****** PART 2 *******")
recipe = result[0]
recipe_in_ore = result[1]
recipe_extra = result[2]
#print("recipe ", recipe)
#print("recipe in ore", recipe_in_ore)
#print("recipe extra", recipe_extra)

ore_required = 0
for el in recipe_in_ore:
    ore_required += recipe_in_ore[el]

#print("ore reqruied", ore_required)

ORE_IN_TANK = 1000000000000
ore_supplied = ORE_IN_TANK
fuel = 0
recalculate = True
while recalculate:
    #print("current level of fuel", fuel)
    basic_fuel = ore_supplied // ore_required
    #print("basic_fuel", basic_fuel)
    fuel += basic_fuel
    for el in recipe:
        required_of_el = basic_fuel * recipe[el]
        #print("el", el, "requires", required_of_el)
        required_ores_for_el = (required_of_el // (recipe[el] + recipe_extra[el])) * recipe_in_ore[el]
        ore_supplied -= required_ores_for_el
    if ore_supplied >= (ore_required * 2):
        #print("next step with", ore_supplied)
        recalculate = True
    else:
        recalculate = False

print("first fuel", fuel)

continue_calculating = True
while continue_calculating:
    result = calculate_recipe(fuel)
    nxt_recipe = result[0]
    nxt_recipe_in_ore = result[1]
    nxt_recipe_extra = result[2]
    #print("next recipe", nxt_recipe)
    #print("next recipe in ore", nxt_recipe_in_ore)
    #print("next recipe extra", nxt_recipe_extra)
    nxt_ore_required = 0
    for el in nxt_recipe_in_ore:
        nxt_ore_required += nxt_recipe_in_ore[el]
    #print("next ore reqruied", nxt_ore_required)
    basic_fuel = (ORE_IN_TANK - nxt_ore_required) // ore_required
    #print("basic fuel next", basic_fuel)
    if basic_fuel > 0:
        fuel += basic_fuel
        print("new fuel", fuel)
    else:
        continue_calculating = False

print("fuel produced", fuel)'''