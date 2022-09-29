"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    In the initial game state, X gets the first move.
    """

    num_Empty = 0

    # Check status of the board
    for row in board:
        num_Empty += row.count(EMPTY)
    # Determine who's turn it is
    if num_Empty % 2 == 0:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    # Scan the board
    for row in range(0, 3):
        for cell in range(0, 3):
            if board[row][cell] == EMPTY:
                moves.add((row, cell))
    # Return set of possible moves
    if len(moves) > 0:
        # Moves available
        return moves
    else:
        # Terminal board provided
        return None


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Make sure action is not none (resulting from terminal board)
    if action == None:
        # Raise exception
        raise Exception("Invalid action")
    # Make sure the action is of type tuple (i, j)
    if type(action) is not tuple:
        # Raise exception
        raise Exception("Invalid action")
    # Store i and j
    i = action[0]
    j = action[1]
    # Move not available, space taken
    if board[i][j] != EMPTY:
        # Raise exception
        raise Exception("Invalid action")
    # Copy board
    copy = deepcopy(board)
    # Set player's move in deepcopy of board
    copy[i][j] = player(board)
    # Return new board
    return copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Reduce number of checks if center is empty
    if board[1][1] == EMPTY:
        # Check row one for winner
        if board[0][0] == board[0][1] == board[0][2]:
            return board[0][0]
        # Check row three for winner
        if board[2][0] == board[2][1] == board[2][2]:
            return board[2][0]
        # Check column one for winner
        if board[0][0] == board[1][0] == board[2][0]:
            return board[0][0]
        # Check column three for winner
        if board[0][2] == board[1][2] == board[2][2]:
            return board[0][2]
    # Else, check all
    else:
        # Check row one for winner
        if board[0][0] == board[0][1] == board[0][2]:
            return board[0][0]
        # Check row two for winner
        if board[1][0] == board[1][1] == board[1][2]:
            return board[1][0]
        # Check row three for winner
        if board[2][0] == board[2][1] == board[2][2]:
            return board[2][0]
        # Check column one for winner
        if board[0][0] == board[1][0] == board[2][0]:
            return board[0][0]
        # Check column two for winner
        if board[0][1] == board[1][1] == board[2][1]:
            return board[0][1]
        # Check column three for winner
        if board[0][2] == board[1][2] == board[2][2]:
            return board[0][2]
        # Check diagonals for winner
        if board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]
        # Check diagonals for winner
        if board[0][2] == board[1][1] == board[2][0]:
            return board[0][2]
    # No winners found, return none
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Either the game has no winner or is in progress
    if winner(board) == None:
        # If the game is in progress
        if any(EMPTY in row for row in board):
            # Game not over
            return False
        # If game tied
        else:
            # Draw
            return True
    # The game is over
    else:
        # Game over
        return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    You may assume utility will only be called on a board if terminal(board) is
    True.
    """
    # Get the winner of the board
    won = winner(board)
    # If X won
    if won == X:
        return 1
    # If O won
    elif won == O:
        return -1
    # No winner, tied
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Check if the game is over
    if terminal(board):
        return None
    # If it's player O's turn (Minimizing)
    if player(board) == O:
        v, action = min_value(board)
        # Return optimal action
        return action
    # If it's player X's turn (Maximizing)
    else:
        v, action = max_value(board)
        # Return optimal action
        return action


def min_value(board):
    """
    Returns the minimum value that would result from a possible action.
    """
    v = (math.inf)
    best = None
    # If game over, return terminal state's value. No action taken
    if terminal(board):
        return utility(board), None
    # Looping through possible actions
    for action in actions(board):
        # Find current best value and action
        curr = max_value(result(board, action))
        # If new value is less than lowest then update lowest
        if curr[0] < v:
            best = action
            v = curr[0]
            if v == -1:
                return v, best
    # Return min value and best action
    return v, best


def max_value(board):
    """
    Returns the maximum value that would result from a possible action.
    """
    v = (-math.inf)
    best = None
    # If game over, return terminal state's value. No action taken
    if terminal(board):
        return utility(board), None
    # Looping through possible actions
    for action in actions(board):
        # Find current best value and action
        curr = min_value(result(board, action))
        # If new value is greater than highest then update highest
        if curr[0] > v:
            best = action
            v = curr[0]
            if v == 1:
                return v, best
    # Return max value and best action
    return v, best
