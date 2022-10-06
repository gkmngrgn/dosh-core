"""DOSH module."""


from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class DoshInitializer:
    """Singleton class to store app-specific settings."""

    base_directory: Path
    config_path: Path

    def update(
        self, base_directory: Optional[Path], config_path: Optional[Path]
    ) -> None:
        """Update initializer config."""
        if base_directory is not None:
            self.base_directory = base_directory

        if config_path is not None:
            self.config_path = config_path


dosh_initializer = DoshInitializer(
    base_directory=Path.cwd(),
    config_path=Path.cwd() / "dosh.lua",
)
