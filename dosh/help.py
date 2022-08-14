"""Help output generator."""
import textwrap
from typing import Dict, Optional


def generate_help(
    commands: Dict[str, str],
    description: Optional[str] = None,
    epilog: Optional[str] = None,
) -> str:
    """Generate a help output looking at available commands."""
    line_len = 79
    max_len = min(max(map(len, commands.keys())), line_len)
    lines = []

    # DESCRIPTION
    if description is not None:
        lines.extend([description, ""])

    # TASKS
    lines.append("Tasks:")

    for name, desc in commands.items():
        command_init = f"  > {name.ljust(max_len)}"
        desc_first, *desc_list = desc.split("\n")

        if not desc_first:
            lines.append(command_init)
            continue

        line_first, *line_list = textwrap.wrap(desc_first, line_len - max_len)
        lines.append(f"{command_init}   {line_first}")
        lines.extend(map(lambda l: f"{' ' * (max_len + 7)}{l}", line_list))

        for desc in desc_list:
            line_list = textwrap.wrap(desc, line_len - max_len)
            lines.extend(map(lambda l: f"{' ' * (max_len + 7)}{l}", line_list))

    # EPILOG
    if epilog:
        lines.extend(["", epilog])

    return "\n".join(lines)
