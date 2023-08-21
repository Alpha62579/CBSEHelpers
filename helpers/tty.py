"""
Functions related to terminal fonts
"""

import sys

if getattr(sys.stdout, "shell", False):
    sys.stderr.write("Warning: tty module is not compatible with the current shell\n")
    sys.stderr.write("Warning: tty module will not be loaded\n")
    sys.stderr.flush()
    raise ImportError


class Fore:
    BLACK = "30"
    RED = "31"
    GREEN = "32"
    YELLOW = "33"
    BLUE = "34"
    MAGENTA = "35"
    CYAN = "36"
    WHITE = "37"
    DEFAULT = "39"


class Back:
    BLACK = "40"
    RED = "41"
    GREEN = "42"
    YELLOW = "43"
    BLUE = "44"
    MAGENTA = "45"
    CYAN = "46"
    WHITE = "47"
    DEFAULT = "49"


class Style:
    DEFAULT = "0"
    BRIGHT = "1"
    DIM = "2"
    ITALIC = "3"
    UNDERLINE = "4"
    BLINKING = "5"
    INVERTED = "7"
    HIDDEN = "8"
    STRIKETHROUGH = "9"


class Font:
    def __init__(
        self, *styles: str, fore: str = Fore.DEFAULT, back: str = Back.DEFAULT
    ) -> None:
        self.prefix = f'\033[{fore};{back}{(";" + ";".join(styles)) if styles else ""}m'
        self.fore = fore
        self.back = back
        self.styles = styles

    def __str__(self) -> str:
        return self.prefix

    def __repr__(self) -> str:
        return "<Font fore: {}, back: {}, styles: {}>".format(
            self.fore, self.back, self.styles
        )

    def format(self, text: str) -> str:
        return self.prefix + text + "\033[0m"

    @staticmethod
    def nformat(
        text: str, *styles: str, fore: str = Fore.DEFAULT, back: str = Back.DEFAULT
    ) -> str:
        return f'\033[{fore};{back}{(";" + ";".join(styles)) if styles else ""}m{text}\033[0m'


def move_up(n: int) -> str:
    print(f"\033[{n}A", end="")


def move_down(n: int) -> str:
    print(f"\033[{n}B", end="")


def move_right(n: int) -> str:
    print(f"\033[{n}C", end="")


def move_left(n: int) -> str:
    print(f"\033[{n}D", end="")


def move_to(x: int, y: int) -> str:
    print(f"\033[{x};{y}H", end="")


def clear_line() -> str:
    print("\033[K", end="")


def save_cursor() -> str:
    print("\033[s", end="")


def restore_cursor() -> str:
    print("\033[u", end="")
