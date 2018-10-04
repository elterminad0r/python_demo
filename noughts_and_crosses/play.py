"""
Play noughts and crosses. Incorporates both human and computer players.

RUN THIS FILE TO ACTUALLY PLAY AGAINST THE COMPUTER
"""

from argparse import ArgumentParser
from itertools import cycle, repeat
from textwrap import dedent

from base import GameFinish, Draw
from interface import do_player_move
from computer import do_computer_move as _do_computer_move

BOARD_SIZE = 3

def get_args():
    """
    Get configuration for the program. See the help text for details.
    """
    parser = ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("-c", "--computer", action="store_true",
                    help="play against computer opponent")
    mode.add_argument("-b", "--battle", action="store_true",
                    help="computer plays against itself")
    parser.add_argument("--headstart", action="store_true",
                    help="start first when playing against computer")
    parser.add_argument("--noughts-start", action="store_true",
                    help="noughts to start instead of crosses")
    parser.add_argument("-s", "--size", type=int, default=3,
                    help="size of board to play on")
    parser.add_argument("-v", "--verbose", action="store_true",
                    help="Show minmax thought process")
    return parser.parse_args()

def play(board, players, noughts_start, n):
    """
    Play a game of noughts and crosses until a finishing condition or a draw,
    given an infinite iterable of players.
    """
    is_crosses = not noughts_start
    try:
        for player in players:
            player(board, is_crosses, n)
            is_crosses = not is_crosses
            if board.count(None) == 0:
                raise Draw("Nobody wins!")
    except GameFinish as gf:
        print("{}: {}".format(type(gf).__name__, gf))

if __name__ == "__main__":
    vb = False #args.verbose
    do_computer_move = lambda *args: _do_computer_move(*args, verbose=vb)
    while True:
        print("\n\n\nLet's play against the computer!")
        print(dedent("""
            Enter a move by writing its x coordinate followed by its y
            coordinate, separated by spaces. For example:

            this is the middle:
            > 1 1
            this is the left middle:
            > 0 1
            """.strip()))
        players = cycle([do_computer_move, do_player_move])
        play([None] * BOARD_SIZE ** 2, players, True, BOARD_SIZE)
