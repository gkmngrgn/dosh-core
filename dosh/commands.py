"""Available commands for `dosh.star`."""
import json
import os
import shutil
import subprocess
from pathlib import Path
from subprocess import CompletedProcess
from typing import Any, Dict


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


def clone(url: str, folder: str = ".", sync: bool = False) -> None:
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
    # FIXME: not ready yet.


def exists(path: str) -> bool:
    """Check if the path exists in the file system."""
    return Path(path).exists()


def exists_command(command: str) -> bool:
    """Check if the command exists."""
    # FIXME: not ready yet.


def home_dir(path: str = ".") -> str:
    """Return absolute path."""
    return Path.home().joinpath(*path.split("/")).as_posix()


def inject_print_commands(locals: Dict[str, Any]) -> None:
    """Inject a function to parse commands in user-defined dosh configuration."""
    from inspect import isfunction

    prefix = "cmd_"
    commands = filter(
        lambda k: k.startswith(prefix) and isfunction(locals.get(k)), locals.keys()
    )
    output = {}

    for cmd_func in commands:
        cmd_name = cmd_func[len(prefix) :]
        cmd_help = locals.get(cmd_func).__doc__
        output[cmd_name] = cmd_help

    print(json.dumps(output))


def log(message: str, level: int) -> None:
    """Print the messages to the stdout."""
    # FIXME: not ready yet.
