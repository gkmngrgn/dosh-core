"""DOSH CLI app."""
import sys
from pathlib import Path
from typing import Final, List, Optional, Tuple

from dosh.commands.base import CommandStatus
from dosh.commands.internal import generate_help, init_config
from dosh.config import CONFIG_FILENAME, ConfigParser
from dosh.logger import set_verbosity

PREDEFINED_TASKS: Final = ["help", "init"]


class ArgumentParser:
    """CLI Argument parser."""

    def __find_arg_index(self, *args: str) -> Optional[int]:
        """Parse CLI arguments and return the index of expected arg."""
        index: Optional[int] = None
        for i, arg in enumerate(sys.argv):
            if arg in args:
                index = i
                break
        return index

    def get_verbosity_level(self) -> int:
        """Get verbosity level."""
        index = self.__find_arg_index("-v", "-vv", "-vvv", "--verbose")

        if index is not None:
            arg = sys.argv[index]
            if arg.startswith("-v"):
                return arg.count("v")

            if arg == "--verbose" and len(sys.argv) > index + 1:
                level = sys.argv[index + 1]
                if level.isdigit():
                    return int(level)

        return 2  # default verbosity level.

    def get_config_path(self) -> Path:
        """Return file path of dosh script."""
        index = self.__find_arg_index("-c", "--config")
        if (
            index is None
            or len(sys.argv) <= index
            or sys.argv[index + 1].startswith("-")
        ):
            filename = CONFIG_FILENAME
        else:
            filename = sys.argv[index + 1]

        return Path.cwd() / filename

    def get_task_param(self, tasks: List[str]) -> Tuple[str, List[str]]:
        """Get task name with its parameters."""
        tasks += PREDEFINED_TASKS
        task_index = self.__find_arg_index(*tasks)
        if task_index is None:
            return ("help", [])
        return sys.argv[task_index], sys.argv[task_index + 1 :]


class CLI:
    """DOSH command line interface."""

    def __init__(self) -> None:
        """Initialize cli with config parser."""
        self.arg_parser = ArgumentParser()

        config_path = self.arg_parser.get_config_path()
        content = config_path.read_text() if config_path.exists() else ""
        self.conf_parser = ConfigParser(content)

    def run(self) -> None:
        """Run cli reading the arguments."""
        set_verbosity(verbosity=self.arg_parser.get_verbosity_level())

        tasks = [t.name for t in self.conf_parser.tasks]
        task_name, task_params = self.arg_parser.get_task_param(tasks)

        if task_name == "init":
            self.run_init()
        elif task_name == "help":
            self.run_help()
        else:
            self.conf_parser.run_task(task_name, task_params)

    def run_init(self) -> None:
        """Create new config."""
        result = init_config(self.arg_parser.get_config_path())
        if result.status == CommandStatus.OK:
            print(result.message)
        elif result.status == CommandStatus.ERROR:
            print(result.message, file=sys.stderr)

    def run_help(self) -> None:
        """Print help output."""
        output = generate_help(
            tasks=self.conf_parser.tasks,
            description=self.conf_parser.description,
            epilog=self.conf_parser.epilog,
        )
        print(output)
