"""DOSH CLI app."""
import sys
from typing import List, Optional, Tuple

from dosh.help import generate_help
from dosh.logger import set_verbosity
from dosh.parser import get_config_parser


class CLI:
    """DOSH command line interface."""

    def __init__(self) -> None:
        """Initialize cli with config parser."""
        self.conf_parser = get_config_parser()

    def get_arg_verbosity(self) -> int:
        """Get verbosity level."""
        for arg in filter(lambda a: a.startswith("-v"), sys.argv):
            v_count = arg.count("v")
            if len(arg) == v_count + 1:
                return v_count - 1
        return 2  # default verbosity level.

    def get_arg_task(self) -> Optional[Tuple[str, List[str]]]:
        """Get task name with its parameters."""
        args = list(filter(lambda a: not a.startswith("-"), sys.argv))

        if len(args) <= 1:
            return None

        return args[1], args[2:]

    def config_exists(self) -> bool:
        """Return dosh configuration file existency."""
        return self.conf_parser.content is not None

    def initialize_config(self) -> None:
        """Create a simple dosh config for a new project."""
        ...

    def run_task(self, task: str, params: List[str]) -> None:
        """Run task that defined by client."""
        self.conf_parser.run_script([f"cmd_{task}({', '.join(params)})"])

    def run(self) -> None:
        """Run cli reading the arguments."""
        verbosity = self.get_arg_verbosity()
        set_verbosity(verbosity=verbosity)

        task = self.get_arg_task()
        if task is None:
            output = generate_help(
                commands=self.conf_parser.get_commands(),
                description=self.conf_parser.get_description(),
                epilog=self.conf_parser.get_epilog(),
            )
            print(output)
            return

        task_name, task_params = task

        if task_name == "init":
            self.initialize_config()
            return

        self.run_task(task_name, task_params)


def run() -> None:
    """Run command line interface app."""
    cli = CLI()

    if cli.config_exists():
        cli.run()
    else:
        print("Config file doesn't exist.")
