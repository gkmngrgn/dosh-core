"""Pre-defined environment variables."""
from __future__ import annotations

import getpass
import os
from typing import Final

from dosh.commands.base import CommandStatus, OperatingSystem

__all__ = ["ENVIRONMENTS"]

SHELL: Final = os.getenv("SHELL") or ""
CURRENT_OS: Final = OperatingSystem.get_current()

ENVIRONMENTS: Final = {
    "USER": getpass.getuser(),
    "HELP_DESCRIPTION": "dosh - shell-independent task manager",
    "HELP_EPILOG": "",
    "DOSH_ENV": os.getenv("DOSH_ENV") or "",
    # shell type
    "IS_ZSH": SHELL.endswith("zsh"),
    "IS_BASH": SHELL.endswith("bash"),
    "IS_PWSH": SHELL.endswith("pwsh"),
    # os type
    "IS_MACOS": CURRENT_OS == OperatingSystem.MACOS,
    "IS_LINUX": CURRENT_OS == OperatingSystem.LINUX,
    "IS_WINDOWS": CURRENT_OS == OperatingSystem.WINDOWS,
    # command statuses
    "STATUS_OK": CommandStatus.OK,
    "STATUS_ERROR": CommandStatus.ERROR,
}
