"""DOSH config parser."""
import shutil
from typing import Any, Dict, Final, List

from lupa import LuaRuntime

from dosh.commands import COMMANDS
from dosh.commands.base import Task
from dosh.environments import ENVIRONMENTS
from dosh.logger import get_logger

CONFIG_FILENAME: Final = "dosh.lua"

logger = get_logger()


class ConfigParser:
    """Dosh configuration parser."""

    tasks: List[Task] = []
    _vars: Dict[str, str] = {}

    def __init__(self, content: str) -> None:
        """Parse config first."""
        commands = COMMANDS.copy()
        commands["add_task"] = self.add_task

        lua = LuaRuntime(unpack_returned_tuples=True)
        lua_code = f"function (env, cmd) {content} return env end"
        lua_func = lua.eval(lua_code)

        self._vars = lua_func(ENVIRONMENTS, commands)

    @property
    def description(self) -> str:
        """Get help description."""
        return self._vars["HELP_DESCRIPTION"]

    @property
    def epilog(self) -> str:
        """Get help epilog."""
        return self._vars["HELP_EPILOG"]

    def run_task(self, task_name: str, params: List[str]) -> None:
        """Find and run tasks with parameters."""
        task = None
        for current_task in self.tasks:
            if current_task.name == task_name:
                task = current_task
                break

        if task is None:
            return

        if (
            task.environments is not None
            and ENVIRONMENTS["DOSH_ENV"] not in task.environments
        ):
            logger.error(
                "This task works only in these environments: %s",
                ", ".join(task.environments),
            )
            return

        for command in task.required_commands or []:
            if shutil.which(command) is None:
                logger.error("The command `%s` doesn't exist in this system.", command)
                return

        try:
            task.command(*params)
        except KeyboardInterrupt:
            print("\r", end="")
            logger.error("keyboard interrupt...")

    def add_task(self, args: Dict[str, Any]) -> None:
        """Parse and add task to task list."""
        for list_key in ["environments", "required_commands"]:
            val = args[list_key]
            args[list_key] = None if val is None else list(val.values())

        task = Task.from_dict(args)
        self.tasks.append(task)
