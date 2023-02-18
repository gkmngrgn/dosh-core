"""Available commands for `dosh.star`."""
from __future__ import annotations

import shutil
import subprocess
import urllib.request
from pathlib import Path
from subprocess import CompletedProcess
from typing import List, Optional

from dosh.commands.base import (
    CommandResult,
    CommandStatus,
    FileType,
    check_command,
    copy_tree,
    is_url_valid,
    normalize_path,
)
from dosh.logger import get_logger
from dosh.lua_runtime import LuaTable, lua_runtime

logger = get_logger()


@check_command("apt")
def apt_install(packages: List[str]) -> CommandResult[None]:
    """Install packages with apt."""
    command = "apt install"

    run(f"{command} {' '.join(packages)}")
    return CommandResult(CommandStatus.OK)


@check_command("brew")
def brew_install(
    packages: LuaTable, options: Optional[LuaTable] = None
) -> CommandResult[None]:
    """Install packages with brew."""
    if options is None:
        options = lua_runtime.table()

    for tap_path in list((options["taps"] or lua_runtime.table()).values()):
        run(f"brew tap {tap_path}")

    command = "brew install"

    if options["cask"] is True:
        command = f"{command} --cask"

    run(f"{command} {' '.join(list(packages.values()))}")
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
            copy_tree(path, dst_path / path.name)
    else:
        path = normalize_path(src)
        copy_tree(path, dst_path / path.name if dst_path.exists() else dst_path)

    return CommandResult(CommandStatus.OK)


@check_command("git")
def clone(url: str, options: Optional[LuaTable] = None) -> CommandResult[None]:
    """Clone repository from VCS."""
    if options is None:
        options = lua_runtime.table()

    destination = normalize_path(
        options["destination"] or url.rsplit("/", 1)[-1].rsplit(".git", 1)[0]
    )

    if destination.exists():
        logger.info("[CLONE] the folder `%s` already exists. skipped.", destination)
    else:
        command = f"git clone {url} {destination}"
        run(command)

    return CommandResult(CommandStatus.OK)


def scan_directory(
    parent_dir: str = ".", file_types: Optional[List[str]] = None
) -> CommandResult[List[str]]:
    """List files and folders."""
    parent = normalize_path(parent_dir)

    if not parent.is_dir():
        return CommandResult(CommandStatus.ERROR, message=f"Not a folder: {parent_dir}")

    files, directories = [], []

    for item in parent.iterdir():
        if item.is_dir():
            directories.append(str(item))
        elif item.is_file():
            files.append(str(item))

    items = []

    if file_types is None:
        file_types = [FileType.FILE, FileType.DIRECTORY]

    if FileType.FILE in file_types:
        items.extend(files)

    if FileType.DIRECTORY in file_types:
        items.extend(directories)

    return CommandResult(CommandStatus.OK, response=items)


def run(command: str) -> CommandResult[str]:
    """Run a shell command using subprocess."""
    logger.info("[RUN] %s", command)

    response_lines = []
    with subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    ) as proc:
        for out, log in [(proc.stdout, logger.debug), (proc.stderr, logger.error)]:
            if out is None:
                continue

            while True:
                line = out.readline()
                if not line:
                    break

                line_str = line.decode().rstrip()
                response_lines.append(line_str)
                log(line_str)

        returncode = proc.wait()
        if returncode == 0:
            status = CommandStatus.OK
        else:
            status = CommandStatus.ERROR

    return CommandResult(status, response="\n".join(response_lines))


def run_url(url: str) -> CommandResult[CompletedProcess[bytes]]:
    """Run a remote shell script directly."""
    if not is_url_valid(url):
        message = f"URL is not valid: {url}"
        return CommandResult(CommandStatus.ERROR, message=message)
    with urllib.request.urlopen(url) as response:
        content = response.read()

    logger.info("[RUN_URL] %s", url)
    result = subprocess.run(content, shell=True, capture_output=True, check=True)
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
