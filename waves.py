"""
Indefinitely draw a quantised sine wave, parametrised by the below constants

Press Ctrl+C to interrupt.
"""

from time import sleep
from math import sin, pi
from itertools import cycle

# global constants - you can edit these
LINES_PER_PERIOD = 40
LINES_PER_SECOND = 10
PERIODS_PER_WAVE = 5
MAX_WIDTH = 80

USE_ASCII = False

# general wave functions, with period 2 * pi, such that
# f: R -> [0, 1], f(2n * pi + x) = f(x)
sin_wave = lambda x: (sin(x) + 1) / 2
square_wave = lambda x: 1 if x % (2 * pi) > pi else 0
sawtooth_wave = lambda x: (x % (2 * pi)) / (2 * pi)

def main():
    for wave in cycle([sin_wave, square_wave, sawtooth_wave]):
        for x in range(PERIODS_PER_WAVE * LINES_PER_PERIOD):
            print(("-" if USE_ASCII else "\u2500")
                * int(MAX_WIDTH * wave(2 * pi * x / LINES_PER_PERIOD)))
            sleep(1 / LINES_PER_SECOND)

if __name__ == "__main__":
    main()
