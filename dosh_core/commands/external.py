"""Available commands for `dosh.star`."""
from __future__ import annotations

import logging
import os
import shutil
import subprocess
import urllib.request
from pathlib import Path
from typing import List, Optional

from dosh_core.commands.base import (
    CommandException,
    check_command,
    copy_tree,
    is_url_valid,
    normalize_path,
)
from dosh_core.logger import get_logger
from dosh_core.lua_runtime import LuaTable, lua_runtime

logger = get_logger()


@check_command("apt")
def apt_install(packages: List[str]) -> None:
    """Install packages with apt."""
    command = "apt install"

    run(f"{command} {' '.join(packages)}")


@check_command("brew")
def brew_install(packages: LuaTable, options: Optional[LuaTable] = None) -> None:
    """Install packages with brew."""
    if options is None:
        options = lua_runtime.table()

    for tap_path in list((options["taps"] or lua_runtime.table()).values()):
        run(f"brew tap {tap_path}")

    command = "brew install"

    if options["cask"] is True:
        command = f"{command} --cask"

    run(f"{command} {' '.join(list(packages.values()))}")


@check_command("winget")
def winget_install(packages: List[str]) -> None:
    """Install packages with winget."""
    command = "winget install -e --id"
    run(f"{command} {' '.join(packages)}")


def copy(src: str, dst: str) -> None:
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


@check_command("git")
def clone(url: str, options: Optional[LuaTable] = None) -> None:
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


def scan_directory(parent_dir: str = ".", opts: Optional[LuaTable] = None) -> LuaTable:
    """
    List files and directories.

    Optional parameters:
        include_files: boolean (default: true)
        include_dirs: boolean (default: true)
        excludes: list[str] (default: [])
    """
    parent = normalize_path(parent_dir)
    options = opts or lua_runtime.table()

    if not parent.is_dir():
        raise CommandException(f"Not a folder: {parent_dir}")

    files, directories = [], []

    for item in parent.iterdir():
        if item.is_dir():
            directories.append(str(item))
        elif item.is_file():
            files.append(str(item))

    items = []

    if options["include_files"] is not False:
        items.extend(files)

    if options["include_dirs"] is not False:
        items.extend(directories)

    excludes = list((options["excludes"] or lua_runtime.table()).values())
    if excludes:
        items = list(filter(lambda i: i.rsplit(os.sep, 1)[-1] not in excludes, items))

    response: LuaTable = lua_runtime.table_from(sorted(items))
    return response


def __run_command_and_log_output(content: str) -> int:
    with subprocess.Popen(
        content,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    ) as proc:
        for out, level in [(proc.stdout, logging.DEBUG), (proc.stderr, logging.ERROR)]:
            if out is None:
                continue

            while True:
                line = out.readline()
                if not line:
                    break

                logger.log(level, line.decode().rstrip())

    return proc.wait()


def run(command: str) -> int:
    """Run a shell command using subprocess."""
    logger.info("[RUN] %s", command)
    return __run_command_and_log_output(command)


def run_url(url: str) -> int:
    """Run a remote shell script directly."""
    if not is_url_valid(url):
        raise CommandException(f"URL is not valid: {url}")

    with urllib.request.urlopen(url) as response:
        content = response.read()

    logger.info("[RUN_URL] %s", url)
    return __run_command_and_log_output(content)


def exists(path: str) -> bool:
    """Check if the path exists in the file system."""
    return Path(path).exists()


def exists_command(command: str) -> bool:
    """Check if the command exists."""
    return shutil.which(command) is not None