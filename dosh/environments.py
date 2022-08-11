"""Pre-defined environment variables."""
from __future__ import annotations

import getpass
import os
from typing import Final

from dosh.commands import CommandStatus

__all__ = ["ENVIRONMENTS"]


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
