"""DOSH config parser."""
import builtins
import json
import logging
from contextlib import redirect_stdout
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Any, Dict, Final, List, Optional

from dosh import commands as cmd
from dosh import environments as env
from dosh import injections as injects

CONFIG_FILENAME: Final = "dosh.star"
GLOBALS: Final = {
    "__builtins__": builtins,  # TODO: remove unused builtins here.
}
COMMANDS: Final = {
    "eval": cmd.eval,
    "eval_url": cmd.eval_url,
    # package managers
    "apt_install": cmd.apt_install,
    "brew_install": cmd.brew_install,
    "winget_install": cmd.winget_install,
    # file system
    "copy": cmd.copy,
    "exists": cmd.exists,
    "exists_command": cmd.exists_command,
    "path": cmd.path,
    "path_home": lambda p: cmd.path(f"{env.HOME}/{p}"),
    # logging
    "debug": lambda m: cmd.logger.log(logging.DEBUG, m),
    "info": lambda m: cmd.logger.log(logging.INFO, m),
    "warning": lambda m: cmd.logger.log(logging.WARNING, m),
    "error": lambda m: cmd.logger.log(logging.ERROR, m),
}
ENVIRONMENTS: Final = {
    # shell type
    "IS_ZSH": env.SHELL == "zsh",
    "IS_BASH": env.SHELL == "bash",
    "IS_PWSH": env.SHELL == "pwsh",
    # os type
    "IS_MACOS": env.OSTYPE.startswith("darwin"),
    "IS_LINUX": env.OSTYPE == "linux",
    "IS_WINDOWS": env.OSTYPE == "msys",
}


@dataclass
class ConfigParser:
    """Dosh configuration parser."""

    content: Optional[str]

    def get_commands(self) -> Dict[str, str]:
        """Parse commands from dosh configuration."""
        output = self.run_script(
            commands=[
                "locals = locals().copy()",
                "print_commands(locals)",
            ],
            locals={
                "print_commands": injects.print_commands,
            },
        )

        data: Dict[str, str] = json.loads(output)
        return data

    def run_script(self, commands: List[str], locals: Dict[str, Any] = {}) -> str:
        """Run dosh script manipulating the content."""
        output = StringIO()
        content = (self.content or "") + "\n".join(commands)

        locals.update(COMMANDS)
        locals.update(ENVIRONMENTS)

        with redirect_stdout(output):
            exec(content, GLOBALS, locals)

        return output.getvalue()

    def run_command(self, command: str) -> str:
        """Run command if the command exists or return error."""
        return self.run_script([f"cmd_{command}()"])


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
