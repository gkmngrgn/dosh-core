"""Pre-defined environment variables."""
import os
from typing import Final

HOME: Final = os.getenv("HOME")

SHELL: Final = os.getenv("SHELL")
IS_ZSH: Final = SHELL == "zsh"
IS_BASH: Final = SHELL == "bash"
IS_PWSH: Final = SHELL == "pwsh"

OSTYPE: Final = os.getenv("OSTYPE")
IS_LINUX: Final = OSTYPE == "linux"
IS_MACOS: Final = OSTYPE.startswith("darwin")
IS_WINDOWS: Final = OSTYPE == "msys"
