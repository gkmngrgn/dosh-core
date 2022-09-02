"""Argument parser."""

import sys
from typing import Optional


def find_arg_index(*args: str) -> Optional[int]:
    """Parse CLI arguments and return the index of expected arg."""
    index: Optional[int] = None
    for i, arg in enumerate(sys.argv):
        if arg in args:
            index = i
            break
    return index
