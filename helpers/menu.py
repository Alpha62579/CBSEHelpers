"""
This file contains functions for constructing user-navigation menus.
"""

import sys
import traceback
from typing import Optional, List, Callable, Union, TypeVar, Any

from .inputs import get_str
from .utils import cls_scr, get_termsize, Align

M = TypeVar('M', bound='Menu')


class MenuOption:
    def __init__(self, *, name: str, callback: Union[Callable, M], n: Optional[int] = None) -> None:
        self.name = name
        self.callback = callback
        self.n = n

    def callback(self) -> Any:
        pass


def option(name: Optional[str] = None, *, n: Optional[int] = None) -> Callable[[Callable], MenuOption]:
    """
    Decorator for adding an option to a menu.
    :param name: The display name of the option. Defaults to the name of the function.
    :param n: The position number of the function. Defaults to the order in which the functions are defined.
              Multiple options with the same value of n will result in alphabetical order being preferred.
    :return: Callable[[Callable], MenuOption]
    """

    def decorator(func: Callable) -> MenuOption:
        opt = MenuOption(name=name or func.__name__, callback=func, n=n)
        return opt

    return decorator


class Menu:
    """
    A class for creating menus.
    """

    def __init__(self, *, title: Optional[str] = None, subtitle: Optional[str] = None,
                 options: Optional[List[MenuOption]] = None, parent: Optional[M] = None) -> None:
        """
        :param title: The title of the menu. Defaults to the name of the class.
        :param subtitle: The subtitle of the menu. Defaults to None.
        :param options: A list of options for the menu. Defaults to None.
                        It is recommended to use the @option decorator. instead
        :param parent:
        """
        self.title = title or self.__class__.__name__
        self.subtitle = subtitle
        self._options = options or []
        self._parent = parent
        self._termsize = get_termsize()

        for attr in dir(self):
            if isinstance(getattr(self, attr), MenuOption):
                self._options.append(getattr(self, attr))

    def on_error(self, error: Exception) -> None:
        sys.stderr.write('\n'.join(traceback.format_tb(error.__traceback__)))

    def on_exit(self) -> None:
        pass

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self):
        return f"<Menu={self.title} options={len(self._options)}>"

    def add_option(self, option: MenuOption) -> None:
        """
        Adds an option to the menu. It is recommended to use the @option decorator instead.
        :param option: The option to add.
        """
        self._options.append(option)

    def option(self, name: Optional[str] = None, *, n: Optional[int] = None) -> Callable[[Callable], MenuOption]:
        """
        Decorator for adding an option to a menu.
        :param name: The display name of the option. Defaults to the name of the function.
        :param n: The position number of the function. Defaults to the order in which the functions are defined.
                  Multiple options with the same value of n will result in alphabetical order being preferred.
        :return: Callable[[Callable], MenuOption]
        """

        def decorator(func: Callable) -> MenuOption:
            opt = MenuOption(name=name or func.__name__, callback=func, n=n)
            self.add_option(opt)
            return opt

        return decorator


    def __pre_invoke(self):
        cls_scr()
        self._options.sort(key=lambda x: x.n or 0)

    def _invoke(self, align=Align.LEFT) -> None:
        self.__pre_invoke()
        while True:
            try:
                # Add support for aligning the title
                print(f"{Align.align(self.title, align=align)}")
                if self.subtitle is not None:
                    print(f"{Align.align(self.subtitle, align=align)}")
                print()
                for i, option in enumerate(self._options):
                    print(Align.align(f"{i + 1}) {option.name}", align=align))

                if self._parent is None:
                    print(Align.align("q) Exit", align=align))
                else:
                    print(Align.align("b) Back", align=align))
                    print(Align.align("q) Go back to the main menu", align=align))

                choice = get_str("Enter your choice: ", error_str="Please enter a valid choice.",
                                 check=lambda x: x in '1234567890bq' and (
                                     0 <= int(x) <= len(self._options) if x.isdigit() else True) and (
                                                         x != 'b' or self._parent is not None))
                if choice == 'b':
                    self._parent.invoke()
                if choice == 'q':
                    if self._parent is not None:
                        temp = self
                        while temp._parent is not None:
                            temp = temp._parent
                        temp.invoke()
                    else:
                        self.on_exit()
                        break

                else:
                    cls_scr()
                    self._options[int(choice) - 1].callback(self)
                    print()
                    input("Press Enter to continue...")
                    cls_scr()
            except Exception as e:
                self.on_error(e)

    def start(self):
        self._invoke()


if __name__ == '__main__':
    print("This file is not meant to be run directly.")
