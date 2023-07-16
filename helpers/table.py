"""
A module that contains functions to convert a 2D list into a table.
"""

from typing import List
import copy


class Border:
    """
    A class that contains the characters used to draw the table.
    """
    top_left = "┌"
    top_right = "┐"
    bottom_left = "└"
    bottom_right = "┘"
    horizontal = "─"
    vertical = "│"
    thin_vertical = "│"
    cross = "┼"
    top_cross = "┬"
    bottom_cross = "┴"
    left_cross = "├"
    right_cross = "┤"


def format_table(data: List[List[str]], *, headers: List[str] = [], split_entries: bool = False, border: Border = Border) -> List[str]:
    """
    Converts a 2D list into a table.

    :param data: A list of lists containing the data to be converted. The first list is the header.
                 The data must be strings or datatypes that can be converted to strings.
    :param headers: The header of the table. Defaults to the first row of the rows param. Pass `None` for
                 no header.
    :param split_entries: Split rows with horizontal lines. Defaults to `False`.
    :param border: The border to use. Must be Border or a subclass of Border.
    :return: A list of strings that make up the table.
    """
    if len(data) != [len(i) for i in data].count(len(data[0])):
        raise Exception("Inconsistent data provided.")

    rows = copy.deepcopy(data)
    table = []
    if headers == [] and headers is not None:
        headers = rows.pop(0)

    max_char = [max([len(str(row[col])) + 2 for row in rows]) for col in range(len(rows[0]))]

    table.append(border.top_left + border.top_cross.join(
                [border.horizontal * max_char[i] for i in range(len(rows[0]))]) + border.top_right)
    if headers is not None:
        table.append(border.vertical + border.vertical.join(
            [str(headers[i]).center(max_char[i]) for i in range(len(headers))]) +
                     border.vertical)
        table.append(border.left_cross + border.cross.join(
            [border.horizontal * max_char[i] for i in range(len(rows[0]))]) + border.right_cross)
    for row in range(len(rows)):
        table.append(
            border.vertical + border.thin_vertical.join(
                [str(rows[row][i]).center(max_char[i]) for i in range(len(rows[0]))]) +
            border.vertical)
        if split_entries and row != len(rows) - 1:
            table.append(border.left_cross + border.cross.join(
                [border.horizontal * max_char[i] for i in range(len(rows[0]))]) + border.right_cross)
    else:
        table.append(border.bottom_left + border.bottom_cross.join(
            [border.horizontal * max_char[i] for i in range(len(rows[0]))]) + border.bottom_right)

    return table


def tablefy(rows: List[List[str]], *, border: Border = Border) -> None:
    """
    Prints a table.

    :param rows: A list of lists containing the data to be converted. The first list is the header.
                 The data must be strings or datatypes that can be converted to strings.
    :param border: The border to use. Must be Border or a subclass of Border.
    """
    for row in format_table(rows, border=border):
        print(row)


if __name__ == '__main__':
    print("This file is not meant to be run directly.")
