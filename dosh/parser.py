"""DOSH config parser."""
import json
from contextlib import redirect_stdout
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Any, Dict, Final, List, Optional

from dosh import injections as injects
from dosh.commands import COMMANDS
from dosh.environments import ENVIRONMENTS

CONFIG_FILENAME: Final = "dosh.star"


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
            variables={
                "print_commands": injects.print_commands,
            },
        )

        data: Dict[str, str] = json.loads(output)
        return data

    def get_description(self) -> str:
        """Get help description."""
        output = self.run_script(commands=["print(HELP_DESCRIPTION)"])
        return output.strip()

    def get_epilog(self) -> str:
        """Get help epilog."""
        output = self.run_script(commands=["print(HELP_EPILOG)"])
        return output.strip()

    def run_script(
        self, commands: List[str], variables: Optional[Dict[str, Any]] = None
    ) -> str:
        """Run dosh script manipulating the content."""
        output = StringIO()
        content = (self.content or "") + "\n".join(commands)

        variables = variables or {}
        variables.update(COMMANDS)
        variables.update(ENVIRONMENTS)

        with redirect_stdout(output):
            exec(content, variables)  # pylint: disable=exec-used

        return output.getvalue()


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
