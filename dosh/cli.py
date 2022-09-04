"""DOSH CLI app."""
import sys
from typing import List, Optional, Tuple

from dosh.arguments import find_arg_index
from dosh.commands.base import CommandStatus
from dosh.commands.internal import generate_help, init_config
from dosh.config import find_config_file, get_config_parser
from dosh.logger import set_verbosity

PREDEFINED_TASKS = ["help", "init"]


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
        tasks = [t.name for t in self.conf_parser.tasks] + PREDEFINED_TASKS
        task_index = find_arg_index(*tasks)
        if task_index is None:
            return None
        return sys.argv[task_index], sys.argv[task_index + 1 :]

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
                tasks=self.conf_parser.tasks,
                description=self.conf_parser.description,
                epilog=self.conf_parser.epilog,
            )
            print(output)
            return

        self.conf_parser.run_task(task_name, task_params)


def run() -> None:
    """Run command line interface app."""
    CLI().run()
