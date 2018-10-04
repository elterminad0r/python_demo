"""
Handling and verifying user input
"""

from base import Win
from formatting import print_board, syms
from checking import is_run

# boolean-indexed array to get a string name for player
name_from_bool = ["noughts", "crosses"]

# dictionary to translate symbols to internal representation of tile states
state_from_string = {"_": None, 'x': True, 'o': False}

def isqrt(n):
    """
    Calculate the integer square root of a number using the "bit-shift"
    algorithm.
    """
    if n < 2:
        return n
    else:
        small = isqrt(n >> 2) << 1
        large = small + 1
        if large ** 2 > n:
            return small
        else:
            return large

def SquareInt(s):
    """
    Acts as a "parser" for perfect square integers for argparse
    """
    n = int(s)
    if isqrt(n) ** 2 != n:
        raise ValueError("{!r} is not a square number".format(s))
    return n

def SquareBoard(board):
    """
    Acts as a "parser" for strings representing square boards, similar to
    SquareInt. Ignores all non-interesting characters and demands squareness.
    """
    b = [state_from_string[c] for c in board if c in state_from_string]
    if isqrt(len(b)) ** 2 != len(b):
        raise ValueError('The board must be square')
    return b

def get_pos(s, n):
    """
    Get position in 1d list from 2d coordinate reference
    """
    x, y = map(int, s.split())
    if not all(0 <= c < n for c in (x, y)):
        raise ValueError("Not in range [0,{})".format(n))

    return y * n + x

def get_input(board, is_crosses, n):
    """
    Get user input of where to play on a board.
    """
    print("You are playing as {}".format(name_from_bool[is_crosses]))
    while True:
        try:
            mov = get_pos(input("Enter the position you want to play in > "), n)
            if board[mov] is not None:
                raise ValueError("This position is already taken")
        except ValueError as ve:
            print(ve)
            continue
        return mov

def do_player_move(board, is_crosses, n):
    """
    Execute player move - assumes board is valid at start of turn.
    """
    print_board(board, n)
    try:
        pos = get_input(board, is_crosses, n)
    except (KeyboardInterrupt, EOFError):
        raise Win("\n{} wins because {} is a coward"
                .format(syms[not is_crosses], syms[is_crosses]))
    board[pos] = is_crosses
    if is_run(board, pos, n):
        raise Win("{} wins".format(syms[is_crosses]))
