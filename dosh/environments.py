"""Pre-defined environment variables."""
import getpass
import os
from enum import Enum
from typing import Final

from dosh.commands import CommandStatus

__all__ = ["ENVIRONMENTS"]


class Environment(Enum):
    """Pre-defined environments."""

    # FIXME: allow client to define it in `dosh.star`.
    development = "dev"
    test = "test"
    staging = "stag"
    production = "prod"

    @classmethod
    def get_current_environment(cls) -> "Environment":
        """Return current environment."""
        # FIXME: check env $ENV or dosh --env parameter here.
        return cls.development


ENV: Final = Environment.get_current_environment()
SHELL: Final = os.getenv("SHELL")
OSTYPE: Final = os.getenv("OSTYPE") or ""
ENVIRONMENTS: Final = {
    "USER": getpass.getuser(),
    # shell type
    "IS_ZSH": SHELL == "zsh",
    "IS_BASH": SHELL == "bash",
    "IS_PWSH": SHELL == "pwsh",
    # os type
    "IS_MACOS": OSTYPE.startswith("darwin"),
    "IS_LINUX": OSTYPE == "linux",
    "IS_WINDOWS": OSTYPE == "msys",
    # command statuses
    "STATUS_OK": CommandStatus.OK,
    "STATUS_ERROR": CommandStatus.ERROR,
}
