"""DOSH config parser."""
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
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        lua_code = f"function (env, cmd) {content} return env end"
        lua_func = self.lua.eval(lua_code)

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
            if task.name != task_name:
                continue

            if (
                task.environments is not None
                and ENVIRONMENTS["DOSH_ENV"] not in task.environments
            ):
                msg = f"This task works on these environments: {', '.join(task.environments)}"
                self.lua.eval(f'error("{msg}")')
                break

            task.command(*params)
            break

    def add_task(self, args: Dict[str, Any]) -> None:
        """Parse and add task to task list."""
        envs = args["environments"]
        args["environments"] = None if envs is None else list(envs.values())
        task = Task.from_dict(args)
        self.tasks.append(task)
