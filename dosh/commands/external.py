"""Available commands for `dosh.star`."""
import shutil
import subprocess
import urllib.request
from pathlib import Path
from subprocess import CompletedProcess
from typing import List, Optional

from dosh.commands.base import (
    CommandResult,
    CommandStatus,
    check_command,
    is_url_valid,
    normalize_path,
)


@check_command("apt")
def apt_install(packages: List[str]) -> CommandResult[None]:
    """Install packages with apt."""
    command = "apt install"

    run(f"{command} {' '.join(packages)}")
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
            run(f"brew tap {tap_path}")

    command = "brew install"
    if cask is True:
        command = f"{command} --cask"

    run(f"{command} {' '.join(packages)}")
    return CommandResult(CommandStatus.OK)


@check_command("winget")
def winget_install(packages: List[str]) -> CommandResult[None]:
    """Install packages with winget."""
    command = "winget install -e --id"

    run(f"{command} {' '.join(packages)}")
    return CommandResult(CommandStatus.OK)


def copy(src: str, dst: str) -> CommandResult[None]:
    """Copy files from source to destination. It works like `cp` command."""
    dst_path = normalize_path(dst)
    glob_index = -1
    src_splitted = src.split("/")
    for index, value in enumerate(src_splitted):
        if "*" in value:
            glob_index = index
            break

    if glob_index >= 0:
        src_path = normalize_path("/".join(src_splitted[:glob_index]))
        for path in src_path.glob("/".join(src_splitted[glob_index:])):
            path_dst = dst_path / path.name

            if path.is_dir():
                shutil.copytree(path, path_dst, dirs_exist_ok=True)
            else:
                shutil.copy(path, path_dst)
    else:
        src_path = normalize_path(src)
        shutil.copy(src_path, dst_path / src_path.name)

    return CommandResult(CommandStatus.OK)


@check_command("git")
def clone(url: str, destination: str = "", fetch: bool = False) -> CommandResult[None]:
    """Clone repository from VCS."""
    if fetch is True and Path(destination).exists():
        command = f"git pull {destination}".strip()
    else:
        command = f"git clone {url} {destination}".strip()
    run(command)
    return CommandResult(CommandStatus.OK)


def run(command: str) -> CommandResult[CompletedProcess[bytes]]:
    """Run a shell command using subprocess."""
    result = subprocess.run(command.split(), capture_output=True, check=True)
    return CommandResult(CommandStatus.OK, response=result)


def run_url(url: str) -> CommandResult[CompletedProcess[bytes]]:
    """Run a remote shell script directly."""
    if not is_url_valid(url):
        message = f"URL is not valid: {url}"
        return CommandResult(CommandStatus.ERROR, message=message)
    with urllib.request.urlopen(url) as response:
        content = response.read()
    result = subprocess.run(content, capture_output=True, shell=True, check=True)
    return CommandResult(CommandStatus.OK, response=result)


def exists(path: str) -> CommandResult[bool]:
    """Check if the path exists in the file system."""
    if not Path(path).exists():
        message = f"The path `{path}` doesn't exist in this system."
        return CommandResult(CommandStatus.ERROR, message=message, response=False)
    return CommandResult(CommandStatus.OK, response=True)


def exists_command(command: str) -> CommandResult[bool]:
    """Check if the command exists."""
    if shutil.which(command) is None:
        message = f"The command `{command}` doesn't exist in this system."
        return CommandResult(CommandStatus.ERROR, message=message, response=False)
    return CommandResult(CommandStatus.OK, response=True)