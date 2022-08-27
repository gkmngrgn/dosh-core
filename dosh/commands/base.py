"""Common helper functions and classes for commands submodule."""
import functools
import shutil
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Generic, Optional, TypeVar
from urllib.parse import urlparse

T = TypeVar("T")


class CommandStatus(Enum):
    """Command status for handling the results."""

    OK = "ok"
    ERROR = "error"


@dataclass
class CommandResult(Generic[T]):
    """Return type of command functions."""

    status: CommandStatus
    message: Optional[str] = None
    response: Optional[T] = None

    def __repr__(self) -> str:
        """Return result as repr."""
        return str(self.response)

    def __bool__(self) -> bool:
        """Return false if command status is not ok."""
        return self.status == CommandStatus.OK


CommandCallable = Callable[..., CommandResult[Any]]


def check_command(
    command_name: str,
) -> Callable[[CommandCallable], CommandCallable]:
    """Check command and return error if the command doesn't exist."""

    def decorator(func: CommandCallable) -> CommandCallable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> CommandResult[Any]:
            if shutil.which(command_name) is None:
                message = f"The command `{command_name}` doesn't exist in this system."
                return CommandResult(CommandStatus.ERROR, message=message)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def is_url_valid(url: str) -> bool:
    """Check if url is valid."""
    result = urlparse(url)
    return all([result.scheme, result.netloc])


def normalize_path(file_path: str) -> Path:
    """Convert file paths to absolute paths."""
    path = Path(file_path)
    if file_path.startswith("~"):
        path = path.expanduser()
    elif file_path.startswith("."):
        path = path.absolute()
    return path