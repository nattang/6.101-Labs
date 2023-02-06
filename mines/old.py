#!/usr/bin/env python3

import typing
import doctest

# NO ADDITIONAL IMPORTS ALLOWED!


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
    board = []
    for r in range(num_rows):
        row = []
        for c in range(num_cols):
            if [r, c] in bombs or (r, c) in bombs:
                row.append(".")
            else:
                row.append(0)
        board.append(row)
    hidden = []
    for r in range(num_rows):
        row = []
        for c in range(num_cols):
            row.append(True)
        hidden.append(row)
    for r in range(num_rows):
        for c in range(num_cols):
            if board[r][c] == 0:
                neighbor_bombs = 0
                if 0 <= r - 1 < num_rows:
                    if 0 <= c - 1 < num_cols:
                        if board[r - 1][c - 1] == ".":
                            neighbor_bombs += 1
                if 0 <= r < num_rows:
                    if 0 <= c - 1 < num_cols:
                        if board[r][c - 1] == ".":
                            neighbor_bombs += 1
                if 0 <= r + 1 < num_rows:
                    if 0 <= c - 1 < num_cols:
                        if board[r + 1][c - 1] == ".":
                            neighbor_bombs += 1
                if 0 <= r - 1 < num_rows:
                    if 0 <= c < num_cols:
                        if board[r - 1][c] == ".":
                            neighbor_bombs += 1
                if 0 <= r < num_rows:
                    if 0 <= c < num_cols:
                        if board[r][c] == ".":
                            neighbor_bombs += 1
                if 0 <= r + 1 < num_rows:
                    if 0 <= c < num_cols:
                        if board[r + 1][c] == ".":
                            neighbor_bombs += 1
                if 0 <= r - 1 < num_rows:
                    if 0 <= c + 1 < num_cols:
                        if board[r - 1][c + 1] == ".":
                            neighbor_bombs += 1
                if 0 <= r < num_rows:
                    if 0 <= c + 1 < num_cols:
                        if board[r][c + 1] == ".":
                            neighbor_bombs += 1
                if 0 <= r + 1 < num_rows:
                    if 0 <= c + 1 < num_cols:
                        if board[r + 1][c + 1] == ".":
                            neighbor_bombs += 1
                board[r][c] = neighbor_bombs
    return {
        "dimensions": (num_rows, num_cols),
        "board": board,
        "hidden": hidden,
        "state": "ongoing",
    }


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
    if game["state"] == "defeat" or game["state"] == "victory":
        game["state"] = game["state"]  # keep the state the same
        return 0

    if game["board"][row][col] == ".":
        game["hidden"][row][col] = False
        game["state"] = "defeat"
        return 1

    bombs = 0
    hidden_squares = 0
    for r in range(game["dimensions"][0]):
        for c in range(game["dimensions"][1]):
            if game["board"][r][c] == ".":
                if game["hidden"][r][c] == False:
                    bombs += 1
            elif game["hidden"][r][c] == True:
                hidden_squares += 1
    if bombs != 0:
        # if bombs is not equal to zero, set the game state to defeat and
        # return 0
        game["state"] = "defeat"
        return 0
    if hidden_squares == 0:
        game["state"] = "victory"
        return 0

    if game["hidden"][row][col] != False:
        game["hidden"][row][col] = False
        revealed = 1
    else:
        return 0

    if game["board"][row][col] == 0:
        num_rows, num_cols = game["dimensions"]
        if 0 <= row - 1 < num_rows:
            if 0 <= col - 1 < num_cols:
                if game["board"][row - 1][col - 1] != ".":
                    if game["hidden"][row - 1][col - 1] == True:
                        revealed += dig_2d(game, row - 1, col - 1)
        if 0 <= row < num_rows:
            if 0 <= col - 1 < num_cols:
                if game["board"][row][col - 1] != ".":
                    if game["hidden"][row][col - 1] == True:
                        revealed += dig_2d(game, row, col - 1)
        if 0 <= row + 1 < num_rows:
            if 0 <= col - 1 < num_cols:
                if game["board"][row + 1][col - 1] != ".":
                    if game["hidden"][row + 1][col - 1] == True:
                        revealed += dig_2d(game, row + 1, col - 1)
        if 0 <= row - 1 < num_rows:
            if 0 <= col < num_cols:
                if game["board"][row - 1][col] != ".":
                    if game["hidden"][row - 1][col] == True:
                        revealed += dig_2d(game, row - 1, col)
        if 0 <= row < num_rows:
            if 0 <= col < num_cols:
                if game["board"][row][col] != ".":
                    if game["hidden"][row][col] == True:
                        revealed += dig_2d(game, row, col)
        if 0 <= row + 1 < num_rows:
            if 0 <= col < num_cols:
                if game["board"][row + 1][col] != ".":
                    if game["hidden"][row + 1][col] == True:
                        revealed += dig_2d(game, row + 1, col)
        if 0 <= row - 1 < num_rows:
            if 0 <= col + 1 < num_cols:
                if game["board"][row - 1][col + 1] != ".":
                    if game["hidden"][row - 1][col + 1] == True:
                        revealed += dig_2d(game, row - 1, col + 1)
        if 0 <= row < num_rows:
            if 0 <= col + 1 < num_cols:
                if game["board"][row][col + 1] != ".":
                    if game["hidden"][row][col + 1] == True:
                        revealed += dig_2d(game, row, col + 1)
        if 0 <= row + 1 < num_rows:
            if 0 <= col + 1 < num_cols:
                if game["board"][row + 1][col + 1] != ".":
                    if game["hidden"][row + 1][col + 1] == True:
                        revealed += dig_2d(game, row + 1, col + 1)

    bombs = 0  # set number of bombs to 0
    hidden_squares = 0
    for r in range(game["dimensions"][0]):
        # for each r,
        for c in range(game["dimensions"][1]):
            # for each c,
            if game["board"][r][c] == ".":
                if game["hidden"][r][c] == False:
                    # if the game hidden is False, and the board is '.', add 1 to
                    # bombs
                    bombs += 1
            elif game["hidden"][r][c] == True:
                hidden_squares += 1
    bad_squares = bombs + hidden_squares
    if bad_squares > 0:
        game["state"] = "ongoing"
        return revealed
    else:
        game["state"] = "victory"
        return revealed


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
    out = []
    for i in range(game['dimensions'][0]):
        
        row = []
        for j in range(game['dimensions'][1]):
            value = game['board'][i][j]
            if not xray:
                if not game['hidden'][i][j]:
                    if value == 0:
                        row.append(' ')
                    else:
                        row.append(str(value)) 
                else: 
                    row.append('_')
            else:
                row.append(str(value)) if value != 0 else row.append(' ')
        out.append(row)

    return out



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
    raise NotImplementedError


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
    raise NotImplementedError


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
    raise NotImplementedError