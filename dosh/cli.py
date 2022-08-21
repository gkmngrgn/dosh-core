"""DOSH CLI app."""
import sys
from typing import List, Optional, Tuple

from dosh.commands.base import CommandStatus
from dosh.commands.internal import generate_help, init_config
from dosh.logger import set_verbosity
from dosh.parser import find_config_file, get_config_parser


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

    def run_task(self, task: str, params: List[str]) -> None:
        """Run task that defined by client."""
        self.conf_parser.run_script([f"cmd_{task}({', '.join(params)})"])

    def run(self) -> None:
        """Run cli reading the arguments."""
        verbosity = self.get_arg_verbosity()
        set_verbosity(verbosity=verbosity)

        task_name, task_params = self.get_arg_task() or ("help", [])

        if task_name == "init":
            result = init_config(find_config_file())
            if result.status == CommandStatus.OK:
                print(result.message)
            elif result.status == CommandStatus.ERROR:
                print(result.message, file=sys.stderr)
            return

        if task_name == "help":
            output = generate_help(
                commands=self.conf_parser.get_commands(),
                description=self.conf_parser.get_description(),
                epilog=self.conf_parser.get_epilog(),
            )
            print(output)
            return

        self.run_task(task_name, task_params)


def run() -> None:
    """Run command line interface app."""
    CLI().run()
