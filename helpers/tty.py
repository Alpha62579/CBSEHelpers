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
        self, *styles: Style, fore: Fore = Fore.DEFAULT, back: Back = Back.DEFAULT
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
        text: str, *styles: Style, fore: Fore = Fore.DEFAULT, back: Back = Back.DEFAULT
    ) -> str:
        return f'\033[{fore};{back}{(";" + ";".join(styles)) if styles else ""}m{text}\033[0m'


def move_up(n: int) -> str:
    return f"\033[{n}A"


def move_down(n: int) -> str:
    return f"\033[{n}B"


def move_right(n: int) -> str:
    return f"\033[{n}C"


def move_left(n: int) -> str:
    return f"\033[{n}D"


def move_to(x: int, y: int) -> str:
    return f"\033[{x};{y}H"


def clear_line() -> str:
    return "\033[K"


def save_cursor() -> str:
    return "\033[s"


def restore_cursor() -> str:
    return "\033[u"
