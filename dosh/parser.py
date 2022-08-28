"""DOSH config parser."""
from pathlib import Path
from typing import Any, Dict, Final, List

from lupa import LuaRuntime

from dosh.commands import COMMANDS
from dosh.commands.base import Task
from dosh.environments import ENVIRONMENTS

CONFIG_FILENAME: Final = "dosh.lua"


class ConfigParser:
    """Dosh configuration parser."""

    tasks: List[Task] = []
    _vars: Dict[str, str] = {}

    def __init__(self, content: str) -> None:
        """Parse config first."""
        lua = LuaRuntime(unpack_returned_tuples=True)
        lua_code = f"function (env, cmd) {content} return env end"
        lua_func = lua.eval(lua_code)

        commands = COMMANDS.copy()
        commands["add_task"] = self.add_task

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
        for task in self.tasks:
            if task.name == task_name:
                task.command(*params)
                return

    def add_task(self, args: Dict[str, Any]) -> None:
        """Parse and add task to task list."""
        task = Task.from_dict(args)
        self.tasks.append(task)


def find_config_file() -> Path:
    """
    Return file path of dosh script.

    TODO: Improve this function to find the file in a different folder.
    """
    return Path.cwd() / CONFIG_FILENAME


def get_config_parser() -> ConfigParser:
    """Create ConfigParser instance with required parameters."""
    config_file = find_config_file()
    content = config_file.read_text() if config_file.exists() else ""
    return ConfigParser(content)
