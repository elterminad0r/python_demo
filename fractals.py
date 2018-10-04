"""
Using Python turtle to draw L-system fractals
It uses layered lazy generators so it is very memory-efficient - effectively
using a call-stack of the size of the number of iterations. See [1].

For a version in Python-processing, see
https://github.com/elterminad0r/lsystems

[1]: https://en.wikipedia.org/wiki/L-system
"""

import turtle as t

# set the turtle speed to be very fast
t.speed(0)
w, h = t.screensize()
print(w, h)

from collections import namedtuple
from math import cos, radians

# global constants
SIERP_ITERATIONS = 6
DRAGON_ITERATIONS = 10
FERN_ITERATIONS = 5
LEVY_ITERATIONS = 10
HILBERT_ITERATIONS = 5
SIERP_HEX_ITERATIONS = 7
KOCH_ITERATIONS = 5
ARERA_ITERATIONS = 6

LSystemFractal = namedtuple("LSystemFractal",
                            "name start rules draw_rules iterations")

def substitute(sequence, rules):
    for symbol in sequence:
        if symbol not in rules:
            yield symbol
        else:
            yield from rules[symbol]

def draw_fd(steps, size):
    def f():
        t.forward(steps * w / size)
    return f

STATE_STACK = []

def save_state():
    STATE_STACK.append((t.pos(), t.heading()))

def restore_state():
    pos, heading = STATE_STACK.pop()
    t.penup()
    t.setpos(pos)
    t.setheading(heading)
    t.pendown()

def nop():
    pass

sierpinski = LSystemFractal(
    "Sierpinski's Gasket",
    "F-G-G",
    {"F": "F-G+F+G-F",
     "G": "GG"},
    {"F": draw_fd(1, 2 ** SIERP_ITERATIONS),
     "G": draw_fd(1, 2 ** SIERP_ITERATIONS),
     "-": lambda: t.right(-120),
     "+": lambda: t.right(+120)},
    SIERP_ITERATIONS)

dragon = LSystemFractal(
    "The Dragon Curve",
    "0FX",
    {"X": "X+YF+",
     "Y": "-FX-Y"},
    {"F": draw_fd(1, 2 * 2 ** (DRAGON_ITERATIONS / 2)),
     "-": lambda: t.right(+90),
     "+": lambda: t.right(-90),
     "0": lambda: [t.penup(), t.setpos(0, 0), t.pendown()],
     "X": nop,
     "Y": nop},
    DRAGON_ITERATIONS)

fern = LSystemFractal(
    "A Lindenmayer Fern",
    "0X",
    {"X": "F+[[X]-X]-F[-FX]+X",
     "F": "FF"},
    {"F": draw_fd(1, 3 ** (FERN_ITERATIONS - 1)),
     "-": lambda: t.right(+25),
     "+": lambda: t.right(-25),
     "X": nop,
     "[": save_state,
     "]": restore_state,
     "0": lambda: [t.penup(), t.setpos(0, -h / 2),
                   t.setheading(90), t.pendown()]},
    FERN_ITERATIONS)

levy_c = LSystemFractal(
    "The Levy C Curve",
    "F",
    {"F": "+F--F+"},
    {"F": draw_fd(1, 2 ** (LEVY_ITERATIONS / 2)),
     "-": lambda: t.right(+45),
     "+": lambda: t.right(-45)},
    LEVY_ITERATIONS)

hilbert = LSystemFractal(
    "Hilbert's Space-Filling Curve",
    "A",
    {"A": "-BF+AFA+FB-",
     "B": "+AF-BFB-FA+"},
    {"F": draw_fd(1, 2 ** (HILBERT_ITERATIONS)),
     "A": nop,
     "B": nop,
     "-": lambda: t.right(-90),
     "+": lambda: t.right(+90)},
    HILBERT_ITERATIONS)

sierp_hex = LSystemFractal(
    "Sierpinski's Gasket Hexagonal Variant",
    "A",
    {"A": "B-A-B",
     "B": "A+B+A"},
    {"A": draw_fd(1, 2 ** SIERP_HEX_ITERATIONS),
     "B": draw_fd(1, 2 ** SIERP_HEX_ITERATIONS),
     "-": lambda: t.right(-60),
     "+": lambda: t.right(+60)},
    SIERP_HEX_ITERATIONS)

koch = LSystemFractal(
    "Square Koch Curve",
    "F",
    {"F": "F+F-F-F+F"},
    {"F": draw_fd(1, 3 ** (KOCH_ITERATIONS)),
     "-": lambda: t.right(+90),
     "+": lambda: t.right(-90)},
    KOCH_ITERATIONS)

arera_lighthouse = LSystemFractal(
    "Arera's Lighthouse Tree",
    "0F-G-G",
    {"F": "F-G+F+G-F",
     "G": "GG"},
    {"F": draw_fd(1, 2 ** ARERA_ITERATIONS),
     "G": draw_fd(1, 2 ** SIERP_ITERATIONS),
     "-": lambda: t.right(+127),
     "+": lambda: t.right(-127),
     "0": lambda: t.right(180)},
    ARERA_ITERATIONS)

arera_spread = LSystemFractal(
    "Arera's big old mess",
    "F-G-G",
    {"F": "F-G+F+G-F",
     "G": "GG"},
    {"F": draw_fd(1, (1 / -cos(radians(117))) ** ARERA_ITERATIONS),
     "G": draw_fd(1, (1 / -cos(radians(117))) ** ARERA_ITERATIONS),
     "-": lambda: t.right(-117),
     "+": lambda: t.right(+117)},
    ARERA_ITERATIONS)

def draw_fractal(fractal):
    t.setpos(-w / 2, -h / 2)
    t.setheading(0)
    t.clear()
    t.pendown()
    path = fractal.start
    for _ in range(fractal.iterations):
        path = substitute(path, fractal.rules)
    for symbol in path:
        fractal.draw_rules[symbol]()

fractals = [sierpinski, dragon, fern, levy_c, hilbert, sierp_hex, koch,
            arera_lighthouse, arera_spread]

if __name__ == "__main__":
    while True:
        print("Available fractals:")
        print("\n".join(
            "{}: {}".format(ind, i.name) for ind, i in enumerate(fractals)))
        result = input("Enter number of fractal > ")
        try:
            result = int(result)
            if not (0 <= result < len(fractals)):
                raise ValueError("outside of range")
            try:
                print("Press Ctrl+C to interrupt")
                draw_fractal(fractals[result])
            except KeyboardInterrupt:
                pass
        except ValueError as ve:
            print("error: {}".format(ve))
