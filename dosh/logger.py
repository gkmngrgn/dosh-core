"""Logging support."""

from logging import DEBUG, ERROR, INFO, WARNING, Logger, basicConfig, getLogger
from typing import Optional

__LOGGER: Optional[Logger] = None


def get_logger() -> Logger:
    """Get logger of dosh."""
    global __LOGGER  # pylint: disable=global-statement

    if __LOGGER is None:
        __LOGGER = getLogger("dosh")

    return __LOGGER


def set_verbosity(verbosity: int = 0) -> None:
    """Set verbosity level for logger."""
    if verbosity >= 3:
        level = DEBUG
    elif verbosity == 2:
        level = INFO
    elif verbosity == 1:
        level = WARNING
    else:
        level = ERROR

    basicConfig(level=level, format="%(message)s")
