"""Help output generator."""
from typing import Dict


def generate_help(commands: Dict[str, str]) -> str:
    """Generate a help output looking at available commands."""
    max_len = max(map(len, commands.keys()))
    lines = [
        "Subcommands:",
        *[f"  > {name.ljust(max_len)}   {desc}" for name, desc in commands.items()],
    ]
    return "\n".join(lines)
