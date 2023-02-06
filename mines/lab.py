#!/usr/bin/env python3

import typing
import doctest
import time
import pickle

# NO ADDITIONAL IMPORTS ALLOWED!
directions = [(1, -1), (1, 0), (1, 1), (0, -1), (0, 0), (0, 1), (-1, -1), (-1, 0), (-1, 1)]

def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# 2-D IMPLEMENTATION
def bomb_neighbors(bombs, r, c, num_rows, num_cols):
    """
    returns number of neighboring bombs
    """
    count = 0
    for direction in directions:
        new_coors = (direction[0] + r, direction[1] + c)
        if 0 <= new_coors[0] < num_rows and 0 <= new_coors[1] < num_cols:
            if new_coors in bombs:
                count += 1
    
    return count


def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, True, True, True]
        [True, True, True, True]
    state: ongoing
    """

    return new_game_nd((num_rows, num_cols), bombs)

def reveal(game, row, col, num_rows, num_cols):
    '''
    returns number of neighbors to dig up
    '''
    count = 0
    for direction in directions:
        new_row =  direction[0] + row
        new_col = direction[1] + col
        if 0 <= new_row< num_rows and 0 <= direction[1] + col < num_cols and game["board"][new_row][new_col] != "." and game["hidden"][new_row][new_col] == True:
            count += dig_2d(game, new_row, new_col)

    return count

def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['hidden'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is revealed on the board after digging (i.e. game['hidden'][bomb_location]
    == False), 'victory' when all safe squares (squares that do not contain a
    bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, False, False, False]
        [True, True, False, False]
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    hidden:
        [False, False, True, True]
        [True, True, True, True]
    state: defeat
    """
    
    return dig_nd(game, (row, col))


def render_2d_locations(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  game['hidden'] indicates which squares should be hidden.  If
    xray is True (the default is False), game['hidden'] is ignored and all
    cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the that are not
                    game['hidden']

    Returns:
       A 2D array (list of lists)

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, False, True],
    ...                   [True, True, False, True]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, True, False],
    ...                   [True, True, True, False]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    return render_nd(game, xray)



def render_2d_board(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'hidden':  [[False, False, False, True],
    ...                            [True, True, False, True]]})
    '.31_\\n__1_'
    """
    g = render_2d_locations(game, xray)
    s = ''
    for i in range(len(g)):
        for j in range(len(g[0])):
            s += g[i][j]
        if i != len(g) -1: 
            s += '\n' 

    return s

# N-D IMPLEMENTATION
def fill_grid(dimensions, value):
        '''
        fills grid of arbitrary dimensions with a certain value
        '''
        out = []
        if len(dimensions) == 1:
            return [value for i in range(dimensions[0])]
        
        else:
            for i in range(dimensions[0]):
                out.append(fill_grid(dimensions[1:], value))

        return out

def get_neighbors(dimensions, coors):
    '''
    list of all neighbors
    '''
    out = []
    directions = (-1, 0, 1)
    if len(coors) == 0:
        return [()]
    
    else:
        for direction in directions:
            for neighbor in get_neighbors(dimensions[1:],coors[1:]):
                val = coors[0]+ direction
                if 0<= val < dimensions[0]:
                    out.append((val,) + (neighbor))

    return out

def set_value(board, location, value):
    '''
    takes in array of arbitrary dimensions and mutates a location to be a certain value
    '''
    #base case
    if len(location) == 1:
        board[location[0]] = value
    
    else:
        return set_value(board[location[0]], location[1:], value)


def get_value(board, location):
    '''
    gets value of arbitrary dimensions and returns value at a certain location
    '''
    if 0<= location[0] < len(board):
        if len(location) == 1:
            return board[location[0]]
        else:
            val = get_value(board[location[0]], location[1:])
            return val if val != None else None
    else:
        return None

def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, True], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    state: ongoing
    """
    start = time.time()
    
    hidden = fill_grid(dimensions, True)
    board = fill_grid(dimensions, 0)
    
    for bomb in bombs:
        set_value(board, bomb, '.')
        for neighbor in get_neighbors(dimensions, bomb):
            current = get_value(board, neighbor)
            if isinstance(current, int):
                set_value(board, neighbor, current + 1)
    
    return {'dimensions': dimensions,
'board': board, 'hidden': hidden, 'state': 'ongoing'}

def get_coors(dimensions):
    '''
    returns list of all possible coordinates to check if it satisfies victory check
    '''
    out = []
    if len(dimensions) == 0:
        return [()]
    for i in range(dimensions[0]):
        for coor in get_coors(dimensions[1:]):
            out.append((i,) + coor )

    return out


def victory_check(game):
    '''
    checks to see if game is won
    '''
    for coor in get_coors(game['dimensions']):
        tile = get_value(game['board'], coor)
        hidden = get_value(game['hidden'], coor)
        
        if tile != '.' and hidden:
            return False
    return True


def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the hidden to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is revealed on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, False], [False, False], [False, False]]
        [[True, True], [True, True], [False, False], [False, False]]
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, False], [True, False], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    state: defeat
    """
    visited = set(coordinates)
    start = time.time()
    def recursive_helper(game, coordinates): 
        revealed = 1
        if game['state'] != 'ongoing' or get_value(game['hidden'], coordinates) == False:
            return 0

        set_value(game['hidden'], coordinates, False)

        if get_value(game['board'], coordinates) == '.':
            game['state'] = 'defeat'
            return 1

        if get_value(game['board'], coordinates) == 0:
            for neighbor in get_neighbors(game['dimensions'], coordinates):
                if neighbor not in visited:
                    visited.add(neighbor)
                    revealed += recursive_helper(game, neighbor)
    
        return revealed

    x = recursive_helper(game, coordinates)

    if victory_check(game):
        game['state'] = 'victory'
    
    return x
    
def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  The game['hidden'] array indicates which squares should be
    hidden.  If xray is True (the default is False), the game['hidden'] array
    is ignored and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [False, False],
    ...                [False, False]],
    ...               [[True, True], [True, True], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    out = []
    #base case:
    
    if isinstance(game['board'], str) or isinstance(game['board'], int):
        if not xray:
            if not game['hidden']:
                if game['board'] == 0:
                    return ' '
                else:
                    return str(game['board'])
            else:
                return '_'
        else:
            return str(game['board']) if game['board'] != 0 else ' '
    
    for i in range(len(game['board'])):
        inner_game = {'board': game['board'][i], 'hidden': game['hidden'][i]}
        out.append(render_nd(inner_game, xray))

    return out


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d_locations or any other function you might want.  To
    # do so, comment out the above line, and uncomment the below line of code.
    # This may be useful as you write/debug individual doctests or functions.
    # Also, the verbose flag can be set to True to see all test results,
    # including those that pass.
    #
    #doctest.run_docstring_examples(render_2d_locations, globals(), optionflags=_doctest_flags, verbose=False)
    with open("test_inputs/testnd_integration1.pickle", "rb") as f:
        game = pickle.load(f)

g = {'dimensions': (2, 4, 2),
'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
[['.', 3], [3, '.'], [1, 1], [0, 0]]],
'hidden': [[[True, True], [True, False], [True, True],
[True, True]],
[[True, True], [True, True], [True, True],
  [True, True]]],
'state': 'ongoing'}

print(dig_nd(g, (0, 3, 0)))
