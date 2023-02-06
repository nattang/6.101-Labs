#!/usr/bin/env python3

import sys
import typing
import doctest

sys.setrecursionlimit(10_000)
# NO ADDITIONAL IMPORTS

def update_formula(formula, state):
    '''
    state is a tuple of the variable and its value
    update cnf formula based on one known value of a variable.
    remove all rules that include 'value, True'
    remove 'val, False' from all other rules (if present)
    '''
    out = []
    for rule in formula:
        new = rule[:]
        for val in rule:
            if val == (state[0], not state[1]):
                new.remove((state[0], not state[1]))
                if len(new) == 0:
                    return None
                else:
                    out.append(new)
        if (state[0], state[1]) not in rule:
                out.append(new)
    return out

def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a', None) is True or x.get('b', None) is False or x.get('c', None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    """

    out = {}
    if formula == None:
        return None


    formula.sort(key = len)
    #unit clause
    units = True
    while units:
        units = False
        for rule in formula:
            if len(rule) == 1:
                units = True
                out[rule[0][0]] = rule[0][1]
                formula = update_formula(formula, (rule[0][0], rule[0][1]))
               
                if formula == None:
                    return None

                break


    for rule in formula:
        if not rule:
            return None

    if not formula:
        return out

    unit = formula[0][0]

    recur_res_1 = satisfying_assignment(update_formula(formula, unit))
    if recur_res_1 != None:
        out[unit[0]] = unit[1]
        return out | recur_res_1

    recur_res_2 = satisfying_assignment(update_formula(formula, (unit[0], not unit[1])))
    if recur_res_2 != None:
        out[unit[0]] = not unit[1]
        return out | recur_res_2

    return None

def cells(dim):
    '''
    creates clauses related to each unique cell
    '''
    out = []
    for row in range(dim):
        for cell in range(dim):
            #there exists a value in the cell
                #for every possible value, one of them has to be true for this cell
            out.append([((row, cell, val), True) for val in range(1, dim+1)])

            #there is at most one value in the cell
            #for every possible pairs of values, at most one of them can be true for this cell
            for val in range(1, dim+ 1):
                for next_val in range(val + 1, dim + 1):
                    out.append([((row, cell, val), False), ((row, cell, next_val), False)])
    return out


def rows(dim):
    '''
    creates clauses related to each row
    '''
    out = []
    
    for val in range(1, dim + 1):
        for row in range(dim):
            clause = []
            for cell in range(dim):
                #each digit appears at least once in the row
                #goes through each cell in the row and ensures that val is true in there once
                clause.append(((row, cell, val), True))
                #each number appears at most once in the row
                #goes through each pair of cells in the row; the value can be here at most once
                for next_cell in range(cell+1, dim):
                    out.append([((row, cell, val), False), ((row, next_cell, val), False)])
                    #print([((row, cell, val), False), ((row, next_cell, val), False)])
            out.append(clause)
    return out

def columns(dim):
    '''
    creates clauses related to each unique column
    '''
    out = []

    for val in range(1, dim + 1):
        for col in range(dim):
            clause = []
            for cell in range(dim):
                clause.append(((cell, col, val), True))

                for next_cell in range(cell+1, dim):
                    out.append([((cell, col, val), False), ((next_cell, col, val), False)])

            out.append(clause)

    return out

def get_section_coors(layer, cube, dim1):
    out = [] #list of coordinates
    for row in range(layer*dim1, (layer + 1)*(dim1)):
        for col in range(cube*dim1, (cube + 1)*(dim1)):
            out.append((row, col))

    return out


def sections(dim):
    '''
    creates clauses related to each unique section
    '''
    out = []
    dim1 = int(dim**(1/2))
    for layer in range(dim1):
        for cube in range(dim1):
            for val in range(1, dim + 1):
                clause = []
                section_coors = get_section_coors(layer, cube, dim1)
                for i, coor in enumerate(section_coors):
                    clause.append(((coor[0], coor[1], val), True))
                        #clause.append(((row, col, val), True))
                    for next_coor in section_coors[i+1:]:
                        out.append([((coor[0], coor[1], val), False), ((next_coor[0], next_coor[1], val), False)])
                out.append(clause)
    return out



def sudoku_board_to_sat_formula(sudoku_board):
    """
    Generates a SAT formula that, when solved, represents a solution to the
    given sudoku board.  The result should be a formula of the right form to be
    passed to the satisfying_assignment function above.
    """
    out = []
    dim = len(sudoku_board)
    #add all of the established values as True
    for r in range(dim):
        for c in range(dim):
            val = sudoku_board[r][c]
            if val != 0:
                out.append([((r, c, val), True)])
    
    return out + cells(dim)+ rows(dim) + columns(dim) + sections(dim)


def assignments_to_sudoku_board(assignments, n):
    """
    Given a variable assignment as given by satisfying_assignment, as well as a
    size n, construct an n-by-n 2-d array (list-of-lists) representing the
    solution given by the provided assignment of variables.

    If the given assignments correspond to an unsolveable board, return None
    instead.
    """
    out = [[0 for c in range(n)] for r in range(n)]
    if assignments == None:
        return None
    for key in assignments:
        if assignments[key] == True:
            
            out[key[0]][key[1]] = key[2]

    return out


if __name__ == "__main__":
    import doctest

    # _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    # doctest.testmod(optionflags=_doctest_flags)
    

#     cnf = [[('a', True), ('a', False)], [('b', True), ('a', True)], 
#     [('b', True)], [('b', False), ('b', False), ('a', False)], 
#     [('c', True), ('d', True)], [('c', True), ('d', True)]]
#     print(satisfying_assignment([[('a', True)], [('a', False)]]))
    
# test =  [[('a', True), ('a', False)], 
#     [('b', True), ('a', True)], 
#     [('b', True)], 
#     [('b', False), ('b', False), ('a', False)], 
#     [('c', True), ('d', True)], [('c', True), ('d', True)]]

grid = [
            [1, 0, 0, 0],
            [0, 0, 0, 4],
            [3, 0, 0, 0],
            [0, 0, 1, 2],
        ]

assignment = sudoku_board_to_sat_formula(grid)

s = satisfying_assignment(assignment)

print(get_section_coors(1, 1, 2))