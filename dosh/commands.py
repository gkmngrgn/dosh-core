"""Available commands for `dosh.star`."""
import logging
import os
import shutil
import subprocess
import urllib.request
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from subprocess import CompletedProcess
from typing import Generic, List, Optional, TypeVar

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

    def __bool__(self) -> bool:
        """Return false if command status is not ok."""
        return self.status == CommandStatus.OK


def apt_install(packages: List[str]) -> CommandResult[None]:
    """Install packages with apt."""
    result = exists_command("apt")
    if result.status != CommandStatus.OK:
        return CommandResult(CommandStatus.ERROR, message=result.message)

    command = "apt install"

    eval(f"{command} {' '.join(packages)}")
    return CommandResult(CommandStatus.OK)


def brew_install(
    packages: List[str],
    cask: bool = False,
    taps: Optional[List[str]] = None,
) -> CommandResult[None]:
    """Install packages with brew."""
    result = exists_command("brew")
    if result.status != CommandStatus.OK:
        return CommandResult(CommandStatus.ERROR, message=result.message)

    if taps is not None:
        for tap_path in taps:
            eval(f"brew tap {tap_path}")

    command = "brew install"
    if cask is True:
        command = f"{command} --cask"

    eval(f"{command} {' '.join(packages)}")
    return CommandResult(CommandStatus.OK)


def winget_install(packages: List[str]) -> CommandResult[None]:
    """Install packages with winget."""
    result = exists_command("winget")
    if result.status != CommandStatus.OK:
        return CommandResult(CommandStatus.ERROR, message=result.message)

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


def clone(url: str, target: str = ".", sync: bool = False) -> None:
    """Clone repository from VCS."""
    # FIXME: not ready yet.


def env(key: str) -> str:
    """Return an OS environment."""
    return os.getenv(key) or ""


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


def path(path: str = ".") -> str:
    """Return absolute path."""
    root = "/" if path.startswith("/") else "."
    return Path(root).joinpath(*path.split("/")).as_posix()
