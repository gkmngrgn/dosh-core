"""Help output generator."""
import textwrap
from typing import Dict


def generate_help(commands: Dict[str, str]) -> str:
    """Generate a help output looking at available commands."""
    line_len = 79
    max_len = min(max(map(len, commands.keys())), line_len)
    lines = ["Tasks:"]

    for name, desc in commands.items():
        desc_first, *desc_list = desc.split("\n")
        line_first, *line_list = textwrap.wrap(desc_first, line_len - max_len)
        lines.append(f"  > {name.ljust(max_len)}   {line_first}")
        lines.extend(map(lambda l: f"{' ' * (max_len + 7)}{l}", line_list))

        for desc in desc_list:
            line_list = textwrap.wrap(desc, line_len - max_len)
            lines.extend(map(lambda l: f"{' ' * (max_len + 7)}{l}", line_list))

    return "\n".join(lines)
