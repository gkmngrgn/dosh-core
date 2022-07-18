"""Pre-defined environment variables."""
import os
from typing import Final

HOME: Final = os.getenv("HOME")
OSTYPE: Final = os.getenv("OSTYPE")
SHELL: Final = os.getenv("SHELL")
