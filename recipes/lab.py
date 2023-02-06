# Recipes Database
# NO ADDITIONAL IMPORTS!
from json.encoder import INFINITY
import sys
import pickle
from tkinter import mainloop

sys.setrecursionlimit(20_000)


def replace_item(recipes, old_name, new_name):
    """
    Returns a new recipes list based on the input list, where all mentions of
    the food item given by old_name are replaced with new_name.
    """
    out = []
    for elem in recipes:
        for i in range(len(elem)):
            if isinstance(elem[i], list):
                new_elem = elem[:i] + (replace_item(elem[i], old_name, new_name),)
                break

            if elem[i] == old_name and old_name != 'atomic' and old_name!= 'compound':
                new_elem = elem[:i] + (new_name,) + elem[i+1:]
                break
            else:
                new_elem = elem[:]
       
        out.append(new_elem)
    
    return out

def get_instance(recipes, food_item):
    l = []
    for i in range(len(recipes)):
        if recipes[i][1] == food_item:
            l.append(recipes[i])
    return l



def lowest_cost(recipes, food_item, forbidden = []):
    """
    Given a recipes list and the name of a food item, return the lowest cost of
    a full recipe for the given food item.
    """
    prices = []
    main = get_instance(recipes, food_item)

    if len(main) == 0 or food_item in forbidden:
        return None
    
    for elem in main: #go through each possible recipe
        total = 0
        if elem[0] == 'atomic': return elem[2]

        for ing in elem[2]: #find minimum price for each ingredient; check to see if ingredient exists
            ing_price = lowest_cost(recipes, ing[0], forbidden)
            if ing_price == None or ing[0] in forbidden:
                total = None
                break #leave if one of the recipes cannot be made
            else:
                total += ing_price*ing[1] #add minimum price of each ingredient to total
        if total is not None: 
            prices.append(total) 

    return min(prices) if len(prices) != 0 else None

def combine(dict1, dict2):
    mapped = {}
    for key in dict1:
        mapped[key] = dict1[key]
    
    for key in dict2:
        if key in mapped:
            mapped[key] += dict2[key]
        else:
            mapped[key] = dict2[key]

    return mapped

def scale(dict, n):
    new = {}
    for i in dict:
        new[i] = dict[i]*n
    return new


def cheapest_flat_recipe(recipes, food_item, forbidden = ()):
    """
    Given a recipes list and the name of a food item, return a dictionary
    (mapping atomic food items to quantities) representing a full recipe for
    the given food item.
    """
    all = all_flat_recipes(recipes, food_item, forbidden)

    result = None
    def get_total(recipe):
        total = 0
        for ing in recipe:
            if lowest_cost(recipes, ing, forbidden) != None:
                total += lowest_cost(recipes, ing, forbidden)*recipe[ing]

        return total

    lowest = INFINITY

    if all == None:
        return None
    for recipe in all:
        if get_total(recipe) < lowest:
            lowest = get_total(recipe)
            result = recipe

    return result


def all_flat_recipes(recipes, food_item, forbidden = ()):
    """
    Given a list of recipes and the name of a food item, produce a list (in any
    order) of all possible flat recipes for that category.
    """
    #base case
    out = []
    main = get_instance(recipes, food_item)
    
    if not main:
        return []

    for elem in main:
        if elem[0] == 'atomic' and elem[1] not in forbidden:
            return [{elem[1]: 1}]
        elif elem[1] in forbidden:
            return []
        
        
        def all_flat_recipes_list(lst):
            out = []
            if len(lst) == 0:
                return [{}]

            #create list of every recipe for the first value in the list
            l1 = []
            temp = all_flat_recipes(recipes, lst[0][0], forbidden)
            if temp!= None:
                for i in temp:
                    l1.append(scale(i, lst[0][1]))

            #combine w all possible types of the rest of the list
            l2 = all_flat_recipes_list(lst[1:])
            for i in l1:
                if i != None:
                    for j in l2:
                        out.append(combine(i, j))
            return out
        
        for i in all_flat_recipes_list(elem[2]):
            out.append(i)
    return out
    


if __name__ == "__main__":
    # you are free to add additional testing code here!
    #with open("test_recipes/big_recipes_00.pickle", "rb") as f:
        #recipe = pickle.load(f)
    pass


example_recipes = [
    ('compound', 'cookie sandwich', [('cookie', 2), ('ice cream scoop', 3)]),
    ('compound', 'cookie', [('chocolate chips', 3)]),
    ('compound', 'cookie', [('sugar', 10)]),
    ('atomic', 'chocolate chips', 200),
    ('atomic', 'sugar', 5),
    ('compound', 'ice cream scoop', [('vanilla ice cream', 1)]),
    ('compound', 'ice cream scoop', [('chocolate ice cream', 1)]),
    ('atomic', 'vanilla ice cream', 20),
    ('atomic', 'chocolate ice cream', 30),
]


print(all_flat_recipes(example_recipes, 'cookie sandwich', forbidden = ['tomato']))



