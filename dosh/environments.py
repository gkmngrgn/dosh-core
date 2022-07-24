"""Pre-defined environment variables."""
import os
from enum import Enum
from typing import Final


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


HOME: Final = os.getenv("HOME")
ENV: Final = Environment.get_current_environment()

SHELL: Final = os.getenv("SHELL")
IS_ZSH: Final = SHELL == "zsh"
IS_BASH: Final = SHELL == "bash"
IS_PWSH: Final = SHELL == "pwsh"

OSTYPE: Final = os.getenv("OSTYPE") or ""
IS_LINUX: Final = OSTYPE == "linux"
IS_MACOS: Final = OSTYPE.startswith("darwin")
IS_WINDOWS: Final = OSTYPE == "msys"
