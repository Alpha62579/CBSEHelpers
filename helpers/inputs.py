"""
This file contains functions for getting user input.
"""

import difflib
import sys
from typing import Optional, Callable


def get_int(prompt: str, /, *, error_str: Optional[str] = "Please enter a valid input.",
            check: Callable[[int], bool] = lambda x: True) -> int:
    """
    Gets an integer from the user.
    :param prompt: The prompt to display to the user.
    :param error_str: The error message to display to the user. Defaults to "Please enter a valid input."
    :param check: The function to check the input against. The callable must accept one argument and return a boolean.
    :return: int
    """
    while True:
        try:
            value = int(input(prompt))
            if check(value):
                return value
            else:
                sys.stderr.write(error_str)
        except ValueError:
            sys.stderr.write(error_str)


def get_float(prompt: str, /, *, error_str: Optional[str] = "Please enter a valid input.",
              check: Callable[[float], bool] = lambda x: True) -> float:
    """
    Gets a float from the user.
    :param prompt: The prompt to display to the user.
    :param error_str: The error message to display to the user. Defaults to "Please enter a valid input."
    :param check: The function to check the input against. The callable must accept one argument and return a boolean.
    :return: float
    """
    while True:
        try:
            value = float(input(prompt))
            if check(value):
                return value
            else:
                sys.stderr.write(error_str)
        except ValueError:
            sys.stderr.write(error_str)


def get_bool(prompt: str, /, *, error_str: Optional[str] = "Please enter a valid input.") -> bool:
    """
    Gets a boolean from the user.
    This supports the usage of y/n, yes/no, true/false, and 1/0.
    :param prompt: The prompt to display to the user.
    :param error_str: The error message to display to the user. Defaults to "Please enter a valid input."
    :return: bool
    """
    while True:
        value = input(prompt).lower().strip()
        if value in difflib.get_close_matches(value, ('yes', 'no', 'true', 'false', '1', '0')):
            if value in ('yes', 'true', '1'):
                return True
            elif value in ('no', 'false', '0'):
                return False
        else:
            sys.stderr.write(error_str)


def get_str(prompt: str, /, *, error_str: Optional[str] = "Please enter a valid input.",
            check: Callable[[str], bool] = lambda x: True) -> str:
    """
    Gets a string from the user.
    :param prompt: The prompt to display to the user.
    :param error_str: The error message to display to the user. Defaults to "Please enter a valid input."
    :param check: The function to check the input against. The callable must accept one argument and return a boolean.
    :return: str
    """
    while True:
        value = input(prompt).strip()
        if check(value):
            return value
        else:
            sys.stderr.write(error_str)


if __name__ == '__main__':
    print("This file is not meant to be run directly.")
