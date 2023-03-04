"""Common helper functions and classes for commands submodule."""
from __future__ import annotations

import functools
import platform
import shutil
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, TypeVar
from urllib.parse import urlparse

from dosh_core import DoshInitializer
from dosh_core.logger import get_logger
from dosh_core.lua_runtime import LuaFunction

T = TypeVar("T")

logger = get_logger()


class CommandException(Exception):
    """Dosh command exception."""


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


CommandCallable = Callable[..., Any]


@dataclass
class Task:
    """Parsed arguments from dosh config."""

    name: str
    command: LuaFunction
    description: str = ""
    environments: List[str] = field(default_factory=list)
    required_commands: List[str] = field(default_factory=list)
    required_platforms: List[str] = field(default_factory=list)

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
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if shutil.which(command_name) is None:
                raise CommandException(
                    f"The command `{command_name}` doesn't exist in this system."
                )
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