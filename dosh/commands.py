"""Available commands for `dosh.star`."""
import json
import os
import subprocess
from pathlib import Path
from subprocess import CompletedProcess
from typing import Any, Dict, List


def brew_install(*packages: List[str]) -> None:
    # FIXME: not ready yet.
    pass


def brew_tap(*repos: List[str]) -> None:
    # FIXME: not ready yet.
    pass


def copy(source: str, destination: str) -> None:
    # FIXME: not ready yet.
    pass


def clone(url: str, folder: str = ".", sync: bool = False) -> None:
    # FIXME: not ready yet.
    pass


def env(key: str) -> str:
    """Return an OS environment."""
    return os.getenv(key) or ""


def eval(command: str) -> CompletedProcess[bytes]:
    """Run a shell command using subprocess."""
    return subprocess.run(command.split(), capture_output=True)


def eval_url(url: str) -> CompletedProcess[bytes]:
    # FIXME: not ready yet.
    pass


def exists(path: str) -> bool:
    # FIXME: not ready yet.
    pass


def exists_command(command: str) -> bool:
    # FIXME: not ready yet.
    pass


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
    # FIXME: not ready yet.
    pass
