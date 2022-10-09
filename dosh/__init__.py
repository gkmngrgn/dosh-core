"""DOSH module."""
from pathlib import Path


class DoshInitializer:  # pylint: disable=too-few-public-methods
    """Pre-configured dosh initializer to store app-specific settings."""

    base_directory: Path = Path.cwd()
    config_path: Path = Path.cwd() / "dosh.lua"
