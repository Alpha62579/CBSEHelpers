"""
CBSEHelpers

A collection of helper functions for my stupid CS project at school
"""

__name__ = "helpers"
__author__ = "Alpha62579"
__version__ = "0.0.10"
__license__ = "MIT"

__path__ = __import__("pkgutil").extend_path(__path__, __name__)

import sys

from . import menu as menu
from . import utils as utils

if not getattr(sys.stdout, "shell", False):
    from . import tty as tty

from .inputs import *
from .menu import *
from .table import *
