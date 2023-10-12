"""
This file contains functions for constructing user-navigation menus.
"""

import sys
import traceback
from typing import Optional, List, Callable, Union, TypeVar, Any

from .inputs import get_str
from .utils import cls_scr, get_termsize, Align

M = TypeVar("M", bound="Menu")


class MenuOption:
    def __init__(
        self,
        *,
        name: str,
        callback: Union[Callable, M],
        disabled: bool = False,
        n: Optional[int] = None,
    ) -> None:
        self.name = name
        self.callback = callback
        self.disabled = disabled
        self.n = n

    def callback(self) -> Any:
        pass


def option(
    name: Optional[str] = None, *, disabled: bool = False, n: Optional[int] = None
) -> Callable[[Callable], MenuOption]:
    """
    Decorator for adding an option to a menu.
    :param name: The display name of the option. Defaults to the name of the function.
    :param disabled: Sets whether this option is disabled or not. Defaults to `False`.
    :param n: The position number of the function. Defaults to the order in which the functions are defined.
              Multiple options with the same value of n will result in alphabetical order being preferred.
    :return: Callable[[Callable], MenuOption]
    """

    def decorator(func: Callable) -> MenuOption:
        opt = MenuOption(
            name=name or func.__name__, callback=func, disabled=disabled, n=n
        )
        return opt

    return decorator


class Menu:
    """
    A class for creating menus.
    """

    def __init__(
        self,
        *,
        title: Optional[str] = None,
        subtitle: Optional[str] = None,
        options: Optional[List[MenuOption]] = None,
        align: Optional[int] = Align.LEFT,
        parent: Optional[M] = None,
    ) -> None:
        """
        :param title: The title of the menu. Defaults to the name of the class.
        :param subtitle: The subtitle of the menu. Defaults to None.
        :param options: A list of options for the menu. Defaults to None.
                        It is recommended to use the @option decorator.
        :param align: Sets the alignment of the menu. Defaults to the left.
        :param parent: Set this option to the parent menu instance if you intend
                        to use this menu as a sub-menu.
        """
        self.title = title or self.__class__.__name__
        self.subtitle = subtitle
        self._options = options or []
        self._parent = parent
        self._align = align
        self._termsize = get_termsize()

        for attr in dir(self):
            if isinstance(getattr(self, attr), MenuOption):
                self._options.append(getattr(self, attr))

    def on_error(self, error: Exception) -> None:
        sys.stderr.write("\n".join(traceback.format_tb(error.__traceback__)))
        input("Press Enter to continue...")
        cls_scr()

    def on_exit(self) -> None:
        pass

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"<Menu={self.title} options={len(self._options)}>"

    def add_option(self, option: MenuOption) -> None:
        """
        Adds an option to the menu. It is recommended to use the @option decorator instead.
        :param option: The option to add.
        """
        self._options.append(option)

    def get_option(
        self, *, n: Optional[int] = None, callback: Optional[Callable[[Any], Any]]
    ) -> Optional[MenuOption]:
        """
        Gets the relevant MenuOption based on either the position (as shown in menu) or the callback.
        Returns the MenuOption or None if not found. Raises ValueError if both
        `n` and `callback` are specified.

        :param n: The position number to search for.
        :param callback: The callback to search with.
        """
        if n is not None and callback is not None:
            raise ValueError("Both n and callback params are specified.")

        if n is not None:
            return None if (n - 1) > len(self._options) else self._options[n - 1]

        if callback is not None:
            return (
                opts[0]
                if len(
                    (opts := [opt for opt in self._options if opt.callback == callback])
                )
                > 0
                else None
            )

    def option(
        self,
        name: Optional[str] = None,
        *,
        disabled: bool = False,
        n: Optional[int] = None,
    ) -> Callable[[Callable], MenuOption]:
        """
        Decorator for adding an option to a menu.
        :param name: The display name of the option. Defaults to the name of the function.
        :param disabled: Sets whether this option is disabled or not. Defaults to `False`.
        :param n: The position number of the function. Defaults to the order in which the functions are defined.
                  Multiple options with the same value of n will result in alphabetical order being preferred.
        :return: Callable[[Callable], MenuOption]
        """

        def decorator(func: Callable) -> MenuOption:
            opt = MenuOption(
                name=name or func.__name__, callback=func, disabled=disabled, n=n
            )
            self.add_option(opt)
            return opt

        return decorator

    def set_align(self, align: int):
        """
        Sets the alignment of the menu.

        :param align: The alignment to use.
        """
        self._align = align

    def __pre_invoke(self):
        cls_scr()
        self._options.sort(key=lambda x: x.n or 0)

    def _invoke(self) -> None:
        self.__pre_invoke()
        while True:
            try:
                # Add support for aligning the title
                print(f"{Align.align(self.title, align=self._align)}")
                if self.subtitle is not None:
                    print(f"{Align.align(self.subtitle, align=self._align)}")
                print()
                for i, option in enumerate(
                    [opt for opt in self._options if not opt.disabled]
                ):
                    print(Align.align(f"{i + 1}) {option.name}", align=self._align))

                if self._parent is None:
                    print(Align.align("q) Exit", align=self._align))
                else:
                    print(Align.align("b) Back", align=self._align))
                    print(Align.align("q) Go back to the main menu", align=self._align))

                choice = get_str(
                    "Enter your choice: ",
                    error_str="Please enter a valid choice.",
                    check=lambda x: x and x in "1234567890bq"
                    and (0 <= int(x) <= len(self._options) if x.isdigit() else True)
                    and (x != "b" or self._parent is not None),
                )
                if choice == "b":
                    self._parent.invoke()
                if choice == "q":
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
                    self._options[int(choice) - 1].callback()
                    print()
                    input("Press Enter to continue...")
                    cls_scr()
            except Exception as e:
                self.on_error(e)

    def start(self):
        self._invoke()


if __name__ == "__main__":
    print("This file is not meant to be run directly.")
