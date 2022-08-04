"""Available commands for `dosh.star`."""
import functools
import logging
import shutil
import subprocess
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from subprocess import CompletedProcess
from typing import Any, Generic, List, Optional, TypeVar

logger = logging.getLogger("dosh")


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
    result: Optional[T] = None

    def __repr__(self) -> str:
        """Return result as repr."""
        return str(self.result)

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
            result = exists_command(command_name)
            if result.status != CommandStatus.OK:
                return CommandResult(CommandStatus.ERROR, message=result.message)
            return func(*args, **kwargs)

        return wrapper

    return decorator


@check_command("apt")
def apt_install(packages: List[str]) -> CommandResult[None]:
    """Install packages with apt."""
    command = "apt install"

    eval(f"{command} {' '.join(packages)}")
    return CommandResult(CommandStatus.OK)


@check_command("brew")
def brew_install(
    packages: List[str],
    cask: bool = False,
    taps: Optional[List[str]] = None,
) -> CommandResult[None]:
    """Install packages with brew."""
    if taps is not None:
        for tap_path in taps:
            eval(f"brew tap {tap_path}")

    command = "brew install"
    if cask is True:
        command = f"{command} --cask"

    eval(f"{command} {' '.join(packages)}")
    return CommandResult(CommandStatus.OK)


@check_command("winget")
def winget_install(packages: List[str]) -> CommandResult[None]:
    """Install packages with winget."""
    command = "winget install -e --id"

    eval(f"{command} {' '.join(packages)}")
    return CommandResult(CommandStatus.OK)


def copy(source: str, destination: str) -> CommandResult[None]:
    """Copy files from source to destination. It works like `cp` command."""
    src_folder, src_path = source.split("/", 1)
    dst_path = Path(destination)

    for path in Path(src_folder or "/").glob(src_path):
        path_dst = dst_path / path.name

        if path.is_dir():
            shutil.copytree(path, path_dst, dirs_exist_ok=True)
        else:
            shutil.copy(path, path_dst)

    return CommandResult(CommandStatus.OK)


@check_command("git")
def clone(url: str, target: str = ".", sync: bool = False) -> CommandResult[None]:
    """Clone repository from VCS."""
    if sync is True and Path(target).exists():
        command = f"git pull {target}"
    else:
        command = f"git clone {url} {target}"
    eval(command)
    return CommandResult(CommandStatus.OK)


def eval(command: str) -> CompletedProcess[bytes]:
    """Run a shell command using subprocess."""
    return subprocess.run(command.split(), capture_output=True)


def eval_url(url: str) -> CompletedProcess[bytes]:
    """Run a remote shell script directly."""
    # TODO: validate URL first.
    with urllib.request.urlopen(url) as response:
        content = response.read()

    return subprocess.run(content, capture_output=True, shell=True)


def exists(path: str) -> CommandResult[bool]:
    """Check if the path exists in the file system."""
    if not Path(path).exists():
        message = f"The path `{path}` doesn't exist in this system."
        return CommandResult(CommandStatus.ERROR, message=message, result=False)
    return CommandResult(CommandStatus.OK, result=True)


def exists_command(command: str) -> CommandResult[bool]:
    """Check if the command exists."""
    if shutil.which(command) is None:
        message = f"The command `{command}` doesn't exist in this system."
        return CommandResult(CommandStatus.ERROR, message=message, result=False)
    return CommandResult(CommandStatus.OK, result=True)


def path(path: str = ".") -> CommandResult[str]:
    """Return absolute path."""
    root = "/" if path.startswith("/") else "."
    result = Path(root).joinpath(*path.split("/")).as_posix()
    return CommandResult(CommandStatus.OK, result=result)
