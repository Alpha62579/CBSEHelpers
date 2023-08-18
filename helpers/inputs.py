"""
This file contains functions for getting user input.
"""

import difflib
import sys
from typing import Optional, Callable


def get_int(prompt: str, /, *, error_str: Optional[str] = "Please enter a valid input.",
            check: Callable[[int], bool] = lambda x: True, cinput: Callable[[str], str] = input) -> int:
    """
    Gets an integer from the user.
    :param prompt: The prompt to display to the user.
    :param error_str: The error message to display to the user. Defaults to "Please enter a valid input."
    :param check: The function to check the input against. The callable must accept one argument and return a boolean.
    :param cinput: The function to use for getting input. Defaults to input.
    :return: int
    """
    while True:
        try:
            value = int(cinput(prompt))
            if check(value):
                return value
            else:
                sys.stderr.write(f'{error_str}\n')
        except ValueError:
            sys.stderr.write(f'{error_str}\n')


def get_float(prompt: str, /, *, error_str: Optional[str] = "Please enter a valid input.",
              check: Callable[[float], bool] = lambda x: True, cinput: Callable[[str], str] = input) -> float:
    """
    Gets a float from the user.
    :param prompt: The prompt to display to the user.
    :param error_str: The error message to display to the user. Defaults to "Please enter a valid input."
    :param check: The function to check the input against. The callable must accept one argument and return a boolean.
    :param cinput: The function to use for getting input. Defaults to input.
    :return: float
    """
    while True:
        try:
            value = float(cinput(prompt))
            if check(value):
                return value
            else:
                sys.stderr.write(f'{error_str}\n')
        except ValueError:
            sys.stderr.write(f'{error_str}\n')


def get_bool(prompt: str, /, *, error_str: Optional[str] = "Please enter a valid input.", cinput: Callable[[str], str] = input) -> bool:
    """
    Gets a boolean from the user.
    This supports the usage of y/n, yes/no, true/false, and 1/0.
    :param prompt: The prompt to display to the user.
    :param error_str: The error message to display to the user. Defaults to "Please enter a valid input."
    :param cinput: The function to use for getting input. Defaults to input.
    :return: bool
    """
    while True:
        value = cinput(prompt).lower().strip()
        if value in difflib.get_close_matches(value, ('yes', 'no', 'true', 'false', '1', '0', 'y', 'n', 't', 'f', 'on', 'off', 'enable', 'disable', 'enabled', 'disabled')):
            return value in ('yes', 'true', '1', 'y', 't', 'on', 'enable', 'enabled')
        else:
            sys.stderr.write(f'{error_str}\n')


def get_str(prompt: str, /, *, error_str: Optional[str] = "Please enter a valid input.",
            check: Callable[[str], bool] = lambda x: True, cinput: Callable[[str], str] = input) -> str:
    """
    Gets a string from the user.
    :param prompt: The prompt to display to the user.
    :param error_str: The error message to display to the user. Defaults to "Please enter a valid input."
    :param check: The function to check the input against. The callable must accept one argument and return a boolean.
    :param cinput: The function to use for getting input. Defaults to input.
    :return: str
    """
    while True:
        value = cinput(prompt).strip()
        if check(value):
            return value
        else:
            sys.stderr.write(f'{error_str}\n')


if __name__ == '__main__':
    print("This file is not meant to be run directly.")
