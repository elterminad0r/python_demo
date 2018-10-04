"""
Implementation of the special case of the minmax algorithm, suited to noughts
and crosses.
"""

from textwrap import indent
from traceback import extract_stack

from base import Win
from checking import State, is_run
from formatting import print_board, strfboard, syms
from interface import SquareBoard, isqrt

from argparse import ArgumentParser

def get_args():
    """
    Get arguments if a demo run is being executed. A demo run will just
    determine the move to be used against a preset board, verbosely by default.
    """
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("-b", "--board", type=SquareBoard, default='_o__x____',
                    help='The initial board state')
    parser.add_argument("-q", "--quiet", action="store_true",
                    help="do not print minmax tree")
    return parser.parse_args()

# boolean-indexed array to get states compactly and quickly
state_from_bool = [State.O_WIN, State.X_WIN]

def optimise(evaluations, is_crosses, minimise):
    """
    "Optimise" a sequence of results for a given player. This simultaneously
    implements both minimisation and maximisation with a bit of Boolean logic.
    It also knows how to short-circuit - if maximising, a win is known to be the
    best possible case and vice verse.
    """
    LOSE_STATE, WIN_STATE = state_from_bool[minimise ^ (not is_crosses)], state_from_bool[minimise ^ is_crosses]
    draw_seen = False
    for e in evaluations:
        if e == LOSE_STATE:
            return e
        elif e == State.DRAW:
            draw_seen = True
    if draw_seen:
        return State.DRAW
    return WIN_STATE

def generate_moves(board, is_crosses):
    """
    Generate possible moves on a board for a certain player. This works by
    mutating the actual board array for each possible move, followed by yielding
    both the move and the board. This is useful as it allows "iteration" over
    moves, while also being memory-efficient (which leads to time efficiency as
    there is no allocation overhead).
    A finally clause implements the restoration of the board, which guarantees
    that the board will retain its state from before after this function exits,
    even if the function is interrupted by, for example, a break.
    """
    for ind, i in enumerate(board):
        if i is None:
            try:
                board[ind] = is_crosses
                yield ind, board
            finally:
                board[ind] = None

def evaluate_board(board, is_crosses, crosses_playing, prev_move, depth, n,
      verbose=False):
    """
    Evaluate a board-state for a given player. This recursively generates moves,
    evaluates them and optimises them.
    Allows printing diagnostics with the verbosity parameter. It will indent
    depending on the current length of the callstack, which helps keep track of
    the recursion.
    """
    verbose and print(indent("Examining as {} {}:\n{}"
                         .format(syms[crosses_playing], depth,
                            indent(strfboard(board, n), ' ')),
                      ' ' * len(extract_stack())))
    if is_run(board, prev_move, n):
        state = state_from_bool[not crosses_playing]
        verbose and print(indent("State here: {}"
                  .format(state), " " * len(extract_stack())))
        return state
    elif depth == len(board):
        verbose and print(indent("Draw here", " " * len(extract_stack())))
        return State.DRAW
    else:
        return optimise(
                (evaluate_board(board, is_crosses, not crosses_playing,
                                move, depth + 1, n, verbose=verbose)
                   for move, board in generate_moves(board, crosses_playing)),
                 is_crosses, not crosses_playing ^ is_crosses)

def get_computer_move(board, is_crosses, n, verbose=False):
    """
    Apply board evaluation to all possible moves and
    select, in order:
    - A winning move
    - A drawing move
    - Any move (which will be a losing move)
    """
    # optimisation: play here for an empty board, because searching through the
    # whole board's tree is known to be unnecessary
    if all(i is None for i in board):
        return 0
    WIN_STATE = state_from_bool[is_crosses]
    moves = generate_moves(board, is_crosses)
    draw = None
    for move, board in moves:
        ev = evaluate_board(board, is_crosses, not is_crosses, move,
                            len(board) - board.count(None), n, verbose=verbose)
        if ev == WIN_STATE:
            verbose and print("Win incoming")
            return move
        elif ev == State.DRAW:
            verbose and print("Draw forcable")
            draw = move
    if draw is not None:
        return draw
    return board.index(None)

def do_computer_move(board, is_crosses, n, verbose=False):
    """
    Wraps get_computer_move to print some stuff, mutate the board and check for
    winning conditions.
    """
    move = get_computer_move(board, is_crosses, n, verbose=verbose)
    board[move] = is_crosses
    print("Computer plays at ({}, {})".format(move % n, move // n))
    print_board(board, n)
    if is_run(board, move, n):
        raise Win("I'm sorry, Dave. I'm afraid I can't do that.")

if __name__ == "__main__":
    #args = get_args()
    board = [None] * 9 #args.board
    n = 3 #isqrt(len(args.board))
    print(board, n)
    print_board(board, n)
    do_computer_move(board, True, n, verbose=True)
