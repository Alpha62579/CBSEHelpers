"""
Some useful functions?
"""

import os
from typing import Optional


def cls_scr() -> None:
    """
    Clears the screen.
    """
    # Check if any stupid IDE is running this
    if 'PYCHARM_HOSTED' in os.environ:
        return

    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def get_termsize() -> int:
    """
    Gets the width of the terminal.
    :return: int
    """
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80


class Align:
    """
    An enum for text alignment.
    """
    LEFT = 0
    CENTER = 1
    RIGHT = 2

    @classmethod
    def align(cls, text: str, width: Optional[int] = get_termsize(), align: Optional[int] = 0) -> str:
        """
        Aligns text.
        :param text: The text to align.
        :param width: The width of the text.
        :param align: The alignment to use.
        :return: str
        """
        if align == Align.LEFT:
            return text.ljust(width)
        elif align == Align.CENTER:
            return text.center(width)
        elif align == Align.RIGHT:
            return text.rjust(width)
