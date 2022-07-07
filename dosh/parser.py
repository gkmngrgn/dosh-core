"""DOSH config parser."""

import json
from contextlib import redirect_stdout
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Any, Dict, Final, Optional

CONFIG_FILENAME: Final = "dosh.star"


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


@dataclass
class ConfigParser:
    """Dosh configuration parser."""

    content: Optional[str]

    def get_commands(self) -> Dict[str, str]:
        """Parse commands from dosh configuration."""
        f = StringIO()

        content = self.content or ""
        content += "\n".join(["locals = locals().copy()", "print_commands(locals)"])

        with redirect_stdout(f):
            exec(content, {"print_commands": inject_print_commands})

        output = f.getvalue()
        data: Dict[str, str] = json.loads(output)
        return data


def find_config_file() -> Path:
    """
    Return file path of dosh script.

    TODO: Improve this function to find the file in a different folder.
    """
    return Path.cwd() / CONFIG_FILENAME


def get_config_parser() -> ConfigParser:
    """Create ConfigParser instance with required parameters."""
    config_file = find_config_file()
    if config_file.exists():
        content = config_file.read_text()
    else:
        content = None

    return ConfigParser(content)
