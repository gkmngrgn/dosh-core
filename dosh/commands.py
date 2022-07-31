"""Available commands for `dosh.star`."""
import json
import logging
import os
import shutil
import subprocess
import urllib.request
from pathlib import Path
from subprocess import CompletedProcess
from typing import Any, Dict

logger = logging.getLogger("dosh")


def brew_install(*packages: str) -> None:
    """Install packages with brew."""
    # FIXME: not ready yet.


def brew_tap(*repos: str) -> None:
    """Install additional repositories of brew."""
    # FIXME: not ready yet.


def copy(source: str, destination: str) -> None:
    """Copy files from source to destination. It works like `cp` command."""
    src_folder, src_path = source.split("/", 1)
    dst_path = Path(destination)

    # TODO: but what if a source is a file, not folder...
    dst_path.mkdir(parents=True, exist_ok=True)

    for path in Path(src_folder or "/").glob(src_path):
        path_dst = dst_path / path.name

        if path.is_dir():
            shutil.copytree(path, path_dst)
        else:
            shutil.copy(path, path_dst)


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


def exists(path: str) -> bool:
    """Check if the path exists in the file system."""
    return Path(path).exists()


def exists_command(command: str) -> bool:
    """Check if the command exists."""
    return shutil.which(command) is not None


def path(path: str = ".") -> str:
    """Return absolute path."""
    root = "/" if path.startswith("/") else "."
    return Path(root).joinpath(*path.split("/")).as_posix()
