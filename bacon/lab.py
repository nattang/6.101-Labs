#!/usr/bin/env python3

from cgi import MiniFieldStorage
import pickle
from tracemalloc import start
from turtle import st

# NO ADDITIONAL IMPORTS ALLOWED!


def transform_data(raw_data):
    dict = {}
    for tup in raw_data:
        if tup[0] not in dict:
            dict[tup[0]] = [{tup[1]}, {tup[2]}]
        else:
            dict[tup[0]][0].add(tup[1])
            dict[tup[0]][1].add(tup[2])
        if tup[1] not in dict:
            dict[tup[1]] = [{tup[0]}, {tup[2]}]
        else:
            dict[tup[1]][0].add(tup[0])
            dict[tup[1]][1].add(tup[2])
    return dict

def acted_together(transformed_data, actor_id_1, actor_id_2):
    result = False
    if actor_id_1 == actor_id_2:
        result = True
    elif actor_id_2 in transformed_data[actor_id_1][0]:
        result = True
    return result

def actors_with_bacon_number(transformed_data, n, starting_node = 4724):
    visited = set()
    queue = [starting_node]
    bacon = {}

    bacon[starting_node] = 0
    visited.add(starting_node)
    

    while queue:          # Creating loop to visit each node
        m = queue.pop(0) 
        for neighbor in transformed_data[m][0]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                bacon[neighbor] = bacon[m] +  1
    return {actor for actor in bacon if bacon[actor] == n}

def bacon_path(transformed_data, actor_id, starting_node = 4724):
    visited = {starting_node}
    queue = [starting_node]
    path = {}
    path[starting_node]= [starting_node]
    while queue:
        m = queue.pop(0)
        for neighbor in transformed_data[m][0]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                path[neighbor] = path[m] + [neighbor]
                
                if neighbor == actor_id:
                    return path[m] + [neighbor]
                
    return None

def get_movies(path, data):
    movies = []
    for i in range(len(path)-1):
        for tup in data:
            if tup[0] == path[i] and tup[1] == path[i+1]:
                movies.append(tup[2])
            elif tup[1] == path[i] and tup[0] == path[i+1]:
                movies.append(tup[2])
    return movies

def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    if actor_id_1 == actor_id_2:
        return [actor_id_1]
    else:
        return bacon_path(transformed_data, actor_id_2, starting_node= actor_id_1)


def actor_path(transformed_data, actor_id_1, goal_test_function):
    visited = {actor_id_1}
    queue = [actor_id_1]
    path = {}
    path[actor_id_1]= [actor_id_1]
    if goal_test_function(actor_id_1):
        return [actor_id_1]
    while queue:
        m = queue.pop(0)
        for neighbor in transformed_data[m][0]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                path[neighbor] = path[m] + [neighbor]
                
                if goal_test_function(neighbor):
                    return path[m] + [neighbor]
    return None


def get_film_actors(transformed_data, film1, film2):
    film1_actors = set()
    film2_actors = set()
    for actor in transformed_data:
        if film1 in transformed_data[actor][1]:
            film1_actors.add(actor)
        if film2 in transformed_data[actor][1]:
            film2_actors.add(actor)
    return (film1_actors, film2_actors)

def actors_connecting_films(transformed_data, film1, film2):
    paths = []
    actor1 = get_film_actors(transformed_data, film1, film2)[0]
    actor2 = get_film_actors(transformed_data, film1, film2)[1]
    for actor_a in actor1:
        for actor_b in actor2:
            try:
                paths.append(actor_to_actor_path(transformed_data, actor_a, actor_b))
            except:
                pass
    if len(paths) > 0:
        shortest = min(paths, key=len)
        return shortest
    else:
        return None



if __name__ == "__main__":
    with open("resources/large.pickle", "rb") as f:
        tiny = pickle.load(f)
    with open("resources/movies.pickle", "rb") as f:
        names = pickle.load(f)
    data = transform_data(tiny)
    ids = get_movies([172559, 323, 102437, 98132, 105288, 1338712, 1338716], tiny)
    #print(actors_with_bacon_number(data, 3))
    #actors = []
    #for id in ids:
        #for name in names:
            #if names[name] == id:
                #actors.append(name)
    
    #print(actors)
    print(actors_connecting_films(data, 18860, 75181))
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    pass

