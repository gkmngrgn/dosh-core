"""DOSH module."""
import importlib.metadata
from pathlib import Path

__version__ = importlib.metadata.version(__package__ or __name__)


class DoshInitializer:  # pylint: disable=too-few-public-methods
    """Pre-configured dosh initializer to store app-specific settings."""

    base_directory: Path = Path.cwd()
    config_path: Path = Path.cwd() / "dosh.lua"
