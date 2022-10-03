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
        r"""local name = "there"                         -- you can use all features of Lua programming language.

            local function hello(there)                  -- even you can define your custom functions.
                there = there or name
                local message = "Hello, " .. there .. "!"
                cmd.run("osascript -e 'display notification \"" .. message .. "\" with title \"Hi!\"'")
            end

            cmd.add_task{                                -- cmd comes from dosh.
               name="hello",                             -- task name, or subcommand for your cli.
               description="say hello",                  -- task description for the help output.
               required_commands={"osascript"},          -- check if the programs exist before running the task.
               environments={"development", "staging"},  -- DOSH_ENV variable should be either development or staging to run this task.
               command=hello                             -- run hello function with its parameters when the task ran.
            }
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
    else:
        lines.extend(
            [
                "",
                "There's no task.",
                "Create a file `dosh.lua` and write your tasks first.",
            ]
        )

    # DOSH COMMANDS
    lines.extend(
        [
            "",
            "Dosh commands:",
            "  > help                 print this output",
            "  > init                 initialize a new config in current working directory",
            "",
            "  -c, --config PATH      specify config path (default: dosh.lua)",
            "  -v|vv|vvv, --verbose   increase the verbosity of messages:",
            "                         1 - default, 2 - detailed, 3 - debug",
        ]
    )

    # EPILOG
    if epilog:
        lines.extend(["", epilog])

    return "\n".join(lines)
