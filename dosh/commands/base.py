"""Common helper functions and classes for commands submodule."""
from __future__ import annotations

import functools
import platform
import shutil
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar
from urllib.parse import urlparse

from dosh import DoshInitializer
from dosh.logger import get_logger

T = TypeVar("T")
LuaFunction = Callable[..., None]
LuaTable = namedtuple("LuaTable", ["values"])

logger = get_logger()


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
        os_type = platform.system().lower()

        if os_type == "darwin":
            return cls.MACOS

        if os_type == "linux":
            return cls.LINUX

        if os_type == "windows":
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


class Task:  # pylint: disable=too-few-public-methods
    """Parsed arguments from dosh config."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        name: str,
        command: LuaFunction,
        description: str = "",
        environments: Optional[LuaTable] = None,
        required_commands: Optional[LuaTable] = None,
        required_platforms: Optional[LuaTable] = None,
    ) -> None:
        """Parse task parameters getting from Lua config to use in Python code well."""
        self.name = name
        self.command = command
        self.description = description
        self.environments = self.parse_table(environments)
        self.required_commands = self.parse_table(required_commands)
        self.required_platforms = self.parse_table(required_platforms)

    @classmethod
    def from_dict(cls, args: Dict[str, Any]) -> Task:
        """Create task from arguments."""
        return cls(**args)

    def parse_table(self, lua_table: Optional[LuaTable]) -> List[str]:
        """Convert lua table to Python object."""
        return [] if lua_table is None else list(lua_table.values())


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
    elif file_path.startswith("~"):
        path = Path(file_path).expanduser()
    else:
        path = DoshInitializer().base_directory.joinpath(*file_path.split("/"))
    return path


def copy_tree(src: Path, dst: Path) -> None:
    """Copy file or directory to destination."""
    if src.is_dir():
        logger.info("COPY DIR: %s -> %s", src, dst)
        shutil.copytree(src, dst, dirs_exist_ok=True)
    else:
        logger.info("COPY FILE: %s -> %s", src, dst)
        shutil.copy(src, dst)
