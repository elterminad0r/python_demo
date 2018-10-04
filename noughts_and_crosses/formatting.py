"""
Pretty-printing OXO boards, using pre-calculated templates.
"""

from argparse import ArgumentParser
from random import choices, randrange

BOARD_RANGE = 3, 10

def get_args():
    """
    Get size of demo board in case of demo run
    """
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("n", type=int, help="size of demo board")
    return parser.parse_args()

def _make_board_template(n):
    """
    Do not use this function. Use get_board_template instead.
    Generate a str.format compatible template to format a noughts and crosses
    board. This is a lot easier and faster than dynamically generating all of
    the "structure" of the board every time.
    """
    return ("{}\n{}"
              .format("".join(map("{:4}".format, range(n))),
                  "  {}".format("+".join(["---"] * n))
                     .join("\n\n").
                         join(map("{0[0]:2}{0[1]}".format,
                                  enumerate(["|".join([" {} "] * n)] * n)))))

# registry to cache templates
BOARD_REGISTRY = {3: _make_board_template(3)}

def get_board_template(n):
    """
    Get a template by checking to see if it has already been calculated and
    cached, and otherwise doing so before returning it. This layer of
    abstraction prevents any arduous calculation on module import, but rather
    incurs a slight penalty on first usage of the function (which is more likely
    through another function).
    """
    if n in BOARD_REGISTRY:
        return BOARD_REGISTRY[n]
    else:
        BOARD_REGISTRY[n] = _make_board_template(n)
        return BOARD_REGISTRY[n]

def strfboard(board, n):
    """
    Format standard board representation as string.
    """
    return get_board_template(n).format(*map(get_sym, board))

def print_board(board, n):
    """
    Print standard board representation as string.
    """
    print("{}\n".format(strfboard(board, n=n)))

syms = "OX"

def get_sym(i):
    """
    Translate (None, True, False) to " XO"
    """
    if i is None:
        return " "
    return syms[i]

if __name__ == "__main__":
    #args = get_args()
    n = randrange(*BOARD_RANGE) #args.n
    print("{0}x{0} template:\n{1}".format(n, get_board_template(n)))
    print("\nrandom {0}x{0} board:".format(n))
    print(strfboard(choices([None, True, False], k=n**2), n=n))
