"""Pre-defined commands for cli."""
import textwrap
from pathlib import Path
from typing import List, Optional

from dosh.commands.base import CommandResult, CommandStatus, Task


def init_config(config_path: Path) -> CommandResult[None]:
    """Initialize dosh config in the current working directory."""
    if config_path.exists():
        return CommandResult(
            CommandStatus.ERROR,
            message=f"The file `{config_path.name}` already exists in current working directory.",
        )

    content = textwrap.dedent(
        """\
    def cmd_install_apps():
        info("install your favourite apps with a command.")

    def cmd_set_theme(profile):
        info("change your editor, terminal, or system theme with a command.")
    """
    )

    config_path.write_text(content)
    return CommandResult(
        CommandStatus.OK, message=f"The file `{config_path.name}` is created."
    )


def generate_help(
    tasks: List[Task],
    description: Optional[str] = None,
    epilog: Optional[str] = None,
) -> str:
    """Generate a help output looking at available commands."""
    line_len = 79
    lines = []

    # DESCRIPTION
    if description is not None:
        lines.append(description)

    # TASKS
    if tasks:
        lines.extend(["", "Tasks:"])

        task_names = [t.name for t in tasks]
        max_len = min(max(map(len, task_names)), line_len)

        for task in tasks:
            command_init = f"  > {task.name.ljust(max_len)}"
            desc_first, *desc_list = task.description.split("\n")

            if not desc_first:
                lines.append(command_init)
                continue

            line_first, *line_list = textwrap.wrap(desc_first, line_len - max_len)
            lines.append(f"{command_init}   {line_first}")
            lines.extend(map(lambda l: f"{' ' * (max_len + 7)}{l}", line_list))

            for desc in desc_list:
                line_list = textwrap.wrap(desc, line_len - max_len)
                lines.extend(map(lambda l: f"{' ' * (max_len + 7)}{l}", line_list))

    # DOSH COMMANDS
    lines.extend(
        [
            "",
            "Dosh commands:",
            "  > help   print this output",
            "  > init   initialize a new config in current working directory",
        ]
    )

    # EPILOG
    if epilog:
        lines.extend(["", epilog])

    return "\n".join(lines)
