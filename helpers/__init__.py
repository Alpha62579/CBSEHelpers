"""
CBSEHelpers

A collection of helper functions for my stupid CS project at school
"""

__name__ = "helpers"
__author__ = "Alpha62579"
__version__ = "0.0.9"
__license__ = "MIT"

__path__ = __import__('pkgutil').extend_path(__path__, __name__)

from . import menu as menu
from . import utils as utils

try:
    from . import tty as tty
except ImportError:
    pass

from .inputs import *
from .menu import *
from .table import *
