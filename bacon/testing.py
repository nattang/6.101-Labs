graph = {1: [2, 3, 4], 2: [1, 3, 7, 8], 3: [4, 1, 2, 5, 6], 
4: [9, 1, 3], 5: [3, 11], 6: [3], 7: [2], 8: [2], 9: [4, 10 ,11], 10: [9], 11: [9, 5]}


def bacon_path(graph, start, goal):
    # keep track of explored nodes
    visited = []
    # keep track of all the paths to be checked
    queue = [[start]]
 
    # return path if start is goal
 
    # keeps looping until all possible paths have been checked
    while queue:
        # pop the first path from the queue
        path = queue.pop(0)
        print(path)
        # get the last node from the path
        node = path[-1]
        if node not in visited:
            # go through all neighbour nodes, construct a new path and
            # push it into the queue
            for neighbour in graph[node][0]:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                # return path if neighbour is goal
                if neighbour == goal:
                    return new_path
 
            # mark node as explored
            visited.append(node)

def bacon_path_2(graph, start, goal):
    visited = [start]
    distance = {start: 0}
    queue = [start]
    prev = {}

    while queue:
        v = queue.pop(0)
        for adj in graph[v]:
            if adj not in visited:
                visited.append(adj)
                distance[adj] = distance[v] + 1
                prev[adj]= v
                queue.append(adj)
                if adj == goal:
                    path = [adj]
                    while adj != start:
                        path.append(prev[adj])
                        adj = prev[adj]
                    path.reverse()
                    return path

def bacon_path_3(transformed_data, actor_id, starting_node = 4724):
    visited = {actor: False for actor in transformed_data}
    queue = [starting_node]

    visited[starting_node]= [starting_node]
    while queue:
        v = queue.pop(0)
        for adj in transformed_data[v][0]:
            if visited[adj] == False:
                if adj == actor_id:
                    return visited[v][:] + [adj]
                queue.append(adj)
                visited[adj]=visited[v][:] + [adj]
    return None

def get_list():
    list1 = []
    list2 = []
    for i in range(8):
        list1.append(i)
    for i in range(3):
        list2.append(i)
    return list1, list2

for list1, list2 in get_list():
    print(list1, list2)