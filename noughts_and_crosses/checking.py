"""
Functions implementing grid checks, efficiently.
"""

from argparse import ArgumentParser

from base import State
from formatting import get_board_template

def get_args():
    """
    Get size of board
    """
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("n", type=int, help="size of board to check")
    return parser.parse_args()

def _make_groups(n):
    """
    This function should not be accessed directly - use get_groups.  Construct
    the list of "groups" present on the board - rows, columns, diagonals. Groups
    are represented as Python ranges because they're all around suitable -
    efficient, linear etc. Return a list of lists of these groups, where
    indexing by board position returns the list of groups that that position is
    contained in. This is pretty memory-efficient as each actual list is only
    stored once, and the remainder of the data structure is primarily pointers.
    """
    rows = ([r for i in range(n)
               for r in [range(i * n, i * n + n), range(i, i + n ** 2, n)]]
          + [range(0, n ** 2, n + 1), range(n - 1, n ** 2 - n + 1, n - 1)])

    return [[r for r in rows if i in r] for i in range(n ** 2)]

# The registry for groups
GROUP_REGISTRY = {}

def get_groups(n):
    """
    Access a list of groups. This checks if the groups have been generated and
    cached already, and if not, does so, caching them in the process, and then
    returns.
    """
    if n in GROUP_REGISTRY:
        return GROUP_REGISTRY[n]
    else:
        GROUP_REGISTRY[n] = _make_groups(n)
        return GROUP_REGISTRY[n]

def is_run(board, pos, n):
    """
    Check if one tile is a part of any complete groups.
    """
    return any(len(set(board[i] for i in group)) == 1 for group in get_groups(n)[pos])

def get_state(board, n):
    """
    Get state of board. This function is given no information about position
    so is necessarily much slower. If you do know the last played tile, use
    is_run instead, as this only checks all groups pertaining to that tile.
    """
    for pos, m in enumerate(board):
        if m is not None:
            if is_run(board, pos, n=n):
                if m:
                    return State.X_WIN
                return State.O_WIN
    if board.count(None) == 0:
        return State.DRAW
    return State.NEUTRAL

def show_groups(n):
    """
    Demo function which displays each groups using functions from formatting.py.
    """
    board_temp = get_board_template(n)
    for ind, pos in enumerate(get_groups(n)):
        print(ind, pos)
        for g in pos:
            dft = [" "] * n ** 2
            for i in g:
                dft[i] = "G"
            dft[ind] = 'M'
            print(board_temp.format(*dft), end="\n\n")

if __name__ == "__main__":
    #args = get_args()
    show_groups(3)
