"""Available commands for `dosh.star`."""

import json
import os
import subprocess
from typing import Any, Dict


def env(key: str) -> str:
    """Return an OS environment."""
    return os.getenv(key) or ""


def eval(command: str) -> None:
    """Run a shell command using subprocess."""
    subprocess.run(command.split(), shell=True)


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
