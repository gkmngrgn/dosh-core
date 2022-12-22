"""Common helper functions and classes for commands submodule."""
from __future__ import annotations

import functools
import os
import shutil
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar
from urllib.parse import urlparse

from dosh import DoshInitializer

T = TypeVar("T")


class CommandStatus(Enum):
    """Command status for handling the results."""

    OK = "ok"
    ERROR = "error"


class OperatingSystem(str, Enum):
    """Operating system types."""

    LINUX = "linux"
    MACOS = "macos"
    WINDOWS = "windows"
    UNSUPPORTED = "unsupported"

    @classmethod
    def get_current(cls) -> OperatingSystem:
        """Get current operating system."""
        os_type = os.getenv("OSTYPE") or ""

        if os_type.startswith("darwin"):
            return cls.MACOS

        if os_type == "linux":
            return cls.LINUX

        if os_type == "msys":
            return cls.WINDOWS

        return cls.UNSUPPORTED


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


@dataclass
class Task:
    """Parsed arguments from dosh config."""

    name: str
    command: CommandCallable
    description: str = ""
    environments: Optional[List[str]] = None
    required_commands: Optional[List[str]] = None
    required_platforms: Optional[List[str]] = None

    @classmethod
    def from_dict(cls, args: Dict[str, Any]) -> Task:
        """Create task from arguments."""
        return cls(**args)


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
    if file_path.startswith("/"):
        path = Path(file_path)
    else:
        path = DoshInitializer().base_directory.joinpath(*file_path.split("/"))

    if file_path.startswith("~"):
        path = path.expanduser()
    elif not file_path.startswith("/"):
        path = path.absolute()
    return path
