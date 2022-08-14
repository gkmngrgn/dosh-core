"""Logging support."""

import logging

__logger = logging.getLogger("dosh")


def get_logger() -> logging.Logger:
    """Get logger of dosh."""
    return __logger


def set_verbosity(verbosity: int = 0) -> None:
    """Set verbosity level for logger."""
    if verbosity >= 3:
        level = logging.DEBUG
    elif verbosity == 2:
        level = logging.INFO
    elif verbosity == 1:
        level = logging.ERROR
    else:
        level = logging.FATAL

    logging.basicConfig(level=level)
