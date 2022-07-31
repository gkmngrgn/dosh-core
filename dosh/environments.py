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


HOME: Final = os.getenv("HOME") or ""
ENV: Final = Environment.get_current_environment()

SHELL: Final = os.getenv("SHELL")
OSTYPE: Final = os.getenv("OSTYPE") or ""
